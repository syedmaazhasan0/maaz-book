---
id: 1
title: Integrated RAG Chatbot Constitution
stage: constitution
date: 2025-12-20
surface: agent
model: Qwen
feature: none
branch: main
user: Maaz Hassan
command: /sp.constitution
labels: ["constitution","rag","chatbot","specifykit"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution Project: Integrated RAG Chatbot Development: Build and embed a Retrieval-Augmented Generation (RAG) chatbot within a published book. This chatbot, utilizing SpecifyKit Plus, Gemini CLI, Coherent API, FastAPI, and Qdrant Cloud Free Tier, must be able to answer user questions about the book's content, including answering questions based only on text selected by the user.
Core principles:

Functionality and reliability in handling book-specific queries
Integration of RAG for accurate, context-aware responses
User-centric design for seamless text selection and querying
Scalability using free-tier services without compromising performance
Security in data handling and API interactions

Key standards:

All responses must be derived from the book's content or user-selected text
Code quality: Follow PEP 8 for Python, with modular and readable structure
API usage: Exclusively use Coherent API for generation tasks, avoiding OpenAI
Testing: Unit tests for core components (retrieval, generation, embedding)
Documentation: Inline comments and a README with setup instructions
Error handling: Graceful failures with user-friendly messages

Constraints:

Tools: SpecifyKit Plus for project management, Gemini CLI for development workflows, Coherent API for AI generation, FastAPI for backend, Qdrant Free Tier for vector storage
No external paid services beyond free tiers
Deployment: Embeddable in a published book format (e.g., web or app integration)
Performance: Response time under 5 seconds for typical queries
Compatibility: Cross-platform support (web, mobile if applicable)

Success criteria:

Chatbot accurately answers 95% of test queries based on book content
Handles user-selected text isolation without external context leakage
Zero critical bugs in production-like testing
Passes code review for best practices and tool adherence
Successful embedding and demo in a sample book publication
```

## Response snapshot

Created a comprehensive constitution for the Integrated RAG Chatbot project with six core principles, key standards, constraints, and success criteria. The constitution includes:

1. Core Principles:
   - Functionality and Reliability
   - RAG Integration
   - User-Centric Design
   - Scalability with Free-Tier Services
   - Security in Data Handling
   - Content Isolation

2. Key Standards covering content accuracy, code quality, API usage, testing, documentation, and error handling.

3. Constraints specifying technology stack, service limitations, deployment requirements, performance standards, and compatibility.

4. Success Criteria defining query accuracy, text isolation, quality assurance, code review, and demonstrable integration.

5. Governance section with version information and amendment procedures.

## Outcome

- ✅ Impact: Created foundational governance document for RAG chatbot project
- 🧪 Tests: none required for constitution creation
- 📁 Files: Updated .specify/memory/constitution.md with project-specific details
- 🔁 Next prompts: Build specification based on updated constitution
- 🧠 Reflection: Constitution provides clear direction and constraints for development team

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin building specification based on constitution