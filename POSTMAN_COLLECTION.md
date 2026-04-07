# Postman Collection for Document QA Chatbot API

This collection includes all endpoints for the Document QA Chatbot API.

## Import Steps

1. Open Postman
2. Click "Import" (top-left)
3. Select "Raw text" tab
4. Copy and paste the JSON below
5. Click "Continue" and "Import"

## Environment Setup

Create a Postman environment with these variables:
- `base_url`: http://localhost:8000
- `document_id`: (automatically populated after upload)

---

```json
{
  "info": {
    "_postman_id": "doc-qa-chatbot",
    "name": "Document QA Chatbot API",
    "description": "Collection for Document Q&A Chatbot REST API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health & Info",
      "item": [
        {
          "name": "Health Check",
          "request": {
            "method": "GET",
            "url": {
              "raw": "{{base_url}}/health",
              "host": ["{{base_url}}"],
              "path": ["health"]
            },
            "description": "Check API health status"
          }
        },
        {
          "name": "API Info",
          "request": {
            "method": "GET",
            "url": {
              "raw": "{{base_url}}/",
              "host": ["{{base_url}}"],
              "path": [""]
            },
            "description": "Get API information and endpoints"
          }
        }
      ]
    },
    {
      "name": "Document Management",
      "item": [
        {
          "name": "Upload Document",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "if (pm.response.code === 201) {",
                  "  var jsonData = pm.response.json();",
                  "  pm.environment.set('document_id', jsonData.document_id);",
                  "  pm.test('Document uploaded successfully', function() {",
                  "    pm.expect(jsonData.document_id).to.exist;",
                  "  });",
                  "}"
                ]
              }
            }
          ],
          "request": {
            "method": "POST",
            "url": {
              "raw": "{{base_url}}/api/upload",
              "host": ["{{base_url}}"],
              "path": ["api", "upload"]
            },
            "body": {
              "mode": "formdata",
              "formdata": [
                {
                  "key": "file",
                  "type": "file",
                  "src": ""
                }
              ]
            },
            "description": "Upload a PDF or TXT file"
          }
        },
        {
          "name": "Get Document Info",
          "request": {
            "method": "GET",
            "url": {
              "raw": "{{base_url}}/api/documents/{{document_id}}",
              "host": ["{{base_url}}"],
              "path": ["api", "documents", "{{document_id}}"]
            },
            "description": "Get information about a stored document"
          }
        },
        {
          "name": "Delete Document",
          "request": {
            "method": "DELETE",
            "url": {
              "raw": "{{base_url}}/api/documents/{{document_id}}",
              "host": ["{{base_url}}"],
              "path": ["api", "documents", "{{document_id}}"]
            },
            "description": "Delete a document and its embeddings"
          }
        }
      ]
    },
    {
      "name": "Query & RAG",
      "item": [
        {
          "name": "Ask Question (Basic)",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "url": {
              "raw": "{{base_url}}/api/query",
              "host": ["{{base_url}}"],
              "path": ["api", "query"]
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"question\": \"What is the main topic of the document?\",\n  \"document_id\": \"{{document_id}}\"\n}"
            },
            "description": "Ask a question about the document"
          }
        },
        {
          "name": "Ask Question (With Context)",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "url": {
              "raw": "{{base_url}}/api/query",
              "host": ["{{base_url}}"],
              "path": ["api", "query"]
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"question\": \"What are the key points?\",\n  \"document_id\": \"{{document_id}}\",\n  \"top_k\": 5,\n  \"include_context\": true\n}"
            },
            "description": "Ask question and get source chunks"
          }
        },
        {
          "name": "Ask Question (Custom top_k)",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "url": {
              "raw": "{{base_url}}/api/query",
              "host": ["{{base_url}}"],
              "path": ["api", "query"]
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"question\": \"Your question here\",\n  \"document_id\": \"{{document_id}}\",\n  \"top_k\": 10,\n  \"include_context\": false\n}"
            },
            "description": "Ask question with custom retrieval count"
          }
        }
      ]
    }
  ]
}
```

## Usage

1. **Upload a Document**
   - Click "Upload Document"
   - In Body, select a PDF or TXT file
   - Send request
   - Document ID is automatically saved to environment

2. **Ask Questions**
   - Choose a question request (Basic, With Context, or Custom)
   - Modify the question
   - Send request
   - View answer and confidence score

3. **Get Document Info**
   - Click "Get Document Info"
   - Send request
   - View document details

4. **Delete Document**
   - Click "Delete Document"
   - Send request to clean up

## Notes

- First request automatically sets `{{document_id}}` for subsequent requests
- Requires API to be running at `http://localhost:8000`
- Files must be in `/uploads` folder or use absolute path
