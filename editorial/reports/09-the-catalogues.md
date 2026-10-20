# book/09-the-catalogues.md

## Summary
- Words before / after: 5617 / 5847
- Edits: clarity 14, filler 3, voice 9, spelling 16, explanation 7, code 0
- Facts checked: 236 · correct 230 · corrected 4 · unverified 2

Method (checked 2026-10-20):
- MASVS: all 24 control statements compared by script, character for character, against the official `OWASP_MASVS.yaml` v2.1.0 release asset (github.com/OWASP/masvs/releases/tag/v2.1.0, published 2024-01-18). 24/24 identical. Glosses checked against each control's official description; NIST SP 800-175B / SP 800-57 reference confirmed in the CRYPTO category text.
- MASWE: all 78 IDs and titles compared by script against the v1.0.0 `OWASP_MASWE.yaml` release asset (github.com/OWASP/maswe/releases/tag/v1.0.0, published 2026-08-17). 78/78 titles identical. Every Control column value equals the first `masvs-v2` mapping. Release notes confirm 119 → 78, 72 renamed, 47 absorbed, 6 new, the block order, "future IDs not consecutive", the four-section page structure, and MASWE-0075 under MASVS-PRIVACY-3.
- MASTG: shallow clone of github.com/OWASP/mastg (HEAD 02ffd85, 2026-09-30). All 78 Tests-column values recomputed from test frontmatter (`maswe:` and `status:`): 78/78 match; 35 weaknesses have zero current tests. 200 v2 tests = 186 current + 14 placeholder; 92 v1 tests, all `status: deprecated`, IDs 0001–0093 without 0074. Current-page counts: 165 techniques, 66 + 8 best practices, 150 demos, 133 knowledge, 129 tools — all match. Each v1 → v2 replacement row checked against `covered_by`. Every test ID, platform, and topic in both "tests worth knowing" tables, every technique ID/title, every best-practice ID/title/placeholder status, the URL-category exceptions (0246–0249, 0372/0374/0375, 0398–0400), the neighboring-weakness trap (0276–0280, 0340 → MASWE-0036; 0334, 0376–0380 → MASWE-0034), and MASTG-DEMO-0106 (test: MASTG-TEST-0341) checked. MASTG v2.0.0 release date 2026-06-30 confirmed via GitHub API.
- mas.owasp.org: banner texts ("is deprecated and should not be used anymore", "This test hasn't been created yet", "No Tests Yet") and the "Show Deprecated" filter (site `table_filters.js`) confirmed live; sample URLs return 200.
- Platform table: Android rows checked against developer.android.com behavior-change pages for 10, 12, 13, 14, 15, 16, 17, the NSC, Keystore, WebSettings, ClipDescription, page-sizes, and Play target-SDK pages, plus source.android.com Conscrypt. iOS rows checked against Apple documentation JSON (availability/deprecation versions), Apple Platform Security guide, Upcoming Requirements page, iOS 12.1.1 release notes, WWDC26 session 201.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| Part 9 intro, Trap | "at least one (beta MASWE-0097) appears under none" | "seven beta IDs appear under more than one v1 weakness, and six (beta MASWE-0090, 0095 to 0098, and 0107) appear under none" | `maswe-beta` keys in https://github.com/OWASP/maswe/releases/download/v1.0.0/OWASP_MASWE.yaml | 2026-10-20 |
| Ch 28, Android table, API 31 | "`allowBackup="false"` no longer stops device transfer" | "on some manufacturers' devices `allowBackup="false"` no longer stops device transfer" | https://developer.android.com/about/versions/12/behavior-changes-12 (D2D transfer section) | 2026-10-20 |
| Ch 28, iOS table, iOS 12 | "Certificate Transparency enforced for publicly trusted certificates issued after 15 October 2018" | "Certificate Transparency enforced (12.1.1) for …" | iOS 12.1.1 release notes, https://developer.apple.com/documentation/ios-ipados-release-notes/ios-12_1_1-release-notes | 2026-10-20 |
| Ch 28, Android techniques | "0127, 0128 inspecting backups" | "0127, 0128 inspecting backup data, and performing a backup and restore" (TECH-0128 is "Performing a Backup and Restore of App Data") | OWASP/mastg `techniques/android/MASTG-TECH-0128.md` | 2026-10-20 |

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| Ch 27, "Three that deserve special attention" | "Engineers routinely miss these three"; MASWE-0024 "common" because logout is built as an auth concern; no-test weaknesses "disproportionately the ones teams miss" | Author judgment, no primary source exists | *(reasoned)* — added |
| Ch 28, iOS 17.3 / 17.4 rows | Stolen Device Protection (17.3), EU alternative marketplaces (17.4) | Confirmed only via secondary press coverage in search results; Apple support/newsroom pages did not render | Facts are well established; no marker added, but recheck against Apple newsroom if desired |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Part 9 intro | MASVS, MASWE, MASTG never expanded in this file | One sentence naming the three catalogs and what each lists |
| Ch 26, MASVS-AUTH-3 | "Step-up authentication" undefined | "asking the user to authenticate again before a risky action" |
| Ch 26, MASVS-RESILIENCE-2 | No gloss | "Covers detecting a modified copy of your app, in its code or its resources" (from the official control description) |
| Ch 27 intro | Reader can't tell why a weakness sits under one control when it maps to several | Paragraph: the Control column is the first control MASWE lists, which decides the block |
| Ch 27, MASWE-0075 | Why non-reproducible builds matter was compressed | Spelled out: without a reproducible build nobody can verify the shipped binary matches reviewed code |
| Ch 28, demos | Why a demo that extracts plaintext belongs to a hook-detection test | Explained it's the failing case of MASTG-TEST-0341: no hook detection, so the hook works |
| Ch 28, no-v2-replacement paragraph | MASVS-STORAGE-2 pointer applied to the WebView JS test too | Scoped STORAGE-2 to the memory tests; Modes of Introduction for all |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| CONTRIBUTING.md | Style | Says "British spelling in prose"; editorial/PROMPT.md requires American | Contradictory house rules; I followed PROMPT.md |
| book/09-the-catalogues.md (heading, not edited) | Part 9 title, "MASVS-AUTH — authentication and authorisation", "Authentication and authorisation (MASVS-AUTH)" | British spelling ("catalogues", "authorisation") in headings | Headings are link targets; left unchanged per hard constraints. Change only with all inbound links |
| book/09-the-catalogues.md frontmatter | `recheck_because` | Uses "neighbouring" | Frontmatter not editable unless a fact changed; facts unchanged |
| book/12-verification.md | Correction log | Add a 2026-10-20 entry for the four corrections above | CONTRIBUTING step 2 |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Step-up authentication | Asking the user to authenticate again before a sensitive action (MASVS-AUTH-3) | Chapter 26 (MASVS-AUTH-3) — add only if the glossary lacks it |

## Judgment calls
- American spelling applied in prose (enrollment, deserialization, minimization, sanitize, analyzing, behavior, catalog, neighboring) per PROMPT.md, against CONTRIBUTING.md. OWASP verbatim titles kept as published (e.g. "Pseudonymisation" in MASWE-0067).
- Platform-defaults intro: "Raising … the iOS deployment target" → "building with a newer iOS SDK". iOS behavior changes in the table (e.g. the 25-entry `LSApplicationQueriesSchemes` limit) key off the linked SDK, not the deployment target. Revert if the author meant deployment target deliberately.
- Added "rechecked on 20 October 2026" to the intro, the Tests-column paragraph, and the MASTG counts, since the numbers were reverified today and are unchanged. "As of September 2026" in the trap became "As of October 2026".
- "So there is no excuse for not checking it" → "so check it on every release" (tone).
- "Which surprises everyone" removed; replaced with "You might not expect it under Privacy".
- Fragment glosses after control statements ("Obfuscation.", "Chapter 19.") turned into full sentences ("Covers …", "See Chapter 19.").
- Serial commas added throughout prose and table descriptions.
