# book/start-here.md

## Summary
- Words before / after: 1694 / 1948 (`wc -w`, including frontmatter, Mermaid and tables)
- Edits: clarity 9, filler 5, voice 7, spelling 9, explanation 14, code 0
- Facts checked: 16 · correct 14 · corrected 2 · unverified 0 (plus 1 claim newly marked *(reasoned)* and 1 newly marked *(estimate)*)

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| On dates | "with iOS 26 and Android 15–16 still on most devices" | "iOS 26 still runs on most iPhones. Android devices are spread across many versions, with Android 15 and 16 the most common *(reported)*." Android 15 + 16 together are well under half of active devices: Google's last official figures (data from 1 Dec 2025) give 19.3% and 7.5%. Third-party trackers (StatCounter, AppBrain) put Android 16 first in mid-2026 at about 24%, with Android 15 second, which is why the claim carries *(reported)*. | Apple App Store adoption page (iOS 26 on 79% of all iPhones, 7 June 2026): https://developer.apple.com/support/app-store/ ; Google distribution, reported: https://9to5google.com/2026/01/30/android-16-is-on-7-5-of-devices-in-latest-distribution-numbers-update/ , https://commandlinux.com/statistics/android-version-distribution/ | 2026-10-20 |
| How to read / On the code | "Most control chapters end with a 'How to implement it' section" (also Figure 1 node "ends with 'How to implement it'") | "Many control chapters…" / "often ends with…". Only 9 chapters have a "How to implement it" section (§5.5, §6.6, §8.10, §9.6, §10.7, §11.6, §16.8, §17.8, §19.8); three more use "…, in code" (§14.4, §14.5, §15.8). Several control chapters (4, 7, 12, 18, 20, 21) have neither. | Book itself (heading grep) | 2026-10-20 |

Also corrected: "the glossary points you back to Part 0" → "points you to the section that teaches it". Glossary entries cite the teaching section, which is often outside Part 0. And Part 10 "About 160 questions … plus design-review scenarios" → "including design-review scenarios": the 156 `**Q:**` entries include the scenarios.

Verified correct (no change): Android 17 released 16 June 2026 (https://developer.android.com/blog/posts/android-17-is-here); iOS 27 released 14 September 2026 (https://www.apple.com/newsroom/2026/09/major-updates-for-apples-software-platforms-are-now-available/); MASVS v2.1.0 is the latest (GitHub OWASP/masvs releases, 18 Jan 2024), with 24 controls (mas.owasp.org/MASVS); MASWE v1.0.0 (17 Aug 2026, https://mas.owasp.org/news/2026/08/17/maswe-v100-release/), with 78 weaknesses (mas.owasp.org/MASWE); MASTG v2.0.0 (GitHub OWASP/mastg, 30 Jun 2026); the OWASP MASTG app list URL is live and lists deliberately vulnerable apps (AndroGoat, DIVA, DVIA-v2, iGoat-Swift …); GitHub renders Mermaid in Markdown files (docs.github.com "Creating diagrams"); OWASP = Open Worldwide Application Security Project, a 501(c)(3) nonprofit (owasp.org/about); `biometryCurrentSet` = currently enrolled biometrics only (Apple docs); GCM authenticates and CBC doesn't; the part table's chapter ranges match the part files; Mermaid link is live; the glossary anchor resolves (check.py).

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| — | None left unmarked. "Most real findings live here" (Part 7 row) has no source; I marked it *(reasoned)*. "About a week of evenings" is now *(estimate)*. | — | — |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Start here | `strings` undefined | What it does, plus a pointer to Chapter 1's Try it |
| Start here | Why "a device you don't control" matters | Whoever controls it can read files, decompile code, and change how it runs |
| Start here | "pinning bypass" undefined | Defined certificate pinning; restated the bypass in plain words |
| What you'll learn | hardware-backed key, StrongBox | One-sentence definitions |
| What you'll learn | static/dynamic/hybrid pinning | Glosses consistent with the glossary entry (§8.6) |
| What you'll learn | device attestation, "hookable function" | Plain definitions |
| What you'll learn | threat-model, "agentic tooling" | Defined threat modeling; replaced the jargon with "AI agents that take actions on the user's behalf" |
| What you'll learn | OWASP | Expanded name and what it is |
| Part table | MAS, CI, IPC, MASVS/MASWE/MASTG | Expansions or one-phrase roles; labeled Play Integrity (Android) and App Attest (iOS) |
| Conventions | trust boundary | Definition |
| On the code | CBC/GCM, biometryAny/biometryCurrentSet | What separates each pair |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| CONTRIBUTING.md | Style | Says "British spelling in prose", but editorial/PROMPT.md requires American | The house rules conflict. I followed PROMPT.md. |
| 09-the-catalogues.md, 11-making-the-case-and-running-the-programme.md | Part headings | "The catalogues", "programme" are British, but they are headings and file names | I kept "The catalogues" in the Figure 1 node and the part-table link text, so they still match the Part 9 heading. Coordinator's call. |
| 12-verification.md | Glossary | Consider adding "Trust boundary" and "Hardware-backed key" if they are missing | Both are now defined in start-here |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Trust boundary | The point where data crosses from code you control to code you don't | Start here (A few conventions) |
| Hardware-backed key | A key that stays inside a secure chip and never reaches your app's memory | Start here (What you'll learn); taught in Chapter 4 |

## Judgment calls
- I kept part titles with British spelling ("The catalogues") wherever they name the part, because they mirror headings that are link targets.
- "Most real findings live here" became "Most real assessment findings come from these surfaces *(reasoned)*". Part 7's intro makes the same claim unmarked.
- "Try Part 10 cold" became "Answer the questions … before you reread anything". "Cold" is an idiom.
- "Expected outputs are described, never fabricated" became "Each block describes the expected output rather than inventing one". Same meaning, active voice.
- "the single most useful thing you can report back" became "the most useful correction you can send me". It names who receives the report.
- The edition line (Edition 1 · September 2026) and the "reflects the state of things in September 2026" sentence are unchanged. Every fact in that sentence still holds on 2026-10-20. `last_verified` is set to 2026-10-20. `recheck_because` is unchanged.
- I didn't recount the part table or word counts. The coordinator refreshes them.
