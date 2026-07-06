---
name: document-paths
description: >
  Canonical paths to source documentation.

---

## Source Documentation Roots

```
.nitro/steering/
├── prd/                  # Product Requirements
├── brd/                  # Business Requirements
├── user_flow_map/        # User journeys
├── IA/                   # Information Architecture
├── layout/               # Layout primitives
├── ui_foundations/       # Typography, spacing, motion principles
├── sdd/                  # Backend System Design
├── sdd_client/           # Client System Design
├── design_tokens/        # Design tokens
├── component_specs/      # Component specifications
└── ui_patterns/          # Reusable UI patterns
```

## Plan Output Root

```
.nitro/steering/plans/    # only the orchestrator writes here
```

## Read/Write Permissions

| Agent | Reads | Writes |
|---|---|---|
| plan-orchestrator | all `.nitro/steering/**` | only `.nitro/steering/plans/**` |
| product-analyzer | `prd/`, `brd/` | nothing |
| ux-flow-analyzer | `user_flow_map/`, `IA/` | nothing |
| ui-system-analyzer | `layout/`, `ui_foundations/`, `design_tokens/`, `component_specs/`, `ui_patterns/` | nothing |
| sdd-analyzer | `sdd/` | nothing |
| sdd-client-analyzer | `sdd_client/` | nothing |
| dependency-planner | input passed by orchestrator | nothing |
| plan-validator | input passed by orchestrator | nothing |
| incremental-planner | scoped subset of source docs | nothing |

Sub-agents return JSON.

## Missing Directories

If an expected directory is empty or missing, the analyzer returns `tasks: []` with a `notes_for_orchestrator` entry. It does not invent content. The orchestrator may ask the user.
