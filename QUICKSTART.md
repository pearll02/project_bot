# Quick Start Guide

## Get Running in 5 Minutes

### Prerequisites
- Python 3.9+
- OpenAI API Key (free trial available)
- 2GB RAM

### Step 1: Clone & Setup (2 min)
```bash
cd project_bot
bash setup.sh
```

This will:
- Create Python virtual environment
- Install dependencies
- Generate .env file

### Step 2: Configure API Key (1 min)
```bash
# Edit .env and add your OpenAI API Key
nano .env
# Find line: OPENAI_API_KEY=your_openai_api_key_here
# Replace with your actual key from platform.openai.com
```

### Step 3: Start Server (1 min)
```bash
python -m uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 4: Test API (1 min)

**In another terminal:**
```bash
bash examples.sh
```

Or visit: http://localhost:8000/docs

---

## Common Tasks

### Upload a Document
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@your_document.pdf"
```

Save the `document_id` from response.

### Ask a Question
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "document_id": "YOUR_DOCUMENT_ID"
  }'
```

### View Interactive Docs
Open: http://localhost:8000/docs

---

---

## Troubleshooting

**"API Key not found"**
- Check .env file exists: `ls -la .env`
- Verify key format: starts with `sk-`

**"Port 8000 already in use"**
```bash
python -m uvicorn app.main:app --port 8001
```

**"Module not found"**
- Activate venv: `source venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

**"FAISS not found"**
```bash
pip install faiss-cpu
```

---

## Next Steps

1. Read [README.md](README.md) - Full documentation
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) - System design
4. Explore API at: http://localhost:8000/docs

---

## Example Workflow

```bash
# 1. Create sample document
cat > sample.txt << 'EOF'
Machine Learning

Machine learning is a subset of AI that enables systems
to learn and improve from experience without being explicitly programmed.

Key Applications:
- Computer Vision
- Natural Language Processing
- Recommendation Systems
- Predictive Analytics

Future:
ML will continue to transform industries in the coming decades.
EOF

# 2. Upload it
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@sample.txt")

DOC_ID=$(echo $RESPONSE | jq -r '.document_id')
echo "Document ID: $DOC_ID"

# 3. Ask questions
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"What is machine learning?\",
    \"document_id\": \"$DOC_ID\"
  }" | jq '.answer'

# 4. Clean up
curl -X DELETE http://localhost:8000/api/documents/$DOC_ID
```

---

## Performance Tips

- **Faster responses**: Use `gpt-3.5-turbo` instead of `gpt-4`
- **Better accuracy**: Increase `top_k` from 5 to 10
- **Optimize costs**: Use `text-embedding-3-small` model
- **Reduce latency**: Decrease `chunk_size` to 300 tokens

---

For detailed documentation, see [README.md](README.md)
