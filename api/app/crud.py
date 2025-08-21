from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Tuple
from .models import Memory
from .embeddings import Embedder
from .utils import time_decay
import os
RECALL_TOP_K=int(os.getenv("RECALL_TOP_K","15"))
IMPORTANCE_BOOST=float(os.getenv("IMPORTANCE_BOOST","0.2"))
RECENCY_HALF_LIFE_DAYS=float(os.getenv("RECENCY_HALF_LIFE_DAYS","14"))
def ensure_vector_dim(db: Session, dim: int): pass
def create_memory(db: Session, embedder: Embedder, content: str, type_: str, tags: list, source: str, importance: int, summary: str|None):
    vec=embedder.embed([content])[0].tolist()
    mem=Memory(type=type_, content=content, summary=summary, importance=importance, tags=tags or [], source=source, embedding=vec)
    db.add(mem); db.commit(); db.refresh(mem); return mem
def recall(db: Session, embedder: Embedder, query: str, tags: list[str]|None=None)->List[Tuple[Memory,float]]:
    qvec=embedder.embed([query])[0]; tag_filter="AND tags && :tags" if tags else ""
    sql=text(f"""
        SELECT id, type, content, summary, importance, tags, source, created_at, last_accessed, recall_count, decay_weight,
               1.0 - (embedding <=> :qvec) AS sim
        FROM memories WHERE embedding IS NOT NULL {tag_filter}
        ORDER BY embedding <=> :qvec LIMIT :k
    """)
    rows=db.execute(sql, {"qvec": qvec.tolist(), "k": RECALL_TOP_K, "tags": tags}).mappings().all()
    results=[]
    for r in rows:
        rec=time_decay(r["created_at"], RECENCY_HALF_LIFE_DAYS)
        imp=(r["importance"] or 0)*IMPORTANCE_BOOST
        tag_bonus=0.15 if (tags and r["tags"]) else 0.0
        score=max(0.0, r["sim"])*0.7 + imp + rec*0.15 + tag_bonus
        results.append((r, score))
    results.sort(key=lambda t: t[1], reverse=True); return results
def reinforce(db: Session, mem_id: int, bonus: float=0.1):
    mem=db.query(Memory).get(mem_id); if not mem: return None
    mem.recall_count=(mem.recall_count or 0)+1; mem.decay_weight=(mem.decay_weight or 1.0)*(1.0+bonus)
    db.commit(); db.refresh(mem); return mem
def forget(db: Session, mem_id: int):
    mem=db.query(Memory).get(mem_id); if not mem: return None
    db.delete(mem); db.commit(); return True
