---
name: priority-detection
description: >
  Used by `product-analyzer`. Recognize priority signals without inventing them.

---

## Signal Hierarchy (strongest to weakest)

1. Explicit phase / milestone assignment ("Phase 1 includes …")
2. MoSCoW labels (Must / Should / Could / Won't)
3. MVP markers ("MVP includes …", "Out of scope for v1")
4. Priority labels ("P0", "P1", "Critical")
5. Roadmap ordering (numbered list)
6. Business rule emphasis (BRD legal/regulatory must-haves)

## Mapping

| Signal | Priority |
|---|---|
| MVP / Must / P0 / Phase 1 | P0 |
| Should / P1 / Phase 2 | P1 |
| Could / P2 / Phase 3 / Post-MVP | P2 |
| Won't | exclude entirely (note in `notes_for_orchestrator`) |

## When Signals Conflict

PRD says feat-X is P0, BRD says P2 → **do not pick**. Emit `priority: "unspecified"` and note the conflict. The orchestrator asks.

## When No Signal Exists

`priority: "unspecified"` plus a note. Default behavior is **ask**, not guess.

## Foundation Phase

Some items always belong in Phase 1 regardless of feature priority:

- Repo / CI setup
- Database setup
- Auth infrastructure
- Logging / observability foundations
- Design token foundation
- Routing skeleton

These come from BRD operational requirements and foundational SDD/UI-system tasks — not from feature priorities. Don't accidentally tag them P2.
