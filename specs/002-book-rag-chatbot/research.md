# Research Notes: AI/Spec-Driven Book Creation + Embedded RAG Chatbot

## Research Summary

This research document addresses all unknowns and technical decisions required for implementing the AI/Spec-Driven Book Creation + Embedded RAG Chatbot project.

## Technology Decisions

### Language/Version
- **Python**: 3.10+ (required by project constraints)
- **Node.js**: LTS version (required by project constraints)
- **JavaScript/TypeScript**: For frontend components

### Primary Dependencies
- **Frontend**: Docusaurus (v3.x), React, MDX
- **Backend**: FastAPI (Python), uvicorn (ASGI server)
- **AI/ML**: OpenAI SDK, python-dotenv, Pydantic
- **Vector Database**: Qdrant client library for Python
- **Deployment**: GitHub Pages (frontend), self-hosted or cloud service (backend)

### Storage
- **Vector Storage**: Qdrant Cloud Free Tier (as specified in requirements)
- **Content**: MDX files in Docusaurus docs directory
- **Configuration**: Environment variables and Docusaurus config files

### Testing
- **Backend**: pytest for FastAPI backend
- **Integration**: API endpoint tests, RAG pipeline tests
- **Frontend**: Manual testing of chatbot integration in Docusaurus

### Target Platform
- **Frontend**: Web-based (Docusaurus site deployed to GitHub Pages)
- **Backend**: Cloud server or local server for API endpoints
- **Development**: Cross-platform (Windows, macOS, Linux)

### Performance Goals
- **Response Time**: <5 seconds for chatbot responses (as per success criteria)
- **Accuracy**: 90%+ for book content questions, 95%+ for selected text questions
- **Build Time**: Docusaurus site builds successfully with `npm run build`

### Constraints
- **API Limits**: Respect OpenAI and Qdrant rate limits
- **Free Tier**: Must work within Qdrant Cloud Free Tier limitations
- **Deployment**: GitHub Pages static hosting (no server-side code)
- **Reproducibility**: 100% success rate for following book instructions

## Architecture Decision: Multi-Project Structure

The project requires a multi-project structure due to the distinct frontend (Docusaurus) and backend (FastAPI) components that need to be developed separately:

### Frontend (Docusaurus)
- Contains the technical book in MDX format
- Includes the embedded chatbot component
- Deployed to GitHub Pages as a static site

### Backend (FastAPI)
- Handles the RAG pipeline
- Manages embedding generation and storage
- Provides API endpoints for the chatbot
- Connects to Qdrant Cloud and OpenAI

## RAG Implementation Strategy

### 1. Content Processing Pipeline
- Extract text from MDX book chapters
- Chunk content into appropriate sizes for embedding
- Generate embeddings using OpenAI API
- Store embeddings in Qdrant Cloud

### 2. Query Processing Pipeline
- For general questions: Use vector search in Qdrant to find relevant book content
- For selected text questions: Use selected text as context directly
- Combine retrieved context with user query
- Generate response using OpenAI API

### 3. Frontend Integration
- Create React component for chatbot UI
- Integrate with Docusaurus site
- Implement text selection functionality
- Handle communication with FastAPI backend

## Deployment Strategy

### Frontend Deployment
- Docusaurus site built and deployed to GitHub Pages
- Uses GitHub Actions for automated deployment
- Static site hosting with no server-side requirements

### Backend Deployment
- FastAPI application deployed to cloud platform (e.g., Heroku, Render, or similar)
- Environment variables for API keys and configuration
- Connection to Qdrant Cloud and OpenAI API

## Compliance with Constitution

All decisions align with the project constitution:
- Technical accuracy: Using official documentation for all technologies
- Clarity and accessibility: Focusing on beginner-to-intermediate developers
- Modularity and reproducibility: Ensuring copy-paste ready code
- Operational reliability: Fully testable and operational system
- Seamless integration: Aligning book content with RAG functionality
- Up-to-date standards: Using current APIs and tools
- MDX formatting: Following Docusaurus conventions
- RAG functionality: Supporting Qdrant Cloud, text selection, and site integration