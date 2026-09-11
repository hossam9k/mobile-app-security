# Changelog

Corrections are the point of this repository, so they are recorded here as well as in
[Part 12](book/12-verification.md). Newest first.

## 2026-09-11

- **Added** a `Verify it` block to all eight implementation sections: the command to run and a
  pass/fail criterion, with an explicit note that they were not executed against a live app.
- **Added** §6.2, stubs for superseded advice — Jetpack Security Crypto, SafetyNet, `UIWebView`,
  WHOIS email validation, "MASVS L1/L2", and two deprecated MASTG tests — so the old terms stay
  findable for readers arriving from older articles.
- **Added** a per-chapter volatility table with re-check cadences, and a table of six claims
  asserted from documentation but never tested on a device.
- **Added** `last_verified` and `volatility` frontmatter to every part file.
- **Fixed** 56 of 152 section numbers that carried the wrong chapter number after an earlier
  renumbering. Chapter 20 held sections numbered 16.x while Chapter 16 held 19.x, so
  cross-references landed in the wrong chapter. All 153 now match; all references resolve.
- **Fixed** 33 interrupting em-dash asides down to 0.
- **Added** nine glossary entries for acronyms used but undefined: ASN.1/DER, GPS, MAC, SSL,
  TXT record, WHOIS. `DER-encoded ASN.1` had been used in the SPKI explanation without ever
  being defined.
- **Removed** a precise vote count for CA/Browser Forum Ballot SC-081v3 that sources disagree
  about, replaced with what all sources support.
- **Corrected** validation arithmetic in §8.5. The chapter had derived DCV frequency two
  contradictory ways, four paragraphs apart.
