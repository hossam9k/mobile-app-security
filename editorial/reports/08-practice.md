# book/08-practice.md

## Summary
- Words before / after: 6,604 / 6,988 (growth is definitions and the "why" sentences listed below)
- Edits: clarity 38, filler 14, voice 9, spelling 14, explanation 17, code 0
- Facts checked: 62 · correct 57 · corrected 4 · unverified 1

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| 22.1 | "Since Android 7 (2016), apps do **not** trust user-added CAs by default." | "Since Android 7 (2016), apps that target API level 24 or higher do **not** trust user-added CAs by default." The default depends on targetSdk, not on the OS version. | https://developer.android.com/privacy-and-security/security-config | 2026-10-20 |
| 23.6 | "Fifty-two weeks of that and you have covered the catalogue" | "After a year of that you've covered most of the catalog (it has 78 entries, and some won't apply to your app)". One weakness a week for 52 weeks can't cover 78 entries. | https://mas.owasp.org/MASWE/ (78 entries counted) | 2026-10-20 |
| 24.2 | "GDPR requires breach notification within 72 hours." | Now names the scope and recipient: if you process EU residents' personal data, Article 33 requires you to notify the supervisory authority within 72 hours of becoming aware of the breach, where feasible. Also notes that other jurisdictions set their own deadlines. | https://gdpr-info.eu/art-33-gdpr/ (Regulation (EU) 2016/679 Art. 33(1)) | 2026-10-20 |
| 24.4 | "On Android 7–12 … Google Play Protect checks that updates carry your latest classical key." | Added "unless the user has turned Play Protect off", the condition Google states. | https://support.google.com/googleplay/android-developer/answer/9842756 | 2026-10-20 |

Precision fixes that are not errors: the "As of" date in §22.1 moved from September to October 2026 after I re-checked the jailbreak table. The Android 14 CA-injection description (§22.1 Trap) now matches HTTP Toolkit's write-up: a writable copy is bind-mounted over the APEX path in the Zygote's and apps' namespaces, and the injection lasts until reboot. The earlier text said the copy was mounted "over the app's certificate directory". The Frida 17 note now says scripts are compiled "with `frida-compile` or the API's built-in compiler", because the Python docs use `frida.Compiler`.

### Verified correct (no change)
- Google Play emulator images can't be rooted; the release-key quote matches developer.android.com/studio/run/managing-avds. I shortened the quote to stay under 15 words.
- Genymotion: Android ≤11 images rooted by default; Android 12+ needs the root toggle, and those images need a paid license (Genymotion help article and release notes).
- Cellebrite completed the Corellium acquisition on 2 December 2025.
- palera1n: A8–A11 and T2, iOS 15+; A11 requires the passcode disabled, plus a reset on iOS 16 (GitHub README).
- Dopamine 3.x support ranges match the repo description exactly. Latest release is 3.0.12 (2026-10-20), with no range change.
- No public jailbreak for current flagships on iOS 26.x/27. iOS 27 shipped in September 2026.
- MASTG-TECH-0090 (Injecting Frida Gadget into an IPA Automatically) and MASTG-TECH-0146 (Dynamic Analysis on Non-Jailbroken Devices).
- Frida 17.0.0 released 17 May 2025; bridges moved out of GumJS; the REPL and frida-trace bundle them (frida.re release post and bridges docs). Current Frida is 17.24.3.
- objection 1.12.x (1.12.5 current): `-n … start`; `-g` and `explore` are deprecated with warnings (objection `cli.py` source).
- Burp Community is free; semgrep is used in MASTG demos.
- `debug-overrides` sets `overridePins` to true by default (Android docs).
- Android 14 APEX path `/apex/com.android.conscrypt/cacerts`, read-only with private mount propagation; `nsenter` workaround (HTTP Toolkit blog).
- MAS Test Apps repos are live with `MastgTest.kt`/`MastgTest.swift`. MAS Crackmes: Android L1–L4, iOS L1–L2. iGoat-Swift, DIVA, and InsecureBankv2 links are live. DIVA's last commit was 2016-01-15; InsecureBankv2's was 2019-11-21. mas.owasp.org/MASTG/apps/ is live.
- MASTG-DEMO-0106 is the Cipher.doFinal Frida hook and demonstrates MASTG-TEST-0341.
- MAS profiles L1, L2, R, and P and their attacker models (mas.owasp.org/Profiles/). The "Modes of Introduction" guidance for weaknesses that have no test (MASWE index page). MASWE has 78 entries.
- Test URL pattern resolves (MASTG-TEST-0207).
- MASWE-0001 title; MASWE-0043 (Enforced Updating Not Implemented, mapped to MASVS-CODE-2); MASTG-TEST-0207 and -0287 titles; MASTG-BEST-0050. None of these is deprecated.
- CVSS v4.0 was published November 2023 and is still current, with no v4.1 or v5 on first.org/cvss. The AV, AT, and PR definitions match the spec. The User Guide section is titled "CVSS Base (CVSS-B) Measures Severity, not Risk", and the guide tells you to add Threat and Environmental metrics.
- **CVSS scores recomputed** with the `cvss` Python library (FIRST v4.0 algorithm):
  - `AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` = 5.1 ✔
  - `AV:P/AC:L/AT:P/…/SC:H/SI:H/SA:N` = 5.8 Medium ✔
  - the same vector with `AV:L` = 7.0 High ✔
  - I added the PR:H variant (`AV:L/AT:N/PR:H`) = 8.2
- Android 17 is API 37 and released June 2026, so the worked example's "Android 17 AOSP emulator image" is plausible.
- Firebase real-time Remote Config: the listener fetches automatically, and you activate in the callback; it stops listening in the background. The default minimum fetch interval is 12 hours.
- App Store phased release: 7 days (1/2/5/10/20/50/100%), pause up to 30 days total, manual updates available to anyone at any time, "Release to All Users".
- Play Console path **Protected with Play → Play Store protection → Manage Play app signing**. Key upgrades are annual. The hybrid key is RSA-4096 + ML-DSA-65 under v3.2 on Android 17+; v3.1 enforces the classical key on Android 13–16. Apps with hybrid signing get two new fingerprints.
- Apple: revoking a distribution certificate doesn't affect live App Store apps while membership is valid; uploaded but unsubmitted builds may be marked Invalid Binary; revoking an in-house certificate stops those apps running (developer.apple.com/support/certificates/).

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| 22.1 | Genymotion: "root on Android 12+ is paid" | Genymotion release notes say Android 12 images need a paying license, and Desktop 3.8.0 added dynamic root for 12+. The current user manual page on root returned 404, so I couldn't confirm the current licensing terms directly. | None needed if Genymotion's licensing is unchanged; otherwise *(reported)* |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| 22.1 | Why iOS jailbreaks are limited to old devices | Jailbreaks depend on exploits Apple patches; only a bootrom flaw survives updates, and the text says what a bootrom is |
| 22.1 | Why rooting skews detection testing | Root is the condition the checks look for, so a rooted device shows whether detection fires, not normal-device behavior |
| 22.1 | AOSP, adb, Magisk, Mainline APEX, Zygote undefined | One-phrase definitions at first use |
| 22.1 | Order of operations on Android 13 vs 14 for option 2 | Option 2 now says it works on Android 13 and earlier and points to the trap |
| 22.1 | Why private mount propagation defeats a simple overlay | A mount made from `adb shell` never reaches app processes; the workaround lasts only until reboot |
| 22.3 | What `strings` does; why release, not debug | Definition, plus "the release build is what an attacker downloads"; examples of sensitive strings |
| 22.3 | What `Cipher.doFinal` is | "the Java call that performs encryption or decryption"; you see data before it is encrypted |
| 22.4 | Which apps ignore the proxy; where to look | Flutter as an example; check `logcat` for TLS errors |
| 22.4 | "Wrong user profile" was vague | Work profiles and secondary users have their own data directories |
| 23.1 | "Modes of Introduction" undefined | Defined as the MASWE page section listing how the weakness gets into an app |
| 23.3 | FIRST unexpanded; severity-not-risk source | Expanded FIRST; linked the CVSS v4.0 User Guide |
| 23.4 | PR:H alternative had no score | Added its score (8.2) so the reader can compare models |
| 23.4 | DPoP unexpanded | Expanded at first use in this file |
| 24.1 | What MASWE-0043 is; how forced update works | Title added; "checks a minimum version from the server and blocks older builds" |
| 24.2 | GDPR scope, recipient, start of clock | See Corrections |
| 24.4 | Why a leaked secret must be treated as public | Anyone can extract it from the binary, as §22.3 experiment one shows |
| 24.4 | Why an upload-key leak isn't fatal | Google keeps signing with the never-exposed app signing key |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| CONTRIBUTING.md | Style | Says "British spelling in prose (artefact, authorisation, behaviour)" | Conflicts with editorial/PROMPT.md, which requires American spelling. I followed PROMPT.md. One of the two needs updating so later contributors don't revert. |
| book/12-verification.md | Correction log | Add an entry for 2026-10-20: Part 8 now says the user-CA default applies to apps targeting API 24+; GDPR Art. 33 scope and recipient; the 52-weeks-covers-78 arithmetic fixed | CONTRIBUTING asks for a log line per fix |
| book/12-verification.md | Glossary, "Conscrypt APEX" | Could add that the workaround is a bind mount over the APEX path in the Zygote and app namespaces, and that it lasts until reboot | Matches the corrected §22.1 Trap |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Bootrom (checkm8) | Read-only startup code in Apple's chips; a flaw in it (checkm8, A8–A11) can't be patched by software updates | §22.1 |
| Zygote | The Android process every app is started from; mount changes made in its namespace are inherited by new apps | §22.1 |
| Modes of Introduction | The MASWE page section listing how a weakness gets into an app; the starting point when no MASTG test exists | §23.1 |

## Judgment calls
- **American spelling** (authorization, license, behavior, organized, catalog, artifact, prioritized, program, organization, recognize, recognizes). PROMPT.md requires it, but CONTRIBUTING.md says British. Reverse if the house style stays British.
- **Opening of Chapter 22.** I cut "You can't learn this from reading." It repeated the Part 8 intro one paragraph earlier.
- **§22.3 experiment four.** I replaced "the single most clarifying experience in mobile security" with "teaches you more about client-side security than any amount of reading". The original was a superlative that nobody can verify.
- **Mermaid Figure 25.** I replaced em dashes in message labels with parentheses. The structure is unchanged, and `check.py --mermaid` passes.
- **Chapter 25 heading.** It contains an em dash ("Reference — testing method at a glance"). I left it because headings are link targets.
- **iOS jailbreak row.** I kept "No public jailbreak" for current flagships. A July 2026 report describes `usbliter8`, a SecureROM exploit for A12/A13, but no confirmed public jailbreak. It doesn't affect current flagships, so I didn't add it. Worth watching for the next recheck.
- `recheck_because` is unchanged, because none of the facts it names changed. `last_verified` is set to 2026-10-20.
