# Codex Current Task: Phase 3 Read-only Verification After Document Landing

You are working on VCReady.

This round is Phase 3 read-only verification after the user-side PowerShell document landing.

## Required working directory

Use this project root as the source of truth:

```text
C:\Users\Administrator\Desktop\VCReady_Demo
```

If your current directory is not the path above, switch to it before doing anything else.

Do not treat any `C:\Users\Administrator\.codex\worktrees\*\VCReady_Demo` path as the main project root.

## Absolute safety rules

- Do not read, print, parse, copy, or infer `.env` content.
- You may only use `Test-Path` or equivalent existence checks for `.env`.
- Do not modify any file.
- Do not use `apply_patch`.
- Do not modify `app.py`.
- Do not modify `prompts.py`.
- Do not modify `requirements.txt`.
- Do not modify `.agents/skills/**`.
- Do not expand or copy `.git/`.
- Do not copy `.venv/`.
- Do not copy `__pycache__/`.
- Do not install dependencies.
- Do not start Streamlit.
- Do not launch a browser.
- Do not run git add, commit, push, checkout, restore, reset, merge, rebase, or clean.

## Files to verify

Verify that these Phase 3 files exist:

```text
docs/refactor_vcready_landing/12_PHASE3_STREAMLIT_MULTIPAGE_DECISION.md
docs/refactor_vcready_landing/13_PHASE3_FILE_OPERATION_BOUNDARY.md
docs/refactor_vcready_landing/14_PHASE3_SAFE_MIGRATION_PLAN.md
docs/refactor_vcready_landing/run_reports/PHASE3_DOC_LANDING_REPORT.md
docs/refactor_vcready_landing/run_reports/GIT_STATUS_AFTER_PHASE3_DOC_LANDING.txt
```

Then read only these Phase 3 markdown/report files for quality verification:

```text
docs/refactor_vcready_landing/12_PHASE3_STREAMLIT_MULTIPAGE_DECISION.md
docs/refactor_vcready_landing/13_PHASE3_FILE_OPERATION_BOUNDARY.md
docs/refactor_vcready_landing/14_PHASE3_SAFE_MIGRATION_PLAN.md
docs/refactor_vcready_landing/run_reports/PHASE3_DOC_LANDING_REPORT.md
```

Do not edit them.

## Quality checks

Confirm whether the Phase 3 documents clearly lock the following:

1. Streamlit multipage is the preferred path.
2. `app.py` is not modified in Phase 3.
3. `prompts.py` is not modified in Phase 3.
4. `requirements.txt` is not modified in Phase 3.
5. `.env`, `.venv`, `.git`, `__pycache__`, and `.agents/skills/**` remain protected.
6. `backups/`, `pages/`, and `assets/landing/` are not created during Phase 3 unless a later phase explicitly allows it.
7. Copying `app.py` to `pages/01_Workspace.py` is not performed in Phase 3.
8. Phase 4 is the earliest phase allowed to create backup/page/asset directories.
9. Phase 5 is the earliest phase allowed to modify `app.py` into a Landing Page.
10. The current `app.py` Risk Map enhancement is treated as accepted baseline.
11. Rollback boundaries and allowed/disallowed file operations are explicit enough for later implementation.

## Git status

Run read-only Git status only:

```text
git status --short
```

Do not run any Git command that changes repository state.

## Required response format

Reply with:

1. Current directory.
2. Whether `.env` content was read.
3. Whether any file was modified.
4. Whether any business code was modified.
5. Phase 3 file existence check.
6. Phase 3 document quality findings.
7. Git status summary.
8. Whether Phase 3 can close.
9. Whether Phase 4 can start, and under what constraints.
10. Any blockers.
