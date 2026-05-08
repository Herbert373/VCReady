# VCReady - Founder Logic Pressure-Test Engine

> An AI prototype that helps early-stage founders pressure-test their founder narrative before talking to investors.

## What this is

VCReady is a working Streamlit prototype. A founder fills in their background, project, evidence, and funding goal. The app simulates a sharp early-stage VC, generates 7 pressure-test questions, and - after the founder answers - returns a structured Founder Reflection Report with scores and concrete advice.

## Why it exists

Early-stage founders often pitch the project when investors are actually evaluating the founder. VCReady surfaces the weakest seams in the founder's own narrative - founder-market fit, execution evidence, resilience, judgment, unfair advantage - before the real meeting happens.

## Features (MVP)

- Sidebar inputs: founder background, project description, current evidence, funding or partnership goal.
- One-click generation of 7 VC-style pressure-test questions covering founder-market fit, problem urgency, execution evidence, resilience, unfair advantage, go-to-market, and risk.
- Per-question answer fields.
- Founder Reflection Report containing:
  - One-sentence diagnosis
  - Strongest part of the narrative
  - Biggest logic gap
  - Scores (1-5) for Founder-Market Fit, Problem Urgency, Execution Evidence, Resilience, Unfair Advantage
  - Three questions the founder must answer before meeting investors
  - Concrete advice to improve the pitch
- Download the report as `.txt`.

## Tech stack

- Python 3.10+
- Streamlit
- OpenAI Python SDK (used against any OpenAI-compatible endpoint - relay/proxy gateways included)
- python-dotenv
- Local CSV for the user-testing template (no database)

## Run it locally

```bash
# 1. Clone and enter the project
cd VCReady_Demo

# 2. (Recommended) create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux
# then edit .env and fill in OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

# 5. Launch
streamlit run app.py
```

## Project structure

```
VCReady_Demo/
  app.py                       Streamlit app: UI, state, API calls
  prompts.py                   Question + report prompt templates
  requirements.txt             Python dependencies
  README.md                    This file
  .env.example                 Environment variable template
  .gitignore                   Excludes .env and caches
  docs/
    VCReady_PRD_v0.1.md        Product requirements document
  data/
    user_testing_template.csv  Template for recording user-testing sessions
```

## Environment variables

Defined in `.env.example`. The app reads the OpenAI-compatible block. Anthropic-native variables are reserved for future use.

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | API key for the relay / OpenAI-compatible endpoint |
| `OPENAI_BASE_URL` | Base URL of the relay (leave empty to use OpenAI default) |
| `OPENAI_MODEL` | Model name exposed by the endpoint |
| `ANTHROPIC_API_KEY` | Reserved - not wired into `app.py` yet |
| `ANTHROPIC_BASE_URL` | Reserved |
| `ANTHROPIC_MODEL` | Reserved |

`.env` is gitignored. Never commit it.

## Non-commercial disclaimer

VCReady is a working prototype built for the HKUST-GZ Red Bird MPhil application portfolio. It is **not** a commercial product, has **no** users, **no** funding, and is **not** deployed to production. Every part of this repo should be read in that context.
