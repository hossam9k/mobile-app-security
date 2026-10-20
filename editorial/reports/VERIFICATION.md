# VERIFICATION.md

## Summary
- Words before / after: 1,201 / 1,294
- Edits: clarity 12, filler 3, voice 10, spelling 6, explanation 5, code 0
- Facts checked: 14 · correct 13 · corrected 1 · unverified 1 (partially)

Facts checked (all 2026-10-20):

| Claim | Result | Source |
|---|---|---|
| Claim 5: Google says a token can't be "reused many times" and gives no number | Correct ("Google Play automatically prevents integrity tokens from being reused many times") | https://developer.android.com/google/play/integrity/standard |
| Claim 5: re-decrypting returns cleared verdicts (the claim, not its test status) | Correct as documented; still untested empirically | same |
| Claim 6: September 2026 Apple Developer Forums thread, about 0.01% of one app's users, persistent across reinstall and reboot, no Apple reply | Correct (about 360,000 active users, 30 users affected, 0 replies) | https://developer.apple.com/forums/thread/844380 |
| Claims 1–4 status text | Matches Part 12 "Claims this book asserts but has not empirically tested" | book/12-verification.md |
| 278 sources, Chapter 33 is the audit log | Consistent with Part 12 (count left for the coordinator) | book/12-verification.md |
| MASTG v2 tests and MAS data drift context | v2.0.0 released 30 June 2026 | https://github.com/OWASP/mastg/releases |
| IBM Cost of a Data Breach report gated behind a form | Consistent: the 2026 report (29 July 2026) is distributed by IBM through registration | https://www.ibm.com/think/x-force/2026-cost-of-a-data-breach-ai-adversaries-enterprise-risk |
| OWASP LLM Top 10 2026 behind a download | Partially confirmed: genai.owasp.org/llm-top-10 still shows only the 2025 list, and the 2026 edition (August 2026) isn't on that page | https://genai.owasp.org/llm-top-10/ |
| `scripts/check.py` parses Swift with `swiftc -parse` and checks XML with `xmllint` where installed, including CI | Correct (the CI runner `ubuntu-24.04` ships swiftc; the workflow installs `libxml2-utils`) | scripts/check.py; .github/workflows/check-book.yml |
| Android 17 emulator, iOS 26.5 and 27.0 simulators | Consistent with Part 12 test record | book/12-verification.md |
| Re-verification cadence table | Corrected: it omitted Chapters 23–25 and Part 10 (see below) | book/12-verification.md § "Where to look first when re-verifying" |
| Corrections list (9 bullets) | Each matches a Part 12 entry; "Validation arithmetic" is the DCV reuse arithmetic (Part 12, 10 September entry, superseded 24 September) | book/12-verification.md |
| `NSC` abbreviation | Expanded at first use | — |
| Last full audit 23–24 September 2026, ten independent reviewers | Consistent with Part 12 | book/12-verification.md |

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| Where to look first when re-verifying | "Semi-annually: 13, 14, 18, 22 tooling and privacy" | "Semi-annually: 13, 14, 18, 22–25 tooling, privacy, and assessment", plus a new row "With each re-check of the chapters it cites: Part 10" | Part 12 table lists 23–25 as semi-annual and Part 10 as inheriting its chapters' cadence | 2026-10-20 |
| Corrections already made | "Validation arithmetic … corrected against the Baseline Requirements" | "Domain-validation (DCV) reuse arithmetic … corrected against the CA/Browser Forum Baseline Requirements" (clarifies which arithmetic; meaning unchanged) | Part 12, "The validation arithmetic" entry | 2026-10-20 |

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| What the last audit did not cover | The OWASP LLM Top 10 2026 list sits "behind a download" | genai.owasp.org/llm-top-10 (shows 2025 only); press says the canonical text is in the GenAI-LLM-Top10 repository, so the 2026 list may now be readable without a download | None needed in this file (it's a coverage statement); Chapter 20's editor should check whether the primary is now public |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Verify it blocks | MASTG undefined | "OWASP Mobile Application Security Testing Guide (MASTG)" |
| Claims with no hardware evidence | Secure Enclave and StrongBox undefined | "the hardware key stores (the Secure Enclave on Apple devices, StrongBox on Android)" |
| Claims table, row 2 | "NSC" used before definition | "network security config (NSC)" |
| Corrections already made | SPKI undefined | "(the encoded public key and its algorithm)" |
| Corrections already made | "Validation arithmetic" opaque | "Domain-validation (DCV) reuse arithmetic", "CA/Browser Forum Baseline Requirements" |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| book/07-platform-surfaces-and-new-frontiers.md | Chapter 20 | Check whether the OWASP Top 10 for LLM Applications 2026 text is now public (the GenAI-LLM-Top10 repository). If it is, cite it directly and drop *(reported)* where the text relies only on press coverage | VERIFICATION.md lists it as a gated primary |
| VERIFICATION.md (coordinator) | Last full audit | After this October 2026 editorial pass finishes, decide whether to record it here | The file still names 23–24 September as the last full audit |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| — | None (all terms added here are glossed inline and already in the glossary) | — |

## Judgment calls
- **"read cold by an editor"** became "an editor with no prior context read it". This removes the idiom.
- **"Stated because an audit that does not declare its own coverage is worthless"** became "An audit that doesn't state its own coverage gives you no way to judge it, so here are the gaps." The new wording is less absolute but makes the same point.
- **"Parts 3 and 5 compiled their listings"** was recast with the action in passive voice ("The listings … were compiled"). A Part can't compile anything, and the actor isn't recorded.
- I kept most past-tense passives about the audit ("were tested", "was re-verified"). The actor varies (the author, editors, reviewers), and the file doesn't name one. Switch them to "I" if the author ran them personally.
- I kept day-month-year dates ("23–24 September 2026") to match the rest of the book.
