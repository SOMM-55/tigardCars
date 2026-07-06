---
name: navigation-modeling
description: >
  Used by `ux-flow-analyzer`. Model page-to-page connections.

---

## Edge Types

| Type | Meaning |
|---|---|
| `redirect` | Automatic navigation (after action, after auth) |
| `link` | User-initiated (click, tap) |
| `modal` | Overlay; not a route change |
| `back` | Returns to previous page |
| `replace` | Navigates without history |
| `external` | Leaves the application |

## Page IDs

`page-{kebab-case-name}` — use the page's purpose, not its route. Routes change; purposes don't.

## Auth-Required Flag

`true` if:
- Page reachable only after login
- Any incoming edge originates from an authenticated page
- Flow map explicitly marks it protected

`false` if reachable in an unauthenticated state.

Ambiguous → `"unspecified"` + a note.

## Page Hierarchy

If IA defines a tree (dashboard → analytics → engagement), set `parent`. Drives breadcrumbs and back-button behavior.

## Cross-Journey Pages

A page like `page-settings` may appear in many journeys. List it once in `pages`, reference from each `journey.steps`. Do not duplicate.

## Modals as Pages

- Modal with a URL (deep-linkable) → page
- Pure UI overlay → not a page (it's a component, out of scope)

The IA usually clarifies. When unclear, treat as a page only if reachable via a route.
