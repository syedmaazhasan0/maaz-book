# Tasks: AI/Spec-Driven Book Creation + Embedded RAG Chatbot

**Input**: Design documents from `/specs/1-ai-robotics-book/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification did not explicitly request test-driven development, so test tasks are integrated as validation steps within the implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`, `docs/`
- Paths shown below assume this web app structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project folder structure: `docs/`, `frontend/`, `backend/`, `.github/workflows/`
- [ ] T002 Initialize Git repository and connect to remote (if not already done)
- [ ] T003 Install Node.js (LTS), Python 3.10+, Docusaurus CLI, and required project dependencies (package.json, requirements.txt) in `frontend/` and `backend/` respectively
- [ ] T004 Configure environment variables for OpenAI API keys and Qdrant Cloud (create `.env.example` in `backend/` and `frontend/`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Set up a working Docusaurus scaffold in `frontend/` using the official template
- [ ] T006 Plan the chapter structure (10–15 chapters) covering Docusaurus, MDX, and RAG concepts in a temporary outline file (e.g., `docs/chapter-outline.md`)
- [ ] T007 Set up FastAPI project structure with basic `main.py`, `routers/`, `models/`, and `services/` in `backend/`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Book Reader Browses Content (Priority: P1) 🎯 MVP

**Goal**: Enable users to navigate and read the technical content of the book.

**Independent Test**: User can access the deployed Docusaurus site, navigate between chapters, read content, and view code snippets without issues.

### Implementation for User Story 1

- [ ] T008 [P] [US1] Write Chapter 1 (Introduction & Project Overview) in `docs/chapter1.mdx`
- [ ] T009 [P] [US1] Write Chapter 2 (Environment Setup) in `docs/chapter2.mdx`
- [ ] T010 [P] [US1] Write Chapter 3 (Creating a Docusaurus Project) in `docs/chapter3.mdx`
- [ ] T011 [US1] Ensure all MDX files render correctly and are consistent in style and format by running `npm start` in `frontend/`
- [ ] T012 [P] [US1] Add placeholders for diagrams, screenshots, and other visuals in `docs/` chapters (e.g., `docs/chapter1.mdx`)
- [ ] T013 [US1] Update `sidebars.js` in `frontend/sidebars.js` to match the planned chapter order and navigation flow
- [ ] T014 [US1] Configure Docusaurus theme, navbar, footer, and layout in `frontend/docusaurus.config.js` and `frontend/src/css/custom.css`
- [ ] T015 [US1] Set up GitHub Pages deployment workflow in `.github/workflows/deploy.yml` based on Docusaurus best practices
- [ ] T016 [US1] Build the Docusaurus site using `npm run build` in `frontend/`
- [ ] T017 [US1] Publish the Docusaurus site to GitHub Pages by pushing to the configured branch
- [ ] T018 [US1] Validate deployed site navigation, formatting, internal links, and MDX rendering on GitHub Pages

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Book Reader Asks General Questions (Priority: P1)

**Goal**: Allow users to ask general questions about the book's content via an integrated chatbot.

**Independent Test**: User can open the chatbot, ask a general question about the book, and receive an accurate answer.

### Implementation for User Story 2

- [ ] T019 [P] [US2] Implement FastAPI endpoint for embedding book content into Qdrant in `backend/src/api/embeddings.py`
- [ ] T020 [P] [US2] Implement FastAPI endpoint for retrieving relevant content based on user query in `backend/src/api/retrieval.py`
- [ ] T021 [P] [US2] Implement FastAPI endpoint for chat generation via OpenAI Agents in `backend/src/api/chat.py`
- [ ] T022 [US2] Chunk book content (e.g., from `docs/chapter1.mdx`) and generate embeddings using OpenAI SDK in `backend/src/services/embedding_service.py`
- [ ] T023 [US2] Upload generated embeddings to Qdrant Cloud Free Tier with proper metadata (e.g., chapter ID, chunk text) using `backend/src/services/qdrant_service.py`
- [ ] T024 [US2] Implement retrieval pipeline from Qdrant to FastAPI, returning top matches based on query vector in `backend/src/services/retrieval_service.py`
- [ ] T025 [US2] Integrate retrieved context with OpenAI Agent for answer generation in `backend/src/services/chat_service.py`
- [ ] T026 [US2] Create a basic React-based chatbot component in `frontend/src/components/Chatbot.js`
- [ ] T027 [P] [US2] Add UI elements to `frontend/src/components/Chatbot.js`: chat window, message list, input box, loading states
- [ ] T028 [US2] Integrate `frontend/src/components/Chatbot.js` with FastAPI endpoints (`/retrieve`, `/chat`) for sending queries and receiving responses
- [ ] T029 [US2] Configure CORS and environment settings in `backend/src/main.py` for backend-frontend communication
- [ ] T030 [US2] Test backend endpoints locally using sample requests (e.g., via `curl` or `Postman`)
- [ ] T031 [US2] Test the chatbot in the local Docusaurus environment (`npm start` in `frontend/`) by asking general book-related questions and validating accuracy

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Book Reader Gets Contextual Answers (Priority: P2)

**Goal**: Enable users to select specific text and ask the chatbot questions *only* on that selection.

**Independent Test**: User can highlight text, trigger a contextual query, and receive an answer strictly limited to the selected text.

### Implementation for User Story 3

- [ ] T032 [US3] Implement user-selected text feature in backend API (`backend/src/api/chat.py`) to prioritize selected text over full retrieval
- [ ] T033 [US3] Implement logic for handling user-selected text in frontend queries (`frontend/src/components/Chatbot.js`) by capturing selected text and sending it with the chat request
- [ ] T034 [US3] Test the chatbot in the local Docusaurus environment by selecting text within a chapter and asking contextual questions, verifying answers are limited to the selected text

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Book Author Maintains System (Priority: P3)

**Goal**: Provide clear and reproducible steps for authors to update and deploy the system.

**Independent Test**: Author can follow documentation to update content, rebuild, and redeploy, verifying continuous system functionality.

### Implementation for User Story 4

- [ ] T035 [US4] Document all API routes with OpenAPI/Swagger in `backend/docs/api_docs.md` (generate from FastAPI app)
- [ ] T036 [US4] Finalize deployment steps for GitHub Pages (update `frontend/docs/deployment.mdx`) and backend (create `backend/docs/deployment.mdx`) within the book content itself
- [ ] T037 [US4] Prepare a user guide for interacting with the chatbot and book as a new chapter in `docs/chapterN-user-guide.mdx`
- [ ] T038 [US4] Verify the entire project (Docusaurus site, FastAPI backend, Qdrant setup) works in a clean environment for reproducibility (e.g., by following documented setup steps)

---

## Phase 7: Finalization & Quality Assurance

**Purpose**: Cross-cutting improvements and final validation.

- [ ] T039 Test all chapters for clarity, formatting, and reproducibility (review against content requirements)
- [ ] T040 Test backend API endpoints for correctness and performance (stress testing, edge cases)
- [ ] T041 Test chatbot accuracy using both full book content queries and user-selected text queries across all chapters
- [ ] T042 Fix any broken links, errors, or inconsistencies found in the Docusaurus site or code examples
- [ ] T043 Perform final proofreading and polish chapter content across all `docs/` MDX files
- [ ] T044 Ensure all code examples are runnable, well-documented, and copy-paste ready
- [ ] T045 Confirm project meets all success criteria defined in `specs/1-ai-robotics-book/spec.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Depends on US1 for Docusaurus site to embed chatbot, but core RAG logic can be developed in parallel.
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US2 for core RAG chatbot functionality.
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Depends on US1, US2, US3 for documenting the complete system.

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority (or integrating with next story if sequential)

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Once Foundational phase completes, User Story 1 and the core backend development aspects of User Story 2 can begin with some parallelism (e.g., Docusaurus site build and core FastAPI development).
- Tasks marked [P] within a user story can run in parallel.
- Different user stories can be worked on in parallel by different team members once their dependencies are met.

---

## Parallel Example: User Story 1

```bash
# Launch multiple chapter writing tasks in parallel:
Task: "Write Chapter 1 (Introduction & Project Overview) in docs/chapter1.mdx"
Task: "Write Chapter 2 (Environment Setup) in docs/chapter2.mdx"
Task: "Write Chapter 3 (Creating a Docusaurus Project) in docs/chapter3.mdx"

# Or, for configuring Docusaurus:
Task: "Configure Docusaurus theme, navbar, footer, and layout in frontend/docusaurus.config.js"
Task: "Set up GitHub Pages deployment workflow in .github/workflows/deploy.yml"
```

---

## Parallel Example: User Story 2 (Backend Development)

```bash
# Launch backend endpoint implementation in parallel:
Task: "Implement FastAPI endpoint for embedding book content into Qdrant in backend/src/api/embeddings.py"
Task: "Implement FastAPI endpoint for retrieving relevant content based on user query in backend/src/api/retrieval.py"
Task: "Implement FastAPI endpoint for chat generation via OpenAI Agents in backend/src/api/chat.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (Integrated general chatbot)
4. Add User Story 3 → Test independently → Deploy/Demo (Contextual chatbot)
5. Add User Story 4 → Test independently → Deploy/Demo (Author maintenance)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together.
2. Once Foundational is done:
   - Developer A: User Story 1 (Docusaurus site and initial content)
   - Developer B: User Story 2 (FastAPI backend for RAG and Qdrant integration)
   - Developer C: User Story 3 (Enhance chatbot with contextual querying)
   - Developer D: User Story 4 (Documentation and deployment finalization)
3. Stories complete and integrate independently.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tasks are working as expected after completion
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
