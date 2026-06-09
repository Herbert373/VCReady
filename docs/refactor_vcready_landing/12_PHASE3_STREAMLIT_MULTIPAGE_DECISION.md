# 12_PHASE3_STREAMLIT_MULTIPAGE_DECISION

Generated at: 2026-06-09 09:36:49 +08:00

## Phase status

Phase 3 locks the safe refactor path before any code migration.

This phase is not an implementation phase. It does not modify pp.py, prompts.py, equirements.txt, or any runtime logic.

## Accepted baseline

The current pp.py contains the Risk Map enhancement. This modified state is accepted as the Phase 3 baseline and must not be treated as accidental damage.

## Route decision

The selected route is Streamlit multipage.

Future target structure:

`	ext
app.py
pages/
  01_Workspace.py
  02_Pressure_Test.py
  03_Founder_Dossier.py
  04_Reflection_Report.py
  05_Profile.py
assets/
  landing/
  mockups/
  references/
backups/
`

## Page responsibilities

| Page | Future role | Runtime status |
|---|---|---|
| pp.py | Public Landing Page | Future Phase 5 change only |
| pages/01_Workspace.py | Existing VCReady pressure-test workspace | Future Phase 5 copy/migration only |
| pages/02_Pressure_Test.py | Feature explanation page | Future static page |
| pages/03_Founder_Dossier.py | Feature explanation page | Future static page |
| pages/04_Reflection_Report.py | Feature explanation page | Future static page |
| pages/05_Profile.py | Static profile prototype | Future static prototype |

## Why multipage

Streamlit multipage is selected because it separates the public product narrative from the functional workspace while preserving the current app logic.

## What Phase 3 does not do

- Does not create pages/
- Does not create ackups/
- Does not create ssets/landing/
- Does not copy pp.py
- Does not rewrite pp.py
- Does not touch LLM/API logic
- Does not start Streamlit
- Does not install dependencies

## Phase 4 gate

Phase 4 may start only after user approval. Phase 4 may create directories and backup copies, but still must not rewrite business logic.
