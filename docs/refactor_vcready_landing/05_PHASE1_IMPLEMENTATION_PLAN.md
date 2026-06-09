# 05_PHASE1_IMPLEMENTATION_PLAN

Generated at: 2026-06-09 09:10:46 +08:00

## Phase 1 goal

Phase 1 establishes the refactor documentation center and product planning foundation.

This phase does not implement UI code.

## Inputs

Current project root:

```text
C:\Users\Administrator\Desktop\VCReady_Demo
```

Accepted Phase 1 baseline:

- `app.py` already has Risk Map enhancement and is accepted as the working baseline.
- `.env` must not be read.
- `.venv`, `.git`, and `__pycache__` must not be copied.
- `docs/refactor_vcready_landing/` is the refactor control center.

## Outputs

Phase 1 should land these documents:

```text
docs/refactor_vcready_landing/
├── 02_PRODUCT_INFORMATION_ARCHITECTURE.md
├── 03_VISUAL_REFERENCE_TRANSLATION.md
├── 04_COPYWRITING_DRAFT.md
├── 05_PHASE1_IMPLEMENTATION_PLAN.md
├── 06_RISK_AND_ROLLBACK_PLAN.md
├── 07_ACCEPTANCE_CHECKLIST.md
└── 08_PHASE1_CHANGELOG.md
```

## Codex role in Phase 1

Codex should only verify the documents and report quality issues.

Codex must not modify:

- `app.py`
- `prompts.py`
- `requirements.txt`
- `.env`
- `.agents/skills/**`
- `.git/**`
- `.venv/**`
- `__pycache__/**`

## Future implementation path

Implementation should not start until Phase 4 or Phase 5.

Expected future path:

```text
Phase 2: Product IA and visual system refinement
Phase 3: Streamlit multipage safety design
Phase 4: Backups and working directories
Phase 5: Landing page + Workspace preservation
Phase 6: Feature pages
Phase 7: Profile prototype
Phase 8: Portfolio screenshots and demo script
Phase 9: Commit plan and optional GitHub sync
```

## Phase 1 close condition

Phase 1 can close when:

- all Phase 1 documents exist
- Codex verifies from Desktop project root
- Codex confirms `.env` content was not read
- Codex confirms business code was not modified
- Git status is recorded
