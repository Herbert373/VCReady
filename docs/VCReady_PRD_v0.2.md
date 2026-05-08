# VCReady - Product Requirements Document v0.2

## 1. Product Name

VCReady

## 2. Product Purpose

VCReady is a prototype that helps early-stage founders pressure-test their founder narrative before investor conversations. It is designed to surface weak logic, unclear evidence, and unanswered investor concerns before a real meeting takes place.

## 3. Portfolio Context

VCReady is a HKUST(GZ) Red Bird MPhil application portfolio prototype. It is intended to demonstrate product thinking, interface design, and AI-assisted workflow design in a focused founder assessment scenario. It should not be interpreted as a launched company or a commercial software product.

## 4. Problem Statement

Early-stage founders often spend more time explaining the project than explaining why they are the right team to build it. In investor conversations, this creates a gap between what founders present and what investors are actually evaluating. Founders need a structured way to test their own narrative, evidence, and decision logic before high-stakes meetings.

## 5. Current Product Scope

The current VCReady prototype is a single-session Streamlit application. A founder enters core context, receives investor-style pressure-test questions, writes a response, and receives a structured reflection report. The current scope is intentionally narrow and focused on one complete founder assessment workflow.

## 6. Current Implemented Features

- Bilingual UI with English and Chinese interface support
- Institutional Dark UI for an internal VC memo and data room style experience
- Founder Dossier sidebar for founder background, project description, current evidence, and funding or partnership goal
- Assessment Framework section for core founder evaluation dimensions
- Workflow cards that explain the end-to-end review process
- VC Pressure-Test Memo that presents generated investor-style questions
- Founder Response input area for the founder's written answers
- Founder Reflection Report with structured diagnostic output
- TXT report download for saving the generated report

## 7. Current User Flow

1. Open the app.
2. Fill in the Founder Dossier sidebar.
3. Generate VC pressure-test questions.
4. Write a Founder Response in the text area.
5. Generate the Founder Reflection Report.
6. Download the report as a TXT file.

## 8. Current Technical Architecture

- Streamlit as the application framework
- `app.py` for UI rendering, session flow, and app orchestration
- `prompts.py` for question and report prompt templates
- OpenAI-compatible relay for model access
- `python-dotenv` for environment variable loading

## 9. Non-Commercial Disclaimer

VCReady is not launched, has no real users, has no funding, and is not production deployed. It is a portfolio prototype only.

## 10. Evaluation and User Testing Plan

The prototype should be evaluated on clarity, usability, and output usefulness.

Evaluation focus:

- Whether a founder can understand the workflow without explanation
- Whether the generated questions feel relevant to investor logic
- Whether the reflection report highlights useful weaknesses in the founder narrative
- Whether the bilingual interface remains clear across the core workflow

User testing plan:

- Test with a small number of early-stage founders, student founders, or founder-like users
- Ask each participant to complete one full session from input to report download
- Record confusion points, unclear terminology, missing fields, and low-value outputs
- Use a simple feedback template to capture qualitative observations after each session

Useful iteration signals:

- Repeated confusion about any step in the workflow
- Inputs that are too vague to support useful output
- Pressure-test questions that feel generic or repetitive
- Reflection reports that do not produce actionable insight

## 11. Known Limitations

- Single-session workflow only
- No user accounts or saved history
- No database or persistent storage
- No production deployment or operational monitoring
- Output quality depends on prompt design and model behavior
- No separate model selection for question generation and report generation
- No multi-round investor challenge flow
- No exportable PDF report yet

## 12. Future Iterations

- Multi-model routing
- Separate question model and report model
- Multi-round investor challenge mode
- User testing with feedback template
- Exportable PDF report

## 13. Scope Honesty Note

This document describes the current prototype state and realistic next iterations. It does not claim commercial traction, production readiness, real user adoption, or funding progress.
