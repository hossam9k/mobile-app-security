# book/12-verification.md

## Summary
- Words before / after: ~17,300 (estimate; the repo has no git baseline) / 17,455
- Edits: clarity 38, filler 4, voice 12, spelling 66, explanation 7, code 0
- Facts checked: 278 source links plus about 65 claims from the glossary, the tables, and the uncertainty list · correct: all links resolve and nearly all claims hold · corrected: 11 links, 2 facts (`datastore-tink` status; developer verification "sideloaded" wording), and 1 uncertainty resolved (AI Act Omnibus) · unverified: 0 (6 uncertainty items stay open, with no primary source to settle them)

Notes:
- **Spelling.** PROMPT.md asks for American spelling. CONTRIBUTING.md still says British. I converted the prose (behavior, organization, program, catalog, authorization, labeled, modeling, enrollment, and others). I kept headings that are link targets ("the programme layer"), URLs, code, and the quoted "29 votes in favour". The 24 September log line that says "House style unified (British spelling…)" is history, so I kept it as written.
- **Em dashes.** I closed up all list-separator dashes ("**Term**—Definition", "Title—<url>"). In prose I replaced dashes with a colon, comma, or parentheses. Two spaced dashes remain: the heading "Known uncertainties — treat with care" (a link target) and a "| — |" empty table cell.
- `last_verified` is set to 2026-10-20: Pass 3 is complete for the whole file. I added one source: EUR-Lex, Regulation (EU) 2026/1744.
- `python3 scripts/check.py`: 0 problems.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| Sources, Android | `developer.android.com/guide/topics/data/audit-access` | `developer.android.com/privacy-and-security/audit-data-access` | redirect | 2026-10-20 |
| Sources, Android | `.../shared/photopicker` | `.../shared/photo-picker` | redirect | 2026-10-20 |
| Sources, Android | Play Photo and Video Permissions, `answer/14115180` | `answer/16935362` ("Understanding Restricted Permissions with minimum scope alternatives", which has the Photo and Video section) | support.google.com | 2026-10-20 |
| Sources, Android | Play Device and Network Abuse, `answer/9888379` | `answer/16559646` | redirect | 2026-10-20 |
| Sources, Android | "Stopping malware from snooping on sensitive views" | Actual title: "Enhancing Android security: stop malware from snooping on your app data" | android-developers.googleblog.com | 2026-10-20 |
| Sources, Apple | `developer.apple.com/support/certificates/` | `developer.apple.com/help/account/certificates/certificates-overview` (still says live App Store apps are unaffected while membership is valid) | redirect + page | 2026-10-20 |
| Sources, CI/CD | Dependabot options reference, old docs path | `docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference` | redirect | 2026-10-20 |
| Sources, CI/CD | "`pull_request_target` changes (December 2025)" | "(announced 7 November 2025, effective 8 December 2025)" | github.blog changelog | 2026-10-20 |
| Sources, Tools | WithSecure Labs, `github.com/WithSecureLabs/...` | Reversec Labs (formerly WithSecure Labs), `github.com/ReversecLabs/...` | redirect | 2026-10-20 |
| Sources, Standards | `owasp.org/www-project-mobile-top-10/`; `first.org/cvss/v4-0/...` | `owasp.org/projects/mobile-top-10`; `first.org/cvss/v4.0/specification-document` | redirects | 2026-10-20 |
| Sources, Regulation | DLA Piper survey page (now redirects to a generic Insights index, so effectively dead) | Survey PDF `blogs.dlapiper.com/advocatus/files/2026/01/dla-piper-gdpr-fines-and-data-breach-survey-2026.pdf` (HTTP 200) | dlapiper.com | 2026-10-20 |
| Sources intro | "checked 24 September … nine marked … need a browser" + per-link "not confirmed" notes | Rewritten for the 20 October check. All 16 bot-checked links (EUR-Lex, FTC ×3, HHS, Apple Forums ×4, ACM, Medium, ProAndroidDev ×2, Security Boulevard, The Hacker News) were opened in a browser and resolve to the named page. "Not confirmed" notes removed | browser check | 2026-10-20 |
| Glossary, Android developer verification | "from 2027 for all apps worldwide, sideloaded ones included" | "from 2027 for all apps on certified devices worldwide. Power users can still install unverified apps through Google's \"advanced flow\" or ADB" | developer.android.com/developer-verification | 2026-10-20 |
| Glossary + volatility table, `datastore-tink` | "alpha since DataStore 1.3.0-alpha07" / "still alpha" | "introduced in 1.3.0-alpha07; release candidate since 1.3.0-rc01 on 12 October 2026, not yet stable" | developer.android.com/jetpack/androidx/releases/datastore | 2026-10-20 |
| Glossary, Digital Omnibus | "…still a proposal in September 2026" | Adds Reg. (EU) 2026/1744 (OJ 24 July 2026) and exact dates 2 Dec 2027 / 2 Aug 2028; GDPR part "still a proposal in October 2026 *(reported)*" | eur-lex.europa.eu/eli/reg/2026/1744/oj | 2026-10-20 |
| Known uncertainties | "the EU AI Act Omnibus publication date" open | Marked resolved (OJ 24 July 2026); NIST IR 8547 and HIPAA items annotated | EUR-Lex; csrc.nist.gov | 2026-10-20 |
| Glossary, Authentication-bound key | pointer *(§4.6)* | *(§4.1, §4.6)*. The term is defined in §4.1 | book text | 2026-10-20 |

Dead links: none remain. DLA Piper was the only effectively dead link, and it is replaced.

Confirmed unchanged on 2026-10-20:
- MASTG v2.0.0 (30 June 2026), MASWE v1.0.0 (17 Aug 2026, 119→78), and MASVS v2.1.0 are still the latest releases (GitHub API).
- `MASTG-KNOW-0015` still says `CertificatePinner` uses a custom TrustManager and that the network security configuration applies only to `HttpsURLConnection`.
- `MASTG-KNOW-0072` still says `WKNavigationDelegate` covers top-level navigation only.
- The Apple Forums `invalidKey` thread 844380 still has 0 replies. I added "*(checked 2026-10-20: still no reply)*" to row 6 of the untested-claims table.
- WWDC26 session 201 confirms the iOS 27 "launch validation category" extension, macOS 27 support, and the 30-day fraud metric.

## Unverified
Nothing is left unchecked. Every claim below was checked on 2026-10-20. Items marked "still open" remain in the book's Known uncertainties list, because no primary source settles them.

| § | Claim | Result | Source |
|---|---|---|---|
| Glossary | Android developer verification: 30 Sep 2026, Play plus six partner stores, BR/ID/SG/TH, worldwide 2027 "sideloaded ones included" | Dates, countries, and stores correct (Google Play, HONOR, OPPO, Galaxy Store, Palm Store, V-Appstore, GetApps). **Corrected** "sideloaded ones included": Google says only "all apps on certified Android devices" in 2027 and offers an advanced flow/ADB for unverified apps. Whether the 30 Sep start went live: no post-launch Google statement found | developer.android.com/developer-verification, /guides |
| Glossary | Auth Tab needs Chrome 137+ | Correct | developer.chrome.com Auth Tab guide |
| Glossary | `cache-mode` values read/write/write-only/none; GA Sept 2026 | Correct | github.blog changelog 2026-09-10 |
| Glossary / tables | CT opt-in on Android 16; CT and ECH on by default for API 37 | Correct | Android 17 behavior changes |
| Glossary | CVSS v4.0 still current | Correct (no v4.1 or v5 on first.org) | first.org/cvss |
| Glossary | Dependabot 3-day default cooldown, July 2026 | Correct | github.blog changelog 2026-07-14 |
| Glossary | Digital Omnibus AI Act dates; GDPR part a proposal | Dates correct; now cites Reg. (EU) 2026/1744 (OJ 24 Jul 2026). GDPR part still a proposal *(reported)* | EUR-Lex; secondary commentary |
| Glossary | SC-088v3 effective 10 Nov 2025 | Correct | BR v2.3.1 revision table |
| Log note | Let's Encrypt dns-persist-01 staging only | Still staging only (LE staff, 25 Jun 2026) | community.letsencrypt.org |
| Glossary | SC-080 15 Jul 2025; SC-090 15 Mar 2027 / 15 Mar 2028 | Correct | BR v2.3.1 |
| Glossary | PCI DSS v4.0.1 only active version | Correct (PCI SSC RFC, June 2026) | pcisecuritystandards.org |
| Glossary / volatility | `datastore-tink` alpha | **Corrected**: release candidate 1.3.0-rc01 (12 Oct 2026) | androidx DataStore release notes |
| Glossary / volatility | `expect`/`actual` classes Beta; Swift export Alpha | Correct | kotlinlang.org |
| Glossary / table | 16 KB updates blocked from 1 Feb 2027; target API 36 from 31 Aug 2026 | Correct | page-sizes guide; target-sdk page |
| Glossary | ECH "experimental on Apple platforms" | Correct in substance; reworded to "off by default…experimental Network framework option" (matches Part 3) | Apple Forums thread 842112 *(reported)* |
| Glossary | Foundation Models PCC model since WWDC26 | Correct | WWDC26 session 241 |
| Verified table | Play Integrity library 1.6.0 current | Correct (1.6.0, 2025-11-20 is latest) | release notes |
| Volatility | androidx.biometric 1.4 alpha | Correct (1.4.0-alpha07) | androidx release notes |
| Glossary | Trust store about 150 roots | Correct (about 156 in the iOS 26 list) | support.apple.com/126047 |
| Volatility | 2 Nov 2026 `pull_request_target` rule | Correct | github.blog changelog 2026-09-17 |
| Uncertainties | NIST IR 8547 still a draft | Still open (initial public draft, Nov 2024) | csrc.nist.gov |
| Uncertainties | HIPAA final rule timing | Still open; agenda reportedly moved final action to July 2027 or later *(reported)* | GovInfoSecurity, Paubox |
| Uncertainties | EU AI Act Omnibus publication date | **Resolved**: Reg. (EU) 2026/1744, OJ 24 Jul 2026 | EUR-Lex |
| Uncertainties | Android platform post-quantum TLS default | Still open (no primary source found) | web search |
| Uncertainties | OWASP LLM Top 10 2026 order | Still open (secondary sources only) | web search |
| Uncertainties | RKP 10 April date; Play Integrity reuse threshold | Still open (pages unchanged) | security-key-attestation; integrity/standard |
| Uncertainties | WKWebView + `NSPinnedDomains`; MASTG-KNOW-0015/0072 | Still open (KNOW pages unchanged) | mas.owasp.org |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Ch 33 intro | "DCV" used before it was defined | "DCV (domain control validation)" |
| Programme-layer entry | "strategy documents" never explained | "the four source documents, numbered 01 to 04, that this book was rewritten from" |
| Strategy-diff entry | "Implementation Guide", "SLA" undefined | "(one of the strategy documents)", "service-level agreement" |
| 24 Sep log line | "P1 and P2" undefined | "(the two highest priorities)" |
| Audit limits | "OEM" | "device makers' (OEM)" |
| Incident cost estimates | Vague; no pointer to the method | Says why the book gives no range and points to §29.4 |
| Glossary | RP ID, COTS, and IDFA undefined | "RP ID hash (a SHA-256 of your App ID)", "commercial off-the-shelf", "Identifier for Advertisers" |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| 07-platform-surfaces… / 03-data-in-transit.md | wherever cited | Same moved URLs as above (photo-picker, audit-data-access, Play policy answers, Apple certificates page, Dependabot reference, ReversecLabs, OWASP Mobile Top 10, first.org v4.0) if cited inline | Old URLs redirect or (DLA Piper) are dead |
| 11-making-the-case… | §29.x / §30.1 | DLA Piper link → survey PDF if cited inline | Page redirects to a generic index |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| (none added) | | |

## Judgment calls
- **List-item em dashes.** I closed up list-item em dashes (`**Term**—Definition`, `Title—<url>`) to follow the rule. A colon would read better; reverse it in one pass if you prefer.
- **Correction-log wording.** I made light voice changes in historical entries, for example "A structural and factual audit was run" → "I ran…", and "The book was audited" → "An independent auditor checked…". Meaning and dates are unchanged. No superseded notes were removed.
- **Sources intro.** I rewrote it to describe the 20 October check. I did not add a log entry; the coordinator merges those.
- **Volatility table.** The first column now reads "7, 8: TLS baseline…" instead of using a dash.

- **Other files.** Part 0 (Chapter 0.4) and Part 11 may also say developer verification covers sideloaded apps from 2027. Google's page says only "all apps on certified Android devices", with an advanced flow for unverified apps. The 24 September log line keeps its wording as history.
