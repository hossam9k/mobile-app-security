# Contributing

Corrections are the most useful contribution. This document ages in specific,
predictable places.

## Highest-value fixes

- **Stale figures.** Annual reports supersede each other. Check the year before trusting a number.
- **Deprecated APIs.** A previous revision cited a deprecated OWASP test as current. Others will go the same way.
- **MASTG identifiers.** The v2 refactor is ongoing: low-numbered tests are being split into atomic tests
  with higher numbers. Check each test page for a deprecation banner before citing it.
- **Certificate lifetimes.** The schedule runs to 2029. Dates and DCV reuse windows will move.

## If you fix something

Add a line to `book/12-verification.md` with the date and what changed. The value of that
chapter is that it is honest about the document's own history, which only works if it stays current.

## Style

- Second person, active voice, present tense.
- Define a term where it first appears.
- Where the industry disagrees, give both sides rather than picking quietly.
- Mark weak claims: *(reported)*, *(estimate)*, *(reasoned)*, *(contested)*.
- If you cannot verify something, say so rather than hedging into vagueness.
