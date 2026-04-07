# Testing & Validation Guide

## Pre-Flight Checklist

Before deploying to production, verify:

- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] OpenAI API key configured in `.env`
- [ ] Python 3.9+ installed: `python3 --version`
- [ ] Sufficient disk space (>2GB recommended)
- [ ] Port 8000 available: `lsof -i :8000`
- [ ] Data directories exist: `ls -la data/`

## Unit Tests

### Test Text Processing

```python
# test_text_processor.py
from app.utils.text_processor import chunk_text, count_tokens, clean_text

def test_chunk_text():
    """Test text chunking with overlap"""
    long_text = "This is a test. " * 100  # ~400 words
    chunks = chunk_text(long_text, chunk_size=500, chunk_overlap=100)
    
    assert len(chunks) > 1, "Should create multiple chunks"
    assert all(len(c) > 0 for c in chunks), "All chunks should be non-empty"
    print(f"✓ Created {len(chunks)} chunks")

def test_count_tokens():
    """Test token counting"""
    text = "Hello world"
    tokens = count_tokens(text)
    assert tokens > 0, "Should count tokens"
    print(f"✓ Counted {tokens} tokens")

def test_clean_text():
    """Test text cleaning"""
    dirty_text = "  Hello   world  \n\n  test  "
    clean = clean_text(dirty_text)
    
    assert clean == "Hello world test", "Should clean whitespace"
    assert "\n\n" not in clean, "Should remove extra newlines"
    print("✓ Text cleaned successfully")

if __name__ == "__main__":
    test_chunk_text()
    test_count_tokens()
    test_clean_text()
    print("\n✅ All text processing tests passed!")
```

### Test Vector Store

```python
# test_vector_store.py
import numpy as np
from app.services.vector_store import VectorStore

def test_vector_store():
    """Test FAISS vector store operations"""
    store = VectorStore(embedding_dim=512)
    
    # Create dummy embeddings
    embeddings = [np.random.rand(512).tolist() for _ in range(10)]
    chunks = [f"Chunk {i}" for i in range(10)]
    
    # Test add
    count = store.add_documents(
        embeddings=embeddings,
        document_id="test-doc-1",
        chunks=chunks,
        filename="test.pdf"
    )
    assert count == 10, "Should add 10 chunks"
    print(f"✓ Added {count} chunks")
    
    # Test search
    query_embedding = embeddings[0]
    results = store.search(query_embedding, top_k=3, document_id="test-doc-1")
    assert len(results) <= 3, "Should return at most top_k results"
    assert all(isinstance(r, tuple) for r in results), "Results should be tuples"
    print(f"✓ Found {len(results)} similar chunks")
    
    # Test get_documents
    docs = store.get_documents("test-doc-1")
    assert len(docs) == 10, "Should get all document chunks"
    print(f"✓ Retrieved {len(docs)} document chunks")
    
    print("\n✅ All vector store tests passed!")

if __name__ == "__main__":
    test_vector_store()
```

## Integration Tests

### Test API Endpoints

```bash
#!/bin/bash
# test_api.sh

API_URL="http://localhost:8000"

echo "🧪 Testing Document QA API"
echo "=========================="

# 1. Health Check
echo -e "\n1️⃣  Health Check"
HEALTH=$(curl -s -X GET "$API_URL/health")
if echo $HEALTH | grep -q "healthy"; then
    echo "   ✅ API is healthy"
else
    echo "   ❌ Health check failed"
    exit 1
fi

# 2. Upload
echo -e "\n2️⃣  Document Upload"
echo "Sample document for testing." > /tmp/test.txt
UPLOAD=$(curl -s -X POST "$API_URL/api/upload" -F "file=@/tmp/test.txt")
DOC_ID=$(echo $UPLOAD | jq -r '.document_id')

if [ "$DOC_ID" != "null" ]; then
    echo "   ✅ Document uploaded: $DOC_ID"
else
    echo "   ❌ Upload failed"
    exit 1
fi

# 3. Query
echo -e "\n3️⃣  Question Answering"
QUERY=$(curl -s -X POST "$API_URL/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is in the document?\", \"document_id\": \"$DOC_ID\"}")

ANSWER=$(echo $QUERY | jq -r '.answer')
if [ ! -z "$ANSWER" ] && [ "$ANSWER" != "null" ]; then
    echo "   ✅ Got answer: ${ANSWER:0:50}..."
else
    echo "   ❌ Query failed"
    exit 1
fi

# 4. Document Info
echo -e "\n4️⃣  Document Info"
INFO=$(curl -s -X GET "$API_URL/api/documents/$DOC_ID")
CHUNKS=$(echo $INFO | jq -r '.chunks_count')

if [ ! -z "$CHUNKS" ] && [ "$CHUNKS" -gt "0" ]; then
    echo "   ✅ Document has $CHUNKS chunks"
else
    echo "   ❌ Get document info failed"
    exit 1
fi

# 5. Delete
echo -e "\n5️⃣  Delete Document"
DELETE=$(curl -s -X DELETE "$API_URL/api/documents/$DOC_ID")
if echo $DELETE | grep -q "deleted"; then
    echo "   ✅ Document deleted"
else
    echo "   ❌ Delete failed"
    exit 1
fi

echo -e "\n✅ All API tests passed!"
```

## Performance Testing

### Measure Latency

```bash
#!/bin/bash
# perf_test.sh

API_URL="http://localhost:8000"

echo "⏱️  Performance Testing"
echo "====================="

# Upload timing
echo "Uploading document..."
START=$(date +%s%N)
RESPONSE=$(curl -s -X POST "$API_URL/api/upload" \
  -F "file=@sample.pdf")
END=$(date +%s%N)
UPLOAD_TIME=$(( ($END - $START) / 1000000 ))

DOC_ID=$(echo $RESPONSE | jq -r '.document_id')
echo "Upload time: ${UPLOAD_TIME}ms"

# Query timing
echo "Querying document..."
START=$(date +%s%N)
curl -s -X POST "$API_URL/api/query" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Test?\", \"document_id\": \"$DOC_ID\"}" > /dev/null
END=$(date +%s%N)
QUERY_TIME=$(( ($END - $START) / 1000000 ))

echo "Query time: ${QUERY_TIME}ms"

# Cleanup
curl -s -X DELETE "$API_URL/api/documents/$DOC_ID" > /dev/null

echo -e "\n✅ Performance metrics collected"
```

## Manual Validation Scenarios

### Scenario 1: PDF Processing
1. Upload a multi-page PDF
2. Verify chunks count matches document length
3. Ask questions about different sections
4. Verify answers reference correct content

### Scenario 2: Large Document
1. Upload a 20+MB document
2. Monitor memory usage
3. Verify all chunks created
4. Test query performance

### Scenario 3: Multiple Documents
1. Upload 3+ documents
2. Query each with unique questions
3. Verify document filtering works correctly
4. Delete all documents in order

### Scenario 4: Error Handling
1. Upload unsupported file type → expect 400
2. Upload >50MB file → expect 413
3. Query non-existent document → expect 404
4. Invalid JSON in request → expect 400

## Validation Checklist

- [ ] All supported file formats work (PDF, TXT)
- [ ] Text extraction preserves content
- [ ] Chunks created match expected count
- [ ] Embeddings generated successfully
- [ ] Vector search returns relevant results
- [ ] LLM provides contextual answers
- [ ] Confidence scores are in range [0.5-1.0]
- [ ] Error messages are helpful and accurate
- [ ] Logs capture all important events
- [ ] Query latency < 10 seconds
- [ ] Memory usage remains stable
- [ ] No temporary file leaks
- [ ] Vector store persists and loads correctly
- [ ] All endpoints documented in Swagger
