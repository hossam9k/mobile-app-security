# book/03-data-in-transit.md

## Summary
- Words before / after: 11,841 / 12,109 (the increase comes from added definitions and corrections)
- Edits: clarity 62, filler 9, voice 58, spelling 27, explanation 14, code 9
- Facts checked: 74 · correct 61 · corrected 11 · unverified 7 (one of these is half-confirmed and marked as such)

Edits by type:

- **Voice:** contractions, active voice, and naming who acts.
- **Spelling:** British to American in prose. Link text "behaviour changes" became "behavior changes". Two code comments changed too: "honoured" and "behaviour".
- **Code:** spaced em dashes in Swift and Kotlin comments became colons or parentheses. No code logic changed.

`python3 scripts/check.py` reports 0 problems. `last_verified` is set to 2026-10-20. `recheck_because` is unchanged because none of its facts changed.

The SPKI hashing was checked on both platforms:

- **Android/OkHttp:** OkHttp's pinner hashes `publicKey.encoded`, which is the SPKI (source read).
- **OpenSSL:** the pipeline (`x509 -pubkey | pkey -pubin -outform der | dgst -sha256 -binary | base64`) is correct. The empty-input hash `47DEQ…FU=` was reproduced locally.
- **Swift RSA wrapper:** the bytes `30 0D 06 09 2A 86 48 86 F7 0D 01 01 01 05 00` are the correct rsaEncryption AlgorithmIdentifier. The BIT STRING has a leading 0x00 for unused bits, and the long-form DER length is right.
- **Swift EC keys:** the x963 lengths 65/97/133 map correctly to P-256/P-384/P-521. CryptoKit `derRepresentation` gives the SPKI.
- **Ktor Darwin:** `validateTrust` defaults to true, and the hardcoded headers cover RSA 1024/2048/3072/4096 and EC P-256/P-384 only (source read).

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| 7.1 | "Apple's current trust store lists about 150 roots" | "Apple's current trust store, for iOS 26 and later, lists about 155 roots" (§7.2 keeps "around 150") | https://support.apple.com/en-us/126047 ; https://support.apple.com/103272 | 2026-10-20 |
| 7.1 table + para | iOS user CAs "Trusted only if the user manually enables full trust" | Added: a root installed through MDM or Apple Configurator is trusted automatically | https://support.apple.com/en-us/102390 | 2026-10-20 |
| 7.1 | "(`MASTG-TEST-0285`, `0286`)" for a user CA in `base-config` | `MASTG-TEST-0286`; `0285` covers apps still running on Android 6 and earlier (its title: "Outdated Android Version Allowing Trust in User-Provided CAs") | https://github.com/OWASP/mastg/tree/master/tests-beta/android/MASVS-NETWORK | 2026-10-20 |
| 7.2 | "Kazakhstan told citizens to install a government root… browser vendors blocked it" | Kazakhstan's internet providers told users to install it; Firefox and Chrome blocked it | https://blog.mozilla.org/security/2019/08/21/protecting-our-users-in-kazakhstan/ | 2026-10-20 |
| 8.1 | OWASP's reasoning: "outage risk now outweighs the benefit, given Certificate Transparency and the other improvements" | "given advances in security such as the ones below, the risk of outages almost always outweighs the benefit". The cheat sheet doesn't name CT in that answer | https://cheatsheetseries.owasp.org/cheatsheets/Pinning_Cheat_Sheet.html | 2026-10-20 |
| 8.2 | "The MASTG tags its pinning tests for the `MAS-L2` profile" | MASTG v2 tests carry no profile tag. The weakness they check, `MASWE-0028` (Insecure Identity Pinning), is tagged L2 (plus EUDIW). Added a MASWE link | https://github.com/OWASP/maswe/blob/main/weaknesses/MASVS-NETWORK/MASWE-0028.md ; https://mas.owasp.org/MASWE/MASVS-NETWORK/MASWE-0028/ | 2026-10-20 |
| 8.5 | "WHOIS contact look-ups already ended on 15 July 2025" | "Methods that contact the domain's registered owner, found through WHOIS, already ended on 15 July 2025" (BR §1.2.2: methods 3.2.2.4.2 and 3.2.2.4.15 sunset, Ballot SC080) | https://github.com/cabforum/servercert/blob/main/docs/BR.md | 2026-10-20 |
| 8.5 | Persistent DCV record "that the CA re-checks at each issuance" | "The CA looks the record up again whenever its last check is more than 10 days old" (BR 3.2.2.4.22 caps reuse for this method at 10 days) | BR v2.3.1 §3.2.2.4.22 | 2026-10-20 |
| 8.10 | "`MASTG-TEST-0396` looks for delegates that weaken trust evaluation" | "…delegates that bypass certificate validation" (test title: "References to URLSessionDelegate Bypassing Certificate Validation") | https://github.com/OWASP/mastg/blob/master/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0396.md | 2026-10-20 |
| 8.10 table | TrustKit "last release June 2025" | "latest release 3.0.8, October 2026" (published 2026-10-14) | https://github.com/datatheorem/TrustKit/releases | 2026-10-20 |
| 8.11 | Cloud-provider row: "Pin the intermediate rather than the leaf *with* a backup at another CA" (pinning the intermediate doesn't fix a rotated intermediate) | "Ship a backup pin at another CA, or a root-level pin as a fallback, or move to dynamic pins (§8.6). Before pinning a provider's intermediate, ask how and when it rotates them" | Logical correction; see Judgment calls | 2026-10-20 |

Also added: an inline source for OkHttp 5.5 ECH (opt-in, Android 17 only), the OkHttp changelog dated 2026-08-16. Added Apple Platform Security as a second source for `X25519MLKEM768`. Added RFC 7518 §3.4 for the JWS ES256 raw `r‖s` encoding. Added the BR version (2.3.1).

Confirmed correct, with no change needed. Each item was checked on 2026-10-20 against the sources named.

**Android defaults and APIs** (network security configuration and behavior-change pages):
- The `debug-overrides` behavior ("completely ignored" when not debuggable).
- `overridePins` defaults to true inside `debug-overrides`.
- The `expiration` text ("thus disabling pinning").
- SHA-256 is the only digest.
- `includeSubdomains` matches subdomains at any depth.
- CT is off on API 36 and on for API 37, and is skipped for user and inline anchors.
- The `domainEncryption` element exists.
- Cleartext is off from API 28.
- TLS 1.3 is the default from Android 10.

**ECH and Android 17:**
- Android 17 turns on CT and ECH for apps targeting API 37.
- The library examples are HttpEngine, WebView, and OkHttp.
- RFC 9849 is the ECH RFC.
- iOS ECH is an experimental `sec_protocol_options` option, off by default.

**Apple TLS:**
- TLS 1.3 is the default from iOS 12.2.
- CT is required from iOS 12.1 for certificates issued after 15 October 2018.
- `X25519MLKEM768` is the default from iOS 26.

**Distrust and trust-store events:**
- Entrust: Chrome cutoff 11 November 2024 (earliest SCT); Apple cutoff 15 November 2024.
- Chunghwa Telecom and NetLock: certificates after 31 July 2025.
- The Android 14 Conscrypt updatable trust store.

**Libraries:**
- Conscrypt 2.7.0 (2026-08-31) made `X25519MLKEM768` the default.
- OWASP cheat sheet quotes.
- Google Android security-ssl quotes.

**OWASP MAS:**
- MASVS-NETWORK-2 text.
- Discussion #573 (May 2021; accepted by cpholguera).
- MASTG-KNOW-0015: "preferred and recommended way", "ensure timely updates", Flutter/Dart BoringSSL.
- MASTG-KNOW-0072: NSPinnedDomains recommended, subresources not covered.
- MASTG-TEST-0235, 0236, 0242, 0243, 0244, 0284, 0286, 0385.
- MASTG-TECH-0012 and 0064.
- MASTG-TEST-0022 and 0068 are deprecated, covered by the v2 tests.
- MASTG-DEMO-0057.

**HPKP:** deprecated in Chrome 67 and removed in Chrome 72.

**CA/Browser Forum:**
- SC-081v3: Apple proposed; Sectigo, Google, and Mozilla endorsed; no votes against (25 yes / 5 abstain among issuers; 4 yes among consumers).
- BR schedule: 200/100/47-day lifetimes and 200/100/10-day reuse, on 15 March 2026, 2027, and 2029.
- SC-088v3 effective 10 November 2025; the record names the CA and the `accounturi`.

**Apple identity pinning:**
- Subdomain example: `example.org`, `math.example.org`, `advanced.math.example.org`.
- The "cannot loosen" quote.
- The `SPKI-SHA256-BASE64` definition.
- NSPinnedDomains needs iOS 14 / macOS 11.
- Listing both CA and leaf pins requires a match in each.

**Apple trust APIs:**
- `SecTrustCopyCertificateChain` requires iOS 15.
- Deprecated: `SecTrustGetCertificateAtIndex` (iOS 15), `SecTrustCopyPublicKey` (iOS 14), `SecTrustEvaluate` (iOS 13).
- `tlsMinimumSupportedProtocolVersion` exists.

**Guardsquare:** the plist-removal attack and the Frida one-liner.

**OkHttp:**
- The repository moved to lysine-dev/okhttp, with docs at lysine.dev/okhttp. The Maven group is still `com.squareup.okhttp3`. 5.5.0 is the latest release.
- `*.`, `**.` and exact-host semantics; `**.` is called "the best way" for most applications.
- `sha1/` pins are accepted.
- The check runs after a successful handshake, before the connection is used.

**Ktor Darwin:** `usePreconfiguredSession` ignores `handleChallenge`.

**Other tools and libraries:**
- objection 1.12.x uses `-n`/`--name` (`-g` is deprecated).
- Wultra ssl-pinning-ios and ssl-pinning-android 2.0.0 were released on 2026-09-07.
- `certbot --reuse-key` exists.

**HTTP Toolkit:** the Android 17 CT post exists (September 2026).

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| Intro | DigiNotar certificates were used against users "mainly in Iran", cited to Google's 2011 post | Fetched the post, but the body didn't render, and only commenters mention Iran. Widely reported (Fox-IT's report); not re-confirmed from the cited source | Keep. Optionally add the Fox-IT report as a second source |
| 8.4 Trap | On 23 September 2026, `example.com` chained through Cloudflare and SSL.com "Transit" intermediates to an SSL.com root | `openssl s_client` had no network access in my sandbox | Author's dated observation; keep the date |
| 8.6 Evidence, 8.10 | Author's emulator, simulator, and macOS test results (WebView 152, iOS 26.5/27.0, Swift 6 on macOS 27) | Can't reproduce here | Already framed as `> **Evidence:**`; keep |
| 8.10 | "A framework can't pin this way on its own behalf" (`NSPinnedDomains`) | No Apple doc found that states it; searched docs and forums | Added *(reasoned)* |
| 7.3 | Rooted devices with a proxy CA in the system store stop working under Android 17 CT | HTTP Toolkit post implies it (all system-trusted certificates need SCTs) but doesn't state it for rooted devices | Kept *(reported)* |
| 7.3 | "Android hasn't documented a platform default" for post-quantum key exchange | Android 17 behavior changes page doesn't mention it; can't prove a negative | Keep as is; recheck at next pass |
| 8.11 | Android WebView: "`onPageFinished` fires anyway" after `onReceivedSslError` cancels | No primary source found quickly | Consider *(reported)* |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| 7.1 | "handshake" undefined | "the opening exchange of every TLS connection" |
| 7.1 | "certificate authority" defined only as a name | "an organization your platform trusts to check who owns a name" |
| 7.1 | "interception proxy" undefined | "a tool that sits between your app and the server and decrypts the traffic" |
| 7.1 | Four validation checks crammed into one sentence | Numbered list |
| 7.1 | MDM used in table before definition | Defined at first use in the table |
| 7.1 | iOS MDM-installed roots skip the manual trust switch | One sentence plus source |
| 7.3 | "Root programs" undefined | "the browser and OS vendors' rules for which CAs they trust" |
| 8.2 | HPKP named without acronym | "HTTP Public Key Pinning (HPKP)" |
| 8.4 | "cross-signatures" undefined | "one CA signing another CA's certificate" |
| 8.5 | CA/Browser Forum and Baseline Requirements undefined | One sentence defining both; forward pointer at first mention |
| 8.6 | "bootstrap pins" undefined | "the pins it uses before it has fetched anything" |
| 8.8 | "tokenized" undefined | "the app handles a stand-in value, not the card number" |
| 8.10 | DER undefined at first use in this file | "the exact binary format certificates use, so every platform hashes the same bytes" |
| 8.10 | Why the bootstrap pins in `PinnedClientProvider` prevent lockout | "A chain that matches any pin passes" |
| 8.10 | What "a DER wrapper for RSA" means | "the RSA algorithm identifier plus a bit string" |
| 8.10 | JWS acronym | "JSON Web Signature" |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| CONTRIBUTING.md | Style | It says "British spelling in prose", but editorial/PROMPT.md requires American. I followed PROMPT.md. Align CONTRIBUTING.md, or the next contributor will revert | Conflicting house rules |
| book/12-verification.md | Glossary: DNS-PERSIST-01 | "the CA re-checks it at each issuance" → "the CA re-checks it whenever its last check is more than 10 days old (BR 3.2.2.4.22 caps reuse for this method at 10 days)" | Same correction as §8.5 |
| book/12-verification.md | Glossary (spelling) | Glossary entries use British spelling (authorisation, behaviour); align with American if PROMPT.md is the rule | Consistency |
| book/12-verification.md | Correction log | Add a 2026-10-20 entry for the §7.1, §8.1, §8.2, §8.5, §8.10, and §8.11 corrections above | CONTRIBUTING.md step 2 |
| book/12-verification.md | Sources | Add the MASWE-0028 page, OkHttp changelog (lysine.dev/okhttp/changelog), and RFC 7518 if Sources is meant to be complete | New links in Part 3 |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Baseline Requirements | The CA/Browser Forum's rules that every publicly trusted CA must follow, including certificate lifetimes and DCV reuse periods | §8.5 |
| CA/Browser Forum | The body of CAs and browser and OS vendors that writes the Baseline Requirements by ballot | §8.5 |
| Bootstrap pins | The pins an app ships with and uses before it has fetched a signed pin manifest; kept as a floor under dynamic pins | §8.6 |
| Interception proxy | A tool that sits between an app and a server and decrypts the traffic, such as mitmproxy; works only if the device trusts its CA | §7.1 |
| MDM (mobile device management) | Software an organization uses to configure devices remotely; on iOS, a root it installs is trusted for TLS automatically | §7.1 |
| Root program | A browser or OS vendor's rules for which CAs it trusts, and the process for removing CAs that break them | §7.3 |
| HSM (hardware security module) | Dedicated hardware that holds signing keys so they can't be exported; recommended for a pin-manifest signing key | §8.6 |

## Judgment calls

**American spelling.** I applied American spelling throughout the prose, per PROMPT.md, although CONTRIBUTING.md says British. If the author keeps British, revert 27 word changes. They're listed by the diff; no URLs or code identifiers changed.

**§8.11 cloud-provider row.** I rewrote the advice because the original suggested pinning the intermediate as a fix for a rotated intermediate. The new text keeps the original's ideas (backup at another CA, dynamic pins, someone else's schedule) and adds a root-level fallback pin. The author may prefer different wording.

**§8.1 OWASP reasoning.** I removed the claim that the cheat sheet cites Certificate Transparency in its answer, and pointed to "the ones below" instead. CT remains in the book's own argument that follows.

**§7.1 trust-store count.** The count is now "about 155" (the iOS 26 store), while §7.2 keeps "around 150". Both are approximate, and the author may prefer one number in both places.

**Spaced em dashes in code comments.** I replaced them with colons or parentheses. The voice rules say comments follow prose style.

**Fixed headings and captions.** I left the "§8.6 …static, dynamic and hybrid" heading and its Figure 9 caption without a serial comma, because headings and captions are link targets and must not change.

**§8.8 intro.** I changed "Reason from the threat, not the table" to "not from this list", because §8.8 has no table.

**§8.8 messengers.** I replaced the idiom "the exception that proves the rule" with "a special case".
