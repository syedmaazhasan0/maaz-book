---
id: 001
title: Implement Selected-Text Capture and Send
stage: spec
date: 2025-12-19
surface: agent
model: gemini-1.5-flash
feature: selected-text-capture
branch: main
user: user
command: "Implement selected-text capture and send"
labels: ["feature-request", "frontend", "text-selection"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - history/prompts/selected-text-capture/001-implement-selected-text-capture-and-send.spec.prompt.md
tests:
  - n/a
---

## Prompt

Implement selected-text capture and send

## Response snapshot

I understand you want to implement a feature to "capture and send selected text". To make sure I build this correctly, could you please provide a few more details?

1.  **Where will the user be selecting the text from?** (e.g., from the main document content, a specific text area, etc.)
2.  **What should happen after the text is "sent"?** (e.g., should it be sent to the chat as a new message, used to query a service, etc.)
3.  **Is there a specific UI element you have in mind for this?** (e.g., a button that appears when text is selected, a context menu option, etc.)

Once I have a clearer picture of your requirements, I can proceed with creating a specification and implementing the feature.

## Outcome

- ✅ Impact: Clarified user request for a new feature and initiated the specification process.
- 🧪 Tests: n/a
- 📁 Files: history/prompts/selected-text-capture/001-implement-selected-text-capture-and-send.spec.prompt.md
- 🔁 Next prompts: User to provide clarification on the desired implementation.
- 🧠 Reflection: Creating a PHR to track the new feature request and asking clarifying questions before proceeding with implementation.

## Evaluation notes (flywheel)

- Failure modes observed: n/a
- Graders run and results (PASS/FAIL): n/A
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
