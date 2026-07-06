---
name: archive-protocol
description: >
  How completed work is archived so future planning runs don't waste tokens re-reading it.
---

## Why Archive

Once a task is `[x]` done and its outputs are stable, no agent has any reason to load its full body again. Keeping done tasks in the live plan inflates the orchestrator's context on every run — Mode B especially, which is supposed to be token-light.

Archive moves done work to a slim, lookup-only structure. The orchestrator never reads archived task bodies; it only consults the archive index when resolving contract references.

## Archive Trigger Rules

Move a task to the archive when **all** of these hold:

1. The task's `status: done` and checkbox `[x]`
2. All of its **direct** dependents are also `done` (its outputs have been consumed and the consumers also shipped) **OR** the orchestrator is in Mode B and the user has approved a "compact" pass
3. The task has been done for at least one plan version (i.e., not just-completed in this run)

The first condition alone is not enough. A done task whose dependent is still `todo` must stay live so the dependent can still link to it cleanly.

## Archive Structure

```
.nitro/steering/plans/
├── archive/
│   ├── outputs-index.yaml      # contract_name → archived_task_id
│   ├── tasks-index.yaml        # archived_task_id → summary (one line each)
│   └── tasks/
│       └── T-005.yaml          # the original task body, frozen
└── outputs-index.yaml          # live contract_name → live_task_id
```

The **live** `outputs-index.yaml` is the orchestrator's primary lookup surface. The **archived** one is consulted only when a live task references a contract that isn't in the live index.

## Live Outputs Index

Compact YAML, written by the orchestrator on every plan write:

```yaml
# .nitro/steering/plans/outputs-index.yaml
version: 3
live:
  auth_login_endpoint: T-018
  jwt_service: T-018
  user_db_schema: T-005
  design_tokens_color: T-002
# updated 2026-05-17, total entries: 38
```

The orchestrator loads this on every run — it's small (one line per contract) and lets agents resolve references without loading task bodies.

## Archive Outputs Index

```yaml
# .nitro/steering/plans/archive/outputs-index.yaml
archived:
  legacy_user_schema:
    task_id: T-005-ARCHIVED
    archived_at: 2026-04-10
    superseded_by: T-091   # if applicable
    summary: "Original User entity schema for v1 auth model"
```

## Tasks Index

A one-line summary per archived task — enough to know it exists, no body:

```yaml
# .nitro/steering/plans/archive/tasks-index.yaml
T-005:
  title: "Create User schema and migration"
  phase: 1
  archived_at: 2026-04-10
  outputs: [user_db_schema, user_migration]
  body: "archive/tasks/T-005.yaml"
```

## What the Orchestrator Reads From the Archive

By default: nothing. The live index suffices.

On demand:
- If a Mode B delta references a contract found only in the archive → read that one task body
- If the user asks "what was T-005?" → read that one task body
- If validation reports an issue traced to archived state → read targeted entries

The orchestrator does **not** scan the archive directory wholesale on every run.

## What Sub-Agents See

Sub-agents receive only the **live outputs index** as part of their dispatch payload. They never receive the archive. If they reference a contract that's not in the live index, they flag it as unknown and the orchestrator decides whether to consult the archive.

This is the mechanism that keeps Mode B cheap: completed work is invisible to analyzers by default.

## Reactivating an Archived Task

If a Mode B change requires modifying an archived task (rare — usually the system creates a new task instead, see `delta-merging`), the orchestrator:

1. Asks the user to confirm
2. Moves the task body back to `tasks/`
3. Sets `status: todo` and checkbox `[ ]`
4. Removes the entry from `archive/outputs-index.yaml`
5. Adds it back to live `outputs-index.yaml`
6. Logs the reactivation in `changelog.md`

Reactivation is exceptional. Default behavior is: create a new task that supersedes the archived one, leave the archived entry frozen.

## Compacting

The orchestrator may run an optional "compact" pass:

1. Walk live tasks; find candidates per the trigger rules
2. List candidates to the user via `AskUserQuestion`: "Archive these N done tasks to save tokens on future runs?"
3. On confirmation: move bodies to `archive/tasks/`, update both indexes, recompute `outputs-index.yaml`, log in `changelog.md`

Compacting never happens silently. The user always sees what's being archived.

## Display

Phase markdowns show only live tasks. A footer line summarizes the archive:

```markdown
---
*This phase has 4 archived tasks. See `archive/tasks-index.yaml` for the list.*
```

## What Never Goes in the Archive

- In-progress tasks
- Tasks blocking live work
- Tasks whose outputs are still being consumed by live tasks
- The current plan's `manifest.yaml` (it tracks all-time totals and lives at root)
