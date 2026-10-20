# book/04-proving-who-is-calling.md

## Summary
- Words before / after: 12,249 / 12,454
- Edits: clarity 34, filler 8, voice 52 (mostly contractions and active voice), spelling 33 (British to American, serial commas), explanation 9, code 6
- Facts checked: 92 · correct 79 · corrected 8 · unverified 5

Pass 3 covered the whole file, so `last_verified` is now 2026-10-20. I left `recheck_because` as it was because every fact in it still holds: androidx.biometric 1.4.0 is still alpha (alpha07, 22 Apr 2026), and Apple still hasn't answered the `invalidKey` reports. `python3 scripts/check.py` reports 0 problems, with swiftc and xmllint present.

### Facts checked and found correct (all checked 2026-10-20)
- **SafetyNet.** Deprecated in 2022 and turned down in January 2025; calls fail with `ApiException` status 7 (`NETWORK_ERROR`).
- **Play Integrity payload.** Five top-level fields, with no guaranteed order. The `appRecognitionVerdict` and `appLicensingVerdict` values are as stated, and `requestDetails` must be checked first.
- **Standard and classic requests.**
  - Warm-up takes a few seconds, most under 10 s. Latency is a few hundred ms (standard) versus a few seconds (classic).
  - `requestHash` is at most 500 bytes and goes into the token verbatim. The `nonce` format is URL-safe Base64, no wrap, 16–500 characters.
  - Replay protection is automatic for standard requests. Local decryption is available for classic requests only.
  - `INTEGRITY_TOKEN_PROVIDER_INVALID` handling, and Google's "exfiltration and certain types of attacks" wording, match the docs.
- **Quotas.** 10,000 token requests a day, shared with standard preparations. 10,000 decryptions a day. 5 classic requests per minute and 5 warm-ups per minute per app instance. Increases can take up to a week. Throttling on spikes is documented.
- **Repeated decryption.** "Reused many times" and the cleared-verdict details are accurate.
- **Optional labels and fields.** The opt-in list (BASIC, STRONG, `deviceAttributes`, `recentDeviceActivity`, `deviceRecall` beta, `environmentDetails`) is accurate. So are the Android 13+ and ≤12 label requirements, the "partially" wording, `MEETS_VIRTUAL_INTEGRITY`, and the `recentDeviceActivity` LEVEL_4 thresholds (>50 standard, >15 classic).
- **May 2025 change.** The ~90% signal cut, the up-to-80% worst-case latency gain, the gradual rollout, the Play-install requirement for optional signals, and the 14.5% and 0.4% estimates all check out.
- **Remediation dialogs.** The version mapping (1.3.0, 1.4.0, 1.5.0 on 28 Aug 2025), `showDialog` on the managers with the per-token method deprecated, and the latest library 1.6.0 (20 Nov 2025) are all correct.
- **Kotlin client APIs.** `createStandard`, the `PrepareIntegrityTokenRequest` and `StandardIntegrityTokenRequest` builders, and the `StandardIntegrityErrorCode` names exist as written. "Implement without enforcement first" is in the overview.
- **App Attest (Apple's establishing page).** The Secure Enclave key, the ≥16-byte challenge, "no restriction on the number of assertions", premium-content examples, one key per user per device, keys surviving updates but not reinstall, migration, or restore, and the `serverUnavailable`-then-same-key rule are all accurate.
- **App Attest validation steps.**
  - The attestation steps and their numbering (1–4, then 5–11), OID `.8.2`, the X9.62 key hash, RP ID, counter 0, the `aaguid` values, and `credentialId` match Apple's page.
  - The iOS 27 extension steps 10 and 11, assertion steps 1–8, macOS `aclBlob` OID `.8.6` with a single published value, and the macOS signing identifier also match.
  - The storage rules match: refuse a public key that another user already holds, store (key, receipt) pairs per device, and keep development and production pairs apart.
- **`appattestsandbox`.** The *Preparing* page does say this, so the contradiction the book describes is real.
- **Rate limits.** Fewer than 100 `attestKey` calls per second, at most 10 million users per day, and "shouldn't result in any throttling" are Apple's figures.
- **Fraud metric.** The receipt round trip, the 30-day count, not-before and expiry dates, and the PKCS #7 container are accurate.
- **WWDC26 Session 201.** The title, iOS 27 extensions, macOS 27 support, ACL Blob, the "Don't reject new keys outright" quote, `isSupported` as a signal, server-controlled attestation, exponential backoff, the steady or decreasing counter, and "investigation signal" all match the session.
- **DCError.** It has exactly five codes.
- **Other Apple details.** The DeviceCheck quote "can't definitively pinpoint…" is exact, and `Apple_App_Attestation_Root_CA.pem` is the right root file name.
- **Android hardware auth token.** The HMAC key is per-boot, shared by Gatekeeper, KeyMint, and biometric TAs, and Keystore and KeyMint verify the token.
- **KeyGenParameterSpec.** `setInvalidatedByBiometricEnrollment` defaults to true and applies only to biometric-only keys with no positive duration. API levels are correct: 24 for `setInvalidatedByBiometricEnrollment` and `setAttestationChallenge`, 30 for `setUserAuthenticationParameters`.
- **iOS biometric APIs.** `biometryCurrentSet` is invalidated on add, remove, or re-enroll. `LAContext.domainState` and `stateHash` exist from iOS 18, and `evaluatedPolicyDomainState` is deprecated in iOS 18.
- **Library versions.** `androidx.biometric` 1.1.0 is the latest stable and 1.4.0 is alpha. `androidx.credentials` 1.6.0 went stable on 8 Apr 2026.
- **Theft protections.** Stolen Device Protection arrived in iOS 17.3. Identity Check behaves as described, and users can turn both off.
- **OWASP IDs.**
  - MASWE-0020, 0021, and 0022 titles match.
  - MASTG-TEST-0326–0330 (Android) and 0266–0271 (iOS) are current v2 tests.
  - MASTG-TEST-0018 and 0064 are deprecated, replaced by those v2 tests.
  - MASTG-BEST-0031, 0036, 0037, and 0038 titles match the book's usage. MASTG-TECH-0043 and 0095 are "Method Hooking".
- **RFCs.** RFC 9449 checks 1–5 (exactly one header, no private key in `jwk`, `htu` ignoring query and fragment, `ath`, `cnf.jkt`), 400 `use_dpop_nonce` at the AS and 401 at the RS, and the §11.2 pre-generation risk are accurate. RFC 8705, RFC 7638, and RFC 7518 §3.4 (raw R‖S) are cited correctly.
- **Links.** These return 200: the Approov critique, the December 2024 Google blog, Apple support 120340, and Google support 15146908.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| 11.3 (Trap) | "falls outside that guarantee *(reasoned for the device-credential case)*" | Removed the marker; the device-credential case is now cited: `setUserAuthenticationRequired` docs say keys stay valid after enrollment changes when `AUTH_DEVICE_CREDENTIAL` is specified | https://developer.android.com/reference/android/security/keystore/KeyGenParameterSpec.Builder | 2026-10-20 |
| 11.3 (Trap) | "`MASTG-TEST-0326` flags the device-credential fallback" | "flags a prompt that allows the `DEVICE_CREDENTIAL` fallback" (the test checks `setAllowedAuthenticators`, not the key) | https://mas.owasp.org/MASTG/tests/android/MASVS-AUTH/MASTG-TEST-0326/ | 2026-10-20 |
| 10.5 | "Note the precise wording of the `attestKey()` rule: **once per key**." | "Note Apple's wording: you *typically* call `attestKey()` **once per user per device**, and you attest each key once." | https://developer.apple.com/documentation/devicecheck/preparing-to-use-the-app-attest-service | 2026-10-20 |
| 10.4 | "Two rough edges, from developer forum reports rather than documentation:" (the throttling bullet is from Apple's docs) | "Two rough edges remain:", with forum links added to the `invalidKey` bullet | https://developer.apple.com/forums/thread/739323, https://developer.apple.com/forums/thread/844380 | 2026-10-20 |
| 11.6 Verify it | "WithSecure's `fingerprint-bypass.js` ([…](https://github.com/WithSecureLabs/android-keystore-audit/…))" | "Reversec Labs' (formerly WithSecure Labs) …" with the link updated to `github.com/ReversecLabs/android-keystore-audit` (the old URL 301-redirects) | https://github.com/ReversecLabs/android-keystore-audit/tree/master/frida-scripts | 2026-10-20 |
| 9.3 table | MEETS_BASIC (A13+): "Android Platform Key Attestation root of trust from Google" | "Only that the key attestation root of trust is provided by Google" | https://developer.android.com/google/play/integrity/verdicts | 2026-10-20 |
| 9.1, 9.3 | Empty device verdict described only as "an empty list" | "empty or missing" (Google: `deviceIntegrity` omits `deviceRecognitionVerdict` when no label applies) | https://developer.android.com/google/play/integrity/verdicts | 2026-10-20 |
| 10.7 | "TestFlight and App Store builds always use production" | "TestFlight, App Store, and Enterprise builds always use production" | https://developer.apple.com/documentation/devicecheck/preparing-to-use-the-app-attest-service | 2026-10-20 |

Precision fixes too small to count as corrections: the 14.5%/0.4% estimates are now marked "averaged across apps" (Google's footnote). The RFC 9449 citation now reads "§4.3 (and §11.1 for tracking `jti`)", because `jti` tracking isn't in §4.3. The nonce paragraph now cites §11.2.

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| 10.4 | A small share of devices fail `attestKey` with `invalidKey` every time, with no answer from Apple | Found two Apple forum threads (2023 and Sep 2026) with no Apple reply; no documentation | Kept *(reported)*; links added |
| 10.4 | A key ID restored from backup causes `invalidKey` | Appears only as a community hypothesis in thread 739323; Apple hasn't confirmed it | Kept *(reported)* |
| 10.3 | Fraud metric "has existed since WWDC21" | WWDC21 session 10244 presents it, but Apple's receipt examples are dated 2020, so it may predate WWDC21; I found no source tying it to iOS 14 | Reworded to "at least since WWDC21" |
| 11.6 Verify it | The script's null-cipher `CryptoObject` reaches the androidx callback as a null `cryptoObject` | The script builds a framework `CryptoObject` wrapping null; androidx's conversion isn't documented | Added *(reasoned)* |
| 10.1 | `generateKey()` creates a P-256 key | Apple's DeviceCheck pages say "Secure Enclave" and a 77-byte COSE key but don't name the curve; P-256 is the only Secure Enclave curve | None needed (reasoned, consistent) |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Ch 9 intro | Why "NETWORK_ERROR" appears when SafetyNet is called | One clause: the name is misleading, the API is gone |
| 9.1 | "Hooked app" used before definition | Inline definition |
| 9.2 | "Take that literally" was vague | Says what the warning means: replay protection and token handling become your code's job |
| 9.2 quotas | Per-instance limit for standard tokens | Row: no public limit, non-public defensive limits |
| 9.3 | `LEVEL_4` "farm replaying one phone" was unclear | Literal description from Google's wording |
| 9.6 | What backoff to use | Google's 5/10/20 s, three attempts, then treat as failed |
| 10.3 | What "launch validation category" values look like | Example: `2` = TestFlight, `4` = App Store |
| 10.7 | Extension key names differ between Apple's attestation and assertion steps | Note naming both, and advice to confirm against a real assertion |
| Ch 11 intro | Frida undefined at first use in this file | Inline definition |
| 11.7 | iOS passkey API was only a framework name | Added `ASAuthorizationPlatformPublicKeyCredentialProvider`; explained phishing resistance in one clause |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| book/12-verification.md | Ch 33 log | Add a 2026-10-20 line for Part 4: device-credential invalidation is now documented (marker removed); `attestKey` wording corrected; Reversec repo link updated | CONTRIBUTING asks every fix to be logged there |
| book/12-verification.md | Sources | Replace `github.com/WithSecureLabs/android-keystore-audit` with `github.com/ReversecLabs/android-keystore-audit` if listed; add the two Apple forum threads and the Play Integrity error-codes page if Sources tracks every cited URL | Repo moved; new citations |
| book/12-verification.md | Glossary | Consider "hardware auth token", "launch validation category", "DPoP proof" if absent | Defined in this file |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Hardware auth token | HMAC-signed token a TEE authenticator (biometric TA or Gatekeeper) emits after a successful authentication; KeyMint checks it before using an auth-bound key | 11.1 |
| Launch validation category | iOS 27+ App Attest extension value saying how the running binary was distributed (for example TestFlight or App Store) | 10.3 |

## Judgment calls
- **Spelling.** I converted the file to American spelling per PROMPT.md, which the coordinator confirmed CONTRIBUTING.md now matches. That includes the author's own Kotlin identifiers (`authoriseTransfer`, `onReEnrolmentNeeded`, `offerEnrolment` became `authorize…`, `onReEnrollmentNeeded`, and `offerEnrollment`) and the Mermaid label "Authorization server". None of these names appears in any other file. Revert the identifiers if you want code untouched.
- **Opinions now marked as mine.** "Most teams skip" is now "I rank it the highest-value control most teams skip". "One of the most commonly missed weaknesses" is now "in my experience". "Here is the consequence almost everyone gets wrong" is now "Many teams get the consequence wrong". "The most common implementation error" is now "a common implementation error". All of these were unsourced superlatives.
- **Fragments.** I turned the intro's sentence fragments ("Four chapters. Two platform…") into full sentences.
- **Idioms.** I replaced several: "burn quota", "hot lifecycle paths", "through the back door", "paying in a different currency", "worth sitting with", and "what crosses the wire".
- **Headings.** I left them unchanged, including "Errors you will actually meet" and "Limits, and when to actually check", even though they contain filler, because other files link to them.
