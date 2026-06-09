# 02_PRODUCT_INFORMATION_ARCHITECTURE

Generated at: 2026-06-09 09:10:46 +08:00

## Phase 1 purpose

This document defines the information architecture for the VCReady landing/workspace refactor.

Phase 1 is documentation-only. It must not modify `app.py`, `prompts.py`, `requirements.txt`, `.env`, `.agents/skills/**`, or any runtime logic.

## Accepted baseline before Phase 1

The current `app.py` already contains a Risk Map enhancement before Phase 1. This modified state is accepted as the Phase 1 baseline unless the user later decides to revert it.

## Product truth

VCReady is not a pitch-deck formatter, a financial modeler, a fundraising guarantee tool, or a generic productivity assistant.

VCReady is a founder logic pressure-test engine. It helps early-stage founders, competition teams, and first-time builders rehearse the investor-facing logic behind the project, especially the parts investors actually care about:

- founder-market fit
- problem urgency
- evidence quality
- execution credibility
- GTM and commercialization logic
- risk map and next validation action

## Target users

### Primary users

- early-stage founders before investor meetings
- student venture teams before demo day or competition defense
- first-time builders who know the project but cannot explain why they are the right founder

### Secondary users

- incubator mentors
- entrepreneurship camp participants
- product/business students building a portfolio project

## Product structure

```text
VCReady
├── Public Landing Page
│   ├── Hero
│   ├── Problem
│   ├── Product Value
│   ├── Feature Cards
│   ├── How It Works
│   ├── Report Preview
│   ├── Boundary Statement
│   └── CTA to Workspace
├── Workspace
│   ├── Founder Dossier
│   ├── VC Question Generation
│   ├── Founder Response
│   ├── Reflection Report
│   ├── Risk Map
│   └── Download / Export
├── Feature Pages
│   ├── Pressure Test
│   ├── Founder Dossier
│   └── Reflection Report
├── Profile Prototype
│   ├── Prototype-only identity card
│   ├── Static usage overview
│   ├── Static report history concept
│   └── Coming soon labels
└── Portfolio Materials
    ├── Screenshots
    ├── Demo Script
    └── Refactor Summary
```

## Page-level responsibilities

### Public Landing Page

The landing page explains the product to outsiders. It should not run the VC pressure test directly. It should answer:

- What is VCReady?
- Who is it for?
- What problem does it solve?
- What does it output?
- What does it not promise?
- Where should the user start?

### Workspace

The workspace is the real working area. It should preserve the current cold, memo-like, VC pressure-test feeling.

The workspace should remain the only place where real user input, model calls, report generation, and report rendering happen.

### Feature Pages

Feature pages are explanatory pages only. They should not call the LLM. Their job is to make the product understandable in a portfolio or demo setting.

### Profile Prototype

The profile page is a static concept page only. It must clearly say:

```text
Prototype only
Local demo
No persistent account system yet
```

## Non-promises

VCReady must not claim:

- guaranteed fundraising results
- investment advice
- real VC evaluation authority
- real investor access
- complete account system
- persistent database
- production-grade security
- automated legal/financial advice

## Phase 1 output boundary

Phase 1 produces planning documents only. Implementation begins later.
