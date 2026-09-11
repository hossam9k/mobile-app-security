---
part: 02
last_verified: 2026-09-11
volatility: high
recheck_because: "Jetpack deprecation is recent; RKP root changed Feb 2026"
---

# Part 2: Data at rest

## Chapter 4: How platform key storage actually works

Most developers use the Keystore and the Keychain without knowing what happens underneath, and then cannot answer basic questions about what their protection is worth. This chapter is the mechanism.

### 4.1 The Android Keystore, from the top down

The `AndroidKeyStore` you call from Kotlin is a Java Cryptography Architecture provider running **inside your app's own process**. It does not hold your keys. It forwards requests to a system daemon.

That daemon is **keystore2** on modern Android — rewritten in Rust, which matters because key handling is exactly the kind of code where memory-safety bugs are catastrophic. keystore2 stores **keyblobs**: your key material, encrypted such that the daemon can store it but **cannot use or reveal it**. That property is the foundation of the whole design. Even the system service holding your key cannot read it.

Below the daemon sits a hardware abstraction layer implementing `IKeyMintDevice`. **KeyMint** is the current HAL, replacing the older **Keymaster**; it added Curve25519 support among other things. Behind the HAL runs the **KeyMint trusted application** — software executing in a secure context, most often in ARM TrustZone. That trusted app has access to raw key material, performs every cryptographic operation, and validates all access-control conditions on a key before permitting its use.

So when your code "encrypts with a Keystore key," what physically happens is: your process sends the plaintext and a key handle to the daemon, the daemon passes the encrypted keyblob and the request to the trusted app, the trusted app decrypts the keyblob inside secure hardware, checks the key's authorizations, performs the operation, and returns only the result. **The key never enters your process, and never enters the Android OS.**

One more component matters: **Gatekeeper**, the system component responsible for user authentication by password and fingerprint. It is not part of the Keystore, but the Keystore supports **authentication-bound keys**, meaning keys usable only after the user has authenticated. Gatekeeper is what vouches for that authentication. This is the machinery behind Chapter 12.

- <https://source.android.com/docs/security/features/keystore>
- <https://developer.android.com/privacy-and-security/keystore>

### 4.2 TEE versus StrongBox, and why the difference is real

A key's protection has a **security level**, and you can query it. `KeyInfo.getSecurityLevel()` returns one of three values (on API 28 and below, use the boolean `KeyInfo.isInsideSecurityHardware()`):

**`SOFTWARE`** means the OS is the only thing protecting the key. On a compromised or rooted device, treat that key as extractable. It is better than a key in your APK, and it is not hardware protection.

**`TRUSTED_ENVIRONMENT`** means the key lives in the TEE — a secure area of the *main* processor, isolated from the OS by hardware. If Android itself is fully compromised, the TEE remains intact: an attacker who can read internal storage might be able to *use* your Keystore keys on that device, but cannot *extract* them from it. Google's own open-source TEE is **Trusty**, provided free to OEMs; other TEE implementations exist and Android supports them.

**`STRONGBOX`** means the key lives in a dedicated, purpose-built secure processor — an embedded Secure Element or an integrated Secure Enclave, physically separate from the application processor. Titan M in Pixel devices is the well-known example. StrongBox arrived in Android 9 (API 28) and offers stronger isolation and tamper resistance than the TEE.

Three practical consequences follow, and they are where designs go wrong.

**StrongBox is not universal.** It became "strongly recommended" for devices launching with Android 12 and is expected to become a requirement eventually, but you cannot assume it. Request it, catch the failure, and decide your fallback deliberately.

**StrongBox is slower and supports fewer algorithms.** Low-power secure elements support a deliberately reduced subset of algorithms and key sizes. If you demand StrongBox with an exotic configuration, key generation will fail on devices that would otherwise have served you fine.

**Silent fallback is a finding, not a fallback.** If your payment flow requests StrongBox, fails, and quietly falls back to a software-backed key without telling anyone, you have a control that reports success while providing nothing. Either fall back to TEE explicitly and record that you did, or require server-side step-up authentication for that flow on that device. Write down which. One question separates people who have shipped hardware-backed crypto from people who have only read about it: what does your app do when StrongBox is unavailable?

### 4.3 The iOS Keychain, from the top down

Apple's design differs in structure but rhymes in principle.

The Keychain is a **single SQLite database** on the file system, shared across all apps, managed by the **securityd** daemon. There is one database, not one per app. When your code calls a Keychain API, that becomes a call to securityd, which decides what your process may see by inspecting your `keychain-access-groups`, `application-identifier`, and `application-group` entitlements. Sharing between apps is possible only for apps signed by the same developer, enforced through code signing and provisioning profiles.

Encryption uses **two distinct AES-256-GCM keys per item**. A **metadata key** encrypts every attribute other than the secret value, which lets securityd search the database quickly; that key is protected by the Secure Enclave but cached in the Application Processor for speed. A **per-row secret key** encrypts `kSecValueData`, the actual secret, and using it **always requires a round trip through the Secure Enclave**.

That split is elegant and worth understanding: search stays fast because metadata decryption is cheap, while the thing that matters cannot be read without hardware involvement.

The **Secure Enclave** itself is a separate coprocessor, present on A7 and later. Apple's own description is the useful one: it provides all cryptographic operations for Data Protection key management and maintains the integrity of Data Protection **even if the kernel has been compromised**. Keys generated in it never enter RAM and are never processed by the OS or by user-space code; a `SecKey` in your Swift is a *handle*, not the key.

Two constraints on the Secure Enclave surprise people. It supports **elliptic-curve keys only** — no RSA. And it is for **signing and key agreement**, not direct encryption and decryption. To encrypt data with Secure Enclave protection you do ECDH key agreement or encrypt a symmetric key, rather than calling an encrypt function on an SE-resident key.

Access control lists on Keychain items are **evaluated inside the Secure Enclave** and released to the kernel only when their constraints are satisfied. That is why biometric-gated Keychain items are meaningfully protected and not just UI.

- <https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web>

### 4.4 Data Protection classes: the decision you keep getting wrong

Every Keychain item carries an accessibility class via `kSecAttrAccessible`, and every file carries an analogous Data Protection class. They control *when* the decryption key is available.

**`kSecAttrAccessibleWhenUnlocked`** — readable only while the device is unlocked. Maps to `NSFileProtectionComplete` for files. The strongest ordinary choice.

**`kSecAttrAccessibleAfterFirstUnlock`** — readable after the user has unlocked once since boot, and thereafter even while locked. Maps to `NSFileProtectionCompleteUntilFirstUserAuthentication`. This is the class for items that background refresh needs, and Apple names that use case explicitly.

**`kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`** — behaves like "when unlocked" but exists only if the device has a passcode set, and never leaves the device.

**`kSecAttrAccessibleAlways`** — readable at any time, mapping to `NSFileProtectionNone`. Apple discouraged this and it should not appear in new code.

Add **`ThisDeviceOnly`** to any of these and the item is excluded from backups and will not migrate to another device.

The failure mode is depressingly consistent. Background refresh breaks because an item is `WhenUnlocked`. Someone loosens the class to make the bug go away. Now a token that should require an unlocked device is readable on a locked one, and it is in the iCloud backup as well. **The right fix is almost always to restructure when the work happens, not to weaken the class.** If background refresh genuinely needs a credential, `AfterFirstUnlock` is the considered answer — not `Always`.

One more thing to know honestly: physical-access attacks have historically defeated these boundaries. Checkm8-class exploits and jailbreak tools such as checkra1n have enabled Keychain dumps without the user's passcode on affected hardware. Data Protection raises the bar substantially; it is not absolute against an attacker with the device and the right exploit.

### 4.5 A note on sharing

On Android, keys are per-app by default and the Keystore's isolation is strong. On iOS, adding another app to your `keychain-access-groups` entitlement means **trusting that app completely** — anything in the group can call `SecItemCopyMatching` on your items, including a compromised app from your own Team ID. Access groups are a genuine feature with a genuine cost; enumerate what is in yours.

---

## Chapter 5: Key attestation — proving where a key lives

The Keystore protects your key. Attestation lets your *server* verify that protection independently, which is a different and more valuable thing.

### 5.1 The problem it solves

Your app tells your backend "I generated a key in hardware." Why would the backend believe it? A rooted device, an emulator, or a modified build can claim anything. Key attestation is the cryptographic answer to that question.

Key attestation arrived in Android 7.0 with Keymaster 2. ID attestation, which can include hardware identifiers, followed in Android 8.0 with Keymaster 3.

### 5.2 How it works

The flow is worth memorising because it is the shape of every attestation protocol you will meet:

1. Your **server** generates a random nonce and sends it to the app.
2. The **app** generates a key pair in the `AndroidKeyStore`, passing that nonce as the attestation challenge.
3. **Android builds an X.509 certificate chain** rooted in a Google hardware attestation root. The leaf certificate carries a `KeyDescription` extension containing the security level, boot state, the key's authorizations, and your nonce.
4. The app sends the **chain** to your server.
5. Your **server** verifies the chain against the Google attestation root, confirms the nonce matches what it issued, and reads the security level and key properties.

The crucial detail is where the information comes from. The authorization list in that certificate is **collected or generated by code inside the secure hardware and is not controlled by the platform** — sourced from the bootloader or over a secure channel that does not require trusting Android. That is why the claim is worth something: the OS cannot forge it, because the OS was never asked.

The `SecurityLevel` field tells you how resistant the key and the attestation itself are to attack: `SOFTWARE`, `TRUSTED_ENVIRONMENT`, or `STRONGBOX`. Reading that field is the point of the exercise.

- <https://source.android.com/docs/security/features/keystore/attestation>
- <https://developer.android.com/identity/digital-credentials/credential-issuer/keystore-attestation>

### 5.3 The thing that will break your production app in 2026

Attestation certificates used to be provisioned into devices at manufacture. Google moved to **Remote Key Provisioning (RKP)**, which improves privacy substantially: each application receives a different attestation key, keys rotate regularly, and Google's backend is segmented so that the server verifying a device's public key does not see the attestation keys — meaning Google cannot correlate attestation keys back to a device.

The operational consequence: **Google activated a new RKP root certificate on 1 February 2026, and all RKP-enabled devices must use it by 10 April 2026. Applications that verify key attestation and do not trust the new root will start failing.**

If your backend pins or hardcodes the attestation root, this is a live outage waiting for you. Many implementations do exactly that, following older tutorials. Two further notes from Google's own guidance: the chain is **longer** under online provisioning than it used to be and **is subject to change**, so do not hardcode a chain length; and the root is moving from RSA to ECDSA, so do not hardcode an algorithm either.

- <https://www.comviva.com/blog/safeguarding-cryptographic-keys-implementing-tee-and-strongbox-in-android-applications/>

### 5.4 What attestation does not prove

Two honest limits.

It proves properties of a **key**, not the trustworthiness of a **user**. An attested key on a genuine device in the hands of a fraudster is still a fraudster.

And the mechanism is a target. Tools exist that defeat hardware-backed key attestation by running a software KeyMint inside the real keystore daemon for selected apps, embedding AOSP's own reference trusted application and signing attestations with a supplied keybox — producing certificates generated the same way real hardware generates them, and therefore internally consistent. Attestation raises the bar considerably. It is not a wall, and a design that treats a single attestation result as dispositive is brittle. Feed it into a risk score alongside other signals; Chapter 13 covers how.

---

## Chapter 6: Choosing storage in practice

Now the applied chapter. This is where the most widely-repeated advice in Android development recently became wrong.

### 6.1 EncryptedSharedPreferences is dead

For years the recommended way to store a token on Android was `EncryptedSharedPreferences` from Jetpack Security Crypto (`androidx.security:security-crypto`), which wrapped `SharedPreferences` with Tink encryption and Keystore-held keys.

**Google deprecated the entire library in April 2025, at version 1.1.0-alpha07, with no further releases planned.** Google's own reference now states the replacements bluntly: `EncryptedSharedPreferences` → use `SharedPreferences`; `EncryptedFile` → use `java.io.File`; `MasterKey` and `MasterKeys` → use `javax.crypto.KeyGenerator` with the `AndroidKeyStore` instance.

Google said little about why, but the reasons are visible in the bug reports. The library had to paper over Android Keystore inconsistencies across manufacturer devices and OS versions. It performed synchronous cryptography on the calling thread, producing StrictMode violations. And "keyset corruption" exceptions plagued Crashlytics logs on specific OEM devices. Maintaining two parallel storage stacks, legacy encrypted preferences alongside the modern DataStore path, was not sustainable.

The execution left developers without clear guidance for a long stretch, and Google still does not publish a single authoritative document combining DataStore with Tink for secure local storage. That gap is why this chapter exists.

- <https://developer.android.com/reference/androidx/security/crypto/package-summary>
- <https://blog.includesecurity.com/2026/08/encryptedsharedpreferences-is-dead-heres-what-you-should-use-instead/>

### 6.2 Superseded advice, kept findable

If you arrived here searching for one of these, you are in the right place and the advice has moved.

> **`EncryptedSharedPreferences`, `EncryptedFile`, `MasterKey` — deprecated April 2025.** The whole Jetpack Security Crypto library was deprecated at 1.1.0-alpha07 with no further releases. Replacement in §6.3; why the original advice was misleading even when current in §6.4.

> **`SafetyNet Attestation` — retired.** Play Integrity is the only supported path. Chapter 9.

> **`UIWebView` — deprecated.** Use `WKWebView`, which runs content out of process. §16.6.

> **WHOIS-based domain email validation — discontinued 15 July 2025.** §8.5.

> **"MASVS L1 / L2 / R".** The verification levels left MASVS at v2.0.0 and became MASTG testing profiles: MAS-L1, MAS-L2, MAS-R. §3.2.

> **`MASTG-TEST-0044` and `MASTG-TEST-0087`** ("Make Sure That Free Security Features Are Activated") — deprecated v1 tests. Superseded by the atomic v2 tests listed in §19.6.

Stubs exist because readers arrive from three-year-old blog posts searching the old term, and because a book that silently rewrites its own advice is harder to trust than one that shows the change.

### 6.3 What to use instead

Three layers, each doing one job:

**Jetpack DataStore** for persistence. Asynchronous I/O through coroutines, type-safe with Proto DataStore, no main-thread blocking. Note carefully that **DataStore is not encrypted**. It is a persistence mechanism, not a security one.

**Google Tink** for encryption. `StreamingAead` encrypts at file level rather than per value, which performs better and avoids a class of problems that per-value encryption created.

**Android Keystore** for key protection, via `KeyGenerator` with the `AndroidKeyStore` provider, so that key material never enters your process.

Migration uses DataStore's `SharedPreferencesMigration` API to move existing values across. Two practical notes: the migration does **not** delete the old XML file, deliberately, so that a failed migration does not lose data — clear it yourself with `context.deleteSharedPreferences(...)` once you are confident. And if you cannot migrate now, a community fork maintains `EncryptedSharedPreferences` and `EncryptedFile` against current Tink versions. Treat that as a bridge with a deadline, not a destination. Its own documentation notes that Tink Android 1.18.0 dropped SDK 21 in favour of a minimum of SDK 23.

### 6.4 The uncomfortable question nobody asked

Here is the part that got lost in a decade of "use EncryptedSharedPreferences" advice, and it is stated most clearly by the maintainer of that community fork: **the existence of the library misled developers into believing plain `SharedPreferences` was inherently insecure, which was never true.**

Since Android 10, file-based encryption is enforced on device, and the app sandbox isolates your data from other applications. An attack that reads another app's `SharedPreferences` generally requires physical access to the device or an already-compromised device. If your threat model does not include those, encrypting your feature flags accomplished nothing except latency and a class of keyset-corruption crashes.

So decide by threat model rather than by reflex:

**Long-lived refresh tokens and credentials** deserve Keystore-backed keys, encrypted payloads, and `setUserAuthenticationRequired` where the user flow tolerates it. These are worth real protection because they are worth stealing and they last.

**Short-lived access tokens** are best held in memory for the session where your architecture allows. What is never written cannot be read off disk. Persist only what you must survive a process death.

**Feature flags, UI state, non-sensitive preferences** belong in plain DataStore. Encrypting them buys nothing.

**Anything you can avoid storing** should not be stored. This is the cheapest control in the entire book and the one most often skipped, because it requires a product conversation rather than a code change.

### 6.5 The leaks that are not about encryption

MASVS-STORAGE-2 exists because sensitive data escapes through channels that have nothing to do with your storage choice. Each of these is a real finding class:

**Logs.** A token in a debug log is a token on disk, and on Android any app with log access on older versions could read it. Strip logging from release builds and verify by inspecting the artifact, not by trusting a build flag.

**Backups.** Android Auto Backup and iCloud backup will happily copy your encrypted files somewhere the key does not exist, producing runtime crashes on restore — and will happily copy your *unencrypted* files somewhere an attacker can read them. Exclude sensitive data explicitly with backup rules; `isExcludedFromBackupKey` on iOS.

**Screenshots.** The OS captures your screen when the app backgrounds, for the recents UI. If a balance or a card number is on screen, it is now in a file. On Android use `FLAG_SECURE` and `setRecentsScreenshotEnabled`, plus `SecureFlagPolicy.SecureOn` for Compose dialogs, which people miss. On iOS use a covering view.

**The keyboard cache.** Predictive text remembers what users type into ordinary fields, including into fields that should never have accepted a secret. Use non-caching input types.

**Notifications.** A locked-screen notification showing a one-time code defeats the purpose of the one-time code.

**The clipboard.** On iOS the general pasteboard is shared and, historically, syncs across devices. Copying a password there is copying it to somewhere you do not control. Restrict to the local device, set an expiry, and clear after use.

**Process memory.** Nothing you can fully solve, but you can reduce the window: avoid holding secrets in long-lived `String` objects, prefer `CharArray` you can zero, and do not keep a decrypted blob resident for the app's lifetime.

---

### 6.6 How to implement it

#### Android: DataStore + Tink + Keystore

Three layers, per §6.2. The Keystore holds the key, Tink does the encryption, DataStore persists the result.

```kotlin
// 1. One-time: create a hardware-backed AES key that never leaves secure hardware.
private fun getOrCreateKey(alias: String): SecretKey {
    val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
    (keyStore.getEntry(alias, null) as? KeyStore.SecretKeyEntry)?.let { return it.secretKey }

    val spec = KeyGenParameterSpec.Builder(
        alias,
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
    )
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)              // AEAD, per Chapter 0.2
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setKeySize(256)
        // For a refresh token, require the user to have authenticated:
        // .setUserAuthenticationRequired(true)
        // .setInvalidatedByBiometricEnrollment(true)             // see Chapter 11.3
        .setIsStrongBoxBacked(true)                               // may throw; see below
        .build()

    return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        .apply { init(spec) }
        .generateKey()
}
```

**Handle the StrongBox failure explicitly**, because this is §4.2's decision in code:

```kotlin
val key = try {
    getOrCreateKey(ALIAS)                       // with setIsStrongBoxBacked(true)
} catch (e: StrongBoxUnavailableException) {
    // Deliberate, recorded fallback to TEE — not a silent downgrade.
    analytics.log("keystore_strongbox_unavailable")
    getOrCreateKeyWithoutStrongBox(ALIAS)
}

// Confirm what you actually got, rather than assuming:
val info = SecretKeyFactory.getInstance(key.algorithm, "AndroidKeyStore")
    .getKeySpec(key, KeyInfo::class.java) as KeyInfo
val level = info.securityLevel   // SECURITY_LEVEL_STRONGBOX / TRUSTED_ENVIRONMENT / SOFTWARE
```

Encrypting, with a fresh IV every time — §0.2's rule that a GCM nonce must never repeat:

```kotlin
fun encrypt(plaintext: ByteArray, key: SecretKey): ByteArray {
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.ENCRYPT_MODE, key)          // IV generated for us — do not supply one
    val ciphertext = cipher.doFinal(plaintext)
    return cipher.iv + ciphertext                  // store the IV alongside; it is not secret
}

fun decrypt(stored: ByteArray, key: SecretKey): ByteArray {
    val iv = stored.copyOfRange(0, 12)
    val ciphertext = stored.copyOfRange(12, stored.size)
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.DECRYPT_MODE, key, GCMParameterSpec(128, iv))
    return cipher.doFinal(ciphertext)              // throws if tampered — that is the point
}
```

**The wrong version, for contrast:**

```kotlin
// DON'T: CBC gives you no integrity, and a fixed IV leaks structure.
val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
cipher.init(Cipher.ENCRYPT_MODE, key, IvParameterSpec(ByteArray(16)))  // fixed IV — broken
```

Then persist the ciphertext with DataStore. Remember DataStore itself is not encrypted; you encrypt, then persist.

#### iOS: Keychain with the right accessibility class

```swift
func storeToken(_ token: Data, account: String) throws {
    // Remove any existing item first; SecItemAdd fails on duplicates.
    let deleteQuery: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account
    ]
    SecItemDelete(deleteQuery as CFDictionary)

    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecValueData as String: token,
        // WhenUnlocked: needs an unlocked device. ThisDeviceOnly: not in backups,
        // does not migrate to a new device. See Chapter 4.4.
        kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
    ]

    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else { throw KeychainError.unhandled(status) }
}
```

If background refresh needs the token while the device is locked, the considered change is `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` — **not** `kSecAttrAccessibleAlways`, which maps to no protection at all.

For a key that must never leave hardware, create it in the Secure Enclave — remembering from §4.3 that it is elliptic-curve only and does signing and key agreement rather than direct encryption:

```swift
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    [.privateKeyUsage, .biometryCurrentSet],   // "CurrentSet", not "biometryAny" — Chapter 11.3
    nil
)!

let attributes: [String: Any] = [
    kSecAttrKeyType as String: kSecAttrKeyTypeECSECPrimeRandom,
    kSecAttrKeySizeInBits as String: 256,
    kSecAttrTokenID as String: kSecAttrTokenIDSecureEnclave,
    kSecPrivateKeyAttrs as String: [
        kSecAttrIsPermanent as String: true,
        kSecAttrApplicationTag as String: "com.example.signing".data(using: .utf8)!,
        kSecAttrAccessControl as String: access
    ]
]

var error: Unmanaged<CFError>?
let privateKey = SecKeyCreateRandomKey(attributes as CFDictionary, &error)
```


#### Verify it

Code review does not tell you whether encryption is in the path you think it is. Check the artifact.

**Android.** Pull the file the app actually wrote and read it:

```
adb shell run-as com.example.app cat /data/data/com.example.app/shared_prefs/*.xml
adb shell run-as com.example.app ls -la /data/data/com.example.app/files/
```

**Pass:** base64 ciphertext, or binary that is not your token. **Fail:** readable JSON or a recognisable token string — which means your encryption layer is not on the write path, a common outcome when a migration half-succeeded.

Confirm the key is where you think:

```kotlin
val info = SecretKeyFactory.getInstance(key.algorithm, "AndroidKeyStore")
    .getKeySpec(key, KeyInfo::class.java) as KeyInfo
Log.d("keycheck", "securityLevel=${info.securityLevel}")   // STRONGBOX / TRUSTED_ENVIRONMENT / SOFTWARE
```

**Fail:** `SOFTWARE` on a flow you designed for hardware backing. That is §4.2's silent-fallback finding, showing up in a log line.

**iOS.** On the simulator, inspect the app container for plaintext:

```
xcrun simctl get_app_container booted com.example.app data
grep -rI "eyJ" <that path>          # a JWT begins "eyJ"
```

**Pass:** nothing. **Fail:** a token in a plist, a cache, or a log file.

### 6.7 Encrypting a local database

Chapter 6 covers tokens and preferences. Databases are the other half, and they are where most personal data actually lives.

**The default position:** on both platforms, app-private database files are already inside the sandbox and covered by platform storage encryption at rest (Chapter 0.4). For a great deal of app data, that is genuinely sufficient.

**When to add database encryption on top:** when your threat model includes a compromised or rooted device, when a regulator requires encryption of data at rest as a distinct control, or when the database holds something whose exposure would be individually serious — health records, financial history, message content.

**Android.** The standard route is **SQLCipher**, which provides a drop-in encrypted SQLite replacement and integrates with Room through a `SupportFactory`. Hold the passphrase in a Keystore-backed key rather than a constant — a hardcoded passphrase converts database encryption into an obfuscation exercise. Note the cost: SQLCipher adds binary size and a measurable performance overhead on large queries, so measure before committing.

**iOS.** Two options. SQLCipher works the same way. Or use **file-level Data Protection** by setting an appropriate protection class on the database file, which leans on the platform rather than adding a dependency — the trade-off being that your data is readable whenever the device is unlocked, which may be exactly what your app needs anyway.

**What database encryption does not solve.** The key has to be available for the app to read its own data, so on a device where an attacker can run code as your app, they can read the database through your app's own key. This raises cost against offline extraction and physical access. It does not defeat a live compromise. Be clear which of those you are buying.

---
