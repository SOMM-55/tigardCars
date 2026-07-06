---
name: keyword-extraction
description: >
  Used by `incremental-planner`. Extract effective search keywords from a user's natural-language feature description.

---

## Three Tiers

**Tier 1 — Specific names** (highest signal):
- Exact feature name as it'd appear in docs ("Social Login", "social_login")
- Named providers / vendors / services ("Google", "Apple", "Stripe")
- Named entities ("Subscription", "Invoice")

**Tier 2 — Domain terms**:
- "OAuth", "SSO", "webhook", "subscription", "checkout"
- Field names if mentioned

**Tier 3 — Generic terms** (low signal, use sparingly):
- "auth", "user", "login" — only if Tier 1+2 returned too little

## Patterns

- Tier 1: exact match
- Tier 2: case-insensitive
- Tier 3: only within already-narrowed directories

## Examples

**"Social login was added — Google and Apple per PRD §4.5"**
- Tier 1: `"social login"`, `"Social Login"`, `"Google"`, `"Apple"`
- Tier 2: `"OAuth"`, `"SSO"`, `"provider"`
- Explicit ref: read `prd/auth.md` directly

**"We added a Subscription entity"**
- Tier 1: `"Subscription"`
- Tier 2: `"subscription_id"`, `"recurring"`, `"billing"`
- Likely layers: `sdd/data-model.md`, `sdd/billing.md`, `sdd_client/billing.md`

**"The dashboard layout changed"**
- Tier 1: `"dashboard"`
- Tier 2: `"AppShell"`, `"sidebar"`
- Layer hint: `layout/`, `IA/`, `sdd_client/dashboard.md`
- Fuzzy — likely needs clarification before deep dive

## When Description Doesn't Yield Keywords

For vague requests like "fix the auth stuff", return:

```json
{
  "clarification_needed": true,
  "reason": "Description too vague",
  "suggested_questions": [
    "Which auth flow — login, signup, password reset, MFA, or social?",
    "Fix to existing planned tasks or a new feature?"
  ]
}
```

The orchestrator turns these into `AskUserQuestion` options.
