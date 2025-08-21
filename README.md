# Mene Long-Term Memory (M-LTM) — v0.1

Local, sovereign long-term memory microservice for agents.
- API (FastAPI): /event, /recall, /reinforce, /forget, /dump
- DB: Postgres + pgvector (384-dim)
- Embeddings: BGE-small via FastEmbed (CPU-friendly)

Quick start:
  cp .env.example .env
  docker compose up -d --build
  curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/health
