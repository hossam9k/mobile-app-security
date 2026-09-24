# Contributing

Corrections are the most useful contribution. This document ages in specific,
predictable places.

## Highest-value fixes

- **Device results.** Any of the six claims with no hardware evidence in `VERIFICATION.md`, run on a real phone.
- **Stale figures.** Annual reports supersede each other. Check the year before trusting a number.
- **Deprecated APIs.** A previous revision cited a deprecated OWASP test as current. Others will go the same way.
- **MAS identifiers.** MASTG v2.0.0 (June 2026) deprecated every v1 test, and MASWE v1.0.0 (August 2026)
  renumbered every weakness. Check each page for a deprecation banner before citing it.
- **Certificate lifetimes.** The schedule runs to 2029. Dates and DCV reuse windows will move.

## If you fix something

1. Edit the part file in `book/`, and update its `last_verified` frontmatter date.
2. Add a line to `book/12-verification.md` with the date and what changed. The value of that
   chapter is that it is honest about the book's own history, which only works if it stays current.
   If you are correcting an earlier entry, annotate it as superseded rather than deleting it.
3. Run the checks, then rebuild `dist/` (below). CI fails if `dist/` is out of date.

## Checking and building

```bash
python3 scripts/check.py            # cross-references, code fences, Swift, XML, workflow YAML
python3 scripts/check.py --mermaid  # also render every Mermaid diagram (needs Node)
python3 scripts/build.py --md-only  # rebuild the single-file Markdown edition
python3 scripts/build.py            # also rebuild the PDF (needs pandoc 3.1+, typst, Node)
```

On macOS: `brew install pandoc typst actionlint`. Each check is skipped if its tool is missing.

## Style

- Second person, active voice, present tense. "I" for the author, never "we".
- British spelling in prose (artefact, authorisation, behaviour); US spelling only in API names and quotations.
- Define a term where it first appears, and add it to the glossary with the section that teaches it.
- Where the industry disagrees, give both sides rather than picking quietly.
- Mark weak claims: *(reported)*, *(estimate)*, *(reasoned)*, *(contested)*, *(illustrative)*.
- Callouts: `> **Trap:**`, `> **Why it matters:**`, `> **In practice:**`, `> **Evidence:**`.
- Refer to sections as `§8.6`, to whole chapters as "Chapter 8", and to Part 0 chapters as "Chapter 0.3".
  Keep existing section numbers and headings stable: other parts link to them.
- Tag every code fence with its language.
- If you cannot verify something, say so rather than hedging into vagueness.
