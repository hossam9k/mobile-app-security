# book/02-data-at-rest.md

## Summary
- Words before / after: 11,462 / 11,867 (growth is mostly the rewritten §5.5 server code, the Tink "both sides" paragraph, and short inline definitions)
- Edits: clarity 34, filler 16, voice 44, spelling 27, explanation 17, code 9
- Facts checked: 100 · correct 78 · corrected 16 · unverified 6

All four passes are complete for the whole file, so `last_verified` is now 2026-10-20. I also updated `recheck_because`, because two facts in it changed (datastore-tink status, keyattestation version and the app-ID check). `python3 scripts/check.py` reports 0 problems. Headings, § numbers, figure numbers and captions, callout labels, confidence markers, and code-fence languages are unchanged. The only new cross-reference is §6.1, which already exists.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| §5.5 (In practice) | Library "at **v0.1**", a "test release"; app-ID check "added and reverted… If it lands, it replaces the manual block" | Latest tag **v0.4 (13 Oct 2026)**, still called a "test release"; app-ID check added and reverted on 24 Sep, then re-added on 25 Sep (commit 411188a), and in v0.3+ | https://github.com/android/keyattestation (tags v0.1–v0.4, RELEASE.md, commits d5b0001/0cb2c37/411188a) | 2026-10-20 |
| §5.5 (In practice) | "README's example still names `ExtensionConstraintViolation`" | The README now uses `ConstraintViolation`, but its constructor call doesn't compile (it passes a `ConstraintConfig` where the 4th parameter is `AttestationApplicationId?`) | repo README.md vs src/main/kotlin/Verifier.kt @ v0.4 | 2026-10-20 |
| §5.5 (prose + code) | "it doesn't check your app identity"; manual `keyDescription()` package/signer block with exact set equality | The library checks app identity when you pass `expectedAttestationApplicationId`. The default `ALLOW_UNKNOWN_PACKAGE` is lenient, so the code selects `STRICT`. Signers match if *any* listed digest is present, and package version must be at or above the one listed. The code now builds `Verifier(GoogleTrustAnchors, CachedRevocations, { Instant.now() }, expectedAppId, strictAppId)` and maps `ConstraintViolation` to its label. The Verify it step 2 expected result changes to `Rejected("Attestation application ID")` | Verifier.kt, ConstraintConfig.kt, Extension.kt @ v0.4 | 2026-10-20 |
| §6.3, takeaways, §6.6 code, frontmatter | datastore-tink "**still alpha** at 1.3.0-alpha11 (September 2026)"; deps `1.3.0-alpha11` | "**not yet stable**: the current release is 1.3.0-rc01 (12 October 2026), a release candidate"; deps `1.3.0-rc01` | https://developer.android.com/jetpack/androidx/releases/datastore ; dl.google.com maven-metadata | 2026-10-20 |
| §6.6 code | `tink-android:1.23.0` | `tink-android:1.24.0` (released 16 Oct 2026; `RegistryConfiguration`, `PredefinedAeadParameters`, and `AndroidKeysetManager` are still present) | https://github.com/tink-crypto/tink-java/releases/tag/v1.24.0 | 2026-10-20 |
| Ch 6 intro, §6.4 | "For almost a decade…"; "a decade of… advice" | "For about six years…"; "six years of… advice" (security-crypto 1.0.0-alpha01 shipped 7 May 2019; deprecated April 2025) | https://developer.android.com/jetpack/androidx/releases/security | 2026-10-20 |
| §5.3, §5.5 | New root named `"Key Attestation CA 1"` (in quotation marks, as if it were Google's name) | "certificate common name `Key Attestation CA1`". Google's page doesn't name the root in its prose; the CN comes from the certificate (P-384 verified with openssl) | https://developer.android.com/privacy-and-security/security-key-attestation ; roots.json in the repo | 2026-10-20 |
| §4.4 table, §6.6 Swift comment | `WhenPasscodeSetThisDeviceOnly` items "are destroyed if the passcode is removed" | "become unusable if the passcode is removed or reset" (Apple: the items are rendered useless by discarding the class keys) | https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web | 2026-10-20 |
| §4.4 | BFU extraction recovers "the `Always` ones" | "the `Always` and `AlwaysThisDeviceOnly` ones" | Elcomsoft post (already cited) | 2026-10-20 |
| §4.6 table | "before API 31 symmetric encryption was not either" | "before API 31, symmetric encryption and verification weren't either" | https://developer.android.com/reference/android/security/keystore/KeyGenParameterSpec.Builder#setUnlockedDeviceRequired(boolean) | 2026-10-20 |
| §6.4 | "Since Android 10, file-based encryption is mandatory" | "Every device that launches with Android 10 or later must use file-based encryption" (+ link) | https://source.android.com/docs/security/features/encryption/file-based | 2026-10-20 |
| §6.5 | Keyboard cache listed with no MASWE ID | Added `MASWE-0036` (MASTG-DEMO-0076 → MASTG-TEST-0313 → MASWE-0036) | https://mas.owasp.org/MASTG/tests/ios/MASVS-STORAGE/MASTG-TEST-0313/ | 2026-10-20 |
| §6.5 | Android 15 OTP hiding marked *(reported)* | Cited the official Android 15 behavior-changes page and removed the marker. Added that Android 16 redacts OTPs on the lock screen only in higher-risk cases *(reported)* | https://developer.android.com/about/versions/15/behavior-changes-all | 2026-10-20 |
| §6.7 prose + code | sqlcipher-android 4.19.0 | 4.19.1 (minSdk 23 and the Room 3 `SQLCipherDriver(passphrase, null, null)` API are confirmed) | Maven Central metadata; https://github.com/sqlcipher/sqlcipher-android README | 2026-10-20 |
| §6.7 | Old library "won't gain 16 KB page-size support" | Its open-source edition won't. Zetetic offers a 16 KB-compatible build to commercial customers only (+ link) | https://www.zetetic.net/blog/2025/06/26/sqlcipher-for-android-16kb-page-size-support/ | 2026-10-20 |
| §6.6 clipboard code comment | "EXTRA_IS_SENSITIVE on API 33+; the literal also works on older targets" | "…if you compile against SDK 33+; the literal works with older SDKs". Google frames this by compile SDK, not target | https://developer.android.com/develop/ui/views/touch-and-input/copy-paste | 2026-10-20 |

Best-practice update (logged here because it changes the guidance): Tink's `AndroidKeysetManager` Javadoc "strongly recommend[s]" not setting a Keystore master key unless you need user authentication. The book didn't mention this, though the Jetpack deprecation points to direct Keystore use. I added a short paragraph to §6.4 that gives both positions and explains when each one is defensible. Source: tink-java v1.24.0 `AndroidKeysetManager.java`.

Confirmed correct (selection): keystore2 in Rust (Android 12) and KeyMint replacing Keymaster (Android 12); KeyMint v2 Curve25519 (Android 13); keyblob wording; ML-DSA in Android 17 Beta 4 (hardware-dependent); PQC quote and date (blog.google, 25 Mar 2026); KeyInfo `getSecurityLevel` (API 31) and `isInsideSecureHardware` deprecated in API 31; StrongBox algorithm list and "slower… fewer concurrent operations"; CDD §9.11.2 wording identical in 16 and 17; Keychain SQLite, securityd, two AES-256-GCM keys, metadata key cached in the AP, ACLs evaluated in the SE; 10-second discard; default class C; `kSecAttrAccessibleAlways` deprecated in iOS 12 with the AfterFirstUnlock note; ThisDeviceOnly backup behavior; SE on iPhone 5s (A7) and later; Secure Enclave P-256 only; CryptoKit `SecureEnclave.MLKEM768/1024` and `MLDSA65/87` in iOS 26; `SecureEnclave.isAvailable`; `KeyStoreManager.grantKeyAccess/revokeKeyAccess` (API 36); key-authorization API levels and invalidation default; key attestation in Android 7.0/Keymaster 2 and ID attestation in 8.0/Keymaster 3; the "collected or generated…" hardwareEnforced text; RKP 2022 blog quotes (chain length, RSA→ECDSA, per-app keys, rotation, split backend); single-device revocation (Google's attestation page); Android 16 RKP-only and Android 15 "optional" wording; 1 Feb 2026 root date; revocation JSON schema (lowercase hex, REVOKED/SUSPENDED, reason enum, expires); Cache-Control guidance; Kotlin library recommendation; library behavior (REVOKED-only parsing, NOT_SOFTWARE plus level match, Origin GENERATED, root of trust non-null, boot state returned and not enforced, `securityLevel` = min of the two); TEESimulator description; Quarkslab details (11 Aug 2026; the app-ID check was run separately and rejected the relay; PoP proposed and untested); security-crypto dates, quote ("favour" kept, since it is a quote), and replacements table; `_androidx_security_master_key_`; `SharedPreferencesMigration` constructors and deletion behavior; fork coordinates, "No, probably not.", quote, minSdk 23; Tink 1.18 dropped API 21/22; Tink cleartext fallback and `KeyStoreException`; `AeadSerializer` signature, file-name associated-data advice, JVM/Android; `DataStore.Builder` recommendation; MASVS-STORAGE-2 text; MASWE-0004/0005/0006/0030/0037/0038 IDs and titles (post-v1.0.0 numbering); MASTG-DEMO-0020/0059/0069/0070/0076 exist with no deprecation banner; DEMO-0020 script details; Auto Backup OEM D2D note, `disableIfNoEncryptionCapabilities`, Android 16 QPR2 cross-platform transfer; `setRecentsScreenshotEnabled` (33), `registerScreenCaptureCallback` (34), `addScreenRecordingCallback` (35); `IME_FLAG_NO_PERSONALIZED_LEARNING` (26); `EXTRA_IS_SENSITIVE` (33) and "does not change clipboard behavior"; Android 10 clipboard restriction; `UITraitCollection.sceneCaptureState` / `UITraitSceneCaptureState` (iOS 17); `UIScreen.isCaptured` deprecated in iOS 27; `.localOnly` (Handoff); `LocalActivity` in activity-compose 1.10; SafetyNet turned down January 2025; WHOIS methods 3.2.2.4.2/.15 barred from 2025-07-15 (BR 2.1.2 / SC-080); MAS-P proposal 10 Oct 2023 and MASVS v2.1.0 18 Jan 2024; 16 KB: 1 Nov 2025 (blog) and 1 Feb 2027 (guide); old SQLCipher deprecated 2023; Room 3 `androidx.room3`. Every link in the file returns 200 (the page-sizes guide timed out with curl but loads through fetch).

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| Ch 5 intro, §5.3 | RKP devices switched exclusively to the new root on 10 April 2026; most phones' chains rejected by old verifiers "by April" | Google's attestation page (no April date); search found only vendor pages (bayton.org, Nevis docs) | *(reported)*. Kept in §5.3 and added to the Ch 5 intro, where the claim was previously unmarked |
| §6.1 | Practitioners' reasons for the deprecation (OEM Keystore inconsistencies, StrictMode, keyset corruption) | No Google statement found | *(reported)* (kept) |
| §6.5 | Keychain items survive app deletion | No Apple documentation either way | *(reported)* (kept) |
| §6.5 | Android 16 lock-screen OTP redaction "in higher-risk situations" | Search summary of Android Authority; the page returns 403 to fetch | *(reported)* (added) |
| §4.4 | checkm8 affects A5–A11 | Elcomsoft gives "iPhone 5s through iPhone X" for its tool; no primary chip-range source fetched (widely documented, from axi0mX's disclosure) | none needed; leave unless a reviewer objects |
| §6.5 | "Since Android 4.1, ordinary apps can read only their own log entries" | `READ_LOGS` confirmed "Not for use by third-party applications"; the 4.1 version boundary wasn't re-found on a primary page | none (long-standing platform fact); recheck if challenged |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| §4.1 | TEE used in "Under the hood" before §4.2 defined it | Inline "trusted execution environment (TEE, §4.2)" |
| §4.1 | "authorisations" used before §4.6 | "(the conditions of use you attached to it, §4.6)" |
| §4.1 | Why Rust matters | Rust rules out most memory-safety bugs at compile time; one such bug in key handling could expose every key |
| §4.1 | Who encrypts keyblobs | "encrypted by the secure hardware" |
| §4.1 | Request flow buried in prose | Converted to a 4-step numbered list |
| §4.2 | Secure Element, side-channel attack, step-up authentication undefined | Short inline definitions |
| §4.3 | Application Processor, ECDH undefined | "(the main CPU)", "(elliptic-curve Diffie-Hellman)" |
| §4.4 | Why checkm8 can't be patched | The bootrom is read-only |
| §4.5 | UID undefined | "(the Linux user ID Android assigns to each app)" |
| §4.6 | Frida undefined | "(a tool that rewrites an app's code while it runs)" |
| §5.3 | RKP not explained before its history | "delivers short-lived attestation keys over the network instead" |
| §5.3 | Cache-Control | One-clause definition |
| §5.4 | AOSP, keybox | Expanded inline |
| §5.5 | CRL/OCSP | "the two standard revocation formats that Java's check understands" |
| §5.5 | Where to get the signer digest | Play Console app-signing certificate SHA-256 |
| §6.4 | Tink vs Jetpack disagreement | Both sides, and when each is defensible |
| §6.5 | Why `String` is a problem | It's immutable, so you can't overwrite it |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| book/12-verification.md | Glossary `AeadSerializer` (line ~721) | "alpha since DataStore 1.3.0-alpha07" → "since DataStore 1.3.0-alpha07; release candidate at 1.3.0-rc01 (Oct 2026)" | datastore-tink reached rc01 on 12 Oct 2026 |
| book/12-verification.md | Volatility table row for Ch 6 (line ~337) | "`datastore-tink` is still alpha" → "release candidate, not yet stable" | Same |
| book/12-verification.md | Facts table (line ~280); book/10-questions-and-answers.md line ~954 | `"Key Attestation CA 1"` → certificate CN `Key Attestation CA1` | Google never names it in prose; the CN has no space |
| book/12-verification.md | Correction log | Add an entry dated 2026-10-20 for this file's corrections (keyattestation v0.4 and the app-ID check now in the library with code rewritten, datastore-tink rc01, Tink 1.24.0, "decade" → six years, FBE wording, SQLCipher 4.19.1 and the commercial 16 KB build, MASWE-0036) | CONTRIBUTING.md requires a log line per fix |
| CONTRIBUTING.md | Style | It says "British spelling in prose", but editorial/PROMPT.md requires American. I followed PROMPT.md | Resolve the conflict so future edits don't flip-flop |
| dist/ | — | Rebuild (`python3 scripts/build.py --md-only`) | CI fails if dist/ is stale |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| `expectedAttestationApplicationId` | The android/keyattestation `Verifier` constructor parameter that makes the library reject chains whose app identity (package, version, signer digest) doesn't match yours | §5.5 |
| Side-channel attack | An attack that infers a key from physical effects such as power use, timing, or electromagnetic emissions | §4.2 |
| Step-up authentication | An extra check, such as a one-time code, required before a risky action | §4.2 |

## Judgment calls
- **American spelling everywhere in prose**, including table cells and code comments (authorization, behavior, defense, honor, artifact, initialized, recognizable, standardized, learned). The quote "in favour of…" stays as Google wrote it. This contradicts CONTRIBUTING.md (see above), so revert if the house style stays British.
- **Dates kept in day-month-year form** ("10 April 2026"). PROMPT.md specifies American spelling but says nothing on date format, so I didn't change them.
- **§5.5 code rewrite.** The manual `attestationApplicationId` block is gone because the library now does that check and the book had said "if it lands, it replaces the manual block". I chose `STRICT` over the library default `ALLOW_UNKNOWN_PACKAGE`, which lets "UnknownPackage" through on old OS versions. If the author prefers to keep compatibility with old devices, switch to the default and say so. I could not compile the snippet against v0.4 (it needs a local Gradle/JDK 21 build). Every symbol, parameter order, and type was checked against the v0.4 source.
- **Tink 1.24.0 bump.** It was released four days before the check. 1.23.0 also works, so revert if the author prefers a version with more field time.
- **Tink vs Jetpack paragraph (§6.4).** This is new content, five sentences, added to meet the "industry disagrees" rule. Trim it if it feels like a digression.
- **"the check doesn't stop it" → "proof of possession doesn't stop it"** (§5.4) to remove an ambiguous reference. The meaning is unchanged.
- **Ch 5 opening.** I added *(reported)* to "By April… rejected", because the April date is practitioner-reported elsewhere in the same chapter.
- **"Apple's design differs in structure but rhymes in principle"** became a literal sentence that states the shared principle (the app holds a handle, secure hardware guards the key). Idioms "paper over", "dead end", "bridge with a deadline", "raises the bar… not a wall", "moving target", and "happily copy" were replaced with literal wording.
- I kept "The thing that will break your production app in 2026" (§5.3 heading) unchanged, as required, even though its "will" is now past for most readers.
