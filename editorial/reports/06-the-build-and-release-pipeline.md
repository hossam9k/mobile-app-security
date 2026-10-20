# book/06-the-build-and-release-pipeline.md

## Summary
- Words before / after: about 6,250 (estimate; the repo has no git baseline) / 6,795
- Edits: clarity 38, filler 9, voice 22, spelling 31, explanation 19, code 4
- Facts checked: 78 · correct 66 · corrected 10 · unverified 2

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| 15.1 | Roadmap "promises dependency locking, scoped secrets and an egress firewall; check which have shipped" | Adds that workflow execution protections went GA on 17 Sep 2026 and workflow lockfiles (`actions.lock`) entered public preview on 14 Oct 2026 | https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/ ; https://github.blog/changelog/2026-10-14-github-actions-workflow-lockfiles-in-public-preview/ | 2026-10-20 |
| 15.3 | Trap: "the comment is not checked by anything" | GitHub doesn't check it, but `pinact` and zizmor's `ref-version-mismatch` audit do | https://github.com/suzuki-shunsuke/pinact ; https://docs.zizmor.sh/audits/ | 2026-10-20 |
| 15.3 | checkout v7 "backported to the other supported majors in July" | Backported on 20 July 2026, and only floating tags pick it up; SHA-pinned workflows must move the pin | https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout | 2026-10-20 |
| 15.3 | Default rule "disables `pull_request_target` in public repositories" | Adds "that have no event policy of their own" and that private and internal repos aren't affected | changelog 2026-09-17 (above) | 2026-10-20 |
| 15.3 | Lockfiles not mentioned | Adds workflow lockfiles (public preview) as the newer pinning control | changelog 2026-10-14 (above) | 2026-10-20 |
| 15.4 | Read-only triggers: "`pull_request_target` runs may only read them" | Also `issue_comment` and `workflow_run`; adds `cache-mode` values and a warning that a write-capable `cache-mode` on `pull_request_target` reopens the hole | https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching | 2026-10-20 |
| 15.5 | "L3's isolation stops one run tampering with another run's environment; a cache your own workflow chooses to restore is an input you accepted" *(reasoned)* | SLSA v1.2 L3 explicitly forbids one build poisoning a cache another build uses, so whether the L3 label held is now marked *(contested)*. The conclusion (verification couldn't catch it) is kept as *(reasoned)* | https://slsa.dev/spec/v1.2/build-requirements | 2026-10-20 |
| 15.5 | "reported by Snyk, which calls them valid SLSA Build Level 3 attestations, and by StepSecurity" | Attribution swapped: StepSecurity uses that wording; Snyk says "validly-attested SLSA Build Level 3 provenance" | https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem ; https://snyk.io/blog/tanstack-npm-packages-compromised | 2026-10-20 |
| 15.6 | Hybrid signing "adds a post-quantum ML-DSA-65 signature … alongside a classical RSA one" | RSA 4096 + ML-DSA-65 hybrid, plus a separate classical key for Android 16 and earlier | https://support.google.com/googleplay/android-developer/answer/9842756 | 2026-10-20 |
| 15.6 | `match` "installs them into a temporary keychain for the build, and cleans up afterwards"; team key "(an Admin creates it)" | `match` installs into the keychain; `setup_ci` creates the temporary keychain on CI. The Account Holder or an Admin creates team keys | fastlane source (`setup_ci.rb`, `match/module.rb`); https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api | 2026-10-20 |
| 15.6 YAML | `gradle/actions/setup-gradle@9c97…fbfb # v6.3.0` | `@3f5f9adaf7d9fecd50b5935e54106014257a94e6 # v6.4.0` (28 Sep 2026). I kept `setup-java` at v6.0.1: v6.1.0 (14 Oct 2026) is inside the chapter's own 7-day cooldown | `git ls-remote` | 2026-10-20 |
| 15.8 Verify | Upload certificate at "Protected with Play → Play Store distribution → Go to Play app signing" | "Protected with Play → Play Store protection → Manage Play app signing", *Upload key certificate* section | Play Console Help 9842756 | 2026-10-20 |
| 15.8 | AGP 9.3 block "which Google's documentation now presents as the replacement" | Docs label `isMinifyEnabled`/`isShrinkResources` "legacy DSL for AGP versions lower than 9.3"; keep files need a `.keep` suffix | https://developer.android.com/topic/performance/app-optimization/enable-app-optimization | 2026-10-20 |

Checked and correct (no change): TanStack (date, `bundle-size.yml`/pnpm store, 7 h 46 min gap, `/proc` memory read, 84 versions/42 packages); Ultralytics (dates, branch-name injection via `pull_request_target`, XMRig, unrevoked PyPI token; per PyPI, Wiz, and StepSecurity); tj-actions (CVE, dates, 23,000+, reviewdog CVE-2025-30154; wording softened to "most likely", since Wiz calls it likely); Nx (date, PR-title injection, npm token, AI CLIs); GhostAction (all figures); Shai-Hulud (`SHA1HULUD` runners, 25,000+ repos); Trivy (CVE, 76/77 tags, all `setup-trivy` tags, v0.69.4, non-atomic rotation); Megalodon (all figures); gluestack (17 packages, >1M weekly, token without 2FA); SparkCat (Kaspersky, Feb 2025, both stores); roadmap date; GitGuardian 64%, 3.2% vs 1.5%, 24,008; push protection free on public repos and part of Secret Protection; checkout v7.0.1, attest v4.2.2, and setup-java v6.0.1 SHAs; `cache-disabled` and `subject-path` inputs; Dependabot 3-day default (14 Jul 2026), security updates exempt, `cooldown.default-days`; SHA-pinning policy and `!` blocking (15 Aug 2025); immutable releases GA (28 Oct 2025); GITHUB_TOKEN default (2 Feb 2023); npm trusted publishing GA (31 Jul 2025); `pull_request_target` from the default branch (8 Dec 2025); `allow-unsafe-pr-checkout`; cache scoping rules; attestation plan limits, L2/L3, private Sigstore without a transparency log; `attest-build-provenance` wraps `attest`; `id-token`/`attestations` permissions; SLSA v1.2 levels and Source track; upload key reset path; Aug 2021 AAB/Play App Signing; developer verification (30 Sep 2026, four countries, 2027 global); R8 full mode default since AGP 8.0; `proguardAndroidTxt.disallowed`; `strictFullModeForKeepRules`; Gradle locking and verification commands; `validate-wrappers` default; MASTG-TEST-0274/0275 titles (no deprecation banner seen); Xcode settings (DEPLOYMENT_POSTPROCESSING, STRIP_*, ENABLE_TESTABILITY disables strip, GCC_GENERATE_DEBUGGING_SYMBOLS); match storage modes; individual keys can't use provisioning endpoints; zizmor audit names.

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| 15.4 | `cache-mode` "generally available since September 2026" | Docs confirm the key and its values. The GA date comes only from secondary sources quoting a 10 Sep 2026 changelog that I couldn't load | Keep as is; recheck the changelog |
| 15.3 | "Compromised releases are usually caught in their first days" | No primary statistic. GitHub's Dependabot cooldown post gives the same rationale qualitatively | *(reasoned)* if the author wants a marker |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| Intro | CI/CD, runner, and supply-chain attack used before they were defined | Moved the definitions paragraph ahead of first use |
| 15.1 | OIDC token used before §15.3 defines it | One-sentence inline definition |
| 15.1 | SparkCat "OCR stealer" unexplained | What it read (wallet recovery phrases from photos) |
| 15.2 | MCP undefined | Short gloss |
| 15.3 | Why tags are unsafe and SHAs aren't | Tag = movable label; SHA = content hash |
| 15.3 | What a cooldown is | Definition and rationale |
| 15.3 | Why `GITHUB_TOKEN` permissions matter | One sentence on blast radius |
| 15.3 | Why the `env:` pattern fixes injection | One sentence after the code |
| 15.3 | `pull_request_target` changes in one long sentence | Numbered list of the three stages |
| 15.3 | Why self-hosted runners and alerts matter | Reasons added |
| 15.4 | Lockfile vs verification metadata | "Lockfile pins the version; verification pins the bytes" |
| 15.4 | Why an SBOM helps | The "do we ship the vulnerable version?" use |
| 15.5 | What a transparency log gives you | Short gloss |
| 15.6 | Why the keystore is base64-encoded | Secret stores hold text |
| 15.8 | R8 and keep rules undefined in this file | Short definitions |
| 15.8 | Why a `BuildConfig` security flag is risky | The relaxed code can survive in the release build |
| 15.8 | "Symbolicate" | Short gloss |
| 15.8 | BFF used as an acronym only | Expanded with a pointer to §12.3 |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| book/12-verification.md | Glossary | `cache-mode` entry: say "GA September 2026 (date from secondary sources)" or confirm it; add `issue_comment`/`workflow_run` to the read-only triggers if the entry lists them | Matches §15.4 |
| book/12-verification.md | Glossary | "SLSA" / "Build provenance" entries: L3 includes a no-cache-poisoning requirement | §15.5 now treats the TanStack L3 claim as contested |
| book/12-verification.md | Correction log | Add an entry for the 2026-10-20 changes listed above | CONTRIBUTING step 2 |
| frontmatter (this file) | recheck_because | Optional: mention that workflow lockfiles shipped in preview and that execution protections are GA | I left it unchanged because no fact in it is wrong |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Workflow lockfile | `.github/workflows/actions.lock`, written by `gh actions-lock`; pins every action a workflow uses, including transitive ones, to a commit (public preview Oct 2026) | §15.3 |
| Workflow execution protections | GitHub rulesets that control which actors and events can start workflows; the default rule disables `pull_request_target` in public repos from 2 Nov 2026 | §15.3 |
| Keep rule | An R8/ProGuard directive that stops R8 removing or renaming a class or member | §15.8 |
| Hybrid signing (Play) | Play App Signing with an RSA 4096 + ML-DSA-65 key pair (APK Signature Scheme v3.2, Android 17+), plus a classical key for older Android versions | §15.6 |

## Judgment calls
- I removed "(…, the project's own spelling)" after SLSA: once the prose is American, the note no longer contrasts with anything.
- I kept `actions/setup-java` at v6.0.1 rather than v6.1.0, because v6.1.0 is six days old and the chapter recommends a seven-day cooldown. The trailing sentence now says the SHAs are the newest releases outside a seven-day cooldown.
- §15.5: I marked whether the L3 claim held as *(contested)*, because SLSA's own L3 text bans cross-build cache poisoning. The author may prefer to argue a position.
- I didn't include `artifact-metadata: write` in the release job. The `actions/attest` README lists it, but only for storage records with `push-to-registry`; the README's own default provenance example omits it.
- Intro: I moved the "Three terms" paragraph above "the shape of the modern supply-chain attack" so the terms are defined before use. No content was removed.
- Headings "What actually happened" and "Verify what actually shipped" keep "actually", because heading text is frozen.
