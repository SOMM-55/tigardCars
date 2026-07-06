---
name: nitro-steering-sdd
description: Generate the System Design Document (SDD) and specialized steering files from PRD, BRD, user flows, information architecture, and wireframes. Use when building or updating architecture documents, API contracts, data models, component standards, testing strategies, and deployment guides. Always reads source reference directories and existing steering before writing.
---

# Nitro SDD & Specialized Steering Skill

Transform business requirements and UX artifacts into a complete, traceable System Design Document and a set of specialized steering files.

---

## Step 0: Read Before Writing (Mandatory)

**Before generating any output**, the agent MUST read all available source documents:

```
.nitro/steering/prd/*          ← Functional requirements, business rules, NFRs
.nitro/steering/brd/*          ← Business objectives, compliance, SLAs
.nitro/steering/user_flow_map/* ← Actor flows, sequences, error paths
.nitro/steering/IA/*           ← Entity hierarchy, resource structure, domain model
.nitro/steering/layout/*       ← Wireframes, screen states, UI interaction points
.nitro/steering/*.md           ← Existing steering (never overwrite valid context)
```

### Dependency Priority

When information conflicts, respect this order:
```
Vision / BRD   →  "why" and constraints
PRD            →  "what" (features, rules, NFRs)
User Flow Map  →  "sequence" (actors, transitions, error paths)
IA             →  "structure" (entities, hierarchy, routes)
Layout         →  "interaction" (screen states, fields, timing)
SDD            →  "how" (architecture, APIs, data model, infra)
```

---

## Clarification Protocol

The agent MUST STOP and ask the user when:

| Situation | Example Question |
|---|---|
| A source directory is missing or empty | "I found no files in `.nitro/steering/layout/`. Could you share wireframes or a description of the key screens so I can design the API contracts and state handling accurately?" |
| An API or external service is referenced but undocumented | "The PRD mentions a payment gateway but I don't have its API documentation. Please share the API docs or a spec so I can design the integration correctly." |
| Business rules are ambiguous | "The PRD says users can 'manage their team' but doesn't specify the permission model. Can you clarify who can add/remove members and what roles exist?" |
| Conflicting information between BRD and PRD | "The BRD mentions EU-only data residency but the PRD describes a global CDN. Which takes precedence for the architecture?" |
| NFRs are not defined | "I don't see performance targets in the PRD. What are the expected concurrent users and acceptable response times? These affect caching and infra choices." |

**Rule:** One focused question per gap. Never stack 5 questions at once. Never assume and fill in blanks silently.

---

## Traceability Table

Before writing any section of the SDD, build this mapping table from source documents:

| PRD Feature ID | User Story | Screen (from Layout) | User Interaction | API Endpoint | DB Entity | Business Rule | UI States |
|---|---|---|---|---|---|---|---|
| F-101 | Register account | SCR-02 | Submit form | `POST /api/auth/register` | `users` | Password ≥ 8 chars | Loading, Error (duplicate email), Success |
| F-102 | … | … | … | … | … | … | … |

This table is the backbone of the SDD. Every API, every DB field, every state must trace back to a row here.

**Ask the user** if a feature in the PRD has no corresponding screen in the layout, or vice versa — do not bridge the gap silently.

---

## SDD Sections

### 1. Introduction
- System purpose (from BRD/PRD)
- Scope and boundaries
- Related documents (list all source files with versions)
- Glossary

### 2. System Architecture (High-Level)

**Context Diagram** — the system and all external actors/services.
Sources: PRD actors, BRD integrations.

**Component Diagram** — internal modules and their responsibilities.
Derived from: PRD feature list, IA entity groups.

```
Example (derive from actual documents, do not copy):
[Auth Service] → [User Service] → [PostgreSQL]
[API Gateway]  → [Queue]        → [Notification Service]
```

**Technology choices** must reference tech.md. If tech.md is missing, generate it first using the `nitro-steering-foundational` skill.

### 3. Data Model (ERD)

For each entity, extract:
- **From PRD:** business rules, required fields, validation constraints
- **From Layout:** form fields visible to users (every input field = a column)
- **From IA:** relationships and hierarchy between entities
- **From User Flows:** state fields (e.g., `status`, `is_active`, `confirmed_at`)

Rules:
- Every input field in a wireframe form must have a corresponding DB column.
- Every state transition in a user flow must have a corresponding status field.
- Ask the user if a relationship is implied but not explicitly defined.

### 4. API Design

**Rule — Click = Call:** Every user interaction that changes data maps to one API call.

For each endpoint, document:

```
Method:    POST
Path:      /api/v1/[resource]
Auth:      Bearer JWT / Public
Request:   { field: type, ... }
Response:  { field: type, ... }
Errors:    { 400: ..., 401: ..., 404: ..., 422: ... }
Source:    [PRD Feature ID] + [Screen ID from Layout]
```

**If an external API is needed** (payment, email, maps, etc.) and no documentation is provided:
> "I need the API documentation for [service] to design the integration layer. Please share the API spec or docs."

### 5. Sequence Diagrams

Generate only for flows that involve:
- Multiple services
- Async operations (queues, webhooks, background jobs)
- Multi-step user journeys (checkout, onboarding, OAuth)
- Error recovery paths

Source: `.nitro/steering/user_flow_map/*`

### 6. State Machines

For every entity that has a lifecycle (e.g., Order, Subscription, Task), document:

```
States:      [list of valid states]
Transitions: [from_state] → [to_state] : [trigger] [guard]
```

Source: User flow maps and PRD business rules.

### 7. Non-Functional Requirements

| NFR | Requirement | Source | Implementation Approach |
|---|---|---|---|
| Performance | p95 < 200ms | PRD | Redis cache, DB indexes |
| Scalability | 10k concurrent users | BRD | Horizontal scaling, queue |
| Security | OWASP Top 10 | BRD | JWT, input validation, rate limiting |
| Data Residency | EU only | BRD | Region-locked infra |

**If NFRs are missing from source documents, ask the user.** Do not invent targets.

### 8. Security Design
- Authentication mechanism (JWT, OAuth2, session)
- Authorization model (RBAC, ABAC)
- Data encryption (at rest, in transit)
- Input validation strategy
- Rate limiting
- Secrets management

### 9. Error Handling & Logging
- Error response format (e.g., RFC 7807 Problem Details)
- Log levels and what gets logged
- Alerting thresholds
- Retry strategies for async operations

### 10. Deployment & Infrastructure
- Environment breakdown (dev, staging, prod)
- Container strategy
- CI/CD pipeline
- Rollback procedure
- Monitoring and observability stack

---

## Specialized Steering Files

After generating the SDD, produce the following additional steering files:

### project-standards.md (inclusion: always)

```markdown
---
inclusion: always
---
# Project Standards

## Code Quality
[Derived from BRD constraints and team conventions]

## Testing Requirements
[Derived from PRD acceptance criteria and NFRs]

## Security Practices
[Derived from BRD security requirements]

## Performance Guidelines
[Derived from NFRs]
```

### api-design.md (inclusion: auto)

```markdown
---
inclusion: auto
name: api-design
description: REST API design patterns, endpoint conventions, error formats, and authentication. Use when creating or modifying API endpoints, routes, or handlers.
---
# API Design Guidelines
[Derived from SDD API section and PRD]
```

### testing-standards.md (inclusion: fileMatch)

```markdown
---
inclusion: fileMatch
fileMatchPattern: ["**/*.test.*", "**/*.spec.*", "**/tests/**"]
---
# Testing Standards
[Derived from PRD acceptance criteria and NFR coverage targets]
```

### deployment.md (inclusion: manual)

```markdown
---
inclusion: manual
---
# Deployment Procedures
[Derived from BRD infrastructure constraints and SDD deployment section]
```

---

## SDD Completeness Checklist

Before finalizing, verify every item:

- [ ] Every Actor in the PRD has a defined role and access level in the SDD
- [ ] Every Feature ID in the PRD has at least one API endpoint
- [ ] Every screen in the Layout has identified API calls
- [ ] Every input field in wireforms maps to a DB column
- [ ] Every state transition in user flows maps to a status field
- [ ] All Loading / Error / Empty / Success UI states are handled in API responses
- [ ] All alternative flows (error, timeout, unauthorized) are covered in sequence diagrams
- [ ] NFRs have concrete implementation strategies (not just listed)
- [ ] All external API dependencies have documented integration contracts
- [ ] No placeholder values (TBD, ???, etc.) remain in the output
- [ ] All values trace back to a source document, not invented

---

## Golden Rules

1. **Click = Call** — every data-changing user interaction has an API endpoint in the SDD.
2. **States** — every UI state in the layout has a technical handling strategy in the API or frontend.
3. **Fields** — every form field and display value in wireframes has a source in the API response and DB schema.
4. **Full Flows** — every flow from A to D in the user flow map has complete technical coverage end-to-end.
5. **Back to PRD** — when ambiguous, business logic comes from the PRD, not the layout.
6. **Ask, don't assume** — missing documentation = ask the user, not guess.