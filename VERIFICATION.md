# Verification status

This book makes claims about platform behaviour. This file records how each kind of claim was established, so you can decide what to trust without reading the whole book first.

**Last full audit:** 23–24 September 2026. Every part was re-verified against live primary sources, read cold by an editor for contradictions, then checked again by ten independent reviewers who had not written the text. Details, counts and every correction: [Chapter 33](book/12-verification.md).

---

## How claims are marked in the text

Anything weaker than a primary source carries a marker inline:

| Marker | Means |
|---|---|
| *(reported)* | Vendor or practitioner figure. Mechanism corroborated, exact number may not be |
| *(estimate)* | A planning figure, not a measurement. Scale it to your situation |
| *(reasoned)* | A conclusion drawn by analogy or first principles, not quoted from a standard |
| *(contested)* | The industry genuinely disagrees. Both sides are given |
| *(illustrative)* | A made-up scenario or example used to show a mechanism, not a report of a real event |

**Unmarked claims trace to a primary source**: a standards body, vendor documentation, or an official report. All 278 sources are listed at the end of [Part 12](book/12-verification.md).

---

## The "Verify it" blocks are mostly a test plan

Each implementation section ends with a **Verify it** block giving the command and a pass/fail criterion. These are written from documented tool behaviour and the OWASP MASTG test procedures.

**Most were not executed against a live app.** Expected outputs are described, never fabricated. Where behaviour varies by device or OS version, the block says so. The exceptions are in Part 3: its Swift and OkHttp listings were compiled and run, and four claims below were tested on an Android 17 emulator and iOS 26.5 and 27.0 simulators. Those chapters carry an `Evidence` note saying exactly what was run.

If you run a Verify it block and get a different result, that is an [empirical result issue](.github/ISSUE_TEMPLATE/empirical-result.md) and it is the most useful thing you can file here.

---

## Claims with no hardware evidence

Six claims were first stated from vendor documentation or practitioner reporting. On 23–24 September 2026, four were tested on an emulator or simulator. **A simulator or emulator is not a phone**: the Secure Enclave, StrongBox, carrier networks and OEM WebView builds are absent or different. These results are stronger than citation and weaker than hardware.

| # | Claim | Where | Status, 24 September 2026 |
|---|---|---|---|
| 1 | `NSPinnedDomains` does not cover `WKWebView` or `SFSafariViewController` | §8.6, §8.10 | **Supported for `WKWebView` on iOS 26.5 and 27.0 simulators**: a wrong pin made `URLSession` fail with -1200 while `WKWebView` loaded the page. Published reports conflict. `SFSafariViewController` untested |
| 2 | Android network security config covers WebView traffic, while OkHttp `CertificatePinner` does not | §8.6 | **Confirmed on an Android 17 emulator**: a wrong NSC pin failed `HttpsURLConnection`, plain OkHttp and WebView alike. The configuration covers OkHttp too, and `CertificatePinner` installs no trust manager |
| 3 | `pin-set expiration` fails open: pinning stops being enforced after the date | §8.6 | **Confirmed on an Android 17 emulator**: a wrong pin with a past expiration connected on all three clients; with a future expiration, all three failed |
| 4 | Changing `NSPinnedDomains` may require an app reinstall before ATS drops the cached trust setting | §8.10 | **Not reproduced** on iOS 26.5 and 27.0 simulators: an update-install took effect on the next launch, in both directions. Xcode-run and device installs untested; still *(reported)* |
| 5 | Re-decrypting a Play Integrity token returns cleared verdicts | §9.2 | **Still untested.** Google says a token cannot be "reused many times" and gives no number. Chapter 9's Try it describes the test |
| 6 | A subset of devices return `DCError.invalidKey` persistently, surviving reinstall and reboot | §10.4 | **Still unreproduced.** A September 2026 Apple Developer Forums thread reports about 0.01% of one app's users affected for weeks; Apple has not replied |

**Every one of these is one small test on a real device away from being settled.** If you run one, open an issue: the result goes into the chapter with credit.

---

## What the last audit did not cover

Stated because an audit that does not declare its own coverage is worthless.

- **Hardware.** No claim was tested on a physical phone (see above).
- **Compiling everything.** Parts 3 and 5 compiled their listings; Parts 2, 4 and 7 checked every API against its reference documentation or source but did not compile every block. Every Swift block parses (`swiftc -parse`) and every XML block is well formed: `scripts/check.py` checks both wherever `swiftc` and `xmllint` are installed, which includes CI.
- **Gated primaries.** The IBM report PDF sits behind a registration form and the OWASP LLM Top 10 2026 list behind a download. Where the text depends on press coverage of them, it is marked *(reported)*.
- **MAS data drift.** Some MASTG v2 tests' `maswe:` metadata links to a neighbouring weakness. The book cites tests by topic; per-weakness test counts follow the MASWE pages.
- **Part 10** answers were reconciled against the rewritten chapters rather than researched from scratch, so a wrong chapter would propagate into its answers.

---

## Where to look first when re-verifying

Full table with reasoning in [Part 12](book/12-verification.md). Summary:

| Cadence | Chapters |
|---|---|
| Quarterly | 5, 6 storage and attestation; 7, 8 TLS and pinning; 9 Play Integrity; 15 pipeline; 20 AI features |
| After each WWDC | 10 App Attest |
| Per MAS release | 3, 26–28 the standard and catalogues |
| Per major OS release | 4, 11, 16, 17, 19 |
| Semi-annually | 13, 14, 18, 22 tooling and privacy |
| Per Kotlin release | 21 Kotlin Multiplatform |
| Each July, and on regulatory dates | 29–32 the business case |
| Annually | 0, 1, 2 (on report release), 12 |

Each part file carries `last_verified` and `volatility` in its frontmatter, so the metadata travels with the file rather than living only here.

---

## Corrections already made

[Part 12](book/12-verification.md) lists every error found and fixed, including the ones found late:

- A content-provider sample labelled "safe" that still passed the caller's column list into SQL (injectable)
- An iOS pinning helper that hashed the raw key instead of the SPKI, so it could never match a pin produced anywhere else
- A biometric example that sent the server output it could not verify
- An iOS WebView bridge example registered in a content world the page cannot reach
- A deprecated OWASP test cited as current, and later every v1 test after MASTG v2.0.0
- Validation arithmetic derived two contradictory ways, then "corrected" wrongly, now corrected against the Baseline Requirements
- A storage API recommended nine months after Google deprecated it
- 56 section numbers attached to the wrong chapters after a renumbering
- Breach-cost and secrets figures carried forward from superseded annual reports

That list is in the book deliberately. A reference whose errors are invisible is harder to trust than one that shows them.
