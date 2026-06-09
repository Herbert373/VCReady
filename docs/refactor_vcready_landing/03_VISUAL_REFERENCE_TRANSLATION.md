# 03_VISUAL_REFERENCE_TRANSLATION

Generated at: 2026-06-09 09:10:46 +08:00

## Purpose

This document translates the desired public-product feeling into a VCReady-specific visual system.

The goal is not to copy another project. The goal is to separate two product moods:

```text
Landing Page = warm, clear, trustworthy, founder-facing
Workspace = cold, sharp, VC memo / data room / pressure-test feeling
```

## Visual direction

### Public Landing Page

The landing page should feel like a serious but approachable founder tool.

Preferred visual language:

- warm white / cream background
- light gold or orange accents
- deep gray-blue text
- calm spacing
- large hero section
- strong one-sentence value proposition
- two CTA buttons
- large feature cards
- report preview block
- clear boundary statement

### Workspace

The workspace should keep the existing darker, sharper VC review feeling.

Preferred visual language:

- deep background
- memo-like cards
- precise labels
- pressure-test tone
- structured report sections
- risk map card
- investor-style critique

## Navigation structure

A future implementation may use Streamlit multipage navigation:

```text
app.py
pages/
  01_Workspace.py
  02_Pressure_Test.py
  03_Founder_Dossier.py
  04_Reflection_Report.py
  05_Profile.py
```

The public landing page should be the entry point. The workspace should remain accessible through a clear CTA.

## Landing page section rhythm

Recommended order:

1. Navbar
2. Hero
3. Problem
4. Product mechanism
5. Feature cards
6. How it works
7. Report preview
8. Boundary statement
9. Final CTA
10. Footer

## Design principles

### Principle 1: Explain before interacting

The public page should make the product understandable before the user enters the workspace.

### Principle 2: Warm shell, cold core

The public shell reduces intimidation. The workspace reintroduces the pressure-test intensity.

### Principle 3: Product evidence over visual decoration

Portfolio screenshots should prove product logic, not just aesthetics.

### Principle 4: Do not over-promise

Every page must preserve the boundary that this is a local demo / prototype unless later upgraded.

## Copy tone

Use direct founder language:

- "Can your logic survive investor questions?"
- "Before you meet investors, let VCReady break your logic first."
- "Stop selling the project. Defend why you are the founder who can win."

Avoid empty SaaS language:

- "AI-powered productivity platform"
- "All-in-one startup solution"
- "Revolutionary fundraising assistant"
