# Batch Strategy — Context Management

## Why Batching Exists

Each MCP call returns a variable amount of content. A single Internal
Ecosystem service with a full Swagger spec can consume as much context as 5
simple External Solution libraries. Processing too many Components in one
session degrades output quality — the model loses precision on later items
as context fills up.

Batching keeps each session focused, predictable, and high-quality.

## Default Batch Size

**5 Components per session** is the default.

This is conservative and works well even on smaller or weaker models. It
ensures the model has sufficient context for:
- Reading the Architecture Manifest
- Processing each Component carefully
- Normalizing documentation into structured Integration Knowledge
- Saving files accurately
- Updating the Manifest correctly

## Batch Size Adjustments

### High Context Components count as 3
A Component marked `High Context: true` (in its Notes) requires
significantly more MCP calls and content. Count it as 3 toward the batch
limit.

Example with default batch of 5:
- 1 High Context Component = 3 slots used → 2 normal slots remaining
- 2 High Context Components = 6 slots = exceeds batch → process only 1 High Context Component per session

### Project Core Components are cheap
A Component with Source Strategy `Project Core` requires no MCP call —
it is generated directly from the Manifest's existing content. Count it as
a normal (1-slot) item, not a High Context item, unless its Notes say
otherwise.

### User override
If the user says "process 3 this session" or "just do 1", respect that
number. If the user says "do all of them", explain the batch limit and why
it exists, then ask for confirmation before proceeding with more than 5.

### Model quality signal
If at any point during the session the agent's responses become shorter,
less specific, or start to repeat content incorrectly — stop the batch
early, save progress, and report. This is a signal that context is near
capacity.

## Session Start Checklist

Before beginning each batch, the agent must know:
1. How many Components remain (from the Architecture Manifest)
2. Which are `ready` vs `needs-input` vs `high-context`
3. The batch size for this session
4. The order to process them (see Processing Order below)

## Processing Order

Process in this priority order within each batch:

1. `ready` + `High Context: false` + `Internal Ecosystem` (Memoria — often more specific)
2. `ready` + `High Context: false` + `External Solution` (Context7 — usually well-documented)
3. `ready` + `Project Core` (no MCP call needed — cheap to process)
4. `ready` + `High Context: true` (only if it fits in remaining batch slots)
5. `needs-input` (only after asking the user to resolve it via the `question` tool)

Never start a `needs-input` item without first asking the user.
Never start a `high-context` item without confirming with the user.

## Between Sessions

The agent does not need to know what happened in previous sessions. The
Architecture Manifest is the single source of truth.

When starting a new session:
1. Read the Architecture Manifest
2. Count `resolved` vs `ready` vs `needs-input`
3. Pick the next batch from `ready` items
4. Report status to the user
5. Begin

No other context from previous sessions is needed.
