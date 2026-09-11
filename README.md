<img width="736" alt="Mobile Application Security — A Study Book for Engineers" src="assets/preview-25.png" />

# Mobile Application Security — A Study Book for Engineers

A practical, verified reference on securing Android, iOS and Kotlin Multiplatform apps. Written to be studied from, not skimmed: every mechanism is explained at the level of *why it works*, so you can reason about cases this book does not cover.

**No security background needed.** Part 0 covers the foundations — cryptography, authentication, what the platforms protect for free. Every term is defined where it first appears, and there is a glossary.

---

## Read it

| Part | What it covers | Words |
|---|---|---|
| [0 — Foundations](book/00-foundations.md) | Vocabulary, cryptography you actually need, authentication and OAuth on mobile, platform guarantees, threat modelling, asset classification | 4,200 |
| [1 — Understanding the threat](book/01-understanding-the-threat.md) | What an attacker can really do, the economics, and how the OWASP standard fits together | 2,200 |
| [2 — Data at rest](book/02-data-at-rest.md) | Keystore and Keychain internals, key attestation, choosing storage, database encryption | 3,800 |
| [3 — Data in transit](book/03-data-in-transit.md) | TLS, the certificate pinning debate, static vs dynamic pinning, implementation and troubleshooting | 7,300 |
| [4 — Proving who is calling](book/04-proving-who-is-calling.md) | Play Integrity, App Attest, biometrics, the backend as the only real arbiter | 4,700 |
| [5 — Resilience](book/05-resilience.md) | How reverse engineering actually works, obfuscation and tamper detection, detection code | 2,600 |
| [6 — The build and release pipeline](book/06-the-build-and-release-pipeline.md) | Why CI is now the target, secrets, workflow hardening, signing keys, build configuration | 2,400 |
| [7 — Platform surfaces](book/07-platform-surfaces-and-new-frontiers.md) | WebViews, IPC and deep links, permissions and privacy, input validation, AI features, KMP | 6,100 |
| [8 — Practice](book/08-practice.md) | Build a test lab, run an assessment, write it up, handle an incident | 3,300 |
| [9 — The catalogues](book/09-the-catalogues.md) | All 24 MASVS controls, all 78 MASWE weaknesses, the MASTG tests and techniques | 2,100 |
| [10 — Questions and answers](book/10-questions-and-answers.md) | ~100 questions with written-out answers. Use these to check yourself | 4,700 |
| [11 — Making the case](book/11-making-the-case-and-running-the-programme.md) | Business case, regulatory position, phased plan, owners, success criteria. **Written to stand alone** | 3,800 |
| [12 — Verification](book/12-verification.md) | What was checked, when, corrections made, and what remains genuinely uncertain | 6,600 |

A single-file PDF is also available in [`dist/`](dist/).

---

## Reading orders

- **Deciding whether to fund this work?** Read [Part 11](book/11-making-the-case-and-running-the-programme.md) on its own. It needs nothing else.
- **New to the engineering side?** Parts 0 through 3, in order. They build on each other.
- **Implementing one control?** Its chapter stands alone. Each control chapter ends with a "How to implement it" section with code for both platforms.
- **Preparing for an interview?** [Part 10](book/10-questions-and-answers.md), then go back to whichever answers were shaky.
- **Auditing an app?** [Part 8](book/08-practice.md), then the catalogues in [Part 9](book/09-the-catalogues.md).

---

## Before you trust it

| | |
|---|---|
| **Claims are marked** | Anything weaker than a primary source carries *(reported)*, *(estimate)*, *(reasoned)* or *(contested)* inline. Unmarked means it traces to a standards body, vendor documentation or an official report |
| **Verification steps are a test plan, not a transcript** | Each implementation section ends with a **Verify it** block. These were written from documented tool behaviour and MASTG procedures, **not executed against a live app** while writing |
| **Six claims are untested** | Listed in [VERIFICATION.md](VERIFICATION.md). Three of them have almost no published evidence either way — settling one is original research |
| **Errors are recorded, not hidden** | [Part 12](book/12-verification.md) lists every correction made during writing, including a deprecated API cited as current and 56 section numbers attached to the wrong chapters |
| **Each file says when it was checked** | `last_verified` and `volatility` in the frontmatter of every part file |

Full detail: [VERIFICATION.md](VERIFICATION.md).

---

## What makes this different

**It argues both sides where the industry disagrees.** Certificate pinning is the clearest example: OWASP's own Pinning Cheat Sheet says most apps should probably never pin, while the MASTG recommends it for apps handling financial or health data. Both are OWASP, both are current. The book gives you both arguments and the question that actually decides it.

**It marks its own confidence.** Claims weaker than they look carry a marker: *(reported)* for vendor or practitioner figures, *(estimate)* for planning numbers, *(reasoned)* for conclusions drawn by analogy rather than quoted from a standard, *(contested)* where the industry disagrees. Unmarked claims trace to a primary source.

**It records its own errors.** [Part 12](book/12-verification.md) lists every correction made during writing, including the ones found late — a deprecated API cited as current, arithmetic derived two contradictory ways, 56 section numbers attached to the wrong chapters. It also states what the verification did *not* cover.

---

## Corrections welcome — and the most useful ones

Three issue templates, in descending order of value:

1. **[Empirical result](.github/ISSUE_TEMPLATE/empirical-result.md)** — you tested one of the six untested claims on a real device. This is the most valuable contribution possible here; the result goes into the chapter with credit.
2. **[Deprecated API cited as current](.github/ISSUE_TEMPLATE/deprecated-api.md)** — a previous revision cited `MASTG-TEST-0044` as current when it was already deprecated. There are almost certainly others.
3. **[Stale figure](.github/ISSUE_TEMPLATE/stale-figure.md)** — annual reports supersede each other and standards schedules step forward.

Found something else stale or wrong? Open an issue or a pull request. The fast-moving items are the certificate lifetime schedule, Play Integrity verdict behaviour, App Attest signals after each WWDC, and MASTG release notes. If you fix something, add a line to Part 12 with the date and what changed — that is what keeps a document like this worth reading.

---

## Licence and attribution

This work is licensed under [Creative Commons Attribution-ShareAlike 4.0](LICENSE).

**Portions adapted from OWASP material**, which is itself licensed CC BY-SA 4.0:

- [OWASP MASVS](https://mas.owasp.org/MASVS/) — the 24 control identifiers and category structure reproduced in Part 9
- [OWASP MASWE](https://mas.owasp.org/MASWE/) — the 78 weakness identifiers and titles reproduced in Part 9
- [OWASP MASTG](https://mas.owasp.org/) — test, technique and best-practice identifiers cited throughout

OWASP does not certify applications and does not endorse this book. Platform documentation from Google and Apple is cited and linked, never reproduced at length.

---
