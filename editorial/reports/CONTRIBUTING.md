# CONTRIBUTING.md

## Summary
- Words before / after: 400 / 695
- Edits: clarity 6, filler 1, voice 5, spelling 2, explanation 3, code 0 (plus the Style section rewrite)
- Facts checked: 7 · correct 6 · corrected 1 · unverified 0

Facts checked (all 2026-10-20):

| Claim | Result | Source |
|---|---|---|
| MASTG v2.0.0 (June 2026) deprecated every v1 test | Correct (30 June 2026) | https://github.com/OWASP/mastg/releases |
| MASWE v1.0.0 (August 2026) renumbered every weakness | Correct (17 August 2026) | https://github.com/OWASP/maswe/releases |
| Certificate lifetime schedule runs to 2029 | Correct (SC-081v3: 200 days from 15 March 2026, 100 from 15 March 2027, 47 from 15 March 2029; DCV reuse 10 days in 2029) | https://pasqualepillitteri.it/en/news/2764/47-day-ssl-tls-certificates-2029-ballot-sc-081v3 (secondary; ballot cited in Part 3) |
| Six claims with no hardware evidence | Correct | VERIFICATION.md |
| `check.py` / `build.py` commands and flags | Correct | scripts/check.py; scripts/build.py |
| PDF needs pandoc 3.1+, typst, Node | Correct (build.py docstring: "pandoc >= 3.1, typst, and Node (npx)") | scripts/build.py |
| "CI fails if `dist/` is out of date" | Corrected (see below) | .github/workflows/check-book.yml |

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| If you fix something | "CI fails if `dist/` is out of date." | "CI fails if the single-file Markdown edition in `dist/` is out of date." | .github/workflows/check-book.yml (diffs only the single-file `.md`) | 2026-10-20 |
| Checking and building | `brew install pandoc typst actionlint` | `brew install pandoc typst actionlint node` (Node is needed for `--mermaid` and the PDF) | scripts/check.py, scripts/build.py | 2026-10-20 |

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| — | None | — | — |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Highest-value fixes | DCV undefined; who sets the schedule | "The CA/Browser Forum schedule…", "domain-validation (DCV) reuse windows" |
| Style | No pointer to the review process | Points to `editorial/PROMPT.md` as the prompt for future review passes |
| Style | TEE undefined in the example | "TEE (trusted execution environment)" |

## Style section rewrite
The section changes from British to American spelling, as briefed. It now has five groups:
- **Voice:** second person, "I" never "we", active voice, present tense for descriptions, imperative for instructions, and contractions.
- **Words and sentences:** the full filler list, condition before instruction, sentence length, and no idioms.
- **Spelling and punctuation:** American spelling with the code, API, file, URL, link-target heading, and quotation exceptions; the serial comma; closed em dashes; and code font.
- **Explanations:** define at first use and add to the glossary, give both sides, and say so when you can't verify something.
- **Book conventions:** these rules are kept from the original: confidence markers, callout labels (now listing **Try it** and **Verify it**), § and Chapter references, stable headings, and fence tags.

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| — | — | None | — |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| — | None | — |

## Judgment calls
- **Active-voice example:** I replaced PROMPT.md's "the TA decrypts the keyblob" with "the server verifies the token", because a contributor guide shouldn't need TA (trusted application) and keyblob defined. Restore the original if you want it to match PROMPT.md word for word.
- **Opening line:** "This document ages in specific, predictable places" became "This book goes out of date in specific, predictable places". The list that follows is about the book, not this file.
- **Certificate lifetimes:** "Dates and DCV reuse windows will move" became "may still move". The SC-081 schedule is adopted, so "will" overstated it.
- The file grew from 400 to 695 words, mostly in the Style section, as briefed.
