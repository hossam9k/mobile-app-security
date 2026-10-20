# book/05-resilience.md

## Summary
- Words before / after: 4,951 / 5,160
- Edits: clarity 24, filler 6, voice 30, spelling 9, explanation 12, code 0
- Facts checked: 79 · correct 75 · corrected 1 · unverified 3

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| 14.4 (Trap) | "Google Play restricts that permission to apps whose core function needs it, and root detection does not qualify." | Same restriction, plus the permitted uses (device search, antivirus, file managers, browsers) and Play's temporary exception for dedicated banking and digital-wallet apps, for security purposes only. Notes that `<queries>` is enough either way. The old text implied no security-based exception exists. | https://support.google.com/googleplay/android-developer/answer/10158779 | 2026-10-20 |

New claims added during the edit, both verified:
- §14.1: Janus, CVE-2017-13156 (System, EoP, High; AOSP 5.1.1–8.0; fixed in the 2017-12-01 patch level), used as the example for "old signature schemes reopen attack classes". Source: https://source.android.com/docs/security/bulletin/2017-12-01. MASTG-BEST-0006 asks for v2 or v3 (checked on mas.owasp.org).
- §14.4 (Trap): Dopamine "roothide" builds randomize the `/var/jb` path. Source: The Apple Wiki (Dopamine-roothide), via search, because the page returned 403 to direct fetch. Marked *(reported)*. The roothide repository status conflicts (archived April 2025 vs. a successor repo with 2026 releases).

## Verified correct (2026-10-20)
- MASTG-TECH: 0001, 0003, 0004, 0008, 0009, 0011, 0012, 0016, 0017, 0026, 0043, 0051, 0052, 0054, 0059, 0060, 0063, 0064, 0068, 0069, 0071, 0095. Titles and platforms match the text.
- MASTG-DEMO-0106, 0107, 0108, 0132, and 0133: titles match exactly. DEMO-0107 does use a `/proc/self/maps` check.
- MASTG-TEST-0368 and 0369, MASTG-KNOW-0030 (its Frida indicators include port 27042 and the `gum-js-loop`/`gdbus` threads, and don't include TracerPid), MASTG-APP-0003, MASTG-APP-0032, and the crackmes URL.
- MASTG-BEST-0002, 0006, 0007, 0008, 0010, and 0022: titles correct. BEST-0029 is still a placeholder as of today.
- MASVS-RESILIENCE-1 to 4: the meanings match the control statements.
- MASWE-0005, 0024, 0030, and 0038: v1.0.0 titles match.
- Frida 17.0.0: released 17 May 2025; bridges unbundled from GumJS; static `Module` APIs removed.
- bagbak: README marks it deprecated in favor of `mremap_encrypted` tools.
- R8 full mode has been the default since AGP 8.0.
- Vector is JingMatrix's LSPosed successor. ElleKit is the Substrate replacement used by Dopamine and palera1n.
- Magisk "Hide the Magisk app" (stub with a chosen name), DenyList, and Shamiko all check out.
- Package names `com.topjohnwu.magisk`, `me.weishu.kernelsu` (KernelSU source; overridable at build time), and `me.bmax.apatch` (F-Droid) are correct.
- TrickyStore and TEESimulator exist and spoof keyboxes.
- `canOpenURL` is deprecated in 27.0, with a 25-scheme limit for apps linked on iOS 27 or later, down from 50 (Apple doc JSON).
- Rootless `/var/jb`, Sileo, and Zebra all check out. rootAVD exists.

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| 14.2 | "some payment-scheme and banking rulebooks expect a local response" | Searched PCI MPoC attestation and monitoring. MPoC has an attestation-and-response domain, but I couldn't find text that mandates a local response | Keep *(contested)*; add a named source (e.g. PCI MPoC Domain 3) if the author has one |
| 14.4 (code) | Zebra URL scheme is `zbra://` | Community samples use `zbra://`, but MASTG-DEMO-0021 reportedly uses `zebra://` | Leave the code as is; consider adding both schemes |
| 13.2 table / 13.1 | IDA Pro and Hopper are commercial, and "cheap next to any fraud payout" | General knowledge; this is a judgment, not a sourced fact | None needed (opinion) |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| 13.1 | DRM unexpanded | "digital rights management" |
| 13.1 | "hook" used before §13.2 defines it | Short gloss plus a §13.2 pointer |
| 13.2 | Why the attacker installs a CA | "so the proxy can decrypt TLS traffic" |
| 13.2 | What Frida Gadget is | "Frida packaged as a library" |
| 13.3 | Which "next chapter" position | Named it: detect and report, don't block (§14.2) |
| 14 intro | Control-flow flattening undefined | One-clause definition |
| 14.1 | Minification undefined | One-sentence definition |
| 14.1 | WebView debugging: no why | Risk via adb and Chrome DevTools |
| 14.1 | "Old signature schemes reopen attack classes": no example | Janus (CVE-2017-13156) |
| 14.2 | Custom ROM undefined here | "third-party builds of Android" |
| 14.4 | dm-verity, JDWP, and ptrace unexplained | Short glosses |
| 14.4 | `currentSigningCertSha256()` described as a local check (conflicted with "send, never branch") | It reads the digest; the backend compares |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| CONTRIBUTING.md | Style | It mandates British spelling; editorial/PROMPT.md mandates American | Conflicting house rules. I followed PROMPT.md (artefact→artifact, favour→favor, licence→license, optimiser→optimizer, defence→defense, behaviour→behavior) |
| book/12-verification.md | Correction log | Add a line for the QUERY_ALL_PACKAGES correction (§14.4) | CONTRIBUTING step 2 |
| book/12-verification.md | Glossary | The "Obfuscation" entry points to §14.3, but the definition is in the Chapter 14 intro | Accuracy of the pointer (minor) |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Tamper detection | Code that notices the app or its environment has been modified (root, hooking framework, debugger, re-signed APK) | Chapter 14 intro |
| Control-flow flattening | Obfuscation that rewrites a function's branches into one dispatch loop so its logic no longer reads top to bottom | Chapter 14 intro |
| Minification | Removing unused code and renaming what's left to short, meaningless names (R8) | §14.1 |
| JDWP | Java Debug Wire Protocol, the debugger protocol Android Studio uses; detected by `Debug.isDebuggerConnected()` | §14.4 |
| dm-verity | Kernel verification of the system partition against a signed hash | §14.4 |

## Judgment calls
- §13.3: "Protect, detect, bypass" became "Attack, detect, bypass". The three demos are attack (0106), defense (0107), and bypass (0108), so "protect" didn't match the first one.
- Opening paragraph: "It is the same sequence that MASTG-DEMO-0107 and 0108 publish" became "publish the same detect-then-bypass sequence for a Frida check". The demos target a Frida check, not a root check, so the old wording overstated the match.
- §14.4: the "two notes" paragraph actually held three notes (scheme check, `fork()`, sandbox write). I split it into a three-item list. The rules after the reporting code became a numbered list.
- §14.2: "You have built a speed bump and paid for a wall" became the literal "You've paid for prevention and got a short delay" (idiom rule). Similar literal rewrites: "speed bump, not a wall" (§13.1), "open door" (§14.1), "survives contact" (§13.2), "real currency" (Chapter 14 intro).
- §14.4 QUERY_ALL_PACKAGES trap: added the banking/wallet exception, which weakens the original absolute statement. The author may prefer a shorter wording.
- The `last_verified` frontmatter field is set to 2026-10-20. `recheck_because` is unchanged: all of its facts still hold.
