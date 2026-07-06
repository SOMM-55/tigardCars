---
name: component-extraction
description: >
  Used by `ui-system-analyzer`. One spec → one task.

---

## Rule

`component_specs/<component>.md` → one task. Exceptions:

1. Multiple components per spec file → split per component
2. Genuinely complex component (DataTable with virtualization, expansion, selection, etc.) → may split into 2–3 tasks (base, interactive, advanced) only when the unsplit version would exceed 24 hours

## Variants and States Stay One Task

A button with 4 variants × 3 sizes × 5 states is **one task**. The matrix is acceptance criteria, not separate tasks. Splitting fragments work and creates merge conflicts.

## Title

`"Implement <ComponentName> component"`. Variant info goes in acceptance criteria, not the title.

## Dependencies

Each component depends on:
- The relevant design token tasks
- The theme provider (if multi-theme)
- The base foundation task

Some depend on other components: `Dropdown` → `Popover` + `Button`; `Modal` → `Portal` + `FocusTrap`; `Select` → `Dropdown` + `Input`.

## Files To Modify (Predicted)

Without knowing the repo layout, predict spec-derived paths. If `sdd_client/` specifies file conventions, follow them. Otherwise predict idiomatically and note that the orchestrator may need to ask.

## Documentation

Don't create separate "document this component" tasks. Storybook / MDX is part of each component's done definition.

## Iconography

Icon system is a separate Phase 1 foundation task. Component tasks reference it as `input_contracts: ["icon_system"]`. Don't create per-icon tasks unless the project has bespoke custom icon implementations.
