---
id: 1
title: Create Hackathon 0 Project Constitution
stage: constitution
date: 2026-02-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-textbook-chatbot
user: Claude Code
command: sp.constitution
labels:
  - constitution
  - hackathon
  - governance
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/1-create-hackathon-0-project.constitution.prompt.md
tests: []
links:
  - spec: null
  - ticket: null
  - adr: null
  - pr: null
outcome: Successfully created the initial project constitution for Hackathon_0 with all core principles and guidelines
evaluation: The constitution document was created with all required sections including core principles, technology stack requirements, development workflow, and governance rules
---

# Create Hackathon 0 Project Constitution

## Prompt Text

```
sp.constitution
## Project Constitution Prompt

**Objective:**
This AI constitution defines the full scope, rules, and standards for the Hackathon_0 project. It ensures that all subsequent prompts (specify, plan, tasks, implement) have a clear, consistent, and complete reference. The AI must follow this constitution strictly during planning and implementation.

---

### 1. Project Overview
- **Project Name:** Hackathon_0
- **Project Type:** Full-stack web application (frontend + backend) with AI-assisted features
- **Primary Technologies:** Python (backend), Node.js (frontend/server-side scripting), React (UI), Docker/Kubernetes (optional for deployment)
- **AI Integration:** Task generation, specification planning, and optional automation using Claude/Qwen CLI

---

### 2. Core Principles
1. **Completeness:** Every plan, task, and implementation must be fully self-contained and executable.
2. **Accuracy:** Follow tech stack constraints strictly (Python 3.13.5, Node v24.x, specified libraries).
3. **Structure:** Maintain clean folder/file organization:
    ```
    hackathon_0/
        sp.constitution
        sp.specify
        sp.plan
        sp.tasks
        sp.implement
        backend/
        frontend/
        docs/
    ```
4. **Reusability:** Prompts, scripts, and modules should be modular for easy updates.
5. **Documentation:** All code and AI outputs must be documented clearly with purpose and usage instructions.
6. **Versioning:** All AI-generated content and code must include version/metadata headers.

---

### 3. AI Behavior Rules
- **Follow Prompt Hierarchy:** constitution → specify → plan → tasks → implement
- **No Skipping:** Every step must produce concrete outputs, not just text summaries.
- **Context Awareness:** AI must remember all previous outputs when generating new outputs.
- **Output Format:** JSON, Markdown, or code files as per the task, with clear filenames and folder placement.
- **Error Handling:** For missing data, AI must provide safe defaults or explicit instructions to user.
- **Verification:** After task generation, verify that all modules/files required for implementation exist.

---

### 4. Implementation Guidelines
- **File Naming Conventions:** Use lowercase with underscores (e.g., `todo_backend.py`).
- **Folder Hierarchy:** As described in Core Principles, maintain frontend/backend separation.
- **Code Style:** Python PEP8, JavaScript/Node best practices, React conventions.
- **AI Tasks:** All tasks must be actionable directly from CLI or automation scripts.
- **Completion Criteria:** A task is considered complete when it is fully functional, tested locally, and documented.

---

### 5. Output Requirements
- Each AI prompt output must include:
    1. **Purpose Statement** – Why this output exists
    2. **Implementation Instructions** – How to use/run
    3. **File/Folder Reference** – Where to save
    4. **Dependencies** – Required libraries or environment setup
    5. **Version Metadata** – Prompt version and date

---

### 6. Metadata
- **Constitution Version:** 1.0
- **Date:** 2026-02-16
- **Maintainer:** Hackathon_0 AI Specification
- **Applicable To:** sp.specify, sp.plan, sp.tasks, sp.implement

---

**Instruction to AI:**
Follow this constitution strictly. Use it as the reference for generating specifications, plans, task lists, and implementation steps. Ensure that no output violates the principles or structure defined here.
```

## Response Text

Successfully created the Hackathon_0 project constitution with all core principles and guidelines. The constitution includes sections for completeness, accuracy, structure, reusability, documentation, and versioning. It also specifies technology stack requirements, development workflow guidelines, file and naming conventions, and governance rules. The constitution serves as the authoritative reference for all Hackathon_0 development activities.