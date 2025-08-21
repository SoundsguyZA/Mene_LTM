import os
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from .db import SessionLocal, Base, engine, init_db
from .models import Memory
from .schemas import EventIn, RecallResponse, MemoryOut, Health
from .embeddings import Embedder
from . import crud
from datetime import datetime, timezone
AUTH_TOKEN=os.getenv("API_AUTH_TOKEN","dev_token_change_me")
app=FastAPI(title="Mene Long-Term Memory (M-LTM)")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
EMBEDDER=Embedder()
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
@app.on_event("startup")
def on_start():
    init_db(); Base.metadata.create_all(bind=engine)
def require_auth(authorization: Optional[str]=Header(None)):
    if not authorization or not authorization.startswith("Bearer "): raise HTTPException(status_code=401, detail="Missing bearer token")
    token=authorization.split(" ",1)[1].strip()
    if token!=AUTH_TOKEN: raise HTTPException(status_code=403, detail="Invalid token")
@app.get("/health", response_model=Health)
def health(_: None=Depends(require_auth)):
    return Health(status="ok", embed_provider=EMBEDDER.provider, embed_model=EMBEDDER.model_name)
@app.post("/event")
def write_event(event: EventIn, _: None=Depends(require_auth), db: Session=Depends(get_db)):
    mem=crud.create_memory(db, EMBEDDER, event.content, event.type, event.tags, event.source or "mene_portal", event.importance, event.summary)
    return {"id": mem.id, "summary": mem.summary}
@app.get("/recall", response_model=RecallResponse)
def recall(q: str, tags: Optional[str]=None, _: None=Depends(require_auth), db: Session=Depends(get_db)):
    tag_list=[t.strip() for t in tags.split(",")] if tags else None
    rows=crud.recall(db, EMBEDDER, q, tag_list); out: List[MemoryOut]=[]
    for r, score in rows:
        mem=db.query(Memory).get(r["id"]); mem.last_accessed=datetime.now(timezone.utc); mem.recall_count=(mem.recall_count or 0)+1; db.commit()
        out.append(MemoryOut(id=r["id"], type=r["type"], content=r["content"], summary=r["summary"], importance=r["importance"],
                             tags=r["tags"] or [], source=r["source"], created_at=r["created_at"], last_accessed=r["last_accessed"],
                             recall_count=r["recall_count"], score=round(score,4)))
    return RecallResponse(query=q, results=out)
@app.post("/reinforce/{mem_id}")
def reinforce(mem_id: int, _: None=Depends(require_auth), db: Session=Depends(get_db)):
    mem=crud.reinforce(db, mem_id); 
    if not mem: raise HTTPException(status_code=404, detail="not found")
    return {"ok": True, "id": mem.id, "decay_weight": mem.decay_weight, "recall_count": mem.recall_count}
@app.post("/forget/{mem_id}")
def forget(mem_id: int, _: None=Depends(require_auth), db: Session=Depends(get_db)):
    ok=crud.forget(db, mem_id); 
    if not ok: raise HTTPException(status_code=404, detail="not found")
    return {"ok": True}
@app.get("/dump")
def dump(_: None=Depends(require_auth), db: Session=Depends(get_db)):
    rows=db.query(Memory).order_by(Memory.created_at.desc()).all()
    return {"count": len(rows), "items": [{"id": m.id, "type": m.type, "content": m.content, "summary": m.summary,
            "importance": m.importance, "tags": m.tags or [], "source": m.source, "created_at": m.created_at,
            "last_accessed": m.last_accessed, "recall_count": m.recall_count} for m in rows]}
