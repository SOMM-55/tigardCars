---
name: sdd-client-extraction
description: >
  Used by `sdd-client-analyzer`. Convert client SDDs into frontend tasks.

---

## Section-to-Task Mapping

| Section | Becomes |
|---|---|
| Routes / Routing | Router setup + per route-group tasks |
| State Management | One task per global store / context |
| API Clients | One task per typed client (per backend service) |
| Pages | One task per page-level orchestration |
| Auth Client | Token storage + refresh + route guards (typically 2–3 tasks) |
| Caching / Data Fetching | Query-client setup + invalidation conventions |
| Error Handling | Error boundary + API error normalization |
| i18n | Setup + per-locale tasks if multiple |

## Page Task Pattern

Pages are orchestration, not components:

- Compose components (produced by `ui-system-analyzer`)
- Wire data fetching
- Handle loading and error states
- Connect actions to API calls

A page task's `requirements_to_read` includes:
- The user-flow doc for the journey this page belongs to
- The IA doc for navigation context
- The backend SDD section for endpoints the page calls
- The component spec files for composed components

## Don't Duplicate UI Work

If the client SDD describes a card with inputs and a button:
- Component-level work → not your task (`ui-system-analyzer` owns it)
- Page-level orchestration (form state, submit, redirect) → your task

## Granularity

- One typed API client per backend service (not per endpoint)
- Auth client → 2–3 tasks: token storage, refresh, route guards
- State management → split by domain (auth, preferences, per-feature), not one giant task
- If the project uses codegen from OpenAPI → one client task per service ("wire codegen for service X"), not per endpoint
