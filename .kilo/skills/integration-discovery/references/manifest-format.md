# Architecture Manifest — Format Reference

## Path

```
.nitro/steering/integration/discovery.md
```

(The filename is kept as `discovery.md` for backward compatibility with the
existing pipeline. Its content is the Architecture Manifest, not a flat
dependency table.)

## Purpose

The Architecture Manifest is the single source of truth between the
Discovery agent and the Resolver agent, and the only official record of the
project's discovered architecture for later phases.

The user can edit this file directly to correct a decision. Every Component
keeps its full context inside one row, so correcting a single decision —
swapping a Selected Solution, changing a Source Strategy, adding an
alternative — only ever requires editing that one row. It never requires
restructuring the file or touching other rows.

No other format exists for this file — no YAML, no duplicate data living
elsewhere.

---

## Template

Copy this template exactly. Do not add stray sections, remove columns, or
reorder rows arbitrarily.

```markdown
# Architecture Manifest

> Status: complete | incomplete
> Last Updated: {date}
> Total Components: {N} | Ready: {N} | Needs Input: {N} | Resolved: {N}

## Component Registry

| Component | Purpose | Category | Source Strategy | Selected Solution | Alternatives Considered | Status | Notes |
|-----------|---------|----------|------------------|--------------------|--------------------------|--------|-------|
| {name} | {one sentence — what role this plays in the project} | {short category label} | Internal Ecosystem / External Solution / Project Core | {chosen solution, or —} | {other options considered, or —} | ready / needs-input / resolved | {anything relevant: source of the decision, open question reference, etc.} |

## Relationship Registry

| Source Component | Target Component | Relationship Type | Notes |
|-------------------|-------------------|--------------------|-------|
| {component} | {component} | {e.g. depends-on / calls / publishes-to / reads-from / triggers} | {clarifying detail, with reference to its source if useful} |

## Constraints Registry

| Constraint | Scope | Description |
|------------|-------|--------------|
| {short label} | {which Component(s) or the whole architecture} | {what the constraint requires, and where it came from} |

## Architecture Definition

{A structured, high-level representation of the architecture — a Mermaid
diagram, an Architecture Matrix, or another Structured Flow Representation.
This must be an actual structural representation, not a substitute prose
description. Long paragraphs of text must not replace this structural view;
short clarifying notes alongside it are fine.}
```

---

## Field Definitions — Component Registry

**Component**
The capability, service, tool, piece of infrastructure, or independent part
— named by what it does for the project, not necessarily by vendor name.

**Purpose**
One sentence: why the project needs this Component.

**Category**
A short label grouping similar Components (left free-form — derive it from
how the project's own documentation or the Catalog describes it, do not
impose a fixed taxonomy).

**Source Strategy**
One of exactly three values:
- `Internal Ecosystem` — fulfilled by an asset of the organization's own internal ecosystem
- `External Solution` — fulfilled by an external/public solution
- `Project Core` — implemented as a native part of the project itself, not a separate sourced service

This value must be explicitly settled by Project Documentation or a user
answer. Catalog presence/absence must never, by itself, decide this value.

**Selected Solution**
The specific solution chosen to fulfill this Component, if decided.
If not yet decided: write `—` and set Status to `needs-input`.

**Alternatives Considered**
Other candidate solutions that were on the table (from the Catalog,
documentation, or user discussion) but not selected. Keeping this in the
same row means switching the decision later is a one-row edit: move an
alternative into Selected Solution, move the previous Selected Solution into
this column.
If none were discussed: write `—`.

**Status**
- `ready` — every required field is explicitly settled, eligible for the Resolver
- `needs-input` — one or more fields are missing, uncertain, or pending a user answer
- `resolved` — the Resolver has retrieved documentation and saved the integration file for this Component

**Notes**
Free text: anything relevant to understanding or revisiting this row later —
which document or answer the decision came from, an open question reference,
a caveat, etc.

---

## Field Definitions — Relationship Registry

**Source Component / Target Component**
Names exactly as written in the Component Registry.

**Relationship Type**
A short label describing the nature of the relationship (e.g. dependency,
call direction, data flow, trigger). Use whatever term the project
documentation uses; do not impose a fixed vocabulary.

**Notes**
Clarifying detail — and, where useful, a pointer to the document or user
answer that established this relationship.

---

## Field Definitions — Constraints Registry

**Constraint**
A short label for the constraint.

**Scope**
Which Component(s) it applies to, or the whole architecture.

**Description**
What the constraint requires, in plain language, with enough detail to act
on it later. Include where it came from if it adds clarity.

---

## Editing Rules

- Edit any row directly to correct a decision — this is the expected way to revise the Manifest
- Changing a decision (Selected Solution, Source Strategy, etc.) should never require touching rows other than the one being changed
- Change `needs-input` to `ready` only after every required field in that row is actually filled
- Do not delete Component rows — change Status to `resolved`, or add a Note, instead
- The Resolver agent updates `Status` from `ready` → `resolved` and updates the header counters
- Do not add extra columns or sections beyond the four sections defined here

---

## Example

```markdown
# Architecture Manifest

> Status: complete
> Last Updated: 2026-06-17
> Total Components: 3 | Ready: 2 | Needs Input: 1 | Resolved: 0

## Component Registry

| Component | Purpose | Category | Source Strategy | Selected Solution | Alternatives Considered | Status | Notes |
|-----------|---------|----------|------------------|--------------------|--------------------------|--------|-------|
| One-Time Password Delivery | Verifies user phone numbers during signup | Identity | Internal Ecosystem | Org OTP Platform | Catalog also lists Org SMS Gateway (rejected — user confirmed OTP Platform per PRD §2) | ready | Confirmed by user answer 2026-06-15 |
| File Storage | Stores user-uploaded documents | Storage | External Solution | — | Catalog lists Org Object Store; user has not yet confirmed whether this project may use it or needs an external alternative | needs-input | Awaiting user decision |
| Request Validation | Validates incoming API payloads | Project Core | Project Core | — | — | ready | Implemented in-project per SDD §4, not a separate service |

## Relationship Registry

| Source Component | Target Component | Relationship Type | Notes |
|-------------------|-------------------|--------------------|-------|
| Request Validation | One-Time Password Delivery | depends-on | Validation runs before OTP requests are issued, per SDD §4 |

## Constraints Registry

| Constraint | Scope | Description |
|------------|-------|--------------|
| Data residency | File Storage | Project documentation requires uploaded files remain within the organization's approved hosting regions |

## Architecture Definition

\`\`\`mermaid
flowchart LR
  User --> RequestValidation --> OTPDelivery
  User --> FileStorage
\`\`\`
```
