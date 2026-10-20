# book/11-making-the-case-and-running-the-programme.md

## Summary
- Words before / after: 8,483 / 9,545. Nearly all of the growth is plain-language definitions, so that executives can read this part on its own.
- Edits: clarity 48, filler 9, voice 42, spelling 31, explanation 47, code 0
- Facts checked: 74 · correct 60 · corrected 11 · unverified 3

All four passes covered the whole file. `python3 scripts/check.py` reports 0 problems. `last_verified` is now 2026-10-20. `recheck_because` is unchanged: every item in it still holds.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| 29.5 | Breaches lasting more than 200 days "cost about a third more" | "cost nearly a third more (about 31%)" ($5.65M vs $4.32M) | https://www.bakerdonelson.com/ten-takeaways-from-ibms-2026-cost-of-a-data-breach-report | 2026-10-20 |
| 29.2 | "Commits co-authored by **Claude Code**" | "Commits made with **Claude Code**" (GitGuardian says "Claude Code-assisted commits"); the explanation of the co-author line is kept in the following paragraph | https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/ | 2026-10-20 |
| 32.7 | "Standard requests after warm-up do not count against the request quota… Request an increase through the form Google links from Play Console" | Warm-ups count against the token-request quota and the standard requests that follow don't; the increase form is linked from Google's setup page, not from Play Console | https://developer.android.com/google/play/integrity/setup | 2026-10-20 |
| 32.5 #3 | "apps ignore user CAs by default since Android 7" | "apps that target Android 7, API level 24, or later ignore user-installed CAs by default" (the behavior depends on targetSdkVersion, not on the device's OS version) | https://developer.android.com/privacy-and-security/security-config | 2026-10-20 |
| 30.1 GDPR | Only the 4% / €20M fine tier was given | Added that breach-notification failures (Articles 33 and 34) fall in the lower 2% / €10M tier, Art. 83(4) | https://eur-lex.europa.eu/eli/reg/2016/679/oj | 2026-10-20 |
| 30.1 GDPR | Digital Omnibus 96-hour proposal "is not law *(reported)*" | Proposal of November 2025 (COM(2025) 837), still awaiting a committee decision in Parliament; primary link added, marker removed | https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0360(COD) | 2026-10-20 |
| 30.1 CRA | Final report "one month (incidents)" | "within one month of the notification (incidents)" (Art. 14(4)(c) counts from the 72-hour notification, not from awareness); EUR-Lex link added | https://eur-lex.europa.eu/eli/reg/2024/2847/oj | 2026-10-20 |
| 30.1 NIS2 | "final report within one month"; "Fines up to €10 million or 2%… €7 million or 1.4%" | Final report within one month of the notification (Art. 23(4)); the fine amounts are minimums for each country's maximum ("maximum fines of at least…", Art. 34(4)–(5)) | https://eur-lex.europa.eu/eli/dir/2022/2555/oj | 2026-10-20 |
| 30.1 AI Act | Omnibus described only as moving the high-risk dates; secondary source only | Added that the Omnibus also created new prohibitions that apply from 2 Dec 2026; added the EUR-Lex link for Regulation (EU) 2026/1744 | https://eur-lex.europa.eu/eli/reg/2026/1744/oj | 2026-10-20 |
| 30.1 HIPAA | "HHS's 2026 agenda moved it to the long-term actions list… *(reported)*" | Primary reginfo.gov citation added (Long-Term Actions, final action 07/2027); marker removed | https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=0945-AA22 | 2026-10-20 |
| 32.7 takeaways | "Every phase ends at a gate of testable success criteria." | "Every phase has testable success criteria, and Phases 1 and 2 end at a gate…" (the old text contradicted §32.1 and Figure 27) | Internal consistency | 2026-10-20 |

Date and tense updates that don't change any fact: "as of September 2026" became "October 2026" in §29.2 and in the §30.1 status column. Android developer verification "starts" became "started" / "since" (30 Sep 2026 has passed), and the executive-summary row is now marked "(in force)".

Confirmed correct (abbreviated):
- **IBM 2026:** $4.99M; +12%; $11.5M US; $6.64M healthcare, 13th year; $6.3M financial; 247 vs 241 days; 1 in 4 AI-enabled breaches, +56%, $6M; ransomware 39% vs 34%; 52% / $192; 41% reputation threats; 602 orgs; 29 Jul 2026; 2024 $4.88M; 2025 $4.44M.
- **Verizon 2026:** 19 May; 31% / 19 years; 48% third parties; mobile scams 40% more successful.
- **GitGuardian 2026:** 17 Mar; 28.65M, +34%; 64%; 3.2% vs 1.5%.
- **CloudSEK:** 3,207 and 230.
- **Settlements and penalties:** Capital One $190M (final 13 Sep 2022) plus OCC $80M (Aug 2020); T-Mobile $350M (final 29 Jun 2023) plus $150M; Equifax $575M–$700M.
- **GDPR:** Meta €1.2B (DPC, May 2023); €7.1B cumulative (DLA Piper); Arts 33, 34 and 83.
- **CRA:** 11 Sep 2026 and 11 Dec 2027; Art. 69(3); 24h / 72h / 14 days; €15M / 2.5%; SBOM; secure by default.
- **DORA:** 17 Jan 2025; 4h / 24h (Delegated Reg. 2025/301).
- **NIS2:** 17 Oct 2024; IP/26/1499 of 8 Jul 2026 (IE, ES, FR, NL).
- **AI Act:** 2 Feb 2025; 2 Aug 2025; 2 Aug 2026; 2 Dec 2026 (Art. 111(4)); 2026/1744 in force 27 Jul 2026; 2 Dec 2027 / 2 Aug 2028.
- **PCI DSS:** v4.0.1 only (v4.0 retired 31 Dec 2024); 51 requirements from 31 Mar 2025; MPoC; no v5 published.
- **FTC HBNR:** 29 Jul 2024.
- **Google Play:** target API 36 from 31 Aug 2026, API 35 for existing apps, extension to 1 Nov 2026, lower minimums for Wear OS, TV, Automotive and XR; Data safety 2022.
- **Android developer verification:** 30 Sep 2026; four countries; Play plus six partner stores; 2027 global; advanced flow.
- **Apple:** 1 May 2024 required reasons; Xcode 26 from 28 Apr 2026; iOS 13 minimum target from 9 Sep 2026; App Attest ~100/s and 10M users a day, no assertion limit.
- **Other platform facts:** Play Integrity 10k/10k/day and 5/min classic; latencies (a few hundred ms, a few seconds); CA/B Forum SC-081v3, 47 days from 15 Mar 2029; MASTG-TEST-0206 title and current status; MAS-L1/L2 profiles; AAB `base/dex/`.
- **Arithmetic:** the worked example in §29.4 adds up ($61,200).
- **Cross-references:** every `§` and Chapter reference resolves to the right heading.

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| 32.7 | App Attest assertions are generated on the device with no round trip to Apple | Apple's App Attest pages say attestation contacts Apple's server, but don't say outright that assertions don't; the Establishing-integrity page renders without body text | *(reasoned)*, added |
| 29.3 | DLA Piper January 2026 survey link and the €7.1bn figure | The figure is confirmed by search summaries; the /en-us/ URL returned HTTP 429 and /en/ rendered empty | Kept as is; recheck the link (the /en/ path may be safer) |
| 29.3 | "Meta appealed" (still true); the current outcome of the appeal | Found the 2023 High Court stay; found no final outcome | No marker needed for the text as written |

Also sourced only from secondary summaries, not IBM's own pages: healthcare's 13th year, 247 vs 241 days, 52% / $192, the >200-day figure, and the 2025 "first decline in five years". These are consistent across Baker Donelson, Integrity360, Paubox and CyberScoop. The existing *(reported)* markers stay.

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Exec summary | Jargon an executive meets on page one | Plain definitions of API key, build pipeline, session token, hardware-backed storage, step-up authentication, reverse engineering, CRA and MVP; the phase table now describes outcomes in plain words |
| 29.1, 29.2 | Target level, "hidden" endpoints, rotation, passkeys | One-clause definitions |
| 29.3, 29.4 | Certificate pinning, rooted/jailbroken, GDPR, supervisory authority, refresh token, FTC/CFPB | Defined at first use |
| 30.1 | SDK, tokenization, acquirer, MFA, MPoC/COTS, PHI "addressable", SOC 2, ICT, ENISA, SBOM, PCI DSS, HIPAA, DORA, NIS2 expansions; GDPR minimization and purpose limitation | Defined inline |
| 30.2 | MASTG and PII | Expanded |
| 31.1, 31.2 | Attestation, defense in depth, OWASP, obfuscation | Defined at first use |
| 32.2 | The "terms" paragraph covered only four terms | Turned into a bulleted glossary that adds CI, Keystore/Keychain, Secure Enclave, verdict, risk scoring, and hooking/tamper detection |
| 32.3 | Why shorter certificate lifetimes raise maintenance for pinned apps | One sentence: each renewal is a chance for a pinned app to stop connecting |
| 32.5, 32.6 | ATS, CA, Frida, tabletop exercise, MAS-L1, APK/AAB/DEX, threat model | Defined inline |
| 32.7 | Custom ROM, certified device, package name, critical path, standard vs classic request | Defined inline |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| CONTRIBUTING.md | Style | Says "British spelling in prose"; the editorial prompt requires American | The two rules conflict. I followed PROMPT.md; the house style should be updated to match |
| book/12-verification.md | Chapter 33 audit log | Add a dated entry for the corrections above | CONTRIBUTING step 2 |
| book/12-verification.md | Glossary: Android developer verification | Consider adding "on certified devices running Android 7+"; Google lists 7 participating stores (Play plus six) | Precision, per developer.android.com/developer-verification/guides |
| book/12-verification.md | Glossary: "Gate (programme)" | Spell it "program" if the book moves to American spelling (keep the anchor stable) | Spelling consistency |
| book/04-proving-who-is-calling.md | §10.1 | Cite a primary source for "assertions don't contact Apple", or mark it *(reasoned)* | Couldn't confirm it in Apple's docs |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| MVP (minimum viable product) | The first version of a product you release to learn whether it works | §32.7 |
| Tabletop exercise | A rehearsal in which the team talks through an incident step by step | §32.5 |
| Tokenization (payments) | A payment provider holds the card number and gives your app a substitute token, which takes most PCI DSS scope off the app | §30.1 |
| Addressable (HIPAA) | A safeguard you implement, or document why it isn't reasonable and what you do instead | §30.1 |
| Certified device | An Android device that passes Google's compatibility tests and ships with Google Play | §32.7 |

## Judgment calls
- **Phase labels.** "1 — Foundations" became "1: Foundations" in both phase tables, to match the Mermaid nodes and the rule on closed-up em dashes. The heading "§29.4 … — do this instead of quoting averages" keeps its spaced em dash, because headings are frozen.
- **"programme".** It stays in the H1 heading and the filename; prose uses "program".
- **Length.** The definitions make the executive summary longer than "one page". I kept them as short parentheticals rather than a separate glossary box, so the summary still stands alone. Cut them if the author wants a strict one-pager and accepts the forward references.
- **Quoted speech.** "We" and "our" stay inside quoted objections and the scripted sentence in §29.4. These are words the reader or stakeholder says, not author voice.
- **"about 100 requests per second".** Kept the "about" (Apple says "fewer than 100") for consistency with §10.5, which notes that the threshold fluctuates.
- **Meta fine row.** Left under "Regulatory penalty" with its existing caveat. No change.
