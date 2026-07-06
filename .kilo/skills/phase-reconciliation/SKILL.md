---
name: phase-reconciliation
description: >
  Used by `dependency-planner`. Reconcile feature-priority-based phases with dependency topology.

---

## Rule

`task.phase >= max(dep.phase for dep in task.dependencies)`

A task cannot ship before its prerequisites.

## Pseudocode

```
for task in topological_order:
    if no dependencies:
        task.phase = priority_to_phase(task)
    else:
        dep_max = max(dep.phase for dep in task.dependencies)
        prio = priority_to_phase(task)
        task.phase = max(dep_max, prio)
        if prio < dep_max:
            warnings.append({
              "task": task.id,
              "issue": f"Priority suggests {prio}, deps force {dep_max}",
              "blocking_deps": [d.id for d in task.dependencies if d.phase == dep_max]
            })
```

## Mapping

| Source | Phase |
|---|---|
| blocking foundation | 1 |
| feature.mvp = true | 2 |
| feature.priority = P1 | 3 |
| feature.priority = P2 | 4 |
| unspecified | warning, default 3 |

## When Reconciliation Surfaces Issues

- **MVP feature blocked by post-MVP work** — usually a misclassified dependency; user re-prioritizes or removes the dep
- **Foundation task pushed into Phase 2** — wrongly extracted; foundation shouldn't have that dependency

## Don't Silently Demote

Phases only go up the topological order, never down. Don't demote a dependency to match a higher-priority dependent silently — warn.
