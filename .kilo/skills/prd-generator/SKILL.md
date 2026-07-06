---
name: prd-generator
description: >
  The authoritative template and writing rules for generating a PRD
  (Product Requirements Document). This skill is consumed by the PRD Generator
  agent. It contains the PRD template, section-by-section writing rules, and
  the canonical question categories. Flow control, state, and scope guardrails
  live in the agent file — not here.
---

# PRD Generator Skill

> **Separation of concerns:**
> - **Agent file** = flow, state machine, boundaries, exit conditions.
> - **This skill** = template, writing rules, question taxonomy.
>
> If you are reading this as an agent, you must have already read your agent file.
> Do not re-implement flow logic here — follow only the *content* rules below.

---

## Core Principle

**A PRD answers What and Why — never How.**

Implementation details (tech stack, infra, latency targets, DB choice, model names) belong in the SDD. If a piece of information is about *how* something is built, note that it belongs in the SDD instead of writing it in the PRD.

---

## Question Taxonomy

Use these categories when forming question batches. The agent file controls *when* and *how many* — this table only defines *what kinds*.

| Category | Topic | Example questions |
|----------|-------|------------------|
| A | Problem & User | What is the core problem? Who is the target user? |
| B | Goals & KPIs | What is the 3-month goal? How do we measure success? |
| C | Scope | What is definitely in/out of scope? What is the MVP? |
| D | Constraints | Are there regulatory, compliance, or accessibility constraints? |
| E | Timeline | What is the target release date? Any milestones? |

### The 5 Core Questions (gate to PRD generation)

1. What is the core problem?
2. Who is the target user?
3. What is the MVP?
4. What is out of scope?
5. What is the target release date?

> The agent must not proceed to writing until all 5 are answered (either from BRD or from the user).

---

## Output Location

```
.nitro/steering/prd/[feature-name]-prd.md
```

`[feature-name]` is the product title in kebab-case (lowercase, hyphens, no special characters).

---

## Section-by-Section Writing Rules

### General rules
- Every section must be present. **Missing info → `⚠️ Needs more information`. Never blank. Never fabricated.**
- Keep language outcome-focused, not implementation-focused.
- Tables with no rows yet → keep the header row and add one empty row with `⚠️ Needs more information`.

### Section-specific rules

| Section | Rule |
|---------|------|
| 1. Metadata | Fill what's known. Unknown dates → `⚠️ Needs more information`. |
| 2. Executive Summary | 1–3 paragraphs. Always include an Elevator Pitch (one sentence). |
| 3. Problem Statement | All 4 sub-points required: core problem, user pain, why now, current solutions. |
| 4. Goals & KPIs | KPIs must be **business outcomes** (activation, retention, completion). Never latency or uptime. |
| 5. User Personas | At least one persona. If unknown → one placeholder marked `⚠️ Needs more information`. |
| 6. Scenarios & User Journey | At least one scenario in arrow notation: `Step 1 → Step 2 → Step 3`. |
| 7. Functional Requirements | Group by module. Each module needs capabilities + acceptance criteria + edge cases. |
| 8. Out of Scope | List explicitly. Never leave empty — at minimum, copy items the user excluded. |
| 9. AI Capability Requirements | **Only if AI product.** User-facing capabilities only. No model names, no token limits. |
| 10. UX / UI Requirements | Reference wireframes if provided; otherwise `⚠️ Needs more information`. |
| 11. Constraints & NFRs | Product-level only (compliance, accessibility, platforms). No latency numbers. |
| 12. Risks & Mitigations | At least one row. Use Likelihood × Impact framing. |
| 13. Dependencies | External services, internal teams, APIs. |
| 14. Timeline | Phase 1 (MVP) is mandatory. Phases 2/3 optional. |
| 15. RACI | **Always include this table**, even partially filled. |
| 16. Open Questions | List unresolved items honestly. |
| 17. Appendix | Link BRD, design files, related docs. |

---

## PRD Standard Template

Copy this template verbatim into the output file, then fill it.

```markdown
# Product Requirements Document

## 1. Document Metadata

| Field | Value |
|-------|-------|
| Product / Feature Title | |
| Document Version | 1.0 |
| Status | Draft |
| Product Owner | |
| Author | |
| Teams Involved | |
| Stakeholders | |
| Created Date | |
| Last Updated | |
| Target Release | |
| Related Links | |

---

## 2. Executive Summary

[1–3 paragraph description]

**Elevator Pitch:** [one sentence]

**Core Value:**
- For users: ...
- For the business: ...

---

## 3. Problem Statement

**Core problem:** ...

**User pain:** ...

**Why now:** ...

**Current solutions and their shortcomings:** ...

---

## 4. Goals & Success Metrics

### Goals
- Goal 1: ...
- Goal 2: ...

### KPIs

| KPI | Current | Target | Timeframe |
|-----|---------|--------|-----------|
| | | | |

> KPIs must be business-level outcomes (e.g. activation rate, task completion, retention).
> Performance/infra metrics (latency, uptime SLA) belong in the SDD.

### AI Product Outcomes (if applicable)

| Outcome | Definition | Target |
|---------|-----------|--------|
| Response accuracy | % of responses rated correct by users | |
| Unhelpful response rate | % of responses user retries or dismisses | |
| Task completion rate | % of AI-assisted tasks completed successfully | |
| User satisfaction (CSAT) | Post-session rating | |

> Do not specify model names, latency budgets, or infra here — those belong in the SDD.

---

## 5. User Personas

### Persona 1: [Name]
- **Needs:** ...
- **Pain points:** ...
- **Behavior:** ...

### Persona 2: [Name]
- **Needs:** ...
- **Pain points:** ...
- **Behavior:** ...

---

## 6. Scenarios & User Journey

**Scenario 1:** [Title]
`Step 1 → Step 2 → Step 3`

**Scenario 2:** [Title]
`Step 1 → Step 2 → Step 3`

---

## 7. Functional Requirements

### Module 1: [Name]
- [ ] Capability 1
- [ ] Capability 2

**Acceptance Criteria:**
- ...

**Edge Cases:**
- ...

---

## 8. Out of Scope
- Item 1
- Item 2

---

## 9. AI Capability Requirements (if applicable)

| Capability | User-facing requirement |
|------------|------------------------|
| Language understanding | Must handle informal language and typos |
| Response quality | Must cite sources when making factual claims |
| Fallback behavior | Must gracefully handle out-of-scope queries |
| Transparency | User must know when they are interacting with AI |
| Data privacy | Must not retain personal data between sessions |

> Model selection, RAG pipeline, vector DB, token limits → SDD.

---

## 10. UX / UI Requirements
- **User Flow:** ...
- **Wireframe Links:** ...
- **Loading / Empty States:** ...
- **Error States:** ...
- **AI Transparency:** (e.g. "AI is thinking..." indicator)

---

## 11. Constraints & Non-Functional Requirements

| Constraint | Requirement |
|------------|-------------|
| Compliance / Legal | |
| Accessibility | |
| Supported platforms | |
| Supported languages | |
| Data residency | |
| Security posture | |

> Specific latency numbers, scalability targets, and availability SLAs → SDD.

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| | | | |

---

## 13. Dependencies
- External services: ...
- Internal teams: ...
- APIs / integrations: ...

---

## 14. Timeline / Milestones

| Phase | Scope | Target Date |
|-------|-------|-------------|
| Phase 1 (MVP) | | |
| Phase 2 | | |
| Phase 3 | | |

---

## 15. Stakeholders & RACI

| Task | Product | Engineering | Design | Marketing |
|------|---------|------------|--------|-----------|
| | | | | |

---

## 16. Open Questions
- Question 1
- Question 2

---

## 17. Appendix
- Market research: ...
- Design files: ...
- Related documents (BRD, SDD): ...
- Glossary: ...
```

---

## Content Rules Recap

1. **PRD = What & Why. Never How.**
2. **Use `⚠️ Needs more information`** for any gap — never blank, never invented.
3. **AI sections (4 AI Outcomes, 9 AI Capabilities)** describe user-facing behavior only.
4. **Always include the RACI table** (Section 15), even partially filled.
5. **KPIs are business outcomes.** Latency, uptime, model accuracy → SDD.
6. **Question batches** follow the taxonomy table; the agent file controls batch size and timing.