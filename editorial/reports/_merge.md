# Cross-file merge (2026-10-20)

This file applies the "Needs a change in another file" and "New glossary terms" sections from every report in `editorial/reports/`. `python3 scripts/check.py` reports 0 problems after the merge.

## Counts

| | Before | After | Where the count is stated |
|---|---|---|---|
| Glossary terms | 210 | 252 (42 added, 6 edited, 1 pointer fixed) | README.md (lines 7 and 30). book/start-here.md and book/12-verification.md state no current count; the 24 September audit row (12, line ~242) and CHANGELOG.md are history and were left alone |
| Sources | 278 stated (279 actual after the Part 12 agent added EUR-Lex 2026/1744) | 284 | README.md line 30, VERIFICATION.md line 21 |

How sources are counted: list items under `## Sources`, excluding "Removed in the September 2026 audit" (9) and "Books" (2). This rule reproduces the old figure of 278 from the stale `dist/` build.

## Items

| From report | Target file | § | Change | Status |
|---|---|---|---|---|
| all | CONTRIBUTING.md | Style | British vs American | Skipped: already handled |
| 01 | 12-verification.md | Glossary | Add CWE, Interception proxy, MCP | Applied (§3.1; §1.1, §7.1; §2.2). "Intercepting proxy" (01) and "Interception proxy" (03) were merged into one entry |
| 01, start-here | 12-verification.md | Glossary | Trust boundary | Skipped: entry already exists *(Chapter 0.5)* |
| 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 00 | 12-verification.md | Ch 33 log | Add 2026-10-20 log entries | Skipped: coordinator owns this |
| 01 | 09-the-catalogues.md | Ch 27 (line ~149) | Note that the v1.0.0 announcement counted 36 at release | Applied, with a pointer to §3.1 |
| 01 | 10-questions-and-answers.md | lines 74, 940 | ADA now hosted by the Linux Foundation | Applied at line 940 ("Google's App Defense Alliance" → founded by Google, now hosted by the Linux Foundation; source: Linux Foundation press release, Nov 2023). Line 74 was already neutral |
| 02 | 12-verification.md | Glossary `AeadSerializer`, volatility table | datastore-tink rc01 | Skipped: the Part 12 agent had already applied it |
| 02, 10 | 12, 10, 02 | — | "Key Attestation CA1" | Skipped: already handled |
| 02, 00 | dist/ | — | Rebuild | Skipped: coordinator owns this |
| 02 | 12-verification.md | Glossary | Add `expectedAttestationApplicationId`, Side-channel attack | Applied (§5.5, §4.2) |
| 02, 09 | 12-verification.md | Glossary | Step-up authentication | Skipped: entry already exists |
| 03 | 12-verification.md | Glossary DNS-PERSIST-01 | 10-day re-check | Skipped: already handled |
| 03, 00 | 12-verification.md | Glossary | American spelling | Already done by the Part 12 agent; a scan found no British spellings left in the glossary |
| 03 | 12-verification.md | Sources | Add MASWE-0028, OkHttp changelog, RFC 7518 | Applied (all return HTTP 200) |
| 03 | 12-verification.md | Glossary | Baseline Requirements, CA/Browser Forum, Bootstrap pins, Interception proxy, MDM, Root program, HSM | Applied (§8.5, §8.5, §8.6, §1.1/§7.1, §7.1, §7.3, §8.6) |
| 04 | 12-verification.md | Sources | WithSecure → Reversec | Already done; the inline link in Part 4 was already correct |
| 04 | 12-verification.md | Sources | Two Apple forum threads; Play Integrity error codes | Forum threads 739323 and 844380 were already listed. Error-codes page added |
| 04 | 12-verification.md | Glossary | Hardware auth token, Launch validation category | Skipped: entries already exist |
| 04 | 12-verification.md | Glossary | DPoP proof | Skipped: the DPoP entry already defines the per-request proof |
| 05 | 12-verification.md | Glossary Obfuscation | Pointer §14.3 → Chapter 14 intro | Applied: *(Chapter 14)* |
| 05 | 12-verification.md | Glossary | Tamper detection, Control-flow flattening, Minification, JDWP, dm-verity | Applied (Chapter 14, Chapter 14, §14.1, §14.4, §14.4) |
| 06 | 12-verification.md | Glossary `cache-mode` | Confirm the GA date | No change: the Part 12 agent confirmed GA in September 2026 (GitHub changelog, 2026-09-10). The entry doesn't list triggers, so nothing was added |
| 06 | 12-verification.md | Glossary SLSA | L3 includes cache-poisoning isolation | Applied. Verified at slsa.dev/spec/v1.2/build-requirements ("MUST NOT be possible for one build to inject false entries into a build cache used by another build") |
| 06 | 06 frontmatter | recheck_because | Optional lockfile/execution-protections mention | Skipped: no fact in the field is wrong |
| 06 | 12-verification.md | Glossary | Workflow lockfile, Workflow execution protections, Keep rule, Hybrid signing (Play) | Applied (§15.3, §15.3, §15.8, §15.6) |
| 07 | 12-verification.md | Glossary Embedding | §20.2 | Skipped: already handled |
| 07 | 07 frontmatter | recheck_because | "behaviour" → "behavior" | Applied |
| 07, 09, 00, start-here | headings | — | British spellings in headings | Skipped: headings are frozen |
| 07 | 03-data-in-transit.md | §8.6 | WKWebView + NSPinnedDomains | Skipped: already handled (stays as written) |
| 07 | 12-verification.md | Glossary | Eval set, Dirty Stream, Attribution tag | Applied (§20.7, Chapter 17/§17.2, §18.4). `expect`/`actual` already exists |
| 08 | 12-verification.md | Glossary Conscrypt APEX | Bind-mount workaround, lasts until reboot | Applied |
| 08 | 12-verification.md | Glossary | Bootrom (checkm8), Zygote, Modes of Introduction | Applied (§22.1, §22.1, §23.1) |
| 09 | 09 frontmatter | recheck_because | "neighbouring" → "neighboring" | Applied |
| 10 | 02-data-at-rest.md | §6.3 | datastore-tink rc01 | Already correct (rc01, 12 October 2026) |
| 10 | 03-data-in-transit.md | §8.2 | Name the answer's author | Skipped: optional, and the reporting agent says the current text is accurate |
| 10 | 04-proving-who-is-calling.md | §9.2 Trap | Optional verdicts → `UNEVALUATED` or empty | Applied. Source: developer.android.com/google/play/integrity/standard |
| 10 | 04-proving-who-is-calling.md | §9.4 | For client-side exceptions, the app picks the dialog | Applied, with a link to the remediation page |
| 10 | 04-proving-who-is-calling.md | §10.3 | `isSupported` → a spike in unsupported responses on a supported platform | Applied (WWDC26 Session 201) |
| 10 | 02-data-at-rest.md | §4.2 | CDD wording limited to devices with a dedicated secure processor | No change: the text already says so |
| 11 | 12-verification.md | Glossary Android developer verification | Android 7+; seven stores | Applied "certified Android 7+ devices" to the 2026 phase (developer.android.com/developer-verification). The entry already named Play plus six stores |
| 11 | 12-verification.md | Glossary Gate (programme) | → program | Already done ("Gate (program)") |
| 11 | 04-proving-who-is-calling.md | §10.1 | "Assertions don't contact Apple": cite a source or mark it | Applied *(reasoned)*. Apple's integrity guide says only `attestKey` "accesses a remote Apple server" and doesn't mention a server for assertions. Linked |
| 11 | 12-verification.md | Glossary | MVP, Tabletop exercise, Tokenization (payments), Addressable (HIPAA), Certified device | Applied (§32.7, §32.5, §30.1, §30.1, §32.7) |
| 12 | 01, 07, 08, 11 | inline links | Moved URLs | Applied: 01 OWASP Mobile Top 10 → owasp.org/projects/mobile-top-10. 07 Play answer 14115180 → 16935362, audit-access → privacy-and-security/audit-data-access, Play answer 9888379 → 16559646. 08 Apple certificates → help/account/certificates/certificates-overview. 11 DLA Piper → survey PDF. All return HTTP 200. No inline photopicker, first.org v4-0, or old Dependabot paths remain. WithSecure mentions in 04 and 10 are prose ("formerly WithSecure Labs"), with Reversec links |
| 12 (judgment) | 00-foundations.md §0.4, 11 §29 table | — | "sideloaded ones included" for 2027 | Skipped: Google's page says "all apps on certified Android devices" and offers an advanced flow so power users can sideload unverified apps, which implies sideloaded apps are covered. The Part 0 agent also confirmed the wording |
| VERIFICATION | 07-platform-surfaces… | Ch 20 | Cite the OWASP LLM Top 10 2026 directly if public | Applied. The final text is public at github.com/GenAI-Security-Project/GenAI-LLM-Top10 (2026/final), and its order matches the §20 table. §20.4 LLM06 rationale: *(reported)* replaced with the primary's reasons. §20.5 LLM07 rationale and the "same model" point: *(reported)* replaced with the 2026 text (LLM03, LLM07). Added to Sources. Known uncertainties item marked resolved. VERIFICATION.md "Gated primary sources" updated |
| VERIFICATION | VERIFICATION.md | Last full audit | — | Skipped: coordinator owns this |
| start-here | 12-verification.md | Glossary | Hardware-backed key | Applied (§4.1) |
| 00 | 12-verification.md | Glossary Refresh token rotation | Reuse detection revokes the active token (RFC 9700 §4.14.2) | Applied. Reuse detection is folded into this entry, not given its own |
| 00 | 12-verification.md | Glossary Argon2id | bcrypt is for legacy systems only | Applied (OWASP Password Storage Cheat Sheet) |
| 00 | 02-data-at-rest.md | §4.3 | Keychain vs Secure Enclave key distinction as in Ch 0.4 | Applied. §4.3 didn't contradict Ch 0.4, but it never said that a Keychain secret is returned to your process. I added one paragraph: securityd returns the decrypted `kSecValueData`, and only Secure Enclave keys never enter the process |
| 00 | 12-verification.md | Glossary | Control, Defense in depth, Replay, Padding oracle, Hybrid encryption, Memory-hard function, Non-repudiation, Authorization server, Credential stuffing, Forward secrecy | Applied (Chapter 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2, 0.3, 0.6, 0.4) |
| 00 | 12-verification.md | Glossary | Reuse detection, Certificate Transparency | Reuse detection is folded into Refresh token rotation. CT already exists |

## Notes
- New glossary entries were inserted in alphabetical order without reordering existing entries. One pre-existing order quirk is unchanged: "CIA triad" comes before "CI/CD".
- Every glossary pointer was machine-checked against the section headings in book/*.md. None are missing.
- New sources: MASWE-0028, RFC 7518, OkHttp changelog, Play Integrity error codes, and the OWASP LLM Top 10 2026 full text on GitHub.
