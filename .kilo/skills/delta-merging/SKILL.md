---
name: delta-merging
description: >
  Used by `incremental-planner`. Integrate new tasks with the existing plan safely.

---

## Three Kinds of Delta

1. **Pure additions** — new tasks unrelated to existing ones. Easy: append.
2. **Bridging additions** — new tasks consuming existing contracts. Easy: link via `outputs-index`.
3. **Modifications** — new feature changes scope of an existing task.

## When to Modify vs Add

| Situation | Decision |
|---|---|
| Modification adds <2 acceptance criteria to a not-yet-started task | Modify (append) |
| Modification touches a `done` task | New task always — don't reopen completed work |
| Modification touches an archived task | New task; flag archive reference; don't reactivate unless user confirms |
| Modification ~doubles the task size | New task |
| Modification is structural (new files) | New task |
| Same surface, small extension | Modify |

**Bias toward new tasks.** Recoverable. Modifying in-flight tasks risks confusing already-dispatched coding agents.

## Modification Operations

```json
{
  "task_id": "T-018",
  "operations": [
    {"field": "acceptance_criteria", "op": "append", "items": ["..."]},
    {"field": "files_to_modify", "op": "append", "items": ["..."]},
    {"field": "requirements_to_read", "op": "append", "items": [{...}]},
    {"field": "estimated_hours", "op": "set", "value": 8},
    {"field": "outputs", "op": "no_change"}
  ]
}
```

**Operations on `outputs` are forbidden** — changing outputs breaks every dependent. If a feature forces this, create a new task instead.

## Linking via outputs-index

```
outputs_index["jwt_service"] == "T-018"
```

New task consuming `jwt_service`:

```json
{
  "id": "T-NEW-001",
  "input_contracts": ["jwt_service"],
  "dependencies": ["T-018"]
}
```

If a contract isn't in the live index:
- Maybe produced by another new task in this delta → link within delta
- Maybe in archive → flag `archived_contract_references` (orchestrator decides)
- Otherwise → missing dependency, surface as a note

## Preserve IDs

Never propose renaming existing tasks. New tasks get IDs at the end of the current sequence. Orchestrator handles final assignment; you use placeholders.

## Output

```json
{
  "new_tasks": [...],
  "modifications_to_existing": [...],
  "new_dependency_edges": [
    {"from": "T-018", "to": "T-NEW-001", "reason": "..."}
  ],
  "archived_contract_references": [
    {"contract": "legacy_user_schema", "archived_task_id": "T-005", "consuming_new_task": "T-NEW-002"}
  ],
  "warnings": [...]
}
```
