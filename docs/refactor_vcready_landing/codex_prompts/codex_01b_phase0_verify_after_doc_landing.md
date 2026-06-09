# VCReady Codex Task: Phase 0 Verification After User-Side Doc Landing

## Absolute project root

`	ext
C:\Users\Administrator\Desktop\VCReady_Demo
`

## Task type

Read-only verification.

## Background

During Phase 0 retry, Codex successfully switched to the Desktop project root and completed read-only audit, but writing the Phase 0 documents was blocked because pply_patch approval returned 503 Service Unavailable.

The user-side PowerShell script has now written the required Phase 0 files. Your task is only to verify them.

## Required steps

1. Switch to:

`	ext
C:\Users\Administrator\Desktop\VCReady_Demo
`

2. Confirm the current directory.

3. Confirm these files exist:

`	ext
docs/refactor_vcready_landing/00_BASELINE_FREEZE.md
docs/refactor_vcready_landing/01_CURRENT_PROJECT_MAP.md
docs/refactor_vcready_landing/run_reports/CODEX_PHASE0_READONLY_AUDIT.md
`

4. Read only the three files listed above and summarize whether they satisfy Phase 0.

5. Check whether .env exists without reading its content.

6. Run:

`powershell
git status --short
`

7. Output:

- Whether current directory is the Desktop project root.
- Whether the three Phase 0 files exist.
- Whether .env content was read.
- Whether any business code was modified in this verification task.
- Git status summary.
- Whether Phase 0 can be closed.
- Whether Phase 1 may begin.
- Any blocking issues.

## Forbidden operations

- Do not read .env.
- Do not modify pp.py.
- Do not modify prompts.py.
- Do not modify equirements.txt.
- Do not modify any file.
- Do not use pply_patch.
- Do not run Git add / commit / push.
- Do not install dependencies.
- Do not start a browser.
- Do not use the .codex\worktrees directory as the project root.
