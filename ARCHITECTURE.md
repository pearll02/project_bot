# Architecture & Design Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      HTTP Client/Postman                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────┐
        │   FastAPI Application      │
        │   (app/main.py)            │
        └────────────────────────────┘
        
        ↓              ↓              ↓
        
    ┌─────────┐   ┌────────┐   ┌──────────┐
    │ Upload  │   │ Query  │   │Health &  │
    │Router   │   │Router  │   │Info      │
    └────┬────┘   └───┬────┘   └────────┘
         │            │
         ↓            ↓
    ┌────────────────────────────────────────────┐
    │         Document & RAG Services            │
    │  ┌─────────────────────────────────────┐  │
    │  │ Document Service                    │  │
    │  │ - Process documents                 │  │
    │  │ - Extract text                      │  │
    │  │ - Manage document lifecycle         │  │
    │  └─────────────────────────────────────┘  │
    │  ┌─────────────────────────────────────┐  │
    │  │ Embedding Service                   │  │
    │  │ - Generate embeddings via OpenAI    │  │
    │  │ - Batch processing                  │  │
    │  │ - Dimension handling                │  │
    │  └─────────────────────────────────────┘  │
    │  ┌─────────────────────────────────────┐  │
    │  │ RAG Service                         │  │
    │  │ - Semantic search                   │  │
    │  │ - LLM integration                   │  │
    │  │ - Answer generation                 │  │
    │  └─────────────────────────────────────┘  │
    │  ┌─────────────────────────────────────┐  │
    │  │ Vector Store (FAISS)                │  │
    │  │ - Store embeddings                  │  │
    │  │ - Similarity search                 │  │
    │  │ - Metadata management               │  │
    │  └─────────────────────────────────────┘  │
    └────────────────────────────────────────────┘
         │              │              │
         ↓              ↓              ↓
    ┌──────────────────────────────────────────┐
    │         Utility Services                 │
    │  ┌──────────────────────────────────┐   │
    │  │ Text Processor                   │   │
    │  │ - Chunking (500 tokens)          │   │
    │  │ - Overlapping (100 tokens)       │   │
    │  │ - Tokenization                   │   │
    │  └──────────────────────────────────┘   │
    │  ┌──────────────────────────────────┐   │
    │  │ Document Parser                  │   │
    │  │ - PDF extraction                 │   │
    │  │ - Text file handling             │   │
    │  │ - DOCX support                   │   │
    │  └──────────────────────────────────┘   │
    │  ┌──────────────────────────────────┐   │
    │  │ File Handler                     │   │
    │  │ - File validation                │   │
    │  │ - Storage operations             │   │
    │  │ - Cleanup                        │   │
    │  └──────────────────────────────────┘   │
    │  ┌──────────────────────────────────┐   │
    │  │ Logger                           │   │
    │  │ - Application logging            │   │
    │  │ - Rotation & management          │   │
    │  └──────────────────────────────────┘   │
    └──────────────────────────────────────────┘
         │              │              │
         ↓              ↓              ↓
    ┌───────────────────────────────────────────────┐
    │   External Services & Storage                │
    │                                               │
    │  ┌──────────────────────────────────────┐   │
    │  │ OpenAI API                           │   │
    │  │ - GPT-4 for LLM                      │   │
    │  │ - text-embedding-3-small for vectors│   │
    │  └──────────────────────────────────────┘   │
    │                                               │
    │  ┌──────────────────────────────────────┐   │
    │  │ Local File System                    │   │
    │  │ - /data/uploads/ - uploaded files   │   │
    │  │ - /data/vector_store/ - FAISS index │   │
    │  │ - /logs/ - application logs         │   │
    │  └──────────────────────────────────────┘   │
    └───────────────────────────────────────────────┘
```

## Module Structure

### 1. **app/main.py** - FastAPI Application
- Creates and configures FastAPI app
- Sets up CORS middleware
- Registers routers
- Implements exception handling
- Manages application lifecycle

### 2. **app/config.py** - Configuration Management
- Loads environment variables
- Provides settings singleton
- Validates configuration
- Creates required directories

### 3. **app/models/schemas.py** - Data Models
Pydantic models for request/response validation:
- `UploadResponse` - Document upload result
- `QueryRequest` - Question asking request
- `QueryResponse` - QA result with metadata
- `ChatMessage` - Chat message model
- `ChatSession` - Session history

### 4. **app/routers/**
#### upload.py
- `POST /api/upload` - Document upload endpoint
- Integration with DocumentService
- File validation and error handling

#### query.py
- `POST /api/query` - Question answering endpoint
- Integration with RAGService
- Retrieval and generation pipeline

### 5. **app/services/**

#### document_service.py
**Responsibilities:**
- Orchestrate document processing
- Integrate all text processing steps
- Manage document lifecycle
- Store metadata

**Process Flow:**
```
File → Parse → Clean → Chunk → Embed → Store
```

#### embedding_service.py
**Responsibilities:**
- Interface with OpenAI Embeddings API
- Generate embeddings for texts
- Handle batch processing
- Manage model dimensions

**Key Features:**
- Batch processing (100 texts at a time)
- Error handling with fallback
- Model-aware dimension handling

#### vector_store.py (FAISS)
**Responsibilities:**
- Store embeddings in FAISS index
- Perform similarity search
- Manage metadata
- Persist/load store

**Data Structure:**
```python
{
  "index": faiss.IndexFlatL2,  # L2 distance index
  "metadata": {
    0: {"document_id": "...", "chunk_index": 0, "text": "..."},
    1: {"document_id": "...", "chunk_index": 1, "text": "..."}
  }
}
```

#### rag_service.py (RAG/LLM)
**RAG Pipeline:**
```
Question
    ↓
[Embed Question]
    ↓
[Search Vector Store] → Top-K similar chunks
    ↓
[Build Context] → Arrange chunks
    ↓
[Send to LLM] → GPT-4 with system prompt
    ↓
[Generate Answer]
    ↓
Answer + Metadata
```

**Key Constraints:**
- Answer only from context
- Prevent hallucination
- Track confidence scores
- Include source attribution

### 6. **app/utils/**

#### text_processor.py
**Functions:**
- `chunk_text()` - Split by tokens with overlap
- `count_tokens()` - Count using tiktoken
- `clean_text()` - Normalize whitespace

**Chunking Algorithm:**
```
1. Split by paragraphs
2. Accumulate until chunk_size reached
3. Add overlap from previous chunk
4. Repeat for all paragraphs
```

#### document_parser.py
**Supported Formats:**
- PDF: via pdfplumber
- TXT: standard text reading
- DOCX: via python-docx

#### file_handler.py
**Functions:**
- File validation
- Upload handling
- Size checking
- Cleanup

#### logger.py
**Configuration:**
- Two handlers: file + console
- Rotating file logs (10MB max)
- Structured format: timestamp | logger | level | message

## Data Flow

### Document Upload Flow
```
1. User uploads file
   ↓
2. Validate: extension, size
   ↓
3. Read file content
   ↓
4. Extract text (PDF/TXT/DOCX)
   ↓
5. Clean text (normalize whitespace)
   ↓
6. Chunk text (500 tokens + 100 overlap)
   ↓
7. Generate embeddings (OpenAI API)
   ↓
8. Store in FAISS with metadata
   ↓
9. Persist vector store to disk
   ↓
10. Return document_id
```

### Question Answering Flow
```
1. User provides: question + document_id
   ↓
2. Embed question (OpenAI API)
   ↓
3. Search FAISS for top-k similar chunks
   ↓
4. Filter by document_id
   ↓
5. Calculate confidence from similarity scores
   ↓
6. Build context string from chunks
   ↓
7. Send to GPT-4:
   - System prompt: "Answer only from context"
   - Context: retrieved chunks
   - Question: user question
   ↓
8. Receive and return answer
   ↓
9. Include metadata: chunks_used, confidence, sources
```

## Performance Characteristics

### Time Complexity
| Operation | Time |
|-----------|------|
| PDF parsing (5MB) | O(pages) |
| Text chunking | O(tokens) |
| Embedding generation | O(chunks) |
| Vector search | O(log n) |
| LLM answer | O(input_tokens) |

### Space Complexity
| Component | Space |
|-----------|-------|
| FAISS index | ~1KB per 512-dim vector |
| Metadata | ~500B per chunk |
| Total per document | ~1MB per 100 chunks |

### Example: 100-page PDF
- Text size: ~2-3MB
- Chunks created: 20-30
- Embedding vectors: 20-30 × 512 dims
- Storage needed: ~50MB (including metadata)
- Upload time: 2-3 seconds
- Query latency: 5-10 seconds (including LLM latency)

## Design Patterns

### 1. **Service Layer Pattern**
- Services encapsulate business logic
- Controllers (routers) handle HTTP
- Clear separation of concerns

### 2. **Dependency Injection**
- Vector store injected into services
- Easy to mock for testing
- Flexible initialization

### 3. **Configuration Management**
- Environment-based settings
- Singleton pattern for settings
- Easy to override per environment

### 4. **Error Handling**
- Custom exceptions (HTTPException)
- Consistent error responses
- Detailed logging

### 5. **Metadata Pattern**
- Track chunk source and context
- Enable source attribution
- Support provenance tracking

## Extension Points

### Adding New File Formats
```python
# In app/utils/document_parser.py
def extract_text_from_markdown(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()

# In app/utils/file_handler.py
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.md'}  # Add .md
```

### Adding Chat History
```python
# Create database models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    session_id = Column(String, primary_key=True)
    message = Column(String)
    timestamp = Column(DateTime)
```

### Adding Authentication
```python
from fastapi.security import HTTPBearer, HTTPAuthCredential

security = HTTPBearer()

@app.post("/api/upload")
async def upload(credentials: HTTPAuthCredential = Depends(security)):
    verify_token(credentials.credentials)
```

### Adding Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_embedding_cached(text: str):
    return embedding_service.generate_embedding(text)
```

## Testing Strategy

### Unit Tests
```python
# Test text chunking
def test_chunk_text():
    text = "long text..." * 100
    chunks = chunk_text(text, chunk_size=500)
    assert all(count_tokens(c) <= 500 for c in chunks)

# Test vector search
def test_vector_search():
    store = VectorStore()
    store.add_documents(embeddings, doc_id, chunks, filename)
    results = store.search(query_embedding, top_k=5)
    assert len(results) <= 5
```

### Integration Tests
```python
# Test full document upload
async def test_upload_document(client):
    response = await client.post(
        "/api/upload",
        files={"file": uploaded_file}
    )
    assert response.status_code == 201
    assert "document_id" in response.json()

# Test question answering
async def test_query(client, document_id):
    response = await client.post(
        "/api/query",
        json={"question": "test", "document_id": document_id}
    )
    assert response.status_code == 200
    assert "answer" in response.json()
```

## Security Architecture

### Input Validation
- Pydantic model validation
- File extension checking
- File size limits
- Question length limits

### API Security
- No authentication (can be added)
- CORS enabled for all origins (restrict in production)
- No rate limiting (add slowapi for production)
- HTTPS recommended

### Data Security
- API key in environment variables
- No sensitive data in logs
- Vector store on local filesystem
- Can add encryption

## Monitoring & Observability

### Logging Strategy
```
Level | When | Example
------|------|--------
INFO  | Normal operations | "Document uploaded"
WARN  | Recoverable issues | "File format warning"
ERROR | Failed requests | "LLM API error"
```

### Metrics to Track
- Request count/latency
- Document upload success rate
- API error rate
- OpenAI API usage
- Vector store growth

### Health Checks
- `/health` endpoint
- OpenAI API connectivity
- File system access
- Memory usage

## Scalability Roadmap

### Phase 1: Current (Single Instance)
- Local FAISS vector store
- Single API instance
- Limited to available RAM

### Phase 2: Distributed (Multiple Instances)
- Shared FAISS store (NFS/S3)
- Load balancer
- Synchronized metadata

### Phase 3: Cloud Scale (Enterprise)
- Pinecone vector database
- PostgreSQL for metadata
- Distributed caching
- Message queue for async processing

## Future Enhancements

1. **Persistent Chat History**
   - Database integration
   - Multi-turn conversations
   - Conversation management

2. **Advanced Retrieval**
   - Hybrid search (keyword + semantic)
   - Multi-document aggregation
   - Ranking algorithms

3. **Performance**
   - Response streaming
   - Caching layer
   - Async embeddings

4. **Production Ops**
   - Authentication/authorization
   - Rate limiting
   - Monitoring suite
   - Analytics dashboard
