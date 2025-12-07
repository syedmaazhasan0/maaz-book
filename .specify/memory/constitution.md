<!--
Sync Impact Report:
Version change: 1.0.0 → 1.0.1
Modified principles: None (content update only)
Added sections: None
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ updated
- .specify/templates/spec-template.md: ✅ updated
- .specify/templates/tasks-template.md: ✅ updated
- .specify/templates/commands/sp.phr.md: ✅ updated
- .specify/templates/commands/sp.specify.md: ✅ updated
- .specify/templates/commands/sp.plan.md: ✅ updated
- .specify/templates/commands/sp.tasks.md: ✅ updated
- .specify/templates/commands/sp.implement.md: ✅ updated
- .specify/templates/commands/sp.git.commit_pr.md: ✅ updated
- .specify/templates/commands/sp.constitution.md: ✅ updated
- .specify/templates/commands/sp.clarify.md: ✅ updated
- .specify/templates/commands/sp.checklist.md: ✅ updated
- .specify/templates/commands/sp.analyze.md: ✅ updated
- .specify/templates/commands/sp.adr.md: ✅ updated
Follow-up TODOs: None
-->
# AI/Spec-Driven Book Creation with Integrated RAG Chatbot Constitution

## Core Principles

### I. Technical Accuracy
All content, code, and configurations MUST be based strictly on official documentation for Docusaurus, GitHub Pages, OpenAI Agents/ChatKit SDKs, FastAPI, and Qdrant Cloud. No assumptions or unofficial practices are permitted.

### II. Clarity and Accessibility
Content MUST be written for beginner-to-intermediate developers, prioritizing clear, concise, and instructional language. The target writing quality is Flesch-Kincaid grade 8–10.

### III. Modularity and Reproducibility
Content and code MUST be modular, reproducible, and implementation-focused. All examples, code blocks, and configurations MUST be copy-paste ready, versioned, and runnable in a clean environment (Node.js LTS and Python 3.10+).

### IV. Operational Reliability
All code, configurations, and examples MUST be fully testable and operational. The final system MUST be reproducible by users following only the book, without encountering broken links, missing files, or configuration issues.

### V. Seamless Integration
Book content and the RAG chatbot architecture MUST align seamlessly. The integration-first approach ensures a cohesive learning and development experience.

### VI. Up-to-Date Standards
All configuration steps, code blocks, and architecture diagrams MUST reflect up-to-date official tools and APIs. Deprecated libraries, commands, or APIs are NOT permitted.

### VII. MDX Formatting
Book content MUST use MDX formatting according to Docusaurus conventions for consistent rendering and functionality.

### VIII. RAG Chatbot Functionality
The RAG chatbot MUST support retrieval from Qdrant Cloud Free Tier, answer user questions about the book, answer questions based *only* on text selected by the user, and integrate into the published Docusaurus site.

## Project Scope

### I. In Scope
The project scope MUST include:
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

### II. Constraints
All file structures, paths, configs, and APIs MUST be explicitly defined. The book length MUST be between 10–15 chapters, with each chapter containing 700–1500 words.

### III. Technologies
All chatbot implementation MUST exclusively use OpenAI Agents or ChatKit SDKs, a FastAPI backend, and Qdrant Cloud Free Tier for vector storage.

## Success Criteria

### I. Book Build and Deployment
A complete Docusaurus book that builds successfully (`npm run build`) and deploys to GitHub Pages without errors.

### II. Functional RAG Chatbot
A fully functional RAG chatbot embedded within the deployed site. The chatbot MUST correctly answer questions based on general book content and user-selected text only.

### III. Code Snippet Integrity
All code snippets provided in the book MUST run without modification and without configuration issues.

## Governance
This Constitution supersedes all other project practices and documentation. Amendments to this Constitution require a documented rationale, explicit approval from project stakeholders, and a clear migration plan for any affected components or practices. All code reviews and project deliverables MUST verify compliance with these principles and standards. Complexity introduced into the system MUST be justified against these core principles.

**Version**: 1.0.1 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-06
