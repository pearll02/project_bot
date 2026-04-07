# 🎯 Visual Setup Cheatsheet

## What You Need to Do - Overview

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Get API Key from OpenAI                           │
│     ↓                                                  │
│  2. Put key in .env file                              │
│     ↓                                                  │
│  3. Install dependencies                              │
│     ↓                                                  │
│  4. Run the server                                    │
│     ↓                                                  │
│  5. Test it                                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step with Code

### STEP 1: Get OpenAI API Key

**Go to:** https://platform.openai.com/account/api-keys

**You'll see:**
```
┌───────────────────────────────────────────┐
│  Create new secret key                    │
│                                           │
│  [Button to create key]                   │
│                                           │
│  Copy this:                               │
│  sk-proj-abc123xyz456...                  │
│                                           │
└───────────────────────────────────────────┘
```

---

### STEP 2: Edit .env File

**Before (WRONG):**
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
```

**After (CORRECT):**
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-abcdefgh12345xyz...
OPENAI_MODEL=gpt-4
```

**How to edit:**
```bash
# Navigate to project
cd /Users/pearlkhuteta/Desktop/project_bot

# Copy the example file
cp .env.example .env

# Open in text editor
nano .env

# Find: OPENAI_API_KEY=your_openai_api_key_here
# Replace with your real key from Step 1

# Save: Ctrl+X → Y → Enter
```

**Verify it worked:**
```bash
cat .env | grep OPENAI_API_KEY
```

Should show:
```
OPENAI_API_KEY=sk-proj-...  ✅ CORRECT
# NOT:
OPENAI_API_KEY=your_openai_api_key_here  ❌ WRONG
```

---

### STEP 3: Install Everything

**Run these commands in order:**

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it (you should see (venv) in your prompt)
source venv/bin/activate

# 3. Install all packages (takes 2-3 minutes)
pip install -r requirements.txt

# 4. Verify it worked
pip list | grep -i openai
```

**Expected output:**
```
openai        1.6.1
fastapi       0.104.1
faiss-cpu     1.7.4
```

---

### STEP 4: Start the Server

**In Terminal 1 (keep this open):**
```bash
python -m uvicorn app.main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

### STEP 5: Test It (Open Terminal 2)

**Test 1: Is it running?**
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "app_name": "Document QA Chatbot",
  "version": "1.0.0"
}
```

**Test 2: Full workflow**
```bash
bash examples.sh
```

**Test 3: View Interactive Docs**
```
Open in browser: http://localhost:8000/docs
```

---

## Configuration Explained

### What Each Setting Does

```env
# Your OpenAI credentials (REQUIRED - get from platform.openai.com)
OPENAI_API_KEY=sk-proj-...

# Which LLM to use
OPENAI_MODEL=gpt-4                          # Most accurate (slower, expensive)
# Alternative: OPENAI_MODEL=gpt-3.5-turbo    # Fast and cheap

# Which embedding model to use
OPENAI_EMBEDDING_MODEL=text-embedding-3-small   # Balanced (recommended)
# Alternative: text-embedding-3-large            # More accurate

# How many tokens in each chunk
CHUNK_SIZE=500                              # Balanced (recommended)
# Larger (1000) = better accuracy            # Smaller (300) = faster search

# How many search results to get
TOP_K_CHUNKS=5                              # Balanced (recommended)
# Larger (10) = more context                # Smaller (3) = faster

# Maximum file size for upload (50MB default)
MAX_FILE_SIZE=52428800                      # In bytes
```

---

## Before & After Checklist

### Before You Start ❌
```
❌ No .env file
❌ No dependencies installed
❌ Server not running
❌ Don't know if it works
```

### After Setup ✅
```
✅ .env file with your API key
✅ Virtual environment activated
✅ All dependencies installed
✅ Server running on http://localhost:8000
✅ Swagger docs at http://localhost:8000/docs
✅ Can upload documents
✅ Can ask questions
✅ Get answers back!
```

---

## Troubleshooting Guide

### ❌ "API Key not found"

**What's wrong:**
```env
OPENAI_API_KEY=your_openai_api_key_here  ← Still has placeholder!
```

**Fix:**
```env
OPENAI_API_KEY=sk-proj-abc123xyz...      ← Real key from OpenAI
```

---

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**What's wrong:**
- Virtual environment not activated
- Dependencies not installed

**Fix:**
```bash
# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### ❌ "Connection refused" or "Connection to localhost failed"

**What's wrong:**
- Server not running in the other terminal

**Fix:**
```bash
# Terminal 1: Start server
python -m uvicorn app.main:app --reload

# Wait 5 seconds for startup
# Then test in Terminal 2
curl http://localhost:8000/health
```

---

### ❌ "Port 8000 is already in use"

**What's wrong:**
- Another app is using port 8000

**Fix:**
```bash
# Use a different port
python -m uvicorn app.main:app --reload --port 8001

# Then test at:
curl http://localhost:8001/health
```

---

## File Structure (What You Should See)

```
project_bot/
├── .env                          ✅ Your config (CREATED BY YOU)
├── .env.example                  📋 Template (already exists)
├── requirements.txt              📦 Python packages
├── venv/                         🐍 Virtual environment (created by you)
├── app/                          🎯 APPLICATION CODE
│   ├── main.py                   (FastAPI app)
│   ├── config.py                 (Settings)
│   ├── routers/                  (API endpoints)
│   ├── services/                 (Business logic)
│   ├── models/                   (Data schemas)
│   └── utils/                    (Helper functions)
├── data/                         💾 Data storage (auto-created)
│   ├── uploads/                  (Your documents)
│   └── vector_store/             (FAISS indexes)
├── logs/                         📝 Log files (auto-created)
├── QUICK_START.md                ⭐ Copy-paste setup
├── SETUP_GUIDE.md                📖 Detailed guide
├── README.md                     📚 Full documentation
└── examples.sh                   🧪 Test script
```

---

## Quick Command Reference

| What | Command |
|------|---------|
| Activate environment | `source venv/bin/activate` |
| Install packages | `pip install -r requirements.txt` |
| Start server | `python -m uvicorn app.main:app --reload` |
| Test health | `curl http://localhost:8000/health` |
| View docs | Open `http://localhost:8000/docs` |
| Run full test | `bash examples.sh` |
| View logs | `tail -f logs/app.log` |
| Deactivate venv | `deactivate` |

---

## Time Estimates

| Task | Time |
|------|------|
| Get API key | 5 minutes |
| Edit .env file | 2 minutes |
| Create venv and install | 5 minutes |
| Start server | 1 minute |
| Run tests | 3 minutes |
| **Total** | **~16 minutes** |

---

## Success! 🎉

If you can do this:
```bash
curl http://localhost:8000/health
```

And get back:
```json
{"status": "healthy", ...}
```

**Then everything is working!** ✅

---

## Next: Learn the System

1. Read [README.md](README.md) - What you can do
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) - How it works
3. Upload your documents and test!

---

Got stuck? Check [SETUP_GUIDE.md](SETUP_GUIDE.md#-common-issues--solutions) for detailed troubleshooting!
