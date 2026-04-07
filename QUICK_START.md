# ⚡ Quick Setup in 5 Steps (Copy-Paste Ready)

## Step 1️⃣: Get OpenAI API Key (5 min)

Go to: https://platform.openai.com/account/api-keys
- Click "Create new secret key"
- Copy it (starts with `sk-`)
- Save it safely

---

## Step 2️⃣: Navigate to Project

```bash
cd /Users/pearlkhuteta/Desktop/project_bot
```

---

## Step 3️⃣: Setup Environment (Copy-Paste These Commands)

### Create .env file:
```bash
cp .env.example .env
```

### Edit .env with your API key:
```bash
# Option A: Using nano (easiest)
nano .env
# Then find the line: OPENAI_API_KEY=your_openai_api_key_here
# Replace with your actual key like: OPENAI_API_KEY=sk-proj-abc123...
# Save: Press Ctrl+X, then Y, then Enter

# Option B: Using sed (automatic)
sed -i '' 's/your_openai_api_key_here/sk-YOUR-ACTUAL-KEY-HERE/' .env
```

### Verify it worked:
```bash
cat .env | head -3
```

---

## Step 4️⃣: Install Dependencies (3-5 min)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
```

---

## Step 5️⃣: Start the Server

```bash
python -m uvicorn app.main:app --reload
```

**Keep this terminal open!** You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🧪 Test It (In Another Terminal)

```bash
# Test 1: Health check
curl http://localhost:8000/health

# Test 2: Upload a sample document
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@<(echo 'Machine learning is AI. It learns from data.')")
DOC_ID=$(echo $RESPONSE | grep -o '"document_id":"[^"]*' | head -1 | cut -d'"' -f4)

# Test 3: Ask a question
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"What is machine learning?\",
    \"document_id\": \"$DOC_ID\"
  }"
```

Or simply:
```bash
bash examples.sh
```

---

## 🌐 View Interactive Docs

Open in browser:
```
http://localhost:8000/docs
```

---

## 🎉 Done!

You now have a working Document Q&A API!

**Next Steps:**
1. Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed steps with troubleshooting
2. Read [README.md](README.md) for all features
3. Upload your own documents and test!

---

## ⚙️ Configuration Options (Optional)

Edit `.env` to change performance:

```env
# Faster responses (cheaper)
OPENAI_MODEL=gpt-3.5-turbo
CHUNK_SIZE=300
TOP_K_CHUNKS=3

# Better accuracy (slower/expensive)
OPENAI_MODEL=gpt-4
CHUNK_SIZE=750
TOP_K_CHUNKS=10
```

---

## ❌ Common Issues

| Issue | Fix |
|-------|-----|
| `No module named 'fastapi'` | Run: `pip install -r requirements.txt` |
| `API Key error` | Check `.env` has real key (starts with `sk-`) |
| `Port 8000 in use` | Run with different port: `--port 8001` |
| `Connection refused` | Make sure server is running in other terminal |

---

That's it! 🚀
