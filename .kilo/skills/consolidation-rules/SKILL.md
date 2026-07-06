---
name: consolidation-rules
description: >
  How the orchestrator merges sub-agent outputs into one task list.

---

## Deduplication

Two tasks are duplicates if any holds:

1. Same `outputs` value (both produce `auth_login_endpoint`)
2. `files_to_modify` overlap ≥80% AND same `agent_type`
3. Semantically equivalent `title` covering the same scope

When merging:

- Keep the more specific `description`
- Union acceptance criteria (dedupe lines)
- Union `requirements_to_read` entries
- Union dependencies
- Use the higher `estimated_hours`
- Preserve the ID from the more detailed source
- `source_documents` and `source_agents` become arrays

## Cross-Reference Validation

After dedup:

- Every `dependencies` ID exists in the merged list
- Every `input_contracts` name has a producing `outputs` somewhere (live or archived)
- If a UI task references an API, an SDD task produces that API
- If two tasks claim the same output, merge or rename

Unresolved references → `AskUserQuestion`.

## ID Reconciliation

Fresh Mode A: assign `T-001`, `T-002`, … in topological order.

Mode A rebuild (plan exists):
- Tasks with the same `outputs` as a prior live task → reuse the old ID and completion state
- Tasks with the same `outputs` as an archived task → use a new ID; reference the archive in `notes` (or, if a true rebuild, ask the user whether to reactivate)
- New tasks → IDs starting from `max(prior_id) + 1`

Never renumber existing tasks.

## Phase Assignment Bridge

Phases come from `product-analyzer`'s priority + dependency reality (resolved in `dependency-planner` via `phase-reconciliation`). The orchestrator passes both inputs to dependency-planner; it doesn't decide phases directly.

## Conflict Surfaces

Surface to the user:

- PRD says feature is MVP, but no SDD coverage exists
- SDD defines an endpoint no UI flow uses
- Two analyzers disagree on phase priority
- A user-flow step references an undefined page
