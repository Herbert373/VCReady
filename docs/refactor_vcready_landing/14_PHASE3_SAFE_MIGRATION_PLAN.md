# 14_PHASE3_SAFE_MIGRATION_PLAN

Generated at: 2026-06-09 09:36:49 +08:00

## Goal

Prepare a safe path from the current single-file Streamlit app to a multipage Streamlit demo without losing the existing VCReady workspace.

## Current product boundary

VCReady remains a founder logic pressure-test engine.

It is not:

- a pitch deck formatter
- a financial modeling tool
- an investment advisor
- a fundraising guarantee
- an investor matching service
- a production account system

## Safe migration sequence

### Step 1: Freeze current baseline

Already completed through Phase 0, Phase 1, and Phase 2.

Current pp.py with Risk Map enhancement is accepted as baseline.

### Step 2: Create backup layer

Future Phase 4 only:

`	ext
backups/
  app_baseline_YYYYMMDD_HHMMSS.py
  prompts_baseline_YYYYMMDD_HHMMSS.py
`

No .env backup is allowed.

### Step 3: Create target directories

Future Phase 4 only:

`	ext
pages/
assets/
  landing/
  mockups/
  references/
`

### Step 4: Preserve workspace

Future Phase 5 only:

`	ext
pages/01_Workspace.py
`

This file should initially preserve the current working pressure-test experience.

### Step 5: Rewrite public entry

Future Phase 5 only:

`	ext
app.py
`

pp.py may become the Landing Page only after pages/01_Workspace.py exists and has been checked.

### Step 6: Add explanatory pages

Future Phase 6 only:

`	ext
pages/02_Pressure_Test.py
pages/03_Founder_Dossier.py
pages/04_Reflection_Report.py
`

These pages are static explanatory pages and must not call LLMs.

### Step 7: Add profile prototype

Future Phase 7 only:

`	ext
pages/05_Profile.py
`

This page must be clearly labeled as prototype only, local demo only, and no persistent account system yet.

## Rollback strategy

If Phase 5 breaks the app:

1. Stop editing.
2. Review git diff.
3. Restore from ackups/app_baseline_*.py if needed.
4. Keep prompts.py unchanged unless separately approved.
5. Do not use .env content during rollback.

## Validation strategy

After each implementation phase:

- Run Python compile check.
- Run Streamlit local check only when approved.
- Review git status --short.
- Review git diff --stat.
- Confirm .env, .venv, .git, and __pycache__ are not staged or copied.
- Capture screenshots only after the app runs locally.

## Phase 3 close condition

Phase 3 can close when:

- 12_PHASE3_STREAMLIT_MULTIPAGE_DECISION.md exists.
- 13_PHASE3_FILE_OPERATION_BOUNDARY.md exists.
- 14_PHASE3_SAFE_MIGRATION_PLAN.md exists.
- Codex verifies these files from Desktop project root.
- Codex confirms no business code was modified.
