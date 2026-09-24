<img width="736" alt="Mobile Application Security — A Study Book for Engineers" src="assets/preview.jpeg" />

# Mobile Application Security — A Study Book for Engineers

A practical, verified reference on securing Android, iOS and Kotlin Multiplatform apps. Written to be studied from, not skimmed: every mechanism is explained at the level of *why it works*, so you can reason about cases this book does not cover.

**No security background needed.** [Start here](book/start-here.md), then Part 0 covers the foundations: cryptography, authentication, what the platforms protect for free. Every term is defined where it first appears, and the [glossary](book/12-verification.md#glossary) has 210 of them.

**Current to September 2026:** Android 17, iOS 27, MASVS v2.1.0, MASWE v1.0.0, MASTG v2.0.0.

---

## Read it

| Part | What it covers | Words |
|---|---|---|
| [Start here](book/start-here.md) | What you'll learn, how to read the book, conventions and confidence markers | 1,700 |
| [0 — Foundations](book/00-foundations.md) | Vocabulary, reading OWASP IDs, the cryptography you actually need, OAuth and PKCE on mobile, platform guarantees, threat modelling, asset classification | 9,300 |
| [1 — Understanding the threat](book/01-understanding-the-threat.md) | What an attacker can really do, who attacks you and which controls work against whom, the economics, how the OWASP MAS standard fits together | 4,700 |
| [2 — Data at rest](book/02-data-at-rest.md) | Keystore and Keychain internals, key attestation with server-side verification, choosing storage after EncryptedSharedPreferences, the leaks that aren't about encryption, database encryption | 11,400 |
| [3 — Data in transit](book/03-data-in-transit.md) | TLS and what's changing (CT, ECH, 47-day certificates), the certificate pinning debate, static vs dynamic pinning, tested implementations, troubleshooting | 11,800 |
| [4 — Proving who is calling](book/04-proving-who-is-calling.md) | Play Integrity, App Attest (client and server), biometrics that can't be hooked away, passkeys, the backend as arbiter, DPoP | 12,200 |
| [5 — Resilience](book/05-resilience.md) | How reverse engineering actually works, obfuscation and tamper detection, detection code that reports rather than blocks | 4,900 |
| [6 — The build and release pipeline](book/06-the-build-and-release-pipeline.md) | Why CI is now the target (tj-actions, TanStack and more), secrets, workflow hardening, provenance, signing keys, build configuration | 6,000 |
| [7 — Platform surfaces](book/07-platform-surfaces-and-new-frontiers.md) | WebViews, IPC and deep links, permissions and privacy, input validation, AI features (OWASP LLM Top 10 2026), Kotlin Multiplatform | 14,900 |
| [8 — Practice](book/08-practice.md) | Build a test lab, run an assessment, write a finding with CVSS v4.0, handle an incident, a one-page checklist | 6,600 |
| [9 — The catalogues](book/09-the-catalogues.md) | All 24 MASVS controls verbatim, all 78 MASWE weaknesses, the MASTG tests worth knowing, platform security defaults by version | 5,600 |
| [10 — Questions and answers](book/10-questions-and-answers.md) | 156 questions tagged by difficulty, plus design-review scenarios. Use these to check yourself | 18,000 |
| [11 — Making the case](book/11-making-the-case-and-running-the-programme.md) | Executive summary, business case, regulation (CRA, DORA, NIS2, AI Act, PCI DSS), phased plan, owners, testable success criteria. **Written to stand alone** | 8,400 |
| [12 — Verification](book/12-verification.md) | What was checked, when, every correction made, what remains uncertain, 278 sources, 210-term glossary | 18,400 |

The whole book is also available as a [single Markdown file](dist/Mobile-Application-Security-single-file.md) and a [PDF](dist/Mobile-Application-Security.pdf), both built from `book/` by `scripts/build.py`.

---

## Reading orders

- **New to the engineering side?** [Start here](book/start-here.md), then Parts 0 through 3, in order. They build on each other. Do each chapter's **Try it**.
- **Deciding whether to fund this work?** Read [Part 11](book/11-making-the-case-and-running-the-programme.md) on its own. Its first page is an executive summary.
- **Implementing one control?** Its chapter stands alone. Most control chapters end with a "How to implement it" section with code for both platforms and a **Verify it** test.
- **Preparing for an interview or a design review?** [Part 10](book/10-questions-and-answers.md), starting with the design-review scenarios, then go back to whichever answers were shaky.
- **Auditing an app?** [Part 8](book/08-practice.md), then the catalogues in [Part 9](book/09-the-catalogues.md).

---

## Before you trust it

| | |
|---|---|
| **Claims are marked** | Anything weaker than a primary source carries *(reported)*, *(estimate)*, *(reasoned)*, *(contested)* or *(illustrative)* inline. Unmarked means it traces to a standards body, vendor documentation or an official report |
| **Verify it blocks are mostly a test plan** | Each implementation section ends with a **Verify it** block. Most were written from documented tool behaviour and MASTG procedures, not executed. Where one was run, on an emulator or simulator, the chapter says so |
| **Two claims are untested; four have emulator or simulator evidence only** | Listed in [VERIFICATION.md](VERIFICATION.md). None has been run on real hardware, so a device result is original research |
| **Errors are recorded, not hidden** | [Part 12](book/12-verification.md) lists every correction, including the ones found late: a deprecated API cited as current, an iOS pinning helper that hashed the wrong bytes, and an earlier "correction" that was itself wrong |
| **Each file says when it was checked** | `last_verified` and `volatility` in the frontmatter of every part file |

Full detail: [VERIFICATION.md](VERIFICATION.md).

---

## What makes this different

**It argues both sides where the industry disagrees.** Certificate pinning is the clearest example: `MASVS-NETWORK-2` asks for identity pinning of endpoints you control, while OWASP's own Pinning Cheat Sheet says most apps should probably never pin. Both are OWASP, both are current. The book gives you both arguments and the question that actually decides it.

**It marks its own confidence.** Claims weaker than they look carry a marker, and the untested ones are listed with what it would take to test them.

**It records its own errors.** [Part 12](book/12-verification.md) is the book's audit log. When an entry turned out to be wrong, it is annotated as superseded rather than deleted.

**It is checked mechanically.** `scripts/check.py` verifies that every `§` and chapter reference resolves, every diagram carries a numbered caption, every code fence is tagged, Swift parses and XML is well formed. Run locally with actionlint and Node installed, it also lints the workflow YAML and renders every Mermaid diagram (`--mermaid`). CI runs the reference, caption, fence, Swift and XML checks on every pull request and every push to `main`, and fails if `dist/` is out of date.

---

## Corrections welcome, and the most useful ones

Three issue templates, in descending order of value:

1. **[Empirical result](.github/ISSUE_TEMPLATE/empirical-result.md)**: you tested one of the six claims with no hardware evidence on a real phone. This is the most valuable contribution possible here; the result goes into the chapter with credit.
2. **[Deprecated API cited as current](.github/ISSUE_TEMPLATE/deprecated-api.md)**: MASTG v2.0.0 deprecated every v1 test in June 2026, and MASWE v1.0.0 renumbered every weakness in August 2026. Old IDs linger.
3. **[Stale figure](.github/ISSUE_TEMPLATE/stale-figure.md)**: annual reports supersede each other and standards schedules step forward.

The fast-moving items are the certificate lifetime schedule, Play Integrity verdict behaviour, App Attest signals after each WWDC, GitHub Actions security defaults, and MASTG releases. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to build and check the book, and add a line to Part 12 with the date and what changed.

---

## Licence and attribution

This work is licensed under [Creative Commons Attribution-ShareAlike 4.0](LICENSE).

**Portions adapted from OWASP material**, which is itself licensed CC BY-SA 4.0:

- [OWASP MASVS](https://mas.owasp.org/MASVS/): the 24 control statements and category structure reproduced in Part 9
- [OWASP MASWE](https://mas.owasp.org/MASWE/): the 78 weakness identifiers and titles reproduced in Part 9
- [OWASP MASTG](https://mas.owasp.org/): test, technique and best-practice identifiers cited throughout

OWASP does not certify applications and does not endorse this book. Platform documentation from Google and Apple is cited and linked, never reproduced at length.
