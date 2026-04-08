# 🚀 Complete Setup & Running Guide

Follow these steps to get the project running on your machine.

## 📋 What You Need Before Starting

- Python 3.9 or higher (check with `python3 --version`)
- A Google Gemini API key (get free at ai.google.com)
- ~2GB free disk space
- ~500MB RAM minimum
- Terminal/Command line access

---

## Key 1: Get Google Gemini API Key (5 minutes)

### 1.1 Create Google Account
1. Go to: https://ai.google.dev
2. Sign in with Google account
3. No credit card needed

### 1.2 Get API Key
1. Go to: https://ai.google.dev/api/keys
2. Click "Create API Key"
3. Copy the key
4. **Save it somewhere safe**

### 1.3 Verify API Key Works (Optional)
```bash
# Test in Python
python3 -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('Valid!')"
```

---

## 💻 Step 2: Setup Project Locally (5 minutes)

### 2.1 Navigate to Project Directory
```bash
cd /Users/pearlkhuteta/Desktop/project_bot
```

### 2.2 Create Environment File
```bash
# Copy the example file
cp .env.example .env
```

### 2.3 Edit .env and Add Your API Key

**Open the .env file:**
```bash
nano .env
```

**You'll see:**
```
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

**Replace with your actual key:**
```
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.5-flash
```

**Save and exit:**
- Press `Ctrl + X`
- Press `Y` (yes)
- Press `Enter`

### 2.4 Verify .env File
```bash
# Check that the file was updated correctly
cat .env | head -5
```

You should see your actual API key printed.

---

## ⚙️ Step 3: Install Dependencies (3 minutes)

### 3.1 Create Virtual Environment
```bash
# Create Python virtual environment
python3 -m venv venv
```

### 3.2 Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt now.

### 3.3 Install Required Packages
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

This will install:
- FastAPI - Web framework
- Uvicorn - Web server
- Google Generative AI - Gemini API
- FAISS - Vector database
- pdfplumber - PDF parsing
- And other dependencies

**This takes 2-3 minutes** depending on your internet speed.

### 3.4 Verify Installation
```bash
# Check if all packages installed
pip list | grep -E "fastapi|google.generative|faiss"
```

You should see:
```
google-generativeai        0.3.0
fastapi                    0.110.0
faiss-cpu                  1.13.2
```

---

## 🏃 Step 4: Run the Server (2 minutes)

### 4.1 Make Sure Virtual Environment is Active
```bash
# Check for (venv) in your terminal prompt
# If not active, run:
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### 4.2 Start the Server
```bash
# Run the FastAPI server
python -m uvicorn app.main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Keep this terminal window open!**

---

## 🧪 Step 5: Test the Project (5 minutes)

### 5.1 In Another Terminal, Test Health Check

**Open a new terminal window** and run:

```bash
# Test if API is running
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app_name": "Document QA Chatbot",
  "version": "1.0.0"
}
```

### 5.2 View Interactive API Documentation

Open your browser and go to:
```
http://localhost:8000/docs
```

You'll see a **Swagger UI** with all API endpoints. You can test them directly from here!

### 5.3 Quick Test - Upload & Query a Document

**Create a sample document:**
```bash
cat > /tmp/sample.txt << 'EOF'
Machine Learning Introduction

Machine learning is a subset of artificial intelligence that enables 
systems to learn and improve from experience without being explicitly programmed.

Key Applications:
- Image Recognition
- Natural Language Processing
- Recommendation Systems
- Autonomous Vehicles

Future of ML:
Machine learning will continue to transform industries in the coming years.
It is becoming essential for modern software development.
EOF
```

**Upload the document:**
```bash
# Save response to variable
RESPONSE=$(curl -X POST http://localhost:8000/api/upload \
  -F "file=@/tmp/sample.txt")

echo $RESPONSE

# Extract document ID
DOC_ID=$(echo $RESPONSE | grep -o '"document_id":"[^"]*' | cut -d'"' -f4)
echo "Document ID: $DOC_ID"
```

**Ask a question:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"What is machine learning?\",
    \"document_id\": \"$DOC_ID\"
  }"
```

Expected response:
```json
{
  "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
  "document_id": "...",
  "chunks_used": 2,
  "confidence": 0.92,
  "sources": [...]
}
```

### 5.4 Clean Up (Optional)

```bash
# Delete the document from the system
curl -X DELETE "http://localhost:8000/api/documents/$DOC_ID"
```

---

## 📝 Complete Test Script

Or run the complete automated test:

```bash
bash examples.sh
```

This will:
1. Create a sample document
2. Upload it
3. Ask multiple questions
4. Show answers
5. Clean up

---

### 🎯 What Each Configuration Means

| Setting | Default | What It Does | Change If |
|---------|---------|-------------|----------|
| `GEMINI_API_KEY` | ❌ Required | Your Gemini credentials | Must add your key |
| `GEMINI_MODEL` | gemini-2.5-flash | Which LLM to use | Want different model |
| `CHUNK_SIZE` | 500 | Tokens per text chunk | Want faster search → reduce to 300 |
| `CHUNK_OVERLAP` | 100 | Overlap between chunks | Want better context → increase to 200 |
| `TOP_K_CHUNKS` | 5 | Results to retrieve | Want more context → increase to 10 |
| `MAX_FILE_SIZE` | 52428800 | Max upload size in bytes | Need larger uploads → increase |

---

### ⏱️ Performance Tips

### For Faster Responses (Trade Accuracy)
```bash
# Edit .env
GEMINI_MODEL=gemini-1.5-flash      # Faster model
CHUNK_SIZE=300                     # Smaller chunks
TOP_K_CHUNKS=3                     # Fewer results
```

### For Better Accuracy (Trade Speed)
```bash
# Edit .env
GEMINI_MODEL=gemini-2.5-flash      # More capable model
CHUNK_SIZE=750                     # Larger chunks
TOP_K_CHUNKS=10                    # More results
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'fastapi'"

**Problem:** Virtual environment not activated or dependencies not installed

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Issue 2: "API Key not provided" or "Gemini API Error"

**Problem:** Gemini API key not configured correctly

**Solution:**
```bash
# Check .env file
cat .env | grep GEMINI_API_KEY

# Should show: GEMINI_API_KEY=AIzaSy...
# If it shows "your_google_gemini_api_key_here", edit .env again
nano .env
```

### Issue 3: "Port 8000 already in use"

**Problem:** Another application is using port 8000

**Solution:**
```bash
# Use a different port
python -m uvicorn app.main:app --reload --port 8001

# Then test at: http://localhost:8001
```

### Issue 4: "Connection refused" when testing API

**Problem:** Server not running or not responding

**Solution:**
```bash
# Check if server is running in another terminal
# You should see: "INFO: Application startup complete"

# If not, start it:
python -m uvicorn app.main:app --reload

# Then try testing again in 5 seconds
sleep 5
curl http://localhost:8000/health
```

### Issue 5: "FAISS not found"

**Problem:** FAISS CPU library not installed

**Solution:**
```bash
pip install faiss-cpu
```

---

## 📊 Testing Checklist

After setup, verify everything works:

- [ ] `.env` file created and has your Gemini API key
- [ ] Virtual environment activated (see `(venv)` in prompt)
- [ ] Dependencies installed (`pip list` shows packages)
- [ ] Server running (`python -m uvicorn app.main:app --reload`)
- [ ] Health check works (`curl http://localhost:8000/health`)
- [ ] Swagger docs load (`http://localhost:8000/docs`)
- [ ] Can upload a document
- [ ] Can ask a question
- [ ] Get answer back with confidence score

---

## 🚀 What's Next?

Once everything is working:

1. **Read the Full Documentation:**
   - [README.md](README.md) - Complete feature guide
   - [ARCHITECTURE.md](ARCHITECTURE.md) - How the system works
   - [INDEX.md](INDEX.md) - Navigation guide

2. **Try with Your Own Documents:**
   - Upload your PDFs or text files
   - Ask questions specific to your documents
   - Adjust settings if needed

3. **Customize Configuration:**
   - Edit `.env` to tune performance
   - Adjust chunk size for better results
   - Change LLM model for cost/quality trade-offs

4. **Integrate with Your Code:**
   - See [client_example.py](client_example.py) for Python integration
   - Use REST API for other languages
   - Build a web interface on top

---

## 💡 Quick Reference

| Task | Command |
|------|---------|
| Activate venv | `source venv/bin/activate` |
| Install deps | `pip install -r requirements.txt` |
| Start server | `python -m uvicorn app.main:app --reload` |
| Test health | `curl http://localhost:8000/health` |
| View docs | Open http://localhost:8000/docs |
| Upload doc | `curl -X POST http://localhost:8000/api/upload -F "file=@doc.pdf"` |
| Ask question | `curl -X POST http://localhost:8000/api/query -H "Content-Type: application/json" -d '{"question":"...","document_id":"..."}' ` |
| Run tests | `bash examples.sh` |
| Check logs | `tail -f logs/app.log` |

---

## 📞 Need Help?

1. Check [INDEX.md](INDEX.md) for troubleshooting section
2. Look at [README.md](README.md) for detailed documentation
3. Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
4. Check logs: `tail -f logs/app.log`

---

## ✅ You're Ready!

Follow these steps in order and you'll have a working Document Q&A chatbot running locally. Start with Step 1 and work through each step sequentially.

**Total time: ~20 minutes from start to your first working query!**
