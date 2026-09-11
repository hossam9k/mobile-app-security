# Verification status

This book makes claims about platform behaviour. This file records how each kind of claim was established, so you can decide what to trust without reading all 102 pages first.

**Last full structural audit:** 11 September 2026.

---

## How claims are marked in the text

Anything weaker than a primary source carries a marker inline:

| Marker | Means |
|---|---|
| *(reported)* | Vendor or practitioner figure. Mechanism corroborated, exact number may not be |
| *(estimate)* | A planning figure, not a measurement. Scale it to your situation |
| *(reasoned)* | A conclusion drawn by analogy or first principles, not quoted from a standard |
| *(contested)* | The industry genuinely disagrees. Both sides are given |

**Unmarked claims trace to a primary source** — a standards body, vendor documentation, or an official report. All sources are linked at the end of [Part 12](book/12-verification.md).

---

## The "Verify it" blocks are a test plan, not a transcript

Each implementation section ends with a **Verify it** block giving the command and a pass/fail criterion. These are written from documented tool behaviour and the OWASP MASTG test procedures.

**They were not executed against a live app while writing.** Expected outputs are described, never fabricated. Where behaviour varies by device or OS version, the block says so.

If you run one and get a different result, that is an [empirical result issue](.github/ISSUE_TEMPLATE/empirical-result.md) and it is the most useful thing you can file here.

---

## Claims asserted but not empirically tested

These come from vendor documentation or practitioner reporting. **Nobody involved in writing this book verified them on a device.** Each is one small test app away from being demonstrated rather than cited.

| # | Claim | Where | Basis |
|---|---|---|---|
| 1 | `NSPinnedDomains` does not cover `WKWebView` or `SFSafariViewController` | §8.6, §8.10 | Documented, widely reported |
| 2 | Android network security config *does* cover WebView traffic, while OkHttp `CertificatePinner` does not | §8.6 | `MASTG-KNOW-0015` plus OkHttp's documented scope |
| 3 | `pin-set expiration` fails open — pinning stops being enforced after the date | §8.6 | Documented behaviour |
| 4 | Changing `NSPinnedDomains` may require an app reinstall before ATS drops the cached trust setting | §8.10 | Practitioner-reported |
| 5 | Re-decrypting a Play Integrity token returns cleared verdicts | §9.2 | Google documentation |
| 6 | A subset of devices return `DCError.invalidKey` persistently, surviving reinstall and reboot | §10.4 | Developer forum reports |

**Claims 1, 2 and 3 have very little published evidence either way.** A small app that settles them would be original research. If you build one, open an issue — the result goes into the chapter with credit.

---

## What the last audit did not cover

Stated because an audit that does not declare its own coverage is worthless.

- **Currency was not re-checked in the most recent pass.** No API, version or statistic was re-verified against a live source on 11 September. Currency rests on verification dated 10–11 September, chapter by chapter — see the volatility table in [Part 12](book/12-verification.md).
- **Evidence tiering was checked for marker presence, not applied claim by claim.** The book contains roughly 500 numeric and normative claims. 29 carry markers. The rest are unmarked because they traced to a primary source when written, not because each was re-confirmed.
- **Implementability was not systematically tested.** Whether a reader can actually build each control from what is written was not verified control by control. 27 sections of the original strategy documents contain complete working code that this book only sketches; those remain in the companion Implementation Guide.
- **The source-document diff is keyword-matched, not semantic.** A topic covered in different words may read as missing; one sharing vocabulary may read as covered while saying something different.

---

## Where to look first when re-verifying

Full table with reasoning in [Part 12](book/12-verification.md). Summary:

| Cadence | Chapters |
|---|---|
| Quarterly | 6 storage, 8 pinning, 9 Play Integrity, 15 pipeline, 20 AI features |
| After each WWDC | 10 App Attest |
| Per MASTG release | 26–28 catalogues |
| Per major OS release | 16, 17, 19 platform surfaces |
| Annually | 0, 1, 4, 5, 11, 12 foundations and stable internals; 2 and 11 on report release |

Each part file carries `last_verified` and `volatility` in its frontmatter, so the metadata travels with the file rather than living only here.

---

## Corrections already made

[Part 12](book/12-verification.md) lists every error found and fixed during writing, including the ones found late:

- A deprecated OWASP test cited as current
- Validation arithmetic derived two contradictory ways, four paragraphs apart
- A storage API recommended nine months after Google deprecated it
- 56 section numbers attached to the wrong chapters after a renumbering
- Breach-cost and secrets figures carried forward from superseded annual reports
- A precise vote count that sources disagree about, now removed rather than picked

That list is in the book deliberately. A reference whose errors are invisible is harder to trust than one that shows them.
