<img width="736" alt="Mobile Application Security — A Study Book for Engineers" src="assets/preview.jpeg" />

# Mobile Application Security — A Study Book for Engineers

A practical, verified reference on securing Android, iOS, and Kotlin Multiplatform apps. It's written for study, not skimming: every mechanism comes with *why it works*, so you can reason about cases the book doesn't cover.

**No security background needed.** Begin with [Start here](book/start-here.md), then read Part 0 for the foundations: cryptography, authentication, and what the platforms protect for free. The book defines every term where it first appears, and the [glossary](book/12-verification.md#glossary) has 252 of them.

**Current to October 2026:** Android 17, iOS 27, and the three OWASP Mobile Application Security (MAS) projects: MASVS v2.1.0 (the security requirements), MASWE v1.0.0 (the weaknesses), and MASTG v2.0.0 (the testing guide).

---

## Read it

| Part | What it covers | Words |
|---|---|---|
| [Start here](book/start-here.md) | What you'll learn, how to read the book, and its conventions and confidence markers | 1,900 |
| [0 — Foundations](book/00-foundations.md) | Vocabulary, reading OWASP IDs, the cryptography you need, OAuth and PKCE on mobile, platform guarantees, threat modeling, and asset classification | 10,300 |
| [1 — Understanding the threat](book/01-understanding-the-threat.md) | What an attacker can do, who attacks you and which controls work against whom, the economics, and how the OWASP MAS standard fits together | 5,200 |
| [2 — Data at rest](book/02-data-at-rest.md) | Keystore and Keychain internals, key attestation with server-side verification, choosing storage after `EncryptedSharedPreferences`, the leaks that aren't about encryption, and database encryption | 11,900 |
| [3 — Data in transit](book/03-data-in-transit.md) | TLS and what's changing (Certificate Transparency, Encrypted Client Hello, and 47-day certificates), the certificate pinning debate, static versus dynamic pinning, tested implementations, and troubleshooting | 12,100 |
| [4 — Proving who is calling](book/04-proving-who-is-calling.md) | Play Integrity, App Attest (client and server), biometrics that a hooking tool can't bypass, passkeys, the backend as arbiter, and DPoP (proof-of-possession tokens) | 12,600 |
| [5 — Resilience](book/05-resilience.md) | How reverse engineering works, obfuscation and tamper detection, and detection code that reports instead of blocking | 5,100 |
| [6 — The build and release pipeline](book/06-the-build-and-release-pipeline.md) | Why continuous integration (CI) is now the target (tj-actions, TanStack, and more), secrets, workflow hardening, build provenance, signing keys, and build configuration | 6,800 |
| [7 — Platform surfaces](book/07-platform-surfaces-and-new-frontiers.md) | WebViews, inter-process communication (IPC) and deep links, permissions and privacy, input validation, AI features (OWASP Top 10 for LLM Applications 2026), and Kotlin Multiplatform | 15,100 |
| [8 — Practice](book/08-practice.md) | Build a test lab, run an assessment, write a finding scored with CVSS v4.0, handle an incident, and work from a one-page checklist | 6,900 |
| [9 — The catalogs](book/09-the-catalogues.md) | All 24 MASVS controls verbatim, all 78 MASWE weaknesses, the MASTG tests worth knowing, and platform security defaults by version | 5,800 |
| [10 — Questions and answers](book/10-questions-and-answers.md) | 156 questions tagged by difficulty, plus design-review scenarios. Use them to test yourself | 18,700 |
| [11 — Making the case](book/11-making-the-case-and-running-the-programme.md) | Executive summary, business case, regulation (CRA, DORA, NIS2, the AI Act, and PCI DSS), a phased plan, owners, and testable success criteria. **Written to stand alone** | 9,600 |
| [12 — Verification](book/12-verification.md) | What was checked and when, every correction, what remains uncertain, 284 sources, and a 252-term glossary | 20,300 |

The whole book also comes as a [single Markdown file](dist/Mobile-Application-Security-single-file.md) and a [PDF](dist/Mobile-Application-Security.pdf). `scripts/build.py` builds both from `book/`.

---

## Reading orders

- **New to security engineering?** Read [Start here](book/start-here.md), then Parts 0 through 3 in order, because each builds on the one before. Do each chapter's **Try it**.
- **Deciding whether to fund this work?** Read [Part 11](book/11-making-the-case-and-running-the-programme.md) on its own. Its first page is an executive summary.
- **Implementing one control?** Go straight to its chapter, which stands alone. Many control chapters end with a "How to implement it" section that has code for both platforms and a **Verify it** test.
- **Preparing for an interview or a design review?** Work through [Part 10](book/10-questions-and-answers.md), starting with the design-review scenarios. Then reread the chapters behind any answer you weren't sure of.
- **Auditing an app?** Read [Part 8](book/08-practice.md), then use the catalogs in [Part 9](book/09-the-catalogues.md).

---

## Before you trust it

| | |
|---|---|
| **Claims are marked** | Any claim weaker than a primary source carries *(reported)*, *(estimate)*, *(reasoned)*, *(contested)*, or *(illustrative)* inline. An unmarked claim traces to a standards body, vendor documentation, or an official report |
| **Verify it blocks are mostly a test plan** | Each implementation section ends with a **Verify it** block. Most describe documented tool behavior and MASTG procedures and haven't been run. Where one was run, on an emulator or simulator, the chapter says so |
| **Two claims are untested; four have emulator or simulator evidence only** | [VERIFICATION.md](VERIFICATION.md) lists all six. None has been tested on a real phone yet, so your device result would be original research |
| **Errors are recorded, not hidden** | [Part 12](book/12-verification.md) lists every correction, including the ones found late: a deprecated API cited as current, an iOS pinning helper that hashed the wrong bytes, and an earlier "correction" that was itself wrong |
| **Each file says when it was checked** | Every part file carries `last_verified` and `volatility` in its frontmatter |

Full detail: [VERIFICATION.md](VERIFICATION.md).

---

## What makes this different

**It argues both sides where the industry disagrees.** Certificate pinning is the clearest example. Pinning means your app accepts only specific certificates or public keys for a server, not any certificate the device trusts. `MASVS-NETWORK-2` asks for identity pinning of endpoints you control, while OWASP's own [Pinning Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Pinning_Cheat_Sheet.html) says most apps should probably never pin. Both come from OWASP, and both are current. [Chapter 8](book/03-data-in-transit.md) gives you both arguments and the question that decides it.

**It marks its own confidence.** Every claim that rests on less than a primary source carries a marker, and the untested claims are listed with what it would take to test them.

**It records its own errors.** [Part 12](book/12-verification.md) is the book's audit log. When an entry turns out to be wrong, it stays in the log, annotated as superseded.

**It is checked mechanically.** `scripts/check.py` verifies that every `§` and chapter reference resolves, every diagram carries a numbered caption, every code fence is tagged, Swift parses, and XML is well formed. If you run it locally with actionlint installed, it also lints the workflow YAML; with Node installed and `--mermaid`, it renders every Mermaid diagram. CI runs the reference, caption, fence, Swift, and XML checks on every pull request and every push to `main`. It fails if the single-file Markdown edition in `dist/` is out of date.

---

## Corrections welcome, and the most useful ones

Use one of three issue templates, listed from most to least valuable:

1. **[Empirical result](.github/ISSUE_TEMPLATE/empirical-result.md)**: you tested one of the six claims that lack hardware evidence on a real phone. This is the most valuable contribution you can make. The result goes into the chapter with credit.
2. **[Deprecated API cited as current](.github/ISSUE_TEMPLATE/deprecated-api.md)**: MASTG v2.0.0 deprecated every v1 test in June 2026, and MASWE v1.0.0 renumbered every weakness in August 2026, so old IDs still turn up.
3. **[Stale figure](.github/ISSUE_TEMPLATE/stale-figure.md)**: each annual report replaces the last, and standards timelines move forward.

The items that change fastest are the certificate lifetime schedule, Play Integrity verdict behavior, App Attest signals after each WWDC, GitHub Actions security defaults, and MASTG releases. If you send a fix, follow [CONTRIBUTING.md](CONTRIBUTING.md) to build and check the book, and add a line to Part 12 with the date and what changed.

---

## License and attribution

This work is licensed under [Creative Commons Attribution-ShareAlike 4.0](LICENSE).

**Portions adapted from OWASP material**, which is itself licensed CC BY-SA 4.0:

- [OWASP MASVS](https://mas.owasp.org/MASVS/): the 24 control statements and category structure reproduced in Part 9
- [OWASP MASWE](https://mas.owasp.org/MASWE/): the 78 weakness identifiers and titles reproduced in Part 9
- [OWASP MASTG](https://mas.owasp.org/): test, technique, and best-practice identifiers cited throughout

OWASP doesn't certify applications and doesn't endorse this book. The book cites and links platform documentation from Google and Apple but never reproduces it at length.
