#!/bin/bash

# Setup and run the Document QA Chatbot

set -e

echo "🚀 Document QA Chatbot Setup"
echo "=============================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python $python_version"

# Check if pip is available
echo "✓ Checking pip..."
pip3 --version > /dev/null

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Creating .env from example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your GEMINI_API_KEY"
    echo ""
    echo "   nano .env"
    echo ""
    exit 1
fi

# Check if GEMINI_API_KEY is set
if ! grep -q "GEMINI_API_KEY=AIzaSy" .env; then
    echo "❌ ERROR: GEMINI_API_KEY not properly configured in .env"
    echo "   Please set a valid Google Gemini API key in .env file"
    exit 1
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🎯 Next Steps:"
echo "   1. Make example script executable:"
echo "      chmod +x examples.sh"
echo ""
echo "   2. Run the server:"
echo "      python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "   3. In another terminal, test the API:"
echo "      bash examples.sh"
echo ""
echo "   4. Visit interactive docs:"
echo "      http://localhost:8000/docs"
echo ""
