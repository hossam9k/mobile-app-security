---
part: 12
last_verified: 2026-09-24
volatility: low
recheck_because: "The record itself; append rather than rewrite. The Sources list, the volatility table and the untested-claims table must be refreshed whenever a part is re-verified"
---

# Part 12: Verification

## Chapter 33: Audit log

This section exists so that nobody has to take the book on faith — including future readers, and including me.

In its first fortnight this book shipped a pinning snippet whose hash could never match, a DCV figure derived wrongly twice, and a "new in 2026" App Attest feature that dates from 2021. Each was found by someone checking the text against a primary source, and each is recorded below rather than quietly fixed. That is the point of the chapter: a reference whose errors are invisible is harder to trust than one that shows them.

**How to read this log.** Entries are in date order. Earlier entries are kept as written; where later work proved one wrong, it carries a *(superseded 2026-09-24: …)* note instead of being deleted. The most recent full verification is [the 23–24 September 2026 audit](#full-audit-and-rewrite-2324-september-2026), which covers Parts 0–9, Part 11 and this part; Part 10 is recorded there separately. A final read-only verification pass over every file followed on 24 September, and is the last of its log lines.

### Verified against primary or authoritative sources (10 September 2026)

This is the table as it stood on 10 September. Rows that the September audit corrected are annotated in place; the current table is [in the audit section](#verified-claims-24-september-2026).

| Claim | Status |
|---|---|
| Breach cost $4.99M global, $11.5M US, 247-day mean time, one in four malicious breaches AI-enabled averaging ~$6M | IBM *Cost of a Data Breach 2026*, released 29 July 2026, 602 organisations breached March 2025 – February 2026. *(checked 2026-09-24: IBM's own press release uses exactly this framing, "one in four malicious breaches" at "$6 million on average"; IBM's landing page phrases it by organisation. Parts 1 and 11 both now follow the press release: one in four, up 56% on the year)* |
| 2024 was $4.88M; 2025 fell to $4.44M; 2026 rose to a record | IBM 2025 and 2026 editions |
| 28.65M new secrets on public GitHub in 2025, +34%, +152% since 2021; AI commits 3.2% vs 1.5% *(superseded 2026-09-24: 3.2% is for Claude Code-assisted commits, identifiable by the co-author trailer the tool adds, against 1.5% across all public commits — not AI commits in general, and not a human-only baseline)*; 24,008 secrets in MCP configs; 64% of 2022 secrets still valid; 59% of compromised machines were CI runners; 28% of incidents outside repositories | GitGuardian *State of Secrets Sprawl 2026*, 5th edition, 17 March 2026 |
| MASVS v2.1.0 current; 8 categories, 24 controls; levels replaced by MAS-L1/L2/R testing profiles in the MASTG; OWASP cannot certify apps *(superseded 2026-09-24: there are four base profiles, L1, L2, R and P, plus the specialised MAS-EUDIW, now published at mas.owasp.org/Profiles; L1 is the baseline for every app. OWASP's wording is that it "does not certify any vendors, verifiers or software")* | mas.owasp.org/MASVS, read 10 September 2026 |
| MASTG v2.0.0 first stable non-beta release; MASWE introduced July 2024; MAS Test Apps and Crackmes exist | OWASP/mastg releases. *(superseded 2026-09-24: MASTG v2.0.0 was released on 30 June 2026 and deprecates every v1 test; MASWE left beta with v1.0.0 on 17 August 2026)* |
| All 24 control IDs, all 78 MASWE weakness titles *(superseded 2026-09-24: MASWE v1.0.0 renumbered every ID once on 17 August 2026; Part 9 now uses v1.0.0 numbering, re-checked against the live catalogue)*, and the test, technique, best-practice and demo catalogues in Part 9 | Read directly from mas.owasp.org, 10 September 2026. IDs and weakness titles as published; one-line control explanations are this book's summaries, not normative text |
| Mobile Top 10 updated late 2024, first update in eight years, separate working group | Guardsquare, OWASP |
| Jetpack Security Crypto deprecated April 2025 at 1.1.0-alpha07, no further releases; per-class replacements as stated *(superseded 2026-09-24: a deprecated stable 1.1.0 followed on 30 July 2025, and Google now ships `androidx.datastore:datastore-tink`)* | developer.android.com reference |
| Keystore architecture: keystore2 in Rust, keyblobs storable but not usable by the daemon, KeyMint replacing Keymaster, TEE trusted app holds raw key material, Gatekeeper for auth-bound keys, Trusty as Google's TEE *(superseded 2026-09-24: Gatekeeper verifies PIN, pattern and password only; biometric auth tokens come from the biometric trusted app)* | source.android.com/docs/security/features/keystore |
| SecurityLevel values SOFTWARE / TRUSTED_ENVIRONMENT / STRONGBOX; `isInsideSecurityHardware()` for API ≤28 *(superseded 2026-09-24: `getSecurityLevel()` is API 31+ with five constants, including `UNKNOWN_SECURE` and `UNKNOWN`; the older method is `isInsideSecureHardware()`, for API ≤30)*; StrongBox from Android 9, eSE or iSE, reduced algorithm subset | developer.android.com/privacy-and-security/keystore |
| Key attestation from Android 7 (Keymaster 2), ID attestation from Android 8 (Keymaster 3); authorization list generated in secure hardware, not platform-controlled | source.android.com/docs/security/features/keystore/attestation |
| New RKP root activated 1 February 2026, mandatory for RKP devices by 10 April 2026; verifiers not trusting it will fail; chain longer and subject to change; root moving RSA → ECDSA | Practitioner analysis and Google guidance as cited. *(superseded 2026-09-24: Google's page gives only the 1 February 2026 start of the ECDSA P-384 "Key Attestation CA 1"; the 10 April date is practitioner-reported; factory-keyed devices stay on the RSA root, so verifiers must trust both. The comviva.com source was replaced by Google's own)* |
| iOS Keychain: single SQLite database, securityd, entitlement-based access, metadata key cached in AP, per-row secret key always via Secure Enclave, ACLs evaluated inside the Secure Enclave | support.apple.com keychain data protection |
| Secure Enclave provides Data Protection key management and maintains integrity even if the kernel is compromised; EC keys only; signing and key agreement rather than direct encryption *(superseded 2026-09-24: P-256 through the Security framework, and since iOS 26 CryptoKit also offers ML-KEM and ML-DSA keys in the Secure Enclave)* | Apple platform security documentation and practitioner sources |
| Data Protection class mappings: WhenUnlocked ↔ NSFileProtectionComplete, AfterFirstUnlock ↔ CompleteUntilFirstUserAuthentication, Always ↔ None; Always discouraged *(superseded 2026-09-24: `Always` has been deprecated since iOS 12)* | Apple documentation, practitioner analysis |
| Certificate lifetimes: 398 → 200 days from 15 March 2026, 100 from 2027, 47 from 2029; DCV reuse to 10 days; Ballot SC-081v3 approved April 2025, proposed by Apple, adopted with no votes against | CA/Browser Forum, confirmed by multiple CAs. **Vote tallies differ between sources** — one reports 29–0, another 25–0 with 5 abstentions — so no precise count is stated. *(superseded 2026-09-24: cabforum.org gives certificate issuers 25 yes, 0 no, 5 abstain, and certificate consumers 4 yes. "No votes against" stands)* |
| Play Integrity May 2025 changes: hardware-backed verified boot for device integrity and 12-month security update for strong integrity on Android 13+; ~90% signal reduction; up to 80% latency improvement; repeated decryption returns cleared verdicts *(superseded 2026-09-24: Google says a token cannot be "reused many times" and gives no threshold)*; library 1.5.0 remediation dialogs; SafetyNet retired | developer.android.com Play Integrity documentation |
| App Attest: attest contacts Apple and assertions do not; counter must be strictly increasing; fraud metric, iOS 27 signals and macOS 27 support new in 2026 *(superseded 2026-09-24: the fraud metric dates from WWDC21; the 2026 additions are the iOS 27 authenticator-data extensions and macOS 27 support)*; do not reject every new key for an existing user | WWDC26 Session 201 |
| CI/CD incidents *(superseded 2026-09-24: tj-actions/changed-files was 14–15 March 2025 and dumped secrets into public workflow logs rather than exfiltrating them; trivy-action was a separate incident on 19 March 2026; TanStack's provenance claim is reported by Snyk and StepSecurity, not by TanStack's post-mortem. Each incident is now sourced to its own advisory or post-mortem in §15.1)*: tag-retargeting of tj-actions/changed-files and trivy-action (19 March 2026); Shai-Hulud runners named SHA1HULUD and exfiltration repos; TanStack cache poisoning with 84 versions across 42 packages carrying valid SLSA L3 provenance; GhostAction 327 accounts and 3,325 secrets; Megalodon 5,718 commits to 5,561 repos | GitHub Security Blog and practitioner analysis |
| `GITHUB_TOKEN` defaults to read-write in repositories created before February 2023 *(superseded 2026-09-24: from 2 February 2023, new enterprises, organisations and personal repositories default to read-only; existing ones kept their setting, and repositories inherit their organisation's)* | Actions hardening guidance |
| Play App Signing split key model; stolen upload key cannot re-sign the app | Android signing guidance |
| KMP adoption rose from ~7% to 18–23% in a year *(superseded 2026-09-24: 7% (2024) to 18% (2025) of JetBrains Developer Ecosystem respondents; the 23% had no source)* | Kotlin ecosystem reporting |

### Corrections made during writing

| Was | Now |
|---|---|
| Breach cost $4.88M (IBM 2024) | $4.99M (IBM 2026), with the 2025 dip noted so the trajectory is not misrepresented |
| 12.8M secrets leaked (2023 figure) | 28.65M new secrets in 2025 |
| Stolen credentials 16% of breaches, 292 days (2024 figures) | 2026: 247-day mean time; supply chain second most common vector at 258 days |
| "Android Keystore + Tink" via `EncryptedSharedPreferences` | Library deprecated April 2025. DataStore + Tink + Keystore `KeyGenerator` |
| "MASVS L2" | "MAS-L2 profile" — levels moved into the MASTG at v2.0.0 |
| Pinning rotation framed against ~398-day certificates | 200 days now, 47 by 2029; rotation strategy needs rebuilding around key reuse or intermediate pinning |
| App Attest guidance predating WWDC26 | Fraud metric, iOS 27 signals, macOS 27, new-key guidance *(superseded 2026-09-24: the fraud metric was not new)* |
| Attestation root treated as static | New RKP root from 1 February 2026, mandatory 10 April 2026 *(superseded 2026-09-24: the 10 April date is reported, not in Google's documentation)* |

### Structural and factual audit (10 September 2026)

A structural and factual audit was run on the finished text. What it checked and found:

**Structure.** 12 parts, 34 chapters, no numbering gaps, no duplicates. All 29 numbered cross-references resolve to existing chapters — two were found broken during the audit (references to the MASWE catalogue pointing at the wrong chapter after a renumbering) and fixed.

**Standard coverage.** All 8 MASVS categories and all 24 control IDs are cited, with no ID above its category maximum. 42 distinct MASWE weaknesses cited, none above the catalogue's 78. 44 MASTG tests, 35 best practices, 20 demos, and the technique families.

**Test IDs.** A sample was verified against the live MASTG: `MASTG-TEST-0250` through `0253` (WebView content-provider and file-access, static and runtime), `0334` (native code through WebViews), `0370`/`0371` (custom URL scheme input and source validation), `0372`–`0375` (implicit intents) and `0376`–`0380` (iOS native methods through WebViews) all match their cited use, as does `MASTG-BEST-0011`. **One error was found and corrected:** `MASTG-TEST-0044` and `0087` were cited as current tests for compiler security features; both are deprecated v1 tests. Chapter 3 now carries a general warning about v1 versus v2 test IDs.

**Links.** 58 unique URLs, none malformed; the largest source is `mas.owasp.org` (16), then `developer.android.com` (9).

**Hygiene.** No TODO markers, no unfilled placeholders, no unbalanced formatting.

**What the audit did not do:** verify all 44 test IDs individually against the live MASTG, or re-fetch every one of the 58 external URLs. A sample was checked. Treat any single ID as a pointer to look up rather than as verified fact, and check the test page for a deprecation banner.

### Drafting pass: certificate lifetimes and the pipeline (10 September 2026)

**Static versus dynamic pinning (§8.6).** Verified: the `pin-set expiration` attribute exists and its effect is fail-open — after the date, pinning is no longer enforced and normal validation applies, which OWASP's own `MASTG-KNOW-0015` guidance addresses by telling you to set a date *and* keep it updated. Verified: Android applies network security configuration rules to WebView traffic in the same app automatically *(confirmed on an Android 17 emulator on 2026-09-23, which also showed the configuration covers OkHttp)*. Verified: the dynamic-pinning architecture of bootstrap pins plus a signed manifest whose signing key sits outside the web PKI, as implemented by open-source libraries such as Wultra's `ssl-pinning-ios` and sold as a managed service by several vendors. The monotonic-version requirement in the client logic is this book's own reasoning, by analogy with App Attest's assertion counter — it is sound but it is not quoted from a standard.

**Implementation sections.** The Android network security configuration syntax, the OkHttp `CertificatePinner` API, and the iOS `URLSessionDelegate` pinning pattern were each checked against current sources. Two API currency points were confirmed and applied: `SecTrustCopyCertificateChain` should be used rather than the deprecated `SecTrustGetCertificateAtIndex` and `SecTrustCopyPublicKey`, and chain evaluation with `SecTrustEvaluateWithError` must happen *before* pin comparison. The remaining snippets — Keystore `KeyGenParameterSpec`, GCM encryption, `BiometricPrompt` with `CryptoObject`, WebView settings, `PendingIntent` flags, content-provider parameterisation, path canonicalisation, `NSKeyedUnarchiver` with secure coding — are standard platform APIs written to current documented usage but **not individually re-verified against a compiler.** *(superseded 2026-09-24: WebView settings and file-access defaults are now verified against the reference pages; the `NSKeyedUnarchiver` sample was replaced with `unarchivedObject(ofClass:from:)` and Codable; the Part 3 Swift and Kotlin pinning listings were compiled and run; the Part 5 detection snippets and the §6.7 SQLCipher snippet (Part 2) were compiled but not run. The remaining snippets are still not compiled.)* Treat them as correct in shape and check against the platform docs before shipping.

### Drafting pass: the programme layer (10 September 2026)

**Part 11, the programme layer.** Earlier drafts rewrote the technical content of the strategy documents and dropped the executive layer entirely — the business case, regulatory position, industry comparison, phased plan, effort estimates, ownership and success criteria. That was an error, and Part 11 restores it.

All figures in it were re-verified rather than carried forward, and several had moved:

| Was, in the strategy documents | Now verified |
|---|---|
| Breach cost $4.88M (IBM 2024) | **$4.99M** (IBM 2026, a record, +12%); trajectory noted because 2025 *fell* to $4.44M |
| Healthcare $9.77M | **$6.64M** — still costliest sector for the 13th consecutive year, but down 10.5% from $7.42M in 2025 |
| — | **Financial services $6.29M**, now second and closing the gap |
| Credentials 16% of breaches, 292 days | **247 days** mean time to identify and contain, up, reversing five years of improvement |
| 12.8M secrets leaked (2023) | **28.65M** new secrets in 2025, up 34% |
| "Capital One lost $190M+" | **$190M class-action settlement** — a settlement, not a fine. The distinction matters because private litigation is a separate exposure from regulatory action |
| Meta €1.2B fine | **Verified**: Irish Data Protection Commission, May 2023, largest GDPR fine to date, for EU→US transfers without adequate safeguards; Meta appealed. Cumulative GDPR fines have passed €7.1B since 2018 |
| "$50,000–$500,000 per incident" | **Removed.** This is an estimate with no traceable basis. §29.4 gives a method for deriving your own exposure instead |

**What is explicitly not verified.** Chapter 31's company-specific practices. The strategy documents asserted particular architectures at named banks, ride-sharing, messaging and e-commerce companies. Those are not publicly confirmed internal designs, so Chapter 31 presents them as **patterns observable from the outside** — from platform documentation, published engineering writing, app behaviour and regulatory requirements — and says so in the chapter, not just here. Do not restate them as facts about a named company.

**Effort estimates** (18–26 engineering days initial, ~6 days annual maintenance) are planning figures carried from the strategy documents and labelled as estimates in §32.3, not measurements.

**Readability pass.** Interrupting paired em-dash asides were reduced from 52 to 29, and 26 teaching sections that previously opened straight into a list now open with a framing sentence. Nine acronyms used in the text but missing from the glossary were added, including MITM, PKI, HAL and KMP.

### Drafting pass: domain validation and pin types (10 September 2026)

This revision started from a question the book could not answer: what is "domain validation reuse"? Chasing it down found two errors and three gaps.

**Two errors corrected.**

*The vote count on Ballot SC-081v3.* Three places stated "29 votes in favour and none opposed." Sources disagree — one reports 29–0, another 25 in favour, 0 against, 5 abstentions. The precise count is now removed and replaced with "adopted with no votes against," which every source supports. The discrepancy is disclosed in the table above rather than resolved silently.

*The validation arithmetic.* *(superseded 2026-09-24: this correction was itself wrong. Baseline Requirements §4.2.1 counts the reuse period back from each issuance, so validation does not run on a rolling 10-day cycle and nothing needs re-validating when no certificate is issued. With 10-day reuse the practical effect is roughly one fresh validation per issuance, not 35 to 37 a year. §8.5 and the DCV glossary entry now say so.)* §8.5 previously said "the proof-of-control mechanism runs roughly five times per certificate," derived from 47 ÷ 10. **That reasoning is wrong.** DCV evidence expires every 10 days regardless of when you renew, so validation runs on a rolling cycle independent of certificate replacement — roughly 35 to 37 times a year per domain, against about eight certificate renewals. Three independent sources give 35, "up to 37", and 36. The correct figure was already in the chapter's opening paragraph; the incorrect derivation sat four paragraphs later, contradicting it. Both now say the same thing, and the mechanism is explained.

**Three gaps filled.**

*Domain validation is now taught before it is used.* §8.5 previously used "domain validation reuse" as a table column heading with no definition anywhere in the book. It now explains what DCV is, the methods (`DNS-01`, `HTTP-01`, and that WHOIS email validation was discontinued on 15 July 2025) *(superseded 2026-09-24: SC-080 ended WHOIS-based contact lookup on 15 July 2025; SC-090 retires the remaining email and phone methods on 15 March 2027 and 15 March 2028)*. And the part that makes the table readable: certificate lifetime and DCV reuse are **two separate clocks doing two different jobs.**

*Persistent DCV.* `DNS-PERSIST-01`, introduced by Ballot SC-088v3 and permitted since November 2025, re-validates against a single standing TXT record at `_validation-persist` with no per-renewal DNS change. It is the practical answer to the 35-validations-a-year problem and was entirely absent. *(superseded 2026-09-24: there is no 35-a-year problem, see above; persistent DCV removes the per-issuance DNS change. Let's Encrypt supported it in staging only as of mid-2026.)*

*The ACME counterweight.* Research at the ACM Web Conference 2025 showed stolen ACME account credentials can yield fraudulent certificates without the attacker controlling the domain, due to validation caching. A book that recommends ACME automation owes the reader that caveat.

**Pin types (§8.4).** The chapter asserted "pin the SPKI, never the certificate" without ever naming the three things people call pinning. It now distinguishes certificate pinning, public key / SPKI pinning and CA pinning, explains *why* certificate pinning breaks on every renewal even with a reused key (it pins the expiry date and serial number too), and answers three questions that kept coming up: the digest is SHA-256 and on Android it is the only accepted value; DV/OV/EV validation levels are irrelevant to pinning because you pin a key; and self-signed or private-CA pinning is legitimate for internal apps but forfeits Certificate Transparency as a fallback.

**Evidence markers.** The book carries *(reported)*, *(estimate)*, *(reasoned)* and *(contested)* markers on claims that are weaker than they look, with the convention declared in the front matter. Fourteen claims are marked. Everything unmarked traces to a primary or authoritative source.

**A source conflict left open rather than hidden.** One source attributes the 10-day DCV reduction to "Ballot SC-70" with a 2028 date, against SC-081v3 and 2029 in every other source consulted. The majority position is stated; the outlier is noted here.

**Terminology normalised.** "Android KeyStore" in prose became "Android Keystore" (the capitalised form is the Java class name and remains in code), and "threat-model" became "threat model".

**What this pass did not do.** The book contains 439 bolded numeric claims, 48 percentages, 50 money figures, 47 day-counts, 187 OWASP identifiers and 60 external links. These were **not** individually re-verified against primary sources in this pass — doing so is a multi-week exercise, and claiming otherwise would be the specific kind of overstatement this chapter exists to prevent. What was done: every claim in Chapter 8 was re-derived from sources, the evidence markers above were applied across the book, and the structural checks (numbering, cross-references, terminology, glossary coverage) were run mechanically over the whole text. Treat unmarked figures as sourced but not re-confirmed this month.

### Drafting pass: platform differences in pinning (10 September 2026)

An earlier draft treated dynamic pinning as platform-neutral across §8.6 and §8.10, which hid a real asymmetry between Android and iOS. Verification also found the iOS declarative mechanism missing entirely.

**`NSPinnedDomains` was absent.** Apple's **Identity Pinning**, available since iOS 14 and macOS 11, configures pinning declaratively in `Info.plist` under `NSAppTransportSecurity`. It is the direct counterpart to Android's network security configuration and the book never mentioned it. Now documented in §8.10 with the `NSPinnedCAIdentities` versus `NSPinnedLeafIdentities` distinction and five verified limitations: `NSIncludesSubdomains` covers only one subdomain level; values must be duplicated in every `Info.plist` and per host; User Defined Settings variables cannot be used in a localized `Info.plist`; it does not apply to `WKWebView` or `SFSafariViewController`; and a changed entry may need an app reinstall before ATS invalidates the cached trust setting. *(superseded 2026-09-24: the User Defined Settings limitation was unsupported and has been removed; the `WKWebView` claim is supported by iOS 26.5 and 27.0 simulator tests; the reinstall claim was not reproduced on simulators and stays (reported).)*

**Verified and worth the cross-check:** `SPKI-SHA256-BASE64` on iOS is the base64-encoded SHA-256 digest of the DER-encoded ASN.1 SPKI structure — the same value Android's `pin digest` takes. If the two platforms' pins differ for one endpoint, one is wrong.

**The platform asymmetry, now in §8.6.** On both platforms the declarative mechanism **cannot be updated at runtime**, so choosing dynamic pinning means giving up declarative pinning and what it provides. The consequence differs:

- **Android:** the network security configuration covers WebView traffic in the same app automatically. OkHttp's `CertificatePinner` does not. So moving to dynamic pinning **silently unpins your WebView**, and you must either keep a static configuration alongside it or intercept WebView requests yourself.
- **iOS:** neither `NSPinnedDomains` nor a `URLSessionDelegate` covers `WKWebView`, because `WKWebView` does not route through your session. iOS offers no supported way to pin WebView traffic at all, which makes it an architectural problem rather than a configuration one. *(superseded 2026-09-24: `WKNavigationDelegate` does receive server-trust challenges, but only for new connections and with undocumented subresource coverage, so §8.6 now calls it best effort rather than impossible.)*

**`CertificatePinner` immutability.** It cannot be modified after construction, so dynamic pinning on Android means rebuilding the pinner and client on a new manifest, or writing a custom `X509TrustManager`. §8.10 now shows the rebuild pattern, keyed on manifest version so the connection pool survives, and retaining the bootstrap pins as a floor so a bad manifest cannot lock you out of your own backend *(reasoned)*.

**A security trade-off now stated.** Declarative pinning is easy to audit and easy to strip — researchers have published removing `NSPinnedDomains` from an `Info.plist`, re-signing and installing with pinning gone, and the same applies to a repackaged APK's network security configuration. Code-based pinning costs more to remove. This matters only where the threat model includes redistributing a modified build to other users; against an attacker on their own device, Chapter 1 still applies.

### Drafting pass: recovering the source material (11 September 2026)

A full read of the strategy documents was carried out at this point, having previously been only partial: document 01 in full, with 02, 03 and 04 sampled by heading. Earlier drafts were built largely from independent research rather than from those documents. The full read found **eight substantive topics present in the strategy documents and absent from the book**, all now added.

| Recovered | Where it now lives |
|---|---|
| **Backend-for-Frontend pattern** — a thin backend owning all secrets and trust decisions | §12.3, with the honest cost of the extra service stated |
| **Kotlin Multiplatform pinning with Ktor** — pins in `commonMain`, enforcement per engine | §8.10, including the trap that **Ktor does not pin automatically** and a project configuring one platform is open on the other *(superseded 2026-09-24: Ktor's Darwin engine has a built-in `CertificatePinner`; you still configure each engine)* |
| **Pinning troubleshooting** — ten symptom-to-cause-to-fix rows | New §8.11 |
| **Asset classification and threat-likelihood tables** | New Chapter 0.6, as fill-in tables supporting the threat-model method in Chapter 0.5 |
| **Local database encryption** — SQLCipher, Data Protection classes, and what neither solves | New §6.6 (now §6.7) |
| **Certificate Transparency monitoring, concretely** — `crt.sh`, inventory, and who receives the alert | §8.9 |
| **Attacker tooling table** — what each tool actually gives an attacker | §13.2 |
| **Stakeholder objection handling** — nine questions with answers | New §32.7 |

**Pros and cons tables added where prose alone required holding too much in mind at once:** static versus dynamic versus hybrid pinning; the three Android pinning mechanisms; and the three iOS pinning mechanisms, which also introduced **TrustKit** — a library the book had never mentioned despite being a reasonable first step for a team new to pinning.

**Where the strategy documents' answers were updated rather than copied.** The originals stated Play Integrity Classic adds "~2–3 seconds" and Standard "~300–500ms"; §32.7 states standard requests add a few hundred milliseconds after warm-up, per Google's own documentation, and flags that quota figures are practitioner-reported *(superseded 2026-09-24: Google documents the quotas; see §9.2)*. The originals cited "5–10% of Android users have rooted devices" as fact; §32.7 says "a meaningful share" because that figure has no primary source I could verify. *(superseded 2026-09-24: §32.7 now cites Google's documented Play Integrity quotas and Apple's App Attest rate guidance, separates token latency from warm-up latency, and says "some" users run rooted devices, marked (reasoned; no reliable primary figure).)* The originals' secret-classification table is preserved in substance in §15.2 and now cross-referenced from §12.3.

### Drafting pass: the systematic strategy-document diff (11 September 2026)

An earlier audit note in this chapter claimed a full read of all 4,354 lines of the strategy documents. That claim was not accurate: document 01 had been read in full, while 02, 03 and 04 were sampled by heading.

So this revision began with a **mechanical diff** rather than a judgement call about what mattered: every heading in all four strategy documents, with its body, keyword-matched against the book. **176 sections analysed. 99 covered, 28 partial, 49 likely missing.**

**The pattern behind the 49 is more useful than the list.** The rewritten text was concept-strong and implementation-thin; the strategy documents were the reverse. Earlier drafts carried across the "why" and dropped most of the "how" — an earlier revision addressed this by adding six implementation sections, when the strategy documents contained roughly forty.

**Recovered in this pass:**

| Topic | Now at | Why it mattered |
|---|---|---|
| App Attest limits and the when-to-check-integrity table | §10.5 | The rate limit and the nine-action table were the most directly actionable artefacts in the whole source set |
| Backend risk scoring, with weights | §12.5 | The book argued for a risk score throughout drafting without ever showing one |
| Impossible-travel detection | §12.5 | Absent entirely, including the recommendation to prefer backend IP geolocation over device GPS |
| Root, debugger, emulator, jailbreak and hooking detection | §14.4 | The book said "detect and report" with no detection code at all |
| Screenshot, logging, clipboard, session-timeout and database-encryption implementations | §6.6, §6.7, §14.5 | Five controls that appear in every assessment, previously described but not shown |
| R8 security rules, iOS strip settings, debug/release separation, build-time secret injection | §15.8 | Including the insight that inverts normal keep-rule advice: **do not keep your detection classes** |
| SDK data-access auditing via `AppOpsManager.OnOpNotedCallback` | §18.4 | Has the OS tell you what your SDKs read, rather than trusting their documentation |

**Two places the strategy documents were more rigorous than the rewritten text.** It labelled the App Attest rate limit as community-reported rather than Apple's figure, and noted there is no official SLA — the same caution the book applies elsewhere and had dropped here. Credit where due. *(superseded 2026-09-24: Apple does publish rate guidance — keep `attestKey` below about 100 requests per second across all installs and ramp at no more than 10 million users a day — so §10.5 now cites it.)*

**What remains outstanding, stated plainly rather than quietly closed.** Of the 49 flagged sections, roughly 19 are full working implementations for concepts the book already explains — Tink initialisation, the iOS Keychain helper, the Play Integrity and App Attest client classes, the Secure Enclave manager, the biometric managers, TrustKit configuration, the Ktor backend verification, Dependency-Check setup. The book gives correct shapes for these; the strategy documents give complete, compiling code. A future revision should either absorb them or state explicitly that the Implementation Guide remains the companion document for working code. It is the latter today.

### Independent audit and remediation (11 September 2026)

The book was audited against a written verification prompt designed to catch the failure modes of its own drafting. It found a defect that eight self-reviews had missed.

**The defect: 56 of 152 section numbers did not match their chapter.** When chapters were renumbered during drafting, the script rewrote `## Chapter N` headings and prose cross-references but not the `### N.M` section headings. Ten chapters were affected. Chapter 20 (AI features) contained sections numbered 16.x while Chapter 16 (WebViews) contained 19.x, so a reader following a cross-reference landed in the wrong chapter. Two references were confirmed broken: `§17.5` and `Chapter 23.6`.

Why the earlier self-checks missed it: they tested for *duplicate* and *gap-free* numbering. The numbers were unique and sequential — attached to the wrong chapters. The check was wrong, not just the output. The audit now verifies each section number against its parent chapter, and all 152 match.

**Also remediated in this pass:**

| Finding | Before | After |
|---|---|---|
| Section numbers mismatched to chapters | 56 of 152 | 0 |
| Unresolved cross-references | 3 | 0 |
| Interrupting paired em-dash asides | 33 | 1 |
| Em dashes per 1,000 words | 12.0 | 10.7 |
| Acronyms used but not in the glossary | 9 real | 0 |

The nine acronyms added were ASN.1/DER, GPS, MAC, SSL, TXT and WHOIS. *(superseded 2026-09-24: that list names seven terms, not nine; the other two were not recorded. The 10 September pass also claimed nine, including MITM and PKI.)* `SSL`, `DER` and `ASN.1` mattered most: the SPKI explanation used "DER-encoded ASN.1" without defining either term, in a book written for readers without a security background.

The interrupting-aside count had **risen** from 29 to 33 between passes, because material added later reused the habit that an earlier pass had corrected. Worth noting as a pattern: a style fix does not hold unless it is re-measured after every addition.

**Evidence markers were added** to claims introduced late and left untiered: the session-timeout recommendations, the detection-signal design, and the R8 keep-rule reasoning.

**A finding that turned out to be a false positive.** Ten sections were flagged as opening into a list with no framing sentence. On inspection all ten are source lists and audit tables in Chapter 33, where a framing sentence would add nothing. Recorded rather than silently dropped.

**What the audit did not do**, restated here because the audit's own output insisted on it: the currency check was not re-run, so no API, version or statistic was re-verified against a live source in this pass. Evidence tiering was checked for presence of markers, not applied claim by claim across roughly 500 claims. The "can a reader actually implement this" check was not run, and the 27 still-missing source sections suggest it would fail for the controls listed below. *(superseded 2026-09-24: nothing is listed below, and the 27 is not derived anywhere in this log; the 11 September diff flagged 49 sections, of which roughly 19 implementations remained outstanding, as the previous entry says.)*

### Full audit and rewrite (23–24 September 2026)

Every earlier entry in this log ends with a paragraph on what that pass did *not* do, and the same gap recurs: currency was not re-checked, code was not compiled, and IDs were sampled rather than read. This audit set out to close that gap. Each part was given to a separate auditor with one brief: classify every factual claim, API, version, date, statistic, ID and link as correct, stale, wrong or unsourced against a primary source; fix the wrong and the stale; compile the code where possible; and rewrite for teaching, with a hook, **Key takeaways** and **Try it** in every chapter.

**In total:** about 1,175 claims and identifiers checked across Parts 0–9 and 11, and roughly 205 wrong or stale statements corrected, not counting the deprecated MASTG test IDs replaced throughout. For the first time, four of the book's untested claims were put to an experiment (see [the untested-claims table](#claims-this-book-asserts-but-has-not-empirically-tested)).

> **Why it matters:** several of the errors below were in code, not prose. An iOS pinning delegate that can never match its own pins, or a biometric flow the server cannot verify, would have shipped into readers' apps. A reference book's errors propagate.

#### Part by part

| Part | What was verified | Counts | Most important corrections |
|---|---|---|---|
| Start here, 0, 1 | RFCs, NIST, developer.android.com, Apple DocC, the MAS repositories, IBM, Verizon, GitGuardian, OWASP cheat sheets | ~180 claims: ~130 correct, 24 stale, 11 wrong, 15 unsourced; 35 corrections | The MASVS→MASWE→MASTG example chain cited a deprecated test (`MASTG-TEST-0001` → `0287`). MAS profiles are four (L1, L2, R, P) plus MAS-EUDIW, and L1 is the baseline for *every* app. GitGuardian's 3.2% is Claude Code commits, not AI commits generally. TLS 1.3 does not use RSA key transport. `MASTG-TEST-0309`/`0310` are placeholders. OAuth guidance brought to RFC 9700, Auth Tab and `ASWebAuthenticationSession` `https` callbacks. IBM links replaced with the report itself |
| 2 (Ch 4–6) | source.android.com, Keystore and DataStore references and release notes, the Android 16 CDD, Apple Platform Security, Tink, DataStore and SQLCipher source | ~95 claims; 31 corrections, 14 newly sourced, 3 cross-references fixed; new §4.6 | Gatekeeper verifies PIN, pattern and password, not fingerprints. `getSecurityLevel()` is API 31+ with five constants. `ThisDeviceOnly` items *are* backed up, bound to the device UID. `EncryptedSharedPreferences` got a deprecated stable 1.1.0, and `datastore-tink` now exists. Tink's `AndroidKeysetManager` silently stores keysets in cleartext when its Keystore self-test fails. SQLCipher moved to `net.zetetic:sqlcipher-android`. The RKP root change sourced to Google, with 10 April marked *(reported)* |
| 3 (Ch 7–8) | CA/Browser Forum ballots and Baseline Requirements v2.3.0, the network security configuration docs, Apple docs and forums, OkHttp and Ktor source, RFC 9849; every Swift listing compiled and run with Swift 6, Kotlin listings compiled and run | ~160 claims; 14 errors (4 breaking code or behaviour), 19 stale, 11 newly sourced, 3 removed; 12 code blocks; new §7.3 | The iOS pinning delegate hashed the raw key, not the SPKI, so it could never match; replaced with a tested `SPKIPin` helper. DCV arithmetic corrected against BR §4.2.1. The network security configuration covers OkHttp and WebView, and `CertificatePinner` installs no trust manager. Android 17 turns on CT and ECH for apps targeting API 37. Ktor's Darwin engine has a built-in `CertificatePinner`. NSC XML samples put a comment before the XML declaration, making them invalid |
| 4 (Ch 9–12) | Play Integrity verdicts, setup, standard, classic, remediation and release notes; Apple DeviceCheck and LocalAuthentication docs; WWDC21 and WWDC26 transcripts; AOSP authentication | ~85 claims: ~52 correct, 14 stale, 12 wrong, 7 unsourced; 26 corrections; new §9.6, §10.7, §11.7 | Play Integrity quotas are documented, not practitioner-reported. `MEETS_BASIC_INTEGRITY` and `MEETS_STRONG_INTEGRITY` are opt-in. The App Attest fraud metric dates from WWDC21. Apple does publish rate guidance (~100 requests per second, ramp ≤10 million users a day). `retryAfter` does not exist. The biometric example "verified" a symmetric-key output the server cannot check; it now signs with an EC key. Enrolment invalidation stops applying with `AUTH_DEVICE_CREDENTIAL`. The Frida verification script could not force success |
| 5–6 (Ch 13–15) | Incident post-mortems and advisories, GitHub changelogs and docs, SLSA, AGP release notes, the MASTG repository; Swift snippets type-checked against the iOS 27 SDK and Kotlin against `android-37` | ~65 claims plus every cited MASTG technique, demo, test and best-practice ID | Trivy's root cause was a non-simultaneous credential rotation, not a token "taken weeks earlier". `setup-gradle` validates the wrapper JAR; Gradle itself checks `distributionSha256Sum`. Dopamine's device coverage corrected; `bagbak` is deprecated by its author. A Compose `Dialog` inherits `FLAG_SECURE` by default. Android developer verification starts on 30 September 2026 with installs from participating stores in four countries and reaches all apps, sideloaded ones included, in 2027 *(scope corrected in the final pass)*. `actions/checkout` v7 blocks fork checkout unless `allow-unsafe-pr-checkout` |
| 7 (Ch 16–21) | All 159 MASTG and MASWE IDs machine-checked against the repositories; WebView, App Links, behaviour-change and Play policy pages; WebKit blogs; WWDC26 sessions 347 and 241; Kotlin docs | ~250 claims and IDs; 31 corrections, ~45 verified additions; new §20.8 | Deprecated tests `0030`, `0033`, `0035`, `0078` replaced by `0381`, `0334`, `0340`, `0376`–`0380`. App Groups mapped to `MASWE-0001`, not `0031`. WebView content access still defaults to true. The iOS bridge sample registered its handler in `.defaultClient`, which page JavaScript cannot reach. `WebViewAssetLoader` replaces `file://`. `identifierForVendor` is not user-resettable. KMP usage is 7% to 18%. OWASP LLM Top 10 2026 mapping added |
| 8–9 (Ch 22–28) | ~250 MAS identifiers against the live site and the `masvs`, `maswe` and `mastg` repositories (mastg at commit `83d6abb` of 18 September 2026, the head when Chapter 28's counts were taken on 23 September); lab tooling and store procedures | All 78 MASWE IDs and titles match v1.0.0; all 24 control statements now verbatim | All 92 v1 tests are deprecated in MASTG v2.0.0; Chapter 28 gained an old→new mapping table. Placeholder tests are labelled. MAS Test Apps live at `cpholguera/mas-app-*`, not the empty OWASP repositories. Android 14's Conscrypt APEX breaks `/system` CA mounts. CVSS v4.0 added. Play upload-key reset distinguished from signing-key upgrade; revoking an iOS distribution certificate does not break live apps |
| 10 (Q&A) | Every answer reconciled against the rewritten chapter it draws on; web checks only for claims the chapters do not cover | 75 original questions: all kept, 63 corrected or rewritten; 83 added, including a new *Design-review scenarios* group; after the final pass merged two near-duplicate pairs, 156 in total, tagged 38 Beginner, 93 Intermediate, 25 Advanced; every answer ends with the § where it is taught | Play Integrity tokens are not "decrypted twice" (reuse threshold unstated); App Attest fraud metric dates from WWDC21; a device-credential fallback switches off enrolment invalidation; Secure Enclave holds ML-KEM/ML-DSA keys from iOS 26; GitGuardian 3.2% is Claude Code commits against 1.5% of all public commits; MAS-L1 is the baseline for every app; the misquoted MASTG pinning line removed; HSTS answer carries a mobile caveat |
| 11 (Ch 29–32) | IBM's 2026 press release, Verizon DBIR 2026, GitGuardian 2026, EU Commission and ENISA CRA pages, OCC and FTC enforcement releases, PCI SSC, HHS, Play and Apple store requirements; figures already verified by other parts reused rather than re-researched | ~75 claims; of those classified, ~45 correct, 9 stale, 6 wrong, 8 unsourced or imprecise (the rest were figures reused from other parts' checks); 27 corrections; new executive summary and §30.4 | Ransomware share is 39% against 34% the year before, not 24%. GitGuardian's 3.2% is Claude Code commits against all public commits. Play Integrity quotas and App Attest rate guidance are documented, not practitioner-reported. §30.1 now covers the CRA (reporting since 11 September 2026), DORA, NIS2 and the AI Act. Capital One's $80M OCC penalty added beside the $190M class settlement; Equifax reclassified as a regulator settlement. HIPAA encryption is still addressable, not mandatory. §32.5's replay-test cross-reference fixed to §12.4 |
| 12 (Ch 33, Sources, Glossary) | Every URL in the Sources list requested on 24 September 2026; glossary checked against the rewritten parts | 33 historical entries annotated as superseded and one as re-checked; Sources grew from 58 to 278 entries (281 before the final pass removed five orphaned pages and added the EUR-Lex texts of DORA and NIS2), deduplicated and grouped; glossary from 81 to 210 terms | Wrong Play Integrity path (`/verdict` → `/verdicts`), dead ASVS path and Mozilla path fixed; unaffiliated and superseded sources removed and listed. Glossary: DCV, Gatekeeper, Secure Enclave, RKP, Deep link and SSL corrected; every entry now points to where it is taught |

#### Log lines from the part audits

- **2026-09-23 — Part 3:** iOS pinning delegate hashed the raw key, not the SPKI; replaced with a tested `SPKIPin` helper. DCV arithmetic corrected against BR §4.2.1. OkHttp `CertificatePinner` does not install a TrustManager, and the network security configuration covers OkHttp and WebView (emulator-tested). Android 17 CT and ECH defaults added. Ktor Darwin has a built-in `CertificatePinner`. objection syntax is now `-n … start`. NSC XML declaration order fixed.
- **2026-09-23 — Part 7:** re-verified. Deprecated `MASTG-TEST-0030`/`0033`/`0035`/`0078` replaced by `0381`/`0334`/`0340`/`0376`–`0380`. `MASWE-0031` misattribution fixed (App Groups → `MASWE-0001`). WebView content-access default corrected (still true). iOS bridge sample fixed (a `.defaultClient` handler is unreachable from the page). KMP figure corrected to 7% → 18%. OWASP LLM Top 10 2026 mapping added.
- **2026-09-23 — Parts 1 and 9:** MASWE v1.0.0 (17 August 2026) consolidated 119 beta entries into 78 and renumbered every ID once; Part 9 uses the new numbering, and IDs cited elsewhere were spot-checked against it. MASTG v2.0.0 (30 June 2026) deprecated all v1 tests and dropped the MAS Checklist spreadsheet.
- **2026-09-24 — Part 12:** this entry. The DCV "validation arithmetic" correction of 10 September is itself superseded (see that entry).
- **2026-09-24 — Part 11:** executive summary and decision table added. §29.2 ransomware comparison corrected (39% against 34%, not 24%); GitGuardian AI figure corrected (Claude Code commits, 3.2% against 1.5% across all public commits); Verizon DBIR 2026 added. §29.3 adds Capital One's $80M OCC penalty and reclassifies Equifax as a regulator settlement. §30.1 adds the CRA, DORA, NIS2, the AI Act, PCI DSS v4.0.1, HIPAA NPRM status and the FTC Health Breach Notification Rule; §30.2 store deadlines; new §30.4. §32.5 cross-reference fixed to §12.4. §32.7 quotas now documented; the rooted-device share is *(reasoned; no reliable primary figure)*.
- **2026-09-24 — Part 10:** rebuilt group by group against the rewritten chapters. 158 questions (from 75), 156 after the final pass merged two near-duplicate pairs, each tagged by difficulty and ending with the section that teaches it; new *Design-review scenarios* group of 15. Corrections as in the table above.
- **2026-09-24 — Editorial pass, start here and Parts 0–9:** a cold read by an editor reading as the target reader found about 60 issues; P1 and P2 items were fixed. Contradictions resolved: MASWE "no test yet" count (35 of 78, not 36); the lab's `debug-overrides` advice silently disabled the pinning experiment; Chapter 14 and Chapter 1 disagreed about the fraudster; three different Play Console paths (now *Protected with Play → Play Store protection → Manage Play app signing*); 16 KB page dates. Duplicated hygiene code moved into §6.6 and §6.7; Chapter 25 compacted to a checklist. Added: a "Reading OWASP IDs" table (Chapter 0.1), an attacker-to-controls map (§1.3), server-side key-attestation verification (§5.5), a Keystore/Keychain comparison (§4.7), a server-side App Attest assertion verifier (§10.7), a DPoP worked example (§12.6), TanStack and TikTok attack diagrams, a worked CVSS v4.0 sample finding (§23.4), an incident-levers table (§24.1) and a platform-defaults-by-version table (Chapter 28). House style unified (British spelling in prose, "I" for the author, far fewer em dashes, one set of confidence markers including the new *(illustrative)*). Facts re-checked: OkHttp's home moved to `lysine-dev/okhttp` (the old `square` URLs redirect or 404); HPKP deprecated in Chrome 67 and removed in Chrome 72; `NSFileProtectionNone` is not deprecated; `canOpenURL` deprecation and the 25-scheme limit in the iOS 27 SDK confirmed; Dopamine coverage corrected against its README.
- **2026-09-24 — MAS data caveat:** some MASTG v2 tests' `maswe:` links point at a neighbouring weakness (pasteboard and overlay tests at `MASWE-0036`, WebView-bridge tests at `MASWE-0034`). The book cites tests by topic; per-weakness test counts in Chapter 27 follow the MASWE pages.
- **2026-09-24 — Final verification pass:** after the rewrite, ten independent verifiers read the whole repository, one to three files each, read-only, checking every claim against primary sources and the code against the libraries it uses. They found **1 critical**, about **30 major** and about **150 minor** problems. Each was fixed in place, or skipped with a recorded reason. The most important, by part:
  - **Critical, Part 7:** the "safe" `ContentProvider.query` sample passed the caller's `projection` straight to `db.query`, and SQLite pastes column names into the statement as raw SQL, so an exported provider copied from it was still SQL-injectable. Projection and sort order are now allowlisted, and §17.8 has a `--projection` probe to test for it.
  - **Parts 0–1:** IBM's AI figure was presented as a first; it is "a 56% increase over last year". The sentence under the §1.3 attacker-to-controls table contradicted the table.
  - **Part 2:** a relayed attestation chain is stopped by the `attestationApplicationId` check, not by proof of possession, which a same-app relay can proxy. The §5.5 verifier accepted a `SOFTWARE` KeyMint level. MAS-P dates from MASVS v2.1.0 (January 2024). The backup check could pass without testing anything, unless the local transport is marked encrypted.
  - **Part 3:** the TLS 1.1 check passed falsely under OpenSSL 3. The signed-manifest format could not be verified over "the exact bytes" it was told to use, so the manifest now travels as opaque base64url bytes.
  - **Part 4:** App Attest attestation verification added beside the assertion verifier. A public key must not already belong to another user. A `ThisDeviceOnly` key ID can survive a reinstall, so `invalidKey` means re-attest. The biometric test mapping is now `MASTG-TEST-0326`/`0328`/`0330`.
  - **Parts 5–6:** artifact attestations on private repositories need GitHub Enterprise Cloud and have no public transparency log. The §15.8 signer check could not pass for an App Bundle. The §14.5 control count contradicted itself. The Play Console path was stale.
  - **Part 7:** Swift export exposes Kotlin to Swift; it does not let Kotlin call CryptoKit. `detectUnsafeIntentLaunch` dates from API 31.
  - **Parts 8–9:** Play's annual signing-key upgrade now enforces a quantum-ready hybrid key on Android 17 (APK Signature Scheme v3.2). The worked CVSS finding's attack description said "brief physical access to an unlocked phone" when the attack needs root. One Zip Slip cross-reference pointed at the wrong section.
  - **Part 10:** refresh-token rotation is useless without reuse detection. Two near-duplicate question pairs were merged, leaving 156 questions.
  - **Part 11 and the repository:** Android developer verification starts on 30 September 2026 with installs from participating stores in four countries; sideloaded apps follow worldwide in 2027. The README and `VERIFICATION.md` claimed CI checks that CI does not run, and two issue templates were stale.
  - **Part 12:** a known uncertainty about the IBM wording was already resolved. The claim that the book gives no MASTG test count was wrong (Chapter 28 gives one). The RKP dates in Google's two primaries disagree, which is now recorded. The glossary had wrong section references and a duplicated entry. Five orphaned sources were removed.

#### Verified claims, 24 September 2026

The current state of the claims most likely to be quoted. Each was checked against the source named on 23 or 24 September 2026.

| Claim | Source | Where |
|---|---|---|
| IBM 2026: $4.99M global average, $11.5M US, 247-day mean time to identify and contain; one in four malicious breaches AI-enabled, costing about $6M on average, up 56% on the year; ransomware 39%, up from 34% | IBM report page and 29 July 2026 press release | §2.1, §29.2 (ransomware §29.2 only) |
| Verizon DBIR 2026: vulnerability exploitation 31%, ahead of credentials for the first time; third parties 48%; mobile-centric social engineering more successful than email | Verizon press release, 19 May 2026 | §2.1 |
| GitGuardian 2026: 28.65M new secrets on public GitHub in 2025, +34%; Claude Code-assisted commits 3.2% against 1.5% across all public commits; 24,008 secrets in MCP configs; more than 64% of secrets valid in 2022 still valid in January 2026 | GitGuardian report and blog | §2.2 |
| MASVS v2.1.0, 8 categories, 24 controls; MASWE v1.0.0 (17 August 2026), 78 weaknesses, renumbered once; MASTG v2.0.0 (30 June 2026), all v1 tests deprecated | mas.owasp.org; OWASP release notes | §3.1, Ch 26–28 |
| MAS profiles: L1 (baseline for all apps), L2, R, P, plus MAS-EUDIW | mas.owasp.org/Profiles | §3.2 |
| KeyMint replaced Keymaster in Android 12; Gatekeeper verifies PIN, pattern and password; `KeyInfo.getSecurityLevel()` is API 31+ with five constants | source.android.com; `KeyInfo` | §4.1, §4.2 |
| Secure Enclave: P-256 through the Security framework, plus ML-KEM and ML-DSA through CryptoKit from iOS 26 | CryptoKit `SecureEnclave` | §4.3 |
| New attestation root, ECDSA P-384 "Key Attestation CA 1", signing chains from 1 February 2026; RKP announced in 2022 as mandatory from Android 13, though Google's attestation page now calls it optional under the Android 15 policy and the only option for devices launching with 16 (see Known uncertainties); factory-keyed devices stay on the RSA root | developer.android.com key attestation; Google 2022 RKP post | §5.3 |
| `EncryptedSharedPreferences` deprecated 9 April 2025, deprecated stable 1.1.0 on 30 July 2025; `datastore-tink` `AeadSerializer` since DataStore 1.3.0-alpha07 | androidx release notes | §6.1 |
| Certificate lifetimes 200 days from 15 March 2026, 100 from 2027, 47 from 2029; DCV reuse 200, 100, then 10 days, counted back from each issuance; SC-081v3 adopted 11 April 2025 with no votes against | cabforum.org ballot; Baseline Requirements §4.2.1, §6.3.2 | §8.5 |
| The network security configuration covers `HttpsURLConnection`, OkHttp and WebView; OkHttp `CertificatePinner` checks the validated chain after the handshake and installs no trust manager | Android docs; OkHttp source; Android 17 emulator test | §8.6, §8.10 |
| Android 17 enables CT and ECH by default for apps targeting API 37 | Android 17 behaviour changes | §7.3 |
| Play Integrity: 10,000 token requests and 10,000 decryptions a day by default; classic requests 5 per minute per instance; basic and strong labels are opt-in; library 1.6.0 current | Play Integrity setup, classic, verdicts, release notes | §9.2–§9.4, §9.6 |
| App Attest: keep `attestKey` below about 100 requests per second across installs and ramp at ≤10 million users a day; fraud metric available since 2021; iOS 27 extensions and macOS 27 support new in 2026 | Apple DeviceCheck docs; WWDC21 10244; WWDC26 201 | §10.3, §10.5 |
| `setInvalidatedByBiometricEnrollment` defaults to true for per-use biometric keys and stops applying with `AUTH_DEVICE_CREDENTIAL` or a validity window | `KeyGenParameterSpec.Builder` | §11.3 |
| tj-actions/changed-files, 14–15 March 2025, secrets dumped to logs; Trivy, 19 March 2026, 76 of 77 tags; TanStack, 11 May 2026, 84 versions across 42 packages; GhostAction, disclosed 5 September 2025; Megalodon, 18 May 2026 | Each incident's own advisory or post-mortem | §15.1 |
| `GITHUB_TOKEN` read-only by default for enterprises, organisations and personal repositories created from 2 February 2023; `pull_request_target` workflows always come from the default branch since 8 December 2025 | GitHub changelog | §15.3 |
| WebView `allowContentAccess` defaults to true on every version; file-access defaults depend on `targetSdkVersion` | `WebSettings` | §16.3 |
| Play requires target API 36 from 31 August 2026; non-compliant 16 KB-page updates blocked from 1 February 2027 | Play target API page; 16 KB page guide | §19.6 |
| KMP usage 7% (2024) to 18% (2025) of JetBrains Developer Ecosystem respondents | kotlinlang.org | Ch 21 |

#### What this audit did not do

- **Hardware.** The four new experiments ran on an Android 17 emulator and iOS 26.5 and 27.0 simulators, and the Part 3 listings also ran on macOS 27. A simulator or emulator is not a phone: the Secure Enclave, StrongBox, carrier networks and OEM WebView builds are absent or different. The results are evidence, not proof.
- **Compile everything.** Part 3 compiled and ran its listings; Parts 5–6 type-checked or compiled theirs against the iOS 27 SDK and `android-37` without running them; Parts 2, 4 and 7 checked signatures against references but did not compile every block. Each part's report says which.
- **Read paywalled or gated primaries.** The IBM PDF sits behind a registration form and the OWASP LLM Top 10 2026 list behind a download; both are marked where the text depends on secondary coverage.
- **Part 10** answers were reconciled against the chapters rather than re-researched from scratch; a wrong chapter would propagate into its answers.

### Known uncertainties — treat with care

Updated 24 September 2026. Two paragraphs from the 10 September version turned out to describe documented facts, and are kept below with their correction so a reader holding the old text can see what changed.

**Play Integrity quotas.** *(superseded 2026-09-24: these are documented, not practitioner-reported.)* Google's setup and classic-request pages give 10,000 token requests a day (shared by classic requests and standard-provider preparations) and 10,000 decryptions a day by default, classic requests at 5 per minute per app instance, and an increase form that can take up to a week. What remains uncertain is **how many times a token can be decrypted** before its verdicts clear: Google says only that tokens cannot be "reused many times" and gives no number (§9.2).

**App Attest rate limits.** *(superseded 2026-09-24: Apple does publish guidance.)* Keep `attestKey` calls below about 100 requests per second across all installs, and ramp a rollout at no more than 10 million users a day (§10.5). What remains uncertain is the cause of persistent `DCError.invalidKey` on a small subset of devices, and whether throttling can ever surface as `invalidKey`. Apple has not said.

**Whether to pin at all.** Genuinely contested and not settled. This book presents both positions rather than manufacturing consensus.

**Supply-chain incident figures.** The mechanisms of TanStack, Trivy, tj-actions, Nx and Ultralytics are now sourced to the projects' own post-mortems or advisories. The counts for Shai-Hulud, GhostAction and Megalodon still come from vendor research write-ups, and TanStack's valid-provenance finding comes from Snyk and StepSecurity rather than TanStack's post-mortem. Treat those numbers as reported.

**MAS identifiers.** MASWE IDs are stable since v1.0.0 (17 August 2026), but any MASWE ID from older material is a beta ID and may name a different weakness. MASTG v1 tests are deprecated; several v2 tests and best practices are still placeholder pages. Per-weakness test counts in Part 9 are a snapshot. MASTG's own release notes (193 tests) and announcement (285) disagree on the test count, so the book quotes neither. Chapter 28 gives a dated count from the repository instead: 186 current v2 tests and 14 placeholders on 23 September 2026.

**IBM figures from secondary sources.** The IBM report PDF sits behind a registration form. The 183/64-day split of the 247 days, "up from 241", and the healthcare and per-record figures come from secondary coverage and are marked *(reported)*. The AI finding is no longer among them: Parts 1 and 11 both follow IBM's own press release ("one in four malicious breaches" AI-enabled, "a 56% increase over last year", "$6 million on average"). It is not a first-time figure: IBM measured AI-enabled breaches the year before.

**The RKP cutover date.** Google's documentation gives only the 1 February 2026 start of the new attestation root. "Mandatory by 10 April 2026" appears only in practitioner sources.

**When RKP became mandatory.** Google's two primaries disagree. The 2022 RKP post says the scheme "will be mandated in Android 13", while the attestation page today says devices launching with Android 16 support only RKP, "expanding on the Android 15 policy where RKP support was optional". §5.3 follows the 2022 announcement. Treat "mandatory from Android 13" as Google's announcement, not as a guarantee that every device launched with Android 13 to 15 uses RKP, and read the chain rather than assuming.

**WebView pinning on iOS.** My iOS 26.5 and 27.0 simulator runs showed `WKWebView` ignoring `NSPinnedDomains`, but published reports conflict (one found it ignored through iOS 15.4, others say it is honoured from iOS 16), and an Apple engineer said on the forums he did not know. In a separate macOS 27 run during the Part 3 audit, the navigation delegate received server-trust challenges for subresource hosts, which `MASTG-KNOW-0072` says it does not; §8.6 still follows `MASTG-KNOW-0072` until an iOS run settles it.

**Upstream documentation that contradicts the source code.** `MASTG-KNOW-0015` says OkHttp's `CertificatePinner` uses a custom trust manager and that the network security configuration covers only `HttpsURLConnection`-based libraries. The OkHttp source and my emulator test contradict both. The book follows the source code.

**Other open items.** Whether Android has a platform post-quantum TLS default (Conscrypt's own documents disagree); the order of the OWASP LLM Top 10 2026, taken from secondary coverage because the list sits behind a download; whether NIST IR 8547 has left draft; the EU AI Act Omnibus publication date; and HIPAA final-rule timing.

**Incident cost estimates.** Any per-incident range you see quoted, including in this book's absence of one, is an estimate rather than a measurement. Derive your own exposure; do not borrow an average.

### Where to look first when re-verifying

One global verification date across roughly 130,000 words tells a reader very little. This table says which chapters decay fastest, so a quarterly re-check has somewhere to start. Updated 24 September 2026; each part's frontmatter carries its own `volatility` and `recheck_because`.

| Chapter | Volatility | Why | Re-check |
|---|---|---|---|
| 7, 8 — TLS baseline and pinning | **High** | Certificate lifetimes and DCV reuse step down in March 2027 and March 2029; Android 17 turns on CT and ECH for API 37 targets; root distrusts force backup-pin changes; persistent DCV support is spreading; OkHttp changed home | Quarterly |
| 5 — Attestation | **High** | New attestation root in 2026, revocation list, post-quantum attestation chains from Android 17, attestation-spoofing and relay tools | Quarterly |
| 6 — Choosing storage | **High** | `datastore-tink` is still alpha; the deprecated library's replacements are still settling; SQLCipher moved packages | Quarterly |
| 9 — Play Integrity | **High** | Verdict semantics changed in May 2025; opt-in labels, remediation dialogs and library versions keep moving | Quarterly |
| 10 — App Attest | **High** | New signals at each WWDC; `invalidKey` behaviour undocumented | After each WWDC |
| 15 — Pipeline | **High** | Monthly incidents; GitHub's 2026 Actions roadmap and the 2 November 2026 `pull_request_target` rule change the baseline | Quarterly |
| 29–32 — The programme | **High** | Annual reports each July; CRA full application 11 December 2027; AI Act and GDPR Omnibus dates; HIPAA final rule; store deadlines | Each July, and on each regulatory date |
| 4 — Key storage | **Medium** | Post-quantum keys arrived (Secure Enclave ML-KEM and ML-DSA in iOS 26, Keystore ML-DSA in Android 17); StrongBox may become required | Per major OS release |
| 11 — Biometrics | **Medium** | androidx.biometric 1.4 alpha redesigns the API; Identity Check and Stolen Device Protection keep changing the threat model | Per major OS release |
| 13, 14 — Resilience | **Medium** | Frida, objection, root-hiding modules and jailbreak coverage move every few months | Semi-annually |
| 3, 26–28 — The standard and catalogues | **Medium** | MASWE is stable since v1.0.0, but MASTG placeholders fill in and test counts drift | Per MAS release |
| 16, 17, 19 — Platform surfaces | **Medium** | API deprecations at each OS release; Play's yearly target-API step (API 36 from 31 August 2026); 16 KB pages from February 2027 | Per major OS release |
| 18 — Privacy | **Medium** | Store policies change faster than law | Semi-annually |
| 20 — AI features | **Medium** | The OWASP LLM Top 10 reordered between 2025 and 2026; on-device model APIs change at each I/O and WWDC | Quarterly |
| 21 — Kotlin Multiplatform | **Medium** | `expect`/`actual` classes are Beta and Swift export is Alpha | Per Kotlin release |
| 22 — Test lab | **Medium** | Emulator images, CA-trust workarounds and jailbreak coverage | Semi-annually |
| 23–25 — Assessment, incidents, reference | **Medium** | CVSS practice and store incident procedures (Play key upgrade, App Store phased release) change; the tools in the checklist move | Semi-annually |
| Part 10 — Questions and answers | **Medium** | Inherits the volatility of the chapters each answer cites | With each re-check of those chapters |
| 2 — Economics | **Medium** | Annual reports supersede each other, and the trend reverses | Annually, on report release |
| Part 0, Chapters 1 and 12 — Foundations, threat, backend | **Low** | Principles, not versions. Watch OAuth 2.1, still a draft | Annually |

### Claims this book asserts but has not empirically tested

These six claims were stated from vendor documentation or practitioner reporting. On 23–24 September 2026, four were tested for the first time, on an Android 17 emulator (API 37, WebView 152) and iOS 26.5 and 27.0 simulators, against `https://example.com` with deliberately wrong pins and a correct-pin control. The probe apps are described in the **Evidence** callout in §8.6.

**A simulator or emulator is not a phone.** These results are stronger than citation and weaker than hardware. Each claim is still one small test on a real device away from being settled.

| # | Claim | Where | Status, 24 September 2026 |
|---|---|---|---|
| 1 | `NSPinnedDomains` does not cover `WKWebView` or `SFSafariViewController` | §8.6, §8.10 | **Supported for `WKWebView` on iOS 26.5 and 27.0 simulators**: a wrong pin made `URLSession` fail with -1200 while `WKWebView` loaded the page. Published reports conflict. `SFSafariViewController` untested. Hardware untested |
| 2 | Android network security config covers WebView traffic, while OkHttp `CertificatePinner` does not | §8.6 | **Confirmed on an Android 17 emulator**: a wrong NSC pin failed `HttpsURLConnection`, plain OkHttp and WebView alike. The configuration covers OkHttp too, and `CertificatePinner` installs no trust manager. Hardware untested |
| 3 | `pin-set expiration` fails open — pinning stops being enforced after the date | §8.6 | **Confirmed on an Android 17 emulator**: a wrong pin with a past expiration (`2020-01-01`) connected on all three clients; with a future expiration (`2030-01-01`), all three failed |
| 4 | Changing `NSPinnedDomains` may require an app reinstall before ATS drops the cached trust setting | §8.10 | **Not reproduced** on iOS 26.5 and 27.0 simulators: an update-install took effect on the next launch, in both directions. Xcode-run and device installs untested; still *(reported)* |
| 5 | Re-decrypting a Play Integrity token returns cleared verdicts | §9.2 | **Still untested.** Google says a token cannot be "reused many times" and gives no number, so "twice" overstated the documentation. Chapter 9's Try it describes the test |
| 6 | A subset of devices return `DCError.invalidKey` persistently, surviving reinstall and reboot | §10.4 | **New forum evidence, still unreproduced**: a September 2026 Apple Developer Forums thread reports about 0.01% of one app's ~360,000 active users, persistent for weeks across reinstall, reboot and updates. Apple has not replied |

If you run any of these on hardware, open an [empirical result issue](../.github/ISSUE_TEMPLATE/empirical-result.md). The result goes into the chapter with credit.

### Keeping this current

Re-verify quarterly. The fastest-moving items are the certificate lifetime schedule, Android's CT and ECH defaults, Play Integrity verdict behaviour, App Attest signals after each WWDC, Android platform security changes at each release, the GitHub Actions security roadmap, and the MAS release notes. Record the date and what changed here each time, and annotate superseded entries rather than deleting them.

---

## Sources

Grouped by topic, primary sources first within each group. Where a link is a secondary or practitioner source, it says so. Every URL below was checked on 24 September 2026; all returned HTTP 200 except the nine marked: five sit behind a bot check that returned 403 to an automated request, two EUR-Lex links answered with a bot challenge (HTTP 202), and two returned 403 or 429 (rate limiting). Those nine could not be confirmed this way and need a browser. Chapters also cite sources inline, next to the claim.

### OWASP Mobile Application Security (MAS)
- OWASP MASVS — <https://mas.owasp.org/MASVS/>
- MASVS, Assessment and Certification — <https://mas.owasp.org/MASVS/04-Assessment_and_Certification/>
- OWASP MASWE — <https://mas.owasp.org/MASWE/>
- MASWE v1.0.0 release announcement (17 August 2026) — <https://mas.owasp.org/news/2026/08/17/maswe-v100-release/>
- MASWE v1.0.0 release notes — <https://github.com/OWASP/maswe/releases/tag/v1.0.0>
- OWASP MASTG — <https://mas.owasp.org/MASTG/>
- MASTG v2.0.0 release notes (30 June 2026) — <https://github.com/OWASP/mastg/releases/tag/v2.0.0>
- MASTG v2.0.0 announcement — <https://mas.owasp.org/news/2026/07/04/mastg-v200-release/>
- MASTG releases — <https://github.com/OWASP/mastg/releases>
- MAS Checklists removal — <https://mas.owasp.org/news/2026/07/14/checklists-removal/>
- MAS Testing Profiles — <https://mas.owasp.org/Profiles/>
- MASTG tests — <https://mas.owasp.org/MASTG/tests/>
- MASTG techniques — <https://mas.owasp.org/MASTG/techniques/>
- MASTG best practices — <https://mas.owasp.org/MASTG/best-practices/>
- MASTG demos — <https://mas.owasp.org/MASTG/demos/>
- MASTG apps — <https://mas.owasp.org/MASTG/apps/>
- MAS Crackmes — <https://mas.owasp.org/crackmes/>
- MASTG-KNOW-0015, Android certificate pinning — <https://mas.owasp.org/MASTG/knowledge/android/MASVS-NETWORK/MASTG-KNOW-0015/>
- MASTG-KNOW-0072, iOS certificate pinning — <https://mas.owasp.org/MASTG/knowledge/ios/MASVS-NETWORK/MASTG-KNOW-0072/>
- MASVS discussion #573, a maintainer on Google's pinning warning — <https://github.com/OWASP/masvs/discussions/573>

### Other standards and OWASP projects
- OWASP Mobile Top 10 — <https://owasp.org/www-project-mobile-top-10/>
- OWASP ASVS — <https://owasp.org/projects/asvs>
- OWASP Pinning Cheat Sheet — <https://cheatsheetseries.owasp.org/cheatsheets/Pinning_Cheat_Sheet.html>
- OWASP Password Storage Cheat Sheet — <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- OWASP GenAI, LLM Top 10 2026 — <https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/>
- Threat Modeling Manifesto — <https://www.threatmodelingmanifesto.org/>
- FIRST, CVSS v4.0 specification — <https://www.first.org/cvss/v4-0/specification-document>
- SLSA v1.2 specification — <https://slsa.dev/spec/v1.2/>

### IETF and NIST
- RFC 7636, PKCE — <https://www.rfc-editor.org/rfc/rfc7636.html>
- RFC 8252, OAuth 2.0 for Native Apps (BCP 212) — <https://www.rfc-editor.org/rfc/rfc8252.html>
- RFC 9700, OAuth 2.0 Security Best Current Practice (BCP 240) — <https://www.rfc-editor.org/rfc/rfc9700.html>
- RFC 9449, DPoP — <https://www.rfc-editor.org/rfc/rfc9449.html>
- RFC 8705, OAuth mutual-TLS — <https://www.rfc-editor.org/rfc/rfc8705.html>
- RFC 7009, Token Revocation — <https://www.rfc-editor.org/rfc/rfc7009.html>
- RFC 7519, JSON Web Token — <https://www.rfc-editor.org/rfc/rfc7519.html>
- RFC 8446, TLS 1.3 — <https://www.rfc-editor.org/rfc/rfc8446.html>
- RFC 9849, TLS Encrypted Client Hello — <https://www.rfc-editor.org/rfc/rfc9849.html>
- OAuth 2.1 draft (not yet an RFC) — <https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/>
- NIST SP 800-38D, GCM — <https://csrc.nist.gov/pubs/sp/800/38/d/final>
- NIST IR 8547, initial public draft — <https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf>

### Certificates, TLS and the web PKI
- CA/Browser Forum Ballot SC-081v3 — <https://cabforum.org/2025/04/11/ballot-sc081v3-introduce-schedule-of-reducing-validity-and-data-reuse-periods/>
- CA/Browser Forum Baseline Requirements, current text (§3.2.2.4, §4.2.1, §6.3.2) — <https://github.com/cabforum/servercert/blob/main/docs/BR.md>
- CA/Browser Forum Ballot SC-088v3, DNS-PERSIST-01 — <https://cabforum.org/2025/10/09/ballot-sc-088v3-dns-txt-record-with-persistent-value-dcv-method/>
- Let's Encrypt, dns-persist-01 deployment status — <https://community.letsencrypt.org/t/dns-persist-01-deployment-status-and-timeline/246468>
- Zhang et al., "ACME++", WWW '25 — <https://doi.org/10.1145/3696410.3714763> *(behind a bot check; returned 403 to the automated check, not confirmed)*
- Google, DigiNotar man-in-the-middle (2011) — <https://security.googleblog.com/2011/08/update-on-attempted-man-in-middle.html>
- Google, Entrust distrust (2024) — <https://security.googleblog.com/2024/06/sustaining-digital-certificate-security.html>
- Google, Chunghwa and NetLock distrust (2025) — <https://blog.google/security/sustaining-digital-certificate-security-chrome-root-store-changes/>
- Chromium, intent to remove HPKP — <https://groups.google.com/a/chromium.org/g/blink-dev/c/he9tr7p3rZ8/m/eNMwKPmUBAAJ>
- Mozilla, the Kazakhstan root (2019) — <https://blog.mozilla.org/security/2019/08/21/protecting-our-users-in-kazakhstan/>
- DigiCert on the 47-day schedule *(secondary)* — <https://www.digicert.com/blog/tls-certificate-lifetimes-will-officially-reduce-to-47-days>
- SSL.com on preparing for 47-day certificates *(secondary)* — <https://www.ssl.com/article/preparing-for-47-day-ssl-tls-certificates/>

### Android platform: keys, attestation and storage
- Hardware-backed Keystore — <https://source.android.com/docs/security/features/keystore>
- Key and ID attestation (AOSP) — <https://source.android.com/docs/security/features/keystore/attestation>
- Authentication, Gatekeeper and HardwareAuthToken — <https://source.android.com/docs/security/features/authentication>
- Android encryption (file-based encryption requirement) — <https://source.android.com/docs/security/features/encryption>
- Android 16 CDD (StrongBox, CDD section 9.11.2) — <https://source.android.com/docs/compatibility/16/android-16-cdd>
- Android Keystore system — <https://developer.android.com/privacy-and-security/keystore>
- Key attestation: roots, revocation list and RKP — <https://developer.android.com/privacy-and-security/security-key-attestation>
- Upgrading Android attestation: Remote Key Provisioning (2022) — <https://android-developers.googleblog.com/2022/03/upgrading-android-attestation-remote.html>
- Security for the quantum era: post-quantum cryptography in Android (2026) — <https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/>
- The fourth beta of Android 17 (Keystore ML-DSA) — <https://android-developers.googleblog.com/2026/04/the-fourth-beta-of-android-17.html>
- Key attestation verification library — <https://github.com/android/keyattestation>
- `KeyInfo` — <https://developer.android.com/reference/android/security/keystore/KeyInfo>
- `KeyGenParameterSpec.Builder` — <https://developer.android.com/reference/android/security/keystore/KeyGenParameterSpec.Builder>
- `KeyStoreManager` (Android 16) — <https://developer.android.com/reference/android/security/keystore/KeyStoreManager>
- Cryptography guidance — <https://developer.android.com/privacy-and-security/cryptography>
- Jetpack Security Crypto (deprecated) — <https://developer.android.com/reference/androidx/security/crypto/package-summary>
- Jetpack Security release notes — <https://developer.android.com/jetpack/androidx/releases/security>
- DataStore release notes (`datastore-tink`) — <https://developer.android.com/jetpack/androidx/releases/datastore>
- `AeadSerializer` — <https://developer.android.com/reference/kotlin/androidx/datastore/tink/AeadSerializer>
- Tink `AndroidKeysetManager` source, Keystore fallback behaviour — <https://github.com/tink-crypto/tink-java/blob/main/src/main/java/com/google/crypto/tink/integration/android/AndroidKeysetManager.java>
- Auto Backup and data extraction rules — <https://developer.android.com/identity/data/autobackup>
- SQLCipher for Android — <https://github.com/sqlcipher/sqlcipher-android>
- Room 3 release notes — <https://developer.android.com/jetpack/androidx/releases/room3>
- 16 KB page size, Play requirement (2025) — <https://android-developers.googleblog.com/2025/05/prepare-play-apps-for-devices-with-16kb-page-size.html>
- Support 16 KB page sizes — <https://developer.android.com/guide/practices/page-sizes>

### Android platform: network
- Network security configuration — <https://developer.android.com/privacy-and-security/security-config>
- Security with network protocols (pinning caution) — <https://developer.android.com/privacy-and-security/security-ssl>
- Certificate Transparency policy — <https://developer.android.com/privacy-and-security/certificate-transparency-policy>
- Conscrypt module and the updatable root store — <https://source.android.com/docs/core/ota/modular-system/conscrypt>
- OkHttp HTTPS documentation (new home) — <https://lysine.dev/okhttp/features/https/>
- OkHttp repository — <https://github.com/lysine-dev/okhttp>
- Ktor Darwin `CertificatePinner` — <https://api.ktor.io/ktor-client-darwin/io.ktor.client.engine.darwin.certificates/-certificate-pinner/index.html>
- Ktor client SSL — <https://ktor.io/docs/client-ssl.html>

### Android platform: integrity, authentication and identity
- Play Integrity overview — <https://developer.android.com/google/play/integrity/overview>
- Play Integrity setup and quotas — <https://developer.android.com/google/play/integrity/setup>
- Play Integrity standard requests — <https://developer.android.com/google/play/integrity/standard>
- Play Integrity classic requests — <https://developer.android.com/google/play/integrity/classic>
- Play Integrity verdicts — <https://developer.android.com/google/play/integrity/verdicts>
- Play Integrity May 2025 improvements — <https://developer.android.com/google/play/integrity/improvements>
- Play Integrity remediation dialogs — <https://developer.android.com/google/play/integrity/remediation>
- Play Integrity library release notes — <https://developer.android.com/google/play/integrity/reference/com/google/android/play/core/release-notes>
- Making the Play Integrity API faster, more resilient and more private (December 2024) — <https://android-developers.googleblog.com/2024/12/making-play-integrity-api-faster-resilient-private.html>
- SafetyNet deprecation timeline — <https://developer.android.com/privacy-and-security/safetynet/deprecation-timeline>
- androidx.biometric releases — <https://developer.android.com/jetpack/androidx/releases/biometric>
- androidx.credentials releases — <https://developer.android.com/jetpack/androidx/releases/credentials>
- Google, Identity Check — <https://support.google.com/android/answer/15146908>
- Chrome for Developers, Auth Tab — <https://developer.chrome.com/docs/android/custom-tabs/guide-auth-tab>
- Android developer verification — <https://developer.android.com/developer-verification>
- Android developer verification announcement (March 2026) — <https://android-developers.googleblog.com/2026/03/android-developer-verification.html>

### Android platform: components, WebView, privacy and releases
- Android 10 behaviour changes (all apps) — <https://developer.android.com/about/versions/10/behavior-changes-all>
- Android 14 behaviour changes (targeting 34) — <https://developer.android.com/about/versions/14/behavior-changes-14>
- Android 15 behaviour changes (targeting 35) — <https://developer.android.com/about/versions/15/behavior-changes-15>
- Android 16 behaviour changes (targeting 36) — <https://developer.android.com/about/versions/16/behavior-changes-16>
- Android 16 behaviour changes (all apps) — <https://developer.android.com/about/versions/16/behavior-changes-all>
- Android 17 behaviour changes (targeting 37) — <https://developer.android.com/about/versions/17/behavior-changes-17>
- `WebSettings` — <https://developer.android.com/reference/android/webkit/WebSettings>
- `WebViewClient` — <https://developer.android.com/reference/android/webkit/WebViewClient>
- Native API access through JavaScript bridges — <https://developer.android.com/develop/ui/views/layout/webapps/native-api-access-jsbridge>
- Load local content (`WebViewAssetLoader`) — <https://developer.android.com/develop/ui/views/layout/webapps/load-local-content>
- Intent redirection risk — <https://developer.android.com/privacy-and-security/risks/intent-redirection>
- FileProvider risk — <https://developer.android.com/privacy-and-security/risks/file-providers>
- Tapjacking risk — <https://developer.android.com/privacy-and-security/risks/tapjacking>
- Stopping malware from snooping on sensitive views (December 2025) — <https://android-developers.googleblog.com/2025/12/enhancing-android-security-stop-malware.html>
- Verify App Links — <https://developer.android.com/training/app-links/verify-applinks>
- Configure `assetlinks.json` and Dynamic App Links — <https://developer.android.com/training/app-links/configure-assetlinks>
- Photo picker — <https://developer.android.com/training/data-storage/shared/photopicker>
- Audit data access (AppOps) — <https://developer.android.com/guide/topics/data/audit-access>
- AI risks and mitigations — <https://developer.android.com/privacy-and-security/risks/ai-risks/risks-mitigations>
- Gemini Nano — <https://developer.android.com/ai/gemini-nano>
- Play target API level requirements — <https://developer.android.com/google/play/requirements/target-sdk>
- Play Photo and Video Permissions policy — <https://support.google.com/googleplay/android-developer/answer/14115180>
- Play Device and Network Abuse policy — <https://support.google.com/googleplay/android-developer/answer/9888379>
- Play Advertising ID (`AD_ID` permission) — <https://support.google.com/googleplay/android-developer/answer/6048248>
- Play App Signing, upload-key reset and signing-key upgrade — <https://support.google.com/googleplay/android-developer/answer/9842756>
- Create and manage virtual devices (Play images versus root) — <https://developer.android.com/studio/run/managing-avds>
- AGP 9.0 release notes — <https://developer.android.com/build/releases/agp-9-0-0-release-notes>
- Enable app optimisation with R8 — <https://developer.android.com/topic/performance/app-optimization/enable-app-optimization>
- R8 full mode — <https://developer.android.com/topic/performance/app-optimization/full-mode>

### Apple platform
- Apple Platform Security, Keychain data protection — <https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web>
- Apple Platform Security, Data Protection classes — <https://support.apple.com/guide/security/data-protection-classes-secb010e978a/web>
- Apple Platform Security, TLS — <https://support.apple.com/guide/security/tls-security-sec100a75d12/web>
- Protecting keys with the Secure Enclave — <https://developer.apple.com/documentation/security/protecting-keys-with-the-secure-enclave>
- CryptoKit `SecureEnclave` — <https://developer.apple.com/documentation/cryptokit/secureenclave>
- CryptoKit `SecureEnclave.MLKEM768` — <https://developer.apple.com/documentation/cryptokit/secureenclave/mlkem768>
- `SecAccessControlCreateFlags` — <https://developer.apple.com/documentation/security/secaccesscontrolcreateflags>
- `SecAccessControlCreateFlags.biometryCurrentSet` — <https://developer.apple.com/documentation/security/secaccesscontrolcreateflags/biometrycurrentset>
- `LAContext.domainState` — <https://developer.apple.com/documentation/localauthentication/lacontext/domainstate>
- About Stolen Device Protection — <https://support.apple.com/en-us/120340>
- WWDC25 Session 314, Get ahead with quantum-secure cryptography — <https://developer.apple.com/videos/play/wwdc2025/314/>
- Identity Pinning (`NSPinnedDomains`) — <https://developer.apple.com/news/?id=g9ejcf8y>
- `NSRequiresCertificateTransparency` (obsolete) — <https://developer.apple.com/documentation/bundleresources/information-property-list/nsrequirescertificatetransparency>
- Apple CT policy — <https://support.apple.com/en-us/103214>
- iOS 26 trusted root list — <https://support.apple.com/en-us/126047>
- Blocked and distrusted roots — <https://support.apple.com/en-us/121668>
- Trusting manually installed certificate profiles — <https://support.apple.com/en-us/102390>
- Apple Developer Forums, `NSPinnedDomains` and `WKWebView` — <https://developer.apple.com/forums/thread/681734>
- Apple Developer Forums, `WKWebView` server trust — <https://developer.apple.com/forums/thread/77658>
- DeviceCheck overview — <https://developer.apple.com/documentation/devicecheck>
- Establishing your app's integrity — <https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity>
- Preparing to use the App Attest service (rate guidance) — <https://developer.apple.com/documentation/devicecheck/preparing-to-use-the-app-attest-service>
- Validating apps that connect to your server — <https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server>
- Assessing fraud risk — <https://developer.apple.com/documentation/devicecheck/assessing-fraud-risk>
- WWDC21 Session 10244, Mitigate fraud with App Attest and DeviceCheck — <https://developer.apple.com/videos/play/wwdc2021/10244/>
- WWDC26 Session 201, Secure your apps with App Attest — <https://developer.apple.com/videos/play/wwdc2026/201/>
- Apple Developer Forums, persistent `invalidKey` (September 2026) — <https://developer.apple.com/forums/thread/844380>
- Apple Developer Forums, persistent `invalidKey` (2023–2024) — <https://developer.apple.com/forums/thread/739323>
- `ASWebAuthenticationSession.Callback.https(host:path:)` — <https://developer.apple.com/documentation/authenticationservices/aswebauthenticationsession/callback/https(host:path:)>
- Supporting associated domains — <https://developer.apple.com/documentation/xcode/supporting-associated-domains>
- WebKit, App-Bound Domains (2020) — <https://webkit.org/blog/10882/app-bound-domains/>
- WebKit, enabling inspection of web content in apps (2023) — <https://webkit.org/blog/13936/enabling-the-inspection-of-web-content-in-apps/>
- UIWebView deprecation — <https://developer.apple.com/news/?id=12232019b>
- Upcoming requirements (privacy manifests, SDK minimums) — <https://developer.apple.com/news/upcoming-requirements/>
- App Review Guidelines — <https://developer.apple.com/app-store/review/guidelines/>
- `canOpenURL(_:)` — <https://developer.apple.com/documentation/uikit/uiapplication/canopenurl(_:)>
- `UIScreen.isCaptured` — <https://developer.apple.com/documentation/uikit/uiscreen/iscaptured>
- `UITraitCollection.sceneCaptureState` — <https://developer.apple.com/documentation/uikit/uitraitcollection/scenecapturestate>
- Certificates (revocation and live apps) — <https://developer.apple.com/support/certificates/>
- Release a version update in phases — <https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/>
- WWDC26 Session 347, Secure your app: mitigate risks to agentic features — <https://developer.apple.com/videos/play/wwdc2026/347/>
- WWDC26 Session 241, What's new in the Foundation Models framework — <https://developer.apple.com/videos/play/wwdc2026/241/>
- Apple Security Research, Memory Integrity Enforcement — <https://security.apple.com/blog/memory-integrity-enforcement/>

### Kotlin Multiplatform
- Why try KMP (usage 7% to 18%) — <https://kotlinlang.org/docs/multiplatform/multiplatform-reasons-to-try.html>
- `expect` and `actual` — <https://kotlinlang.org/docs/multiplatform/multiplatform-expect-actual.html>
- KMP platform stability — <https://kotlinlang.org/docs/multiplatform/supported-platforms.html>
- Swift export (Alpha) — <https://kotlinlang.org/docs/native-swift-export.html>
- cryptography-kotlin — <https://github.com/whyoleg/cryptography-kotlin>
- Swift standard library, `SystemRandomNumberGenerator` — <https://github.com/swiftlang/swift/blob/main/stdlib/public/core/Random.swift>

### CI/CD and supply chain
- TanStack post-mortem (May 2026) — <https://tanstack.com/blog/npm-supply-chain-compromise-postmortem>
- Snyk, TanStack packages and "Mini Shai-Hulud" — <https://snyk.io/blog/tanstack-npm-packages-compromised/>
- Trivy advisory GHSA-69fq-xp46-6x23 (CVE-2026-33634) — <https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23>
- tj-actions advisory GHSA-mrrh-fwg8-r2c3 (CVE-2025-30066) — <https://github.com/advisories/GHSA-mrrh-fwg8-r2c3>
- CISA, tj-actions and reviewdog alert — <https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction>
- SafeDep, Megalodon — <https://safedep.io/megalodon-mass-github-repo-backdooring-ci-workflows/>
- GitGuardian, GhostAction — <https://blog.gitguardian.com/ghostaction-campaign-3-325-secrets-stolen/>
- SentinelOne, Sha1-Hulud: The Second Coming — <https://www.sentinelone.com/blog/defending-against-sha1-hulud-the-second-coming/>
- Nx "s1ngularity" post-mortem — <https://nx.dev/blog/s1ngularity-postmortem>
- PyPI, Ultralytics attack analysis — <https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/>
- gluestack incident report — <https://gluestack.io/blogs/public-incident-report>
- Securelist, SparkCat — <https://securelist.com/sparkcat-stealer-in-app-store-and-google-play/115385/>
- GitHub, securing the open source supply chain — <https://github.blog/security/supply-chain-security/securing-the-open-source-supply-chain-across-github/>
- GitHub Actions 2026 security roadmap — <https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/>
- Actions policy: blocking and SHA pinning — <https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/>
- Immutable releases GA — <https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/>
- Dependabot default cooldown — <https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/>
- Dependabot options reference — <https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference>
- `pull_request_target` changes (December 2025) — <https://github.blog/changelog/2025-11-07-actions-pull_request_target-and-environment-branch-protections-changes/>
- Safer `pull_request_target` defaults for `actions/checkout` — <https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/>
- Workflow execution protections GA — <https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/>
- Read-only Actions cache for untrusted triggers — <https://github.blog/changelog/2026-06-26-read-only-actions-cache-for-untrusted-triggers/>
- Actions `cache-mode` — <https://github.blog/changelog/2026-09-10-control-github-actions-cache-access-with-cache-mode/>
- npm trusted publishing GA — <https://github.blog/changelog/2025-07-31-npm-trusted-publishing-with-oidc-is-generally-available/>
- `GITHUB_TOKEN` read-only default (February 2023) — <https://github.blog/changelog/2023-02-02-github-actions-updating-the-default-github_token-permissions-to-read-only/>
- GitHub artifact attestations — <https://docs.github.com/en/actions/concepts/security/artifact-attestations>
- fastlane, App Store Connect API — <https://docs.fastlane.tools/app-store-connect-api/>
- Actions security checklist *(practitioner)* — <https://corgea.com/learn/github-actions-security-checklist>
- Actions checklist mapped to incidents *(practitioner)* — <https://www.aikido.dev/blog/checklist-github-actions>

### Data and research
- IBM, Cost of a Data Breach Report 2026 — <https://www.ibm.com/reports/data-breach>
- IBM newsroom, 2026 Cost of a Data Breach press release — <https://newsroom.ibm.com/2026-07-29-ibm-study-one-in-four-malicious-breaches-are-ai-enabled,-costing-companies-6-million-on-average>
- HIPAA Journal, IBM 2026 sector figures *(secondary)* — <https://www.hipaajournal.com/2026-cost-data-breach-study-ibm/>
- Help Net Security, IBM 2026 summary *(secondary)* — <https://www.helpnetsecurity.com/2026/07/30/ibm-cost-of-a-data-breach-2026/>
- Infosecurity Magazine, IBM 2026 figures *(secondary)* — <https://www.infosecurity-magazine.com/news/cost-of-a-data-breach-5m-ibm/>
- Security Boulevard, IBM 2026 US average *(secondary)* — <https://securityboulevard.com/2026/08/how-much-does-a-data-breach-cost-ibms-2026-report-puts-the-us-average-at-11-5-million/> *(behind a bot check; returned 403 to the automated check, not confirmed)*
- Verizon, 2026 DBIR press release — <https://www.verizon.com/about/news/breach-industry-wide-dbir-finds>
- Verizon DBIR — <https://www.verizon.com/business/resources/reports/dbir/>
- GitGuardian, State of Secrets Sprawl 2026 — <https://www.gitguardian.com/state-of-secrets-sprawl-report-2026>
- GitGuardian, key findings — <https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/>
- The Hacker News, CloudSEK finds Twitter API keys in 3,207 apps (2022) *(secondary)* — <https://thehackernews.com/2022/08/researchers-discover-nearly-3200-mobile.html>

### Regulation, enforcement and precedent
- European Commission, Cyber Resilience Act reporting obligations — <https://digital-strategy.ec.europa.eu/en/policies/cra-reporting>
- ENISA, CRA Single Reporting Platform — <https://www.enisa.europa.eu/news/the-cra-single-reporting-platform-is-launched>
- DORA, Regulation (EU) 2022/2554 — <https://eur-lex.europa.eu/eli/reg/2022/2554/oj> *(EUR-Lex answered the automated check with a bot challenge, HTTP 202; not confirmed)*
- NIS2, Directive (EU) 2022/2555 — <https://eur-lex.europa.eu/eli/dir/2022/2555/oj> *(EUR-Lex answered the automated check with a bot challenge, HTTP 202; not confirmed)*
- DORA incident reporting *(secondary guide)* — <https://www.regulation-dora.eu/dora-incident-reporting>
- Wavestone, NIS2 transposition tracker *(secondary; for transposition status only)* — <https://www.wavestone.com/en/insight/nis-2-european-countries-transposing-directive/>
- Gibson Dunn, EU AI Act Omnibus agreement *(secondary)* — <https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/>
- Taylor Wessing, the Digital Omnibus and incident reporting *(secondary)* — <https://www.taylorwessing.com/en/global-data-hub/2026/the-digital-omnibus-proposal/gdh---the-digital-omnibus-and-incident-reporting>
- DLA Piper, GDPR fines and data breach survey, January 2026 — <https://www.dlapiper.com/en-us/insights/publications/2026/01/dla-piper-gdpr-fines-and-data-breach-survey-january-2026> *(did not return 200 to the automated check; not confirmed)*
- PCI SSC, future-dated requirements of PCI DSS v4.x — <https://blog.pcisecuritystandards.org/now-is-the-time-for-organizations-to-adopt-the-future-dated-requirements-of-pci-dss-v4-x>
- HHS, HIPAA Security Rule NPRM fact sheet — <https://www.hhs.gov/hipaa/for-professionals/security/hipaa-security-rule-nprm/factsheet/index.html> *(did not return 200 to the automated check; not confirmed)*
- Clark Hill, HIPAA Security Rule update delayed to 2027 *(secondary)* — <https://www.clarkhill.com/news-events/news/hipaa-security-rule-update-delayed-until-2027/>
- FTC, updated Health Breach Notification Rule (2024) — <https://www.ftc.gov/business-guidance/blog/2024/04/updated-ftc-health-breach-notification-rule-puts-new-provisions-place-protect-users-health-apps>
- OCC, $80M civil money penalty against Capital One (2020) — <https://www.occ.gov/news-issuances/news-releases/2020/nr-occ-2020-101.html>
- FTC, Equifax settlement (2019) — <https://www.ftc.gov/news-events/news/press-releases/2019/07/equifax-pay-575-million-part-settlement-ftc-cfpb-states-related-2017-data-breach>
- National Law Review, T-Mobile data breach settlement *(secondary)* — <https://natlawreview.com/article/t-mobile-agrees-mdl-to-record-setting-350-million-data-breach-settlement-to-resolve>
- Google Play, target API level requirements (policy) — <https://support.google.com/googleplay/android-developer/answer/11926878>

### Incidents and vulnerability research
- Microsoft, TikTok one-click account hijack (2022) — <https://www.microsoft.com/en-us/security/blog/2022/08/31/vulnerability-in-tiktok-android-app-could-lead-to-one-click-account-hijacking/>
- Microsoft, Dirty Stream (2024) — <https://www.microsoft.com/en-us/security/blog/2024/05/01/dirty-stream-attack-discovering-and-mitigating-a-common-vulnerability-pattern-in-android-apps/>
- FTC, X-Mode / Outlogic order (2024) — <https://www.ftc.gov/news-events/news/press-releases/2024/01/ftc-order-prohibits-data-broker-x-mode-social-outlogic-selling-sensitive-location-data>
- NVD, CVE-2025-32711 (EchoLeak) — <https://nvd.nist.gov/vuln/detail/CVE-2025-32711>
- Snyk, Zip Slip (2018) — <https://security.snyk.io/research/zip-slip-vulnerability>
- Quarkslab, bypassing Android hardware attestation (August 2026) — <https://blog.quarkslab.com/bypassing-android-hardware-attestation.html>
- Elcomsoft, before-first-unlock extraction (2019) — <https://blog.elcomsoft.com/2019/12/bfu-extraction-forensic-analysis-of-locked-and-disabled-iphones/>

### Tools and practice targets
- Frida 17.0.0 release — <https://frida.re/news/2025/05/17/frida-17-0-0-released/>
- JADX — <https://github.com/skylot/jadx>
- WithSecure Labs, android-keystore-audit Frida scripts — <https://github.com/WithSecureLabs/android-keystore-audit/tree/master/frida-scripts>
- TEESimulator — <https://github.com/JingMatrix/TEESimulator>
- Vector (Xposed framework fork) — <https://github.com/JingMatrix/Vector>
- ElleKit — <https://github.com/tealbathingsuit/ellekit>
- Dopamine — <https://github.com/opa334/dopamine>
- palera1n — <https://github.com/palera1n/palera1n>
- bagbak (now deprecated by its author) — <https://github.com/ChiChou/bagbak>
- TrustKit — <https://github.com/datatheorem/TrustKit>
- HTTP Toolkit, Android 14 system CA changes — <https://httptoolkit.com/blog/android-14-breaks-system-certificate-installation/>
- HTTP Toolkit, installing a system CA on Android 14 — <https://httptoolkit.com/blog/android-14-install-system-ca-certificate/>
- HTTP Toolkit, Android 17 Certificate Transparency *(secondary)* — <https://httptoolkit.com/blog/android-17-certificate-transparency/>
- mitmproxy, system-trusted CA on Android — <https://docs.mitmproxy.org/stable/howto/install-system-trusted-ca-android/>
- Firebase Remote Config, Android — <https://firebase.google.com/docs/remote-config/android/get-started>
- Firebase AI Logic and App Check — <https://firebase.google.com/docs/ai-logic/app-check>
- MAS Test Apps, Android — <https://github.com/cpholguera/mas-app-android>
- MAS Test Apps, iOS — <https://github.com/cpholguera/mas-app-ios>
- iGoat-Swift — <https://github.com/OWASP/iGoat-Swift>
- InsecureShop — <https://github.com/hax0rgb/InsecureShop/>
- OVAA — <https://github.com/oversecured/ovaa>
- DIVA Android (2016, stale) — <https://github.com/payatu/diva-android>
- InsecureBankv2 (2019, stale) — <https://github.com/dineshshetty/Android-InsecureBankv2>

### Practitioner analysis
- What to use instead of EncryptedSharedPreferences — <https://blog.includesecurity.com/2026/08/encryptedsharedpreferences-is-dead-heres-what-you-should-use-instead/>
- DataStore and Tink migration guide — <https://proandroiddev.com/goodbye-encryptedsharedpreferences-a-2026-migration-guide-4b819b4a537a> *(behind a bot check; returned 403 to the automated check, not confirmed)*
- Maintained EncryptedSharedPreferences fork — <https://github.com/ed-george/encrypted-shared-preferences>
- Jason Bayton, key attestation root certificate change — <https://bayton.org/android/android-enterprise-faq/key-attestation-root-certificate-change/>
- Practical Play Integrity guide — <https://proandroiddev.com/a-practical-guide-to-play-integrity-api-everything-you-need-to-implement-attestation-on-android-c010f0fc8f09> *(behind a bot check; returned 403 to the automated check, not confirmed)*
- An independent view of Play Integrity's limits (vendor) — <https://approov.io/blog/limitations-of-google-play-integrity-api-ex-safetynet>
- Info.plist pinning and its shortcomings (Guardsquare) — <https://www.guardsquare.com/blog/leveraging-infoplist-based-certificate-pinning-ios-and-making-its-shortcomings>
- Marco Eidinger, testing `NSPinnedDomains` — <https://blog.eidinger.info/infoplist-based-certificate-pinning-on-ios>
- Secure Vale, deep dive into iOS certificate pinning — <https://securevale.blog/articles/deep-dive-into-certificate-pinning-on-ios/>
- Putting MASVS, MASTG and MASWE into practice (NowSecure) — <https://www.nowsecure.com/blog/2026/01/21/owasp-mobile-application-security-explained-how-to-put-masvs-mastg-and-maswe-into-practice/>
- Mobile Top 10 versus the MAS project (Guardsquare) — <https://www.guardsquare.com/blog/revisiting-owasp-mobile-top-10>
- iOS Keychain and Data Protection misuse — <https://medium.com/@salamsajid7/ios-keychain-and-data-protection-classes-abuse-and-misuse-759267ee03b4> *(behind a bot check; returned 403 to the automated check, not confirmed)*

### Removed in the September 2026 audit
Kept here so an old citation can be traced. None of these is relied on any more.
- `ibm.com/think/insights/cost-of-a-data-breach-industrial-sector` — a sector article, not the report. Replaced by the IBM report page.
- `databreachcost.com/report/2026` — an unaffiliated aggregator, by its own description. Replaced by IBM and Infosecurity Magazine.
- `shop.sslinsights.com` 47-day roadmap — secondary, and carried the wrong DCV arithmetic. Replaced by the CA/Browser Forum ballot and Baseline Requirements.
- `comviva.com` TEE and StrongBox article — a vendor blog that had been the source for the RKP root change. Replaced by Google's attestation documentation and 2022 RKP post.
- `developer.android.com/google/play/integrity/verdict` — wrong path; the page is `/verdicts`.
- `square.github.io/okhttp` — now returns 404; OkHttp's documentation moved to `lysine.dev/okhttp`.
- `developer.android.com/identity/digital-credentials/credential-issuer/keystore-attestation` — no chapter cites it; it supported no current claim.
- `vervali.com` "MASVS in 2026", `buildmvpfast.com` Actions hardening guide, `dev.to` Android hardening post — unaffiliated secondary pages not cited in any chapter; the primary sources (mas.owasp.org, GitHub docs, developer.android.com) are listed above.
- The Hacker News, "nine takeaways" from GitGuardian's 2026 report — a secondary summary of the GitGuardian report and blog listed above.

### Books
- *The Mobile Application Hacker's Handbook* — Chell, Erasmus, Colley, Whitehouse. Still the standard reference for methodology; published 2015, so read it for approach rather than current APIs.
- *Android Security Internals* — Elenkov. The best explanation of why the platform behaves as it does. Also dated.

---

## Glossary

One line per term, alphabetical. The reference in brackets is where the book teaches it.

- **16 KB page size** — Android 15+ devices that use 16 KB memory pages. Native libraries must be rebuilt and aligned; Play blocks non-compliant updates from 1 February 2027. *(§19.6)*
- **Accessibility service** — An app granted permission to read the screen and act for the user. `setAccessibilityDataSensitive` (API 34) hides a view from all but genuine accessibility tools. *(§17.6)*
- **ACME** — The protocol behind automated certificate issuance and renewal. Its default of a fresh key pair per certificate breaks leaf SPKI pins unless you reuse the key. *(§8.5)*
- **Actively exploited vulnerability** — In the CRA, a vulnerability with reliable evidence that a malicious actor has exploited it without the owner's permission. It triggers the 24-hour early warning. *(§30.1)*
- **`addWebMessageListener`** — AndroidX WebKit's recommended JavaScript bridge. It injects an object only into frames whose origin matches an allowlist. *(§16.2)*
- **AEAD** — Authenticated encryption with associated data: encryption that also detects tampering, optionally bound to non-secret context. AES-GCM is one. *(Chapter 0.2)*
- **`AeadSerializer`** — The `androidx.datastore:datastore-tink` class that encrypts a whole DataStore file with a Tink `Aead` (alpha since DataStore 1.3.0-alpha07). *(§6.3)*
- **Android developer verification** — Google's requirement that apps on certified Android devices come from registered developers: from 30 September 2026 for installs from Play and six partner stores in Brazil, Indonesia, Singapore and Thailand; from 2027 for all apps worldwide, sideloaded ones included. *(Chapter 0.4)*
- **App Attest** — Apple's service for proving that a request comes from a genuine instance of your app on a genuine Apple device, using a Secure Enclave key. *(Chapter 10)*
- **App Links / Universal Links** — `https` deep links verified against a file on your domain (`assetlinks.json`, `apple-app-site-association`). They prove the link reached your app, not that its parameters are safe. *(§17.5)*
- **App set ID** — An Android identifier scoped to one developer's apps on one device, for non-advertising uses. Not user-resettable. *(§18.2)*
- **App Store Connect team key** — An App Store Connect API key with a chosen role across the team. CI needs one for provisioning endpoints; individual keys cannot use them. *(§15.6)*
- **App Tracking Transparency (ATT)** — The iOS 14.5+ framework requiring the user's permission before tracking or reading the IDFA. *(§18.2)*
- **App-Bound Domains** — An iOS 14+ opt-in (`WKAppBoundDomains`, up to 10 domains) that limits a `WKWebView` to listed domains and restricts powerful APIs elsewhere. *(§16.2)*
- **Argon2id** — The memory-hard password-hashing function OWASP prefers. Minimum 19 MiB memory, 2 iterations, parallelism 1. Server-side. *(Chapter 0.2)*
- **Artifact attestation** — GitHub's Sigstore-signed build provenance: SLSA Build L2 by default, L3 through a reusable workflow. *(§15.5)*
- **ASN.1 / DER** — A notation for data structures, and the exact binary encoding of them used in certificates. A pin is the SHA-256 of the DER-encoded SPKI, so both platforms hash the same bytes. *(§8.10)*
- **Assertion** — In App Attest, a signature by the attested key over one request. The server checks the signature, the embedded challenge, the RP ID and a strictly increasing counter. *(§10.1)*
- **`ASWebAuthenticationSession`** — Apple's system-browser sign-in session. It supports `https` callbacks on associated domains from iOS 17.4. *(Chapter 0.3)*
- **Attack surface** — Every point where untrusted input or an untrusted actor meets your code. *(Chapter 0.1)*
- **Attestation** — A platform vendor's cryptographic statement about app, device or key properties. *(Chapter 5)*
- **Attestation challenge** — A server-issued, single-use value embedded in an attested key's certificate or an App Attest request, so an old answer cannot be replayed. *(§5.2)*
- **Attestation object (App Attest)** — The certificate chain, authenticator data and receipt returned by `attestKey`. *(§10.1)*
- **Auth Tab** — A Custom Tab specialised for sign-in (`androidx.browser` `AuthTabIntent`, Chrome 137+). It returns the redirect straight to the app and verifies `https` redirects with Digital Asset Links. *(Chapter 0.3)*
- **Authentication** — Proving who you are. Distinct from authorisation. *(Chapter 0.1)*
- **Authentication-bound key** — A Keystore or Keychain key that the secure hardware will use only after the user has authenticated. *(§4.6)*
- **Authorisation** — Deciding whether an authenticated party may do a particular thing. *(Chapter 0.1)*
- **Authorisation code flow** — The OAuth flow in which the browser returns a short-lived code that the app exchanges, with its PKCE verifier, for tokens. *(Chapter 0.3)*
- **Backend-for-Frontend (BFF)** — A thin server you run between the app and third-party APIs, holding the secrets and making the decisions the app must not. *(§12.3)*
- **Backup pin** — A second pin you can switch to without the thing that failed: a spare key pair you hold offline, or an intermediate at a different CA. *(§8.4)*
- **BFU / AFU** — Before / after first unlock since boot. Determines which Data Protection keys are in memory. *(§4.4)*
- **BOLA (broken object level authorisation)** — The server returns or changes an object without checking that it belongs to the caller. API1 in the OWASP API Security Top 10 (2023). *(Chapter 0.3)*
- **Build provenance** — A signed statement of how, where and from what source an artifact was built. It attests to the process, not to the cleanliness of the inputs. *(§15.5)*
- **Cache poisoning** — Writing malicious content to a CI cache that a trusted job later restores. *(§15.1)*
- **`cache-mode`** — A GitHub Actions setting (`read`, `write`, `write-only`, `none`) that limits a job's cache access. GA September 2026. *(§15.4)*
- **Certificate Transparency (CT)** — Public append-only logs of issued certificates. Enforced by browsers and iOS, opt-in on Android 16, on by default for Android apps targeting API 37. Detection, not prevention. *(§7.3)*
- **CIA triad** — Confidentiality, integrity, availability: the three properties security protects. *(Chapter 0.1)*
- **CI/CD** — Continuous integration and delivery: the automation that builds, tests and releases an app. *(Chapter 15)*
- **Class 3 / `BIOMETRIC_STRONG`** — Android's biometric tier strong enough to gate cryptographic operations. *(§11.2)*
- **Conscrypt APEX** — Android's TLS provider as an updatable module. From Android 14 the system CA store lives at `/apex/com.android.conscrypt/cacerts` and updates through Google Play, so mounting over `/system/etc/security/cacerts` no longer affects apps. *(§7.3, §22.1)*
- **Consumer rules** — Keep rules shipped inside a library's AAR or JAR and applied automatically by R8. *(§15.8)*
- **Content provider** — An Android component exposing structured data through a URI interface. *(§17.4)*
- **Content world (`WKContentWorld`)** — A separate JavaScript namespace in `WKWebView` that shares the DOM but not globals with the page (iOS 14+). *(§16.2)*
- **`CryptoObject`** — The Android object binding a biometric prompt to a cryptographic key, turning a boolean check into a real one. *(§11.1)*
- **Custom ROM** — A third-party build of Android. Common in some regions and a frequent source of false positives in root detection. *(§14.2)*
- **CVSS v4.0** — FIRST's severity-scoring standard (November 2023, still current). It measures severity, not risk. *(§23.3)*
- **Cyber Resilience Act (CRA)** — EU Regulation 2024/2847 on products with digital elements, commercial mobile apps included. Vulnerability and incident reporting has applied since 11 September 2026; full requirements from 11 December 2027. *(§30.1)*
- **Data extraction rules** — Android 12+ XML (`android:dataExtractionRules`) controlling cloud backup, device-to-device and cross-platform transfer. *(§6.5)*
- **Data Protection class** — The iOS setting that decides when a file's or Keychain item's key is available. Files use Complete, CompleteUnlessOpen, CompleteUntilFirstUserAuthentication and None; Keychain items use accessibility values instead: WhenUnlocked and AfterFirstUnlock (matching Complete and CompleteUntilFirstUserAuthentication), and WhenPasscodeSet, which has no file equivalent. Nothing matches CompleteUnlessOpen, and the Keychain's `Always` is deprecated. *(§4.4)*
- **Data safety section** — Google Play's store declaration of the data an app collects and shares. *(§18.3)*
- **DCV (domain control validation)** — The check a CA runs to confirm you control a domain before issuing a certificate. An earlier validation may be reused only if it is younger than the reuse period at the moment of issuance (200 days now, 100 from March 2027, 10 from March 2029), so at 10 days nearly every issuance needs a fresh validation. *(§8.5)*
- **`debug-overrides`** — An Android network security configuration block honoured only when the app is debuggable. Its trust anchors bypass pinning by default (`overridePins="true"`). *(§7.1)*
- **Deep link** — A URL that opens your app at a specific screen. Verified `https` links (App Links, Universal Links) prove the link reached your app; custom URI schemes can be claimed by any app. Neither makes the parameters safe. *(§17.5)*
- **DenyList / Shamiko** — Magisk's feature, and a module, for hiding root from chosen apps. *(§14.4)*
- **Dependency cooldown** — A delay before adopting newly published versions. Dependabot's default has been 3 days since July 2026. *(§15.3)*
- **Deserialisation** — Turning bytes into objects. Unsafe when the input chooses the type. *(§19.4)*
- **Device recognition verdict** — Play Integrity's list of device labels (`MEETS_BASIC_INTEGRITY`, `MEETS_DEVICE_INTEGRITY`, `MEETS_STRONG_INTEGRITY`, `MEETS_VIRTUAL_INTEGRITY`). Basic and strong are opt-in. *(§9.3)*
- **Digital Omnibus** — The European Commission's 2025 simplification package. Its AI Act part moved high-risk deadlines to December 2027 and August 2028; its GDPR part (96-hour, high-risk-only breach notification) was still a proposal in September 2026. *(§30.1)*
- **DNS-PERSIST-01 (persistent DCV)** — A DCV method (Ballot SC-088v3, effective 10 November 2025). One standing TXT record at `_validation-persist.<domain>` names your CA and account, and the CA re-checks it at each issuance with no per-renewal DNS change. *(§8.5)*
- **DORA** — The EU Digital Operational Resilience Act (Regulation 2022/2554): ICT risk and incident-reporting rules for financial entities, applicable since 17 January 2025. *(§30.1)*
- **DPoP** — Demonstrating Proof of Possession (RFC 9449). The client signs a per-request proof with a private key, binding its tokens to that key. *(Chapter 0.3)*
- **DV / OV / EV** — Domain-, organisation- and extended-validation certificates. They differ in how much the CA verified about your organisation, not in cryptographic strength. Irrelevant to pinning. *(§8.4)*
- **Dynamic analysis** — Running an app and observing or interfering with it at runtime. *(§13.2)*
- **Dynamic App Links** — Android 15+ server-side path and query rules in `assetlinks.json` (`dynamic_app_link_components`). *(§17.5)*
- **Dynamic code loading (DCL)** — Loading executable code at runtime from outside the signed package. *(§19.5)*
- **ECDH / ECDSA** — Elliptic-curve key agreement and signing. Smaller keys than RSA for equivalent strength. *(Chapter 0.2)*
- **ECH (Encrypted Client Hello)** — A TLS extension (RFC 9849) that encrypts the ClientHello, including the SNI hostname. On by default for Android apps targeting API 37 where the library supports it; experimental on Apple platforms. It does not affect pinning. *(§7.3)*
- **Embedding** — A numeric vector representation of text, used for semantic search and retrieval. *(§20.1)*
- **Event-bound biometric authentication** — The biometric unlocks a key that signs data specific to one operation, so the result cannot be replayed for another. *(§11.6)*
- **Excessive agency / unbounded consumption** — OWASP LLM risks: tools with too much power, and resource or cost abuse. *(§20.1)*
- **`expect` / `actual`** — The KMP mechanism by which common code declares something and each platform implements it. `expect`/`actual` classes are still Beta. *(Chapter 21)*
- **Explicit intent** — An Android intent naming its destination component. Use these for internal communication. *(§17.2)*
- **Exported component** — An Android activity, service, receiver or provider that other apps may start or query. *(§17.1)*
- **Fail-open** — A failure mode that restores availability by dropping a security check, as Android's `pin-set expiration` does. *(§8.6)*
- **FairPlay encryption** — Apple's DRM on App Store binaries. It must be removed, by dumping from memory on a jailbroken device, before static analysis. *(§1.1)*
- **FIPS 140** — The US government's standard for validating cryptographic modules; some regulated customers require FIPS-validated algorithms such as PBKDF2. *(Chapter 0.2)*
- **`FLAG_SECURE`** — The Android window flag that blocks screenshots, screen recording and the recents thumbnail for that window. *(§6.5)*
- **Foundation Models framework** — Apple's API (iOS 26+) to the on-device Apple Intelligence model and, since WWDC26, optionally the Private Cloud Compute model. *(§20.2)*
- **Fraud (risk) metric** — App Attest's approximate count of attested keys for your app on one device over 30 days, obtained by refreshing the receipt. Available since 2021. *(§10.3)*
- **Frida** — A dynamic instrumentation toolkit for hooking and modifying app behaviour at runtime. Frida 17 (May 2025) moved the Java and Objective-C bridges out of the core. *(§13.2)*
- **Frida Gadget** — Frida as an embeddable library, injected into a repackaged app so it can be hooked on a device that is not rooted or jailbroken. *(§13.2)*
- **FTC Health Breach Notification Rule** — The US rule requiring health apps outside HIPAA to notify users and the FTC of breaches, including unauthorised sharing. Amended rule effective 29 July 2024. *(§30.1)*
- **Gate (programme)** — The testable success criteria that must pass before the next phase of the security programme starts. *(§32.1)*
- **Gatekeeper** — The Android TEE component that verifies the user's PIN, pattern or password and issues a signed auth token that KeyMint checks before using an authentication-bound key. Biometrics use their own trusted apps, not Gatekeeper. *(§4.1)*
- **Gemini Nano / AICore** — Google's on-device model, and the Android system service that runs it. *(§20.2)*
- **Google Play SDK Index** — Google's catalogue of SDKs, with permission data and policy or vulnerability flags. *(§18.4)*
- **GPS** — The device's own satellite positioning. Distinct from IP geolocation, which is derived server-side from the network address. *(§12.5)*
- **HAL (hardware abstraction layer)** — The interface between Android and a device's hardware implementation. KeyMint is one. *(§4.1)*
- **Hardware authentication token (HAT)** — The HMAC-signed token that Gatekeeper or a biometric trusted app emits after successful authentication. KeyMint checks it before using an authentication-bound key. *(§11.1)*
- **Hash** — A one-way, fixed-size fingerprint of data. Not encryption: there is no key and no reversing it. *(Chapter 0.2)*
- **HMAC** — A keyed hash proving both integrity and that the sender held the shared key. *(Chapter 0.2)*
- **Hooking** — Intercepting a function call at runtime so that other code runs instead of it, or around it. *(§13.2)*
- **HSTS** — HTTP Strict Transport Security: a browser mechanism forcing HTTPS on later visits. For native clients, forbidding cleartext in configuration is the equivalent. *(§8.9)*
- **Identity pinning** — MASVS-NETWORK-2's umbrella term for restricting which server identities (a certificate, a public key or a CA) an app accepts. Apple also uses the name for `NSPinnedDomains` (see that entry). *(§8.2, §8.10)*
- **Immutable release** — A GitHub release whose tag and assets cannot change after publication (GA October 2025). *(§15.3)*
- **Implicit intent** — An Android intent describing an action and letting the system pick a handler. Interceptable; avoid for internal use. *(§17.2)*
- **Indirect prompt injection** — Attacker-controlled content steering a model's behaviour, arriving through content the model reads rather than the user's own message. *(§20.1)*
- **Injection** — A bug class in which data gets interpreted as code. Fixed by separating code from data. *(§19.3)*
- **Integrity token** — An encrypted, signed blob from Google Play services that only Google's server (or, for classic requests, your server with downloaded keys) can decrypt into a verdict. *(§9.1)*
- **Intent redirection** — A vulnerability in which an app launches an attacker-supplied nested intent under its own identity. *(§17.2)*
- **IPC** — Inter-process communication. On Android: intents, services, broadcasts and content providers. *(Chapter 17)*
- **IV (initialisation vector)** — A per-message cipher input that makes identical plaintext encrypt differently. With GCM it must never repeat under the same key. See Nonce. *(Chapter 0.2)*
- **JADX** — A decompiler turning an APK's DEX code into readable Java source. *(§1.1)*
- **JavaScript bridge** — A mechanism letting web content in a WebView call native code: Android `addJavascriptInterface` or `addWebMessageListener`, iOS script message handlers. *(§16.2)*
- **JWS** — JSON Web Signature: the signed form of a JWT. Readable by anyone; the signature proves origin and integrity only when verified. *(§9.1, §12.6)*
- **JWT** — JSON Web Token: base64url-encoded claims, usually signed rather than encrypted, so anyone can read the payload. *(Chapter 0.3)*
- **KDF (key derivation function)** — A function that derives a key from a password or from another key (Argon2id, scrypt, PBKDF2, HKDF). *(Chapter 0.2)*
- **Key authorization** — A condition of use, fixed at key creation and enforced by the secure hardware. *(§4.6)*
- **Keyblob** — Encrypted key material that the Android keystore daemon can store but cannot use or reveal. *(§4.1)*
- **Keybox** — Informal name for a factory-provisioned attestation key and certificate chain. Leaked keyboxes power attestation spoofing and are revoked. *(§5.4)*
- **KeyDescription** — The X.509 extension (OID 1.3.6.1.4.1.11129.2.1.17) that carries attestation data, with `softwareEnforced` and `hardwareEnforced` authorization lists. *(§5.2)*
- **KeyMint** — The Android Keystore HAL and trusted application that replaced Keymaster in Android 12. KeyMint 2 (Android 13) added Curve25519. *(§4.1)*
- **Keyset (Tink)** — Tink's container of working keys, usually encrypted by a Keystore master key. *(§6.3)*
- **keystore2** — The modern Android keystore daemon, rewritten in Rust. *(§4.1)*
- **KMP / CMP** — Kotlin Multiplatform and Compose Multiplatform: sharing logic, and sharing UI, across Android and iOS. *(Chapter 21)*
- **Launch validation category** — An iOS 27+ App Attest authenticator-data extension identifying how the app was launched and distributed. *(§10.3)*
- **LINDDUN** — A privacy threat-modelling framework; the privacy counterpart to STRIDE. *(Chapter 0.5)*
- **LLM / tool / agent** — A language model; an action the model may trigger; a model allowed to call tools in a loop. *(§20.1)*
- **MAC (message authentication code)** — A keyed value proving data was not altered and came from someone holding the shared key. HMAC-SHA256 is the usual choice. Unrelated to a network MAC address. *(Chapter 0.2)*
- **Mach-O** — The executable binary format used on iOS and macOS. *(§13.1)*
- **Magisk** — The most widely used Android root solution. "Systemless": it leaves the system partition untouched and can hide itself from chosen apps (DenyList). *(§14.4, §22.1)*
- **MAS testing profiles** — MAS-L1 (the baseline for every app: the OS is trusted, other apps are not), MAS-L2 (untrusted OS, physical access), MAS-R (the device's user is the adversary; added on top of L1 or L2), MAS-P (privacy), plus the specialised MAS-EUDIW. They replaced the old MASVS levels and are published at mas.owasp.org/Profiles. *(§3.2)*
- **MASTG** — OWASP Mobile Application Security Testing Guide: the tests. v2.0.0 (30 June 2026) completed the modular refactor, and all v1 tests (`MASTG-TEST-0001` to `0093`) are deprecated. *(§3.1)*
- **MASVS** — OWASP Mobile Application Security Verification Standard: the requirements. Currently v2.1.0, with 8 categories and 24 controls. *(§3.1)*
- **MASWE** — OWASP Mobile App Security Weakness Enumeration, which bridges controls and tests. v1.0.0 (17 August 2026) consolidated 119 beta entries into 78 and renumbered every ID once; IDs are stable from then on. *(§3.1)*
- **Memory Integrity Enforcement (MIE)** — Apple's hardware memory-safety system (EMTE plus secure allocators) on iPhone 17 and iPhone Air. Apps opt in through the Enhanced Security capability. *(§19.6)*
- **MITM (man-in-the-middle)** — An attack in which an adversary sits between two parties and can read or alter what passes. The book calls it interception; the coffee-shop attacker with an interception proxy is one. *(§7.1)*
- **ML-KEM / ML-DSA** — NIST's post-quantum key-encapsulation (FIPS 203) and signature (FIPS 204) algorithms. In the Secure Enclave through CryptoKit from iOS 26; ML-DSA in the Android 17 Keystore. *(Chapter 0.2)*
- **MPoC** — PCI Mobile Payments on COTS: the standard for accepting card payments on commercial phones (tap to pay). *(§30.1)*
- **MSTG** — The old name for the MASTG. A source still using it predates the v2 refactor. *(§3.1)*
- **NIS2** — EU Directive 2022/2555 on cybersecurity for essential and important entities. Transposition deadline 17 October 2024. *(§30.1)*
- **Nonce** — A number used once. Two senses: a protocol freshness value that stops replay, and a per-message cipher input (see IV). *(Chapter 0.2)*
- **`NSPinnedDomains`** — Apple's declarative pinning in `Info.plist` (iOS 14+), which Apple calls Identity Pinning. `NSIncludesSubdomains` covers one level only; it cannot change at runtime and has no expiry. `WKWebView` did not honour it in iOS 26.5 and 27.0 simulator tests. *(§8.10)*
- **OAEP** — Optimal Asymmetric Encryption Padding: the modern, randomised padding for RSA encryption. Use it instead of PKCS #1 v1.5 padding, which has practical attacks. *(Chapter 0.2)*
- **Obfuscation** — Transforming code so it is harder to read, without changing its behaviour. *(§14.3)*
- **objection** — A Frida-powered toolkit for runtime mobile exploration without writing scripts. Current syntax: `objection -n <app> start`. *(§8.10)*
- **OIDC token (in CI)** — A short-lived, workflow-scoped signed identity token that a job exchanges for cloud or registry credentials, replacing stored static keys. *(§15.1)*
- **`overridePins`** — A network security configuration attribute. When true, chains ending in that trust anchor skip pinning. *(§7.1)*
- **OWASP MAS identifiers** — `MASVS-…` requirements, `MASWE-…` weaknesses, and `MASTG-TEST/TECH/BEST/DEMO/KNOW-…` tests, techniques, best practices, demos and knowledge articles. *(Chapter 0.1, Chapter 3)*
- **Passkey** — A FIDO2/WebAuthn credential whose private key, unlocked by biometric or PIN, signs a server challenge. Synced passkeys prove the user, not the device. *(§11.7)*
- **PCI DSS v4.0.1** — The only active version of the Payment Card Industry Data Security Standard. Its future-dated requirements became mandatory on 31 March 2025. *(§30.1)*
- **`PendingIntent`** — A wrapped Android intent that another app can fire as you, with your permissions. Make it immutable, with an explicit base intent. *(§17.3)*
- **Photo picker** — A system UI that returns user-selected media without a storage or media permission. *(§18.1)*
- **Pin manifest** — A signed list of pins fetched at runtime in dynamic pinning, signed with a key outside the web PKI. *(§8.6)*
- **PKCE** — Proof Key for Code Exchange (RFC 7636). Protects an OAuth authorisation code in a public client; required for native apps by RFC 8252. *(Chapter 0.3)*
- **PKI (public key infrastructure)** — The system of certificate authorities and certificates that lets clients validate a server's identity. The web PKI is the public one your device trusts by default. *(§7.1, §8.6)*
- **Play App Signing** — Google holds your app signing key and re-signs on upload; you hold only a resettable upload key. *(§15.6)*
- **Post-quantum hybrid key exchange (`X25519MLKEM768`)** — TLS key agreement combining classical X25519 with ML-KEM, so recorded traffic resists future quantum decryption. The default in iOS 26 `URLSession`. *(§7.3)*
- **Privacy manifest (`PrivacyInfo.xcprivacy`)** — Apple's file declaring collected data, tracking domains and required-reason API use. *(§18.3)*
- **Public client** — An OAuth client that cannot keep a secret. Every mobile app is one. *(Chapter 0.3)*
- **`pull_request_target`** — A GitHub Actions trigger that runs in the base repository's context, with its secrets, even for fork pull requests. High risk. *(§15.3)*
- **RASP** — Runtime application self-protection: in-app detection of tampering and instrumentation, best used to produce signals. *(§14.2)*
- **Refresh token rotation** — Each refresh returns a new refresh token and invalidates the old one. RFC 9700 requires rotation or sender-constraining for public clients. *(Chapter 0.3)*
- **Remediation dialog** — A Play-provided screen (`GET_LICENSED`, `GET_INTEGRITY`, `GET_STRONG_INTEGRITY`, `CLOSE_*_ACCESS_RISK`) that lets a user fix a failing verdict. *(§9.4)*
- **Repackaging** — Decoding, modifying, rebuilding and re-signing an app with a different key. *(§1.1)*
- **Report-only mode** — Logging attestation verdicts without enforcing them, to learn the real distribution before blocking anyone. *(§32.2)*
- **`requestHash`** — A digest of the request a standard Play Integrity token is bound to; up to 500 bytes, returned verbatim in the verdict. *(§9.2)*
- **Required-reason API** — An Apple API that could be used for fingerprinting, whose use must be declared with an approved reason (enforced since 1 May 2024). *(§18.3)*
- **Revocation status list** — Google's JSON list of revoked or suspended attestation certificates, at `android.googleapis.com/attestation/status`. *(§5.2)*
- **RKP (Remote Key Provisioning)** — Short-lived attestation keys provisioned over the air instead of in the factory. Introduced in Android 12 and announced in 2022 as mandatory from 13; Google's attestation page now describes RKP support as optional under the Android 15 policy and the only option for devices launching with 16 (see Known uncertainties). Chains root in the ECDSA P-384 "Key Attestation CA 1" from 1 February 2026. *(§5.3)*
- **Rootless jailbreak** — An iOS jailbreak installed under `/var/jb`, leaving the system volume untouched. *(§14.4)*
- **Runner** — The machine that executes a CI job. *(§15.1)*
- **Safer Intents** — Android's multi-release tightening of intent resolution: StrictMode's `detectUnsafeIntentLaunch` (since API 31, Android 12; Android 15 extended what it reports), Android 16 `intentMatchingFlags`. *(§17.2)*
- **Salt** — A random per-password value added before hashing, defeating precomputed attacks. *(Chapter 0.2)*
- **Same-origin policy** — The browser rule that script from one origin (scheme, host and port) cannot read another origin's data. *(§16.1)*
- **Sandbox** — The platform isolation that gives each app private storage and its own process. *(Chapter 0.4)*
- **SBOM** — Software bill of materials: the inventory of every component in a build. *(§15.4)*
- **`sceneCaptureState`** — The iOS 17+ trait reporting whether a scene is being recorded or mirrored. *(§6.6)*
- **Script injection (CI)** — Untrusted text expanded by `${{ }}` into a `run:` script and executed. *(§15.3)*
- **Secure Enclave** — Apple's isolated secure subsystem for key storage and cryptography. P-256 keys through the Security framework; since iOS 26, CryptoKit adds ML-KEM and ML-DSA keys. No RSA and no symmetric keys. *(§4.3)*
- **Security level** — The Keystore's statement of where a key lives: `SOFTWARE`, `TRUSTED_ENVIRONMENT`, `STRONGBOX`, `UNKNOWN_SECURE` or `UNKNOWN` (`KeyInfo.getSecurityLevel()`, API 31+). *(§4.2)*
- **securityd** — The iOS daemon that mediates Keychain access based on entitlements. *(§4.3)*
- **Sender-constrained token** — A token usable only by the holder of a bound key (DPoP, mTLS). The opposite of a bearer token. *(Chapter 0.3)*
- **SHA pinning** — Referencing a dependency or CI action by immutable commit hash rather than by a mutable tag. *(§15.3)*
- **Sigstore** — Open signing infrastructure using short-lived, OIDC-bound certificates and a transparency log. *(§15.5)*
- **Single Reporting Platform (SRP)** — ENISA's portal for CRA early warnings, notifications and final reports. *(§30.1)*
- **SLSA** — Supply-chain Levels for Software Artifacts. v1.2 defines Build levels L0–L3 and a Source track. *(§15.5)*
- **Smali** — Human-editable assembly for Dalvik bytecode, produced by apktool. *(§13.1)*
- **SNI (Server Name Indication)** — The hostname a client sends in the TLS ClientHello so one server can host many certificates. Visible to the network unless ECH is used. *(§7.3)*
- **SPKI** — Subject Public Key Info: the public key and its algorithm. The thing to pin, because it survives renewal with a reused key. *(§8.4)*
- **Spotlighting** — Delimiting untrusted content in a prompt so the model treats it as data. Probabilistic, not a guarantee. *(§20.1)*
- **SQLCipher** — An encrypted drop-in replacement for SQLite. On Android, `net.zetetic:sqlcipher-android`. *(§6.7)*
- **SSL** — The predecessor to TLS, long obsolete as a protocol but still used loosely in phrases such as "SSL pinning", which in practice always means TLS. *(§8.4)*
- **Standard / classic request** — Play Integrity's two request types. Standard: a pre-warmed provider, `requestHash`, and replay protection by Google. Classic: your server's nonce, and replay protection is yours. *(§9.2)*
- **`state` (OAuth)** — A random value tying an authorisation response to the request the app started (CSRF protection). *(Chapter 0.3)*
- **Static / dynamic / hybrid pinning** — Pins baked in at build time; pins fetched at runtime from a signed manifest; or both, with a static backup under a dynamic primary. *(§8.6)*
- **Static analysis** — Reading an app's code and resources without running it. *(§13.1)*
- **Step-up authentication** — Requiring additional proof for a sensitive action inside an existing session. *(Chapter 0.3)*
- **STRIDE** — A threat-modelling prompt set: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. *(Chapter 0.5)*
- **StrongBox** — A KeyMint implementation in a separate secure processor (an embedded or integrated secure element). From Android 9; optional, slower, with a reduced algorithm set. *(§4.2)*
- **Supply-chain attack** — Compromising something the build trusts (a dependency, tool, cache or action) rather than the app itself. *(§15.1)*
- **Systemless root** — Rooting that does not modify `/system` (Magisk, KernelSU, APatch), so file checks miss it. *(§14.4)*
- **Tapjacking (overlay attack)** — Tricking the user into tapping through, or around, a window another app draws over yours. *(§17.6)*
- **TEE (trusted execution environment)** — A hardware-isolated area of the main processor that runs trusted applications such as KeyMint. *(§4.1)*
- **`ThisDeviceOnly`** — A Keychain accessibility suffix. The item is backed up only in a form usable on the same device, and never migrates or syncs. *(§4.4)*
- **Threat Modeling Manifesto questions** — What are we working on? What can go wrong? What are we going to do about it? Did we do a good enough job? *(Chapter 0.5)*
- **Trust anchor** — The key or certificate a verification ultimately rests on. In dynamic pinning it is your manifest signing key, not a CA. *(§7.1, §8.10)*
- **Trust boundary** — A line where data crosses from something you control to something you do not. Every one needs a check. *(Chapter 0.5)*
- **Trust store** — The set of root CA certificates a platform trusts (about 150 on current Apple OSes). Updatable through Google Play system updates from Android 14. *(§7.1, §7.3)*
- **Trusted publishing** — Registry publishing authenticated by the CI's OIDC identity instead of a stored token. *(§15.3)*
- **Trusty** — Google's open-source TEE implementation, provided to OEMs. *(§4.1)*
- **TXT record** — A DNS record holding arbitrary text. CAs use it for domain validation, including the standing record in persistent DCV. *(§8.5)*
- **Upload key** — The key that proves to Google Play an upload came from you. Resettable, unlike the app signing key. *(§15.6)*
- **Validated (evaluated) chain** — The chain the platform builds from the server's certificates, cached intermediates and cross-signs. It is what every pinning mechanism compares against. *(§8.4)*
- **Verified boot** — A hardware-backed check that the device booted an unmodified OS. On Android 13+, Play Integrity's device verdict requires it, with a locked bootloader. *(Chapter 0.4)*
- **WebView** — An embedded browser engine running web content inside your app's security context. *(Chapter 16)*
- **`WebViewAssetLoader`** — The AndroidX class that serves bundled assets over `https://appassets.androidplatform.net` instead of `file://`. *(§16.3)*
- **WHOIS** — The public registry of domain ownership records. WHOIS-based contact lookup for DCV ended on 15 July 2025 (SC-080); the remaining email and phone methods retire in March 2027 and March 2028 (SC-090). *(§8.5)*
- **Zip Slip** — Archive-extraction path traversal through entry names containing `../`. *(Chapter 19, §19.8)*
- **Zygisk** — Magisk's mechanism for running code inside the Zygote, the process every Android app is forked from, so modules can hook any app. *(§13.2)*

---

*Corrections and additions welcome. If you find something stale, update Chapter 33 with the date and what changed — that is what keeps a book like this worth reading.*
