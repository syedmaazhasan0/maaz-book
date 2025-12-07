---
id: PHR-0001
title: Constitution Update for AI Book Project
stage: constitution
date: 2025-12-06
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: 1-ai-robotics-book
user: Maaz Hassan
command: /sp.constitution
labels: ["constitution", "documentation", "project-standards", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - ".specify/memory/constitution.md"
tests:
 - "none"
---

## Prompt

Write a constituion file on the following data:
Project: AI/Spec-Driven Book Creation with Integrated RAG Chatbot

Core principles:
- Technical accuracy based strictly on official documentation (Docusaurus, GitHub Pages, OpenAI Agents/ChatKit SDKs, FastAPI, Qdrant Cloud).
- Clarity and accessibility for beginner-to-intermediate developers.
- Modular, reproducible, and implementation-focused content.
- Reliability: all code, configurations, and examples must be fully testable and operational.
- Integration-first approach: book content and the RAG chatbot architecture must align seamlessly.

Key standards:
- All configuration steps, code blocks, and architecture diagrams must reflect up-to-date official tools and APIs.
- Writing quality target: Flesch-Kincaid grade 8–10 (clear, concise, instructional).
- Use MDX formatting according to Docusaurus conventions.
- Code samples must be copy–paste ready, versioned, and runnable in a clean environment.
- RAG chatbot must support:
  - Retrieval from Qdrant Cloud Free Tier
  - Answering user questions about the book
  - Answering questions based *only* on text selected by the user
  - Integration into the published Docusaurus site
- No deprecated libraries, commands, or APIs allowed.

Constraints:
- Output format: MDX files compatible with a Docusaurus `docs/` folder.
- All chatbot implementation must use:
  - OpenAI Agents or ChatKit SDKs
  - FastAPI backend
  - Qdrant Cloud Free Tier for vector storage
- All examples must run on Node.js LTS and Python 3.10+.
- Book length: 10–15 chapters, each 700–1500 words.
- Scope must include:
  1. Docusaurus setup & project scaffolding
  2. Writing and organizing book content in MDX
  3. GitHub Pages deployment
  4. Fundamentals of RAG systems
  5. FastAPI backend creation
  6. Qdrant vector database integration
  7. Embedding model integration via OpenAI SDK
  8. Frontend chatbot UI embedded within Docusaurus
  9. User-selected text → retrieval → answer pipeline
  10. Testing, debugging, and deployment of the RAG system
- All file structures, paths, configs, and APIs must be explicitly defined.

Success criteria:
- A complete Docusaurus book that builds successfully (`npm run build`) and deploys to GitHub Pages without errors.
- Fully functional RAG chatbot embedded within the deployed site.
- The chatbot must correctly answer questions based on:
  - General book content
  - User-selected text only
- All code snippets must run without modification.
- No broken links, missing files, or configuration issues.
- Documentation must be clear, consistent, and technically accurate.
- The final system must be reproducible by users following only the book.

## Response snapshot

Updated the constitution file at .specify/memory/constitution.md to reflect the project requirements for the AI/Spec-Driven Book Creation with Integrated RAG Chatbot project. The file already contained most of the required principles and standards, but I updated the version information and sync impact report to reflect today's date and the current version (1.0.1).

## Outcome

- ✅ Impact: Constitution file updated with proper versioning and dates
- 🧪 Tests: none
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: none needed
- 🧠 Reflection: The constitution file was already well-structured and aligned with requirements; only version and date updates were needed.

## Evaluation notes (flywheel)

- Failure modes observed: Script .specify/scripts/bash/create-phr.sh was not found, requiring manual PHR creation
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create the missing bash script for automated PHR creation