---
name: sdd-extraction
description: >
  Used by `sdd-analyzer`. Convert SDD prose into discrete tasks.

---

## Section-to-Task Mapping

| SDD section | Becomes |
|---|---|
| Endpoints / API listings | One task per endpoint (group trivial CRUD up to 3) |
| Data Model / Entities | One task per entity |
| Services / Modules | One task per service skeleton |
| Middleware | One task per cross-cutting concern |
| External Integrations | One task per adapter |
| Configuration / Secrets | One task per config surface |
| Background Jobs / Events | One task per worker / handler |

## Granularity

- One endpoint = one task (unless trivial CRUD → group)
- One entity = one task
- One service skeleton = one task
- Migrations separate from entities they migrate

If a task exceeds ~24 hours, suggest a split.

## What NOT to Extract

- Per-endpoint test tasks — tests are part of each endpoint's done definition
- Separate documentation tasks — docs are part of done
- Endpoints / entities the SDD doesn't mention
- Observability or metrics unless the SDD says so

## When Sections Are Vague

If the SDD says "implement standard auth" without specifying mechanism, do **not** pick JWT or sessions. Emit a task and a `notes_for_orchestrator` entry — the orchestrator asks.

## Stay in Scope

You don't produce frontend tasks, UI tasks, or component tasks. Other analyzers handle those.
