\# VCReady - Claude Code Instructions



\## Project Purpose



VCReady is a Streamlit-based portfolio prototype for the HKUST(GZ) Red Bird MPhil application.



It is a working demo for founder narrative pressure-testing. It is not a commercial product, not a launched startup, not a funded company, and not a production system.



The core evidence chain is:



problem discovery -> AI prototype -> working demo -> user testing -> iteration -> portfolio material



\## First-Principles Working Rule



Start from the actual project goal and the current working code, not from generic templates.



Before changing code:

1\. Identify the real problem.

2\. Explain the shortest safe path.

3\. List the files you plan to modify.

4\. Wait for user confirmation unless the user explicitly authorized edits.



Do not patch blindly. If a bug appears, find the root cause first.



\## Agent Division



Claude Code is responsible for complex engineering tasks only:

\- API compatibility

\- model routing

\- call\_model stability

\- environment/config logic

\- difficult bugs

\- final code review



Claude Code should not do routine UI polishing unless explicitly asked.



Codex is responsible for low-risk implementation tasks:

\- UI layout

\- CSS

\- bilingual UI text

\- README and docs

\- simple copy changes



\## Files and Boundaries



Never modify these unless explicitly asked:

\- .env

\- API keys

\- real credentials

\- .venv/

\- .git/

\- requirements.txt



Do not modify call\_model unless the task is about API/model routing.



Do not rewrite app.py from scratch. Make minimal targeted edits.



Do not modify prompts.py during UI-only tasks.



\## Current Tech Stack



\- Python

\- Streamlit

\- OpenAI-compatible API through a relay

\- python-dotenv

\- pandas

\- local CSV for user testing template



\## UI Direction



Target UI style:

Institutional Dark + VC Memo / Data Room style.



Visual language:

\- deep navy background

\- dark slate cards

\- subtle borders

\- champagne gold or institutional blue accents

\- professional investment memo feeling

\- no cyberpunk

\- no flashy SaaS style

\- no large red primary buttons



Core UI modules:

\- Hero Header

\- Founder Dossier sidebar

\- Assessment Framework cards

\- Workflow card

\- VC Pressure-Test Memo

\- Founder Response

\- Founder Reflection Report

\- low-key disclaimer



\## Bilingual Requirement



The app should support:

\- English UI

\- Chinese UI

\- English model output when English is selected

\- Chinese model output when Chinese is selected



Switching language does not need to translate old generated content. It only needs to affect future generated output.



\## Encoding Rule



Avoid special punctuation that may cause encoding issues in PowerShell:

\- avoid em dash

\- avoid en dash

\- avoid smart quotes



Prefer plain ASCII punctuation:

\- hyphen

\- straight quotes

\- normal apostrophe



\## Language Key Safety



Internal language keys must use ASCII codes only.



Use:

\- en

\- zh



Do not use non-ASCII strings as internal dictionary keys for language routing.



Avoid:

\- TEXTS\["中文"]

\- st.session\_state.language == "中文"

\- any mojibake key such as TEXTS\["æ..."]



Preferred structure:

\- TEXTS\["en"]

\- TEXTS\["zh"]

\- LANGUAGE\_LABELS = {"en": "English", "zh": "中文"}



The UI may display Chinese text, but internal routing keys must remain ASCII.



If Chinese UI text is needed, edit the existing zh dictionary values only. Do not create new non-ASCII dictionary keys.



Never copy terminal mojibake into source code.



\## Git Workflow



One task = one agent = one commit.



Before modifying files:

\- git status must be clean



After modifying files:

\- show what changed

\- run syntax check

\- ask user to test

\- commit only after user confirms



Required checks:

.\\\\.venv\\\\Scripts\\\\python.exe -m py\\\_compile app.py prompts.py

.\\\\.venv\\\\Scripts\\\\python.exe -m streamlit run app.py



Output Style:

\-Be concise.

\-Focus on decisions and risks.

\-Do not list irrelevant background.

\-Do not over-engineer.



\## Response Language



Use Chinese for all explanations, plans, risk notes, summaries, and testing instructions addressed to the user.

Keep code, variable names, function names, CSS class names, CLI commands, and English UI copy in English when appropriate.

