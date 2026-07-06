---
name: checkbox-format
description: >
  Markdown checkbox conventions so humans can tick tasks and the orchestrator can parse state on the next run.

---

## Format

```markdown
- [ ] **T-018** — Implement POST /auth/login endpoint
- [x] **T-019** — Implement password hashing utility
- [~] **T-020** — Wire login flow into client (in progress)
```

## States

| Marker | Meaning | status field |
|---|---|---|
| `[ ]` | Not started | `todo` |
| `[~]` | In progress | `in_progress` |
| `[x]` | Done | `done` |

Use lowercase `x`. Archived tasks are not in the phase markdowns at all — they live in the archive (see `archive-protocol`).

## Where Checkboxes Appear

- `phases/phase-N-*.md` — primary tick surface
- `README.md` — phase-level progress only (computed counts)

Checkboxes do **not** appear in:
- `tasks/T-NNN.yaml` — uses `status` field
- `graphs/*.yaml` — structural

## Monotonic Completion

`[x]` does not revert to `[ ]` automatically. If a user manually un-checks, the orchestrator treats it as "redo this" and notes affected dependents in `changelog.md`.

## Parsing on Next Run

The orchestrator parses `phases/*.md` for checkbox state and reconciles with `tasks/*.yaml`. If they disagree, the markdown wins — humans tick markdown.

## Per-Task Detail Block

```markdown
- [ ] **T-018** — Implement POST /auth/login endpoint
  - Phase 2 · PG-003 · backend · 6h · blocking
  - Requirements: `sdd/auth.md §2,§4`, `sdd/data-model.md §User`
  - Outputs: `auth_login_endpoint`, `jwt_service`
  - Depends on: T-005, T-012
```

Keep dense — one line per category. Full detail lives in `tasks/T-018.yaml`.
