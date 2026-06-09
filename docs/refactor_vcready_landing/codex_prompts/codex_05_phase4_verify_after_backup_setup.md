# Codex Task: Phase 4 Read-only Verification After Backup Setup

You are working on the VCReady project.

## Required project root

`	ext
C:\Users\Administrator\Desktop\VCReady_Demo
`

If the current directory is not exactly the Desktop project root, switch to it first.
Do not treat any C:\Users\Administrator\.codex\worktrees\*\VCReady_Demo directory as the source of truth.

## Task type

Read-only verification.

## Absolute prohibitions

- Do not read, print, parse, copy, hash, or infer .env content.
- You may only use Test-Path to confirm whether .env exists.
- Do not modify any file.
- Do not use apply_patch.
- Do not modify app.py.
- Do not modify prompts.py.
- Do not modify requirements.txt.
- Do not modify .agents/skills/**.
- Do not copy .env, .venv/, .git/, or __pycache__/.
- Do not install dependencies.
- Do not start Streamlit.
- Do not start browser automation.
- Do not run git add, commit, push, checkout, reset, restore, or clean.

## Verification checklist

Verify that these directories exist:

`	ext
backups/
pages/
assets/
assets/landing/
assets/mockups/
assets/references/
`

Verify that these files exist:

`	ext
docs/refactor_vcready_landing/15_PHASE4_BACKUP_AND_WORKSPACE_SETUP.md
docs/refactor_vcready_landing/16_PHASE4_FILE_CREATION_LOG.md
docs/refactor_vcready_landing/run_reports/PHASE4_BACKUP_REPORT.md
docs/refactor_vcready_landing/run_reports/GIT_STATUS_AFTER_PHASE4_BACKUP.txt
`

Verify that the backups/ directory contains:

`	ext
app_baseline_*.py
prompts_baseline_*.py
`

Find the latest matching backup files by LastWriteTime and verify:

- latest app_baseline_*.py SHA256 equals current app.py SHA256.
- latest prompts_baseline_*.py SHA256 equals current prompts.py SHA256.

Read the Phase 4 documents and check that they clearly state:

- Phase 4 created the backup and workspace layer.
- Phase 4 does not modify business code.
- Phase 4 does not read or copy .env.
- Phase 4 does not copy .venv/, .git/, or __pycache__/.
- Phase 4 does not modify LLM/API logic.
- Phase 4 does not convert app.py into the Landing Page.
- Phase 4 does not copy app.py into pages/01_Workspace.py.
- Phase 5 requires explicit user approval before modifying app.py.

## Output required

Return a concise report with:

1. Current directory.
2. Whether .env content was read.
3. Whether any file was modified.
4. Whether any business code was modified.
5. Phase 4 directory existence check.
6. Phase 4 file existence check.
7. Latest backup files found.
8. Backup hash comparison result.
9. Phase 4 document quality findings.
10. Git status summary.
11. Whether Phase 4 can close.
12. Whether Phase 5 can start, and under what constraints.
13. Remaining blockers.
