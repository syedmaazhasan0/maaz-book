---
id: 1
title: Integrated RAG Chatbot Plan
stage: plan
date: 2025-12-20
surface: agent
model: Qwen
feature: integrated-rag-chatbot
branch: 001-integrated-rag-chatbot
user: Maaz Hassan
command: /sp.plan
labels: ["rag", "chatbot", "planning", "ai"]
links:
  spec: specs/001-integrated-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-integrated-rag-chatbot/plan.md
 - specs/001-integrated-rag-chatbot/research.md
 - specs/001-integrated-rag-chatbot/data-model.md
 - specs/001-integrated-rag-chatbot/quickstart.md
 - specs/001-integrated-rag-chatbot/contracts/api-contract.yaml
tests:
 - none
---

## Prompt

```
/sp.plan Integrated RAG Chatbot Development
Phase 1: Setup and Environment Configuration (Day 1-2)

Create project repository and structure using SpecifyKit Plus
Install and configure Gemini CLI for development workflow
Set up virtual environment with required packages: fastapi, uvicorn, qdrant-client, cohere, langchain (or langchain-community), python-dotenv
Create .env file with credentials:
COHERE_API_KEY=uXRHJv5LaobbAjG4AWk65bOzJAQYZLkMbXzIkqdJ
QDRANT_URL=https://5e0d3b5a-03d5-492e-994c-d89788695a89.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ccZWfmf7KRQhP8qEj2AuFQ8hpfBwYgURSQN6etVHoxY
NEON_DB_URL=postgresql://neondb_owner:npg_PmRJ7FGhB4AS@ep-green-tree-ahpo85q1-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
Test connections to Qdrant and Cohere APIs
Milestone: All services connected successfully, .env secure

Phase 2: Book Content Ingestion and Vector Store Setup (Day 3-4)

Prepare sample book content (plain text or markdown format)
Split text into manageable chunks (using LangChain RecursiveCharacterTextSplitter)
Generate embeddings using Cohere's embed-english-v3.0 model
Create Qdrant collection (name: book_collection, vector size: 1024 for Cohere embed v3)
Upsert all book chunks with metadata into Qdrant
Add optional persistent storage to Neon PostgreSQL for chunk metadata or query logs
Milestone: Full book content indexed in Qdrant, searchable via similarity queries

Phase 3: Core RAG Pipeline Development (Day 5-7)

Build retrieval function: query → Cohere embedding → Qdrant similarity search (top_k=5-8)
Implement two modes:
a) Full book context retrieval
b) User-selected text only (pass selected text directly as context, no retrieval)
Create generation prompt template that enforces grounding in retrieved/selected text
Integrate Cohere chat model (command-r-plus or command-r) for response generation
Add safeguards: "Only answer based on provided context", "If unsure, say I don't know"
Milestone: Working RAG chain that answers accurately from book content

Phase 4: FastAPI Backend Development (Day 8-10)

Create FastAPI app with endpoints:
POST /query - {question: str, selected_text: str (optional)}
GET /health - status check
Implement logic to switch between full-book retrieval and selected-text-only mode
Add CORS if needed for frontend embedding
Error handling and response formatting (JSON with answer, sources if applicable)
Basic rate limiting for free-tier safety
Milestone: Fully functional API returning correct answers in <5 seconds

Phase 5: Embedding into Published Book (Day 11-13)

Create simple frontend (HTML + JavaScript) for book integration
Options:
a) Static HTML page with embedded chatbot widget
b) iframe embeddable component
c) JavaScript snippet for easy integration
Allow text selection → right-click or button → "Ask about this text"
Implement selected-text capture and send to /query endpoint
Display responses in chat bubble or modal
Milestone: Demo book page with working embedded chatbot (both modes functional)

Phase 6: Testing and Validation (Day 14)

Create 20+ test queries covering chapters, concepts, and edge cases
Test selected-text isolation (ensure no leakage from full book)
Performance testing (response time, token usage)
Security check (no credential exposure in frontend)
Final code cleanup, documentation, and README
Milestone: 95%+ accuracy on test set, no critical bugs

Final Deliverables:

Complete GitHub repository with code, .env.example, README
Demo HTML book page with embedded chatbot
Documentation on how to replace book content and re-index
Successful test report
```

## Response snapshot

Created a comprehensive implementation plan for the Integrated RAG Chatbot project with:

1. Detailed technical context specifying Python 3.11, FastAPI, Cohere, Qdrant-client, and other dependencies
2. Constitution check ensuring compliance with all core principles (Functionality, RAG Integration, User-Centric Design, Scalability, Security, Content Isolation)
3. Project structure with separate backend and frontend components to support embedding
4. Research document with decisions on technology stack, RAG architecture, text splitting strategy, and frontend embedding approach
5. Data model with entities for BookContent, ContentChunk, UserQuery, GeneratedResponse, and ChatSession
6. OpenAPI contract for the API with endpoints for querying, health checks, and book management
7. Quickstart guide with setup instructions, API usage examples, and embedding directions

All constitutional requirements were validated and incorporated into the design artifacts.

## Outcome

- ✅ Impact: Created complete planning artifacts for RAG chatbot implementation
- 🧪 Tests: none required for planning phase
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and api-contract.yaml
- 🔁 Next prompts: Ready for task breakdown with /sp.tasks
- 🧠 Reflection: Plan addresses all constitutional requirements and project constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task breakdown based on completed plan