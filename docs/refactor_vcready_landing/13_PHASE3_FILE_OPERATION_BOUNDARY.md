# 13_PHASE3_FILE_OPERATION_BOUNDARY

Generated at: 2026-06-09 09:36:49 +08:00

## Purpose

This document locks the file-operation boundary before directory creation, backup, page migration, or landing-page implementation.

## Always protected

| Path | Rule |
|---|---|
| .env | Existence check only. Never read, print, parse, copy, or infer content. |
| .venv/ | Never copy into refactor packages. |
| .git/ | Never expand or copy. |
| __pycache__/ | Ignore generated cache. |
| .agents/skills/** | Do not modify. |
| prompts.py | Read-only unless the user explicitly opens a prompt refactor phase. |
| equirements.txt | Read-only unless the user explicitly approves dependency changes. |

## Current baseline file

| Path | Current status | Phase 3 rule |
|---|---|---|
| pp.py | Modified by accepted Risk Map enhancement | Do not modify in Phase 3. Treat as accepted baseline. |

## Phase 3 allowed operations

Only these operations are allowed in Phase 3:

- Create or update markdown documents under docs/refactor_vcready_landing/
- Create or update Codex task files under docs/refactor_vcready_landing/codex_prompts/
- Create run reports under docs/refactor_vcready_landing/run_reports/
- Run readonly checks
- Save git status --short output into run reports

## Phase 3 forbidden operations

- Modify pp.py
- Modify prompts.py
- Modify equirements.txt
- Create pages/
- Create ackups/
- Create ssets/landing/
- Copy pp.py
- Copy prompts.py
- Move files
- Delete files
- Install dependencies
- Start Streamlit
- Commit or push

## Phase 4 proposed allowed operations

Only after explicit user approval, Phase 4 may:

- Create ackups/
- Create pages/
- Create ssets/landing/
- Create ssets/mockups/
- Create ssets/references/
- Copy current pp.py to timestamped backup
- Copy current prompts.py to timestamped backup
- Save git diff -- app.py before migration

Phase 4 still should not rewrite business logic.

## Phase 5 proposed allowed operations

Only after explicit user approval, Phase 5 may:

- Copy current workspace logic into pages/01_Workspace.py
- Rewrite pp.py as Public Landing Page
- Keep prompts.py unchanged
- Keep LLM/API behavior unchanged
- Keep Risk Map enhancement available in the workspace route

## Required confirmation before Phase 5

Before Phase 5, the user must approve:

1. Whether to create pages/01_Workspace.py
2. Whether to rewrite pp.py
3. Whether the current pp.py baseline should be backed up again
4. Whether landing page implementation should be static only
5. Whether feature pages remain non-LLM explanatory pages
