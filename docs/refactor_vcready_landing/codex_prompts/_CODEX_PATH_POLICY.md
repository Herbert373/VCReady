# VCReady Codex Path Policy

## Source of truth

VCReady 本轮重构的唯一主项目根目录是：

`C:\Users\Administrator\Desktop\VCReady_Demo`

## Codex worktree policy

如果 Codex 当前位于：

`C:\Users\Administrator\.codex\worktrees\*\VCReady_Demo`

该目录只能作为 Codex 的临时副本或执行环境参考，不能被当作主项目根目录。

## Task file policy

以后给 Codex 的一句话必须使用绝对路径：

`C:\Users\Administrator\Desktop\VCReady_Demo\docs\refactor_vcready_landing\codex_prompts\_CURRENT_CODEX_TASK.md`

不要再使用相对路径版：

`docs/refactor_vcready_landing/codex_prompts/_CURRENT_CODEX_TASK.md`

除非你已经确认 Codex 当前目录就是桌面主项目根目录。

## Safety policy

- 不读取、打印、复制 `.env` 内容。
- 不复制 `.git`、`.venv`、`__pycache__`。
- 不在 `.codex\worktrees` 下沉淀正式文档成果。
