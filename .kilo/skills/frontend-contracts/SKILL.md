---
name: frontend-contracts
description: >
  Used by `sdd-client-analyzer`. Which client-side artifacts must be `blocking: true`.

---

## Blocking Client-Side Artifacts

- Typed API clients — pages and stores import them
- Auth context / store — route guards, headers, redirects depend on it
- Routing setup — every page registers with it
- Theme / token providers — components consume them at runtime
- Global error boundary — pages mount inside it
- Query client / data layer setup — features register queries
- i18n provider setup — translation calls fail without it

## Non-Blocking

- Individual pages
- Feature-specific stores (scoped consumption)
- Page-specific hooks
- Component compositions

## Detection

If task X is incomplete and another task fails at build or runtime → blocking. Otherwise not.

## Don't Re-Declare External Contracts

Don't mark "design tokens" or "backend API contract" as blocking from the client side — they're already blocking in their own analyzer's output. Reference them as `input_contracts` and let the orchestrator wire the dependency.
