<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections added
Removed sections: N/A
Templates requiring updates: N/A
Follow-up TODOs: None
-->
# Hackathon_0 Constitution

## Core Principles

### I. Completeness
Every plan, task, and implementation must be fully self-contained and executable. All deliverables must include clear purpose statements, implementation instructions, and documentation.

### II. Accuracy
Follow tech stack constraints strictly (Python 3.13.5, Node v24.x, specified libraries). All implementations must adhere to the defined technology stack without deviation unless explicitly approved.

### III. Structure
Maintain clean folder/file organization with designated backend/, frontend/, docs/, specs/, and history/ directories. All AI-generated content follows the hierarchy: constitution → specify → plan → tasks → implement.

### IV. Reusability
Prompts, scripts, and modules should be modular for easy updates. Code components must be designed with reusability in mind, avoiding tight coupling where possible.

### V. Documentation
All code and AI outputs must be documented clearly with purpose and usage instructions. Every significant function, class, and module must include appropriate documentation.

### VI. Versioning
All AI-generated content and code must include version/metadata headers. Version control follows semantic versioning principles with clear changelog entries for all significant changes.

## Technology Stack Requirements
- Primary Technologies: Python (backend), Node.js (frontend/server-side scripting), React (UI)
- Optional: Docker/Kubernetes for deployment
- AI Integration: Task generation, specification planning, and automation using Claude/Qwen CLI
- Environment: Python 3.13.5, Node v24.x

## Development Workflow
- Follow Prompt Hierarchy: constitution → specify → plan → tasks → implement
- No Skipping: Every step must produce concrete outputs, not just text summaries
- Context Awareness: Maintain awareness of all previous outputs when generating new outputs
- Output Format: JSON, Markdown, or code files as per the task, with clear filenames and folder placement
- Error Handling: Provide safe defaults or explicit instructions to user for missing data
- Verification: After task generation, verify that all modules/files required for implementation exist

## File and Naming Conventions
- File Naming: Use lowercase with underscores (e.g., `todo_backend.py`)
- Folder Hierarchy: Maintain frontend/backend separation as specified in structure principle
- Code Style: Python PEP8, JavaScript/Node best practices, React conventions
- AI Tasks: All tasks must be actionable directly from CLI or automation scripts
- Completion Criteria: A task is considered complete when it is fully functional, tested locally, and documented

## Governance
This constitution serves as the authoritative reference for all Hackathon_0 development activities. All subsequent prompts (specify, plan, tasks, implement) must have a clear, consistent, and complete reference to this document. Any deviations from these principles require explicit approval and constitutional amendment.

**Version**: 1.0.0 | **Ratified**: 2026-02-16 | **Last Amended**: 2026-02-16
