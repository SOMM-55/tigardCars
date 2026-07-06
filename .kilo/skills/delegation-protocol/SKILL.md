---
name: delegation-protocol
description: >
  How the orchestrator invokes sub-agents.

---

## Pattern

Use the `Task` tool. For parallel dispatches (Mode A Step 3), emit multiple `Task` calls in a single message — separate messages serialize them.

## Payload

Every dispatch carries these four fields. Nothing more.

```yaml
mission: "<one-line goal>"
scope:
  read_paths:
    - ".nitro/steering/sdd/**/*"
  ignore_paths: []
existing_plan_summary:        # null in Mode A fresh
  completed_task_ids: ["T-001", "T-002"]
  live_outputs_index: { ... }   # the small lookup map
  total_live_tasks: 38
output_schema: "task-schema"
```

The `existing_plan_summary.live_outputs_index` lets the sub-agent skip tasks whose outputs already exist. Archived contracts are not included by default.

## What NOT to Pass

- Full content of other analyzers' outputs (each works only on its own domain)
- Full prior plan task bodies (summary is enough)
- Free-form instructions overlapping the agent's own definition

## Sequential Dispatches

These are sequential, not parallel:

1. `dependency-planner` — needs the consolidated task list
2. `plan-validator` — needs the graph from dependency-planner
3. `incremental-planner` (Mode B) — runs before the others; it produces the scoped task list

Everything else (the five analyzers in Mode A) runs in parallel.

## Failure Handling

If a sub-agent fails or returns malformed output:

1. Retry once with the same payload (transient failures happen)
2. Still failing → surface to the user via `AskUserQuestion`; do not silently skip the domain
