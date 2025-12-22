# Data Model: Integrated RAG Chatbot

## Entities

### BookContent
- **id**: string (unique identifier for the book)
- **title**: string (title of the book)
- **author**: string (author of the book)
- **content**: string (full text content of the book)
- **chunks**: array of ContentChunk (split content for vector storage)
- **metadata**: object (additional information like publication date, etc.)

### ContentChunk
- **id**: string (unique identifier for the chunk)
- **content**: string (text content of the chunk)
- **book_id**: string (reference to the parent book)
- **chunk_index**: integer (position in the book)
- **vector_id**: string (ID in the vector database for retrieval)

### UserQuery
- **id**: string (unique identifier for the query)
- **question**: string (the question asked by the user)
- **book_id**: string (reference to the book being queried)
- **selected_text**: string (optional, text selected by the user)
- **timestamp**: datetime (when the query was made)
- **mode**: enum ('full_book', 'selected_text') (query mode used)

### GeneratedResponse
- **id**: string (unique identifier for the response)
- **query_id**: string (reference to the original query)
- **answer**: string (the generated answer)
- **sources**: array of string (IDs of content chunks used to generate the answer)
- **confidence**: float (confidence score of the response)
- **timestamp**: datetime (when the response was generated)

### ChatSession
- **id**: string (unique identifier for the session)
- **book_id**: string (reference to the book being queried)
- **user_queries**: array of UserQuery (queries made in this session)
- **created_at**: datetime (when the session was created)
- **last_accessed**: datetime (when the session was last used)

## Relationships
- BookContent contains many ContentChunk
- UserQuery references BookContent
- GeneratedResponse references UserQuery
- ChatSession contains many UserQuery
- UserQuery may reference multiple ContentChunk through sources

## Validation Rules
- ContentChunk.content must not exceed Cohere's input token limit
- UserQuery.question must be non-empty
- GeneratedResponse.answer must be grounded in provided sources
- BookContent.id must be unique across the system