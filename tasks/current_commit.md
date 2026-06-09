\# Commit 7D-fix-1 - Show Risk Map in Dashboard



Mode: patch-plan-only

Allowed file: app.py



\## Current status



Commit 7D has been implemented but not accepted.



The downloaded txt report already contains:



\- ## 风险地图

\- Risk Map content with 6 risk categories



So report generation, deterministic guarantee, and txt download are working.



However, the Dashboard does not display the Risk Map / 风险地图 section.



\## Goal



Fix Dashboard rendering so that Risk Map / 风险地图 appears as a dashboard card when it exists in report\_markdown.



\## Scope



Only modify app.py.



Focus only on:



\- parse\_report\_markdown\_sections(...)

\- render\_report\_dashboard(...)

\- section title / alias matching logic

\- report\_sections assignment if it still parses the wrong markdown variable



\## Do not modify



\- prompts.py

\- call\_model

\- get\_client

\- API logic

\- QUESTION\_PROMPT

\- REPORT\_PROMPT\_EN

\- REPORT\_PROMPT\_ZH

\- build\_report\_risk\_map\_instruction

\- build\_fallback\_risk\_map\_markdown

\- ensure\_report\_has\_risk\_map

\- report generation prompt injection

\- txt download core logic

\- Guided Mode answer saving

\- Review All synchronization



\## Required diagnosis before patch



Before editing, inspect:



1\. parse\_report\_markdown\_sections(...)

2\. render\_report\_dashboard(...)

3\. the two report generation paths where st.session\_state.report\_sections is assigned



Determine why this markdown heading is not shown in Dashboard:





\## 风险地图



Likely causes:



parse\_report\_markdown\_sections does not preserve unknown headings

parse\_report\_markdown\_sections only maps original report headings

render\_report\_dashboard does not match 风险地图 / Risk Map correctly

st.session\_state.report\_sections is parsed from raw\_report instead of the post-processed report\_markdown

Required fix



Ensure that when report\_markdown contains any of these headings:



风险地图

Risk Map



Dashboard renders a Risk Map / 风险地图 card.



If the section is missing, do not render an empty card.



Do not duplicate Risk Map.



Do not change report generation behavior.



Do not change txt download behavior.



Acceptance criteria



After the fix:



txt still contains 风险地图 / Risk Map.

Dashboard displays 风险地图 / Risk Map.

Assessment Lens / 评估视角 still displays.

Original six sections still display.

No empty Risk Map card appears if the section is absent.

Only app.py is modified.

py\_compile passes.

Required output now



Produce patch plan only.



Patch plan must explain:



Why Dashboard currently misses Risk Map.

Which app.py region will be modified.

Whether parse\_report\_markdown\_sections needs to change.

Whether render\_report\_dashboard needs to change.

Whether report\_sections assignment needs to change.

How the fix avoids changing report generation and download logic.

Test commands.

