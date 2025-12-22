# Quickstart Guide: Integrated RAG Chatbot

## Prerequisites

- Python 3.11+
- pip package manager
- Git (optional, for cloning the repository)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```env
   COHERE_API_KEY=uXRHJv5LaobbAjG4AWk65bOzJAQYZLkMbXzIkqdJ
   QDRANT_URL=https://5e0d3b5a-03d5-492e-994c-d89788695a89.europe-west3-0.gcp.cloud.qdrant.io
   QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ccZWfmf7KRQhP8qEj2AuFQ8hpfBwYgURSQN6etVHoxY
   NEON_DB_URL=postgresql://neondb_owner:npg_PmRJ7FGhB4AS@ep-green-tree-ahpo85q1-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

## Embedding in a Book

1. Copy the `frontend/chatbot-widget.js` file to your book's HTML directory.

2. Add the following to your HTML file:
   ```html
   <div id="chatbot-container"></div>
   <script src="chatbot-widget.js"></script>
   <script>
     initChatbot({
       apiUrl: 'http://localhost:8000',
       bookId: 'your-book-id'
     });
   </script>
   ```

## API Usage

### Query the Chatbot

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main theme of this book?",
    "book_id": "book-123"
  }'
```

### Query with Selected Text

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does this text mean?",
    "selected_text": "This is the specific text the user selected...",
    "book_id": "book-123"
  }'
```

## Indexing a New Book

1. Prepare your book content in text format.

2. Run the indexing script:
   ```bash
   python scripts/index_book.py --book-path path/to/book.txt --book-id book-123
   ```

## Testing

Run the test suite:
```bash
cd backend
pytest tests/
```