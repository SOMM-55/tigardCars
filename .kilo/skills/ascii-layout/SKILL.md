---
name: ascii-layout
description: >
  Generate ASCII wireframe layouts from User Flow Maps, Information Architecture (IA),
  PRD, and BRD files. Use this skill whenever the user wants to create, edit, or extend
  wireframe layouts for their product — especially when they mention "layout", "wireframe",
  "ASCII layout", "page structure", or when they refer to .nitro/steering/ directories.
  This skill reads existing IA, user_flow_map, PRD, and BRD files (PRD/BRD content is
  extracted per-page, not loaded in full), reads and maintains a project-wide
  agent_memory.md file for design consistency across pages and sessions, asks one
  clarifying question at a time when ambiguous, and produces structured ASCII wireframe
  files page-by-page into .nitro/steering/layout/.
  Always trigger this skill when the user mentions building layouts after an IA or user flow step., ascii-layout
---

# ASCII Layout Skill

> **Read this entire file before doing any work.**
> Every rule here is a hard constraint — not a suggestion.
> This skill is the single source of truth for how layouts are produced.
> The agent definition controls *when* you act; this skill controls *how* you act.

---

## Purpose
Convert Information Architecture (IA), User Flow Maps, and business context from PRD/BRD
files into ASCII wireframe layout files.
Each page gets its own `.md` file under `.nitro/steering/layout/`.
Output is **structure-only** — no UI, no color, no design — just spatial hierarchy and behavior.
A project-wide `agent_memory.md` file is read before every page and updated when new
design-consistency decisions emerge, so that pages stay uniform even across separate
sessions or if a different agent instance continues the work later.

---

## Phase 0 — Session Initialization (runs ONCE per session)

> **Important:** Run Phase 0 only at the very first turn of a new session.
> On any subsequent turn within the same session, **skip Phase 0 entirely** — the context is already loaded.
> The agent definition (`LIFECYCLE-01`, `LIFECYCLE-02`) enforces this.

### Step 0.1 — Read source files (once)
Read these directories fully:
```
.nitro/steering/user_flow_map/
.nitro/steering/IA/
```
Extract:
- All page/screen names
- User roles (student, instructor, admin, etc.)
- Navigation flows and parent-child relationships
- Entry/exit points per page

### Step 0.1b — Read BRD/PRD directories (once, index only)
Read these directories:
```
.nitro/steering/prd/
.nitro/steering/brd/
```

- If **both** are missing or empty → STOP and tell the user (per agent RULE-INIT-01). Do not proceed.
- If only one exists → use that one.
- Do **not** load the full content of every file into working context here. Since these files are typically large (often a single big document covering the whole product), just confirm they exist and note their paths. The actual relevant section is extracted per-page in Step 1.1b — this keeps context lean as more pages get processed.

### Step 0.1c — Check / initialize Agent Memory file (once, then every page)
Check whether `.nitro/steering/layout/agent_memory.md` exists.
- If it does **not** exist → create it now using the template in "Agent Memory File" section below.
- If it exists → read it fully now, and again before every subsequent page (see Step 1.1c). This is the project's running record of design-consistency decisions (naming, recurring patterns, structural choices) — it must inform every page, including the very first one.

### Step 0.2 — Index existing layouts (once)
List files under `.nitro/steering/layout/` if it exists.
**Do NOT read file contents** at this point — only build a list of what already exists.
You will read a specific file's content only when the user explicitly asks to edit it.

### Step 0.3 — Ask language preference (once)
Use the question tool:
> "Should the wireframe content (labels, zone names, placeholder text) be in **Farsi** or **English**?"

- If **Farsi** → set `LANG: fa`, set `DIRECTION: RTL`.
- If **English** → set `LANG: en`, set `DIRECTION: LTR`.

Store both values. Apply to **all** pages. Never ask again in this session.

File names and metadata keys stay in English regardless of the language choice.

### Step 0.4 — Confirm starting page
Present the list of pages extracted from IA and ask:
> "Which page should we start with? Or should I go in the order defined in the IA?"

---

## Phase 1 — Page-by-Page Generation

Process **ONE page at a time**. Never batch-generate.

### Step 1.1 — Pre-generation checklist (silent, internal)
Before generating each page, verify:
- [ ] Page exists in IA
- [ ] Role is identified
- [ ] Parent page is known
- [ ] Entry points are clear
- [ ] Exit points are clear
- [ ] Primary action is known
- [ ] DIRECTION is known (RTL or LTR)

If ANY item is unclear → use the question tool. **Ask only ONE question at a time.**

### Step 1.1b — Extract relevant PRD/BRD section for this page
Before generating, search the PRD/BRD file(s) for content relevant to the **current page only**:
- Its business goal(s) — why this page exists from a business perspective.
- Its functional requirement(s) — what it must let the user do.

Pull only that section into working context. Do not carry the rest of the PRD/BRD forward.

If the page cannot be matched to anything in the PRD/BRD:
> "I could not find this page in the PRD/BRD. Do you want me to continue without business-requirement context, or should we pause here?"

Wait for the user's explicit answer before proceeding.

### Step 1.1c — Read Agent Memory (every page, no exceptions)
Read `.nitro/steering/layout/agent_memory.md` now, even if it was just read for a previous page in this same session. It may have been updated since, and consistency depends on always working from the latest version.

Apply any naming conventions, structural patterns, or prior decisions found there to this page.

### Step 1.2 — Generate ASCII wireframe
Follow the layout grammar (Section: ASCII Layout Grammar) strictly.
If `DIRECTION: RTL`, apply all RTL rules from Section: RTL Layout Rules.
Apply the UX Quality Rules from the agent definition (RULE-UX-01 through RULE-UX-07).

### Step 1.3 — Save file
Path:
```
.nitro/steering/layout/{role}/{page-name}.page.md
```
Role folders: `student/`, `instructor/`, `admin/`, `shared/`.

### Step 1.3b — Update Agent Memory (only if something new emerged)
Ask internally: did this page introduce a new naming convention, a new recurring structural pattern, or a notable decision that future pages should follow?

- **No** (this page just reused existing conventions) → skip this step, do nothing to the memory file.
- **Yes** → append a short entry to `.nitro/steering/layout/agent_memory.md` (see template below) **before** moving to Step 1.4. Never overwrite or remove prior entries — only append.

### Step 1.4 — Confirm and continue
After saving, show the user the output and ask:
> "Page saved ✓ — shall I continue to **[next page name]**?"

If the user says yes → proceed to next page.
If the user says no or stops → wait for further instruction.

### Step 1.5 — Completion check
After saving each page, check: are there any unprocessed pages left in the IA?
- **Yes** → continue with Step 1.4.
- **No** → output the termination message from `LIFECYCLE-03` and stop.

---

## Phase 2 — Edit Mode

Triggered only when the user explicitly asks to edit an existing layout.

1. Read `.nitro/steering/layout/agent_memory.md` first (RULE-INIT-05 — this applies to edits too, not just new pages).
2. Read the target file under `.nitro/steering/layout/` (this is the only time existing layout files get read).
3. Show the current content to the user.
4. Confirm what changes are needed.
5. Apply changes.
6. Increment `VERSION` (e.g., `1.0` → `1.1`; major restructure → `2.0`).
7. Save.
8. If the change introduces a new convention or pattern → append to `agent_memory.md` (Step 1.3b applies here too).

Never overwrite a file without reading it first.

---

## ASCII Layout Grammar (HARD RULES)

### RULE 1 — Structure Only
✅ Allowed: zones, grouping, positioning, hierarchy, spacing
❌ Forbidden: color, animation, border-radius, font style, gradients, shadows, pixel/rem values, icon graphics

### RULE 2 — Fixed Width: 80 chars
Every layout must be exactly 80 characters wide. Include in header:
```
-- layout-width: 80 chars --
```

### RULE 3 — Consistent Symbols

| Symbol | Meaning |
|--------|---------|
| `[ Label ]` | Button / Action |
| `[__________]` | Text input |
| `( )` / `(*)` | Radio button |
| `[ ]` / `[x]` | Checkbox |
| `[ IMAGE ]` | Image placeholder |
| `[ VIDEO ]` | Video placeholder |
| `...` | Dynamic / scrollable content |
| `> Link text` | Navigation link (LTR) |
| `Link text <` | Navigation link (RTL) |
| `↓↓↓` / `↑↑↑` | Scroll boundary |
| `(1)`, `(2)`, ... | Behavior footnote reference |

### RULE 4 — Box Drawing
```
+---+    ╔═══╗
|   |    ║   ║
+---+    ╚═══╝
```
- Use `+`, `-`, `|` for standard zones.
- Use `╔ ═ ╗ ║ ╚ ╝` **only** for the single primary action zone per page.

### RULE 5 — One Responsibility Per Zone
Each bordered section does exactly one thing.

❌ Bad:
```
| Chat + Payment + Video |
```

✅ Good:
```
+------------------------+
| [ VIDEO PLAYER ]       |
+------------------------+
| Chat                   |
+------------------------+
```

### RULE 6 — Visual Weight via Space (not color)
Importance shown by **size**, **position** (top = primary always; left = primary for LTR; right = primary for RTL), **whitespace**.

### RULE 7 — State Placeholders
Every page with dynamic content must include:
```
[ Loading State ] — while data fetches
[ Empty State   ] — when no content exists
[ Error State   ] — on failure
```
If a page is fully static, write: `-- no dynamic states required --`. Never silently omit.

### RULE 8 — Primary Action Must Be Visually Dominant
Exactly **one** primary action per page, in a double-line box:
```
╔══════════════════════════════════════════════════════════════════════════╗
║                        [ Primary Action Label ]                         ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### RULE 9 — Fixed Navigation Zones
- Header → top
- Sidebar → left (LTR) | right (RTL)
- Bottom Nav (mobile) → bottom
Exception only if IA/flow explicitly demands otherwise.

### RULE 10 — Scroll Awareness
Mark all scrollable areas:
```
↓↓↓ Scrollable Content Area ↓↓↓
...
↑↑↑ End of Scroll ↑↑↑
```

### RULE 11 — No Pixel-Level Thinking
Never write CSS-like values (`16px`, `1rem`, `width: 320px`). This is a blueprint, not a mockup.

### RULE 12 — Semantic Labels Only
❌ `[ Button ]`, `[ Box ]`, `[ Area ]`, `[ Item ]`, `[ Section ]`
✅ `[ Enroll Now ]`, `[ Course Progress ]`, `[ Upload Thumbnail ]`, `[ Student Avatar ]`

### RULE 13 — No Orphan Screens
Every layout must define at least one **ENTRY** and at least one **EXIT**.
If unknown from IA → ask the user.

### RULE 14 — Spaces Only, Never Tabs
Use only space characters for alignment and indentation.

---

## RTL Layout Rules (applies when DIRECTION: RTL)

These rules **override** their LTR equivalents. All other grammar rules stay in effect.

### RTL-01 — Mirror the Horizontal Axis
The reading and visual flow is right-to-left.
- Primary content → right side of layout
- Secondary content (sidebar, nav) → left side of layout
- This is the **opposite** of LTR layouts.

### RTL-02 — Sidebar Position
Sidebar moves to the **right** of the main content area:

```
+------------------------------------------------------------------------------+
| HEADER                                                                       |
+----------------------------------------------+---------+--------------------+
|                                              |         |                    |
|   MAIN CONTENT                               | SIDEBAR |                    |
|                                              |         |                    |
+----------------------------------------------+---------+--------------------+
```

❌ Never place sidebar on the left in RTL mode.

### RTL-03 — Navigation Links
Use `<` arrow prefix instead of `>` for nav items:
```
< آیتم ناوبری ۱
< آیتم ناوبری ۲ (فعال)
< آیتم ناوبری ۳
```

### RTL-04 — Text Alignment Markers
Use alignment comments to signal RTL text blocks:
```
-- align: right --
| متن فارسی اینجا قرار می‌گیرد                                              |
-- /align --
```
Apply this wrapper to every zone that contains Farsi text.

### RTL-05 — Header Element Order
In RTL, header elements are mirrored:
```
+------------------------------------------------------------------------------+
| HEADER                                                                       |
| [ اعلان ] [ آواتار ]          [ جستجو ]                          لوگو      |
+------------------------------------------------------------------------------+
```
Left side = user actions. Right side = brand/logo.

### RTL-06 — Input Fields
Text inputs show placeholder aligned to the right:
```
[__________راهنمای ورود]
```

### RTL-07 — Breadcrumbs and Paths
Use `<` as separator instead of `>`:
```
خانه < دوره‌ها < جزئیات دوره
```

### RTL-08 — Footnote References Stay Numeric
`(1)`, `(2)` etc. are kept as-is. Numbers are LTR even in RTL documents.

### RTL-09 — DIRECTION Metadata Required
Every RTL file must include in its metadata block:
```
DIRECTION: RTL
LANG:      fa
```

### RTL-10 — No Mixed Directions Per Zone
A single zone must not mix RTL and LTR content blocks.
If a page genuinely needs both (e.g., code snippet inside a Farsi page), create a sub-zone:
```
+------------------------------------------------------------------------------+
| -- align: right --                                                           |
| توضیحات فارسی                                                               |
| -- /align --                                                                 |
|                                                                              |
|   +-- LTR Sub-zone (code) -----------------------------------------------+ |
|   |  const x = getValue();                                                | |
|   +-----------------------------------------------------------------------+ |
+------------------------------------------------------------------------------+
```

---

## File Template — LTR (English)

```
======================================================================
PAGE:      [Exact page name from IA]
FILE:      [filename.page.md]
ROLE:      [student | instructor | admin | shared]
IA NODE:   [Parent > Child path from IA]
FLOW:      [Flow name from user_flow_map]
VIEWPORT:  [Desktop First ≥1280px | Mobile First ≤375px]
DIRECTION: LTR
LANG:      en
VERSION:   1.0
======================================================================

ENTRY:
  - [Page or action that leads here]

EXIT:
  - [Page or action that leads away]

-- layout-width: 80 chars --

LAYOUT:
+------------------------------------------------------------------------------+
| HEADER                                                                       |
| Logo                              [ Search ]         [ Avatar ] [ Notif ]   |
+------------------------------------------------------------------------------+
|                          |                                                   |
|  SIDEBAR                 |   MAIN CONTENT                                   |
|  > Nav Item 1            |                                                   |
|  > Nav Item 2 (active)   |   [ Primary Content Zone ]                       |
|  > Nav Item 3            |                                                   |
|                          |   ↓↓↓ Scrollable Content Area ↓↓↓               |
|                          |   ...                                             |
|                          |   ↑↑↑ End of Scroll ↑↑↑                         |
+------------------------------------------------------------------------------+
| FOOTER                                                                       |
+------------------------------------------------------------------------------+

STATES:
  [ Loading State ] - shown while data fetches
  [ Empty State   ] - shown when no content exists
  [ Error State   ] - shown on failure

======================================================================
BEHAVIORS & INTERACTIONS
======================================================================

(1) Click [ Primary CTA ] → navigates to [target-page.page.md]
    - Conditional path A → ...
    - Conditional path B → ...
(2) Click > Nav Item → highlight active state, load content in MAIN
(3) [ Search ] → opens search overlay (see search.page.md)

RESPONSIVE NOTES:
  - Sidebar collapses below 768px into hamburger menu
  - Header actions condense into [ ≡ Menu ] on mobile

======================================================================
```

---

## File Template — RTL (Farsi)

```
======================================================================
PAGE:      [نام دقیق صفحه از IA]
FILE:      [filename.page.md]
ROLE:      [student | instructor | admin | shared]
IA NODE:   [مسیر والد > فرزند از IA]
FLOW:      [نام فلو از user_flow_map]
VIEWPORT:  [Desktop First ≥1280px | Mobile First ≤375px]
DIRECTION: RTL
LANG:      fa
VERSION:   1.0
======================================================================

ENTRY:
  - [صفحه یا اکشنی که به اینجا منتهی می‌شود]

EXIT:
  - [صفحه یا اکشنی که از اینجا خارج می‌شود]

-- layout-width: 80 chars --

LAYOUT:
+------------------------------------------------------------------------------+
| HEADER                                                                       |
| -- align: right --                                                           |
| [ اعلان ] [ آواتار ]            [ جستجو ]                          لوگو    |
| -- /align --                                                                 |
+----------------------------------------------------+-------------------------+
|                                                    |                        |
|   MAIN CONTENT                                     |  SIDEBAR               |
|   -- align: right --                               |  -- align: right --    |
|                                                    |  آیتم ۱ <             |
|   [ ناحیه محتوای اصلی ]                           |  آیتم ۲ (فعال) <      |
|                                                    |  آیتم ۳ <             |
|   ↓↓↓ ناحیه اسکرول‌پذیر ↓↓↓                      |  -- /align --          |
|   ...                                              |                        |
|   ↑↑↑ پایان اسکرول ↑↑↑                            |                        |
|   -- /align --                                     |                        |
+----------------------------------------------------+-------------------------+
| FOOTER                                                                       |
| -- align: right --                                                           |
| لینک‌های پایین صفحه                                                         |
| -- /align --                                                                 |
+------------------------------------------------------------------------------+

STATES:
  [ در حال بارگذاری ] - نمایش هنگام دریافت داده
  [ محتوایی وجود ندارد ] - نمایش هنگام خالی بودن
  [ خطا ] - نمایش هنگام شکست عملیات

======================================================================
BEHAVIORS & INTERACTIONS
======================================================================

(1) کلیک روی [ اکشن اصلی ] → انتقال به [target-page.page.md]
    - مسیر شرطی الف → ...
    - مسیر شرطی ب → ...
(2) کلیک روی آیتم ناوبری < → فعال‌سازی آیتم، بارگذاری محتوا در MAIN
(3) [ جستجو ] → باز شدن پوشش جستجو (نگاه کنید به search.page.md)

RESPONSIVE NOTES:
  - سایدبار در زیر ۷۶۸px به منوی همبرگری تبدیل می‌شود (سمت چپ صفحه)
  - اکشن‌های هدر در موبایل در [ ≡ منو ] جمع می‌شوند (سمت راست صفحه)

======================================================================
```

---

## Agent Memory File

### Purpose
`.nitro/steering/layout/agent_memory.md` is the project's running record of design-consistency decisions. Because layout generation happens one page at a time — sometimes across many separate sessions or even a different agent instance taking over mid-project if context runs out — this file is what keeps every page feeling like it came from the same hand.

It is **not** a log of every page generated. It only holds decisions and patterns that future pages need to stay consistent with.

### When to create it
If the file does not exist when you check for it (Step 0.1c) → create it immediately using the template below, before generating any page.

### When to read it
Every single page, no exceptions — both new pages (Step 1.1c) and edits (Phase 2). Read it even if you already read it earlier in the same session; it may have changed.

### When to update it
Only when a page introduces something future pages must follow:
- A new naming convention for a recurring concept (e.g., this project always calls it "Sign Out", never "Logout").
- A new recurring structural pattern (e.g., every list page gets a `[ Filter ]` zone directly under the header).
- A notable project-specific exception to a default rule (e.g., this project's bottom nav uses 4 items max, not 5).
- Any other decision that, if forgotten, would make a future page visibly inconsistent with the rest.

Do **not** update it for routine pages that simply reuse what's already documented. Most pages should not trigger an update.

When updating: **append only**. Never delete or rewrite prior entries — the memory must stay cumulative. Keep each entry to one line or a short bullet.

### Template (create with this structure if the file doesn't exist)

```markdown
# Layout Agent Memory

> Append-only. Read before every page. Update only when a new project-wide
> design decision or pattern emerges — not after every page.

## Project Conventions
- DIRECTION: [RTL | LTR]
- LANG: [fa | en]

## Naming Conventions
<!-- e.g. "Sign Out" not "Logout"; "Course" not "Class" -->

## Recurring Structural Patterns
<!-- e.g. every list page includes a [ Filter ] zone under the header -->

## Notable Decisions / Exceptions
<!-- e.g. bottom nav limited to 4 items max for this project -->

## Page Log (optional, lightweight — page name + date only, no detail)
<!-- e.g. dashboard.page.md — 2026-06-20 -->
```

### Example entry being appended
```markdown
## Naming Conventions
- Use "Sign Out" everywhere (not "Logout") — decided on shared/header.page.md

## Recurring Structural Patterns
- Every list-type page (courses, students, etc.) includes a [ Filter ] zone
  directly below the header, above the list itself — decided on
  student/course-list.page.md
```

---

## Behavior Documentation Rules

### B-01: Number Every Interaction
Every interactive element gets a footnote number:
```
[ Enroll Now ](1)       ← LTR
[ ثبت‌نام ](1)           ← RTL
```
With a matching entry in BEHAVIORS:
```
(1) Click [ Enroll Now ] → navigates to checkout.page.md
    - If user is already enrolled → shows [ Already Enrolled ] message
    - If course is free → skips checkout, goes to lesson-player.page.md
```

### B-02: Name the Target File
Every navigation target must name the exact destination file:
- ✅ `→ dashboard.page.md`
- ❌ `→ "the dashboard"`

### B-03: Document ALL Conditional Paths
Every conditional outcome (success/error, logged-in/guest, etc.) must be listed. Never document only the happy path.

### B-04: Responsive Notes Mandatory
Every file must include a `RESPONSIVE NOTES:` section.
For RTL pages, responsive notes must address:
- Which side the collapsed menu appears on (right for RTL)
- Any directional changes in mobile vs desktop layout

If no responsive differences exist, write:
```
RESPONSIVE NOTES:
  -- Layout is identical across all viewports --
```

---

## Clarification Protocol

When ambiguity exists, use the question tool. **One question per turn.** Wait for the answer, then ask the next if still needed.

Common clarifying questions:
- "Is this page accessible to guests, or only authenticated users?"
- "Does this page have a sidebar, or is it full-width?"
- "What is the single most important action on this page?"
- "Does the mobile layout differ significantly from desktop?"
- "Is there a step-by-step flow (wizard) on this page, or is it a single view?"

---

## File Management Rules

### F-01: Correct File Path
All layout files saved to:
```
.nitro/steering/layout/{role}/{page-name}.page.md
```
Role folders: `student/`, `instructor/`, `admin/`, `shared/`.
Files anywhere else are INVALID.

### F-02: Mandatory Metadata Header
All 8 metadata fields must be filled (including `DIRECTION` and `LANG`). A file with any empty metadata field is INVALID.

### F-03: Read Before Edit
When editing: (1) read agent_memory.md → (2) read current file → (3) show to user → (4) confirm changes → (5) apply → (6) save with version bump.

### F-04: Agent Memory Path
The agent memory file is always at `.nitro/steering/layout/agent_memory.md` — never elsewhere. Create it if missing (template in "Agent Memory File" section), read it before every page, and append to it only when a new project-wide pattern or decision emerges.

---

## Quality Gate (run silently before every save)

If any item fails → fix before saving.

```
[ ] Metadata block complete (all 8 fields filled, including DIRECTION and LANG)
[ ] ENTRY defined
[ ] EXIT defined (at least one)
[ ] Layout width is 80 characters
[ ] "-- layout-width: 80 chars --" header present
[ ] All zones have semantic labels
[ ] Each zone has exactly one responsibility
[ ] Primary action uses ╔═╗ double-line box
[ ] State placeholders present or explicitly marked N/A
[ ] Scrollable areas marked with ↓↓↓ / ↑↑↑
[ ] No design details (colors, fonts, radii, px values)
[ ] No Tab characters
[ ] All interactions numbered with footnotes
[ ] All navigation targets name the destination .page.md
[ ] All conditional paths documented
[ ] Responsive notes section exists
[ ] File saved to correct path under .nitro/steering/layout/
[ ] agent_memory.md was read before generating/editing this page
[ ] agent_memory.md created if it didn't already exist
[ ] Relevant PRD/BRD section was checked for this page (or user agreed to continue without it)
[ ] agent_memory.md updated ONLY if a new convention/pattern emerged (not on routine pages)
[ ] Primary action reachable without scrolling on stated viewport
[ ] Terminology consistent with agent_memory.md naming conventions
[ ] Destructive actions (if any) document a confirmation step
[ ] Empty State (if any) documents a next action

-- RTL-specific (skip if DIRECTION: LTR) --
[ ] DIRECTION: RTL and LANG: fa present in metadata
[ ] Sidebar is on the RIGHT side of main content
[ ] Header element order is mirrored (logo right, actions left)
[ ] Nav links use < prefix instead of >
[ ] Breadcrumbs use < separator
[ ] All Farsi text zones wrapped in -- align: right -- / -- /align --
[ ] No mixed RTL/LTR content in a single zone (sub-zone used if needed)
[ ] Input placeholders are right-aligned
[ ] Responsive notes address collapsed menu direction (right side)
```

---

## Forbidden Patterns (Hard Stops)

| # | Pattern | Action |
|---|---------|--------|
| 1 | Generating without IA/user_flow loaded | STOP → load source |
| 2 | Page with no ENTRY or EXIT | STOP → ask user |
| 3 | Any design detail in layout | STOP → remove it |
| 4 | Generic label like `[ Button ]` | STOP → rename |
| 5 | Multiple pages generated without confirmation | STOP → confirm first |
| 6 | Editing a file without reading it first | STOP → read file |
| 7 | Multiple questions in one turn | STOP → ask one |
| 8 | Wrong save path | STOP → correct path |
| 9 | Empty metadata field | STOP → fill it |
| 10 | Zone with multiple responsibilities | STOP → split it |
| 11 | Re-reading IA/flow files mid-session | STOP → use context |
| 12 | Re-reading existing layout files when not editing | STOP → only read on explicit edit |
| 13 | RTL page with sidebar on the left | STOP → move to right |
| 14 | RTL page with > nav arrows | STOP → replace with < |
| 15 | RTL page with logo on the left in header | STOP → mirror header |
| 16 | Farsi text zone without align marker | STOP → add -- align: right -- |
| 17 | Generating without checking PRD/BRD (when at least one exists) | STOP → extract relevant section |
| 18 | Loading the entire PRD/BRD into context instead of the relevant section only | STOP → extract only what's relevant |
| 19 | Page missing from PRD/BRD, proceeding without asking | STOP → ask the user |
| 20 | Generating/editing a page without reading agent_memory.md first | STOP → read it |
| 21 | Updating agent_memory.md after every routine page | STOP → only update on new pattern/decision |
| 22 | Overwriting or deleting prior agent_memory.md entries | STOP → append only |

---

## Termination

When all IA pages have been generated and saved, output **exactly** this and stop:

> ✅ All pages from the IA have been generated and saved under `.nitro/steering/layout/`.
> My work here is complete. You can move to the next agent.

Do not ask further questions. Do not loop.

---

## Folder Structure (reference)

```
.nitro/steering/layout/
│
├── student/
│   ├── dashboard.page.md
│   ├── course-detail.page.md
│   └── lesson-player.page.md
│
├── instructor/
│   ├── instructor-dashboard.page.md
│   └── course-editor.page.md
│
├── admin/
│   └── admin-dashboard.page.md
│
└── shared/
    ├── login.page.md
    ├── register.page.md
    └── checkout.page.md
```