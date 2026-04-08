# Complete Project Index & Navigation Guide

Welcome to the **Document Q&A Chatbot REST API**! This file helps you navigate all project resources.

## START HERE - Read These First!

### For Complete Beginners (Copy-Paste Commands)
👉 **Start Here:** [QUICK_START.md](QUICK_START.md) - Get running in 5 minutes with copy-paste commands

### For Step-by-Step Learning (With Explanations)
👉 **Then Read:** [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed guide with explanations for each step

## 📖 Complete Documentation Map

### 📍 Setup & Getting Started (START HERE!)
| Document | Purpose | Time | Best For |
|----------|---------|------|----------|
| [QUICK_START.md](QUICK_START.md) | Copy-paste 5 steps | ⏱️ 5 min | "Just run it" |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Full step-by-step guide | ⏱️ 15 min | "Explain each step" |

### 📚 Complete Reference & Learning (After Setup Works)
| Document | Purpose | For Whom |
|----------|---------|----------|
| [README.md](README.md) | Complete feature docs | Everyone |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & internals | Developers |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project stats & overview | Quick reference |
| [TESTING.md](TESTING.md) | Testing & validation | QA/Testing |
| [POSTMAN_COLLECTION.md](POSTMAN_COLLECTION.md) | API testing guide | API users |

## 🛠️ Setup Instructions

### Option 1: Quick Local Setup (Recommended)
```bash
# 1. Run setup script
bash setup.sh

# 2. Add your Gemini API key
nano .env
# Add: GEMINI_API_KEY=your_key_here

# 3. Start server
python -m uvicorn app.main:app --reload

# Server will run at: http://localhost:8000
```



### Option 3: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add OPENAI_API_KEY

# Run server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Project Structure Overview

```
Core Application (app/)
├── main.py              ← FastAPI app entry point
├── config.py            ← Configuration/settings
├── routers/             ← API endpoints
│   ├── upload.py        ← Document upload endpoint
│   └── query.py         ← Question answering endpoint
├── services/            ← Business logic
│   ├── document_service.py    ← Document processing
│   ├── embedding_service.py   ← OpenAI embeddings
│   ├── vector_store.py        ← FAISS vector database
│   └── rag_service.py         ← RAG (retrieval + LLM)
├── models/              ← Data schemas
│   └── schemas.py       ← Request/response models
└── utils/               ← Utility functions
    ├── logger.py        ← Logging setup
    ├── file_handler.py  ← File operations
    ├── text_processor.py ← Text chunking
    └── document_parser.py ← PDF/TXT parsing

Data Storage (data/)
├── uploads/             ← Uploaded documents
└── vector_store/        ← FAISS indexes & metadata

Scripts
├── setup.sh             ← One-time setup
├── examples.sh          ← API usage examples
└── client_example.py    ← Python client code

Documentation
├── README.md            ← Full documentation
├── QUICKSTART.md        ← 5-minute guide
├── ARCHITECTURE.md      ← System design

├── TESTING.md          ← Testing guide
├── POSTMAN_COLLECTION.md ← API testing
└── PROJECT_SUMMARY.md  ← Project overview
```

## 📡 API Endpoints

### Health & Info
```bash
GET  /health                      # Health check
GET  /                            # API info & endpoints
GET  /docs                        # Swagger UI
GET  /redoc                       # ReDoc documentation
```

### Document Management
```bash
POST   /api/upload                # Upload document
GET    /api/documents/{id}        # Get document info
DELETE /api/documents/{id}        # Delete document
```

### Question Answering
```bash
POST   /api/query                 # Ask question & get answer
```

### Example Requests
```bash
# Upload
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.pdf"

# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?", "document_id": "..."}'
```

## 🧪 Testing & Validation

### Run Example Script
```bash
bash examples.sh        # Full API test suite
```

### Check Health
```bash
curl http://localhost:8000/health
```

### View Logs
```bash
tail -f logs/app.log
```

### Test with Postman
1. Import collection from [POSTMAN_COLLECTION.md](POSTMAN_COLLECTION.md)
2. Set `base_url` to `http://localhost:8000`
3. Run requests in order

## 📋 Configuration

### Required Settings (.env)
```env
GEMINI_API_KEY=your_key_here       # Your Gemini API key (required)
GEMINI_MODEL=gemini-2.5-flash      # LLM to use
```

### Optional Tuning
```env
CHUNK_SIZE=500                     # Tokens per chunk (default: 500)
CHUNK_OVERLAP=100                  # Overlap between chunks (default: 100)
TOP_K_CHUNKS=5                     # Search results to retrieve (default: 5)
MAX_FILE_SIZE=52428800             # Upload limit in bytes (default: 50MB)
DEBUG=false                        # Enable debug mode (default: false)
SIMILARITY_THRESHOLD=0.5           # Min similarity score (default: 0.5)
```

### All Settings
See [README.md](README.md#configuration) for complete configuration guide.

## 🚀 Common Commands

```bash
# Install/Setup
bash setup.sh                      # One-time setup
pip install -r requirements.txt    # Install dependencies

# Development
python -m uvicorn app.main:app --reload  # Run with auto-reload
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000  # Production

# Testing
bash examples.sh                   # Run example requests
python -m pytest tests/            # Run unit tests (if available)



# Cleanup
rm -rf data/uploads/*              # Clear uploaded files
rm -rf data/vector_store/*         # Clear vector indexes
rm -f logs/app.log*                # Clear logs
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
**Solution**: Ensure you're running from project root with activated venv
```bash
cd project_bot
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### "OPENAI_API_KEY not configured"
**Solution**: Check .env file has valid key
```bash
cat .env | grep OPENAI_API_KEY
# Should show: OPENAI_API_KEY=sk-...
```

### "Port 8000 already in use"
**Solution**: Use different port
```bash
python -m uvicorn app.main:app --port 8001
```

### "vector store corrupted"
**Solution**: Regenerate vector store
```bash
rm -rf data/vector_store/
# Re-upload documents to rebuild
```

See [README.md#troubleshooting](README.md#troubleshooting) for more solutions.

## 📈 Performance Optimization

### Faster Responses
```env
OPENAI_MODEL=gpt-3.5-turbo         # Use cheaper, faster model
CHUNK_SIZE=300                     # Smaller chunks = faster search
TOP_K_CHUNKS=3                     # Return fewer results
```

### Better Accuracy
```env
CHUNK_SIZE=750                     # Larger chunks = more context
TOP_K_CHUNKS=10                    # More results to choose from
OPENAI_MODEL=gpt-4                 # More capable model
```

## 💡 Tips & Tricks

### 1. Create Sample Document
```bash
cat > sample.txt << 'EOF'
Your document content here.
Multiple paragraphs work best.
The system will chunk it intelligently.
EOF

curl -X POST http://localhost:8000/api/upload -F "file=@sample.txt"
```

### 2. Save Document ID for Later
```bash
DOC_ID=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@doc.pdf" | jq -r '.document_id')
echo $DOC_ID  # Use this for queries
```

### 3. Batch Upload Multiple Files
```bash
for file in *.pdf; do
  curl -X POST http://localhost:8000/api/upload -F "file=@$file"
done
```

### 4. Monitor Vector Store Size
```bash
du -sh data/vector_store/
```

## 🎓 Learning Resources

### Understanding the System
1. Start with [QUICKSTART.md](QUICKSTART.md) - 5 min overview
2. Read [README.md](README.md) - Full feature guide
3. Study [ARCHITECTURE.md](ARCHITECTURE.md) - System design
4. Review [app/main.py](app/main.py) - Entry point

### Understanding RAG
- This uses **Retrieval-Augmented Generation** pattern
- Upload → Chunk → Embed → Store (FAISS)
- Query → Embed → Search → Pass to LLM → Answer
- See [ARCHITECTURE.md#data-flow](ARCHITECTURE.md#data-flow) for diagrams

### Understanding FAISS
- FAISS = Facebook AI Similarity Search
- Indexes vectors and finds similar ones efficiently
- Uses L2 distance for similarity
- See [vector_store.py](app/services/vector_store.py) for implementation

### Understanding FastAPI
- Modern Python web framework
- Auto-validates requests with Pydantic
- Auto-generates API docs (Swagger)
- See [main.py](app/main.py) and [routers/](app/routers/) for examples

## 🔐 Security Notes

### For Development
- API currently has no authentication
- CORS is open to all origins
- Debug mode is off by default

### For Production
- ✅ Add authentication (if needed)
- ✅ Use HTTPS/TLS (reverse proxy required)
- ✅ Restrict CORS origins (app/main.py)
- ✅ Add rate limiting (if needed)
- ✅ Store secrets securely (use environment variables)
- ✅ Monitor API usage (OpenAI costs)



## 📊 What's Included

| Component | Status | Location |
|-----------|--------|----------|
| FastAPI app | ✅ Complete | [app/main.py](app/main.py) |
| Upload endpoint | ✅ Complete | [app/routers/upload.py](app/routers/upload.py) |
| Query endpoint | ✅ Complete | [app/routers/query.py](app/routers/query.py) |
| Document processing | ✅ Complete | [app/services/document_service.py](app/services/document_service.py) |
| Embeddings (OpenAI) | ✅ Complete | [app/services/embedding_service.py](app/services/embedding_service.py) |
| Vector store (FAISS) | ✅ Complete | [app/services/vector_store.py](app/services/vector_store.py) |
| RAG/LLM | ✅ Complete | [app/services/rag_service.py](app/services/rag_service.py) |
| Error handling | ✅ Complete | Throughout codebase |
| Logging | ✅ Complete | [app/utils/logger.py](app/utils/logger.py) |
| Swagger docs | ✅ Auto | At `/docs` endpoint |

| Chat history | ⏳ Ready-to-add | See [ARCHITECTURE.md](ARCHITECTURE.md#future-enhancements) |


## 📞 Need Help?

### Check Documentation First
- [QUICKSTART.md](QUICKSTART.md) - Common startup issues
- [README.md](README.md#troubleshooting) - Troubleshooting section
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design questions


### Test with API Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### View Logs
```bash
tail -f logs/app.log
```

---

## Next Steps

1. ✅ You have all the code and documentation
2. 🚀 Run `bash setup.sh` to prepare environment
3. 📝 Add your OpenAI API key to `.env`
4. 🏃 Start the server
5. 🧪 Test with `bash examples.sh`
6. 📖 Read [README.md](README.md) for detailed documentation
7. 🚀 Implement additional features (auth, caching, etc.)

## Enjoy! 🎉

You now have a production-ready Document Q&A API. Happy coding!

For questions or issues, refer to the relevant documentation section above.
