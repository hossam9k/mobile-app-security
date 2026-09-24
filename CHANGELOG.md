# Changelog

Corrections are the point of this repository, so they are recorded here as well as in
[Part 12](book/12-verification.md). Newest first.

## 2026-09-24 — final verification pass and diagram redesign

- **Ten independent reviewers**, none of whom wrote the text, re-checked every part against primary
  sources: 1 critical, 32 major and 152 minor findings. All critical and major findings are fixed, and
  minor ones where they improved the book (fix logs record each decision). The critical one: §17.8's
  content-provider sample, labelled safe, passed the caller's projection into SQL. It now allowlists columns.
- **Corrected** the Android developer verification scope (the September 2026 phase covers Play and six
  partner stores in four countries; sideloaded apps from 2027), the Play Console signing path (now
  *Protected with Play → Play Store protection → Manage Play app signing*), the key-attestation relay
  explanation, refresh-token reuse detection, artifact-attestation plan limits, the pin-manifest
  signing design, and the IBM AI-breach wording.
- **Added** server-side App Attest attestation verification (§10.7) and a projection-injection probe.
- **Redesigned all 27 diagrams**: one house theme, one text size, no labels crossed by lines, numbered
  captions under every figure, and named high-resolution PNGs in `dist/diagrams/`.
- **Tooling:** the build pins its diagram renderer and stamps the PDF with the content date; the checker
  verifies figure captions and the repository's own workflow; CI installs xmllint and pins an image
  with Swift.

## 2026-09-24 — full audit and rewrite

Every part re-verified against live primary sources, rewritten for teaching, then read cold by an
editor for contradictions. Chapter 33 has per-part counts and every correction.

- **Fixed code that could not work.** The iOS pinning delegate hashed the raw key, not the SPKI, so it
  never matched an OpenSSL or Android pin (§8.10; now tested against OpenSSL for P-256, P-384 and RSA).
  The biometric example sent the server AES output it could not verify (§11.6; now an EC signing key).
  The iOS WebView bridge was registered in a content world the page cannot reach (§16.8). Part 5's
  detection code did not compile. The Part 6 R8 block had its Verify it section pasted inside the fence.
- **Tested four untested claims** on an Android 17 emulator and iOS 26.5/27.0 simulators: three
  confirmed or supported, one not reproduced. The network security configuration also covers OkHttp.
- **Brought the OWASP material current.** MASTG v2.0.0 (30 June 2026) deprecated every v1 test and
  MASWE v1.0.0 (17 August 2026) renumbered every weakness; all cited IDs checked, deprecated ones
  replaced. MASVS control statements now verbatim. MAS profiles: L1 (baseline), L2, R, P, EUDIW.
- **Corrected about 250 stale or wrong facts**, among them: EncryptedSharedPreferences shipped a
  deprecated stable 1.1.0 and has an official successor (`datastore-tink`); Play Integrity and App
  Attest quotas are documented, not practitioner-reported; the App Attest fraud metric dates from 2021;
  a device-credential fallback switches off biometric enrolment invalidation; Android 17 enables CT and
  ECH by default; the DCV reuse arithmetic; GitGuardian's 3.2% figure is about one tool; incident
  details for tj-actions, Shai-Hulud, TanStack and others.
- **Added for learning:** a *Start here* preface (previously only in the PDF), a hook, Key takeaways and
  Try it for every chapter, 27 Mermaid diagrams, a "Reading OWASP IDs" table, an attacker-to-controls
  map, a Keystore/Keychain comparison, a platform-defaults-by-version table, a worked CVSS v4.0 finding,
  and an incident-levers table.
- **Added server-side code** the book's thesis needed: key-attestation verification (§5.5), Play
  Integrity (§9.6), App Attest attestation and assertion verification (§10.7), passkeys (§11.7), DPoP
  (§12.6).
- **Part 10** rebuilt: 156 questions (from 75) tagged Beginner/Intermediate/Advanced, each pointing to
  the section that teaches it, plus a design-review scenarios group.
- **Part 11** now opens with an executive summary and decision table; regulation updated (CRA, DORA,
  NIS2, AI Act, PCI DSS v4.0.1, HIPAA proposal status).
- **Part 12:** sources from 58 to 278, grouped and link-checked; glossary from 81 to 210 terms; old log
  entries now known to be wrong annotated as superseded rather than deleted.
- **Unified house style:** British spelling in prose, one set of callouts and confidence markers (new:
  *(illustrative)*), `§` for sections, far fewer em dashes, duplicated material merged.
- **Tooling:** `scripts/build.py` builds the single-file Markdown and the PDF (Mermaid rendered);
  `scripts/check.py` checks references, captions, fences, Swift and XML (plus workflow YAML and diagram
  rendering where actionlint and Node are installed);
  `.github/workflows/check-book.yml` runs the checks and fails if `dist/` is stale.

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
