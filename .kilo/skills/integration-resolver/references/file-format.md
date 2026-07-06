# Per-Component Integration Knowledge File Format

## Path Convention

```
.nitro/steering/integration/{kebab-case-name}.md
```

Naming rules:
- Lowercase kebab-case only
- Derived from the Component name in the Architecture Manifest
- No spaces, no uppercase

Examples:
```
nitro-otp.md
redis.md
payment-gateway.md
bull-queue.md
gov-inquiry-services.md
digital-signature-service.md
request-validation.md
```

---

## Why This File Is Normalized, Not Raw

Earlier versions of this process saved MCP output verbatim. The current
policy requires normalization: every file must be Machine Readable, Human
Readable, structurally consistent with every other Component's file, free
of duplication, and usable directly for software development — a developer
or another Agent should be able to understand the Component's place in the
architecture from this file alone, without going back to raw source
documents.

This means summarizing, restructuring, and standardizing terminology is
expected and required. What is **not** allowed is inventing information that
was not present in the retrieved documentation, the Manifest, or a user
answer — if something needed is missing, the file must say so explicitly
rather than filling the gap.

---

## Standard Structure — Retrieved Documentation (Internal Ecosystem / External Solution)

```markdown
# {Component Name} — Integration Knowledge

> Source: Memoria MCP | Context7 MCP
> Retrieved: {YYYY-MM-DD}
> Source Strategy: Internal Ecosystem | External Solution
> Selected Solution: {name from the Manifest}
> MCP Query: "{exact search string used}"
> Status: Retrieved | PartialDocumentation

---

## Purpose

{What this Component does and why the project needs it — from the Manifest and retrieved documentation.}

## Responsibilities

{What this Component is responsible for within the architecture.}

## Dependencies

{What this Component itself depends on — other Components, services, or infrastructure.}

## Integration Points

{How the project connects to this Component: protocol, endpoints, SDK, events, etc.}

## Configuration Requirements

{Environment variables, credentials, setup steps, environment-specific URLs.}

## Runtime Requirements

{Versioning, runtime environment, resource expectations, rate limits.}

## Interaction Model

{Request/response shape, authentication flow, event flow, or whatever interaction pattern applies.}

## Constraints

{Any constraints from the Constraints Registry in the Manifest that apply to this Component, plus any additional constraints found in retrieved documentation.}

## Source Notes

{Brief note on what was retrieved and from where — enough to trace back to the original documentation if ever needed, without reproducing it wholesale.}
```

---

## Standard Structure — Project Core Components (No MCP Call)

```markdown
# {Component Name} — Integration Knowledge

> Source: Architecture Manifest (Project Core — no external documentation)
> Generated: {YYYY-MM-DD}
> Source Strategy: Project Core
> Status: ProjectCore

---

## Purpose

{From the Manifest's Purpose field and Notes.}

## Responsibilities

{What this Component does inside the project.}

## Dependencies

{Other Components this one depends on, per the Relationship Registry.}

## Integration Points

{How other parts of the project interact with this Component, if documented.}

## Configuration Requirements

{If any are documented; otherwise state that none were documented.}

## Runtime Requirements

{If any are documented; otherwise state that none were documented.}

## Interaction Model

{If documented; otherwise state that none was documented.}

## Constraints

{Any constraints from the Constraints Registry that apply to this Component.}

## Source Notes

This Component is implemented as a native part of the project (Project
Core) and has no external documentation source. This file was generated
directly from the Architecture Manifest.
```

---

## Missing Documentation File

When MCP returns nothing for an Internal Ecosystem or External Solution
Component, still create the file:

```markdown
# {Component Name} — Integration Knowledge

> Source: N/A
> Retrieved: {YYYY-MM-DD}
> Source Strategy: Internal Ecosystem | External Solution
> Selected Solution: {name from the Manifest}
> MCP Query: "{exact search string used}"
> Status: MissingDocumentation

---

No documentation found via MCP.

Queries attempted:
- "{query 1}"
- "{query 2}"

What is needed for integration:
- API endpoints and request/response format
- Authentication method
- SDK or client library information
- Error codes and handling
- Environment URLs (dev / staging / production)

Next steps:
- Ask the service owner for documentation
- Check if an OpenAPI spec exists
- Consider marking as Mock or Deferred until docs are available
```

---

## Partial Documentation File

When MCP returns some but not all needed content, use the standard
structure above with `Status: PartialDocumentation`, and explicitly mark
which sections are incomplete rather than silently leaving them thin:

```markdown
## Configuration Requirements

_Not found in retrieved documentation — needed before this Component can be integrated._
```

Add a closing section listing what's still missing:

```markdown
## Still Missing

- {what was not found}
- {what was not found}
```

---

## Normalization Rules

Apply these when turning retrieved documentation into the structure above:

- **Summarize**, do not transcribe — restate content in your own structure, do not mirror the source document's headings or order
- **De-duplicate** — if the same fact appears in multiple retrieved documents, state it once
- **Standardize terminology** — use one consistent term for the same concept across every Component file in this project (e.g. don't call the same thing "token" in one file and "auth key" in another, if the underlying documentation used both inconsistently — pick one and note the alternate term if useful)
- **Translate to English** as much as possible, per the project's documentation standardization rules
- **Never invent** — if retrieved documentation does not cover one of the required sections, write that explicitly (e.g. "_Not documented in retrieved sources._") rather than guessing or omitting the section

---

## Why Normalization Matters

Future phases (SDD, implementation agents, plan-orchestrator) read these
files as their working reference. If they had to work from raw,
inconsistent, duplicated source material, they would spend more effort
re-deriving structure than building on it, and could miss requirements
buried in inconsistent formatting. Normalizing here, once, correctly, means
every later phase gets a consistent, complete, honestly-gapped view of each
Component.
