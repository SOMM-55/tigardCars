# Output Templates — IA Builder

Exact format for every IA output file the agent must produce.

---

## File: `00_ia_overview.md`

```markdown
# IA Overview — [Project Name]

> Created: [date]
> Source: User Flow Map
> Version: 1.0

---

## IA Principles

- [ ] Mobile-first / Desktop-first
- [ ] Single language / Multilingual
- [ ] Role-based architecture
- [ ] Max depth: [number] levels
- [ ] Primary language: [language]

---

## System Roles

| Role | Description | Access Level |
|------|-------------|--------------|
| [Role] | [description] | [level] |

---

## Key Architectural Decisions

### Why [decision X]?
[explanation]

### Known Constraints
- [constraint]

---

## Glossary

| Term | Definition |
|------|------------|
| [Term] | [what it means in this system] |
```

---

## File: `01_sitemap.md`

```markdown
# Sitemap — [Project Name]

---

## Overall Structure

\`\`\`
Platform
├── Public Zone (unauthenticated)
│    ├── Home                        [P-01]
│    ├── Login                       [P-02]
│    ├── Register                    [P-03]
│    └── ...
│
├── [Role 1] Zone
│    ├── Dashboard                   [R1-01]
│    ├── [Section]                   [R1-02]
│    │    ├── [Sub-page]             [R1-02-01]
│    │    └── [Sub-page]             [R1-02-02]
│    └── Settings                    [R1-99]
│
└── [Role 2] Zone
     ├── Dashboard                   [R2-01]
     └── ...
\`\`\`

---

## Page Reference

### Public Zone

| ID | Page | Description | Entry Points |
|----|------|-------------|--------------|
| P-01 | Home | Public landing page | Direct, SEO, Ads |

### [Role 1] Zone

| ID | Page | Description | Parent | Level |
|----|------|-------------|--------|-------|
| R1-01 | Dashboard | Main overview | Root | 1 |
| R1-02 | [Section] | ... | Root | 1 |
| R1-02-01 | [Sub-page] | ... | R1-02 | 2 |
```

---

## File: `02_roles_and_access.md`

```markdown
# Roles & Access — [Project Name]

---

## Role Definitions

### Role: [Role Name]

**Description:** [who holds this role]
**Primary Goal:** [what this role mainly does in the system]
**Entry Point:** [where they land after login]

**IA for this role:**
\`\`\`
[Role Name] Area
├── [Section 1]
│    ├── [Sub-page]
│    └── [Sub-page]
└── [Section 2]
\`\`\`

**Primary Actions:**
- [most important action]
- [second most important action]

**Cannot access:**
- [what this role cannot see or do]

---

## Permission Boundaries

| Feature | [Role 1] | [Role 2] | [Role 3] |
|---------|----------|----------|----------|
| [Feature] | ✅ Full | ⚠️ Limited | ❌ None |
```

---

## File: `03_entity_map.md`

```markdown
# Entity Map — [Project Name]

---

## Core Entities

| Entity | Description | Owner | Visibility |
|--------|-------------|-------|------------|
| [Entity] | [description] | [role] | [who can see it] |

---

## Entity Relationships

\`\`\`
[Parent Entity]
├── has many → [Child Entity]
│              ├── has many → [Grandchild Entity]
│              └── has one  → [Entity]
└── belongs to → [Entity]
\`\`\`

---

## Ownership Model

| Entity | Created by | Managed by | Visible to |
|--------|-----------|-----------|------------|
| [Entity] | [role] | [role] | [roles] |

---

## Cross-reference Rules

- [Entity A] can appear in [Section X] as a reference, but its primary home is [Section Y]
- [Any special relationship notes]
```

---

## File: `04_navigation_model.md`

```markdown
# Navigation Model — [Project Name]

---

## Navigation Types

### Global Navigation (Top Nav)
- Position: top of every page, always visible
- Items: [list — max 7]
- Mobile behavior: [Hamburger / Bottom Tab Bar / ...]

### Side Navigation
- Position: [left / right]
- Visibility: [always / inside authenticated sections only]
- Per-role items: [description]

### Contextual Navigation
- [Related links that appear within page content]

### Breadcrumbs
- Shown from: Level [number] and deeper
- Format: Home > Section > Page

### Footer Navigation
- [Fixed utility links: About, Contact, Privacy, ...]

---

## Navigation per Role

### [Role 1]
- Primary Nav items: [list]
- Secondary items: [list]
- Hidden from this role: [list]

### [Role 2]
- Primary Nav items: [list]
- Secondary items: [list]
- Hidden from this role: [list]

---

## Primary Navigation Flows

\`\`\`
[Page] → [Page] → [Page]
(Primary path: [description])

[Page] → [Page]
(Secondary path: [description])
\`\`\`
```

---

## File: `05_access_matrix.md`

```markdown
# Access Matrix — [Project Name]

---

## Full Feature Access Table

| Feature / Page | [Role 1] | [Role 2] | [Role 3] | [Role 4] |
|----------------|----------|----------|----------|----------|
| **Public Pages** | | | | |
| Home | ✅ | ✅ | ✅ | ✅ |
| **[Section Name]** | | | | |
| [Feature] | ✅ Full | ⚠️ Own only | ❌ | ✅ Full |
| [Feature] | 👁️ Read-only | ❌ | ✅ Full | ✅ Full |

**Legend:**
- ✅ Full — complete access
- ⚠️ Limited — restricted access (see notes below)
- 👁️ Read-only — can view but not modify
- ❌ None — no access

---

## Access Restriction Notes

### ⚠️ [Feature X] — Limited for [Role]
[Explanation of what "limited" means here]

---

## Data Visibility Rules

| Data Type | [Role 1] | [Role 2] |
|-----------|----------|----------|
| [Data] | All records | Own records only |
| [Data] | Full detail | Summary only |
```

---

## General Formatting Notes

1. All files are written in **English**
2. IDs are uppercase and alphanumeric: `P-01`, `R1-02-01`
3. Every file must include the project name in its H1 header
4. IDs must be unique and consistent across all files
5. Use emoji in tables only for the access matrix (✅ ⚠️ 👁️ ❌)
6. Keep nesting in sitemap trees aligned with 4-space indentation