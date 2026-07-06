---
name: plan-file-layout
description: >
  File structure for `.nitro/steering/plans/`.

---


## Directory Structure

```
.nitro/steering/plans/
├── README.md                  # human overview, phase progress
├── manifest.yaml              # single source of truth for plan metadata
├── outputs-index.yaml         # live contract_name → task_id (cheap lookup)
├── changelog.md               # append-only update log
├── phases/
│   ├── phase-1-foundation.md
│   ├── phase-2-core.md
│   ├── phase-3-extended.md
│   └── phase-4-polish.md
├── tasks/
│   └── T-NNN.yaml             # one per live task
├── graphs/
│   ├── dependency-graph.yaml
│   ├── parallel-groups.yaml
│   └── mermaid.md             # mermaid visualization
└── archive/                   # see archive-protocol skill
    ├── outputs-index.yaml
    ├── tasks-index.yaml
    └── tasks/
        └── T-NNN.yaml
```

## `manifest.yaml`

```yaml
plan_version: 3                # incremented on every write
generated_at: 2026-05-17T10:00:00Z
mode_last_run: incremental
source_documents_snapshot:
  prd: [".nitro/steering/prd/v1.2.md"]
  sdd: [".nitro/steering/sdd/auth.md", "..."]
totals:
  live_tasks: 38
  archived_tasks: 9
  completed_live: 6
  phases: 4
  parallel_groups: 9
  blocking_tasks: 5
```

## `tasks/T-NNN.yaml`

One file per live task. Schema in `task-schema`. Must include `requirements_to_read` — explicit, with reasons.

## `phases/phase-N-*.md`

Human-readable list of live tasks for that phase, grouped by parallel group, using checkbox format from `checkbox-format`. Archived tasks not shown (only a footer count).

## `outputs-index.yaml`

Compact map of every live contract name to its producing task ID. Single source of truth for cross-task references. Updated on every plan write.

## `changelog.md`

Append-only. Every run adds an entry:

```markdown
## 2026-05-17 — Incremental update

**Trigger:** User reported "social login added per PRD §4.5"

**New tasks:** T-048, T-049, T-050

**Modified:** none

**Archived:** none

**No completed tasks were affected.**
```

## Atomicity

Write order (so the manifest only commits when everything else is in place):

1. `tasks/T-NNN.yaml`
2. `graphs/*.yaml`
3. `phases/*.md`
4. `outputs-index.yaml`
5. `archive/*` (if archiving in this run)
6. `changelog.md`
7. `manifest.yaml` — last; its `plan_version` increment commits the update
8. `README.md`

If anything fails mid-write, the old `manifest.yaml` still points at the previous valid state.
