from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
POSTGRES_HOST=os.getenv("POSTGRES_HOST","db")
POSTGRES_PORT=int(os.getenv("POSTGRES_PORT","5432"))
POSTGRES_DB=os.getenv("POSTGRES_DB","mene_mem")
POSTGRES_USER=os.getenv("POSTGRES_USER","mene")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD","change_me")
DATABASE_URL=f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine=create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base=declarative_base()
def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
