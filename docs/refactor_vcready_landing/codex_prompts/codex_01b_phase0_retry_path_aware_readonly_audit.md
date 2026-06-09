# VCReady Codex Current Task
# Phase 0 Retry：路径感知版安全冻结与项目体检

## 0. 为什么需要本轮 Retry

上一轮 Codex 在当前工作目录：

`C:\Users\Administrator\.codex\worktrees\ffd3\VCReady_Demo`

中寻找：

`docs/refactor_vcready_landing/codex_prompts/_CURRENT_CODEX_TASK.md`

但该 worktree 不是本次 VCReady 重构的主工作区，因此没有找到任务文件。

本轮必须修正路径判断：

**主项目根目录只有一个：**

`C:\Users\Administrator\Desktop\VCReady_Demo`

如果当前 shell 位于：

`C:\Users\Administrator\.codex\worktrees\*\VCReady_Demo`

你必须先切换到主项目根目录，或者明确说明无法访问该主目录。不要把 `.codex\worktrees` 下的副本当成主项目。

---

## 1. 本轮任务性质

本轮是 Phase 0 Retry：安全冻结与项目体检。

只允许做：

- 只读审计；
- 文档补全；
- 路径差异说明；
- 生成 Phase 0 run report。

不允许做：

- 页面优化；
- 业务代码修改；
- LLM prompt 修改；
- 依赖安装；
- Git commit；
- Git push；
- 浏览器启动。

---

## 2. 绝对路径要求

请先执行路径确认：

1. 查看当前目录；
2. 如果当前目录不是 `C:\Users\Administrator\Desktop\VCReady_Demo`，请切换到该目录；
3. 如果无法切换，请停止任务并说明原因；
4. 不要在 `.codex\worktrees` 目录中创建本轮正式成果。

主项目根目录：

`C:\Users\Administrator\Desktop\VCReady_Demo`

正式成果只能写入主项目根目录下的：

`docs/refactor_vcready_landing/`

---

## 3. 最高优先级安全边界

禁止读取、打印、复制 `.env` 内容。只允许判断 `.env` 是否存在，以及 `.gitignore` 是否覆盖它。

禁止修改以下文件：

- `app.py`
- `prompts.py`
- `requirements.txt`
- `.env`
- `.env.example`
- `.gitignore`
- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.agents/skills/**`

禁止展开、复制或写入：

- `.git/`
- `.venv/`
- `__pycache__/`

禁止自动执行：

- `git add`
- `git commit`
- `git push`
- `pip install`
- `streamlit run`
- 任何会启动浏览器的命令。

---

## 4. 允许读取的内容

允许只读查看：

- 根目录文件名；
- `docs/` 下 Markdown 文件；
- `tasks/current_commit.md`
- `tasks/progress_log.md`
- `README.md`
- `app.py` 的结构摘要，但不要重写；
- `prompts.py` 的结构摘要，但不要重写；
- `.gitignore`；
- `.env.example`；
- `.agents/skills/**/SKILL.md` 的文件名和用途摘要，不改内容。

---

## 5. 本轮需要补全或创建的文档

请在主项目根目录下补全或创建：

1. `docs/refactor_vcready_landing/00_BASELINE_FREEZE.md`
2. `docs/refactor_vcready_landing/01_CURRENT_PROJECT_MAP.md`
3. `docs/refactor_vcready_landing/run_reports/CODEX_PHASE0_RETRY_PATH_AWARE_AUDIT.md`

如果前两个文档已经存在，请只做 Phase 0 范围内的补全，不要重写成完全不同版本。

---

## 6. `00_BASELINE_FREEZE.md` 应包含

请写清楚：

- 主项目绝对路径；
- 本轮是否发现 `.codex\worktrees` 副本；
- 为什么 `.codex\worktrees` 不能被当成主工作区；
- 当前 Git 状态摘要；
- `.env` 是否存在，但不要展示内容；
- `.env` 是否被 `.gitignore` 覆盖；
- `.venv`、`.git`、`__pycache__` 的处理原则；
- 当前版本冻结说明；
- Phase 0 后是否允许进入 Phase 1；
- 阻塞项。

---

## 7. `01_CURRENT_PROJECT_MAP.md` 应包含

请写清楚：

- 当前目录树摘要，不展开 `.git`、`.venv`、`__pycache__`；
- 核心文件用途：
  - `app.py`
  - `prompts.py`
  - `requirements.txt`
  - `README.md`
  - `docs/VCReady_PRD_v0.1.md`
  - `docs/VCReady_PRD_v0.2.md`
  - `docs/VCReady_v0.3_Guided_Flow_Spec.md`，如果存在
  - `tasks/current_commit.md`，如果存在
  - `tasks/progress_log.md`，如果存在
  - `.agents/skills/**`，如果存在
- 当前业务主链路摘要；
- 当前文档证据链摘要；
- 哪些文件未来可改；
- 哪些文件未来只读；
- 哪些文件未来禁止处理。

---

## 8. `CODEX_PHASE0_RETRY_PATH_AWARE_AUDIT.md` 应包含

请记录：

- 本轮实际启动目录；
- 是否成功切换到主项目目录；
- 是否误用 `.codex\worktrees`；
- 本轮读取了哪些文件；
- 本轮写入了哪些文档；
- 本轮是否读取 `.env` 内容，正确答案应为否；
- 本轮是否修改业务代码，正确答案应为否；
- 本轮 Git status 摘要；
- 本轮发现的风险；
- 是否建议进入 Phase 1；
- 下一轮 Phase 1 建议。

---

## 9. 输出格式

完成后，请在回复中只输出以下内容：

1. 本轮是否成功切换到 `C:\Users\Administrator\Desktop\VCReady_Demo`；
2. 本轮是否读取 `.env` 内容；
3. 本轮是否修改业务代码；
4. 新增或更新了哪些文档；
5. 当前 Git status 摘要；
6. 是否建议进入 Phase 1；
7. 阻塞项；
8. 下一轮 Codex Round 2 建议。

再次强调：不要修改业务代码，不要读取 `.env` 内容，不要使用 `.codex\worktrees` 作为主项目根目录。
