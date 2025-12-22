# Research Summary: Integrated RAG Chatbot

## Decision: Technology Stack
**Rationale**: Selected Python with FastAPI backend and simple HTML/JS frontend to meet project requirements for embedding in book formats. This stack provides good support for AI integration, is lightweight for embedding, and aligns with the constitutional requirements.

**Alternatives considered**: 
- Node.js/Express backend with React frontend: More complex for embedding purposes
- Pure client-side solution: Would require exposing API keys to frontend
- Full native application: Would not meet embedding requirements

## Decision: RAG Architecture
**Rationale**: Using Cohere's embedding model with Qdrant vector database provides a robust RAG pipeline that can handle both full-book retrieval and user-selected text-only modes as required by the specification.

**Alternatives considered**:
- OpenAI embeddings: Violates constitutional requirement to use Cohere API exclusively
- Local embedding models: Would exceed free-tier constraints and add complexity
- Simple keyword search: Would not meet accuracy requirements

## Decision: Text Splitting Strategy
**Rationale**: Using LangChain's RecursiveCharacterTextSplitter with appropriate chunk size to balance retrieval accuracy and context window limitations. This approach maintains semantic coherence while enabling effective retrieval.

**Alternatives considered**:
- Sentence-level splitting: Might break up related concepts
- Fixed character count: Might split mid-sentence or mid-concept
- Paragraph-level splitting: Might create chunks too large for context windows

## Decision: Frontend Embedding Approach
**Rationale**: Creating a JavaScript widget that can be embedded via script tag or iframe allows for seamless integration into various book formats while maintaining a clean separation between book content and chatbot functionality.

**Alternatives considered**:
- Full custom HTML template: Less flexible for different book formats
- Native PDF integration: Would require different technology stack
- Separate application: Would not meet the embedding requirement

## Decision: Content Isolation Implementation
**Rationale**: Implementing two distinct query pathways (full-book retrieval vs. selected-text-only) ensures strict isolation as required by the constitution and specification.

**Alternatives considered**:
- Single pathway with filtering: Risk of context leakage
- Client-side selection processing: Security concerns with exposing full content