---
name: task-schema
description: >
  The canonical structure every task must conform to. All analyzers emit this; the orchestrator merges them; the validator enforces it.
---


## YAML Form (on disk)

```yaml
id: T-018                          # globally unique, T-NNN
title: "Implement POST /auth/login endpoint"
description: |
  What the task accomplishes. Keep it short — the coding agent reads
  the source documents listed in requirements_to_read for detail.

phase: 2                           # 1..4
parallel_group: PG-003             # PG-NNN, assigned by dependency-planner
agent_type: backend                # backend | frontend | infra | design-system | qa | docs
status: todo                       # todo | in_progress | done | archived
checkbox: "[ ]"                    # "[ ]" or "[x]" or "[~]"

# ─── Execution metadata ───────────────────────────────────────────────
estimated_hours: 6                 # ≤24 hours. Larger → split.
blocking: false                    # true if other tasks cannot start without this
dependencies:                      # other task IDs that must complete first
  - T-005
  - T-012
shared_resources: []               # named locks: "db_migration", "openapi_spec"
files_to_modify:                   # predicted; coding agent will refine
  - "apps/api/src/routes/auth.ts"

# ─── Inputs for the downstream coding system ──────────────────────────
# CRITICAL: list the exact documents and sections the coding agent must
# read before starting. No generic entries like "the SDD".
requirements_to_read:
  - path: ".nitro/steering/sdd/auth.md"
    sections: ["§2 Login flow", "§4 Token format"]
    reason: "Endpoint contract and JWT claims"
  - path: ".nitro/steering/sdd/data-model.md"
    sections: ["§User entity"]
    reason: "Field names and types"

# ─── Contracts ────────────────────────────────────────────────────────
outputs:                           # named artifacts other tasks reference
  - "auth_login_endpoint"
input_contracts:                   # named artifacts this task consumes
  - "user_db_schema"

# ─── Done definition ──────────────────────────────────────────────────
acceptance_criteria:
  - "Valid credentials return 200 + JWT"
  - "Invalid credentials return 401"

# ─── Provenance ───────────────────────────────────────────────────────
source_documents:                  # which source docs this task derived from
  - ".nitro/steering/sdd/auth.md"
source_agents:                     # which analyzers produced or merged this
  - sdd-analyzer
created_in_plan_version: 1
last_modified_plan_version: 1
```

## JSON Form (sub-agent → orchestrator)

Same fields, JSON shape, plus:

```json
{
  "tasks": [ ... ],
  "notes_for_orchestrator": [
    "Sections found but undefined: ..."
  ]
}
```

## Required Fields

`id`, `title`, `description`, `phase`, `agent_type`, `status`, `checkbox`, `estimated_hours`, `blocking`, `dependencies` (may be empty), `files_to_modify`, `requirements_to_read`, `outputs`, `acceptance_criteria`, `source_documents`, `source_agents`.

`parallel_group` is filled by `dependency-planner`, not analyzers.

## INVEST-T

Every task:

- **I**ndependent — minimal coupling
- **N**egotiable — implementation open
- **V**aluable — produces a named output
- **E**stimable — `estimated_hours` set
- **S**mall — ≤24 hours
- **T**estable — acceptance criteria present
- **T**argeted — `requirements_to_read` specific
