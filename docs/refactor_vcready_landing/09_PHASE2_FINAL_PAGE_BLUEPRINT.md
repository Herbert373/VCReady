# 09_PHASE2_FINAL_PAGE_BLUEPRINT

Generated at: 2026-06-09 09:21:19 +08:00

## Phase 2 purpose

Phase 2 locks the target page blueprint before any code refactor. It does not create pages, move code, edit Streamlit logic, change prompts, or touch environment files.

VCReady remains a founder logic pressure-test engine. It is not a pitch deck formatter, not a financial modeling tool, not investment advice, and not a promise of fundraising success.

## Accepted baseline before Phase 2

- Project root: `C:\Users\Administrator\Desktop\VCReady_Demo`
- Current `app.py` already contains the Risk Map enhancement and is accepted as the Phase 1 / Phase 2 baseline.
- `.env` must not be read, printed, copied, parsed, or inferred from.
- `.venv`, `.git`, and `__pycache__` must not be copied into any refactor package.
- Phase 2 is documentation-only.

## Target product structure

```text
VCReady
├── Public Landing Page
├── Workspace
├── Feature Pages
│   ├── Pressure Test
│   ├── Founder Dossier
│   └── Reflection Report
├── Profile Prototype
└── Report Preview
```

## Page role separation

| Area | Role | Current / future implementation boundary |
|---|---|---|
| Public Landing Page | Explain VCReady, create trust, guide users to the workspace | Future `app.py`, but not changed in Phase 2 |
| Workspace | Preserve the current pressure-test flow and report generation | Future `pages/01_Workspace.py`, but not created in Phase 2 |
| Pressure Test page | Explain the VC interrogation mechanism | Future static feature page, no LLM call |
| Founder Dossier page | Explain why founder context matters before questioning | Future static feature page, no database |
| Reflection Report page | Explain report output, logic gaps, Risk Map, and next actions | Future static feature page, no fake history |
| Profile Prototype | Show long-term usage concept | Static prototype only, no login, no persistent account system |
| Report Preview | Show example report structure | Demo preview only, not a real generated history record |

## Public Landing Page blueprint

### 1. Navigation

Purpose: make VCReady feel like a product rather than a single script.

Recommended items:

- VCReady logo / wordmark
- Product
- Pressure Test
- Founder Dossier
- Reflection Report
- Profile Prototype
- Start Test

Primary CTA:

```text
Start Pressure Test
```

Secondary CTA:

```text
View Example Report
```

### 2. Hero section

Purpose: immediately state the cognitive asymmetry VCReady solves.

Core message:

```text
Before you pitch, survive the questions.
```

Supporting message:

```text
VCReady helps early founders pressure-test founder-market fit, evidence strength, execution logic, and investor-facing risks before they enter a real pitch room.
```

Hero should not imply real financing probability, investment matching, or professional investment advice.

### 3. Problem section

Purpose: explain why founders fail in investor conversations.

Core problem:

- Founders sell projects.
- Investors evaluate people, evidence, logic, and risk.
- Early teams often cannot explain why they are the right people to solve the problem.
- A polished deck can hide weak reasoning, but a VC-style interview exposes it quickly.

### 4. Product mechanism section

Purpose: explain what VCReady actually does.

Mechanism:

```text
Founder Dossier → AI VC Questions → Founder Response → Reflection Report → Risk Map → Next Validation Actions
```

### 5. Feature cards

Required cards:

1. Founder Dossier
2. Pressure Test Questions
3. Founder Response Review
4. Reflection Report
5. Risk Map
6. Next Validation Actions

Risk Map should be treated as a first-class feature because it is now part of the accepted `app.py` baseline.

### 6. How it works

Suggested steps:

1. Describe the founder and project context.
2. Generate VC-style pressure-test questions.
3. Answer under a skeptical investor lens.
4. Receive structured reflection and risk diagnosis.
5. Convert weak logic into validation tasks.

### 7. Assessment framework

The framework should include:

- Founder-Market Fit
- Problem Urgency
- Evidence / Validation Strength
- Execution Credibility
- Commercialization / GTM Logic
- Sector-Specific Risk

### 8. Example report preview

Purpose: show the output format without pretending to have a real user history database.

Preview blocks:

- Assessment Lens
- Risk Map
- One-sentence Diagnosis
- Logic Gaps
- Strongest Part
- Next 7 Days
- Next 30 Days

### 9. Boundary / disclaimer section

Must state:

- VCReady is a local demo / product prototype.
- It does not provide investment advice.
- It does not guarantee fundraising outcomes.
- It does not replace professional legal, financial, or investment judgment.
- Profile and history pages are prototype-only unless future persistence is built.

### 10. Final CTA

Primary:

```text
Start Pressure Test
```

Secondary:

```text
Read the Product Logic
```

## Workspace blueprint

The Workspace preserves the existing VCReady pressure-test application.

Future Workspace should retain:

- Language switch
- Founder / project context input
- Guided flow
- Question generation
- Founder response
- Reflection report
- Risk Map
- Report download

Phase 2 does not move code into `pages/01_Workspace.py`. That belongs to a later implementation phase after backup and rollback rules are locked.

## Feature page blueprints

### Pressure Test

Purpose: explain the AI VC interrogation logic.

Sections:

- What the pressure test simulates
- Why generic pitch advice is not enough
- Example VC questions
- What a strong answer contains
- CTA to Workspace

### Founder Dossier

Purpose: explain why the system needs founder and project context.

Sections:

- Founder-market fit
- Project stage
- Evidence already collected
- Good input vs weak input
- CTA to Workspace

### Reflection Report

Purpose: explain how to read the output.

Sections:

- Assessment Lens
- Risk Map
- Logic Gap
- Strongest Part
- Next validation actions
- Disclaimer
- CTA to Workspace

## Profile Prototype blueprint

Purpose: communicate a future long-term usage direction without pretending that account persistence exists.

Sections:

- Prototype-only badge
- Founder identity card
- Demo metrics
- Reflection notes
- Growth overview
- Coming soon modules

Mandatory copy:

```text
Prototype only. Local demo. No persistent account system yet.
```

## Phase 2 exit criteria

Phase 2 can close when:

- This blueprint exists.
- Visual system lock exists.
- Copy lock exists.
- Codex verifies these documents from the Desktop project root.
- No business code has been modified.
- No sensitive file has been read.

## Phase 3 entry gate

Before Phase 3 or any implementation phase starts, the user must explicitly approve:

- Whether backup directories may be created.
- Whether `pages/` may be created.
- Whether `app.py` may be copied but not rewritten.
- Whether `prompts.py` may be backed up but not edited.
- Which files are allowed to change.
