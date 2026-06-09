# VCReady Codex Current Task

## Round
Codex Round 1：Phase 0 安全冻结与项目体检，只读审计。

## Working Directory
`C:\Users\Administrator\Desktop\VCReady_Demo`

## Task Goal
本轮任务不是改页面，也不是优化代码，而是完成 Phase 0 的只读审计与文档补全。

请确认当前桌面目录是否为主工作区，复核项目结构、关键文件、Git 状态、敏感文件边界、可改/不可改文件范围，并补全 Phase 0 文档。

## Absolute Safety Boundaries

### Forbidden
- 禁止读取、打印、复制 `.env` 内容。
- 禁止修改 `app.py`。
- 禁止修改 `prompts.py`。
- 禁止修改 `requirements.txt`。
- 禁止修改 `.agents/skills/**`。
- 禁止展开、复制或修改 `.git/`。
- 禁止复制或修改 `.venv/`。
- 禁止复制或修改 `__pycache__/`。
- 禁止删除任何文件。
- 禁止自动 commit。
- 禁止 push。
- 禁止安装依赖。
- 禁止启动浏览器。
- 禁止运行 Streamlit 服务器。
- 禁止把 `.bak` 文件直接删除。

### Allowed
- 可以只读查看项目目录结构。
- 可以只读查看 README、docs、tasks、AGENTS.md、CLAUDE.md、app.py、prompts.py。
- 可以检查 `.env` 是否存在，但不得读取其内容。
- 可以检查 `.gitignore` 是否包含 `.env`、`.venv`、`__pycache__` 等规则。
- 可以创建或更新 `docs/refactor_vcready_landing/` 下的 Phase 0 文档。
- 可以新增本轮审计报告 Markdown。

## Files to Create or Update

请创建或补全以下文件：

1. `docs/refactor_vcready_landing/00_BASELINE_FREEZE.md`
2. `docs/refactor_vcready_landing/01_CURRENT_PROJECT_MAP.md`
3. `docs/refactor_vcready_landing/run_reports/CODEX_PHASE0_READONLY_AUDIT.md`

## Required Content: 00_BASELINE_FREEZE.md

请至少包含：

- Phase 0 名称与日期
- 当前主工作区路径
- 当前 Git 状态摘要
- 当前可运行版本冻结说明
- 敏感文件处理原则
- 明确列出禁止上传/复制/打印的内容
- 明确列出 Phase 0 不做什么
- 下一阶段进入条件

## Required Content: 01_CURRENT_PROJECT_MAP.md

请至少包含：

- 当前目录树摘要
- 核心业务文件说明
- 文档文件说明
- tasks 文件说明
- portfolio_assets 文件说明
- `.agents/skills/` 文件说明
- `.env`、`.venv`、`.git`、`__pycache__`、`.bak` 文件的处理建议
- 初步判断：哪些文件后续可改，哪些文件必须保护
- Streamlit 页面重构的潜在入口，但不要实施

## Required Content: CODEX_PHASE0_READONLY_AUDIT.md

请至少包含：

- 本轮审计时间
- 本轮是否修改业务代码：必须回答
- 本轮是否读取 `.env`：必须回答
- 本轮新增/更新了哪些文档
- 当前目录与预期目录的差异
- 风险项
- 阻塞项
- 是否建议进入 Phase 1
- 下一轮 Codex Round 2 建议
- Git status 摘要

## Expected Final Response from Codex

完成后，请只输出以下结构：

1. Phase 0 执行结果
2. 是否触碰业务代码
3. 是否读取 `.env`
4. 新增/更新文件列表
5. 风险与阻塞项
6. 是否建议进入 Phase 1
7. 下一轮建议
