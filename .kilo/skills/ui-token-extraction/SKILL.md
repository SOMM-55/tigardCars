---
name: ui-token-extraction
description: >
  Used by `ui-system-analyzer`. Structure design token tasks.

---

## Categories

| Category | Examples |
|---|---|
| Color | brand palette, semantic (success/warning/danger), neutrals |
| Typography | font families, type scale, line height, weights |
| Spacing | spatial scale, padding/gap tokens |
| Radii | corner radius scale |
| Shadow / Elevation | levels, focus rings |
| Motion | durations, easings |
| Z-index | layering scale |
| Breakpoints | viewport sizes |
| Iconography | size scale, stroke widths |

## Granularity

Default: one task per category. Keeps work small and parallel-friendly.

Alternative: one consolidated `design_tokens_setup` task if the project keeps them together (Style Dictionary, Tailwind config). Choose based on the `design_tokens/` layout.

## Outputs

Each task outputs a named contract: `design_tokens_color`, `design_tokens_typography`, etc., or a consolidated `design_tokens`.

## Light / Dark Modes

If foundations specify multiple themes:
- Color tokens task handles both modes (one task, two value sets)
- A separate `theme_provider` task (UI foundation) consumes them and handles switching

## Validation

For each token reference in `ui_foundations/`, `component_specs/`, `ui_patterns/`:
- Confirm it's defined in `design_tokens/`
- If not, add a `notes_for_orchestrator` entry — do not invent values
