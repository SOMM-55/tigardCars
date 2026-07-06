# Questioning Rules

## Tool

All questions must be asked using the `question` tool. Never ask a
classification, scope, or confirmation question as plain conversational
text — always use the tool, so the user gets a real interactive prompt.

## Language

All questions must be in Persian. Questions must be understandable to
non-technical users — avoid technical jargon where possible. Keep questions
short, clear, and direct.

## Supported Question Types

Use whichever type fits the decision being asked about:

- **Single Choice** — user picks exactly one option
- **Multiple Choice** — user can pick more than one option at once
- **Yes / No**
- **Free Text** — for anything that needs an open answer
- **Mixed** — predefined options plus a free-text option

Prefer multiple-choice / structured formats where the decision is genuinely
a choice among known options, since they are faster for the user to answer
than free text. Never force the user into a fixed list with no way out.

## Mandatory "Other" Option

Every question must include a "سایر / توضیح دلخواه" (other / free
explanation) option. The user must never be forced to pick from only the
predefined options if none of them fit.

## Batching and Grouping

- Group related questions into a single `question` call rather than asking
  one Component at a time.
- Combine questions about the same Component (e.g. relevance + Source
  Strategy + selected solution) into one question where the options make
  sense together, rather than spreading them across separate rounds.
- Keep the number of back-and-forth rounds as low as the situation honestly
  allows.

## Never Skip a Needed Question to Save a Round

Reducing rounds is a secondary goal. It must never come at the cost of
leaving a genuine ambiguity unresolved in the Manifest. If something is not
explicitly settled by a permitted source, ask — even if that means one more
round than you'd prefer. An unconfirmed assumption silently written into the
Manifest is a worse outcome than an extra question.

## Framing Catalog-Derived Options

When a question offers an option that comes from the Architecture Catalog,
frame it as something to confirm, not as a default already assumed true.

Weaker (avoid): assuming the Catalog option is correct and asking only for a
correction.

Better: presenting the Catalog option neutrally alongside other
possibilities (including "none of these" / "something else") and letting the
user's answer be the actual source of the decision.

## Conflict Questions

When Project Documentation, the Architecture Catalog, user answers so far,
or MCP-retrieved documentation disagree with each other about the same
point, do not resolve it yourself. Present the conflicting information
plainly and ask the user to decide. State what each source says, without
picking a side.

## Practical Question Design

- Design questions around information already available about the project
  — reference what was found in documentation so the user has context, not
  an out-of-the-blue question.
- Do not force the user to provide technical detail they may not have;
  offer plain-language options and let "سایر / توضیح دلخواه" capture
  anything more technical they want to add.
- When several open items are of the same type (e.g. several Components all
  missing a Source Strategy), present them together in one structured
  question rather than one question per item.

## Protecting Output Quality and Context

Within these constraints, make whatever batching and sequencing choices best
protect two things at once: the accuracy of the Manifest (never sacrificed
to save a round) and the practical limits of the session (avoid so many
small, fragmented question calls that context or coherence degrades). When
in doubt, prefer fewer, well-structured, multi-part questions over many
single-item ones — not fewer questions overall.
