---
name: feature-extraction
description: >
  Used by `product-analyzer`. How to identify what counts as a feature.

---

## Definitions

- **Feature** — independently shippable user-facing capability with a distinct name
- **Sub-feature** — meaningful slice within a feature, big enough to phase separately
- **User story** — behavior statement; many belong to one feature

## Granularity Rule

A feature must be independently shippable. If feature X delivers user value without feature Y, X is a feature, not a sub-feature of Y.

## Process

1. Scan PRD section headers
2. For each, classify: feature, sub-feature, cross-cutting concern (not a feature)
3. Pull user stories from "as a user…" patterns
4. Pull acceptance signals from given/when/then or explicit AC blocks

## Output Shape

```json
{
  "feature_id": "feat-auth",
  "name": "User Authentication",
  "summary": "...",
  "mvp": true,
  "priority": "P0",
  "user_stories": ["..."],
  "acceptance_criteria": ["..."],
  "depends_on_features": [],
  "source_documents": [".nitro/steering/prd/auth.md"]
}
```

## Don't Over-Extract

A PRD with 30 section headers usually has 6–10 features. Most headers are context, not features.

## Don't Invent

If the PRD doesn't describe a feature, you don't extract one. Surface gaps in `notes_for_orchestrator`.
