---
name: nitro-steering-foundational
description: Create or update the three foundational steering files for any project — product.md, tech.md, and structure.md. These files give the AI agent persistent knowledge about product goals, technology stack, and codebase structure. Use when starting a new project, onboarding a codebase, or refreshing core context. Always reads existing steering files and reference directories before writing.
---

# Nitro Foundational Steering Skill

Generate or update the three core steering files that form the persistent baseline of the agent's understanding of the project.

## Output Location

```
.nitro/steering/sdd/
├── product.md     ← What you're building and why
├── tech.md        ← How you're building it
└── structure.md   ← How your codebase is organized
```

All three use `inclusion: always` — loaded in every agent interaction automatically.

---

## Step 0: Read Before Writing

**MANDATORY** — Before creating or updating any steering file, the agent MUST read:

1. All existing steering files:
   ```
   .nitro/steering/*.md
   .nitro/steering/**/*.md
   ```

2. All reference source documents (if they exist):
   ```
   .nitro/steering/prd/*
   .nitro/steering/brd/*
   .nitro/steering/user_flow_map/*
   .nitro/steering/IA/*
   .nitro/steering/layout/*
   ```

3. Any previously generated steering files to avoid overwriting valid context.

**NEVER** guess or hallucinate values. If required information is missing from source files, stop and ask the user before proceeding (see Clarification Protocol below).

---

## Clarification Protocol

The agent MUST ask the user when:

- A source directory is empty or missing (e.g., no PRD files found)
- A required field cannot be inferred from available documents
- Conflicting information exists between BRD, PRD, and UX files
- Technology stack is ambiguous or not mentioned
- Directory structure cannot be determined from existing files

**How to ask:** Use a focused, single question per gap. Do not guess and fill in placeholders — stop, surface the blocker, and wait for user input.

Example:
> "I couldn't find any files in `.nitro/steering/prd/`. To fill in the product goals and feature list accurately, could you share the PRD or a summary of what this product does?"

---

## product.md

Defines product purpose, target users, key features, and business objectives.

### Template

```markdown
---
inclusion: always
---

# Product Overview

## What We're Building
[One paragraph — core value proposition derived from PRD/BRD]

## Target Users
- **Primary:** [Main user type and key characteristics]
- **Secondary:** [Other user types if applicable]

## Core Features
1. [Feature 1] — [Why it matters]
2. [Feature 2] — [Why it matters]
3. [Feature 3] — [Why it matters]

## Business Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Out of Scope
- [Explicitly excluded features]

## Success Metrics
- [Metric 1]
- [Metric 2]
```

### Sources (in priority order)
| Field | Read From |
|---|---|
| Value proposition | `.nitro/steering/prd/*`, `.nitro/steering/brd/*` |
| User types / roles | `.nitro/steering/prd/*`, `.nitro/steering/user_flow_map/*` |
| Feature list | `.nitro/steering/prd/*` |
| Business rules | `.nitro/steering/brd/*` |
| Success metrics | `.nitro/steering/prd/*`, `.nitro/steering/brd/*` |

---

## tech.md

Documents frameworks, libraries, tools, and technical constraints.

### Template

```markdown
---
inclusion: always
---

# Technology Stack

## Languages
- **Primary:** [Language + version]

## Frontend
- **Framework:** [e.g., Next.js 14, React 18]
- **Styling:** [e.g., Tailwind CSS]
- **State Management:** [e.g., Zustand]
- **Testing:** [e.g., Vitest + Playwright]

## Backend
- **Runtime/Framework:** [e.g., Node.js 20 + Express]
- **Database:** [e.g., PostgreSQL 15 via Prisma]
- **Cache:** [e.g., Redis 7]
- **Testing:** [e.g., Jest, pytest]

## Infrastructure
- **Cloud:** [e.g., AWS, GCP]
- **Containers:** [e.g., Docker + Kubernetes]
- **CI/CD:** [e.g., GitHub Actions]

## Key Libraries
- [library] — [what it's used for]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Conventions
- [Convention 1]
- [Convention 2]
```

### Sources (in priority order)
| Field | Read From |
|---|---|
| Tech stack | `.nitro/steering/prd/*`, `.nitro/steering/brd/*`, existing project files |
| API constraints | `.nitro/steering/prd/*` |
| Infrastructure | `.nitro/steering/brd/*` |
| Conventions | Existing `.nitro/steering/*.md` |

---

## structure.md

Outlines file organization, naming conventions, import patterns, and architectural decisions.

### Template

```markdown
---
inclusion: always
---

# Project Structure

## Directory Layout
```
[Paste actual or planned directory tree here]
```

## Key Directories
- `[dir]/` — [what lives here and why]

## Naming Conventions
- **Files:** [e.g., kebab-case: `user-profile.ts`]
- **Components:** [e.g., PascalCase: `UserProfile.tsx`]
- **Functions:** [e.g., camelCase: `getUserProfile()`]
- **Constants:** [e.g., SCREAMING_SNAKE_CASE]

## Import Patterns
- [Pattern 1]
- [Pattern 2]

## Architectural Patterns
- [Pattern 1, e.g., Repository pattern for DB access]
- [Pattern 2, e.g., Services hold business logic]

## What Goes Where
- New API endpoints → `[path]`
- New components → `[path]`
- Shared utilities → `[path]`
- Type definitions → `[path]`
```

### Sources (in priority order)
| Field | Read From |
|---|---|
| Directory layout | `.nitro/steering/IA/*`, `.nitro/steering/layout/*` |
| Component patterns | `.nitro/steering/layout/*`, `.nitro/steering/user_flow_map/*` |
| Naming/import conventions | Existing `.nitro/steering/*.md`, existing project files |

---

## Process

### 1. Read All Source Documents
Scan every file in `.nitro/steering/prd/`, `.nitro/steering/brd/`, `.nitro/steering/user_flow_map/`, `.nitro/steering/IA/`, `.nitro/steering/layout/`, and existing `.nitro/steering/*.md`.

### 2. Identify Gaps
For each field in each template, determine if the source documents provide enough information. List any missing data before writing.

### 3. Ask Before Assuming
If any required field has no source, ask the user. Never use placeholder text like "[TBD]" in a finished steering file.

### 4. Generate All Three Files
Write all three files to `.nitro/steering/`. Each file must start with the appropriate front-matter.

### 5. Validate Coverage
- [ ] product.md explains the "why" behind the product
- [ ] tech.md lists all major dependencies and constraints
- [ ] structure.md covers naming conventions and file organization
- [ ] All three files are specific to this project, not generic
- [ ] No sensitive data (API keys, passwords) in any file
- [ ] All values are derived from source documents, not invented

### 6. Keep Updated
Update steering files when:
- Tech stack changes (new library, dropped dependency)
- Directory structure is reorganized
- Product scope changes
- New architectural patterns are adopted

---

## Relationship to Other Steering

```
.nitro/steering/sdd/
├── product.md             ← always (foundational)
├── tech.md                ← always (foundational)
├── structure.md           ← always (foundational)
├── project-standards.md   ← always (from sdd-steering skill)
├── api-design.md          ← auto
├── testing-standards.md   ← fileMatch: **/*.test.*
└── deployment.md          ← manual
```