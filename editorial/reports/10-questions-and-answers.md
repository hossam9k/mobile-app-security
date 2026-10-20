# book/10-questions-and-answers.md

## Summary
- Words before / after: 18,027 / 18,643 (definitions, hedges, and a few nuances added)
- Edits: clarity 78, filler 9, voice 64, spelling 38, explanation 27, code 0
- Facts checked: 268 · correct 233 · corrected 21 · unverified 14

Every one of the 156 Q&As was read in Pass 2 and Pass 4. I opened each `Taught in §…` target in the source chapter and confirmed it teaches the topic. All 156 pointers are correct, and none was changed. Difficulty tags are unchanged. Four questions that depended on the previous question, or were fragments, now stand alone. `last_verified` is set to 2026-10-20. `scripts/check.py` reports 0 problems.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| Storage and keys (auth token on Android; `datastore-tink`) | `datastore-tink` "still alpha" / "still alpha at 1.3.0-alpha11 in September 2026" | Release candidate 1.3.0-rc01 since 12 October 2026, not yet stable | https://developer.android.com/jetpack/androidx/releases/datastore | 2026-10-20 |
| Foundations (OAuth) | "RFC 9700 says to use `S256`, never `plain`" | RFC 9700 tells clients to use a challenge method that doesn't expose the verifier, and `S256` is currently the only one, so never use `plain` | https://www.rfc-editor.org/rfc/rfc9700 §2.1.1 | 2026-10-20 |
| Foundations (RFC 9700 / DPoP) | The DPoP proof covers "a hash of the access token" | It does so only when the request carries an access token (`ath`) | https://www.rfc-editor.org/rfc/rfc9449 | 2026-10-20 |
| Key attestation (2026 root), Design review (verifier rejects phones) | "Key Attestation CA 1" | "Key Attestation CA1" (the certificate CN has no space) | https://developer.android.com/privacy-and-security/security-key-attestation (decoded root certificate) | 2026-10-20 |
| Key attestation (2026 root) | Verifiers trusting only RSA "started rejecting most modern Android phones" right after 1 Feb | Rejection followed RKP devices' reported exclusive switch on 10 April; the February date is when signing began | Same, plus §5.3 | 2026-10-20 |
| Key attestation (RKP) | "mandatory from Android 13" stated flatly | Mandatory per Google's 2022 announcement; Google's attestation page now calls RKP support optional under the Android 15 policy (matches §5.3) | https://android-developers.googleblog.com/2022/03/upgrading-android-attestation-remote.html ; https://developer.android.com/privacy-and-security/security-key-attestation | 2026-10-20 |
| Storage and keys (Keychain class) | "`AfterFirstUnlockThisDeviceOnly` …, and Apple names that use case" | Apple names background refresh for `AfterFirstUnlock`; `ThisDeviceOnly` adds the no-migration property | https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web | 2026-10-20 |
| Storage and keys (TEE vs StrongBox) | "the Android 17 CDD still only strongly recommends it" | …and only for devices with a dedicated secure processor | https://source.android.com/docs/compatibility/17/android-17-cdd §9.11.2 | 2026-10-20 |
| Foundations (root detection) | `MASTG-DEMO-0108` "demonstrates a detection check being defeated" (beside a root-check example) | Shows a Frida-detection check bypassed | https://mas.owasp.org/MASTG/demos/android/MASVS-RESILIENCE/MASTG-DEMO-0108/MASTG-DEMO-0108/ | 2026-10-20 |
| Storage and keys (Keychain) | "two AES-256-GCM keys per item" | "two AES-256-GCM keys": a metadata (table) key, plus a per-row secret key | https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web | 2026-10-20 |
| Foundations (Top 10 vs MASVS) | MASVS v2.1.0 "still current in September 2026" | "still current in October 2026" | https://github.com/OWASP/masvs/releases | 2026-10-20 |
| Network (should you pin) | "an OWASP MAS maintainer read it as 'a complicated procedure'" | "an answer the MAS project lead accepted in the MASVS discussions read it as…". The author, mkk7ns, is not labelled a maintainer; cpholguera accepted the answer | https://github.com/OWASP/masvs/discussions/573 | 2026-10-20 |
| Attestation (empty verdicts) | Opted-in optional verdicts "are cleared too" | They come back `UNEVALUATED`, or empty for multi-value verdicts | https://developer.android.com/google/play/integrity/standard | 2026-10-20 |
| Attestation (rollout) | "Your server chooses the dialog code, because only your server can read the verdict" | The server chooses for verdict problems; for remediable client-side exceptions, the app shows `GET_INTEGRITY` itself | https://developer.android.com/google/play/integrity/remediation | 2026-10-20 |
| Attestation (what's new in App Attest) | "treat an unexpected `isSupported == false` as a possible tampering signal" | A spike of `isSupported == false` from a user on a platform that supports App Attest | https://developer.apple.com/videos/play/wwdc2026/201/ | 2026-10-20 |
| Attestation (attest once) | "Apple's rule is once per key, not per request" | Removed the "not per request" contrast. Apple's text is "typically … once per user per device"; §10.5's actual contrast is per key versus per installation | https://developer.apple.com/documentation/devicecheck/preparing-to-use-the-app-attest-service | 2026-10-20 |
| Biometrics (stolen phone), Storage (key conditions), Design review (device PIN) | `AUTH_DEVICE_CREDENTIAL` "silently switches enrolment invalidation off" (flat) | Validity window: documented. Device credential: outside Google's documented guarantee *(reasoned)*, matching §11.3 | https://developer.android.com/reference/android/security/keystore/KeyGenParameterSpec.Builder (setInvalidatedByBiometricEnrollment) | 2026-10-20 |
| Pipeline (AI-assisted coding) | Commits "co-authored by" Claude Code; "eight of the ten fastest-growing leaked-secret categories" | "made with" Claude Code; "eight of the ten fastest-growing secret detectors were tied to AI services" | https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/ | 2026-10-20 |
| Judgment (programme squeezed) | "Each phase ends at a gate" | Each phase delivers something testable; only Phases 1 and 2 end at a gate (§32.1) | Book §32.1–§32.2 | 2026-10-20 |
| Pipeline (SHA pinning) | Immutable releases stop tag changes (unqualified) | They don't cover floating major-version tags such as `v7` (matches §15.3) | §15.3; https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/ | 2026-10-20 |
| Pipeline (`pull_request_target` tightened) | The checkout v7 backport is unqualified; the 2 Nov rule's scope is unstated | The backport reaches floating major tags only (SHA or minor pins don't get it). The rule covers public repos only, not private or internal | https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout ; https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/ | 2026-10-20 |

Also confirmed correct with primary sources this pass (sample): MASVS 8/24, MAS profiles, MASWE 119→78 (17 Aug 2026), MASTG v2.0.0 (30 Jun 2026), NIST SP 800-38D 2³², RFC 8252/9700 MUST/SHOULD wording, Jetpack Security deprecation dates and "nothing since 1.1.0", `_androidx_security_master_key_`, Tink cleartext fallback, KeyInfo constants, StrongBox algorithms, `errSecInteractionNotAllowed` −25308, iOS 26 SecureEnclave ML-KEM/ML-DSA, `KeyStoreManager.grantKeyAccess()`, attestation OID and revocation-list format, SC-081v3 schedule and vote, BR 6.3.2/4.2.1, SC-088 persistent DCV, NSC/OkHttp/iOS pin formats, `debug-overrides` behavior, MASTG-TEST-0284, Play Integrity latencies, quotas, opt-in labels, LEVEL_4 thresholds, May 2025 criteria and 14.5%/0.4%, remediation 1.5.0, App Attest rate limits, DCError rule, 30-day risk metric and receipt refresh, WWDC26 Session 201 guidance, MASWE-0020/21/22, MASTG-BEST-0031/0038, MASTG-TEST-0326/0328/0330, `setConfirmationRequired` default, `domainState` iOS 18, Dependabot 3-day default (14 Jul 2026) and `default-days`-only for actions, cache-mode GA (10 Sep 2026), TanStack 84/42, trivy-action 76/77, npm trusted publishing GA (31 Jul 2025), SHA-pinning policy (15 Aug 2025), developer verification (dates, countries, seven stores, 99%), GitGuardian 2026 figures, IBM 2026 figures, Android 17 content-capture change, KMP survey/Stable/Beta/Alpha statuses, `cryptography-kotlin` 0.6.0, Ktor `usePreconfiguredSession` ignoring `handleChallenge`, Remote Config real-time listener behavior.

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| Foundations (MASVS L2) | Profiles were "reworked during the 2026 MASWE refactor" | mas.owasp.org/Profiles shows per-MASWE requirements, which fits, but I found no announcement | Keep; consider *(reported)* |
| Key attestation | RKP devices switched exclusively to the new root on 10 April 2026 | Google's docs give only 1 Feb; community sources only | Already "reportedly"; keep |
| Key attestation | No date yet for a post-quantum root | Nothing found | Keep (absence claim) |
| Storage (WhenUnlocked) | checkm8 forensics recover only `Always` items before first unlock | Vendor (Elcomsoft) reports only | *(reported)*, added |
| Storage (ESP deprecation) | Reasons (OEM inconsistency, StrictMode, keyset corruption) | Practitioner reports only | *(reported)*, added |
| Attestation (DCError) | ~0.01% of one app's users fail `invalidKey` permanently | Apple forum thread 844380 (Sept 2026, 0 replies; ~30 of ~360,000 users) | *(reported)*, added |
| Network (NSC / WebView) | The book's Android 17 emulator and iOS 26.5/27.0 simulator results | The book's own tests; no Apple statement exists | Keep as stated (labelled as the book's test) |
| AI (OWASP LLM 2026) | Full 2026 ranking (LLM03 Excessive Agency … LLM10 Improper Output Handling) | The genai.owasp.org resource page confirms the 3 Aug 2026 release, but its list page still shows 2025; I took the ranking from the CSA research note and other coverage | *(reported)*, added |
| AI (model wrong) | The 2026 edition says the checker shouldn't be the proposing model | Not found in secondary coverage; couldn't read the PDF | *(reported)*, added |
| AI (indirect injection) | EchoLeak details | NVD confirms the CVE; the attack narrative is from researchers | *(reported)*, added |
| Pipeline (SHA pinning) | Megalodon 5,718 commits / 5,561 repos / ~6 h | SecurityWeek, SafeDep, CSA (secondary) | *(reported)*, added |
| Pipeline (`pull_request_target`) | TanStack OIDC-from-memory, 84/42 | The TanStack post-mortem confirms 84/42; the mechanism detail is from secondary analyses | *(reported)*, added |
| Pipeline (SLSA) | TanStack packages carried valid SLSA L3 provenance | Snyk and StepSecurity only | Already *(reported by Snyk and StepSecurity)* |
| Pipeline (SHA pinning) | Immutable releases GA October 2025 | Only a secondary source (Classmethod) gives 28 Oct 2025 | Keep; low risk |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Foundations (AES-GCM) | Nonce undefined at first use | One-line definition |
| Foundations (OAuth) | PKCE not expanded | Expansion, plus what the verifier is |
| Foundations (Top 10 vs MASVS) | MAS not expanded | "OWASP Mobile Application Security (MAS)" |
| Storage (Keystore internals) | Binder and TA undefined | Short glosses |
| Storage (TEE/StrongBox) | TEE and CDD not expanded | Expansions |
| Storage (`datastore-tink`) | AEAD undefined | Gloss |
| Key attestation | RKP used before being expanded; keybox undefined | Expansion and gloss |
| Network | CA, CT, ECH, SPKI, ClientHello, ACME, and HSTS not expanded at first use | Expansions and glosses |
| Network (targetSdk 37) | OkHttp ECH support is opt-in | One clause |
| Network (SPKI) | Legacy `sha1/` pins | One clause |
| Attestation (Standard vs classic) | `requestHash` meaning | Gloss |
| Attestation (opt-in labels) | On Android 13+, optional labels come back only for licensed apps | One sentence |
| Attestation (DCError) | The Keychain survives reinstall but the attest key doesn't (from §10.4) | One sentence |
| Biometrics | Hardware auth token unexplained; `setConfirmationRequired` is only a hint | Glosses |
| Pipeline | OIDC not expanded; `if: always()` purpose; provenance/SLSA undefined; Shai-Hulud undefined | Short glosses |
| Pipeline (`pull_request_target`) | Three changes run together in one sentence | Numbered list, with scope of each |
| AI | Tool, embeddings, MCP, and trust boundaries undefined in this file | Short glosses |
| Judgment (CVSS) | CVSS, AT:P, AV:P not expanded; how to "enrich" the Base score | Expansions; Threat and Environmental metrics named |
| Design review (kill switch) | The real-time listener is foreground-only and needs `activate()` (from §24.4) | One sentence |
| Design review (SDK) | Which API does data-access auditing | `AppOpsManager.setOnOpNotedCallback` |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| book/02-data-at-rest.md | §5.3 | "Key Attestation CA 1" → "Key Attestation CA1" | The certificate CN has no space |
| book/02-data-at-rest.md | §6.3 | "still alpha at 1.3.0-alpha11 (September 2026)" → release candidate 1.3.0-rc01 (12 October 2026) | DataStore release notes |
| book/03-data-in-transit.md | §8.2 | Optionally name the answer's author as a participant, not "the project's lead" accepting it (current text is accurate) | Discussion #573: mkk7ns answered; cpholguera accepted |
| book/04-proving-who-is-calling.md | §9.2 trap | Optional verdicts after re-decryption: "set to `UNEVALUATED` (or empty)", not "cleared" | Play Integrity standard-request docs |
| book/04-proving-who-is-calling.md | §9.4 | Note that for client-side exceptions the app, not the server, picks the dialog | Remediation docs |
| book/04-proving-who-is-calling.md | §10.3 | "`isSupported` returning false … can itself indicate tampering" → a spike of unsupported responses from a user on a supported platform | WWDC26 Session 201 |
| book/02-data-at-rest.md | §4.2 | CDD "strongly recommended" applies only to devices with a dedicated secure processor (current wording implies this; check) | Android 17 CDD §9.11.2 |
| book/12-verification.md | Correction log | Add a 2026-10-20 entry for the Part 10 corrections above | CONTRIBUTING.md step 2 |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| — | None new; every term glossed here is already taught in its source chapter | — |

## Judgment calls
- **"Judgement" heading.** I kept the heading `## Judgement`, its anchor, and the link text in the groups line, because other files may link to it. The prose uses American spelling. The author may want to rename the heading in a coordinated pass.
- **Rewritten questions.** I reworded four questions to stand alone: "Play Integrity: standard or classic requests?", "A device returns device integrity but not strong integrity…", "Which two monitoring alerts…", and "…What's your first move?". The Q&A text isn't a link target, so no anchors broke.
- **Lists.** I turned three dense answers into lists: the three LLM questions, KMP shareable vs native, and the `pull_request_target` changes, plus the MAS profiles in "bank-level". This follows the house rule (numbered list for a sequence, bullets for a set). Revert if a strict one-paragraph-per-answer format is preferred.
- **New hedges.** I added *(reasoned)* to the device-credential invalidation claim (three places) and *(contested)* to "Should you pin?", for consistency with §11.3 and §8.3.
- **Added nuance.** Some sentences grew to carry nuance from the chapters (the §10.4 key-ID caveat and the §24.4 listener caveats). That is why the file is about 600 words longer.
- **"Taught in" lines.** I added an Oxford comma to each "Taught in" line with three or more sections. The § numbers are unchanged.
