# Validation Checklist — UI System Agent (Mode B)

Run this checklist **silently** before saving any file. Fix every failure before reporting completion.

---

## Pre-Save Checklist

```
PREREQUISITES
□ .nitro/steering/ui_foundations/ contains all 7 required files
□ .nitro/steering/sdd/ and .nitro/steering/sdd_client/ were read before speccing components
□ Technology stack confirmed with user
□ Token format confirmed with user

UI INVENTORY
□ UI Inventory was run before writing any component spec
□ Inventory was shown to user and confirmed
□ All components in confirmed inventory are spec'd

DESIGN TOKENS
□ $source traces back to correct ui_foundations file
□ All token names match semantic names in ui_foundations
□ No component-specific hardcoding in token names
□ Machine-readable format matches confirmed stack
□ Light and dark values both present when theme = both
□ Token counts within hard caps:
    color   ≤ 12
    spacing ≤ 8
    type sizes ≤ 6
    duration ≤ 3
    easing   ≤ 2

COMPONENT SPECS
□ Assumptions / Constraints / Dependencies / Non-Goals / Open Questions present
□ Dependencies section lists specific foundation files consumed
□ All variants documented
□ All sizes documented
□ All states documented:
    Default / Hover / Active / Focus / Disabled / Loading
□ Anatomy section present
□ Token Usage table uses semantic token names only — no raw hex
□ Accessibility section present
□ Touch target ≥ 44×44px stated
□ Focus ring rule stated (2px solid color.accent, 2px offset)
□ Responsive behavior section present
□ Do / Don't usage guidelines present

UI PATTERNS
□ Pattern Goal stated
□ Layout Structure shown
□ Components Used list present
□ Interaction Flow documented
□ States table complete:
    Empty / Loading / Error / Populated for each surface
□ Accessibility notes present
□ Responsive rules present
□ Common Variants listed
□ Assumptions / Constraints / Dependencies / Non-Goals / Open Questions present

OUTPUT
□ All files in English
□ All files saved to correct paths:
    design_tokens/   → .nitro/steering/design_tokens/
    component_specs/ → .nitro/steering/component_specs/
    ui_patterns/     → .nitro/steering/ui_patterns/
□ No [TBD], ???, [FILL ME IN] in any file
□ Version number and date in every file header
□ Existing files versioned (not deleted) if Fresh mode was chosen
```

---

## Anti-Pattern Scanner

Before saving, check for these patterns and fix any found:

| Anti-pattern | Detection | Fix |
|---|---|---|
| Component-specific token name | Token named after a component, e.g. `button.background` | Rename to semantic, e.g. `color.accent` |
| Raw hex in prose or token table | Hex not tracing to `color_system.md` | Ensure value is pulled from `color_system.md` |
| Motion duration > 300ms | Check duration values | Cap at 300ms |
| Touch target < 44px | Check component state descriptions | Fix to 44×44px minimum |
| `outline: none` without replacement | Check focus state rules | Add accessible focus ring |
| Token not in ui_foundations | Token name that doesn't appear in any foundation file | Trace or remove |
| Re-running discovery interview | Interview questions in Mode B output | Remove — discovery is Mode A's job |
| Mode A files produced by this agent | ui_foundations/ path in output | Redirect to Mode A agent |
