# README.md

## Summary
- Words before / after: 1,250 / 1,367
- Edits: clarity 14, filler 5, voice 9, spelling 4, explanation 8, code 0
- Facts checked: 17 · correct 16 · corrected 1 · unverified 0 (2 rest on secondary sources only; see notes)

Facts checked (all 2026-10-20):

| Claim | Result | Source |
|---|---|---|
| MASVS v2.1.0 is current | Correct (latest release) | https://github.com/OWASP/masvs/releases |
| MASWE v1.0.0, August 2026, renumbered every weakness | Correct (17 Aug 2026, "renumbers every weakness") | https://github.com/OWASP/maswe/releases |
| MASTG v2.0.0, June 2026, deprecated every v1 test | Correct (30 Jun 2026) | https://github.com/OWASP/mastg/releases |
| 24 MASVS controls | Correct (8 categories, 24 control pages) | https://mas.owasp.org/MASVS/ |
| 78 MASWE weaknesses | Correct (MASWE-0001 to MASWE-0078) | https://mas.owasp.org/MASWE/ |
| `MASVS-NETWORK-2` asks for identity pinning of endpoints you control | Correct (matches the verbatim control text in Part 9) | https://mas.owasp.org/MASVS/controls/MASVS-NETWORK-2/ |
| OWASP Pinning Cheat Sheet says most apps should probably never pin | Correct ("The answer to this is probably never.") | https://cheatsheetseries.owasp.org/cheatsheets/Pinning_Cheat_Sheet.html |
| Android 17 is current | Correct: API 37; stable for Pixel on 16 June 2026 per press. The developer.android.com release-notes page still lists only betas (last: Beta 4.1, 1 June 2026) | https://developer.android.com/about/versions/17 ; https://www.androidauthority.com/android-17-release-date-3639790/ |
| iOS 27 is current | Correct: public release 14 September 2026 (press coverage; no Apple primary fetched) | https://www.etvbharat.com/en/technology/apple-confirms-ios-27-release-date-heres-when-it-lands-on-your-iphone-enn26091003097 |
| 47-day certificates | Correct (CA/B Forum SC-081v3: 47 days from 15 March 2029) | https://pasqualepillitteri.it/en/news/2764/47-day-ssl-tls-certificates-2029-ballot-sc-081v3 (secondary; ballot cited in Part 3) |
| OWASP LLM Top 10 2026 exists | Correct (published August 2026) | https://labs.cloudsecurityalliance.org/research/csa-research-note-owasp-genai-top10-2026-agent-control-stand/ |
| CVSS v4.0 is the current version | Correct (no later version found) | https://www.first.org/cvss/v4-0/ |
| tj-actions and TanStack CI incidents | Correct (TanStack: 11 May 2026, cache poisoning via `pull_request_target`) | https://www.infoq.com/news/2026/05/tanstack-supply-chain-attack |
| Two claims untested, four with emulator/simulator evidence only | Correct (matches VERIFICATION.md and Part 12) | book/12-verification.md |
| OWASP MAS material is CC BY-SA 4.0; book is CC BY-SA 4.0 | Correct | LICENSE; https://mas.owasp.org/ |
| `scripts/check.py` checks listed (refs, captions, fences, Swift, XML; actionlint; `--mermaid`) | Correct | scripts/check.py |
| CI "fails if `dist/` is out of date" | Corrected (see below) | .github/workflows/check-book.yml |

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| What makes this different | "CI … fails if `dist/` is out of date" | "It fails if the single-file Markdown edition in `dist/` is out of date" | `.github/workflows/check-book.yml` (only `build.py --md-only` plus `git diff` on the single-file `.md`; the PDF isn't checked) | 2026-10-20 |

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| — | None. Android 17 stable date and iOS 27 release date rest on press reports; the README states only the version names, so no marker is needed | developer.android.com release notes, press searches | — |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Intro | MASVS, MASWE, and MASTG used undefined | "the three OWASP Mobile Application Security (MAS) projects", each glossed (requirements, weaknesses, testing guide) |
| Read it table | CT, ECH, CI, IPC, DPoP undefined | Expanded to Certificate Transparency, Encrypted Client Hello, continuous integration (CI), inter-process communication (IPC), DPoP (proof-of-possession tokens) |
| What makes this different | "Pinning" undefined | One-sentence definition, plus a link to the Pinning Cheat Sheet and to Chapter 8 |
| What makes this different | `check.py` sentence conflated actionlint and Node | Split: actionlint lints workflow YAML; Node plus `--mermaid` renders diagrams |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| — | — | None | — |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| — | None (README isn't a teaching section) | — |

## Judgment calls
- **Heading "## Licence and attribution" kept** with British spelling because headings are link targets. Rename to "License and attribution" if nothing links to `#licence-and-attribution`.
- **Spaced em dashes kept** in the H1 title, the image `alt`, and the "0 — Foundations" link labels in the parts table. They mirror the title, which I can't change. Close them up if the coordinator wants consistency.
- **"catalogues" kept** in the link label "9 — The catalogues", in the file name, and in the Part 9 title; changed to "catalogs" in prose.
- **"New to the engineering side?" → "New to security engineering?"** I read the original as meaning engineers new to security, which matches the book's stated audience. Reverse if it was meant for non-engineers.
- **"go back to whichever answers were shaky"** became "reread the chapters behind any answer you weren't sure of". This removes the idiom and states the action.
- Word counts, the 210-term glossary count, and the 278 source count were left for the coordinator to refresh.
