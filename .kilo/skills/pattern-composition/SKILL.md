---
name: pattern-composition
description: >
  Used by `ui-system-analyzer`. Model UI patterns (form, list-with-filters, app shell).

---

## Pattern vs Component

- **Component** — atomic / molecular UI unit (Button, Input, Card)
- **Pattern** — composition of components solving a recurring UI problem (form-with-validation, list-with-filters, empty state, app shell)

Patterns usually live in `ui_patterns/`. Components in `component_specs/`.

## Pattern vs Page

Most common confusion.

- **Pattern** — reusable abstraction usable in many pages; no business logic; in `patterns/` or `compositions/`
- **Page-orchestration** — specific to one page; knows business data and routes; in `pages/<page>/`

If reusable across pages → pattern (your scope).
If specific to one screen → page (sdd-client-analyzer's scope).

## Dependencies

Patterns depend on:
- The components they compose
- Possibly other patterns (Form pattern uses Field pattern)
- Theme provider / design tokens (transitively via component deps)

## Acceptance Criteria

- "Renders N component types from the design system"
- "Pattern API accepts X props matching the spec"
- "Handles edge cases listed in spec"
- "Storybook composition demonstrating typical use"

## Common Patterns

| Pattern | Composes |
|---|---|
| Form | Input, Select, Checkbox, Button, FieldLabel |
| List | Table/Card list, Pagination, EmptyState |
| Dialog flow | Modal, Button, Stepper |
| App shell | AppBar, Sidebar, NavItem, Avatar |
| Empty state | Illustration, Heading, Body, Button |
| Toast system | Toast component + provider + queue |

## When Underspecified

If `ui_patterns/` describes a pattern without listing components, infer from visual/behavior and add a `notes_for_orchestrator` entry.
