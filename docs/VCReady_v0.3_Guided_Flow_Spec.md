# VCReady v0.3 Guided Founder Assessment Flow Spec

## 1. Product Direction

VCReady v0.3 is a guided interaction redesign. It is not a minor UI polish pass.

The product direction is to turn the current single-page assessment flow into a clearer guided founder assessment sequence. The user should move through a structured path from Founder Dossier setup, to VC pressure-test questions, to one-question-at-a-time guided answering, to review, to report generation, to structured report cards.

VCReady remains a portfolio prototype. This spec does not claim real users, funding, revenue, or production deployment.

VCReady v0.3 must remain bilingual. The product UI must continue to support English and Chinese.

## 2. Why v0.3 Is Needed

VCReady v0.2 is a stable working Streamlit prototype, but the interaction pattern is still close to a conventional form plus generated Markdown output. That is useful for a first portfolio version, but it does not fully express the intended founder assessment workflow.

v0.3 is needed for three reasons:

1. The founder needs a guided sequence instead of a dense single-page experience.
2. One question per card can improve focus and answer quality.
3. The final report should feel like a structured product output, not only a long Markdown response.

The redesign should preserve the working logic of v0.2 while improving the user journey and report presentation.

## 3. Bilingual Product Requirement

VCReady v0.3 remains a bilingual product.

The product must continue to support:

- English UI
- Chinese UI
- English question flow
- Chinese question flow
- English report cards
- Chinese report cards

All new v0.3 user-facing UI must support both `en` and `zh`.

Internal language routing keys must remain ASCII:

- `en`
- `zh`

Do not rename internal language keys to `English` or Chinese display text. Do not create non-ASCII language routing keys. Do not remove Chinese UI support. Do not replace the bilingual product with an English-only product.

This spec document is written in English only for repository clarity and encoding safety. The product itself must remain bilingual.

## 4. Target User Flow

The target v0.3 flow is:

1. Founder Dossier Setup
2. Generate VC Pressure-Test Questions
3. Guided Mode with one question per card
4. Review All Answers
5. Generate Report with synchronized progress
6. Structured Report Cards
7. Download full TXT report

The flow should feel like an assessment sequence rather than a generic form. The founder should always understand what step they are in, what is required next, and what will happen after submission.

## 5. Founder Dossier Behavior

The Founder Dossier is collected first in the main page.

Required fields:

- Founder background
- Project description
- Current evidence
- Funding or partnership goal

The app should block question generation until required dossier fields are complete.

After dossier setup is complete, the sidebar should become a Founder Profile Summary. The summary should give the founder a compact view of the entered context while the main page moves into the guided assessment flow.

The Founder Profile Summary must be bilingual. Labels and helper text must support both `en` and `zh`.

## 6. Guided Mode Behavior

v0.3 should not build a real modal dialog. The guided assessment should use an in-page guided card flow.

Guided Mode must show one question per card. Each card should include:

- Current question number
- Total number of questions
- The active VC pressure-test question
- Founder answer input
- Navigation controls
- Progress through the question set

The founder should be able to move between questions without losing answers. Answer state should be retained per question.

All Guided Mode labels, controls, captions, warnings, and empty states must support both `en` and `zh`.

## 7. Review All Answers Behavior

Review All Answers must exist before report generation.

The review step should show:

- All generated questions
- The founder answer for each question
- Clear indication of missing or weakly completed answers
- A way to return to the guided cards for edits
- A final action to generate the report

Report generation should not be the immediate next action after answering the last guided card. The founder should see the full answer set first.

The review screen must support both `en` and `zh`.

## 8. Report Generation Progress Behavior

Report generation should show synchronized progress that reflects actual readiness.

The progress indicator must not show 100 percent until report data is available and ready to render.

Recommended progress stages:

1. Preparing transcript
2. Sending report request
3. Waiting for model output
4. Parsing report data
5. Preparing report cards
6. Ready to render

The final stage should only be reached after the report has been received and the selected rendering path is ready.

Loading states, progress labels, error messages, and retry actions must support both `en` and `zh`.

## 9. Structured Report Cards

The report should render as structured cards when possible. The goal is to make the output easier to scan and more product-like than a plain Markdown block.

Expected report card sections:

- One-sentence diagnosis
- Strongest part of the founder narrative
- Biggest logic gap
- Scores
- Three questions to answer before meeting investors
- Concrete advice to improve the pitch

The full TXT report download must remain available.

Report card headings, empty states, fallback labels, and download labels must support both `en` and `zh`.

## 10. JSON-First Report Strategy With Markdown Fallback

The long-term rendering strategy should be JSON-first.

Preferred path:

1. Ask for or receive structured report data.
2. Parse report data into known sections.
3. Render each section as a structured report card.

Fallback path:

1. If JSON parsing fails, use a Markdown section parser.
2. If Markdown section parsing fails, display the full Markdown report.

The fallback behavior should protect the user experience. The founder should still receive a usable report even if structured parsing fails.

All rendering paths must support bilingual UI framing. The model output language should follow the active language selection.

## 11. Session State Design

v0.3 should use explicit flow state so the interface can move through guided steps without losing data.

Proposed state groups:

- Dossier state
- Question generation state
- Guided question state
- Answer state
- Review state
- Report generation progress state
- Raw report state
- Parsed report state
- Report render mode state

Possible state responsibilities:

- Track whether the dossier is complete
- Store generated questions
- Store current guided question index
- Store answer text per question
- Track whether the user has entered review mode
- Track report generation progress
- Store raw report Markdown or text
- Store parsed JSON or parsed section data when available
- Store selected fallback render mode

Language state must continue to use safe ASCII language keys:

- `en`
- `zh`

Do not introduce non-ASCII routing keys for language or flow state.

## 12. Error and Fallback Rules

Missing dossier fields:

- Show a clear validation message.
- Do not generate questions until required fields are complete.
- Message must support both `en` and `zh`.

Failed question generation:

- Keep dossier data available.
- Show a retry path.
- Do not advance into Guided Mode without questions.

Missing answers:

- Preserve answer drafts.
- Highlight incomplete questions during Review All Answers.
- Allow the founder to return to the relevant question card.

Failed report generation:

- Do not show 100 percent progress.
- Keep reviewed answers available.
- Show an error and retry path.

JSON parse failure:

- Fallback to Markdown section parser.
- Do not discard the raw report.

Markdown section parse failure:

- Fallback to full Markdown report display.
- Keep download available if raw report text exists.

All error and fallback messages must support both `en` and `zh`.

## 13. Out of Scope for v0.3

The following items are out of scope for v0.3:

- Real modal dialog
- Account system
- Database
- Production deployment claim
- PDF export
- Multi-model routing
- Multi-round investor challenge

v0.3 should stay focused on the guided assessment flow and structured report presentation.

## 14. Development Plan by Commits

Commit 1: Add guided flow spec.

Commit 2: Define flow states and bilingual UI text structure.

Commit 3: Move Founder Dossier setup into the main page.

Commit 4: Convert the sidebar into Founder Profile Summary after dossier setup.

Commit 5: Add guided question card flow with one question per card.

Commit 6: Add Review All Answers step.

Commit 7: Add synchronized report progress behavior.

Commit 8: Add structured report card rendering.

Commit 9: Add JSON-first parsing with Markdown fallbacks.

Commit 10: Run bilingual QA and flow polish.

Each commit should be small and reviewable. Do not rewrite `app.py` from scratch. Do not modify model calling logic unless a later commit explicitly allows it.
