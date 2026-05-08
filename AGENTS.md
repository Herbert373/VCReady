\# VCReady - Agent Instructions



\## Project Purpose



VCReady is a Streamlit-based portfolio prototype for the HKUST(GZ) Red Bird MPhil application.



It helps early-stage founders pressure-test their founder narrative before investor conversations.



This is not a commercial product, not a launched startup, not a funded company, and not a production system.



\## Working Principle



Work from first principles:

1\. Understand the actual user goal.

2\. Identify the smallest safe change.

3\. Do not follow generic templates blindly.

4\. Explain the plan before editing files.

5\. Do not patch symptoms without identifying the root cause.



\## Codex Role



Codex should handle low-risk implementation tasks:

\- UI layout

\- CSS

\- card-based layout

\- bilingual UI text

\- README and docs

\- simple copy updates

\- user testing templates



Codex should not handle complex API/model logic unless explicitly asked.



\## Hard Boundaries



Do not modify:

\- .env

\- real API keys

\- .venv/

\- .git/

\- call\_model

\- API call logic

\- model routing logic

\- requirements.txt



Do not rewrite app.py from scratch.



For UI-only tasks, do not modify prompts.py.



\## UI Target



Use Institutional Dark + VC Memo / Data Room style.



The interface should look like an internal founder assessment dashboard used by an investment institution.



Core modules:

\- Hero Header

\- Founder Dossier sidebar

\- Assessment Framework cards

\- Workflow card

\- VC Pressure-Test Memo

\- Founder Response

\- Founder Reflection Report

\- footer disclaimer



Color direction:

\- deep navy background

\- dark slate cards

\- subtle borders

\- off-white text

\- muted gray secondary text

\- champagne gold or institutional blue accents



Avoid:

\- cyberpunk

\- flashy gradients

\- consumer SaaS look

\- large red buttons

\- excessive emojis



\## Bilingual Requirement



Support English and Chinese UI.



Language selection should affect:

\- page title

\- section titles

\- input labels

\- button text

\- helper text

\- disclaimer

\- future AI output language



Old generated content does not need automatic translation.



\## Encoding Rule



Avoid special punctuation:

\- em dash

\- en dash

\- smart quotes



Use plain ASCII punctuation to avoid PowerShell encoding issues.



\## Git and Safety



Before editing:

\- inspect current files

\- explain plan

\- list files to modify

\- wait for confirmation



After editing:

\- summarize changes

\- provide test commands

\- do not commit automatically unless asked



Required checks:

.\\.venv\\Scripts\\python.exe -m py\_compile app.py prompts.py

.\\.venv\\Scripts\\python.exe -m streamlit run app.py



Communication Style:

\-Be direct.

\-Prioritize safe minimal changes.

\-Do not over-engineer.

\-Do not add unrelated features.

