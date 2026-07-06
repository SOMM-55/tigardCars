# MCP Query Strategy

## General Principles

- Use the Component's **Selected Solution** name from the Architecture Manifest as the primary search term — not the generic Component name, when the two differ
- Also check the Component's **Notes** in the Manifest — they may contain hints left by Discovery or the user
- If the first query returns nothing, try alternate terms before marking MissingDocumentation
- Prefer specific queries over generic ones
- Never query MCP for a `Project Core` Component — see the dedicated section below

---

## Memoria MCP — `Internal Ecosystem` Components

### Primary query
Use the exact Selected Solution name as written in the Manifest.

Example: Selected Solution is "Nitro OTP" → search `"Nitro OTP"`

### If primary returns nothing, try:
1. Shortened name: `"OTP"`, `"otp-service"`, `"otp@v1"`
2. Functional name based on the Component's Purpose: `"SMS OTP"`, `"one-time-password"`
3. Hints from the Component's Notes in the Manifest

### What to retrieve from Memoria
Prioritize documents that contain:
- API endpoint definitions (path, method, request, response)
- Authentication / authorization requirements
- Error codes and their meanings
- SDK or client library documentation
- Environment-specific URLs (dev, staging, prod)
- Versioning information
- Rate limits or usage constraints

Do not retrieve:
- Internal architecture documents (DB schema, infrastructure diagrams) unless they contain API info
- Team process documents
- Meeting notes or changelogs unless they contain breaking change information

### Maximum queries per Component
3 queries. If nothing is found after 3 tries → MissingDocumentation.

---

## Context7 MCP — `External Solution` Components

### Primary query
Use the canonical public name of the Selected Solution.

Examples:
- "Redis" → search `"Redis"`
- "Bull Queue" → search `"BullMQ"` or `"Bull"` (check the Manifest's Notes for version hints)
- "Express.js" → search `"Express"`
- "PostgreSQL" → search `"PostgreSQL"` or `"node-postgres"`

### If primary returns nothing, try:
1. Common abbreviations: `"pg"` for PostgreSQL, `"bullmq"` for Bull Queue
2. The npm package name if known: `"ioredis"`, `"express"`, `"pg"`
3. Alternate common names: `"Postgres"`, `"Bull"`, `"BullMQ"`

### What to retrieve from Context7
Prioritize documents that contain:
- Connection / initialization setup
- Core API methods used by this project (based on the Manifest's Notes and Relationship Registry)
- Configuration options
- Error handling
- TypeScript type definitions if available
- Integration with other Components in this project's Relationship Registry (e.g. a queue Component + the cache Component it relies on)

### Focus query based on Manifest notes
If a Component's Notes say something like "used for session storage and
rate limiting," search specifically for those use cases rather than pulling
the full general-purpose reference for that solution.

### Maximum queries per Component
3 queries. If nothing found after 3 tries → MissingDocumentation.

---

## `Project Core` Components — No MCP Call

If a Component's Source Strategy is `Project Core`, do not query Memoria or
Context7 at all. There is no external service to document. Instead:

1. Read the Component's full row in the Architecture Manifest (Purpose, Notes)
2. Read the Relationship Registry for any relationships involving this Component
3. Read the Constraints Registry for any constraints scoped to this Component
4. Generate the Integration Knowledge file directly from this information, following the `Project Core` structure in `references/file-format.md`
5. If the Manifest does not contain enough detail to fill a required section, state that explicitly in the file rather than inventing detail — do not query MCP to fill the gap, since this Component has no external source

---

## Query Log

For each Component (Internal Ecosystem or External Solution only), record
what was searched:

```
MCP Query: "Nitro OTP"
Fallback 1: "otp-service"
Fallback 2: —
Result: Retrieved (2 documents)
```

This goes into the file header as `MCP Query` and is also useful for
MissingDocumentation files.

---

## When to Stop Querying

Stop after:
- You have sufficient integration documentation (API endpoints, auth, error codes)
- You have hit 3 queries with no useful results → MissingDocumentation
- The user asks you to stop

Do not keep querying trying to find perfect documentation. Sufficient
documentation for integration purposes is enough.
