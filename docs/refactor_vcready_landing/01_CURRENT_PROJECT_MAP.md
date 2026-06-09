# 01_CURRENT_PROJECT_MAP

Generated at: 2026-06-09 08:38:24 +08:00

## Project root

`	ext
C:\Users\Administrator\Desktop\VCReady_Demo
`

## Known current directory structure

`	ext
VCReady_Demo
├── .agents
├── .git
├── .venv
├── data
├── docs
├── portfolio_assets
├── tasks
├── __pycache__
├── .env
├── .env.example
├── .gitignore
├── AGENTS.md
├── AGENTS.md.bak
├── app.py
├── CLAUDE.md
├── CLAUDE.md.bak
├── prompts.py
├── README.md
└── requirements.txt
`

## Core files

| Path | Role | Phase 0 handling |
|---|---|---|
| pp.py | Current Streamlit application / workspace entry | Read-only audit only. Do not modify in Phase 0. |
| prompts.py | Prompt and LLM-related logic | Read-only audit only. Do not modify in Phase 0. |
| equirements.txt | Dependency list | Read-only audit only. Do not modify in Phase 0. |
| .env | Local secrets / environment variables | Check existence only. Do not read, print, copy, or parse. |
| .env.example | Safe environment template | May be read if needed. Do not infer real secrets from it. |
| .gitignore | Ignore rules | May be read to verify .env, .venv, __pycache__. |
| README.md | Public project description | May be read. Do not update in Phase 0. |
| docs/VCReady_PRD_v0.1.md | Earlier PRD | May be read. |
| docs/VCReady_PRD_v0.2.md | Earlier PRD | May be read. |
| docs/VCReady_v0.3_Guided_Flow_Spec.md | Guided flow spec in Desktop project root | May be read. |
| 	asks/current_commit.md | Current work planning record | May be read. Do not update in Phase 0. |
| 	asks/progress_log.md | Project progress log | May be read. Do not update in Phase 0. |
| .agents/skills/** | Local agent skills | Do not modify. |
| .venv/ | Local Python environment | Do not copy or inspect deeply. |
| .git/ | Git repository internals | Do not expand or copy. |
| __pycache__/ | Generated Python cache | Ignore. |

## Refactor documentation center

`	ext
docs/refactor_vcready_landing/
├── codex_prompts
├── powershell_commands
└── run_reports
`

This directory is the control center for the VCReady landing/workspace refactor.

## Phase 0 conclusion

Phase 0 is not a UI refactor phase. It only establishes the baseline, confirms safety boundaries, and prepares the project for later documentation and implementation phases.
