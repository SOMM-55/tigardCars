---
name: parallel-grouping
description: >
  Used by `dependency-planner`. The greedy algorithm for parallel-group assignment.

---

## Constraints (every pair in a group must satisfy all three)

1. **DAG independence** — no directed path between them either way
2. **File disjointness** — `files_to_modify` sets disjoint
3. **Resource disjointness** — `shared_resources` sets disjoint

## Greedy Algorithm

```
groups = []
for task in topological_order:
    placed = false
    for group in groups:
        if can_add(task, group):
            group.append(task); placed = true; break
    if not placed:
        groups.append([task])
```

Optimal grouping is NP-hard (graph coloring); greedy is sufficient at plan granularity.

## Tie-breakers

When multiple groups can accept a task:
1. Prefer the group with the most members of the same `agent_type` (one coding agent picks up the whole group efficiently)
2. Prefer the group whose existing members share the same phase

## Singleton Groups

Normal for:
- Blocking foundation tasks at start of Phase 1
- Tasks with broad `files_to_modify` (e.g., touching `tsconfig.json`)
- Tasks claiming a `shared_resource` (e.g., `db_migration` — one at a time)

## Refresh on Incremental Update

Re-run grouping only for:
- New tasks
- Existing tasks whose dependencies changed

Untouched groups stay as-is. Preserves IDs.

## Output

```json
{
  "parallel_groups": {
    "PG-001": {
      "tasks": ["T-001", "T-002"],
      "phase": 1,
      "primary_agent_type": "infra"
    }
  }
}
```
