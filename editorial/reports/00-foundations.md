# book/00-foundations.md

## Summary
- Words before / after: 9,322 / 10,247 (`wc -w`, code included). The increase comes from definitions and "why it works" sentences added for readers new to security. Filler cuts offset part of it.
- Edits: clarity 42, filler 14, voice 27, spelling 34, explanation 26, code 1
- Facts checked: 74 · correct 60 · corrected 14 · unverified 0 (one claim kept as hedged; see the `Cipher.getInstance("AES")` row in Judgment calls)
- `last_verified` set to 2026-10-20. `recheck_because` unchanged: OAuth 2.1 still isn't published as an RFC.
- `python3 scripts/check.py`: 0 problems.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| Ch 0.1 Trap | "MASWE v1.0.0 renumbered … MASTG v2.0.0 deprecated …" (no dates) | Adds the dates: MASTG v2.0.0 (June 2026), MASWE v1.0.0 (August 2026) | https://github.com/OWASP/mastg/releases/tag/v2.0.0 (2026-06-30), https://github.com/OWASP/maswe/releases/tag/v1.0.0 (2026-08-17) | 2026-10-20 |
| Ch 0.2 | MASTG-TEST-0309/0310 placeholders "as of September 2026" | "as of October 2026" (re-confirmed: both still placeholders) | https://mas.owasp.org/MASTG/tests/android/MASVS-CRYPTO/MASTG-TEST-0309/ | 2026-10-20 |
| Ch 0.2 | RSA "3,072 or more is preferred for anything meant to last" | "NIST asks for 3,072 bits or more for protection that must last beyond 2030" | NIST SP 800-57 Pt 1 Rev 5, Table 4 (112-bit strength acceptable through 2030) | 2026-10-20 |
| Ch 0.2 | "Its draft transition plan, NIST IR 8547, proposes…" | States that IR 8547 is still an initial public draft (Nov 2024) as of October 2026 | https://csrc.nist.gov/pubs/ir/8547/ipd | 2026-10-20 |
| Ch 0.2 password table | bcrypt listed without qualification; takeaway "Argon2id or bcrypt for passwords" | bcrypt marked "only for legacy systems that can't use Argon2id or scrypt"; takeaway now "Argon2id (or scrypt)" | OWASP Password Storage Cheat Sheet (bcrypt "should only be used … in legacy systems") https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html | 2026-10-20 |
| Ch 0.2 password table | bcrypt "only uses the first 72 bytes" | "Most implementations use only the first 72 bytes" | Same cheat sheet ("for most implementations") | 2026-10-20 |
| Ch 0.2 MAC | "An ordinary `==` can leak, through timing…" | Uses `contentEquals` as the example. In Kotlin, `==` on a `ByteArray` compares references, not contents, so it isn't the timing-leak example the text meant. Also states that `MessageDigest.isEqual` is constant time on Android, not only on the JVM. | Android libcore `MessageDigest.isEqual` source ("time-constant comparison") https://android.googlesource.com/platform/libcore/+/refs/heads/main/ojluni/src/main/java/java/security/MessageDigest.java | 2026-10-20 |
| Ch 0.3 | Reuse detection "revokes the whole token family: the old token and every token issued from it" | "revokes the currently active refresh token in that chain, and both copies stop working" | RFC 9700 §4.14.2 ("it will revoke the active refresh token") | 2026-10-20 |
| Ch 0.3 | RFC 9700: "don't use the implicit grant" | "clients should not use the implicit grant" (it's a SHOULD NOT; ROPC stays MUST NOT) | RFC 9700 §2.1.2, §2.4 | 2026-10-20 |
| Ch 0.3 | PKCE pronounced "pixie" | "pixy", the spelling RFC 7636 uses | RFC 7636 §1 | 2026-10-20 |
| Ch 0.3 Auth Tab | "falls back to a normal Custom Tab on browsers without it" | Adds that in fallback the redirect arrives through the app's App Link (the result is `RESULT_CANCELED`), so the app must handle that path. The Kotlin `else` branch comment now says so. | https://developer.chrome.com/docs/android/custom-tabs/guide-auth-tab | 2026-10-20 |
| Ch 0.3 | "the MASVS says … that the MASVS covers only the app" | "the MASVS states that enforcement must happen on the remote endpoint and points you to a separate standard for the server" (ASVS) | https://mas.owasp.org/MASVS/07-MASVS-AUTH/ | 2026-10-20 |
| Ch 0.4 | "The iOS Keychain is protected by the Secure Enclave. Your app asks the hardware to *use* the key, and the key material never enters your process." | Separates Secure Enclave keys (P-256, non-extractable; only use is possible) from Keychain items (secrets encrypted under SE-protected keys, which *are* returned to your process) | Apple Platform Security guide (Keychain data protection; Secure Enclave) | 2026-10-20 |
| Ch 0.4 | MIE "On iPhone 17, iPhone Air and later models (A19 chips onward)" | "On all iPhone 17 models and iPhone Air (A19 and A19 Pro chips)". The source doesn't say "later models". | https://security.apple.com/blog/memory-integrity-enforcement/ (2025-09-09) | 2026-10-20 |

## Claims confirmed correct (for the record)
MASWE IDs and titles 0001 (tagged L2, EUDIW in the source frontmatter), 0003, 0004, 0007 (link live; has *Modes of Introduction*, covers IV/nonce misuse), 0008, 0011, 0012, 0013, 0014, 0015, 0023, 0024; MASWE total 78. MASTG-TEST 0204, 0205, 0211, 0232, 0307, 0311, 0317, 0349, 0350 live and not deprecated. DEMO-0058 (ECB via `KeyGenParameterSpec`), TECH-0011 (interception proxy), BEST-0001, KNOW-0015, and KNOW-0003 (app signing) also live. MASVS-AUTH-1 and -3 wording. fail0verflow at 27C3 (December 2010). PS3 ECDSA repeated nonce. NIST SP 800-38D 2³² limit. Android Keystore rejects caller IVs by default. Tink prefix‖IV‖ciphertext‖tag. CryptoKit `seal` generates a nonce. `SecureEnclave.MLKEM768/1024` and `MLDSA65/87` available from iOS 26.0. FIPS 203/204 (13 August 2024). iOS 26 X25519MLKEM768 by default (Apple Platform Security, TLS page). SHA-1 collision 2017. OWASP password parameters (Argon2id 19 MiB/t=2/p=1 and 46 MiB/t=1; scrypt 2¹⁷/8/1; bcrypt ≥10; PBKDF2 600,000). `SystemRandomNumberGenerator` uses `arc4random_buf`. RFC 9700 (January 2025): refresh tokens rotated or sender-constrained for public clients, ROPC MUST NOT, PKCE S256. RFC 9449 proof claims (htm, htu, iat, jti, ath). RFC 8705. RFC 7519. RFC 8252 (BCP 212): PKCE MUST, implicit NOT RECOMMENDED, embedded user-agents MUST NOT, custom-scheme "indeterminate". RFC 7636 S256 MUST. RFC 7009. AppAuth-Android 0.11.1 (22 December 2021) is still the latest release. `androidx.browser` 1.9.0 and Chrome 137 for Auth Tab, plus its `launch(…, host, path)` signature and result codes. `ASWebAuthenticationSession.Callback.https(host:path:)` iOS 17.4, with the host in an associated domain. OWASP API Top 10 2023 API1 BOLA. ASVS 5.0.0 (30 May 2025) is still the latest release. FBE on Android 10+ launches. iOS default class is *complete until first user authentication*. Android developer verification: 30 September 2026; seven stores (Play plus six partner stores); four countries; Android 7+; global in 2027; advanced flow. Cleartext off for targetSdk 28+. User CAs not trusted for targetSdk 24+. CT on by default for API 37, off for user/inline anchors. Play Integrity Android 13+ verdict requirements. LINDDUN categories. Threat Modeling Manifesto's four questions.

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| — | None open. One claim, that `Cipher.getInstance("AES")` "can silently give you ECB", rests on the documented "provider-specific default" plus the Conscrypt registrations. I didn't find an Android page that names ECB as the default. The text already hedges with "can", so I left it as is. | Android `Cipher` reference; Conscrypt `OpenSSLProvider` source | none (already hedged) |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| 0.1 | "Control" was used but never defined | One-clause definition |
| 0.1 | "Pinning" appeared without a definition | Parenthetical definition with a pointer to Chapters 7 and 8 |
| 0.1 | Why "you don't control the client" matters | Two sentences: users can read and change the app; only the server can hold a check they can't remove |
| 0.1 | "Hooking is how client-side security gets bypassed": the mechanism wasn't explained | One sentence describing the mechanism |
| 0.1 | OWASP expanded at first use | Added |
| 0.1 | Defense in depth: what "independent" means | Defined |
| 0.2 | Why testing misses crypto bugs | "Your round-trip test passes while an attacker reads or forges the data" |
| 0.2 | Why AES alone isn't enough | AES encrypts exactly one block |
| 0.2 | Padding oracle: how the leak happens | Added the mechanism (valid/invalid padding reported through errors or timing) |
| 0.2 | Associated data: what breaks without it | Moving a ciphertext onto another record fails decryption |
| 0.2 | Why the 2³² limit exists | Random-nonce collision probability |
| 0.2 | TLS 1.3 hybrid example as one long sentence | Numbered three-step sequence |
| 0.2 | "Memory-hard" and KDF undefined | Defined |
| 0.2 | Why seeding with a timestamp is fatal | Attacker reproduces the output |
| 0.2 | Hardcoded key "public constant with extra steps" (idiom) | Literal explanation |
| 0.3 | "Identity provider", "authorization code", "authorization server", and "client" used before definition | Defined at first use |
| 0.3 | PKCE mechanism as one paragraph | Numbered three steps, plus why the challenge doesn't reveal the verifier |
| 0.3 | `state`: what the attack achieves | The user is signed in to the attacker's account |
| 0.3 | DPoP: why a stolen token fails | The attacker can't sign the proof |
| 0.3 | Step-up: why a boolean is weak | A Frida user flips the boolean |
| 0.3 | Verify it as one dense paragraph | Pass criteria as a bulleted list; intercepting proxy defined |
| 0.4 | CA, Certificate Transparency, and forward secrecy undefined | Defined in one clause each |
| 0.5 | Why the receipt-import bug is dangerous | The other app can't read the file, but tricks your app into reading it |
| 0.5 | Why prompt lists beat imagination | One sentence |
| 0.6 | PII, PCI DSS, GDPR, credential stuffing, and "asset" undefined | Defined |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| book/00-foundations.md (headings; not edited, per the hard constraints) | Ch 0.1 | Headings "Authentication versus authorisation" and "Attack surface, threat model, defence in depth" still use British spelling | Heading text is a link target. If the book moves fully to American spelling, rename both together with any anchors that point to them |
| book/12-verification.md | Glossary | "Refresh token rotation": note that rotation needs reuse detection, which revokes the *active* token (RFC 9700 §4.14.2). Change "Authorisation"/"Authorisation code flow" entries to American spelling if the glossary is converted | Consistency with the corrected Ch 0.3 text |
| book/12-verification.md | Glossary | "Argon2id" entry is fine. Consider adding that OWASP treats bcrypt as legacy-only | Matches the corrected Ch 0.2 table |
| book/12-verification.md | Audit log | Add a 2026-10-20 line for this pass's corrections (bcrypt legacy, reuse-detection wording, Keychain vs Secure Enclave, Kotlin `==`, Auth Tab fallback) | CONTRIBUTING.md step 2 |
| book/02-data-at-rest.md | Chapter 4 | Check that Chapter 4 makes the same Keychain vs Secure Enclave key distinction now made in Ch 0.4 | Avoid contradiction |
| dist/ | — | Rebuild (`scripts/build.py --md-only`) | The Figure 2 caption spelling changed |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Control | Anything you put in place to protect confidentiality, integrity, or availability | Chapter 0.1 |
| Defense in depth | Layered, independent controls, so one failure doesn't expose everything | Chapter 0.1 |
| Replay | Sending an old copy of a valid request again | Chapter 0.1 |
| Padding oracle | An attack that recovers CBC plaintext from valid/invalid padding signals | Chapter 0.2 |
| Hybrid encryption | Asymmetric crypto agrees on or protects a key; symmetric crypto carries the data | Chapter 0.2 |
| Memory-hard function | A password hash that needs a lot of memory per guess, making specialized cracking hardware expensive | Chapter 0.2 |
| Non-repudiation | Being able to prove to a third party who performed an action | Chapter 0.2 |
| Reuse detection | The server revokes the active refresh token when an already-used one is presented again | Chapter 0.3 |
| Authorization server | The OAuth server that issues tokens (run by the identity provider) | Chapter 0.3 |
| Credential stuffing | Trying username/password pairs leaked from other sites against your login | Chapter 0.6 |
| Certificate Transparency | Requirement that certificates appear in public logs; on by default for Android 17 targets | Chapter 0.4 |
| Forward secrecy | A key stolen later can't decrypt traffic recorded earlier | Chapter 0.4 |

## Judgment calls
- **American spelling everywhere except headings.** I applied it per PROMPT.md and the updated CONTRIBUTING.md, including the Figure 2 caption ("authorization code flow") and the Mermaid participant label. No other file references the caption text (only `dist/`, which is regenerated). Headings were left untouched, per the hard constraints.
- **Removed "(spelt *authorization* in the OAuth specifications)".** With American spelling throughout, the note is no longer needed.
- **Date formats** such as "30 September 2026" were left in day-month-year order. PROMPT.md doesn't specify a date style, and changing it in one file would be inconsistent with the rest of the book.
- **"Refresh tokens are the crown jewels"** became "your most valuable credential", per the idiom rule.
- **"TLS 1.3, the protocol behind every HTTPS connection"**: I wrote this phrase during Pass 2, then corrected it to "the current version of the protocol behind HTTPS" in Pass 4.
- **Kotlin Auth Tab code:** only the `else` branch comment changed (expanded to mention the Custom Tab fallback). No API changes.
- **The Swift `@MainActor` coordinator** was left as is. `swiftc -parse` passes; I didn't type-check it against the iOS 26 SDK's concurrency annotations for `ASWebAuthenticationPresentationContextProviding`.
- **Word count grew about 10%.** Every addition is a definition or a one-sentence "why" for a term the reader would otherwise meet undefined. If length matters, the 0.6 table-definitions sentence and the ECDSA parenthetical are the easiest cuts.

## Addendum (second agent, 2026-10-20)
A second agent ran in parallel on this file and re-checked the Chapter 0.1 and 0.2 facts independently (all MAS IDs and titles, MASTG-TEST-0309/0310 placeholders, NIST IR 8547 still an initial public draft, Apple iOS 26 X25519MLKEM768 default, `SecureEnclave.MLKEM768`/`MLDSA65` from iOS 26.0, OWASP password parameters, `arc4random_buf`, §6.6 target). All agree with the tables above. Two extra edits:
- Ch 0.1: "rooted (defined below)" at its first use in the defense-in-depth paragraph (term used before its definition).
- Ch 0.2 correction: IR 8547 sentence said 112-bit algorithms are "disallowed after 2035", which a reader could take to mean P-256 stays allowed. Now: 112-bit algorithms (such as RSA-2048) deprecated after 2030, and every quantum-vulnerable public-key algorithm, P-256 and RSA-3072 included, disallowed after 2035. Source: https://csrc.nist.gov/pubs/ir/8547/ipd (draft Tables 2 and 4), summary at https://postquantum.com/security-pqc/nist-ir-8547-ipd/ *(reported)*. Checked 2026-10-20.
