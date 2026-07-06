---
name: validation-rules
description: >
  Used by `plan-validator`. The full check matrix.

---


## A. Structural

- Required fields present per `task-schema`
- IDs unique
- IDs match `T-NNN`
- Parallel group IDs match `PG-NNN`
- Phase in {1, 2, 3, 4}

## B. Graph Integrity

- No cycles
- Every `dependencies` entry references an existing task
- Every `input_contracts` entry has a producing `outputs` somewhere
- No two live tasks produce the same `outputs`
- Every task in exactly one parallel group
- No two tasks in the same parallel group have a dependency edge
- No overlap in `files_to_modify` within a parallel group
- No overlap in `shared_resources` within a parallel group

## C. Phase Integrity

- `task.phase >= max(dep.phase)`
- Phase 1 tasks are foundation / blocking (sanity)

## D. INVEST-T Per Task

- **Small** — `estimated_hours ≤ 24` (error if violated)
- **Testable** — `acceptance_criteria` non-empty (error if empty; warn if <3)
- **Targeted** — `requirements_to_read` non-empty; each entry has `path`, `sections` (or "whole document"), and `reason` (error if violated)
- **Valuable** — `outputs` non-empty
- **Estimable** — `estimated_hours > 0`
- **Independent** — warn if >5 dependencies

## E. Coding-Agent Usability

- `requirements_to_read` has ≤5 entries (warn if more; possibly too broad)
- Every entry has a `reason` (error if missing)
- `files_to_modify` non-empty
- Acceptance criteria items observable/verifiable

## F. Completed Preservation

- Every previously-completed ID still exists (live or archived)
- Completed tasks have `status: done` and checkbox `[x]`
- Completed tasks' `outputs` unchanged

## G. Archive Consistency

- No live task lists an archived task as a direct `dependencies` entry without the orchestrator's explicit acknowledgment
- Archived `outputs` references in live tasks go through the archived-outputs-index (validator flags but does not block, since `archive-protocol` allows this with a warning)

## H. Manifest Consistency

- Total task count matches actual
- Completed count matches completed
- `outputs-index.yaml` matches live tasks' `outputs`

## Errors vs Warnings

**Errors block the plan:**
- Cycles
- Missing required fields
- Orphan dependencies
- Tasks > 24 hours
- Empty `requirements_to_read` or `acceptance_criteria`
- Parallel-group violations
- Phase-order violations

**Warnings pass the plan:**
- >5 dependencies on a task
- <3 acceptance criteria
- >5 `requirements_to_read` entries
- Singleton parallel groups in heavily-parallel phases
- Prescriptive descriptions

## Special Cases

- **Tiny projects** (<15 tasks): don't error on small plans
- **Mode B delta validation**: applies all rules to the merged plan; completed tasks are immutable inputs
