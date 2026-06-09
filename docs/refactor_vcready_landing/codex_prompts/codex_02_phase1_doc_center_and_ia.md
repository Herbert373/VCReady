# Codex Round 2 - Phase 1 Document Center and Information Architecture

## Project root

Use this Desktop project root as the only source of truth:

```text
C:\Users\Administrator\Desktop\VCReady_Demo
```

If the current working directory is not this path, first switch to it. Do not treat any `.codex\worktrees\*\VCReady_Demo` path as the main project root.

## Phase

Phase 1: establish the refactor documentation center and write the first planning documents.

This is still a documentation phase. Do not refactor UI code yet.

## Accepted baseline

- The current `app.py` already contains a Risk Map / 风险地图 enhancement.
- Treat this modified `app.py` state as the accepted Phase 1 baseline.
- Do not revert, rewrite, format, or optimize `app.py` in this round.
- A stray `$null` file may have been inspected or removed by the PowerShell prep script. Do not recreate it.

## Non-negotiable boundaries

Do not read, print, parse, or copy `.env`.

Do not modify:
- `app.py`
- `prompts.py`
- `requirements.txt`
- `.env`
- `.agents/skills/**`
- `.git/**`
- `.venv/**`
- `__pycache__/**`
- `portfolio_assets/screenshots/**`

Do not:
- install dependencies
- launch Streamlit
- launch browser automation
- run Git add / commit / push
- delete files unless the task explicitly asks you to do so

## Allowed reads

You may read:
- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.gitignore`
- `docs/VCReady_PRD_v0.1.md`
- `docs/VCReady_PRD_v0.2.md`
- `docs/VCReady_v0.3_Guided_Flow_Spec.md` if present
- `docs/refactor_vcready_landing/00_BASELINE_FREEZE.md`
- `docs/refactor_vcready_landing/01_CURRENT_PROJECT_MAP.md`
- `docs/refactor_vcready_landing/run_reports/*.txt`
- `docs/refactor_vcready_landing/run_reports/*.md`
- `tasks/current_commit.md` if present
- `tasks/progress_log.md` if present

You may inspect `app.py` only to understand current product structure. Do not edit it.

## Allowed writes

Only create or update files under:

```text
docs/refactor_vcready_landing/
```

Specifically create or update these files:

```text
docs/refactor_vcready_landing/02_PRODUCT_INFORMATION_ARCHITECTURE.md
docs/refactor_vcready_landing/03_VISUAL_REFERENCE_TRANSLATION.md
docs/refactor_vcready_landing/04_COPYWRITING_DRAFT.md
docs/refactor_vcready_landing/05_PHASE1_IMPLEMENTATION_PLAN.md
docs/refactor_vcready_landing/06_RISK_AND_ROLLBACK_PLAN.md
docs/refactor_vcready_landing/07_ACCEPTANCE_CHECKLIST.md
docs/refactor_vcready_landing/run_reports/CODEX_PHASE1_DOC_CENTER_AUDIT.md
```

Do not modify Phase 0 files except to read them.

## Product truth to preserve

VCReady is not a pitch-deck formatter or a financial modeling tool.

VCReady is an AI-powered VC pressure-test workspace for early-stage founders. It helps founders move from "selling the project" to defending their logic, evidence, founder-market fit, and risk awareness under investor-style questioning.

The existing dark workspace and report flow should be preserved in later implementation phases.

## Phase 1 document requirements

### 02_PRODUCT_INFORMATION_ARCHITECTURE.md

Define the future product structure:

- Public Landing Page
- Workspace
- Feature Pages
  - Pressure Test
  - Founder Dossier
  - Reflection Report
- Profile Prototype
- Report Preview

Clarify what is already real in the local demo and what is only a prototype / future concept.

### 03_VISUAL_REFERENCE_TRANSLATION.md

Translate the desired design direction into VCReady principles:

- Landing Page: warm white / cream / light gold-orange / deep gray-blue
- Workspace: keep cold dark VC memo / data room feeling
- Landing tells the story
- Workspace performs the pressure test
- Feature pages explain modules
- Profile page is prototype only

Do not reference inaccessible private screenshots as if they are in the repo.

### 04_COPYWRITING_DRAFT.md

Write bilingual or mixed Chinese-English copy for:

- Hero headline
- Hero subheadline
- Primary CTA
- Secondary CTA
- Problem section
- Feature cards
- How it works
- Report preview explanation
- Boundary / disclaimer copy

Avoid exaggerated claims. Do not promise real fundraising outcomes, investment advice, login, database, or persistent history.

### 05_PHASE1_IMPLEMENTATION_PLAN.md

Describe what Phase 1 does and does not do.

State clearly:
- Phase 1 writes documents only.
- No business code changes.
- No Streamlit multipage migration yet.
- No `app.py` rewrite yet.
- Later code work starts only after backup and implementation phases.

### 06_RISK_AND_ROLLBACK_PLAN.md

Cover:

- `app.py` currently modified and accepted as baseline
- `.env` secrecy
- `.venv`, `.git`, `__pycache__` exclusion
- possible Codex worktree confusion
- possible PowerShell vs cmd confusion
- apply_patch approval failures
- rollback strategy before future code changes

### 07_ACCEPTANCE_CHECKLIST.md

Create a checklist for Phase 1 completion:

- required docs exist
- no business code changed
- `.env` not read
- current directory is Desktop project root
- `app.py` remains accepted baseline
- no install / browser / commit / push
- Phase 2 can start only after user approval

### run_reports/CODEX_PHASE1_DOC_CENTER_AUDIT.md

Summarize:

- current working directory
- files read
- files created or updated
- whether `.env` content was read
- whether business code was modified
- Git status summary
- whether Phase 1 can be closed
- whether Phase 2 can start
- blockers

## Handling write failures

If file writing is blocked by an approval or tooling error, do not bypass the failure with unrelated write methods. Stop and report exactly which files were not written and why.

## Final response format

After completing the task, report:

1. Current directory
2. Whether `.env` content was read
3. Whether any business code was modified
4. Created or updated files
5. Git status summary
6. Whether Phase 1 can close
7. Whether Phase 2 can start
8. Blockers

