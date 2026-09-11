---
part: 10
last_verified: 2026-09-11
volatility: medium
recheck_because: "Inherits volatility of its source chapters"
---

# Part 10: Questions and answers

These are the questions that come up in design reviews and interviews, and the ones where people's understanding tends to be thin. Answers are written out properly. If you cannot answer one without looking, that is your next reading.

## Foundations

**Why not just obfuscate everything and prevent reverse engineering?**
Because you cannot. Any app decompiles with free tools and any method can be hooked at runtime. Obfuscation raises cost and buys time against opportunistic attackers and automated tooling; it does nothing against a determined one. Design so that whatever is extracted is worthless without server-side validation. See Chapters 1 and 14.

**What does "the client is not the trust boundary" mean in practice?**
Every decision that matters happens on your server. The client gathers signals and proposes actions; the server decides. If your app decides locally whether a transfer is permitted, an attacker patches that decision out in minutes.

**A root detection library flags a device. What should the app do?**
Report it to the backend as a risk signal and let the session continue under elevated scrutiny. The backend then decides whether to require step-up authentication, cap limits, or flag the account. Blocking locally is trivially removed by an attacker who is already hooking your code, generates false positives against developers and custom-ROM users, and destroys the intelligence you would otherwise have gained. MASTG-DEMO-0108 demonstrates the bypass.

**What is the difference between the Mobile Top 10 and MASVS?**
The Top 10 is an awareness list from a separate working group, updated in late 2024 after eight years. MASVS is the verification standard: eight categories, twenty-four controls in v2.1.0. Top 10 builds awareness; MASVS provides assurance. Different groups, different jobs.

**What is MASVS L2?**
A trap. Since MASVS v2.0.0 the verification levels moved out of MASVS and became MASTG testing profiles: MAS-L1, MAS-L2 and MAS-R. Say "the MAS-L2 profile." If a source still says MASVS L2, or MSTG rather than MASTG, treat its technical detail as dated too.

**Can you get an app OWASP-certified?**
No. OWASP states it cannot certify mobile applications or accredit third parties to do so. What you can publish is a certification statement — your own claim about which controls you meet and how you verified them, which anyone can check with the MASTG. That is more useful than a badge because it is falsifiable.

**Who am I actually defending against?**
Four different adversaries with different economics: the opportunist running automated scans, the cloner repackaging your binary, the fraudster abusing your business logic at scale, and the targeted adversary with time and money. Naming which one a control addresses stops you from arguing about obfuscation when your real problem is that your API trusts a client-supplied user ID. Chapter 1.3.

## Storage and keys

**Where do you store an auth token on Android in 2026?**
Not `EncryptedSharedPreferences` — Google deprecated the whole Jetpack Security Crypto library in April 2025 at 1.1.0-alpha07 with no further releases. Use DataStore for persistence, Tink for encryption, and Android Keystore via `KeyGenerator` for key protection. For long-lived tokens add `setUserAuthenticationRequired`. Better still, keep short-lived access tokens in memory and persist only the refresh token.

**Why was EncryptedSharedPreferences deprecated?**
Google was quiet about it, but the reasons are visible: it had to paper over Keystore inconsistencies across OEM devices and Android versions, it performed synchronous crypto on the calling thread producing StrictMode violations, and keyset corruption exceptions plagued specific OEM devices. Maintaining it alongside the modern DataStore path was not sustainable.

**Is plain SharedPreferences insecure?**
Mostly no, and the existence of `EncryptedSharedPreferences` misled a generation of developers about this. Since Android 10, file-based encryption is enforced on device and the app sandbox isolates your data; reading another app's preferences generally requires physical access or an already-compromised device. Encrypt because your threat model includes device compromise, not out of reflex.

**What actually happens when I encrypt with a Keystore key?**
Your process sends the data and a key handle to the keystore2 daemon. The daemon holds your key as an encrypted keyblob it can store but cannot use or reveal. It passes the request to the KeyMint trusted application running in secure hardware, which decrypts the keyblob internally, validates the key's authorizations, performs the operation and returns only the result. The key never enters your process or the Android OS.

**TEE versus StrongBox — what is the real difference?**
The TEE is a secure area of the *main* processor, isolated by hardware; if Android is fully compromised an attacker might *use* your keys on that device but cannot *extract* them. StrongBox is a dedicated, physically separate secure processor: an embedded or integrated Secure Element, such as Titan M in Pixel devices. It offers stronger isolation and tamper resistance. StrongBox arrived in Android 9, is not universal, is slower, and supports a deliberately reduced subset of algorithms and key sizes.

**Why does StrongBox availability change your design?**
Because you must decide the fallback explicitly. Check `KeyInfo.getSecurityLevel()`, which returns `SOFTWARE`, `TRUSTED_ENVIRONMENT` or `STRONGBOX`, and either fall back to TEE and record that you did, or require server-side step-up for that flow on that device. Silently falling back to a software-backed key for a payment flow is a finding, not a fallback.

**How does the iOS Keychain protect an item?**
It is one SQLite database for all apps, managed by securityd, which decides your access from your entitlements. Each item uses two AES-256-GCM keys: a metadata key encrypting all attributes except the secret, protected by the Secure Enclave but cached in the Application Processor so searches stay fast; and a per-row secret key encrypting `kSecValueData`, which always requires a round trip through the Secure Enclave.

**Which Keychain accessibility class for a token, and why?**
`WhenUnlockedThisDeviceOnly` for most tokens. "WhenUnlocked" requires the device to be unlocked; "ThisDeviceOnly" keeps the item out of backups and off other devices. If background refresh needs access, `AfterFirstUnlock` is the considered answer — Apple names that exact use case. `kSecAttrAccessibleAlways` maps to no protection and should not appear in new code.

**Background refresh is failing because my Keychain item is WhenUnlocked. What do I do?**
Restructure when the work happens, or move to `AfterFirstUnlock` deliberately. Do not loosen to `Always` — that makes the item readable on a locked device and puts it in the backup. This is the single most common way iOS token storage gets quietly weakened.

**Can the Secure Enclave encrypt my data directly?**
No, and this catches people. It supports elliptic-curve keys only, with no RSA, and it is for signing and key agreement rather than direct encryption and decryption. To get Secure Enclave protection for encrypted data you do ECDH key agreement, or encrypt a symmetric key. Your `SecKey` in Swift is a handle; the key itself never enters RAM.

**What is the risk of adding an app to my keychain-access-group?**
You are trusting that app completely. Anything in the group can call `SecItemCopyMatching` on your items, including a compromised app under your own Team ID. Enumerate what is in your groups.

**Where do secrets leak that has nothing to do with encryption?**
Logs, backups, auto-generated screenshots when the app backgrounds, the keyboard cache, lock-screen notifications, the clipboard (on iOS the general pasteboard is shared and has historically synced across devices), and process memory. MASVS-STORAGE-2 exists for exactly this, and it is where most real leaks happen.

## Key attestation

**What is key attestation, and why would my backend believe the app?**
Your server issues a nonce; the app generates a key in the Keystore with that nonce as the attestation challenge; Android produces an X.509 chain rooted in a Google attestation root, with a `KeyDescription` extension carrying the security level, boot state and your nonce; your server verifies the chain and reads the properties. It is credible because the authorization list is collected or generated by code inside the secure hardware and is not controlled by the platform — sourced from the bootloader or a secure channel that does not require trusting Android.

**What is going to break my attestation verification in 2026?**
Google activated a new Remote Key Provisioning root certificate on 1 February 2026, and all RKP-enabled devices must use it by 10 April 2026. Applications that verify key attestation and do not trust the new root will start failing. Also: under online provisioning the chain is longer than it used to be and is subject to change, and the root is moving from RSA to ECDSA. Do not hardcode the root, the chain length, or the algorithm.

**Why is RKP better for privacy than factory-provisioned keys?**
Each application receives a different attestation key, keys rotate regularly, and Google's backend is segmented so the server verifying a device's public key does not see the attached attestation keys — so attestation keys cannot be correlated back to a device.

**Can hardware key attestation be defeated?**
Yes, and you should know it. Tooling exists that serves selected apps from a software KeyMint running inside the real keystore daemon while other keys stay on real hardware, embedding AOSP's own reference trusted application and signing with a supplied keybox — producing certificates generated the same way real hardware generates them, and therefore internally consistent. Attestation raises the bar substantially; treat a single result as a strong signal rather than proof.

## Network and pinning

**Should you pin certificates?**
Know both sides. OWASP's Pinning Cheat Sheet says for most apps probably never, because outage risk outweighs benefit now that Certificate Transparency, short lifetimes and automated issuance exist; Google's Android docs caution against it for the same operational reason. But MASTG recommends it for MAS-L2 apps and MASVS-NETWORK-2 asks for it on endpoints you control, and MASTG notes that Google's warning is often misread — the real advice is to pin *with* backup pins and a rotation plan. My position: pin if you control both ends, can update the pinset, and have an owned rotation runbook. Otherwise CT plus HSTS.

**What does pinning actually protect against, given TLS already validates?**
Standard validation trusts any root in the device trust store — roughly a hundred organisations plus anything an administrator or user has added. Pinning narrows that to a specific identity you nominated. The threat is a rogue or compromised CA, or an administrator-installed certificate.

**Why pin SPKI rather than the certificate?**
The SPKI is the public key info. If a certificate is renewed with the same key pair, the SPKI is unchanged and an SPKI pin still validates; a full-certificate pin breaks on every renewal. Given lifetimes dropped to 200 days in March 2026 and reach 47 days by 2029, that difference decides whether pinning is operable at all.

**Why is an intermediate CA pin more rotation-resilient than a leaf pin?**
The leaf changes every renewal, and if your ACME automation generates a fresh key pair each time, the SPKI changes with it. The intermediate changes rarely, so it survives leaf renewals. The trade-off is a wider trust surface — you are trusting anything that CA issues for your domain. At 47-day certificates, leaf pinning without key reuse is close to unworkable.

**What is the certificate lifetime schedule, exactly?**
CA/Browser Forum Ballot SC-081v3, approved April 2025, originally proposed by Apple, adopted with no votes against. Maximum lifetime: 398 days until 15 March 2026, then 200 days, then 100 days from 15 March 2027, then 47 days from 15 March 2029. Domain validation reuse shrinks in parallel to 10 days by 2029 — the second column most summaries omit, and the one that breaks manual processes first.

**What breaks first when pinning goes wrong?**
Everything, at once, for every user on that build — and only an app store release fixes it. That is why you ship at least one backup pin, monitor pin-validation failures, keep a remote kill switch, and make sure whoever manages certificates knows that changes require a coordinated release.

**What are the alternatives to pinning, and what do they actually do?**
Certificate Transparency gives you public append-only logs of issued certificates, so you can detect a certificate you did not request for your domain — that is *detection*, not prevention. HSTS forces HTTPS and prevents protocol downgrade; it does nothing about a fraudulently issued certificate. Backend anomaly detection catches the traffic pattern of interception. Together: fast detection and a narrowed surface, without the outage risk.

**What is the single worst network security mistake you see?**
`onReceivedSslError` calling `proceed()` in a WebView. It silently disables all certificate validation for that WebView, it usually gets added to make a development warning go away, and it survives to production because nothing visibly breaks. MASTG-TEST-0284 exists for it.

## Attestation and integrity

**What does Play Integrity prove?**
That the request came from your genuine, Play-installed, unmodified app binary, on a device meeting a stated integrity level, associated with a licensed account. Not that the user is legitimate, and it is not a jailbreak oracle. One strong input to a backend risk decision.

**Standard or classic requests?**
Standard for almost everything: lowest latency at a few hundred milliseconds, high reliability, and Google Play handles some replay and exfiltration protection. Classic for infrequent high-value one-off checks where you want a server-issued nonce and accept responsibility for replay protection yourself. Classic is more expensive and easier to get wrong.

**MEETS_BASIC_INTEGRITY but not MEETS_DEVICE_INTEGRITY — what do you do?**
Do not hard-block. Since May 2025, device integrity on Android 13+ requires a hardware-backed positive verified boot verdict, so failure often means an older or unusual-but-legitimate device. Route the session into a higher-risk bucket: allow browsing, require step-up or reduce limits for sensitive actions, monitor. Blocking before you have measured your install base's verdict distribution locks out real customers.

**And device integrity without strong integrity?**
Usually a legitimate user whose device has not had a security update in twelve months — that is the Android 13+ requirement for strong integrity. Treat strong integrity as a bonus signal for your very highest-risk flows, never as a baseline gate.

**Why did my Play Integrity verdicts suddenly come back empty?**
Most likely you decrypted the same token twice. Repeated decryption returns cleared verdicts: the device recognition verdict comes back empty and the app and licensing verdicts return `UNEVALUATED`. Check your retry path.

**What is the first thing to check in an integrity verdict?**
`requestDetails`. Confirm the package name and nonce or request hash match what you issued, before reading anything else. Otherwise you may be evaluating a replayed token from a different request.

**How do you roll out attestation without breaking users?**
Implement without enforcement first. Collect verdicts from your real install base, look at the actual distribution, estimate the impact of each enforcement option, then enforce incrementally starting with the highest-value flows. Google's own documentation recommends this sequence, and library 1.5.0 added remediation dialogs so users can fix their own problem rather than hitting a dead end.

**What does App Attest prove, and what does it not?**
It proves a key lives in the Secure Enclave of a genuine Apple device running your genuine app, with attestation data derived from an unmodifiable boot-time hardware snapshot. It does not prove the user's identity, and Apple states it cannot guarantee the device is not jailbroken.

**Why attest once but assert many times?**
Attestation contacts Apple's servers; assertions are generated locally with no round trip. So you register the key once and assert per protected request. Assertions still perform cryptographic work, so avoid generating them in tight loops or hot lifecycle paths.

**What is the one server-side check people forget in App Attest?**
The assertion counter. Track it per key and require it to be strictly increasing. Without that, assertions are replayable and you have built a signature check that does not stop the attack it exists to prevent.

**A returning user's device produces a brand-new App Attest key. Fraud?**
Usually not. Reinstalls and device migrations legitimately generate new keys, and Apple's 2026 guidance is explicit: do not reject every new key for an existing user. Handle it as a re-registration event with appropriate risk scoring.

**How should I handle DCError.invalidKey?**
Discard the key, generate a new one, retry — with a cap and backoff. For `serverUnavailable`, retry with the *same* key and client data hash. Be aware that a small subset of devices report persistent `invalidKey` that survives reinstall and reboot, and Apple has not confirmed whether throttling can surface that way. Design a grace mode rather than locking those users out.

**What is new in App Attest for 2026?**
A fraud metric to feed into your risk pipeline, new signals in iOS 27, App Attest on macOS 27, and the explicit guidance about not rejecting new keys for existing users. WWDC26 Session 201.

## Biometrics

**How do you implement biometrics so they cannot be bypassed?**
Tie the prompt to a cryptographic operation. On Android, `BiometricPrompt` with a `CryptoObject` backed by a key created with `setUserAuthenticationRequired`; then sign or decrypt something your server verifies. On iOS, `LocalAuthentication` with a Secure Enclave key whose access control requires biometry. If you only branch on a boolean callback, an attacker hooks it and returns true.

**Why does Class 3 matter?**
Class 3 (`BIOMETRIC_STRONG`) is the only Android tier strong enough to gate cryptographic operations, meaning the only tier that can back a `CryptoObject`. Class 2 accepts weaker modalities and cannot. Accepting Class 2 for a payment means accepting a modality the platform itself considers insufficient to protect a key.

**An attacker steals an unlocked phone and adds their fingerprint. What stops them?**
Key invalidation on enrollment change: `setInvalidatedByBiometricEnrollment(true)` on Android, `kSecAccessControlBiometryCurrentSet` rather than `biometryAny` on iOS. Apple documents that access can be limited to require that enrolment has not changed since the item was added, for exactly this reason. MASWE-0022, and one of the most commonly missed items in the catalogue. The cost is that legitimate re-enrolment forces re-registration in your app — for a banking app, the right trade.

**How do you provide a fallback without creating a bypass?**
Make the fallback equivalent in strength, not weaker. Device credential fallback that still unlocks a hardware key is fine; server-side step-up is fine. A fallback that sets `authenticated = true` is the vulnerability with a friendlier label. MASWE-0021 names the failure.

**When should you not require biometrics?**
On every cold start, for browsing, or for anything users do dozens of times daily. Friction that does not buy security gets routed around: users disable the feature or abandon the flow, which leaves you less secure than before. This is a security argument, not a UX concession.

## Backend

**What is the one test for any authenticated endpoint?**
If an attacker replays a valid request from a different device, what stops them? If the answer is nothing, that is your next piece of work. Token binding, attestation assertions, and nonce or counter checks are the three mechanisms that answer it.

**Why build a risk score instead of just allowing or blocking?**
Because a single binary signal is a single point of failure — when it is defeated you have nothing, and Chapter 5 showed attestation can be defeated. A score degrades gracefully. It also gives you proportionate responses: allow silently, allow with step-up, allow with a lower limit, flag for review, queue, refuse. Most fraud is better handled in the middle, where you impose cost on the attacker without punishing false positives.

**What should never be trusted from the client?**
Identity claims, prices, quantities, entitlements, balances, permissions, discounts and limits. Derive the acting user from the session token, never from a body field.

## Pipeline

**Why pin GitHub Actions to a commit SHA rather than a tag?**
Tags are mutable, SHAs are not. Force-pushing a tag to malicious code is exactly how `tj-actions/changed-files` and `aquasecurity/trivy-action` were compromised, both exfiltrating runner secrets. Pin to the full-length SHA with the version in a trailing comment, automate updates with Dependabot, and add a cooldown so you do not adopt a bad release immediately.

**Your CI has a stored AWS key. What replaces it, and why?**
OIDC. A stored key is valid indefinitely and portable the moment it leaks; an OIDC token is minted per workflow run, scoped to that job, and expires in minutes — so compromising the workflow yields a credential that is nearly worthless by the time it is exfiltrated. AWS, Azure and GCP all support it natively.

**What is wrong with `pull_request_target`?**
It runs with repository secrets in scope against fork code. That is the vector in the May 2026 TanStack attack: an attacker poisoned the pnpm cache through such a workflow, and the legitimate release workflow consumed it eight hours later, pulled OIDC tokens from runner memory, and published 84 malicious versions across 42 packages. If you must use it, never check out or execute fork code in the same job that holds secrets.

**Someone says "we have SLSA Build Level 3 provenance, so our supply chain is verified." Respond.**
Provenance attests to *how* an artifact was built, not that the inputs were clean. In the TanStack attack the malicious packages carried valid, signed SLSA Build Level 3 provenance and verification tools reported them clean, because the poisoned input arrived through a cache rather than a dependency change. Provenance closes the substitution attack; it does nothing about a compromised input. Caches remain a trust boundary.

**An attacker steals your Android upload key. How bad is it?**
Recoverable, with Play App Signing. Google holds the app signing key and re-signs on upload, so a stolen upload key cannot be used to ship code under your identity — you register a new upload key. Without Play App Signing, a stolen signing key is close to unrecoverable. This is the strongest argument for the split key model.

**How do you get a keystore into CI safely?**
Base64-encode it into the CI secret store, or GPG-encrypt it in the repository with the passphrase in the secret store; decode at build time to a path you delete afterwards. Never commit `key.properties` or a `gradle.properties` with passwords — that has the same blast radius as a leaked server key. And fail the build when release signing is missing rather than silently emitting a debug-signed artifact.

**A production API key was committed six months ago. First move?**
Rotate the credential. Not remove the commit — rotate. Assume harvest within minutes; 64% of secrets validated in 2022 are still active, which tells you how rarely this happens. Then purge history, add scanning, and check access logs for use of the old key.

**What is script injection in a workflow?**
Attacker-controlled text such as a PR title, issue body, branch name or commit message, interpolated directly into a `run:` block where it executes as shell. Pass untrusted values through `env:` and quote them; never inline `${{ github.event.* }}` into a shell step.

**Two monitoring alerts that would have caught real 2025–26 attacks?**
New self-hosted runner registrations and new public repository creation in your organisation. In Shai-Hulud, compromised machines registered as runners named `SHA1HULUD` and stolen credentials created public repos as exfiltration buckets.

**Does AI-assisted coding change your secrets posture?**
Measurably. AI-assisted commits on public GitHub leak secrets at about 3.2% versus a 1.5% human-only baseline, eight of the ten fastest-growing leak categories are tied to AI services, and MCP configuration files alone exposed 24,008 unique secrets — partly because official documentation encouraged hardcoding. Commit-time scanning becomes load-bearing rather than optional.

**Where do secrets leak from now?**
Increasingly not from developer laptops. In one analysed supply-chain attack, 59% of compromised machines were CI/CD runners, and about 28% of secret incidents originate outside code repositories entirely, in Slack, Jira and Confluence, where they were 13 percentage points more likely to be rated critical.

**Why lock dependencies and enable Gradle dependency verification?**
An unlocked build silently resolves a different version a month later and nobody notices. Verification with checksums makes a swapped artifact fail the build rather than ship. Both are cheap and both close the class of attack that requires no code change to review.

## AI features

**You are adding an LLM assistant to a banking app. First three security questions?**
One: if the user can influence the prompt, what can the prompt influence — especially if the model has tool access? Treat model output as untrusted input, exactly as you treat WebView content. Two: what user data leaves the device, and does that break a commitment we made to a regulator? Three: where does the model key live, and what stops a script from spending our inference budget?

**Why is prompt injection a mobile problem rather than just a backend one?**
Because the mobile client is where untrusted content enters: the camera, the share sheet, the clipboard, a WebView, the file picker. If that content reaches a model with tool access, you have a new execution path that your input validation, designed for form fields, was never built to catch. Indirect injection arrives in what the model reads, not in what the user typed.

**What is the strongest business case for attestation on an AI feature?**
That an attacker does not need to steal any data to hurt you. An unattested endpoint behind a metered model is a billing incident waiting to happen; they only need to spend your inference budget. That framing lands with finance in a way "defence in depth" does not.

**Is evaluation a security concern?**
Yes. Without an eval set you cannot tell whether a prompt change, a retrieval change, or a model version bump broke a behaviour you were treating as a control. Evaluation is usually framed as quality practice; it is also regression detection for safety properties.

## Kotlin Multiplatform

**What security code can you share in KMP, and what cannot you?**
Share interfaces, encryption utilities behind `expect`/`actual`, header and nonce construction, input validation, and risk-signal models. Keep native: Keystore and Keychain access, `BiometricPrompt` and `LocalAuthentication`, Play Integrity and App Attest, and network security configuration. The rule that generalises: anything whose security derives from platform hardware or a vendor attestation service cannot be abstracted without losing the property that made it valuable.

**What is the most common KMP security mistake?**
Defining `expect` declarations around mechanism instead of intent. `expect fun getKeystoreKey()` leaks Android assumptions into shared code and will not map onto the Secure Enclave, which supports elliptic curves only and does not do direct encryption. `expect suspend fun storeToken(token, requiringUserAuth)` describes intent and implements cleanly on both platforms.

**What gets missed in review on a KMP codebase?**
The `actual` implementations. Shared code is read by everyone; platform-specific code is often read by one person. The iOS `actual` that loosened a Keychain accessibility class to fix a background bug survives because the Android reviewers never opened that file.

## Judgement

**You have two weeks and one engineer. What comes first?**
Audit for hardcoded secrets and rotate anything exposed — the highest ratio of risk removed to effort spent. Then move tokens into Keystore or Keychain-backed storage. Then enforce TLS configuration and strip release logging. Attestation, biometrics and tamper detection come after; they are more work and they matter less while a live credential sits in your repository.

**Your product manager wants "bank-level security." What do you ask?**
What data are we handling, which regulator cares, and what is the actual threat — account takeover, payment fraud, data exfiltration, or cloning? "Bank-level" is not a specification. The MAS-L1 versus MAS-L2 versus MAS-R distinction turns that into something you can build against.

**How do you justify security work to a finance stakeholder?**
Compare prevention cost to incident cost using current figures — $4.99M global average and $11.5M in the US in the 2026 IBM report, 247 days mean time to identify and contain — then scope your *own* exposure honestly, because most mobile incidents cost far less than an enterprise average. Overstating it costs you credibility on every future request.

**What is the most over-engineered control you see, and the most under-engineered?**
Over: elaborate client-side root detection with hard local blocks, which is trivially removed and generates support load. Under: server-side validation of things the client sent, and token binding. The second pair is unglamorous and decides whether an attack works.

---
