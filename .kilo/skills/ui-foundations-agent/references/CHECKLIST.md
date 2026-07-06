# Validation Checklist — UI Foundations Agent (Mode A)

Run this checklist **silently** before saving any file. Fix every failure before reporting completion.

---

## Pre-Save Checklist

```
INITIALIZATION
□ AGENT.md was read before any output (if present)
□ SKILL.md was read before any output
□ Existing artifacts were checked before generating new ones
□ Mode confirmed (Update or Fresh)
□ All required upstream files were read — no improvisation

DISCOVERY INTERVIEW
□ All 4 rounds completed
□ Exactly one primary reference brand chosen
□ Density confirmed (compact / comfortable / spacious)
□ Theme mode confirmed (light / dark / both)
□ Exactly 3 voice adjectives — none from the banned list
□ At least 3 allowed copy examples provided
□ At least 3 banned copy examples provided
□ UI language confirmed (English / Farsi / both)

DESIGN PRINCIPLES
□ At least 4 principles, maximum 8
□ Each principle has: statement, in-practice examples, violation example
□ Voice section has adjectives + allowed + banned examples
□ Assumptions, Constraints, Non-Goals, Open Questions sections present

COLOR SYSTEM
□ Maximum 12 semantic color tokens
□ If theme = both: every token has both light and dark values
□ WCAG AA contrast rules stated
□ Accessibility section present
□ Assumptions, Constraints, Non-Goals, Open Questions sections present
□ No raw hex codes in prose — all values are in the token table

TYPOGRAPHY
□ Maximum 6 type sizes
□ Maximum 3 font weights
□ Scale steps are logical (no arbitrary intermediate values)
□ Responsive rules stated
□ Assumptions, Constraints, Non-Goals, Open Questions sections present

SPACING
□ Maximum 8 spacing scale steps
□ All values are multiples of 4px
□ Component spacing rules table present
□ Grid system section present
□ Breakpoints defined
□ Assumptions, Constraints, Non-Goals, Open Questions sections present

MOTION
□ Maximum 3 duration tokens
□ Maximum 2 easing curves
□ prefers-reduced-motion rule stated
□ Forbidden motion list present
□ Assumptions, Constraints, Non-Goals, Open Questions sections present

ACCESSIBILITY
□ WCAG 2.1 AA target stated
□ Contrast minimums stated
□ Focus state rules stated
□ Keyboard navigation table present
□ Touch target minimum stated (44×44px)
□ ARIA expectations table present

ICONOGRAPHY
□ Icon library chosen and documented
□ Icon size scale present (max 5 sizes)
□ Color rules documented
□ RTL flip rules documented if RTL is supported

OUTPUT
□ All files in English
□ All files saved to .nitro/steering/ui_foundations/
□ No [TBD], ???, [FILL ME IN] left in any file
□ Version number and date present in every file header
□ Existing files versioned (not deleted) if Fresh mode was chosen
```

---

## Anti-Pattern Scanner

Before saving, check for these patterns and fix any found:

| Anti-pattern | Detection | Fix |
|---|---|---|
| Raw hex in prose | Hex like `#5e6ad2` appearing outside a token table | Move to token table or reference by token name |
| Banned adjective in voice | modern / clean / intuitive / delightful / sleek / beautiful / elegant / friendly / engaging / professional / polished / refined | Ask user for non-banned substitute |
| More than one primary reference brand | Multiple brands named as "primary" | Keep one; move others to anti-references |
| Color token count > 12 | Count rows in color token table | Remove or merge tokens |
| Type size count > 6 | Count rows in type scale | Remove least-used size |
| Font weight count > 3 | Count rows in weights table | Remove least-needed weight |
| Spacing steps > 8 | Count rows in spacing table | Remove or merge the outlier |
| Missing Assumptions section | Check each file | Add section |
| Missing Open Questions section | Check each file | Add section |
| Motion longer than 300ms | Check duration values | Cap at 300ms |
| No prefers-reduced-motion rule | Check motion_principles.md | Add the CSS rule |
| Touch target less than 44px | Check component spacing | Update to 44×44px minimum |
| Focus state removed without replacement | Check any state descriptions | Add accessible focus ring |
