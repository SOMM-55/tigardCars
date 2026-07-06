---
name: integration-discovery
description: >
  Use this skill when starting the Integration phase of a Spec-Driven Development
  workflow, after the ecosystem-decision step has produced an architecture-catalog.md.
  Reads the Architecture Catalog and all project documentation, discovers the
  project's real architecture by asking the user via the `question` tool whenever
  information is not explicitly available, and saves an architecture-manifest.md
  (stored at discovery.md for backward compatibility) for the resolver agent.

  Trigger when the user says: "start integration", "run integration discovery",
  "find components", "integration phase", or when they have an architecture_catalog
  and are ready to begin integration.

  Does NOT call MCP for documentation retrieval. Does NOT generate integration
  documentation. Does NOT design or propose architecture. Produces only the
  Architecture Manifest. After this skill completes, the user runs
  integration-resolver-agent.
---

# Integration Discovery Skill

Handles Component discovery, source-strategy determination, relationship
mapping, and constraint extraction for the Integration phase.
No MCP documentation calls. No documentation generation. No architecture design.
Output: a single Architecture Manifest file, in the structure defined by
`references/manifest-format.md`.

---

## What This Skill Does

1. Loads the Architecture Catalog as an availability reference (never as a decision)
2. Reads all project documentation
3. Identifies Components actually required by the project — explicit and implied
4. Removes Catalog entries the project does not actually need
5. Detects Components the project needs that are missing from the Catalog
6. Asks the user, via the `question` tool, whenever a fact needed for the
   Manifest is not explicitly available in a permitted source
7. Discovers relationships and constraints between confirmed Components
8. Saves the Architecture Manifest using the template in `references/manifest-format.md`

## What This Skill Does NOT Do

- Call MCP servers for documentation retrieval
- Generate API documentation or per-Component integration files
- Design new architecture, propose architecture, or recommend a "best" solution
- Decide a Component's relevance or Source Strategy solely from Catalog presence/absence
- Fill any information gap with a guess, inference, or common-pattern assumption

## Key Rules

**The Catalog is an availability list, not a source of truth**
A Component existing in the Architecture Catalog never by itself means the
project uses it, and never by itself confirms a Source Strategy. A Component
missing from the Catalog never by itself means it's forbidden. Relevance and
Source Strategy must always trace back to Project Documentation or an
explicit user answer.

**No guessing, ever**
If a fact needed to fill a Manifest cell isn't explicitly available from
Project Documentation, the Catalog (for availability only), a prior user
answer, or MCP-retrieved documentation, ask the user. Never infer from
general knowledge, common architecture patterns, or personal preference.

**Conflicts go to the user**
If sources disagree, do not resolve the conflict yourself. Ask.

**Batch questions, but don't skip needed ones**
Group related questions into a single `question` call where possible, and
keep rounds to the minimum the situation honestly allows — but never drop a
genuinely necessary question just to reduce round count. An unresolved
ambiguity in the Manifest is worse than one extra round of questions.

**One source of truth, easy to revise**
The Architecture Manifest is the only output. The Resolver agent reads it
directly. Each Component's full decision context lives in its own row/entry
so that changing one decision (e.g. swapping the Selected Solution or Source
Strategy) only requires editing that one row — never restructuring the file.

## Reference Files

- `references/manifest-format.md` — the exact structure and field definitions for the Architecture Manifest (Component Registry, Relationship Registry, Constraints Registry, Architecture Definition)
- `references/component-rules.md` — what counts as a Component, the Component vs Implementation Detail rule, and how Source Strategy must be determined
- `references/questioning-rules.md` — how to batch, phrase, and format questions in Persian using the `question` tool
