# Codex Task: Phase 2 Read-only Verification After Document Landing

## Absolute project root

`C:\Users\Administrator\Desktop\VCReady_Demo`

If your current directory is not this path, switch to it before doing anything else. Do not treat any `.codex\worktrees\*\VCReady_Demo` path as the source of truth.

## Task type

Read-only verification.

## Required safety rules

- Do not modify any file.
- Do not use `apply_patch`.
- Do not read, print, parse, copy, or infer `.env` content.
- Do not modify `app.py`.
- Do not modify `prompts.py`.
- Do not modify `requirements.txt`.
- Do not create `pages/`.
- Do not create `backups/`.
- Do not copy `.venv`, `.git`, or `__pycache__`.
- Do not install dependencies.
- Do not launch Streamlit or a browser.
- Do not run `git add`, `git commit`, or `git push`.

## Files to verify

Confirm these files exist:

- `docs/refactor_vcready_landing/09_PHASE2_FINAL_PAGE_BLUEPRINT.md`
- `docs/refactor_vcready_landing/10_PHASE2_VISUAL_SYSTEM_LOCK.md`
- `docs/refactor_vcready_landing/11_PHASE2_COPY_LOCK.md`
- `docs/refactor_vcready_landing/run_reports/PHASE2_DOC_LANDING_REPORT.md`
- `docs/refactor_vcready_landing/run_reports/GIT_STATUS_AFTER_PHASE2_DOC_LANDING.txt`

You may read these files and the Phase 1 docs under `docs/refactor_vcready_landing/` for consistency checks.

## Verification criteria

Check whether the Phase 2 docs clearly lock:

1. VCReady as a founder logic pressure-test engine.
2. Landing Page and Workspace role separation.
3. Workspace preservation and Risk Map baseline acceptance.
4. Feature Pages as explanatory pages only.
5. Profile Prototype as static prototype only.
6. No promise of fundraising outcome, investment advice, login, database, investor matching, or production-grade persistence.
7. Warm public landing visual system and darker VC memo workspace system.
8. Locked hero copy, CTA copy, feature copy, and disclaimer copy.
9. Phase 3 entry gate requiring explicit user approval before any code or directory restructuring.

## Output format

Return a concise report with:

1. Current directory.
2. Whether `.env` content was read.
3. Whether any file was modified.
4. Whether any business code was modified.
5. Phase 2 file existence check.
6. Documentation quality issues, if any.
7. Git status summary.
8. Whether Phase 2 can close.
9. Whether Phase 3 can start and under what constraints.
