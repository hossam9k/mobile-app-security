---
part: 02
last_verified: 2026-10-20
volatility: high
recheck_because: "datastore-tink is a release candidate (1.3.0-rc01), not yet stable; android/keyattestation (§5.5) is a pre-1.0 test release (v0.4, 13 Oct 2026) whose API may change (an app-identity check was added, reverted, and re-added upstream on 24–25 Sep 2026); attestation root moved to ECDSA P-384 (from February 2026; an April cut-over date is practitioner-reported) and chains begin a post-quantum migration from Android 17; Keystore gained ML-DSA in Android 17"
---

# Part 2: Data at rest

## Chapter 4: How platform key storage actually works

A security reviewer asks one question about your token storage: *"If someone roots this phone, can they take the key off it?"* You answer "it's in the Keystore". That's the start of an answer, not the answer. Whether an attacker can copy the key, only use it, or read it in plain text depends on hardware you never see and flags you may never have set.

This chapter explains the mechanism underneath. Once you can draw it, you can answer the reviewer's question for any device.

### 4.1 The Android Keystore, from the top down

Start with the short version. Your app never holds a hardware-backed key: it holds a **handle** (an alias) that names the key. The key itself lives in secure hardware that Android can't read. Each time you use the key, that hardware checks the conditions you attached to it (an unlocked device, a recent fingerprint) and only then does the work, handing back the result and never the key.

The diagram shows the layers a request passes through. You don't need every name in it to use the Keystore well; the subsection after it explains them for when you do.

```mermaid
flowchart TB
    A["<small>YOUR APP PROCESS</small><br/>Your Kotlin code"]:::app
    B["<small>YOUR APP PROCESS</small><br/>AndroidKeyStore JCA provider"]:::app
    C["<small>ANDROID OS</small><br/>keystore2 daemon, stores encrypted keyblobs"]:::os
    D["<small>ANDROID OS</small><br/>KeyMint HAL (IKeyMintDevice)"]:::os
    E["<small>SECURE HARDWARE</small><br/>KeyMint TA in the TEE<br/>e.g. Trusty on TrustZone"]:::hw
    F["<small>SECURE HARDWARE</small><br/>StrongBox KeyMint<br/>separate chip, e.g. Titan M"]:::hw
    G["<small>SECURE HARDWARE</small><br/>Gatekeeper and biometric TAs"]:::hw
    A --> B
    B -->|"Binder: key alias + data"| C
    C --> D
    D --> E
    D --> F
    G -.->|"signed hardware auth token"| E
    classDef ext fill:#FDECEC,stroke:#B83232,color:#1B1F23
    classDef app fill:#EEF3FB,stroke:#2F5597,color:#1B1F23
    classDef os fill:#F1F3F5,stroke:#5F6B7A,color:#1B1F23
    classDef hw fill:#FFF6E5,stroke:#C08A1E,color:#1B1F23
    classDef srv fill:#EAF6EE,stroke:#2E7D4F,color:#1B1F23
```

*Figure 5: The Android Keystore stack: your process holds a handle, the key stays in secure hardware*

#### Under the hood

Skip this on a first read; come back when a reviewer asks where the key is.

The `AndroidKeyStore` you call from Kotlin is a Java Cryptography Architecture (JCA) provider: a plug-in behind the standard `KeyStore`, `Cipher`, and `Signature` classes. It runs **inside your app's own process**, and it doesn't hold your keys. It forwards each request over Binder (Android's inter-process call mechanism) to a system daemon.

That daemon is **keystore2**, introduced in Android 12 and written in Rust. Rust matters here because it rules out most memory-safety bugs at compile time, and in key-handling code one such bug could expose every key on the device. keystore2 stores **keyblobs**: your key material, encrypted by the secure hardware so that the daemon can store it but **can't use or reveal it**. That property is the foundation of the design.

Below the daemon sits a hardware abstraction layer (HAL: the interface Android uses to talk to vendor hardware) implementing `IKeyMintDevice`. **KeyMint** is the current HAL. It replaced the older **Keymaster** in Android 12, and KeyMint 2 (Android 13) added Curve25519 for signing and key agreement. Behind the HAL runs the **KeyMint trusted application (TA)**: software in a **trusted execution environment** (TEE, §4.2), most often ARM TrustZone, the processor's hardware-isolated "secure world". The TA is the only component that ever sees raw key material. It checks every access condition on the key, and only then performs the operation.

So when your code "encrypts with a Keystore key", this is what physically happens:

1. Your process sends the plaintext and the key alias to keystore2.
2. keystore2 passes the encrypted keyblob and the request to the TA.
3. The TA decrypts the keyblob inside secure hardware and checks the key's **authorizations** (the conditions of use you attached to it, §4.6).
4. The TA performs the operation and returns only the result.

**For a hardware-backed key, the key material never enters your process and never enters Android itself.** For a `SOFTWARE` key (§4.2), the key material lives in the OS, and the OS is all that protects it.

One more component matters. **Gatekeeper** is the TA that verifies the user's PIN, pattern, or password. Fingerprint and face checks go through the biometric HAL and their own TAs instead. On success, each one issues a signed **hardware auth token**, which KeyMint verifies before it uses an **authentication-bound key** (a key usable only after the user has authenticated). Despite the name, a hardware auth token has nothing to do with the OAuth access and refresh tokens of Chapter 0.3: it's a short-lived message between secure components that never reaches your code. This machinery is why Chapter 11's biometric binding is enforced by hardware, not only by your UI.

The algorithm list keeps growing. Android 17 added **ML-DSA** (a post-quantum signature scheme standardized by NIST) to the Keystore, on devices whose hardware supports it ([Android 17 Beta 4](https://android-developers.googleblog.com/2026/04/the-fourth-beta-of-android-17.html)).

- <https://source.android.com/docs/security/features/keystore>
- <https://developer.android.com/privacy-and-security/keystore>

### 4.2 TEE versus StrongBox, and why the difference is real

Every Keystore key has a **security level**, and you can query it. On API 31 and later, `KeyInfo.getSecurityLevel()` returns one of five constants, all prefixed `KeyProperties.SECURITY_LEVEL_`. On API 30 and below, all you have is the boolean `KeyInfo.isInsideSecureHardware()`, deprecated since API 31.

| Constant | Where the key lives | Treat it as |
|---|---|---|
| `SOFTWARE` | In the Android OS | Extractable on a compromised device |
| `TRUSTED_ENVIRONMENT` | In the TEE on the main processor | Hardware-backed |
| `STRONGBOX` | In a separate secure chip | Hardware-backed, tamper-resistant |
| `UNKNOWN_SECURE` | Secure hardware of an unreported kind | Hardware-backed |
| `UNKNOWN` | Not reported | Unknown: don't assume hardware |

You'll mostly see the first three, and each deserves a closer look.

**`SOFTWARE`** means the OS is the only thing protecting the key. On a rooted or compromised device, treat the key as extractable. It's better than a key in your APK, but it isn't hardware protection.

**`TRUSTED_ENVIRONMENT`** means the key lives in the **TEE** (trusted execution environment): an isolated area of the *main* processor, separated from Android by hardware. If an attacker fully compromises Android, the TEE still keeps the key material out of reach. An attacker with root can ask the TEE to *use* your key on that device. They can't *copy* it off the device. Google's open-source TEE is **Trusty**; other TEEs exist, and Android supports them.

**`STRONGBOX`** means the key lives in a separate, purpose-built secure processor: an embedded Secure Element (a tamper-resistant chip) or an on-chip secure unit with its own CPU, storage, and random-number generator. Titan M in Pixel phones is the familiar example. StrongBox arrived in Android 9 (API 28). It resists physical tampering and side-channel attacks (attacks that infer a key from power use, timing, or electromagnetic emissions) better than a TEE.

Three practical consequences follow, and they are where designs go wrong.

**StrongBox is not universal.** The Android 17 compatibility definition still only says devices with a dedicated secure processor are "STRONGLY RECOMMENDED" to support it, and that it "will likely become a requirement in a future release" ([Android 17 CDD §9.11.2](https://source.android.com/docs/compatibility/17/android-17-cdd)). The wording hasn't changed from Android 16. Check `PackageManager.FEATURE_STRONGBOX_KEYSTORE`, request StrongBox, catch `StrongBoxUnavailableException`, and choose your fallback deliberately.

**StrongBox is slower and supports less.** Google's list is RSA-2048, AES-128 and AES-256, ECDSA and ECDH on P-256, HMAC-SHA256, and Triple DES. Google also warns that it's slower, has fewer resources, and handles fewer concurrent operations. Reserve it for keys that justify it. If you ask StrongBox for an algorithm or key size outside that list, key generation fails, even on devices whose TEE would have handled the request.

**Silent fallback is a finding, not a fallback.** Suppose your payment flow requests StrongBox, fails, and quietly settles for a software key without telling anyone. You now have a control that reports success while providing nothing. Either fall back to the TEE explicitly and record that you did, or require server-side step-up authentication (an extra check, such as a one-time code, before the risky action) for that flow on that device. Write down which. One question separates people who have shipped hardware-backed crypto from people who have only read about it: *what does your app do when StrongBox is unavailable?*

### 4.3 The iOS Keychain, from the top down

Apple's design has a different structure but follows the same principle: secure hardware guards the keys, and for a key generated in the Secure Enclave your app holds only a handle.

The Keychain is **a single SQLite database** on the file system, managed by the **securityd** daemon. All apps share that one database; no app gets its own. When your code calls a Keychain API, securityd decides what your process may see by reading your `keychain-access-groups`, `application-identifier`, and `application-group` entitlements. Only apps from the same developer can share items, and code signing and provisioning profiles enforce that.

iOS encrypts each item with **two AES-256-GCM keys**. A **metadata key** encrypts every attribute except the secret value, so securityd can search quickly. The Secure Enclave protects that key, but iOS caches it in the Application Processor (the main CPU) for speed. A **per-row secret key** encrypts `kSecValueData`, the secret itself, and using it **always requires a round trip through the Secure Enclave**.

This split explains the design. Search stays fast because metadata decryption is cheap, while nobody can read the secret itself without the hardware taking part.

The hardware takes part in decrypting the secret, but it doesn't keep it. Once the item's conditions are met, securityd returns the decrypted `kSecValueData` to your process, so code running inside your app at that moment can read it. Only a key generated *in* the Secure Enclave, described next, never enters your process (Chapter 0.4 makes the same distinction).

The **Secure Enclave** is a separate secure subsystem, present on A7 and later chips. It performs the cryptography for Data Protection key management and keeps Data Protection intact **even if an attacker compromises the kernel**. Private keys created in it never leave it in plain text; neither your process nor the kernel ever sees them. A `SecKey` in your Swift code is a *handle*, not the key.

Two constraints surprise people.

- **Algorithms are limited.** Through the Security framework, the Secure Enclave takes **NIST P-256 elliptic-curve keys only**. It doesn't support RSA. Since iOS 26, CryptoKit also offers post-quantum **ML-KEM** and **ML-DSA** keys inside it (`SecureEnclave.MLKEM768`, `SecureEnclave.MLDSA65` and their larger variants).
- **It doesn't encrypt your data directly.** Its keys are for signing and key agreement. To protect data with it, you perform ECDH (elliptic-curve Diffie-Hellman) key agreement, or ML-KEM encapsulation, and derive a symmetric key from the result. You don't call an encrypt function on an enclave key.

The Secure Enclave **evaluates the access control lists on Keychain items itself**, and releases the key only when their conditions are met. That's why a biometric-gated Keychain item is protected by hardware, not only by a UI prompt.

- <https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web>
- <https://developer.apple.com/documentation/security/protecting-keys-with-the-secure-enclave>

### 4.4 Data Protection classes: the decision you keep getting wrong

Every Keychain item carries an accessibility class, set with `kSecAttrAccessible`. Every file carries an analogous **Data Protection class**. Both decide *when* the decryption key is available.

| Keychain class | File class | Readable when | Use it for |
|---|---|---|---|
| `kSecAttrAccessibleWhenUnlocked` | `NSFileProtectionComplete` | Only while unlocked. The key is discarded about 10 seconds after lock (with Require Password set to Immediately) | Tokens and secrets used in the foreground. Your default |
| `kSecAttrAccessibleAfterFirstUnlock` | `NSFileProtectionCompleteUntilFirstUserAuthentication` | After the first unlock since boot, then even while locked | Items background refresh needs. Apple names this use case |
| `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` | — | Like "when unlocked", and only if a passcode is set | Your most sensitive items. They become unusable if the passcode is removed or reset |
| — | `NSFileProtectionCompleteUnlessOpen` | A file open at lock time stays usable; new files can still be written while locked | Downloads that must finish in the background |
| `kSecAttrAccessibleAlways` | `NSFileProtectionNone` | Always, even before first unlock | Nothing sensitive. The Keychain class is deprecated since iOS 12; the file class is not deprecated, but it protects nothing |

Know two defaults. **Files your app creates default to `CompleteUntilFirstUserAuthentication`**, not `Complete`, so a file you never thought about is readable on a locked phone. And Apple names the replacement for `Always` in its deprecation note: use `AfterFirstUnlock`.

If you append **`ThisDeviceOnly`** to a Keychain class, the item never migrates to another device. iOS still copies it into a device backup, but encrypts it with a key fused into that device's hardware, so it's useless if restored anywhere else. It also never syncs to iCloud Keychain. The `WhenPasscodeSetThisDeviceOnly` class goes further: iOS doesn't back it up at all.

The same failure keeps recurring. Background refresh breaks because an item is `WhenUnlockedThisDeviceOnly`. The symptom is `errSecInteractionNotAllowed` (-25308) from `SecItemCopyMatching` while the phone is locked. Someone "fixes" it by switching to `kSecAttrAccessibleAlways`, and drops `ThisDeviceOnly` at the same time. Now a token that needed an unlocked device is readable before the user has ever unlocked it, and it migrates to new devices too.

> **Trap:** the right fix is almost always to restructure *when* the work happens, not to weaken the class. If background refresh needs a credential, `AfterFirstUnlockThisDeviceOnly` is the considered answer, never `Always`.

This risk is real. The checkm8 bootrom exploit affects A5 to A11 devices (up to the iPhone X), and Apple can't patch it in software because the bootrom is read-only. Forensic tools built on it can extract data from a locked phone before first unlock. Without the passcode, the only Keychain items they recover are the `Always` and `AlwaysThisDeviceOnly` ones ([Elcomsoft](https://blog.elcomsoft.com/2019/12/bfu-extraction-forensic-analysis-of-locked-and-disabled-iphones/)) *(reported)*. The class is the difference between "recovered" and "not recovered". Data Protection makes extraction much harder. It doesn't stop an attacker who has your device, the right exploit, and, eventually, the passcode.

### 4.5 A note on sharing

On Android, keys are per-app by default, and the Keystore's isolation is strong. Android 16 added a deliberate exception: `KeyStoreManager.grantKeyAccess()` lets your app grant another app, identified by its UID (the Linux user ID Android assigns to each app), the use of one specific key until you revoke it. Treat each grant as a trust decision you record, as you would a Keychain access group (below). See the [`KeyStoreManager` reference](https://developer.android.com/reference/android/security/keystore/KeyStoreManager).

On iOS, adding another app to your `keychain-access-groups` entitlement means **trusting that app completely**. Anything in the group can call `SecItemCopyMatching` on your items, including a compromised app under your own Team ID. The same applies to App Group containers you share with extensions. Access groups are useful, and every member adds risk. List what's in yours.

### 4.6 Key authorizations: the conditions the hardware enforces

A key's protection depends not only on *where* it lives but on *when* it may be used. You set those conditions once, at creation, and the secure hardware enforces them from then on. Nothing your app does later can relax them, and neither can a Frida hook (Frida is a tool that rewrites an app's code while it runs).

On Android you set them on `KeyGenParameterSpec.Builder`:

| Setter (API level) | What the hardware enforces | Watch out for |
|---|---|---|
| `setUserAuthenticationRequired(true)` (23) | The key works only after the user authenticates | Needs a secure lock screen. Removing the lock screen permanently invalidates the key |
| `setUserAuthenticationParameters(timeout, type)` (30) | `timeout` 0 means authenticate for every use, via `BiometricPrompt` with a `CryptoObject`; above 0 means a window in seconds. `type` is `AUTH_BIOMETRIC_STRONG`, `AUTH_DEVICE_CREDENTIAL` or both | Replaces the deprecated `setUserAuthenticationValidityDurationSeconds` |
| `setInvalidatedByBiometricEnrollment(…)` (24) | Defaults to `true`: enrolling a new biometric destroys the key | Stops applying if the key also accepts the device credential or has a validity window. §11.3 |
| `setUnlockedDeviceRequired(true)` (28) | Symmetric and private-key operations fail while the device is locked | Public-key operations are never restricted; before API 31, symmetric encryption and verification weren't either. Background work breaks, as it does with iOS `WhenUnlocked` |
| `setIsStrongBoxBacked(true)` (28) | Generate the key in StrongBox or fail | §4.2's fallback decision |

On iOS, the equivalent is a `SecAccessControl` object passed as `kSecAttrAccessControl`, combining an accessibility class from §4.4 with flags:

| Flag | Meaning |
|---|---|
| `.biometryCurrentSet` | Face ID or Touch ID, **and** the enrolled set must not have changed since the item was created. The stolen-phone defense of §11.3 |
| `.biometryAny` | Any enrolled biometric, including one enrolled yesterday by a thief |
| `.userPresence` | Biometry or the device passcode |
| `.devicePasscode` | The passcode only |
| `.privateKeyUsage` | Required for a Secure Enclave private key to sign at all |
| `.or`, `.and` | Combine the constraints above |

The pattern is the same on both platforms. **Authorization lives in the key, not in your `if` statement.** Chapter 11 builds biometric flows on this mechanism.

### 4.7 The two platforms side by side

The mechanisms differ; the questions you ask of them don't. Use this table when you design a feature for both platforms, or when a reviewer asks how the Android and iOS halves compare.

| | Android Keystore | iOS Keychain and Secure Enclave |
|---|---|---|
| Hardware | TEE on the main processor (all modern devices); StrongBox secure chip on some (§4.2) | Secure Enclave on A7 and later; Keychain item keys also depend on it (§4.3) |
| Algorithms in hardware | AES, HMAC, RSA, EC (P-256 and others), Curve25519 from KeyMint 2, ML-DSA from Android 17 where supported; StrongBox narrower | Security framework: P-256 only. CryptoKit from iOS 26: ML-KEM and ML-DSA as well |
| Encrypt data directly with the hardware key? | Yes: an AES key does `Cipher` work in the TEE | No: derive a symmetric key by ECDH or ML-KEM (§4.3) |
| Biometric binding API | `setUserAuthenticationParameters` plus `BiometricPrompt` with a `CryptoObject` (§4.6, Chapter 11) | `SecAccessControl` with `.biometryCurrentSet` (§4.6, Chapter 11) |
| New biometric enrolled | Key destroyed by default (`setInvalidatedByBiometricEnrollment`) | Item unusable with `.biometryCurrentSet`; survives with `.biometryAny` |
| Backup behavior | Keys are never backed up; restored ciphertext cannot decrypt (§6.5) | Items are backed up; a `ThisDeviceOnly` item restores only to the same device, and `WhenPasscodeSetThisDeviceOnly` is not backed up at all (§4.4) |
| Sharing with other apps | Per-app; `KeyStoreManager.grantKeyAccess()` from Android 16 (§4.5) | Keychain access groups within one Team ID (§4.5) |
| Query what you got | `KeyInfo.getSecurityLevel()` (§4.2); key attestation for your server (Chapter 5) | No per-key security-level query; check `SecureEnclave.isAvailable` (CryptoKit) before creating a key, and a Secure Enclave key fails to create if the hardware is absent. App Attest for your server (Chapter 10) |

**Key takeaways**

- The Keystore and the Secure Enclave hand your process a *handle*; an ordinary Keychain item returns the secret itself once its conditions are met. For hardware-backed keys, the key material never reaches your code or the OS.
- Query the security level you got. `SOFTWARE` on a flow designed for hardware is a finding.
- StrongBox is optional, slower, and narrower than the TEE. Decide and record your fallback.
- On iOS, the accessibility class decides when a secret is readable. `Always` is deprecated and is exactly what forensic tools recover.
- Put conditions of use in the key's authorizations, where the hardware enforces them.

**Try it**

1. On one physical Android phone and one emulator, generate an AES key with `setIsStrongBoxBacked(true)`, catch `StrongBoxUnavailableException`, retry without it, and log `KeyInfo.securityLevel` (§6.6 has the code). Explain the difference you see.
2. In an iOS test app, store an item as `WhenUnlockedThisDeviceOnly`. Lock the phone, trigger a background task that reads it, and confirm you get `-25308`. Then decide, in writing, whether that task should move to the foreground or the item should become `AfterFirstUnlockThisDeviceOnly`.

---

## Chapter 5: Key attestation — proving where a key lives

In February 2026, Google's key attestation began moving to a new root certificate. By April, most modern Android phones were presenting attestation chains that older server code rejected *(reported)*. The apps themselves hadn't changed. Their backends had hard-coded an assumption that Google had warned about four years earlier.

The Keystore protects your key. **Attestation** lets your *server* verify that protection for itself, which is a different and more valuable thing. Its details also keep changing, and this chapter shows you which ones.

### 5.1 The problem it solves

Your app tells your backend, "I generated this key in hardware." Why would the backend believe it? A rooted device, an emulator, or a modified build can claim anything. Key attestation is the cryptographic answer to that question.

Key attestation arrived in Android 7.0 with Keymaster 2. ID attestation, which can also vouch for hardware identifiers, followed in Android 8.0 with Keymaster 3.

### 5.2 How it works

Learn this flow well. Every attestation protocol you'll meet has the same shape, App Attest included (Chapter 10):

```mermaid
sequenceDiagram
    participant S as Your server
    participant A as Your app
    participant K as KeyMint in secure hardware
    S->>A: fresh random challenge
    A->>K: generate key with setAttestationChallenge(challenge)
    K-->>A: certificate chain, leaf signed inside the hardware
    A->>S: certificate chain
    Note over S: verify chain to a Google root, check revocation
    Note over S: check challenge, security levels, boot state, app identity
    S-->>A: accept, or ask for step-up
```

*Figure 6: Key attestation: the server's challenge comes back inside a certificate chain signed by the hardware*

1. Your **server** generates a random, single-use challenge (a nonce) and sends it to the app.
2. The **app** generates a key pair in the `AndroidKeyStore`, passing the challenge to `setAttestationChallenge()`.
3. **KeyMint, inside the secure hardware, signs a certificate for the new public key** using an attestation key. The leaf certificate carries a `KeyDescription` extension, identified by the OID `1.3.6.1.4.1.11129.2.1.17` (an OID, or object identifier, is the dotted number that names a certificate extension). It records the security level of the key and of the attestation, the boot state, the key's authorizations, and your challenge.
4. The app reads the chain with `KeyStore.getCertificateChain(alias)` and sends it to your server.
5. Your **server** verifies the chain up to a Google attestation root, checks every certificate against Google's revocation list, confirms the challenge is the one it issued, and reads the properties.

The crucial detail is where the information comes from. Code in the secure hardware **collects or generates the hardware-enforced authorization list, and the platform doesn't control it**: the data comes from the bootloader, or over a channel that doesn't require trusting Android. The OS can't forge those claims, because the OS was never asked.

That is also the limit. The `KeyDescription` carries a `softwareEnforced` list alongside `hardwareEnforced`. Anything in the software list is only as trustworthy as the Android that wrote it. Read each field from the list you expect it in.

What a server should check, at minimum:

| Check | Why |
|---|---|
| Chain verifies to one of Google's current roots | Otherwise anyone can mint a chain |
| No certificate appears in the [revocation list](https://android.googleapis.com/attestation/status) | Leaked attestation keys are revoked there |
| `attestationChallenge` equals the challenge you issued, used once | Stops replay of an old, genuine chain |
| `attestationSecurityLevel` and `keyMintSecurityLevel` are `TrustedEnvironment` or `StrongBox` | The whole point of the exercise |
| `RootOfTrust.verifiedBootState` is `Verified` and `deviceLocked` is true | An unlocked bootloader means the OS can lie |
| `attestationApplicationId` matches your package name and signing-certificate digest | Stops a genuine chain from another app being passed off as yours |
| The client later signs a fresh challenge with the attested private key | Forces the attacker to hold the key, or keep a live signing proxy to a device that does |

Don't write this parser yourself. Google publishes a [Kotlin verification library](https://github.com/android/keyattestation) and recommends migrating custom verifiers to it. §5.5 shows it in use.

- <https://source.android.com/docs/security/features/keystore/attestation>
- <https://developer.android.com/privacy-and-security/security-key-attestation>

### 5.3 The thing that will break your production app in 2026

Manufacturers used to inject attestation keys into each device at the factory. Google moved to **Remote Key Provisioning (RKP)**, which delivers short-lived attestation keys over the network instead. RKP was optional from Android 12. Google announced in 2022 that it would be mandatory from Android 13, though its attestation page now describes RKP support as optional under the Android 15 policy. For devices launching with Android 16, it's the only mechanism. RKP improves privacy substantially. Each app receives a different attestation key, keys rotate regularly, and Google splits its backend so that the server verifying a device's public key never sees the attestation keys attached to it. Google can't correlate attestation keys back to a device ([Android Developers Blog, 2022](https://android-developers.googleblog.com/2022/03/upgrading-android-attestation-remote.html)).

It improves revocation too. A leaked factory key compromised every device that shared it. Google can revoke an RKP key for a single device.

The operational consequence arrived this year. Google's attestation documentation announced that a new **ECDSA P-384 root** (certificate common name `Key Attestation CA1`) would "begin signing attestation certificate chains on February 1, 2026" ([Google](https://developer.android.com/privacy-and-security/security-key-attestation)). RKP-enabled devices switched to it exclusively on **10 April 2026** *(reported)*. From that date, a verifier that trusts only the old RSA root rejects chains from most modern Android phones. Devices with factory-provisioned keys keep using the RSA root, so you must trust **both**.

None of this was a surprise. When Google introduced RKP in 2022, it warned that "the chain length is longer than it was previously, and is subject to change", and that the root "will eventually be updated from the current RSA key to an ECDSA key".

The migration isn't over. Android 17 "begins the transition of Remote Attestation to a fully PQC-compliant architecture", moving KeyMint's certificate chains to post-quantum algorithms ([Google, March 2026](https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/)). Google hasn't published a date for a post-quantum root.

> **Trap:** hard-coding the root certificate, the chain length, or the signature algorithm in your verifier. All three have changed or are changing. Load the roots from Google's published list, accept any chain length, and verify with a library that supports every algorithm Google announces.

The revocation list lives at the same URL it always has (`https://android.googleapis.com/attestation/status`). It is JSON: an `entries` object keyed by certificate serial number in lowercase hex. Each entry carries a `status` of `REVOKED` or `SUSPENDED`, an optional `reason` such as `KEY_COMPROMISE` or `SOFTWARE_FLAW`, and an optional expiry date. Honor its `Cache-Control` header (the HTTP header that says how long you may cache the response) rather than fetching it once at deploy time.

### 5.4 What attestation does not prove

Attestation has two limits.

It proves properties of a **key**, not the trustworthiness of a **user**. A fraudster holding a genuine device still produces a valid attested key.

The mechanism is also a target. Tools such as [**TEESimulator**](https://github.com/JingMatrix/TEESimulator) defeat hardware-backed key attestation for selected apps. They run the reference KeyMint TA from AOSP (the Android Open Source Project) inside the real keystore daemon, and sign attestations with a supplied (in practice, leaked) factory "keybox": an attestation key and its certificates. The resulting certificates are built the same way real hardware builds them, so they're internally consistent. Researchers have also shown **relay attacks**: the attacker obtains a genuine chain on a clean phone and splices it into an app running on a rooted one ([Quarkslab, August 2026](https://blog.quarkslab.com/bypassing-android-hardware-attestation.html)).

Both attacks leave marks a good verifier can use. A leaked keybox ends up on the revocation list once Google detects it; until then it works. RKP devices never had a factory keybox to leak. A chain relayed from another app fails the `attestationApplicationId` check; Quarkslab added that one comparison and it rejected their relayed chain. A same-app relay must then answer §5.2's proof-of-possession challenge by relaying every signature to the clean phone as well. That's a live proxy, costly and fragile, but proof of possession doesn't stop it; Quarkslab proposes that check without having tested it against their relay. Attestation makes these attacks much more expensive, but it doesn't stop them, and a design that treats one attestation result as the final word fails as soon as that one check is fooled. Feed it into a risk score alongside other signals; §12.2 and §12.5 cover how.

### 5.5 How to implement it

The table in §5.2 is your specification. This section turns it into server code: Kotlin on the JVM, using Google's [android/keyattestation](https://github.com/android/keyattestation) library for the parts you shouldn't write yourself (chain validation, revocation, and extension parsing).

> **In practice:** the library's latest tag is **v0.4 (13 October 2026), which its own release notes call a "test release"**. Since 16 October 2026 it's on Google's Maven repository as `com.android.keyattestation:keyattestation:0.4` (not Maven Central), so add `google()` to your server build's repositories and pin that exact version. I read the API below from the v0.4 source on 20 October 2026. It may change before 1.0, and it's already moving: an app-identity check (an `expectedAttestationApplicationId` constructor parameter) was added and reverted upstream on 24 September 2026, then landed again the next day. The code below uses it. The README's example still doesn't compile against the source (it passes a `ConstraintConfig` where the constructor expects the app identity), so trust the source over the README.

#### The app side: generate the key and send the chain

```kotlin
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import java.security.KeyPairGenerator
import java.security.KeyStore
import java.security.spec.ECGenParameterSpec

/** Returns the attestation chain, leaf first, as Base64 DER strings for your API. */
fun attestedKeyChain(alias: String, serverChallenge: ByteArray): List<String> {
    val spec = KeyGenParameterSpec.Builder(alias, KeyProperties.PURPOSE_SIGN)
        .setAlgorithmParameterSpec(ECGenParameterSpec("secp256r1"))
        .setDigests(KeyProperties.DIGEST_SHA256)
        .setAttestationChallenge(serverChallenge)      // the server's one-time nonce
        .build()
    KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_EC, "AndroidKeyStore")
        .apply { initialize(spec) }
        .generateKeyPair()
    val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
    return keyStore.getCertificateChain(alias).map {
        Base64.encodeToString(it.encoded, Base64.NO_WRAP)
    }
}
```

#### The server side: verify, then check what the library leaves to you

The library validates the chain against both Google roots. Its `GoogleTrustAnchors` object is generated from a mirror of `https://android.googleapis.com/attestation/root`, which holds the 2022 RSA-4096 root and the P-384 root `Key Attestation CA1`. It checks every serial against the revocation list and parses the `KeyDescription`. Its parser treats only `REVOKED` entries as revoked; if you want `SUSPENDED` keys rejected too, supply your own `revokedSerialsSource`. Its default constraints require the attestation and KeyMint security levels to match and not be `SOFTWARE`, and reject an imported rather than generated key and a missing root of trust. The code below still checks the security level itself, so a relaxed `ConstraintConfig` or a change to the pre-1.0 defaults can't quietly accept a software key. Since v0.3 the library also checks your app identity, but only if you give it the expected identity; without one, it accepts any app. Its default for that check, `ALLOW_UNKNOWN_PACKAGE`, also accepts a chain whose identity reads `UnknownPackage` on older OS versions, so the code below selects `STRICT`. It **returns** the boot state without enforcing it. That check is yours.

```kotlin
import com.android.keyattestation.verifier.AttestationApplicationId
import com.android.keyattestation.verifier.AttestationApplicationIdConstraint
import com.android.keyattestation.verifier.AttestationPackageInfo
import com.android.keyattestation.verifier.ChallengeChecker
import com.android.keyattestation.verifier.ConstraintConfig
import com.android.keyattestation.verifier.GoogleTrustAnchors
import com.android.keyattestation.verifier.SecurityLevel
import com.android.keyattestation.verifier.VerificationResult
import com.android.keyattestation.verifier.VerifiedBootState
import com.android.keyattestation.verifier.Verifier
import com.android.keyattestation.verifier.getGoogleRevocationStatusFromWeb
import com.google.common.util.concurrent.Futures
import com.google.common.util.concurrent.ListenableFuture
import com.google.protobuf.ByteString
import java.math.BigInteger
import java.security.PublicKey
import java.security.Signature
import java.security.SignatureException
import java.security.cert.X509Certificate
import java.time.Duration
import java.time.Instant

/** Your nonce store. consume() must atomically delete the entry and return true only once. */
interface ChallengeStore {
    fun consume(sessionId: String, challenge: ByteArray): Boolean
}

/** The challenge must be one you issued to this session, and unused. This stops replay. */
class OneTimeChallenge(
    private val store: ChallengeStore,
    private val sessionId: String,
) : ChallengeChecker {
    override fun checkChallenge(challenge: ByteString): ListenableFuture<Boolean> =
        Futures.immediateFuture(store.consume(sessionId, challenge.toByteArray()))
}

/** The library's fetcher downloads the list on every call. Cache it, and fail closed. */
object CachedRevocations : () -> Set<String> {
    private val maxAge = Duration.ofHours(1)   // simplification: honor Cache-Control in your own fetcher
    @Volatile private var serials: Set<String> = emptySet()
    @Volatile private var fetchedAt: Instant = Instant.EPOCH

    @Synchronized
    override fun invoke(): Set<String> {
        if (Duration.between(fetchedAt, Instant.now()) > maxAge) {
            serials = getGoogleRevocationStatusFromWeb()   // throws on failure: fail closed
            fetchedAt = Instant.now()
        }
        return serials
    }
}

/** Your app: package name, lowest accepted versionCode, SHA-256 of each signing certificate. */
val expectedAppId = AttestationApplicationId(
    packages = setOf(AttestationPackageInfo("com.example.app", BigInteger.ONE)),
    signatures = setOf(ByteString.copyFrom(YOUR_SIGNER_SHA256)),
)

/** STRICT: no exception for chains that report an unknown package. */
val strictAppId = ConstraintConfig(attestationApplicationId = AttestationApplicationIdConstraint.STRICT)

private val productionVerifier =
    Verifier(GoogleTrustAnchors, CachedRevocations, { Instant.now() }, expectedAppId, strictAppId)

sealed interface Attestation {
    data class Accepted(val publicKey: PublicKey, val strongBox: Boolean) : Attestation
    data class Rejected(val reason: String) : Attestation
}

fun verifyAttestation(
    chain: List<X509Certificate>,             // leaf first, as the app sent it
    sessionId: String,
    store: ChallengeStore,
    verifier: Verifier = productionVerifier,  // tests pass one with a pinned clock
): Attestation {
    val result = verifier.verify(chain, OneTimeChallenge(store, sessionId))
    if (result !is VerificationResult.Success) {
        // A wrong package or signer arrives as ConstraintViolation("Attestation application ID").
        val label = (result as? VerificationResult.ConstraintViolation)?.constraintLabel
        return Attestation.Rejected(label ?: result::class.simpleName ?: "unknown")
    }

    // The library reports boot state; it doesn't enforce it. keystore2 writes the app identity
    // into the software-enforced list, so that check is trustworthy only if this one passes too.
    if (result.verifiedBootState != VerifiedBootState.VERIFIED || !result.deviceLocked) {
        return Attestation.Rejected("boot=${result.verifiedBootState} locked=${result.deviceLocked}")
    }

    // §5.2 wants both levels in hardware. securityLevel is the lower of the two, so SOFTWARE
    // means at least one is in software. The default constraints catch this; don't rely on it.
    if (result.securityLevel == SecurityLevel.SOFTWARE) return Attestation.Rejected("securityLevel=SOFTWARE")

    return Attestation.Accepted(result.publicKey, result.securityLevel == SecurityLevel.STRONG_BOX)
}

/** Last row of §5.2's table: the client signs a second, fresh challenge with the attested key. */
fun provesPossession(publicKey: PublicKey, freshChallenge: ByteArray, signature: ByteArray): Boolean =
    try {
        Signature.getInstance("SHA256withECDSA").run {
            initVerify(publicKey)
            update(freshChallenge)
            verify(signature)
        }
    } catch (e: SignatureException) {
        false   // a malformed signature is a failed proof, not a server error
    }
```

Decode the app's Base64 strings with `CertificateFactory.getInstance("X.509")` before calling `verifyAttestation`. Issue the proof-of-possession challenge only after an `Accepted` result, and consume it once, like the first. The app signs it with `Signature.getInstance("SHA256withECDSA")` initialized with the Keystore private key. Store the public key against the account only after `provesPossession` returns `true`.

Three notes on this code. `result.securityLevel` is the lower of the attestation and KeyMint levels, so a `STRONG_BOX` result means both, and a `SOFTWARE` result means at least one is in software. The library accepts the chain if it carries *any* of your listed signer digests, and a package version at or above the one you list. If you have rotated your signing key with APK Signature Scheme v3, look at what your real chains carry before you decide which digests to list. `YOUR_SIGNER_SHA256` stands for that digest as bytes; the Play Console shows it as the app signing key certificate's SHA-256. And the app must not branch on `Rejected`: the server turns it into a risk decision (§12.2, §12.5).

If you can't adopt a pre-1.0 library, the manual route is the same list in the same order. Run a `java.security.cert` PKIX validation against both roots with the built-in revocation check switched off: Google's list is neither a CRL nor OCSP, the two standard revocation formats that Java's check understands. Look up every serial in the status JSON yourself. Then parse the extension with the ASN.1 schema on [source.android.com](https://source.android.com/docs/security/features/keystore/attestation#schema). That parse is where homemade verifiers go wrong, which is why Google recommends the library.

#### Verify it

Test the rejections, not only the happy path. Record a real chain from a test phone once, and keep it as a fixture along with the time you recorded it. RKP intermediates are short-lived and the `Verifier` checks certificate dates against its clock, so build the test verifier with that time pinned (`Verifier(GoogleTrustAnchors, CachedRevocations, { recordedAt }, expectedAppId, strictAppId)`) and pass it to `verifyAttestation`. Otherwise, once the intermediates expire, the replay test returns `PathValidationFailure` and never reaches the challenge check.

1. **Replay.** Submit the recorded chain a second time, or with a session whose challenge is already consumed. **Pass:** `Rejected("ChallengeMismatch")`. **Fail:** `Accepted`, which means your store's `consume` is not atomic or not single-use.
2. **Another app's leaf.** On the same device, generate an attested key in a second app you own (different package name or signing key), using a challenge your server issued to the same session you then submit it under (otherwise the challenge check fires first and you see `ChallengeMismatch`). **Pass:** `Rejected("Attestation application ID")`. **Fail:** `Accepted`, so the verifier isn't checking `attestationApplicationId`; confirm you passed `expectedAppId`.
3. **Emulator or unlocked bootloader.** Submit a chain from an emulator or from a test device with an unlocked bootloader. **Pass:** a rejection: `PathValidationFailure` for an emulator, whose chain ends in a software root, or the boot-state check for an unlocked device. Note which one fired, so you know what your server caught.
4. **Revocation fetch fails.** Block `android.googleapis.com` from the test server after the cache has expired. **Pass:** `verifyAttestation` throws, and your endpoint answers with an error. **Fail:** `Accepted`.

**Key takeaways**

- Attestation lets your server verify the key's claims itself, instead of trusting the app's word.
- Verify the chain, the revocation list, the challenge, the security levels, boot state, app identity, and proof of possession. Missing any one of them opens a known bypass.
- Trust both Google roots, and never hard-code root, chain length, or algorithm. The post-quantum migration will change them again.
- Use Google's verification library rather than writing your own parser.
- Treat an attestation result as a strong signal in a risk decision, not a verdict.

**Try it**

1. Generate an attested EC key on a physical phone and send the chain to your laptop (Base64 in logcat is fine for a test). Parse the leaf with `openssl x509 -text -noout` and find the extension with OID `1.3.6.1.4.1.11129.2.1.17`. Then check which Google root the chain ends in.
2. Fetch `https://android.googleapis.com/attestation/status` and check every serial in your chain against it. **Pass:** none listed. Now write down what your production verifier does when this fetch fails.
3. Run the same chain through [android/keyattestation](https://github.com/android/keyattestation) and compare its verdict with what you read by hand.

---

## Chapter 6: Choosing storage in practice

For about six years, the standard answer to "where do I store a token on Android?" was one class: `EncryptedSharedPreferences`. Tutorials, code reviews, and security checklists all said so. Then Google deprecated it, and the advice most developers had learned was suddenly wrong.

This is the applied chapter. It covers what replaced that class, whether you needed it in the first place, and the leaks that have nothing to do with encryption at all.

### 6.1 EncryptedSharedPreferences is dead

`EncryptedSharedPreferences` came from Jetpack Security Crypto (`androidx.security:security-crypto`). It wrapped `SharedPreferences` with Tink encryption, using a key held in the Android Keystore.

**Google deprecated every API in the library on 9 April 2025, in 1.1.0-alpha07**, "in favour of existing platform APIs and direct use of Android Keystore". The line then shipped as a stable 1.1.0 on 30 July 2025 with everything still deprecated, and nothing has been released since ([release notes](https://developer.android.com/jetpack/androidx/releases/security)). Google's reference names the replacements directly:

| Deprecated | Google's stated replacement |
|---|---|
| `EncryptedSharedPreferences` | `android.content.SharedPreferences` |
| `EncryptedFile` | `java.io.File` |
| `MasterKey`, `MasterKeys` | `javax.crypto.KeyGenerator` with the `AndroidKeyStore` instance |

Google said little about why. Practitioners point to the bug trackers *(reported)*. The library had to work around Keystore inconsistencies across manufacturers and Android versions. It performed synchronous cryptography on the calling thread, which tripped StrictMode (Android's detector for slow work on the main thread). And "keyset corruption" exceptions filled crash logs on specific OEM (device manufacturer) devices. Maintaining that stack alongside Jetpack DataStore wasn't sustainable.

For almost a year there was no official encrypted replacement. That changed in March 2026 (§6.3).

- <https://developer.android.com/reference/androidx/security/crypto/package-summary>
- <https://blog.includesecurity.com/2026/08/encryptedsharedpreferences-is-dead-heres-what-you-should-use-instead/>

### 6.2 Superseded advice, kept findable

Skim this on a first read; it exists for readers arriving from older articles. If you arrived here searching for one of these, you're in the right place, and the advice has moved.

> **`EncryptedSharedPreferences`, `EncryptedFile`, `MasterKey`: deprecated April 2025.** These were Jetpack's one-line wrappers for encrypted preferences and files. Google deprecated the whole Jetpack Security Crypto library at 1.1.0-alpha07 and shipped it as a deprecated stable 1.1.0 in July 2025. Replacement in §6.3; why the original advice was misleading even when current in §6.4.

> **`SafetyNet Attestation`: retired.** This was Google's earlier "is this a genuine device?" API. Play Integrity is the only supported path. Chapter 9.

> **`UIWebView`: deprecated.** This was iOS's original embedded browser view, running web content inside your app's process. Use `WKWebView`, which runs content out of process. §16.6.

> **WHOIS-based domain email validation: discontinued 15 July 2025.** This was a way for certificate authorities to prove you own a domain by emailing the contact in its public registration record. §8.5.

> **"MASVS L1 / L2 / R".** These were the OWASP standard's old verification levels. They left MASVS at v2.0.0 and became testing profiles: MAS-L1 (the baseline for every app), MAS-L2, MAS-R, and MAS-P for privacy (proposed with the MASVS-PRIVACY category in October 2023, which shipped in MASVS v2.1.0 in January 2024). §3.2.

> **`net.zetetic:android-database-sqlcipher` with `SupportFactory`: deprecated 2022, end of life 2023.** This was the original Android packaging of SQLCipher, the encrypted SQLite. Use `net.zetetic:sqlcipher-android`. §6.7.

Stubs exist because readers arrive from three-year-old blog posts searching for the old term, and because a book that silently rewrites its own advice is harder to trust than one that shows the change.

### 6.3 What to use instead

The replacement has three layers, each doing one job:

**Jetpack DataStore for persistence.** It does asynchronous I/O through coroutines, it's type-safe, and it does nothing on the main thread. **DataStore on its own isn't encrypted**. It's a persistence mechanism, not a security one; `MASTG-DEMO-0069` shows a token sitting in a DataStore file in plain text.

**Google Tink for encryption.** Tink is Google's cryptography library, designed so that the simplest way to use it is also the safe way. You ask for an **AEAD** (authenticated encryption with associated data: encryption that also detects tampering) rather than assembling ciphers, modes, and IVs (initialization vectors) yourself.

**The Android Keystore for key protection.** Tink keeps its working keys in a **keyset**, and a master key in the Keystore encrypts that keyset. The master key never enters your process.

Since **DataStore 1.3.0-alpha07 (11 March 2026)**, Google ships the glue as `androidx.datastore:datastore-tink`. Its `AeadSerializer` wraps your existing DataStore serializer and encrypts the whole file as one AEAD message: file-level encryption, not per-value. That design removes a whole class of per-value problems the old library had. It is JVM and Android only, and **not yet stable**: the current release is 1.3.0-rc01 (12 October 2026), a release candidate ([release notes](https://developer.android.com/jetpack/androidx/releases/datastore)). §6.6 shows it in code.

> **Trap:** Tink's own `AndroidKeysetManager` warns that the Android Keystore "is unreliable" on some devices. When its self-test fails, it disables the Keystore and **stores the keyset in cleartext**, with nothing but a logcat warning to show for it. (If the master key already exists but is unusable, `build()` throws a `KeyStoreException` instead, so handle that too.) That is §4.2's silent fallback, inside a library. Check `isUsingKeystore()` after building the manager, and record the result, as you would a StrongBox fallback.

Migration uses DataStore's `SharedPreferencesMigration`, which accepts any `SharedPreferences` instance, including an `EncryptedSharedPreferences` one. Read the old store through the deprecated API one last time, and let DataStore copy the values across. Know what its clean-up does and doesn't do. It removes the keys it migrated, and it deletes the file only when you used the constructor that takes a context and a file name. It never deletes the old library's Keystore master key (alias `_androidx_security_master_key_` by default). Once the migration has succeeded in production, delete the old preferences with `context.deleteSharedPreferences(...)` and the old alias with `KeyStore.deleteEntry(...)`.

If you can't migrate yet, a community fork (`dev.spght:encryptedprefs-ktx`, [ed-george/encrypted-shared-preferences](https://github.com/ed-george/encrypted-shared-preferences)) keeps `EncryptedSharedPreferences` and `EncryptedFile` building against current Tink. Treat it as a temporary measure with a removal date, not a permanent home; its own README asks whether you should use it and answers "No, probably not." It requires minSdk 23, because Tink Android dropped API 21 and 22 in 1.18.0.

In Kotlin Multiplatform, `datastore-tink` covers only the Android side. Put storage of secrets behind an interface with a Keychain implementation on iOS; Chapter 21 explains where that line belongs.

### 6.4 The uncomfortable question nobody asked

Here is the part that got lost in six years of "use EncryptedSharedPreferences" advice. The maintainer of that community fork puts it most clearly: the library "has misled many developers by implying that there's an inherent insecurity with SharedPreferences, which is simply not true."

Every device that launches with Android 10 or later must use file-based encryption ([source.android.com](https://source.android.com/docs/security/features/encryption/file-based)), and the app sandbox (Chapter 0.4) keeps other apps out of your private files. Reading another app's `SharedPreferences` generally requires physical access plus an exploit, or an already-compromised device. Tink's own documentation makes the same argument when explaining its cleartext fallback. If your threat model doesn't include those attackers, encrypting your feature flags bought nothing except latency and a class of keyset-corruption crashes.

Google's guidance pulls two ways here *(reasoned)*. Tink's documentation strongly recommends not setting a Keystore master key at all, unless you need user authentication and are sure the Keystore works on your target devices. The Jetpack team points to direct use of the Keystore instead (§6.1). Option A in §6.6 follows the Keystore route and detects Tink's fallback. If your threat model excludes device compromise, Tink's simpler advice is also defensible.

So decide by threat model, not by reflex:

**Long-lived refresh tokens and credentials** deserve Keystore-protected keys and encrypted payloads. Where the flow tolerates it, make the key authentication-bound (`setUserAuthenticationParameters`, §4.6). These are worth real protection because they are worth stealing and they last.

**Short-lived access tokens** are best held in memory for the session, where your architecture allows it. What is never written cannot be read off the disk. Persist only what must survive a process death.

**Feature flags, UI state, and non-sensitive preferences** belong in plain DataStore. Encrypting them buys nothing.

**Anything you can avoid storing** should not be stored. This is the cheapest control in the entire book and the one most often skipped, because it takes a product conversation rather than a code change.

```mermaid
flowchart TD
    Q1{"Must it survive<br/>a process restart?"} -- No --> M["Keep it in memory only"]
    Q1 -- Yes --> Q2{"Is it a secret?<br/>token, key, credential"}
    Q2 -- No --> P["Plain DataStore or UserDefaults<br/>sandbox + platform encryption"]
    Q2 -- Yes --> Q3{"Small secret or<br/>bulk data?"}
    Q3 -- "Small secret" --> Q4{"Must each use prove<br/>the user is present?"}
    Q4 -- Yes --> K1["Auth-bound Keystore key<br/>iOS: Keychain + SecAccessControl"]
    Q4 -- No --> K2["DataStore + Tink AEAD<br/>iOS: Keychain, WhenUnlockedThisDeviceOnly"]
    Q3 -- "Bulk or database" --> D1["SQLCipher, key wrapped by Keystore/Keychain<br/>iOS: or a file protection class"]
    K1 --> B["Exclude from backup (§6.5)"]
    K2 --> B
    D1 --> B
```

*Figure 7: Choosing where to store a piece of data*

### 6.5 The leaks that are not about encryption

MASVS-STORAGE-2, "the app prevents leakage of sensitive data", exists because data escapes through channels that have nothing to do with your storage choice. Each of these channels is a real class of finding, listed with its MASWE weakness ID where one exists.

**Logs (`MASWE-0005`).** A token in a log line is a token on disk. Since Android 4.1, ordinary apps can read only their own log entries. But logs still reach `adb logcat`, bug reports, and any crash reporter that uploads recent log lines. Strip logging from release builds (§6.6 has the pattern), and verify by inspecting the built artifact, not by trusting a build flag.

**Backups (`MASWE-0006`).** Android Auto Backup and iCloud backup copy your *unencrypted* files to storage that an attacker may be able to read. They also copy your *encrypted* files to a new device where the Keystore key doesn't exist. Keystore keys are never backed up, so the restored ciphertext fails to decrypt, typically as a crash on first launch.

On Android 12 and later (targeting API 31+), you control this with `android:dataExtractionRules`, which has separate `<cloud-backup>` and `<device-transfer>` sections. Since Android 16 QPR2 (the second quarterly platform release of Android 16), a third section, `<cross-platform-transfer>`, covers moves to iOS. For Android 11 and lower, use `android:fullBackupContent`. Two details catch people:

- For apps targeting API 31+, Android's documentation warns that on some manufacturers' devices `android:allowBackup="false"` disables cloud backup but not device-to-device transfer ([Auto Backup](https://developer.android.com/identity/data/autobackup)). Exclude sensitive files explicitly in `<device-transfer>` as well.
- `disableIfNoEncryptionCapabilities="true"` on `<cloud-backup>` sends a backup only if it can be end-to-end encrypted, which in practice means the user has a lock screen.

On iOS, set `isExcludedFromBackup` on the file's `URLResourceValues`, and prefer `ThisDeviceOnly` Keychain classes (§4.4).

**Screenshots and screen recording (`MASWE-0038`).** When your app goes to the background, the OS captures its screen for the app switcher. If a balance or card number is on screen, it's now in a file.

- On Android, `FLAG_SECURE` blocks screenshots, recording, and the recents thumbnail for that window. `Activity.setRecentsScreenshotEnabled(false)` (API 33) blocks only the thumbnail.
- In Compose, a `Dialog` defaults to `SecureFlagPolicy.Inherit`, taking the flag from its parent window. Set `SecureFlagPolicy.SecureOn` when the dialog itself shows the secret on an otherwise ordinary screen. A classic `android.app.Dialog` has its own window and inherits nothing.
- Android 14 (API 34) can *tell* you a screenshot was taken, via `registerScreenCaptureCallback`. Android 15 (API 35) can tell you the app is being recorded, via `addScreenRecordingCallback`. Detection is not prevention.
- On iOS, cover sensitive views when the scene leaves the foreground, and watch `UITraitCollection.sceneCaptureState` (iOS 17+) for recording and mirroring.

§6.6 has the code.

**The keyboard cache (`MASWE-0036`).** Keyboards learn what users type, including text typed into fields they should never learn from. On Android, use a password input type or `TYPE_TEXT_FLAG_NO_SUGGESTIONS`, and set `IME_FLAG_NO_PERSONALIZED_LEARNING` (API 26). The flag is a request, and some keyboards ignore it. On iOS, use `isSecureTextEntry` for secrets, and set `autocorrectionType = .no` and `spellCheckingType = .no` on other sensitive fields. `MASTG-DEMO-0076` shows how testers find the omission.

**Notifications (`MASWE-0037`).** A lock-screen notification showing a one-time code, or a balance, gives it to anyone holding the phone. On Android, mark such notifications `VISIBILITY_PRIVATE` with a redacted `setPublicVersion(...)`. On iOS, keep the payload generic and fetch the detail after the user unlocks. Android 15 also hides one-time codes in notifications from untrusted notification-listener apps ([Android 15 behavior changes](https://developer.android.com/about/versions/15/behavior-changes-all)), but that protects the code from other apps, not from someone looking at the screen. Android 16 redacts such codes from the lock screen only in some higher-risk situations ([Android Authority](https://www.androidauthority.com/android-16-sensitive-notifications-lock-screen-3501564/)) *(reported)*, so don't rely on it.

**The clipboard (`MASWE-0030`).** Since Android 10, only the focused app and the default keyboard can read the clipboard. From API 33, mark sensitive clips with `ClipDescription.EXTRA_IS_SENSITIVE` so the system hides their preview. On iOS the general pasteboard can travel to the user's other devices through Universal Clipboard, so use `.localOnly` and an `.expirationDate`. §6.6 has the code.

**Keychain items that outlive the app.** On iOS, Keychain items have historically survived app deletion, so a reinstall can find a previous user's refresh token *(reported)*. Apple doesn't document this behavior either way. The common defense is to write a "has launched" flag to `UserDefaults` (which *is* deleted with the app) and clear your Keychain items when the flag is missing.

**Process memory.** You can't fully solve this one, but you can shorten the time a secret spends in memory *(reasoned)*. Avoid holding secrets in long-lived `String` objects, which are immutable, so you can't overwrite them. Prefer a `ByteArray` or `CharArray` you can `fill(0)` after use. And don't keep a decrypted blob in memory for the app's whole lifetime.

### 6.6 How to implement it

#### Android, option A: DataStore + Tink + Keystore

This is §6.3's three layers: the Keystore holds the master key, Tink encrypts, and DataStore persists. Use it for any secret you store as data: refresh tokens, cached personal data, small files.

```kotlin
// build.gradle.kts
dependencies {
    implementation("androidx.datastore:datastore:1.3.0-rc01")
    implementation("androidx.datastore:datastore-tink:1.3.0-rc01")  // pre-release: pin and test
    implementation("com.google.crypto.tink:tink-android:1.24.0")
}
```

```kotlin
import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.core.DataStoreFactory
import androidx.datastore.core.Serializer
import androidx.datastore.dataStoreFile
import androidx.datastore.tink.AeadSerializer
import com.google.crypto.tink.Aead
import com.google.crypto.tink.KeyTemplate
import com.google.crypto.tink.RegistryConfiguration
import com.google.crypto.tink.aead.AeadConfig
import com.google.crypto.tink.aead.PredefinedAeadParameters
import com.google.crypto.tink.integration.android.AndroidKeysetManager
import java.io.InputStream
import java.io.OutputStream

data class Session(val refreshToken: String = "")

// Your ordinary, unencrypted serializer. AeadSerializer wraps it.
object SessionSerializer : Serializer<Session> {
    override val defaultValue = Session()
    override suspend fun readFrom(input: InputStream): Session =
        Session(input.readBytes().decodeToString())
    override suspend fun writeTo(t: Session, output: OutputStream) =
        output.write(t.refreshToken.encodeToByteArray())
}

object SecureSessionStore {
    private const val FILE = "session.enc"
    @Volatile private var instance: DataStore<Session>? = null

    /** False if Tink fell back to a cleartext keyset. Read it in tests and debug logs. */
    @Volatile var usingKeystore: Boolean = false
        private set

    // DataStore allows exactly one instance per file, so this is a process-wide singleton.
    fun get(context: Context): DataStore<Session> =
        instance ?: synchronized(this) {
            instance ?: create(context.applicationContext).also { instance = it }
        }

    private fun create(context: Context): DataStore<Session> {
        AeadConfig.register()
        val manager = AndroidKeysetManager.Builder()
            .withSharedPref(context, "session_keyset", "tink_keysets")  // keyset, itself encrypted
            .withKeyTemplate(KeyTemplate.createFrom(PredefinedAeadParameters.AES256_GCM))
            .withMasterKeyUri("android-keystore://session_master_key")  // the Keystore key
            .build()
        usingKeystore = manager.isUsingKeystore
        if (!usingKeystore) {
            // Tink fell back to a cleartext keyset (§6.3). Record it; do not pretend.
            SecurityTelemetry.record("tink_keystore_unavailable")
        }
        val aead = manager.keysetHandle.getPrimitive(RegistryConfiguration.get(), Aead::class.java)

        return DataStoreFactory.create(
            serializer = AeadSerializer(
                aead = aead,
                wrappedSerializer = SessionSerializer,
                associatedData = FILE.encodeToByteArray(),  // binds ciphertext to this file
            ),
            produceFile = { context.dataStoreFile(FILE) },
        )
    }
}
```

`SecurityTelemetry` stands for whatever your app uses to report security events (§14.4). The `associatedData` isn't secret. Tink mixes it into the authentication tag, so a ciphertext copied from another encrypted file fails to decrypt here instead of being silently accepted. Google's documentation recommends the file name for this reason.

DataStore 1.3 also introduces `DataStore.Builder`, which Google now recommends over `DataStoreFactory`. I use `DataStoreFactory` here because it's the API that has been stable longest.

To migrate from `EncryptedSharedPreferences`, add a migration to `DataStoreFactory.create(...)`:

```kotlin
import androidx.datastore.migrations.SharedPreferencesMigration
import androidx.datastore.migrations.SharedPreferencesView

val fromLegacyPrefs = SharedPreferencesMigration(
    produceSharedPreferences = { openLegacyEncryptedPrefs(context) },  // your existing EncryptedSharedPreferences.create(...)
    keysToMigrate = setOf("refresh_token"),
) { prefs: SharedPreferencesView, current: Session ->
    prefs.getString("refresh_token")?.let { current.copy(refreshToken = it) } ?: current
}
// DataStoreFactory.create(..., migrations = listOf(fromLegacyPrefs), ...)
```

#### Android, option B: a Keystore key used directly

Use a Keystore key directly when the key needs authorizations Tink can't express: authentication-bound keys, StrongBox, or per-use biometric binding (Chapter 11). This code assumes minSdk 28, which `setIsStrongBoxBacked` and `setUnlockedDeviceRequired` both need; the commented-out `setUserAuthenticationParameters` line needs API 30.

```kotlin
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyInfo
import android.security.keystore.KeyProperties
import android.security.keystore.StrongBoxUnavailableException
import java.security.KeyStore
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.SecretKeyFactory

private const val ANDROID_KEYSTORE = "AndroidKeyStore"

private fun getOrCreateKey(alias: String, strongBox: Boolean): SecretKey {
    val keyStore = KeyStore.getInstance(ANDROID_KEYSTORE).apply { load(null) }
    (keyStore.getEntry(alias, null) as? KeyStore.SecretKeyEntry)?.let { return it.secretKey }

    val spec = KeyGenParameterSpec.Builder(
        alias,
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT,
    )
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)              // AEAD, per Chapter 0.2
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setKeySize(256)
        .setUnlockedDeviceRequired(true)                          // §4.6: drop if background work must decrypt
        // For a refresh token, require the user as well (§4.6, Chapter 11):
        // .setUserAuthenticationRequired(true)
        // .setUserAuthenticationParameters(0, KeyProperties.AUTH_BIOMETRIC_STRONG)
        .setIsStrongBoxBacked(strongBox)
        .build()

    return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, ANDROID_KEYSTORE)
        .apply { init(spec) }
        .generateKey()
}
```

**Handle the StrongBox failure explicitly**, because this is §4.2's decision in code:

```kotlin
fun tokenKey(context: Context, alias: String): SecretKey {
    val hasStrongBox =
        context.packageManager.hasSystemFeature(PackageManager.FEATURE_STRONGBOX_KEYSTORE)
    return try {
        getOrCreateKey(alias, strongBox = hasStrongBox).also { if (!hasStrongBox) SecurityTelemetry.record("keystore_strongbox_absent") }
    } catch (e: StrongBoxUnavailableException) {
        // Deliberate, recorded fallback to the TEE, not a silent downgrade.
        SecurityTelemetry.record("keystore_strongbox_unavailable")
        getOrCreateKey(alias, strongBox = false)
    }
}

// Confirm what you got, rather than assuming.
fun securityLevelOf(key: SecretKey): String {
    val info = SecretKeyFactory.getInstance(key.algorithm, ANDROID_KEYSTORE)
        .getKeySpec(key, KeyInfo::class.java) as KeyInfo
    return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        when (info.securityLevel) {
            KeyProperties.SECURITY_LEVEL_STRONGBOX -> "strongbox"
            KeyProperties.SECURITY_LEVEL_TRUSTED_ENVIRONMENT -> "tee"
            KeyProperties.SECURITY_LEVEL_UNKNOWN_SECURE -> "secure_unknown"
            KeyProperties.SECURITY_LEVEL_SOFTWARE -> "software"
            else -> "unknown"
        }
    } else {
        @Suppress("DEPRECATION")
        if (info.isInsideSecureHardware) "secure_hardware" else "software"
    }
}
```

Each encryption needs a fresh IV. That's Chapter 0.2's rule that a GCM nonce must never repeat, and the Keystore enforces it for you:

```kotlin
import javax.crypto.Cipher
import javax.crypto.spec.GCMParameterSpec

private const val IV_BYTES = 12
private const val TAG_BITS = 128

fun encrypt(plaintext: ByteArray, key: SecretKey, aad: ByteArray): ByteArray {
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.ENCRYPT_MODE, key)          // the Keystore generates the IV; do not supply one
    cipher.updateAAD(aad)                          // e.g. "refresh_token", binds purpose to ciphertext
    val ciphertext = cipher.doFinal(plaintext)
    return cipher.iv + ciphertext                  // store the IV alongside; it is not secret
}

fun decrypt(stored: ByteArray, key: SecretKey, aad: ByteArray): ByteArray {
    val iv = stored.copyOfRange(0, IV_BYTES)
    val ciphertext = stored.copyOfRange(IV_BYTES, stored.size)
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.DECRYPT_MODE, key, GCMParameterSpec(TAG_BITS, iv))
    cipher.updateAAD(aad)
    return cipher.doFinal(ciphertext)              // throws AEADBadTagException if tampered
}
```

**The wrong version, for contrast:**

```kotlin
// DON'T: CBC gives you no integrity, and a fixed IV leaks structure.
val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
cipher.init(Cipher.ENCRYPT_MODE, key, IvParameterSpec(ByteArray(16)))  // fixed IV: broken
// (A Keystore key refuses a caller-supplied IV unless you also weakened it with
// setRandomizedEncryptionRequired(false). If your code compiles and runs, check for that.)
```

Then persist the result, for example as Base64 in plain DataStore. The DataStore file isn't encrypted; your bytes are.

#### Android: keep secrets out of backups

Exclude the ciphertext **and** the Tink keyset. The Keystore master key never leaves the device, so restoring either one to a new device produces data that nobody can decrypt.

```xml
<!-- AndroidManifest.xml -->
<application
    android:allowBackup="true"
    android:dataExtractionRules="@xml/data_extraction_rules"
    android:fullBackupContent="@xml/backup_rules">
</application>
```

```xml
<!-- res/xml/data_extraction_rules.xml: Android 12+ when targeting API 31+ -->
<data-extraction-rules>
    <cloud-backup disableIfNoEncryptionCapabilities="true">
        <exclude domain="file" path="datastore/session.enc" />
        <exclude domain="sharedpref" path="tink_keysets.xml" />
    </cloud-backup>
    <device-transfer>
        <exclude domain="file" path="datastore/session.enc" />
        <exclude domain="sharedpref" path="tink_keysets.xml" />
    </device-transfer>
</data-extraction-rules>
```

```xml
<!-- res/xml/backup_rules.xml: Android 11 and lower -->
<full-backup-content>
    <exclude domain="file" path="datastore/session.enc" />
    <exclude domain="sharedpref" path="tink_keysets.xml" />
</full-backup-content>
```

After a restore, the user signs in again on the new device. That is the correct outcome for a credential.

#### iOS: Keychain with the right accessibility class

```swift
import Foundation
import Security

enum KeychainError: Error {
    case unexpectedStatus(OSStatus)
}

func storeToken(_ token: Data, account: String,
                service: String = "com.example.app.session") throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: service,
        kSecAttrAccount as String: account,
    ]
    let attributes: [String: Any] = [
        kSecValueData as String: token,
        // WhenUnlocked: needs an unlocked device. ThisDeviceOnly: never migrates
        // to another device. See §4.4.
        kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
    ]

    // Update in place if it exists; add it if not. No delete-then-add window.
    var status = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)
    if status == errSecItemNotFound {
        let newItem = query.merging(attributes) { _, new in new }
        status = SecItemAdd(newItem as CFDictionary, nil)
    }
    guard status == errSecSuccess else { throw KeychainError.unexpectedStatus(status) }
}

func readToken(account: String,
               service: String = "com.example.app.session") throws -> Data? {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: service,
        kSecAttrAccount as String: account,
        kSecReturnData as String: true,
        kSecMatchLimit as String: kSecMatchLimitOne,
    ]
    var item: CFTypeRef?
    let status = SecItemCopyMatching(query as CFDictionary, &item)
    switch status {
    case errSecSuccess: return item as? Data
    case errSecItemNotFound: return nil
    default: throw KeychainError.unexpectedStatus(status)   // -25308: device locked, §4.4
    }
}
```

If background refresh needs the token while the device is locked, the considered change is `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`. It is **not** `kSecAttrAccessibleAlways`, which is deprecated and protects nothing before first unlock.

For a key that must never leave hardware, create it in the Secure Enclave. Remember from §4.3 that it's P-256 only through this API, and that it does signing and key agreement, not direct encryption:

```swift
func makeSigningKey(tag: Data) throws -> SecKey {
    var cfError: Unmanaged<CFError>?
    guard let access = SecAccessControlCreateWithFlags(
        kCFAllocatorDefault,
        kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,   // unusable if the passcode is removed
        [.privateKeyUsage, .biometryCurrentSet],           // "CurrentSet", not "Any": §11.3
        &cfError
    ) else { throw cfError!.takeRetainedValue() as Error }

    let attributes: [String: Any] = [
        kSecAttrKeyType as String: kSecAttrKeyTypeECSECPrimeRandom,
        kSecAttrKeySizeInBits as String: 256,
        kSecAttrTokenID as String: kSecAttrTokenIDSecureEnclave,
        kSecPrivateKeyAttrs as String: [
            kSecAttrIsPermanent as String: true,
            kSecAttrApplicationTag as String: tag,
            kSecAttrAccessControl as String: access,
        ] as [String: Any],
    ]
    guard let key = SecKeyCreateRandomKey(attributes as CFDictionary, &cfError) else {
        throw cfError!.takeRetainedValue() as Error
    }
    return key   // a handle; the private key stays in the Secure Enclave
}
```

For files, choose the class when you write, and exclude from backup what must not travel:

```swift
func writeSensitive(_ data: Data, to url: URL) throws {
    try data.write(to: url, options: [.atomic, .completeFileProtection])
    var values = URLResourceValues()
    values.isExcludedFromBackup = true
    var fileURL = url
    try fileURL.setResourceValues(values)
}
```

#### Screenshots and the recents thumbnail

`MASWE-0038`, *Insufficient Protection of Sensitive Data from Screenshots or Screen Recordings* (§6.5). On Android, apply `FLAG_SECURE` to the sensitive screen for as long as that screen exists:

```kotlin
import android.os.Bundle
import android.view.WindowManager
import androidx.appcompat.app.AppCompatActivity

class PaymentActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)   // before content is shown
        setContentView(R.layout.activity_payment)
    }
}
```

> **Trap:** a common snippet sets `FLAG_SECURE` in `onResume()` and clears it in `onPause()`. That clears the flag at the moment the user leaves the app, which is when the system captures the thumbnail for the recents screen. The one screenshot you most wanted to block is the one you let through. The lifecycle order predicts this, and the Verify it step below checks it on your own device *(reasoned)*.

In a single-activity Compose app, scope the flag to the screen instead (`LocalActivity` is in `androidx.activity:activity-compose` 1.10 and later):

```kotlin
import android.view.WindowManager
import androidx.activity.compose.LocalActivity
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect

@Composable
fun SecureScreen(content: @Composable () -> Unit) {
    val activity = LocalActivity.current
    DisposableEffect(activity) {
        activity?.window?.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
        onDispose { activity?.window?.clearFlags(WindowManager.LayoutParams.FLAG_SECURE) }
    }
    content()
}
```

§6.5's dialog rule, in code, is `DialogProperties(securePolicy = SecureFlagPolicy.SecureOn)`. One more gap catches people who did everything else right: a `SurfaceView` needs `setSecure(true)` before its window is attached.

iOS has no `FLAG_SECURE`. You can detect that the screen is being recorded or mirrored and hide sensitive content. From iOS 17, read the scene's capture state from the trait collection and observe changes (`UIScreen.isCaptured`, which older samples use, is deprecated in iOS 27):

```swift
final class PaymentViewController: UIViewController {
    private let sensitiveView = UIView()   // the balance, card number, or similar

    override func viewDidLoad() {
        super.viewDidLoad()
        view.addSubview(sensitiveView)
        registerForTraitChanges([UITraitSceneCaptureState.self]) { (self: Self, _) in
            self.updateForCapture()
        }
        updateForCapture()
    }

    private func updateForCapture() {
        sensitiveView.isHidden = traitCollection.sceneCaptureState == .active
    }
}
```

Screenshots are different: iOS tells you only *after* one was taken (`UIApplication.userDidTakeScreenshotNotification`), which is useful for logging, not prevention. For the app-switcher snapshot, cover sensitive content when the scene resigns active. The long-standing `isSecureTextEntry` trick (placing your sensitive view inside the layer of a secure `UITextField`, which the OS excludes from captures) works, but it relies on undocumented behavior, so test it after each iOS release.

#### Secure logging

`MASWE-0005`, *Insertion of Sensitive Data into Logs*. The robust pattern is a logging tree that drops everything below error in release:

```kotlin
// Application.onCreate
if (BuildConfig.DEBUG) {
    Timber.plant(Timber.DebugTree())
} else {
    Timber.plant(object : Timber.Tree() {
        override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
            if (priority >= Log.ERROR) crashReporter.log(message)   // no verbose/debug/info
        }
    })
}
```

This beats scattering `if (BuildConfig.DEBUG)` at call sites, because nobody can forget it at one of them. It doesn't stop an error message carrying a token or an email address, so keep personal data out of error messages too. Pair it with the `-assumenosideeffects` rule in §15.8, and verify by inspecting the built artifact.

#### The clipboard

`MASWE-0030`, *Improper Use of the Clipboard*. Both platforms have a flag for this, and almost nobody sets it.

```kotlin
val clip = ClipData.newPlainText("", sensitiveValue).apply {
    description.extras = PersistableBundle().apply {
        // ClipDescription.EXTRA_IS_SENSITIVE if you compile against SDK 33+; the literal works with older SDKs
        putBoolean("android.content.extra.IS_SENSITIVE", true)
    }
}
clipboardManager.setPrimaryClip(clip)
```

On Android 13 and later the flag hides the value in the system's copy-confirmation preview. Google's documentation states that it doesn't otherwise change clipboard behavior or add security: any app that can read the clipboard can still read it, so copy sensitive values only when the user asks to.

```swift
import UniformTypeIdentifiers

UIPasteboard.general.setItems(
    [[UTType.plainText.identifier: sensitiveValue]],
    options: [
        .localOnly: true,                                // do not sync to other devices
        .expirationDate: Date().addingTimeInterval(60)   // clears itself
    ]
)
```

The iOS `localOnly` option matters more than it looks: without it, a copied value can travel to the user's other devices through Universal Clipboard.

#### Verify it

Code review doesn't tell you whether encryption is on the write path you think it is. Check the built artifact.

**Android.** `run-as` works only on a debuggable build, so run this on a debug build of the same code, or on a rooted test device. The glob must expand inside the app's sandbox, which is why the first command uses `sh -c`:

```bash
adb shell "run-as com.example.app sh -c 'cat shared_prefs/*.xml'"
adb shell "run-as com.example.app ls -la files/datastore/"
adb exec-out run-as com.example.app cat files/datastore/session.enc | xxd | head   # exec-out: binary-safe
```

**Pass:** the DataStore file is binary that doesn't contain your token, and the preferences hold only Tink's encrypted keyset. **Fail:** readable JSON or a recognizable token string. That means your encryption layer isn't on the write path, a common outcome when a migration half-succeeded. `MASTG-DEMO-0069` (DataStore) and `MASTG-DEMO-0059` (SharedPreferences) show the failing case.

Confirm the key is where you think, using `securityLevelOf()` from option B:

```kotlin
Log.d("keycheck", "securityLevel=${securityLevelOf(key)} tinkKeystore=${SecureSessionStore.usingKeystore}")
```

**Fail:** `software`, or `tinkKeystore=false`, on a flow you designed for hardware backing. That is §4.2's silent-fallback finding, showing up in a log line. Remove the line before release.

**Android backups.** Follow `MASTG-DEMO-0020`'s script. It enables `bmgr`, selects the local transport (`com.android.localtransport/.LocalTransport`), and marks it encrypted (`adb shell settings put secure backup_local_transport_parameters 'is_encrypted=true'`). It then runs `adb shell bmgr backupnow com.example.app` and reinstalls the app, so Android restores the backup. Without the encrypted flag, `disableIfNoEncryptionCapabilities` skips the whole `<cloud-backup>` section, so the check passes without testing anything. Without the local transport, the backup goes somewhere you can't inspect. **Pass:** after the restore, your other files are back (list them with `run-as`) but neither `session.enc` nor `tink_keysets.xml` is. `bmgr` never exercises `<device-transfer>`, so check that section by review, or with a real device-to-device transfer to a second phone.

**iOS.** On the simulator, inspect the app container for plain text:

```bash
DATA=$(xcrun simctl get_app_container booted com.example.app data)
grep -rIl "eyJ" "$DATA"          # a JWT begins "eyJ"
```

**Pass:** no output. **Fail:** a token in a plist, a cache, or a log file. The simulator doesn't enforce Data Protection classes, so it proves only what your app wrote in plain text. Check classes and Secure Enclave keys on a physical device.

**Screenshots and recents.** On a physical device, open each sensitive screen, press Home, and open the recents screen. **Pass:** the thumbnail is blank (Android) or covered (iOS), and a screenshot of the screen itself fails or comes out black on Android. **Fail:** you can read the balance or card number in the thumbnail.

**Logs.** Install the release build, exercise sign-in and the flows that handle secrets, and watch `adb logcat --pid=$(adb shell pidof -s com.example.app)`. **Pass:** nothing below error level from your app, and no tokens or email addresses at any level.

### 6.7 Encrypting a local database

The rest of this chapter covers tokens and preferences. Databases are the other half, and they're where most personal data lives.

**The default position.** On both platforms, app-private database files sit inside the sandbox and are covered by platform storage encryption at rest (Chapter 0.4). For most app data, that's enough. Room adds no encryption of its own; `MASTG-DEMO-0070` shows a Room database read in plain text.

**When to add database encryption on top.** Add it when your threat model includes a compromised or rooted device, when a regulator requires encryption at rest as a distinct control, or when the database holds something whose exposure would seriously harm an individual: health records, financial history, or message content.

**Android.** The standard route is **SQLCipher**, now shipped as `net.zetetic:sqlcipher-android` (package `net.zetetic.database.sqlcipher`; 4.19.1 at the time of writing, minSdk 23). Two things to know:

- **It plugs into Room.** Room 3 takes it through `SQLCipherDriver`, and Room 2 through `SupportOpenHelperFactory`. Call `System.loadLibrary("sqlcipher")` before opening any database.
- **Don't use the old library.** `net.zetetic:android-database-sqlcipher` (package `net.sqlcipher`), with its `SupportFactory`, was deprecated in 2022, reached end of life in 2023, and receives no updates; don't start a new project on it. Its open-source edition won't gain 16 KB page-size support; Zetetic offers a compatible build only to commercial customers ([Zetetic](https://www.zetetic.net/blog/2025/06/26/sqlcipher-for-android-16kb-page-size-support/)). Google Play first announced that requirement for 1 November 2025 ([Android Developers Blog](https://android-developers.googleblog.com/2025/05/prepare-play-apps-for-devices-with-16kb-page-size.html)); Android's current guide says that from **1 February 2027** you cannot release an update targeting Android 15 or later without it ([page sizes guide](https://developer.android.com/guide/practices/page-sizes)). §19.6 has the rest.

With Room 3:

```kotlin
// build.gradle.kts:
//   implementation("net.zetetic:sqlcipher-android:4.19.1@aar")
//   implementation("androidx.sqlite:sqlite:<the version SQLCipher's README names>")

import android.content.Context
import androidx.room3.Room
import net.zetetic.database.sqlcipher.driver.SQLCipherDriver

fun buildDatabase(context: Context, passphrase: ByteArray): AppDatabase {
    System.loadLibrary("sqlcipher")                  // once, before first use
    return Room.databaseBuilder(
            context, AppDatabase::class.java, context.getDatabasePath("app.db").absolutePath
        )
        .setDriver(SQLCipherDriver(passphrase, null, null))
        .build()
}
```

On Room 2, the equivalent is `.openHelperFactory(SupportOpenHelperFactory(passphrase))`, also from `net.zetetic.database.sqlcipher`.

The passphrase is where implementations go wrong. **You can't read the bytes of a hardware-backed Keystore key.** `getEncoded()` returns `null`, by design. So generate 32 random bytes with `SecureRandom`, encrypt them with a Keystore key (§6.6 option B), store the ciphertext, and decrypt it at startup to pass to `buildDatabase`. Never use a constant.

> **Trap:** a hard-coded passphrase converts database encryption into an obfuscation exercise. `strings` on your APK will find it (`MASWE-0004`).

Count the cost, too. SQLCipher adds native libraries to your app, and it adds measurable overhead to large queries. Measure before you commit to it.

**iOS.** Two options. SQLCipher works the same way, with the passphrase kept in the Keychain. Or use **file-level Data Protection**: `NSPersistentStoreFileProtectionKey` for Core Data, or the `SQLITE_OPEN_FILEPROTECTION_*` flags with `sqlite3_open_v2`. That relies on the platform instead of adding a dependency. The trade-off is that your data is readable whenever the device is unlocked, which may be what your app needs anyway.

> **Trap:** `NSFileProtectionComplete` on a database your app touches from background tasks. The database becomes unreadable about 10 seconds after lock, and a background sync that opens it fails or crashes. Use `CompleteUntilFirstUserAuthentication` for such stores, or move the work into the foreground.

**What database encryption doesn't solve.** The key has to be available for the app to read its own data. On a device where an attacker can run code as your app, they read the database through your app's own key. Encryption raises the cost of offline extraction and physical access. It doesn't defeat a live compromise. Be clear which of those you're paying for.

**Key takeaways**

- `EncryptedSharedPreferences` is deprecated. The replacement is DataStore + Tink + Keystore, now packaged as `datastore-tink` (a release candidate, not yet stable).
- Plain `SharedPreferences` inside the sandbox was never insecure. Encrypt because your threat model includes device compromise, not by reflex.
- Detect and record every silent fallback (StrongBox to TEE, Tink to cleartext).
- Most real storage findings are leaks, not weak ciphers: logs, backups, screenshots, keyboards, notifications, and the clipboard.
- For databases, derive nothing from the Keystore key itself. Wrap a random passphrase with it, and use `sqlcipher-android`, not the deprecated library.

**Try it**

1. Reproduce `MASTG-DEMO-0059` (<https://mas.owasp.org/MASTG/demos/android/MASVS-STORAGE/MASTG-DEMO-0059/MASTG-DEMO-0059/>) in your own app: write a fake token to plain `SharedPreferences` and read it back with `run-as`. Then switch the write to §6.6 option A and confirm the file no longer contains it.
2. Add §6.6's backup rules, run `adb shell bmgr backupnow` on your package over an encrypted local transport, restore it, and confirm the excluded files are absent while your other files came back (`MASTG-DEMO-0020` shows the setup; §6.6's Verify it explains why the encrypted flag matters).
3. On iOS, list every file your app writes under `Library/` and `Documents/`, and record its protection class and backup status. Anything sensitive that is still at the default `CompleteUntilFirstUserAuthentication`, or backed up, is a finding for your backlog.

---
