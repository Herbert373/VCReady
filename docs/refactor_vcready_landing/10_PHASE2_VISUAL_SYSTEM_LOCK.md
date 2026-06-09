# 10_PHASE2_VISUAL_SYSTEM_LOCK

Generated at: 2026-06-09 09:21:19 +08:00

## Purpose

This document locks the visual direction for the VCReady landing/workspace refactor before implementation. Phase 2 does not change UI code.

## Visual principle

VCReady should have a dual visual system:

```text
Warm public product surface + cold VC pressure-test workspace
```

The landing page should feel accessible, clear, and premium. The workspace should retain the pressure, skepticism, and data-room seriousness of the VC interview environment.

## Public Landing Page visual system

### Mood

- Warm white
- Cream / ivory background
- Light gold-orange accent
- Dark gray-blue text
- Calm premium SaaS feeling
- Founder-friendly but not soft

### Suggested palette roles

| Role | Description |
|---|---|
| Page background | Warm white / cream |
| Main text | Dark gray-blue |
| Secondary text | Muted slate gray |
| Accent | Light gold-orange |
| CTA fill | Deep blue or dark gray-blue |
| CTA hover | Slightly warmer or darker version |
| Card background | White with subtle warm tint |
| Border | Low-contrast warm gray |

Do not use a loud neon startup palette. VCReady should feel like a serious preparation room, not a consumer entertainment app.

### Layout rhythm

Landing page sections should use a calm vertical rhythm:

1. Full-width hero
2. Problem explanation
3. Product mechanism strip
4. Feature card grid
5. How-it-works steps
6. Assessment framework
7. Report preview
8. Boundary / disclaimer
9. Final CTA

### Hero section composition

Recommended structure:

```text
Left: value proposition + CTA
Right: abstract report / memo / question card mockup
```

The right-side mockup should suggest:

- VC-style question card
- Founder dossier snippet
- Risk Map preview
- Report memo fragment

No fake logos, no fake investor names, no fake financing result.

### Cards

Feature cards should be:

- Large enough to read quickly
- 2-column or 3-column depending on viewport
- Rounded but not playful
- With short titles and one-sentence explanations
- Optional small labels such as `Input`, `Question`, `Report`, `Risk`

### CTA design

Primary CTA should be visually decisive:

```text
Start Pressure Test
```

Secondary CTA should be quieter:

```text
View Example Report
```

Do not create more than two CTA styles on the same page.

## Workspace visual system

### Mood

- Darker
- Sharper
- More memo-like
- Investor interview / data room atmosphere
- High contrast for report readability

### Preserve from current product

- VC pressure-test identity
- Founder dossier input seriousness
- Report dashboard structure
- Risk Map as accepted baseline
- Bilingual capability if currently present

### Workspace must not become warm and decorative

The landing page can be warm. The workspace should remain cold enough to communicate pressure and scrutiny.

## Feature Pages visual system

Feature pages should reuse landing page warmth but become more educational.

Structure:

```text
Feature Hero
Explanation Blocks
Example Cards
Boundary Note
CTA to Workspace
```

Each feature page should look like part of the same product, not an unrelated blog post.

## Profile Prototype visual system

Profile page should look like a future product concept, not a fully launched account system.

Required visual markers:

- `Prototype only` badge
- `Local demo` label
- `No persistent account system yet` note
- Soft cards for future modules
- No fake real history

## Typography guidance

| Layer | Use |
|---|---|
| H1 | One sharp product claim |
| H2 | Section claim |
| H3 | Card title |
| Body | Short explanation |
| Caption | Boundary, prototype note, disclaimer |

Avoid long paragraphs on landing pages. Save detailed reasoning for docs and feature pages.

## Visual no-go list

- Do not use cartoon startup visuals.
- Do not overuse gradients.
- Do not imply VC endorsement.
- Do not show fake funding outcomes.
- Do not show fake persistent user history.
- Do not use images that suggest a real investor database.
- Do not make the workspace look like a generic chatbot.

## Implementation note for later phases

When code implementation begins, visual constants should be centralized in CSS or helper functions where possible. Phase 2 only locks the visual intent; it does not implement it.
