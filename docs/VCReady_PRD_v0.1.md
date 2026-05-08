# VCReady — Product Requirements Document (v0.1)

## 1. One-line positioning
VCReady is an AI prototype that helps early-stage founders pressure-test their founder narrative before talking to investors.

## 2. Problem
Early-stage founders tend to pitch the *project* when investors are actually evaluating the *founder*. Pitch decks rehearse the product story but rarely surface the weak seams in the founder's own logic: founder-market fit, execution evidence, resilience, judgment, and unfair advantage. Founders often discover these gaps only in the meeting itself, when it is too late to recover.

## 3. Core insight
Investor due diligence at the seed stage is primarily a test of the founder. A founder who has already been pressure-tested — privately, in advance — walks into the meeting with a tighter narrative and visible self-awareness. Both signals correlate with fundability.

## 4. Target user
- First-time or early-stage founders preparing for their first serious investor or strategic-partner meetings.
- Founders from non-traditional backgrounds (researchers, engineers, domain experts) who are strong on substance but under-rehearsed on narrative.

## 5. Primary job-to-be-done
"Before I meet an investor, help me find the holes in my own story so I can fix them, not be ambushed by them."

## 6. MVP scope
### In scope
- Single-session web app (Streamlit).
- User enters founder background, project description, current evidence, and funding/partnership goal.
- System generates 7 VC-style pressure-test questions.
- User writes answers in-app.
- System returns a Founder Reflection Report with a one-sentence diagnosis, strongest narrative part, biggest logic gap, five 1–5 scores (Founder-Market Fit, Problem Urgency, Execution Evidence, Resilience, Unfair Advantage), three must-answer questions, and concrete advice.
- `.txt` download of the report.

### Out of scope (v0.1)
- Accounts, login, user profiles.
- Persistent database, history of past sessions.
- Payments or monetization.
- PDF export, rich formatting.
- Deployment, hosting, scaling.
- Any claim of production users or revenue.

## 7. User flow
1. Land on app → read positioning and "How it works".
2. Fill 4 sidebar fields.
3. Click **Generate Pressure-Test Questions** → see 7 questions.
4. Answer each question.
5. Click **Generate Founder Reflection Report** → see structured report.
6. Download `.txt`.

## 8. AI design
- Two prompts: `QUESTION_PROMPT` and `REPORT_PROMPT`, kept in `prompts.py`.
- Both prompts produce Markdown output rendered directly in the UI.
- Model called via an OpenAI-compatible relay endpoint (configurable base URL), so Claude or other models can be used behind the same SDK.

## 9. Success criteria (portfolio context)
- App runs end-to-end with `streamlit run app.py`.
- A real early-stage founder can complete the full loop in under 20 minutes.
- At least 3 user-testing sessions recorded in `data/user_testing_template.csv` with actionable feedback.
- Reviewer can read the PRD, README, and code and recognize intentional scope choices.

## 10. Non-goals and honesty disclaimer
VCReady is a working prototype built for the HKUST-GZ Red Bird MPhil application portfolio. It is not a commercial product, has no users, no funding, and is not deployed to production.
