from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
class EventIn(BaseModel):
    content: str = Field(..., min_length=1, max_length=8192)
    type: str = Field("episodic", pattern="^(episodic|semantic|procedural|identity|social)$")
    tags: List[str] = []
    source: Optional[str] = "mene_portal"
    importance: int = Field(1, ge=0, le=3)
    summary: Optional[str] = None
class MemoryOut(BaseModel):
    id: int; type: str; content: str; summary: Optional[str]
    importance: int; tags: List[str]; source: Optional[str]
    created_at: datetime; last_accessed: Optional[datetime]
    recall_count: int; score: float
class RecallResponse(BaseModel):
    query: str; results: List[MemoryOut]
class Health(BaseModel):
    status: str; embed_provider: str; embed_model: str
