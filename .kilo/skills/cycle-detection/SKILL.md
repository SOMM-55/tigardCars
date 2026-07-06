---
name: cycle-detection
description: >
  Used by `dependency-planner`. Detect dependency cycles and report them usefully.

---

## Algorithm

Kahn's: compute in-degrees, push zero-in-degree nodes, decrement successors, repeat. Remaining nodes form cycles. Use Tarjan's SCC to extract cycle membership.

## Report Format

```json
{
  "cycle_id": "C1",
  "tasks": ["T-018", "T-031", "T-042", "T-018"],
  "cycle_edges": [
    {"from": "T-018", "to": "T-031", "reason": "..."}
  ],
  "suggestion": "Concrete suggestion the orchestrator can present to the user"
}
```

## Common Patterns

- **Schema ↔ middleware** — auth middleware depends on user schema, user schema cites something in auth → SDD mixed concerns; split one task
- **Frontend ↔ backend round-trip** — unusual; usually wrong
- **Mutual feature dependency** — A declares B prerequisite and vice versa

## Do Not Auto-Break

Cycle resolution is a design decision, not algorithmic. Surface the cycle clearly; the orchestrator asks the user.
