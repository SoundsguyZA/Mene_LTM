from sqlalchemy import Column, Integer, String, DateTime, Text, ARRAY, Float
from sqlalchemy.dialects.postgresql import VECTOR
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, Optional
from .db import Base
class Memory(Base):
    __tablename__="memories"
    id: Mapped[int]=mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str]=mapped_column(String(32), index=True)
    content: Mapped[str]=mapped_column(Text)
    summary: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    importance: Mapped[int]=mapped_column(Integer, default=1)
    tags: Mapped[Optional[List[str]]]=mapped_column(ARRAY(String), default=list)
    source: Mapped[Optional[str]]=mapped_column(String(64), nullable=True)
    created_at: Mapped=mapped_column(DateTime(timezone=True), server_default=func.now())
    last_accessed: Mapped[Optional]=mapped_column(DateTime(timezone=True), nullable=True)
    recall_count: Mapped[int]=mapped_column(Integer, default=0)
    decay_weight: Mapped[float]=mapped_column(Float, default=1.0)
    embedding=Column(VECTOR(384))
