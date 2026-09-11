---
part: 06
last_verified: 2026-09-11
volatility: high
recheck_because: "Supply-chain techniques and GitHub controls both move fast"
---

# Part 6: The build and release pipeline

## Chapter 15: Why your pipeline is now the target

In 2026 your CI is a more attractive target than your app, and the reasoning is simple. It holds your signing keys, your store credentials and your cloud access. It runs code on every commit. And an attacker who owns it does not need to reverse engineer anything — they ship malicious code to your users **under your own signature**, through your own release channel.

Treat workflow files as production code with production privileges. That framing decides everything below.

### 15.1 What actually happened

These are not hypotheticals, and each one maps to a control.

**Shai-Hulud** (late 2025) was a self-replicating npm campaign *(reported)*. Compromised machines were registered as self-hosted runners named `SHA1HULUD`, and stolen credentials were used to create public repositories that served as exfiltration buckets. It prompted GitHub's revamped npm security roadmap and accelerated the roll-out of npm trusted publishing. *Lesson: monitor runner registrations and new-repository creation.*

**tj-actions/changed-files** and **aquasecurity/trivy-action** (the latter on 19 March 2026) were compromised by **force-pushing tags** to point at malicious code, which then exfiltrated secrets from CI runners. *Lesson: tags are mutable. Pin to commit SHAs.*

**Mini Shai-Hulud / TanStack** (May 2026) is the one to study. An attacker poisoned the pnpm store cache through a `pull_request_target` workflow. **Eight hours later**, the legitimate release workflow consumed the poisoned cache, extracted OIDC tokens from runner memory, and published 84 malicious versions across 42 packages *(reported)*. *Lesson: caches are a trust boundary. And see §15.5, because this one has a sting in it.*

**GhostAction** (September 2025) hijacked 327 GitHub accounts and stole 3,325 secrets *(reported)* using malicious workflows disguised as "GitHub Actions Security" repositories. *Lesson: workflow changes need review by someone who reads them.*

**Megalodon** (May 2026) pushed 5,718 malicious commits to 5,561 repositories in a single six-hour window *(reported)* using throwaway bot accounts. *Lesson: automated attacks outrun manual review.*

GitHub's own 2026 Actions security roadmap describes the pattern plainly: attackers abuse untrusted code execution, mutable dependencies, over-permissioned tokens, secrets, and weak runner observability. Those five categories are the agenda for this part.

- <https://github.blog/security/supply-chain-security/securing-the-open-source-supply-chain-across-github/>

### 15.2 Secrets: classify, then protect

Not every string is a secret, and treating them all identically makes people careless with the ones that matter.

**Not secret at all:** public API base URLs, feature flags, public keys. Source control is fine. Encrypting these teaches your team that the secret store is bureaucracy.

**Client identifiers:** OAuth client IDs, Firebase configuration. These necessarily ship in the app. Protect them **server-side** by restricting use to your package name and signing certificate — the identifier is public, the authorisation is not.

**Restricted:** any third-party key with quota or cost attached, including model provider keys. **Proxy through your backend.** Never in the app. If it is in the app, it is public, and now metered.

**Never in the client under any circumstances:** signing keys, service account credentials, database credentials, store API keys. CI secret store only, injected at build time.

The operational rules follow from Chapter 2's finding that 64% of 2022's leaked secrets are still valid:

**When a secret leaks, rotate first, then clean history.** Not the other way round. Deleting the commit does not un-leak the credential; assume harvest within minutes of the push. Then purge history, add scanning, and check access logs for use of the old credential.

**Scan every commit**, blocking: GitGuardian, `trufflehog`, or GitHub Push Protection.

**Prefer short-lived credentials to stored ones** wherever the platform allows — see §15.3.

**Audit your outputs, not just your inputs.** Run `strings` on your release artifact. This is the same experiment as Chapter 1 and it belongs in your release gate.

And two 2026-specific realities: with AI-assisted commits leaking at roughly double the human baseline, commit-time scanning has become load-bearing rather than optional for any team running agentic workflows; and if your tooling uses MCP servers, audit those configuration files specifically, because 24,008 secrets leaked through them and most scanning setups were not built with them in mind.

### 15.3 Hardening the workflow

Six controls, in the order I would apply them.

**Pin third-party actions to full-length commit SHAs.** Tags are mutable; SHAs are not. Keep the version in a trailing comment so the file stays readable:

```yaml
- uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8 # v5.0.1
```

Automate with `pinact` or StepSecurity's `secure-repo`. Keep SHAs current with Dependabot grouped updates, and add a **cooldown window**, seven days being a common choice, so you do not adopt a compromised release within an hour of publication. Then enforce it in repository settings, which can require actions to be pinned to a full-length SHA.

**Deny token permissions by default.** Set `permissions: {}` at workflow level and grant the minimum per job. **Repositories created before February 2023 default to read-write** — check yours rather than assuming.

```yaml
permissions: {}          # workflow level: deny everything
jobs:
  build:
    permissions:
      contents: read     # job level: only what this job needs
```

**Replace static cloud credentials with OIDC.** A stored key is valid indefinitely and portable the moment it leaks. An OIDC token is minted per workflow run, scoped to that job, and expires in minutes — so a compromised workflow yields a credential that is nearly worthless by the time it is exfiltrated. AWS, Azure and GCP all support it natively.

For package publishing, use **trusted publishing** and scope it to the **exact workflow filename and branch** rather than the whole repository, paired with branch protection requiring pull requests and blocking force pushes.

**Treat all external input as hostile.** PR titles, issue bodies, branch names and commit messages are attacker-controlled and get interpolated straight into shell steps. That is script injection. Pass untrusted values through `env:` and quote them; never inline `${{ github.event.* }}` into a `run:` block.

Be especially careful with **`pull_request_target`**, which runs with repository secrets in scope against code from a fork. It is the TanStack vector. If you need it, never check out or execute fork code in the same job that holds secrets.

**Put workflow files under review.** Add a `CODEOWNERS` entry pointing `.github/workflows/` at someone who understands the implications, and require CODEOWNERS approval through branch protection. Without it, anyone with write access can change what runs with your secrets. Be suspicious of external pull requests that modify pinned versions.

**Harden and watch the runners.** Prefer ephemeral runners so nothing persists between jobs. Never expose self-hosted runners to untrusted pull requests. Alert on **new runner registrations** and **new public repository creation** in your organisation — both would have surfaced Shai-Hulud early.

### 15.4 Dependencies and build inputs

Your build consumes more than your own code. Each input below is something an attacker can influence if you leave it unpinned.

**Lock your dependencies.** Commit `gradle.lockfile` via Gradle dependency locking, plus `Gemfile.lock` and `Package.resolved` for tooling. An unlocked build silently resolves a different version a month later and nobody notices.

**Enable Gradle dependency verification** with checksums, so a swapped artifact fails the build rather than shipping.

**Generate an SBOM per build** and scan it. The OWASP Dependency-Check Gradle plugin is free and flags known CVEs before release. MASTG-TEST-0274 and 0275 test exactly this, on both platforms.

**Audit what your dependencies request.** Check permissions in the *merged* manifest, not just the ones you declared. A UI animation library requesting `INTERNET` and storage access deserves a question.

**Treat caches as inputs.** A poisoned cache is a supply-chain attack with no dependency change to review. Scope cache keys tightly, and never let a fork-triggered workflow write to a cache your release workflow reads.

**Pin your toolchain**, not just your libraries: Gradle wrapper with checksum verification, a fixed JDK, `.ruby-version`, and fastlane pinned in `Gemfile.lock` so CI and every laptop run identical versions.

### 15.5 Provenance, and the uncomfortable thing about it

Build provenance — a signed statement about how an artifact was produced, expressed in frameworks such as SLSA — is genuinely valuable. It is also routinely oversold, and the TanStack incident is the proof.

**The malicious packages published in that attack carried valid, signed SLSA Build Level 3 provenance. Verification tools reported them clean.**

The reason is precise and worth internalising: **provenance attests to the process, not to the cleanliness of the inputs.** The build genuinely ran in the declared environment, from the declared repository, through the declared workflow. It just consumed a poisoned cache. Everything the attestation claimed was true, and the artifact was still malicious.

So when someone in a design review says "we have provenance, our supply chain is verified," the correct response is that provenance closes the *substitution* attack, meaning someone publishing an artifact that did not come from your build. It does nothing about a compromised input. You still need §15.4's controls on what enters the build.

### 15.6 Signing keys and release integrity

This is the part that decides whether an attacker can ship code as you.

**Android: use Play App Signing with a split key model.** Google holds the app signing key; you hold an **upload key** used only to upload. The property that matters: if your upload key is stolen, the attacker **cannot re-sign your app** — Google re-signs with the key they hold, and you register a new upload key and move on. Without this, a stolen signing key means an attacker ships code under your identity, which is close to unrecoverable. This is the strongest single argument for the split key model and it is why the recommendation is unambiguous.

**Keystore handling in CI.** Store it base64-encoded in the CI secret store, or GPG-encrypted in the repository with the passphrase in the secret store. Decode at build time into a path you delete afterwards. Never commit `key.properties` or a `gradle.properties` containing passwords — a leaked `gradle.properties` with a signing password has the same blast radius as a leaked server key.

And **fail the build when release signing is missing**, rather than silently producing a debug-signed artifact that the store rejects on upload. That check catches an entire class of embarrassing release incidents.

**iOS: use `fastlane match`.** Certificates and profiles live encrypted in a private repository, get pulled into a temporary keychain for the build, and are cleaned up automatically. Authenticate to the store with an **App Store Connect API key** rather than an Apple ID: no interactive 2FA, and it can be scoped and revoked.

**Both platforms.** Give store service accounts the **minimum role** — a key that can publish to production when it only needs the internal track is standing risk for no benefit. Restrict who can trigger release workflows and require manual approval for the production track. And keep releases **auditable**: tag the commit, record which workflow run produced the artifact, retain the build log. When someone asks "what exactly is in production," you want an answer rather than an investigation.

### 15.7 Verify what actually shipped

A perfect pipeline can still produce a bad artifact. Check the output, in an automated release-gate job rather than when someone remembers:

Run `strings` and a decompiler on the **release** build. Confirm `debuggable` is false, logging is stripped, and no debug network configuration survived. Confirm the artifact is signed with the expected key. Diff the dependency tree against the previous release and ask about anything new.

- <https://corgea.com/learn/github-actions-security-checklist>
- <https://www.buildmvpfast.com/blog/github-actions-supply-chain-security-hardening-guide-2026>
- <https://www.aikido.dev/blog/checklist-github-actions>

### 15.8 Build configuration, in code

The pipeline chapter covers secrets and supply chain. This is the build configuration itself, which is where several cheap protections live.

#### Android: R8 rules with security in mind

```proguard

#### Verify it

Build configuration is the area where the source and the artifact most often disagree, so check the artifact.

```
# What actually shipped?
unzip -p app-release.apk classes.dex | strings | grep -iE "api[_-]?key|secret|password|bearer"
aapt dump badging app-release.apk | grep -E "debuggable|application-label"
apksigner verify --print-certs app-release.apk
```

**Pass:** no credentials in the output, no `debuggable` flag, and a signing certificate that matches your expected fingerprint. **Fail on any of the three** is a release-blocking finding, not a backlog item.

For iOS:

```
strings MyApp.app/MyApp | grep -iE "api[_-]?key|secret|https://.*internal"
otool -l MyApp.app/MyApp | grep -A3 LC_CODE_SIGNATURE
```

Then confirm logging is gone by running the release build and watching `adb logcat` or Console during a login flow. A build flag that says logging is disabled is not evidence; an empty log is.

Put all of this in a release-gate job (§15.7). A check that runs when someone remembers is not a control.

# proguard-rules.pro

# Keep serialization models — reflection needs the names
-keepclassmembers class * {
    @kotlinx.serialization.Serializable *;
}

# Keep Tink, which uses reflection internally
-keep class com.google.crypto.tink.** { *; }

# DO NOT add keep rules for your security detection classes.
# Letting R8 obfuscate them is the point: an attacker grepping the
# decompiled output for "RootDetector" should find nothing.

# Strip logging from release builds
-assumenosideeffects class android.util.Log {
    public static int v(...);
    public static int d(...);
    public static int i(...);
}
```

That middle comment is the part worth internalising *(reasoned)*, and it is the opposite of most keep-rule advice. Every `-keep` rule you add is a name you have handed to an attacker. Keep what reflection genuinely requires, and nothing else — especially not the classes whose job is to be hard to find.

#### Android: separate debug and release properly

```kotlin
android {
    buildTypes {
        debug {
            isDebuggable = true
            buildConfigField("Boolean", "ENABLE_PINNING_BYPASS", "true")
            buildConfigField("Boolean", "ENABLE_SECURITY_CHECKS", "false")
        }
        release {
            isDebuggable = false
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            buildConfigField("Boolean", "ENABLE_PINNING_BYPASS", "false")
            buildConfigField("Boolean", "ENABLE_SECURITY_CHECKS", "true")
        }
    }
}
```

The `BuildConfig` flag pattern is how you get a debuggable app without shipping a debuggable app. But note the risk it introduces: **a flag that disables pinning is a flag an attacker would love to flip.** Gate it on `BuildConfig.DEBUG` as well, so the bypass path is not even compiled into release, and verify by inspecting the release artifact (Chapter 15.7) rather than trusting the configuration.

#### iOS: strip the release build

Set these in Build Settings for the Release configuration:

| Setting | Value |
|---|---|
| `STRIP_INSTALLED_PRODUCT` | `YES` |
| `STRIP_STYLE` | `all` |
| `DEPLOYMENT_POSTPROCESSING` | `YES` |
| `GCC_GENERATE_DEBUGGING_SYMBOLS` | `NO` |
| `SWIFT_OPTIMIZATION_LEVEL` | `-O` |

Keep the generated dSYM files somewhere you can retrieve them — you need them to symbolicate crash reports, and stripping the binary is precisely what makes them necessary.

#### Injecting secrets at build time

**Android**, reading from a file CI writes and `.gitignore` excludes:

```kotlin
// build.gradle.kts
val localProps = java.util.Properties().apply {
    val f = rootProject.file("local.properties")
    if (f.exists()) f.inputStream().use { load(it) }
}

android {
    defaultConfig {
        buildConfigField("String", "API_BASE_URL",
            "\"${localProps["API_BASE_URL"] ?: System.getenv("API_BASE_URL")}\"")
    }
}
```

```yaml
# .github/workflows/release.yml — CI writes the file, then builds
- name: Write local.properties
  run: |
    echo "API_BASE_URL=${{ secrets.API_BASE_URL }}" >> local.properties
    echo "MAPS_API_KEY=${{ secrets.MAPS_API_KEY }}" >> local.properties
- run: ./gradlew assembleRelease
```

**iOS**, using an `.xcconfig` that CI generates and source control ignores:

```
// Secrets.xcconfig  (gitignored; CI writes it)
API_BASE_URL = api.example.com
```

Reference it from `Info.plist` as `$(API_BASE_URL)` and read it via `Bundle.main.infoDictionary`.

**Remember what this does and does not achieve.** Build-time injection keeps secrets out of source control — which is Chapter 15.2's actual goal. It does **not** keep them out of the app: anything in `BuildConfig` or `Info.plist` is in the binary and recoverable with `strings`. Only the classification in Chapter 15.2 decides what may ship at all, and anything genuinely sensitive belongs behind the BFF (Chapter 12.3).

---
