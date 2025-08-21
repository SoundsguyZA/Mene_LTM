import os, numpy as np
from typing import List
EMBED_PROVIDER=os.getenv("EMBED_PROVIDER","fastembed").lower()
EMBED_MODEL=os.getenv("EMBED_MODEL","BAAI/bge-small-en-v1.5")
class Embedder:
    def __init__(self):
        self.provider=EMBED_PROVIDER; self.model_name=EMBED_MODEL
        if self.provider=="fastembed":
            from fastembed import TextEmbedding
            cache=os.getenv("MODEL_CACHE", os.path.expanduser("~/.cache/mene_ltm")); os.makedirs(cache, exist_ok=True)
            self.model=TextEmbedding(model_name=self.model_name, cache_dir=cache)
            self._dim=len(list(self.model.embed(["dim_probe"]))[0])
        elif self.provider=="openai":
            import httpx
            self.http=httpx.Client(base_url=os.getenv("OPENAI_BASE_URL","https://api.openai.com/v1"),
                                   headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY','')}"})
            self._dim=int(os.getenv("OPENAI_EMBED_DIM","1536"))
        else: raise ValueError(f"Unknown EMBED_PROVIDER: {self.provider}")
    @property
    def dim(self)->int: return self._dim
    def embed(self, texts: List[str])->np.ndarray:
        if self.provider=="fastembed":
            vecs=list(self.model.embed(texts)); return np.array(vecs, dtype="float32")
        else:
            payload={"input": texts, "model": self.model_name}
            r=self.http.post("/embeddings", json=payload, timeout=60); r.raise_for_status()
            data=r.json()["data"]; return np.array([d["embedding"] for d in data], dtype="float32")
