# Integrated RAG Chatbot

An interactive chatbot that allows readers to ask questions about book content and receive accurate, context-aware responses. The system uses Retrieval-Augmented Generation (RAG) to ensure responses are grounded in the provided book content.

## Features

- Query book content for accurate answers
- Select specific text and ask questions about only that text
- Seamless embedding in book formats
- Context isolation to prevent information leakage
- Rate limiting for free-tier safety
- Comprehensive error handling and logging

## Tech Stack

- **Backend**: FastAPI
- **AI Generation**: Cohere API
- **Vector Storage**: Qdrant Cloud
- **Embeddings**: Cohere embed-english-v3.0
- **Language**: Python 3.11

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables by copying `.env.example` to `.env` and adding your credentials:
   ```bash
   cp .env.example .env
   # Edit .env to add your actual API keys and URLs
   ```
5. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## Docker Setup

Alternatively, you can run the application using Docker:

```bash
docker-compose up --build
```

## API Usage

The API is available at `http://localhost:8000` when running locally.

### Health Check Endpoint
```
GET /health
```
Returns the health status of the service and its dependencies.

### Query Endpoint
```
POST /query
```

Request body:
```json
{
  "question": "Your question about the book",
  "book_id": "book-identifier",
  "selected_text": "Optional text selected by user"
}
```

Response:
```json
{
  "answer": "Generated answer",
  "sources": ["chunk-id-1", "chunk-id-2"],
  "mode_used": "full_book|selected_text"
}
```

## Frontend Integration

The frontend component can be embedded in book formats using the HTML template and JavaScript widget:

1. Include `frontend/styles.css` for styling
2. Add the HTML structure as in `frontend/index.html`
3. Include `frontend/chatbot-widget.js` and initialize with:
   ```javascript
   initChatbot({
     apiUrl: 'http://localhost:8000',  // Update to your backend URL
     bookId: 'your-book-id'
   });
   ```

## Adding New Books

To add a new book to the system:

1. Use the content ingestion service to split and store the book content
2. Generate embeddings for the content chunks
3. Store the embeddings in Qdrant for retrieval

(T059) See `src/services/content_ingestion_service.py` for implementation details.

## Architecture

The system follows a modular architecture:

- `src/models/` - Data models
- `src/services/` - Business logic (RAG, Cohere, Qdrant, etc.)
- `src/api/` - API endpoints
- `src/utils/` - Utility functions (logging, configuration)
- `frontend/` - Frontend components for embedding

## Testing

Run the test suite:
```bash
pytest tests/
```

The test suite includes:
- Unit tests for individual components
- Integration tests for the full RAG pipeline
- Performance tests to ensure response times
- Security tests to validate no credential exposure
- Context isolation tests to ensure proper text selection

## Logging

The application logs to the `logs/` directory with:
- API calls and their parameters
- Errors with full stack traces
- Performance metrics for key operations
- Rotation of log files to prevent excessive disk usage

## Deployment

(T057) For deployment, use the provided Docker configuration:
```bash
docker-compose up -d  # Run in detached mode
```

For production deployment, ensure:
- Properly configured environment variables with API keys
- SSL/TLS for secure communication
- Regular monitoring of logs
- Backup of vector database if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request