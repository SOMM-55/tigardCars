---
name: id-conventions
description: >
  Canonical ID rules used by all agents.

---

## Task IDs

Format: `T-NNN` (zero-padded, ≥ 001).

- Globally unique across all phases and the archive.
- Assigned by the orchestrator. Analyzers use temporary prefixes (`sdd-tmp-001`, `ui-tmp-001`, etc.); the orchestrator rewrites them.
- **Never reused.** A deleted or archived task's ID is retired forever.
- **Never renumbered.** Once on disk, `T-018` stays `T-018`.

## Phase IDs

Integer 1–4:

- 1 — Foundation
- 2 — Core (MVP)
- 3 — Extended (post-MVP)
- 4 — Polish

If a project needs more, the orchestrator asks the user.

## Parallel Group IDs

Format: `PG-NNN`. Assigned by `dependency-planner`.

Two tasks share a parallel group only when all three hold:
1. No dependency path between them in either direction
2. `files_to_modify` sets disjoint
3. `shared_resources` sets disjoint

A task belongs to exactly one group. Groups are flat (no nesting).

## Output Artifact Names

`snake_case`. Examples: `auth_login_endpoint`, `jwt_service`, `user_db_schema`.

- Must be unique across the live plan.
- Two tasks producing the same name → duplicate, must be merged or renamed.

## Archived Artifact Names

Archived tasks may share output names with live ones only if the live one supersedes it. The archive entry carries a `superseded_by: T-NNN` field.

## Input Contract Names

Same `snake_case`. Every `input_contract` must resolve to:
- An `output` of a live task in this task's transitive dependencies, **or**
- An `output` of an archived task (warns the orchestrator)

## Document References

Repository-relative paths starting with `.nitro/steering/`:

```yaml
- ".nitro/steering/sdd/auth.md"
```

Section references go in the `sections` array, not in the path.
