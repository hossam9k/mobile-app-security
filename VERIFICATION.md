# Verification status

This book makes claims about platform behavior. This file records how each kind of claim was established, so you can decide what to trust before you read the whole book.

**Last full audit:** 23–24 September 2026. Every part was re-verified against live primary sources. Then an editor with no prior context read it for contradictions, and ten independent reviewers who hadn't written the text checked it again. For details, counts, and every correction, see [Chapter 33](book/12-verification.md).

**Last editorial and currency pass:** 20 October 2026. Every claim was re-checked against primary sources, and the house style moved to American spelling. See [Part 12](book/12-verification.md#editorial-and-currency-pass-20-october-2026).

---

## How claims are marked in the text

Any claim weaker than a primary source carries a marker inline:

| Marker | Means |
|---|---|
| *(reported)* | A vendor or practitioner figure. The mechanism is corroborated; the exact number may not be |
| *(estimate)* | A planning figure, not a measurement. Scale it to your situation |
| *(reasoned)* | A conclusion drawn by analogy or from first principles, not quoted from a standard |
| *(contested)* | The industry disagrees. The text gives both sides |
| *(illustrative)* | A made-up scenario or example that shows a mechanism, not a report of a real event |

**Unmarked claims trace to a primary source**: a standards body, vendor documentation, or an official report. [Part 12](book/12-verification.md) lists all 284 sources at the end.

---

## The "Verify it" blocks are mostly a test plan

Each implementation section ends with a **Verify it** block that gives the command and a pass/fail criterion. The blocks are written from documented tool behavior and the test procedures in the OWASP Mobile Application Security Testing Guide (MASTG).

**Most haven't been run against a live app.** The blocks describe the expected output; they never invent it. If behavior varies by device or OS version, the block says so. The exceptions are in Part 3: its Swift and OkHttp listings were compiled and run, and four of the claims below were tested on an Android 17 emulator and on iOS 26.5 and 27.0 simulators. Those chapters carry an **Evidence** callout that says exactly what was run.

If you run a **Verify it** block and get a different result, file an [empirical result issue](.github/ISSUE_TEMPLATE/empirical-result.md). It's the most useful thing you can contribute.

---

## Claims with no hardware evidence

Six claims were first stated from vendor documentation or practitioner reporting. On 23–24 September 2026, four were tested on an emulator or simulator. **A simulator or emulator is not a phone**: the hardware key stores (the Secure Enclave on Apple devices, StrongBox on Android), carrier networks, and OEM WebView builds are absent or different. These results are stronger evidence than a citation and weaker than a test on hardware.

| # | Claim | Where | Status, 24 September 2026 |
|---|---|---|---|
| 1 | `NSPinnedDomains` does not cover `WKWebView` or `SFSafariViewController` | §8.6, §8.10 | **Supported for `WKWebView` on iOS 26.5 and 27.0 simulators**: a wrong pin made `URLSession` fail with -1200 while `WKWebView` loaded the page. Published reports conflict. `SFSafariViewController` untested |
| 2 | Android network security config (NSC) covers WebView traffic, while OkHttp `CertificatePinner` does not | §8.6 | **Confirmed on an Android 17 emulator**: a wrong NSC pin failed `HttpsURLConnection`, plain OkHttp, and WebView alike. The configuration covers OkHttp too, and `CertificatePinner` installs no trust manager |
| 3 | `pin-set expiration` fails open: pinning stops being enforced after the date | §8.6 | **Confirmed on an Android 17 emulator**: a wrong pin with a past expiration connected on all three clients; with a future expiration, all three failed |
| 4 | Changing `NSPinnedDomains` may require an app reinstall before ATS drops the cached trust setting | §8.10 | **Not reproduced** on iOS 26.5 and 27.0 simulators: an update-install took effect on the next launch, in both directions. Xcode-run and device installs untested; still *(reported)* |
| 5 | Re-decrypting a Play Integrity token returns cleared verdicts | §9.2 | **Still untested.** Google says a token cannot be "reused many times" and gives no number. Chapter 9's Try it describes the test |
| 6 | A subset of devices return `DCError.invalidKey` persistently, surviving reinstall and reboot | §10.4 | **Still unreproduced.** A September 2026 Apple Developer Forums thread reports about 0.01% of one app's users affected for weeks; Apple has not replied |

**One small test on a real device would settle each of these.** If you run one, open an [empirical result issue](.github/ISSUE_TEMPLATE/empirical-result.md). The result goes into the chapter with credit.

---

## What the last audit did not cover

An audit that doesn't state its own coverage gives you no way to judge it, so here are the gaps.

- **Hardware.** No claim was tested on a physical phone (see the previous section).
- **Compiling everything.** The listings in Parts 3, 5, and 6 were compiled or type-checked, and on 20 October 2026 the server listings in §5.5 and §10.7 were compiled and run on the JVM. For Parts 2, 4, and 7, every API was checked against its reference documentation or source, but not every block was compiled. Every Swift block parses (`swiftc -parse`) and every XML block is well formed: `scripts/check.py` checks both wherever `swiftc` and `xmllint` are installed, which includes CI.
- **Gated primary sources.** The IBM Cost of a Data Breach report PDF sits behind a registration form. Where the text depends on press coverage of it, it's marked *(reported)*. The OWASP Top 10 for LLM Applications 2026, once available only as a download, is now public in the project's GitHub repository, and Chapter 20 cites it directly.
- **MAS data drift.** In some MASTG v2 tests, the `maswe:` metadata points to a neighboring weakness. The book cites tests by topic, and its per-weakness test counts follow the MASWE pages.
- **Part 10.** The answers were reconciled against the rewritten chapters, not researched from scratch, so an error in a chapter carries into its answers.

---

## Where to look first when re-verifying

[Part 12](book/12-verification.md) has the full table with the reasoning. In summary:

| Cadence | Chapters |
|---|---|
| Quarterly | 5, 6 storage and attestation; 7, 8 TLS and pinning; 9 Play Integrity; 15 pipeline; 20 AI features |
| After each WWDC | 10 App Attest |
| Per MAS release | 3, 26–28 the standard and catalogs |
| Per major OS release | 4, 11, 16, 17, 19 |
| Semi-annually | 13, 14, 18, 22–25 tooling, privacy, and assessment |
| With each re-check of the chapters it cites | Part 10 questions and answers |
| Per Kotlin release | 21 Kotlin Multiplatform |
| Each July, and on regulatory dates | 29–32 the business case |
| Annually | 0, 1, 2 (on report release), 12 |

Each part file carries `last_verified` and `volatility` in its frontmatter, so the metadata travels with the file instead of living only here.

---

## Corrections already made

[Part 12](book/12-verification.md) lists every error found and fixed, including the ones found late:

- A content-provider sample labeled "safe" that still passed the caller's column list into SQL, so it was injectable
- An iOS pinning helper that hashed the raw key instead of the SPKI (the encoded public key and its algorithm), so it could never match a pin produced anywhere else
- A biometric example that sent the server output it couldn't verify
- An iOS WebView bridge example registered in a content world the page can't reach
- A deprecated OWASP test cited as current, and later every v1 test after MASTG v2.0.0
- Domain control validation (DCV) reuse arithmetic derived two contradictory ways, then "corrected" wrongly, and now corrected against the CA/Browser Forum Baseline Requirements
- A storage API recommended nine months after Google deprecated it
- 56 section numbers attached to the wrong chapters after a renumbering
- Breach-cost and secrets figures carried forward from superseded annual reports

The book includes that list on purpose. A reference whose errors are invisible is harder to trust than one that shows them.
