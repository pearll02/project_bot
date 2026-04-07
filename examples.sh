#!/bin/bash

# Document QA API - Example cURL Requests
# This script demonstrates all API endpoints

API_URL="http://localhost:8000"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Document QA Chatbot API Examples ===${NC}\n"

# 1. Health Check
echo -e "${YELLOW}1. Health Check${NC}"
curl -s -X GET "$API_URL/health" | jq '.'
echo ""

# 2. API Info
echo -e "${YELLOW}2. API Information${NC}"
curl -s -X GET "$API_URL/" | jq '.'
echo ""

# 3. Upload Document
echo -e "${YELLOW}3. Creating sample document for upload...${NC}"

# Create a sample document
SAMPLE_DOC=$(cat <<'EOF'
Machine Learning Fundamentals

Introduction
Machine learning is a subset of artificial intelligence that focuses on 
the development of algorithms and statistical models that enable computers 
to learn from and make predictions based on data.

Key Concepts
1. Supervised Learning: Models trained on labeled data
2. Unsupervised Learning: Models find patterns in unlabeled data
3. Reinforcement Learning: Models learn through interaction with environment

Applications
Machine learning is used in:
- Image recognition and computer vision
- Natural language processing
- Recommendation systems
- Predictive analytics
- Autonomous vehicles

Conclusion
Machine learning is transforming industries and will continue to be a 
crucial technology in the future of artificial intelligence.
EOF
)

echo "$SAMPLE_DOC" > /tmp/sample_document.txt

echo -e "${YELLOW}Uploading document...${NC}"
UPLOAD_RESPONSE=$(curl -s -X POST "$API_URL/api/upload" \
  -F "file=@/tmp/sample_document.txt")

echo "$UPLOAD_RESPONSE" | jq '.'

# Extract document ID
DOCUMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.document_id')

if [ "$DOCUMENT_ID" = "null" ] || [ -z "$DOCUMENT_ID" ]; then
    echo -e "${RED}Error: Failed to extract document ID${NC}"
    exit 1
fi

echo -e "${GREEN}Document ID: $DOCUMENT_ID${NC}\n"

# 4. Get Document Info
echo -e "${YELLOW}4. Get Document Information${NC}"
curl -s -X GET "$API_URL/api/documents/$DOCUMENT_ID" | jq '.'
echo ""

# 5. Ask Questions
echo -e "${YELLOW}5. Asking Questions${NC}\n"

# Question 1
echo -e "${BLUE}Q1: What is machine learning?${NC}"
QUERY1=$(curl -s -X POST "$API_URL/api/query" \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"What is machine learning?\",
    \"document_id\": \"$DOCUMENT_ID\",
    \"top_k\": 3,
    \"include_context\": false
  }")

echo "$QUERY1" | jq '.answer'
echo -e "Confidence: $(echo "$QUERY1" | jq '.confidence')"
echo ""

# Question 2
echo -e "${BLUE}Q2: What are the types of machine learning?${NC}"
QUERY2=$(curl -s -X POST "$API_URL/api/query" \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"What are the types of machine learning?\",
    \"document_id\": \"$DOCUMENT_ID\",
    \"top_k\": 5,
    \"include_context\": true
  }")

echo "$QUERY2" | jq '.answer'
echo -e "Chunks used: $(echo "$QUERY2" | jq '.chunks_used')"
echo ""

# Question 3
echo -e "${BLUE}Q3: What are the applications of ML?${NC}"
QUERY3=$(curl -s -X POST "$API_URL/api/query" \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"List the applications of machine learning.\",
    \"document_id\": \"$DOCUMENT_ID\"
  }")

echo "$QUERY3" | jq '.answer'
echo ""

# 6. Delete Document
echo -e "${YELLOW}6. Deleting Document${NC}"
DELETE_RESPONSE=$(curl -s -X DELETE "$API_URL/api/documents/$DOCUMENT_ID")
echo "$DELETE_RESPONSE" | jq '.'
echo ""

# Cleanup
rm -f /tmp/sample_document.txt

echo -e "${GREEN}=== Examples Complete ===${NC}"
echo -e "\nNote: The vector store has been cleaned up."
echo -e "Try uploading your own PDF or TXT files to test with real documents!"
