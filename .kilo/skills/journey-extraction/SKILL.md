---
name: journey-extraction
description: >
  Used by `ux-flow-analyzer`. Identify and structure user journeys.

---


## What Counts as a Journey

A goal-oriented sequence of pages delivering user value. Starts at an entry point, ends at value realization.

## Common Patterns

- Onboarding (signup → verify → setup → first use)
- Authentication (login → dashboard, with 2FA branch)
- Transactional (list → detail → action → confirmation)
- Recovery (error / abandonment → recovery flow → original goal)
- Settings change
- Multi-step wizard

## Branches

Capture as `alternate_paths` rather than separate journeys:

- "Already have an account?" — branch from signup to login
- "Forgot password?" — branch from login to recovery
- "Skip for now" — branch in onboarding

Rule: one happy path + branches → one journey. Distinct value-realization endpoint → separate journey.

## Journey-Level Tasks

Per journey, typically:

1. "Implement navigation transitions for journey-X" — `agent_type: frontend`, depends on the page tasks
2. "E2E test: journey-X happy path" — `agent_type: qa`, depends on all pages
3. Optional: one task per significant alternate path needing separate E2E coverage

Don't create a task per navigation edge — over-fragments.

## When Flow Map Is Missing

If a feature exists in PRD but no user flow map describes it:

```json
{
  "notes_for_orchestrator": "Feature 'feat-billing' has no user flow map — pages and journeys for billing cannot be extracted"
}
```

Do not invent the journey from PRD alone.
