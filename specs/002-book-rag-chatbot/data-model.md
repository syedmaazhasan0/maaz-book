# Data Model: AI/Spec-Driven Book Creation + Embedded RAG Chatbot

## Overview

This document defines the key data entities and their relationships for the AI/Spec-Driven Book Creation + Embedded RAG Chatbot project.

## Core Entities

### 1. Book Chapter
- **Name**: Book Chapter
- **Fields**:
  - id: string (unique identifier for the chapter)
  - title: string (chapter title)
  - content: string (full MDX content of the chapter)
  - wordCount: integer (number of words in the chapter)
  - position: integer (order in the book sequence)
  - tags: string[] (topics/tags related to the chapter)
  - createdAt: datetime (when the chapter was created)
  - updatedAt: datetime (when the chapter was last modified)

- **Relationships**:
  - One-to-many with Content Chunk (a chapter can be split into multiple chunks)
  - Part of Book (belongs to one book)

### 2. Content Chunk
- **Name**: Content Chunk
- **Fields**:
  - id: string (unique identifier for the chunk)
  - content: string (text content of the chunk)
  - chapterId: string (reference to the parent chapter)
  - chunkIndex: integer (position of this chunk within the chapter)
  - embedding: float[] (vector embedding of the content)
  - metadata: object (additional information like source, position, etc.)

- **Relationships**:
  - Many-to-one with Book Chapter (belongs to one chapter)
  - Stored in Qdrant Vector Database (for retrieval)

### 3. Chat Session
- **Name**: Chat Session
- **Fields**:
  - id: string (unique identifier for the session)
  - userId: string (identifier for the user, if applicable)
  - createdAt: datetime (when the session started)
  - lastActiveAt: datetime (when the session was last used)
  - isActive: boolean (whether the session is currently active)

- **Relationships**:
  - One-to-many with Chat Message (contains multiple messages)

### 4. Chat Message
- **Name**: Chat Message
- **Fields**:
  - id: string (unique identifier for the message)
  - sessionId: string (reference to the parent session)
  - role: string (either "user" or "assistant")
  - content: string (the text content of the message)
  - timestamp: datetime (when the message was created)
  - contextUsed: string (the context that was used to generate the response)

- **Relationships**:
  - Many-to-one with Chat Session (belongs to one session)

### 5. User Selection
- **Name**: User Selection
- **Fields**:
  - id: string (unique identifier for the selection)
  - sessionId: string (reference to the session where selection was made)
  - text: string (the selected text content)
  - sourceUrl: string (URL where the text was selected from)
  - selectionStart: integer (start position of selection in source)
  - selectionEnd: integer (end position of selection in source)
  - createdAt: datetime (when the selection was made)

- **Relationships**:
  - Many-to-one with Chat Session (belongs to one session)

## API Data Contracts

### 1. Query Request
- **Purpose**: Request for the chatbot to answer a question
- **Fields**:
  - query: string (the user's question)
  - sessionId: string (optional session identifier)
  - useSelectedTextOnly: boolean (whether to use only selected text as context)
  - selectedText: string (optional text selected by user)

### 2. Query Response
- **Purpose**: Response from the chatbot to a query
- **Fields**:
  - response: string (the chatbot's answer)
  - sources: array (list of sources used to generate the answer)
  - sessionId: string (session identifier)
  - timestamp: datetime (when the response was generated)

### 3. Index Request
- **Purpose**: Request to index book content for RAG
- **Fields**:
  - chapters: array (list of book chapters to be indexed)
  - forceReindex: boolean (whether to reindex existing content)

### 4. Index Response
- **Purpose**: Response confirming indexing operation
- **Fields**:
  - status: string (success or failure)
  - indexedCount: integer (number of chunks indexed)
  - message: string (additional information)

## Validation Rules

### Book Chapter
- Title must not be empty
- Content must be between 700-1500 words (as per requirements)
- Position must be unique within the book
- Content must be valid MDX format

### Content Chunk
- Content must not exceed token limits for embedding model
- Must have a valid chapter reference
- Embedding must be a valid vector

### Chat Message
- Content must not be empty
- Role must be either "user" or "assistant"
- Must belong to a valid session

### User Selection
- Text must not be empty
- Must belong to a valid session
- Source URL must be valid

## State Transitions

### Chat Session
- Created → Active (when first message is sent)
- Active → Inactive (after period of inactivity or explicit closure)
- Inactive → Active (if user returns to session)

## Data Flow

1. Book content is stored as Book Chapters
2. Chapters are processed into Content Chunks with embeddings
3. Chunks are stored in Qdrant Vector Database for retrieval
4. User interactions create Chat Sessions and Messages
5. User selections are stored separately for context-specific responses
6. Query requests are processed using either vector search or selected text
7. Responses are generated and returned to the frontend