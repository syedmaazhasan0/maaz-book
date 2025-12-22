---
id: 001
title: Implement Selected Text Capture and Send
stage: spec
date: 2025-12-19
surface: agent
model: gemini-1.5-flash
feature: selected-text-feature
branch: main
user: user
command: Implement selected-text capture and send
labels: ["feature-request", "frontend", "interaction"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - history/prompts/selected-text-feature/001-implement-selected-text-capture-and-send.spec.prompt.md
tests:
  - n/a
---

## Prompt

Implement selected-text capture and send

## Response snapshot

To clarify, could you please specify the following for the "selected-text capture and send" feature:

1.  **Where** should text selection be enabled (e.g., across the entire documentation, only within specific content blocks, etc.)?
2.  **What action** should trigger the "send" (e.g., a button click after selection, automatically upon selection, a context menu option)?
3.  **What should happen to the captured text** when it's "sent" (e.g., send it to a backend API for processing, display it in a popup, copy it to clipboard)?

## Outcome

- ✅ Impact: Initiated clarification for a new feature, "selected-text capture and send".
- 🧪 Tests: n/a
- 📁 Files: history/prompts/selected-text-feature/001-implement-selected-text-capture-and-send.spec.prompt.md created.
- 🔁 Next prompts: User to provide clarification on the desired functionality.
- 🧠 Reflection: Clarifying broad feature requests before proceeding is essential for efficient development.

## Evaluation notes (flywheel)

- Failure modes observed: n/a
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a