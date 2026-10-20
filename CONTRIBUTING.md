# Contributing

Corrections are the most useful contribution. This book goes out of date in specific,
predictable places.

## Highest-value fixes

- **Device results.** Test any of the six claims in `VERIFICATION.md` that lack hardware evidence on a real phone.
- **Stale figures.** Each annual report replaces the last. Check the year before you trust a number.
- **Deprecated APIs.** A previous revision cited a deprecated OWASP test as current. Others will go the same way.
- **MAS identifiers.** MASTG v2.0.0 (June 2026) deprecated every v1 test, and MASWE v1.0.0 (August 2026)
  renumbered every weakness. Before you cite a page, check it for a deprecation banner.
- **Certificate lifetimes.** The CA/Browser Forum schedule runs to 2029. Its dates and its domain control validation (DCV)
  reuse windows may still move.

## If you fix something

1. Edit the part file in `book/`, and update its `last_verified` frontmatter date.
2. Add a line to `book/12-verification.md` with the date and what changed. That chapter is valuable
   because it's honest about the book's own history, which works only if it stays current.
   If you're correcting an earlier entry, annotate it as superseded instead of deleting it.
3. Run the checks, then rebuild `dist/` (see the next section). CI fails if the single-file Markdown
   edition in `dist/` is out of date.

## Checking and building

```bash
python3 scripts/check.py            # cross-references, code fences, Swift, XML, workflow YAML
python3 scripts/check.py --mermaid  # also render every Mermaid diagram (needs Node)
python3 scripts/build.py --md-only  # rebuild the single-file Markdown edition
python3 scripts/build.py            # also rebuild both PDFs: book and cheat sheet (needs pandoc 3.1+, typst, Node)
```

On macOS, run `brew install pandoc typst actionlint node`. If a tool is missing, the check that needs it is skipped.

## Style

The book follows the Google and Microsoft developer style guides. For a full review pass, use the
editorial prompt in `editorial/PROMPT.md`; it applies these rules line by line and adds a fact check.

**Voice**

- Address the reader as "you". The author is "I", never "we", "our", or "let's".
- Use active voice and make clear who acts: "the server verifies the token", not "the token is verified".
  Keep passive voice only when the actor is unknown or irrelevant.
- Use present tense for descriptions and the imperative for instructions ("Run `strings` on your release build").
- Use contractions (it's, don't, you'll) where they read naturally.

**Words and sentences**

- Cut filler: simply, just, actually, basically, really, very, obviously, clearly, of course, easy, easily,
  quickly, please, please note, at this time, it is important to note that, it should be noted.
  Write "to", not "in order to".
- Put the condition before the instruction: "If StrongBox is unavailable, fall back to the TEE (trusted execution environment)."
- Aim for one idea per sentence, about 15–25 words. Split anything over about 35.
- Replace idioms with the literal statement, so a reader whose first language isn't English can't misread it.

**Spelling and punctuation**

- Use American spelling in prose: authorization, behavior, organization, artifact, defense, license, catalog.
  Keep the original spelling in code, API names, file names, URLs, 
  and direct quotations.
- Use the serial (Oxford) comma in every list of three or more: "Android, iOS, and Kotlin Multiplatform".
- Close up em dashes (word—word). Prefer a comma, colon, or parentheses when one works.
- Put code-related text in code font: `KeyGenParameterSpec`, `kSecAttrAccessible…`.

**Explanations**

- Define every term at first use, in plain words, or link to the section that defines it. Add new terms
  to the glossary with the section that teaches it.
- Where the industry disagrees, give both sides instead of picking one quietly.
- If you can't verify something, say so instead of hedging into vagueness.

**Book conventions**

- Mark weak claims: *(reported)*, *(estimate)*, *(reasoned)*, *(contested)*, or *(illustrative)*.
- Use these callout labels exactly: `> **Trap:**`, `> **Why it matters:**`, `> **In practice:**`, `> **Evidence:**`,
  plus **Try it** and **Verify it** blocks.
- Refer to sections as `§8.6`, to whole chapters as "Chapter 8", and to Part 0 chapters as "Chapter 0.3".
  Keep existing section numbers and headings stable: other parts link to them. Headings use American
  spelling. If you must rename one, update every link to its anchor: `scripts/check.py` checks § and
  Chapter references, not anchors.
- Tag every code fence with its language.
