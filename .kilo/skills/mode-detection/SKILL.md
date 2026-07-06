---
name: mode-detection
description: >
  Decide between Mode A (full build) and Mode B (incremental update).

---

## Decision Tree

1. Does `.nitro/steering/plans/manifest.yaml` exist?
   - No → **Mode A** (fresh build)
   - Yes → continue

2. Does the user name a specific feature, change, or scope-delta? ("X was added", "update for Y", "the PRD changed on Z")
   - Yes → **Mode B**
   - No → continue

3. Does the user ask for a full rebuild? ("rebuild", "regenerate everything", "start over")
   - Yes → **Mode A** (rebuild, preserving completed task IDs and checkboxes)
   - No → continue

4. Ambiguous. Ask the user via `AskUserQuestion`:

```
"A plan already exists. How should I proceed?"
options:
  - "Incremental update — tell me what changed"
  - "Full rebuild — re-analyze all documentation"
  - "Just review the existing plan"
```

## Default Bias

When a plan exists and the user names a delta, default to **Mode B**. Don't trigger Mode A out of caution.

## Token Cost Implication

Mode A: reads all docs, runs all five analyzers in parallel. ~50–200k tokens of source material.
Mode B: reads only scoped docs. ~5–20k tokens. The archive (per `archive-protocol`) keeps this small even as the project grows.
