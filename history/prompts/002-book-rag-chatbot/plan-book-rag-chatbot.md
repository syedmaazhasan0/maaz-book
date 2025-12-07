---
id: PHR-0003
title: Book RAG Chatbot Planning
stage: plan
date: 2025-12-06
surface: agent
model: claude-haiku-4-5-20251001
feature: book-rag-chatbot
branch: 002-book-rag-chatbot
user: Maaz Hassan
command: /sp.plan
labels: ["planning", "architecture", "ai", "rag", "docusaurus", "fastapi"]
links:
  spec: specs/002-book-rag-chatbot/spec.md
  plan: specs/002-book-rag-chatbot/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - "specs/002-book-rag-chatbot/plan.md"
 - "specs/002-book-rag-chatbot/research.md"
 - "specs/002-book-rag-chatbot/data-model.md"
 - "specs/002-book-rag-chatbot/quickstart.md"
 - "specs/002-book-rag-chatbot/contracts/rag-api.yaml"
 - ".specify/memory/constitution.md"
tests:
 - "none"
---

## Prompt

now based on this write a plan file on the following data:
Project: AI/Spec-Driven Book Creation + Embedded RAG Chatbot

Overview:
This project will produce a complete technical book written in MDX, built with Docusaurus, deployed to GitHub Pages, and integrated with a fully functional Retrieval-Augmented Generation (RAG) chatbot. The chatbot will use OpenAI Agents/ChatKit SDKs, FastAPI, and Qdrant Cloud Free Tier, and will be embedded into the deployed Docusaurus site. It will answer questions about the book and provide responses based solely on text selected by the user.

Plan Phases:

Phase 1 — Foundation & Setup
1. Define project structure according to SpeckitPlus (constitution, specifications, blueprint).
2. Create the Docusaurus project scaffold.
3. Initialize GitHub repository and connect it to the Docusaurus project.
4. Configure environment: Node.js (LTS), Python 3.10+, Qdrant Cloud account, OpenAI API keys.
5. Establish folder structure for:
   - /docs (book chapters)
   - /backend (FastAPI RAG server)
   - /frontend (chatbot component embedded into Docusaurus)

Phase 2 — Book Development (MDX)
1. Create a 10–15 chapter outline covering:
   - Docusaurus basics
   - MDX writing
   - GitHub Pages deployment
   - RAG concepts
   - FastAPI backend development
   - Qdrant integration
   - Chatbot UI embedding
   - User-selected text retrieval pipeline
2. Write each chapter in MDX with:
   - Learning objectives
   - Step-by-step instructions
 build issues.

Phase 3 — Docusaurus Customization & Deployment
1. Configure Docusaurus theme, navbar, footer, and layout.
2. Add custom components needed for chatbot embedding.
3. Set up GitHub Pages deployment using:
   - docusaurus.config.js
   - GitHub Actions workflow
4. Test deployment:
   - Run `npm run build`
   - Publish live site on GitHub Pages
5. Validate navigation, formatting, internal links, and MDX rendering.

Phase 4 — RAG Backend Development (FastAPI + Qdrant)
1. Create a FastAPI project folder with:
   - Retrieval routes
   - Embedding routes
   - Chat completion routes
2. Connect FastAPI backend to Qdrant Cloud Free Tier.
3. Build embedding pipeline:
   - Chunking MDX content
   - Generating embeddings using OpenAI SDK
   - Uploading vectors to Qdrant
4. Implement retrieval logic:
   - Query Qdrant
   - Return top matches
5. Implement generation:
   - Combine retrieved context + user query
   - Send to OpenAI Agent/ChatKit
6. Implement user-selected text retrieval:
   - Accept text payload from frontend
   - Skip vector search when selection exists
7. Add CORS, environment variables, and API docs (Swagger/OpenAPI).

Phase 5 — Chatbot Frontend (Docusaurus Integration)
1. Create React-based chatbot widget.
2. Add UI features:
   - Chat window
   - Input box
   - Response rendering
   - “Use selected text only” mode
3. Implement logic:
   - Send queries to FastAPI backend
   - Send user-selected text as priority context
4. Embed chatbot component into Docusaurus:
   - Custom page
   - Floating widget or sidebar integration
5. Test interaction:
   - Ask questions about book content
   - Ask questions based on selected text

Phase 6 — Testing, Debugging, and Validation
1. Test Docusaurus build and GitHub Pages deployment.
2. Test FastAPI backend in local + cloud environments.
3. Validate Qdrant indexing and retrieval accuracy.
4. Test chatbot across various scenarios:
   - Book content questions
   - Selected text questions
   - Edge cases with empty or long selections
5. Resolve build i

## Response snapshot

Created a comprehensive implementation plan for the AI/Spec-Driven Book Creation + Embedded RAG Chatbot project. The plan includes technical context, constitution compliance check, project structure, research findings, data models, quickstart guide, and API contracts. All components align with the project constitution and specification requirements.

## Outcome

- ✅ Impact: Complete implementation plan created with all required artifacts
- 🧪 Tests: none
- 📁 Files: 5 files created (plan.md, research.md, data-model.md, quickstart.md, contracts/rag-api.yaml)
- 🔁 Next prompts: Ready for task breakdown (/sp.tasks)
- 🧠 Reflection: The plan comprehensively addresses both frontend (Docusaurus book) and backend (RAG chatbot) components with proper separation of concerns.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with task breakdown phase