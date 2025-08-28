# Mene Long-Term Memory (M-LTM) 🧠 v1.0

**Complete RAG-enabled long-term memory system with integrated conversation history and VERITAS AI memory.**

## 🎯 **What This Does**
- **Semantic memory storage** with pgvector embeddings
- **Conversation recall** via natural language queries  
- **Memory reinforcement** and decay algorithms
- **Tagged categorization** for organized retrieval
- **RESTful API** for agent integration
- **Complete ChatGPT conversation history** (Aug 2025)
- **VERITAS AI project archive** (353MB+ in AI Drive)

## 🚀 **Quick Start**
```bash
# Setup environment
cp .env.example .env
# Edit .env with your PostgreSQL and API settings

# Launch system
docker compose up -d --build

# Test authentication 
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/health
```

## 🔌 **API Endpoints**
- **POST /event** - Store new memory
- **GET /recall?q=query&tags=tag1,tag2** - Retrieve relevant memories  
- **POST /reinforce/{id}** - Strengthen memory importance
- **POST /forget/{id}** - Delete memory
- **GET /dump** - Export all memories
- **GET /health** - System status

## 💾 **Data Architecture**
- **Database**: PostgreSQL + pgvector (384-dim embeddings)
- **Embeddings**: BGE-small via FastEmbed (CPU-friendly)
- **Memory Scoring**: Importance + recency + reinforcement
- **Storage**: Docker volumes for persistence

## 📚 **Memory Archives**
### 1. **Mene Chat History (Aug 2025)**
- **CONVERSATION_TOPICS_23-08-25.md** - 152KB of categorized discussions
- **MASTER_INDEX_23-08-25.json** - 179KB of structured metadata
- **36 conversation chunks** (available in AI Drive)
- **Ready for RAG ingestion** via API endpoints

### 2. **VERITAS AI Memory (353MB in AI Drive)**  
- **10 major projects**: Aluna Africa, Black Orchid Indicator, Cake-O-Clock, Truth Button, etc.
- **Audio assets**: 52MB of podcast voices and samples
- **System configs**: AI bridge components
- **Development logs**: Session tracking and project history

## 🏗️ **Tech Stack**
- **FastAPI** - RESTful API server
- **PostgreSQL + pgvector** - Vector database for semantic search
- **BGE-small embeddings** - Semantic similarity via FastEmbed
- **Docker Compose** - Container orchestration
- **CORS enabled** - Web integration ready

## 🔐 **Environment Configuration**
Copy `.env.example` to `.env` and configure:
```bash
# Database
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=mene_ltm
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# API
API_HOST=0.0.0.0
API_PORT=8000
API_AUTH_TOKEN=your_secure_token

# Embeddings
EMBED_PROVIDER=fastembed
EMBED_MODEL=BAAI/bge-small-en-v1.5
MODEL_CACHE=/app/models

# Memory Settings
RECALL_TOP_K=10
IMPORTANCE_BOOST=1.2
RECENCY_HALF_LIFE_DAYS=30
```

## 📊 **Memory Statistics**
- **Total VERITAS Archives**: 197 files, 353MB (AI Drive)
- **ChatGPT Conversation**: 36 chunks, indexed and searchable
- **Audio Library**: 32 files, 52MB of voice assets (AI Drive)
- **Project History**: 134 development files across 10 projects (AI Drive)

## 🛠️ **Development**
```bash
# View logs
docker compose logs -f api

# Access database directly
docker exec -it mene-ltm_db_1 psql -U postgres -d mene_ltm

# Rebuild after changes
docker compose down && docker compose up -d --build
```

## 📱 **Integration Example**
```python
import requests

# Store memory
response = requests.post(
    "http://localhost:8000/event",
    headers={"Authorization": "Bearer YOUR_TOKEN"},
    json={
        "content": "Rob completed the Aluna Africa website project",
        "type": "project_completion", 
        "tags": ["development", "aluna", "website"],
        "importance": 0.9
    }
)

# Recall memories  
response = requests.get(
    "http://localhost:8000/recall?q=Aluna Africa project&tags=development",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
```

## 📂 **File Organization**
- **Code Repository** (GitHub): Core system, docs, conversation indexes
- **AI Drive Storage**: Large binary files (audio, images, videos, PDFs)
- **Local Development**: Docker containers with persistent volumes

## 🚀 **Data Ingestion**
To ingest conversation history into the RAG system:
1. Start the M-LTM system: `docker compose up -d`
2. Use the conversation chunks from AI Drive or GitHub docs
3. POST each chunk to `/event` endpoint with appropriate tags
4. Query memories using `/recall` endpoint

## 🎯 **Deployment Status**
- **Platform**: Docker Compose (local/server)
- **Status**: ✅ Production Ready
- **GitHub**: https://github.com/SoundsguyZA/Mene_LTM
- **Last Updated**: August 28, 2025
- **Version**: v1.0 - Complete memory integration

## 🚀 **Next Steps**
1. **Ingest conversation history** via `/event` API
2. **Deploy to production server** with persistent volumes
3. **Integrate with AI agents** for automatic memory storage
4. **Add web interface** for memory browsing
5. **Implement memory clustering** for topic discovery

---

**Built with 🔥 by VERITAS AI**  
*Living memory for digital minds*

**Truth**: All large binary files (353MB+) remain safely in AI Drive for instant access while keeping GitHub lean and deployable.