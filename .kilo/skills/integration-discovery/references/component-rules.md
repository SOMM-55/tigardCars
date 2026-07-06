# Component Rules

## What Counts as a Component

A Component is any capability, service, tool, piece of infrastructure,
dependency, or independent part that plays a role in the project's
architecture.

Record a Component when the project's own documentation, or a confirmed user
answer, indicates the project needs it — regardless of whether it appears in
the Architecture Catalog.

---

## Component vs Implementation Detail Rule

Not everything mentioned in documentation is a Component. Before recording
any candidate, check whether it is a genuine architectural Component or
merely an implementation detail with no independent role.

A reasonable signal (not a substitute for checking the project's actual
documentation): does the project need to connect to, depend on, or
coordinate with something that exists or operates separately from the
project's own code, in order to fulfill this need?

- If documentation or the user's answer confirms this — record it as a Component.
- If documentation or the user's answer indicates this is fully contained
  within the project's own code with no separate counterpart — it is an
  implementation detail, not a Component (its Source Strategy, if recorded
  at all, would be `Project Core`).

When this is not explicitly clear from a permitted source, do not decide it
yourself — ask the user.

---

## Source Strategy — How It Must Be Determined

Source Strategy has exactly three allowed values: `Internal Ecosystem`,
`External Solution`, `Project Core`.

This value must come from Project Documentation, MCP-retrieved
documentation, or an explicit user answer. It must never be assigned purely
from:
- The Component's presence in the Architecture Catalog
- The Component's absence from the Architecture Catalog
- What the Component's name suggests
- What is typical or common for similar projects

### Why Catalog presence is not enough on its own

The Architecture Catalog reflects what is *available* in the ecosystem this
project was assigned to:
- If the project's ecosystem is internal, the Catalog lists the
  organization's internal assets.
- If the project's ecosystem is external, the Catalog lists external
  equivalents of those same internal assets.

Either way, the Catalog only tells you an option exists and what it's
called. It does not tell you whether *this* project actually needs that
option, and it does not by itself confirm the Source Strategy for a
Component the project does need. That confirmation must still come from
Project Documentation or the user.

### Practical handling

- If Project Documentation explicitly states or clearly implies a Source
  Strategy for a Component, use it, and note where it came from.
- If only the Catalog suggests an option, present it to the user as an
  option to confirm — phrased as a question, never recorded as a decision
  before the user confirms it.
- If nothing in your permitted sources settles it, ask.

---

## Identifying Components from Documentation

Scan Project Documentation for two kinds of signal:

**Explicitly stated** — a Component is directly named.

**Implied by a documented requirement** — the documentation describes a
need, feature, flow, or constraint that requires some Component to exist,
without naming it. Do not silently resolve this to a specific name or
Source Strategy on your own. Surface it to the user as an open item: state
what the documentation describes, and ask what fulfills it.

Never invent an implied Component's identity, name, or strategy from what
would be typical for a project like this. The fact that a need is
documented does not mean its solution is decided — only that something must
fill that role, and that decision belongs to the project's documentation or
the user.

---

## Removing Irrelevant Catalog Entries

Once Components are identified from documentation and confirmed answers,
compare against the Architecture Catalog. Any Catalog entry that nothing in
the project's actual, confirmed requirements points to should not enter the
Architecture Manifest. This filtering does not require asking the user about
every excluded entry individually — only Components that are genuinely
ambiguous need a question.

## Detecting Missing Components

A Component the project needs, based on documentation or user answers, but
which has no corresponding entry in the Architecture Catalog, must still be
recorded in the Manifest. Catalog absence is never a reason to exclude a
genuinely needed Component, and never a reason to mark its Source Strategy
as anything other than what the documentation/user actually indicates.

---

## What This Rule Set Deliberately Avoids

This reference intentionally contains no list of "well-known" services,
technologies, or vendors to auto-classify. Earlier versions of this process
used such a list to reduce questions; the current policy is stricter: every
Source Strategy and every relevance decision must trace to Project
Documentation, the Catalog (availability only), or an explicit user answer
— never to the Agent's own familiarity with a name or pattern.
