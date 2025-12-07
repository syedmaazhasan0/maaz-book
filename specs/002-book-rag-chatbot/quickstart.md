# Quickstart Guide: AI/Spec-Driven Book Creation + Embedded RAG Chatbot

## Overview

This guide provides a high-level overview of how to set up and run the AI/Spec-Driven Book Creation + Embedded RAG Chatbot project. For complete implementation details, refer to the full book content.

## Prerequisites

- **Node.js**: LTS version installed
- **Python**: 3.10 or higher installed
- **Package managers**: npm/yarn for Node.js, pip for Python
- **API Keys**: OpenAI API key and Qdrant Cloud API key
- **Git**: For version control

## Project Structure

```
project-root/
├── docs/                    # Book chapters in MDX format
├── backend/                 # FastAPI RAG server
│   ├── src/
│   │   ├── api/            # API routes
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/               # Docusaurus site (integrated)
│   ├── docs/              # MDX book chapters
│   ├── src/               # Custom components (including chatbot)
│   ├── docusaurus.config.js
│   └── package.json
└── .env                   # Environment variables (not committed)
```

## Setup Instructions

### 1. Clone and Initialize

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Create virtual environment for backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the backend directory with the following content:

```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=book_content
```

### 3. Set Up the Frontend (Docusaurus)

```bash
# From project root
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 4. Set Up the Backend (FastAPI)

```bash
# From backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the FastAPI server
uvicorn src.main:app --reload --port 8000
```

## Basic Usage

### 1. Indexing Book Content

Before the RAG chatbot can answer questions, you need to index your book content:

```bash
# Make a POST request to index your MDX content
curl -X POST http://localhost:8000/api/index \
  -H "Content-Type: application/json" \
  -d '{
    "chapters": [
      {"id": "ch1", "title": "Chapter 1", "content": "Your chapter content here..."}
    ],
    "forceReindex": true
  }'
```

### 2. Using the Chatbot

Once the backend is running and content is indexed, you can query the chatbot:

```bash
# Ask a question about the book content
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does the book say about RAG systems?",
    "sessionId": "session-123",
    "useSelectedTextOnly": false
  }'
```

Or ask using selected text only:

```bash
# Ask a question using only selected text as context
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain this concept in simpler terms",
    "sessionId": "session-123",
    "useSelectedTextOnly": true,
    "selectedText": "The selected text content here..."
  }'
```

## Frontend Integration

The chatbot is embedded in the Docusaurus site through a custom React component. The frontend handles:

1. Text selection on book pages
2. Communication with the backend API
3. Displaying chat interface
4. Managing chat sessions

## Development Workflow

### Adding New Book Chapters

1. Create a new MDX file in `frontend/docs/`
2. Add the chapter to `frontend/sidebars.js`
3. Re-index the content by calling the indexing API again

### Running Tests

Backend tests:
```bash
cd backend
python -m pytest tests/
```

Frontend development:
```bash
cd frontend
npm run build  # Build for production
npm run serve  # Serve built site locally for testing
```

## Deployment

### Frontend (GitHub Pages)

1. Configure `docusaurus.config.js` with your GitHub Pages settings
2. Run `npm run build` to generate static files
3. Deploy to GitHub Pages using GitHub Actions or manually

### Backend (Cloud Provider)

Deploy the FastAPI application to your preferred cloud provider (Heroku, Render, AWS, etc.) with the required environment variables.

## Troubleshooting

- **API Rate Limits**: If you encounter rate limit errors, check your OpenAI and Qdrant usage
- **Indexing Issues**: Ensure your Qdrant Cloud instance is accessible and properly configured
- **Frontend Integration**: Verify that the backend API URL is correctly configured in the frontend
- **Build Errors**: Check that all dependencies are properly installed and environment variables are set