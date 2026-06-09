# 06_RISK_AND_ROLLBACK_PLAN

Generated at: 2026-06-09 09:10:46 +08:00

## Risk 1: Codex starts in a temporary worktree

Observed issue:

```text
C:\Users\Administrator\.codex\worktrees\...\VCReady_Demo
```

Required rule:

Codex tasks must reference the Desktop project root explicitly:

```text
C:\Users\Administrator\Desktop\VCReady_Demo
```

## Risk 2: apply_patch approval failure

Observed issue:

```text
apply_patch failed with 503 Service Unavailable
```

Safe response:

- Do not ask Codex to bypass the approval failure.
- Use PowerShell-side document landing for docs-only phases.
- Ask Codex to verify read-only after PowerShell landing.

## Risk 3: Running PowerShell commands in cmd.exe

Observed issue:

PowerShell variables and commands such as `$ErrorActionPreference`, `Set-Location`, and `Set-Content` fail in cmd.exe.

Required rule:

Run commands only in PowerShell. The prompt should look like:

```text
PS C:\Users\Administrator>
```

## Risk 4: Business code changes before backup

Current status:

`app.py` already contains Risk Map enhancement and is accepted as the Phase 1 baseline.

Rule:

Do not refactor or split `app.py` until the backup phase.

## Risk 5: Sensitive files

Rules:

- Do not read `.env`.
- Do not print `.env`.
- Do not copy `.env`.
- Do not copy `.venv`.
- Do not expand `.git`.
- Do not copy `__pycache__`.

## Rollback plan for future code phases

Before any code modification:

1. create `backups/`
2. copy `app.py` into backup
3. copy `prompts.py` into backup
4. record `git status --short`
5. record `git diff --stat`
6. only then modify code

## Rollback principle

If implementation breaks the app, restore from the backup copy or use Git restore only after confirming the backup state.
