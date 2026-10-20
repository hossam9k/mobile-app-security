# book/01-understanding-the-threat.md

## Summary
- Words before / after: 4,723 / 5,210 (`wc -w`; the growth is mostly new definitions)
- Edits: clarity 24, filler 7, voice 12, spelling 14, explanation 16, code 0
- Facts checked: 74 · correct 61 · corrected 7 · unverified 6

Checked on 2026-10-20. `python3 scripts/check.py`: 0 problems. `last_verified` is set to 2026-10-20. `recheck_because` is unchanged because none of its facts changed.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| 1.1 | "Android's developer verification requirement, starting 30 September 2026 (Chapter 0.4)" | The requirement took effect on 30 September 2026 for installs from participating stores on certified devices in Brazil, Indonesia, Singapore, and Thailand. Google plans to expand it globally from 2027. | https://developer.android.com/developer-verification | 2026-10-20 |
| 1.1 | "apps targeting Android 7 or later ignore user-installed certificate authorities" | Adds "By default" and "(API level 24)". An app can opt back in with `<certificates src="user"/>`. | https://developer.android.com/privacy-and-security/security-config | 2026-10-20 |
| 2.1 | "driven by higher detection, escalation and lost-business costs" | "Its two largest cost categories each rose by more than 11%: detection and escalation, and lost business *(reported)*". The old wording split IBM's single "detection and escalation" category into two items, and IBM itself doesn't call these the drivers. | https://www.secureworld.io/industry-news/cost-data-breach-report-2026 | 2026-10-20 |
| 2.1 | DBIR: mobile social engineering "outperforming email phishing" | Adds the figure: it succeeds about 40% more often than email phishing. | https://www.verizon.com/about/news/breach-industry-wide-dbir-finds | 2026-10-20 |
| 3.1 | "OWASP counts 35 of the 78 as having no MASTG test yet" | "At release, 36 of the 78 had no MASTG test. On 20 October 2026, 35 of the weakness pages still said 'No Tests Yet'." The release post says 36. I fetched all 78 MASWE pages today and counted 35. | https://mas.owasp.org/news/2026/08/17/maswe-v100-release/ and the 78 MASWE pages | 2026-10-20 |
| 3.1 | MASTG v2.0.0 "released at the end of June 2026"; "no longer ships the MAS Checklist spreadsheet (or a PDF)" | "released on 30 June 2026". The spreadsheet removal now links to the OWASP post. The text now says OWASP had already discontinued the PDF before v2, so v2 didn't drop it. | https://github.com/OWASP/mastg/releases/tag/v2.0.0, https://mas.owasp.org/news/2026/07/14/checklists-removal/ | 2026-10-20 |
| 3.2 / 3.3 | Profiles "reworked again during the 2026 MASWE refactor"; "Google's App Defense Alliance MASA" | Profiles: "rebuilt them around MASWE weaknesses (each profile page lists its requirements by MASWE ID)". I couldn't confirm the timing of the rework, but I saw the structure on the pages myself. ADA: Google founded it, and the Linux Foundation now hosts it. | https://mas.owasp.org/Profiles/MAS-L1/, https://security.googleblog.com/ (ADA move to the Linux Foundation) | 2026-10-20 |

Date updates, not corrections: "editions available in September 2026", "still current in September 2026", and "Current versions, September 2026" now say October 2026. I checked that no newer IBM, DBIR, GitGuardian, MASVS, MASWE, or MASTG edition exists as of 2026-10-20.

Verified as correct: CloudSEK 3,207 and 230 apps; JADX; FairPlay and in-memory decryption; frida-ios-dump listed in MASTG; the iOS profile plus full-trust step; the Android 14 Conscrypt APEX root store, updated through Play; Frida Gadget; the sandbox paths. IBM: 29 July release, 602 organizations, 17 industries, March 2025 to February 2026, $4.99M, +12%, record, $6M AI-enabled, both quotes, 247 days, +2.5% from 241, first rise after five years of improvement, 2024 $4.88M, 2025 $4.44M. DBIR: 19 May, 31%, first time in 19 years, 48%. GitGuardian: 5th edition, 17 March, 28.65M, +34%, largest jump, 152% vs 98%, 64% still valid, 1,275,105 (+81%), 8 of 10, 3.2% vs 1.5% plus the caveat, 24,008 and 2,117 MCP secrets plus the setup-guide reason, Shai-Hulud 2 at 59%, 28% outside code, +13 points. Mobile Top 10: 2024 final, M1, M2. MAS rebrand August 2022. MASVS: v2.1.0 on 18 January 2024, 8 categories, 24 controls, PRIVACY added, v2.0.0 April 2023, STORAGE-1 and NETWORK-2 wording. MASWE: July 2024 beta, 17 August 2026, 78 weaknesses, 119/47/72/6, ID stability, a requirement sentence for each weakness, the mapping link, MASWE-0001 title and L2 tag. MASTG: first stable release, refactor since 2021, about 860 components, the "no longer maintained" and "for a limited time" quotes, the Show Deprecated switch, TEST-0001 → 7 v2 tests, TEST-0044 → 2, TEST-0287 title. DEMO-0059 exists (its title is paraphrased in Figure 4). Profile names, assumptions, and recommendations. MAS-R "never alone". EUDIW partners and risk-register mapping. The no-certification text. ASVS pointer. "Tools alone" text. CC BY-SA 4.0. Pinning Cheat Sheet quotes. Crackmes link (200). xcarchive path.

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| 2.1 | US average $11.5M | Not in IBM's press release or on the report landing page. Baker Donelson and SecureWorld both report it. | *(reported)*, added |
| 2.1 | 16 countries and regions | Not on IBM's pages. Secondary sources disagree: 16 or 17. | *(reported)*, added |
| 2.1 | 183 days to identify / 64 to contain | Only in secondary reporting (SecureWorld). | Covered by the existing *(reported)* |
| 2.1 | Cost-category growth (>11% each) | Secondary reporting only. | *(reported)*, added |
| 1 (opening) | CloudSEK figures | The Hacker News and Security Magazine links return 403 to automated fetchers. Several outlets (ITPro, SC Media, Venafi) confirm the figures. The links probably still work in a browser. | Existing *(reported)* kept |
| 2.3 | "Any $50,000 to $500,000 per incident figure… is an estimate someone made up" | An author judgment; nothing to check it against. | Left as is |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| 1.1 | rooted, jailbroken, instrumented | Plain definitions in the opening paragraph |
| 1.1 | APK, DRM, MASTG (used before §3.1), disassembler | Short glosses at first use |
| 1.1 | `strings` | What the tool does |
| 1.1 | Why an intercepting proxy works | "The proxy presents its own certificate, so the attacker only has to make your app trust it" |
| 1.1 | Android options listed in one long sentence | Split into three options, and named the Conscrypt module |
| 1.1 | Certificate pinning, hooking, Frida, sideload, sandbox | One-clause definitions |
| 1.2 | Trust boundary | Definition |
| 1.2 | Why client checks are only signals | One sentence: the check runs on the attacker's device and can be hooked |
| 1.2 | "one layer in a costume" (idiom) | Literal wording plus a Frida example |
| 1.3 | Attestation, BFF, hygiene | Definitions at first use |
| 1.3 | Triage | Glossed as "decide which risk to address first" |
| 1 Try it | "Rotate" | "issue a new one and revoke the old one" |
| 2.2 | Hardcoded secrets, MCP | Definitions |
| 3.1 | CWE | Expanded |
| 3.3 | MASA, ASVS, CC BY-SA | Expanded |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| CONTRIBUTING.md | Style | The style rules say "British spelling in prose". The editorial PROMPT says American. | I followed PROMPT. Every part needs the same rule, and the glossary in `book/12-verification.md` is still British (Authorisation, Deserialisation, and others). |
| book/12-verification.md | Glossary | Add a CWE entry. Consider "Trust boundary" and "Intercepting proxy" (see below). | New terms defined in §1.2 and §3.1 |
| book/12-verification.md | Audit log | Add a line for the 2026-10-20 pass: the developer-verification wording, the 36-at-release vs 35-today MASWE count, and the ADA host. | CONTRIBUTING requires the log line, and I may edit only Part 1. |
| book/09-the-catalogues.md | Line 147 | The "35 of the 78" count, read on 24 September, still matches today's count. You could add that the v1.0.0 release post said 36. | Consistency with §3.1 |
| book/10-questions-and-answers.md | Lines 74, 918 | Check how the App Defense Alliance is described (it's now hosted by the Linux Foundation). | Consistency with §3.3 |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Trust boundary | The line where you stop trusting input and start checking it. In mobile, your server, never the client. | §1.2 |
| CWE | MITRE's Common Weakness Enumeration: the general-software catalog of weakness types that MASWE mirrors for mobile. | §3.1 |
| Intercepting proxy | A tool (mitmproxy, Burp Suite) that sits between app and server, presents its own certificate, and reads or changes traffic. | §1.1 |
| MCP | Model Context Protocol, a standard way to connect AI assistants to tools and data. Its config files are a leading place where secrets leak. | §2.2 |

## Judgment calls
- **American spelling** (organize, behavior, defense, authorization, catalog, program, practice, specialized, analyzed). This follows PROMPT.md, which contradicts CONTRIBUTING.md. I didn't touch any headings. If the book stays British, revert these.
- **MASWE count**: I give both numbers, 36 at release (OWASP's post) and 35 today (my page count). Part 9 already uses 35. "One of the 35 that still have none" in Try it will go stale. That's deliberate, the same as Part 9.
- **Figure 4**: I left the demo node label as the existing paraphrase. The official title is "Using SharedPreferences to Write Sensitive Data Unencrypted to the App Sandbox".
- **Definitions vs links**: Part 0 already defines rooting, hooking, attestation, and defense in depth. I added short inline glosses rather than `Chapter 0.1` links, so the threat list reads on its own. Cut them if they feel repetitive.
- **"Getting this wrong is the most common way to show… that your knowledge is out of date"** replaces the idiom "date yourself". It's longer but literal.
- I removed a second expansion of OWASP from Chapter 3, because start-here.md already defines it.
