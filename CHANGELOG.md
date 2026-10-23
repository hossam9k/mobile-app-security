# Changelog

Corrections are the point of this repository, so they are recorded here as well as in
[Part 12](book/12-verification.md). Newest first.

## 2026-10-22 — code samples dual-licensed

- **Cheat sheet re-verified** against the book: 18 accuracy fixes (for example, App Attest results are verified by your own server, and a SPKI pin survives only renewals that keep the same key).
- **README links [masaudit](https://github.com/hossam9k/masaudit)**, the book's free companion scanner.

- **Code samples are now CC BY-SA 4.0 or MIT-0, at your choice.** Every code block written for the book
  can be pasted into any app, including closed-source ones, with no attribution or ShareAlike duty. The
  prose, and the OWASP text reproduced in Part 9, stay CC BY-SA 4.0. See `LICENSE`.

## 2026-10-20 — cheat sheet

- **Added [`CHEATSHEET.md`](CHEATSHEET.md)** and a printable `dist/Mobile-Security-Cheat-Sheet.pdf`: a
  20-minute review before an interview or design review. Key terms in one line each, every topic in a few
  lines, 31 top questions with short answers, myths versus facts, numbers worth remembering, and a
  five-step way to answer any design question. `scripts/check.py` checks its section references.
- **Part 10:** removed "a user can't spoof it casually" from the impossible-travel answer, matching §12.5.
- **Build:** `scripts/build.py` now renders the cheat-sheet PDF too, and both PDFs use US English
  hyphenation (`region=US`), matching the American house style.

## 2026-10-20 — editorial and currency pass

- **Every line re-edited** in the Google and Microsoft developer-documentation voice: second person,
  active voice, present tense, contractions, and no filler. Terms that a reader new to security would
  hit undefined now get a plain definition where they first appear.
- **House style moved to American spelling** in prose and headings, and prose lists take the serial comma. File names
  are unchanged, and internal links to renamed headings were updated; external deep links to an old
  heading anchor need updating. `CONTRIBUTING.md` records the new rules.
- **Every claim re-checked** against primary sources: about 1,590 claims and identifiers plus all 278
  source links, with 140 corrections. The largest: §5.5's attestation verifier now uses the app-identity
  check that `android/keyattestation` restored in September 2026 (v0.3 and later); `datastore-tink` is a release candidate; bcrypt is
  legacy-only; workflow lockfiles and the floating-tag-only `actions/checkout` backport are covered.
- **Glossary** grew from 210 to 252 terms, and **Sources** from 278 to 284 entries. The OWASP Top 10 for
  LLM Applications 2026 is now cited from its public text.
- **Independent verification of the pass:** six reviewers re-read every edit against the original and
  re-checked every correction. They found 1 critical error introduced by the pass (a MASWE beta-mapping
  count, now reverted to the original, correct text), 15 major and 61 minor problems. All are fixed except
  one major finding that proved wrong: Google documents both Play Console paths the book gives.
- **A second, cold verification round** on the final text found no critical, 8 major and 60 minor problems,
  all fixed except two style points left to the author. The largest: the CBC encrypt-then-MAC advice now
  covers the IV with a separate key, and Part 11's pin-rotation steps no longer cause an outage.
- **Compiled and ran** §5.5's attestation verifier and §10.7's App Attest verifiers on the JVM. Each had
  the same bug, now fixed: a malformed signature threw instead of returning `false`.
- **The review prompt** is in `editorial/PROMPT.md`, with one report per file in `editorial/reports/`.

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
