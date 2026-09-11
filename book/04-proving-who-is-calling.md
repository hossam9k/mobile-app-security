---
part: 04
last_verified: 2026-09-11
volatility: high
recheck_because: "Verdict semantics changed May 2025; App Attest signals change each WWDC"
---

# Part 4: Proving who is calling

## Chapter 9: Play Integrity — what it proves and what it does not

Attestation is the highest-value control most teams skip, because it moves the trust decision to your server and backs it with a cryptographic statement from the platform vendor rather than a claim from a client you do not control.

SafetyNet Attestation is fully retired. Play Integrity is the only supported path on Android.

### 9.1 The shape of the thing

Your app requests an **integrity token** from Google Play services. That token is encrypted and signed by Google. Your app sends it to your backend, your backend sends it to a Google server for decryption and verification, and Google returns a verdict payload. Your backend decides what to do with it, then tells the app.

Note where the decryption happens. The token is not something your app can read or forge, and the verdict arrives at your server from Google rather than from the device. That is what makes it worth more than any client-side root check.

The payload is plain-text JSON with a fixed structure:

```json
{
  "requestDetails":     { ... },
  "appIntegrity":       { ... },
  "deviceIntegrity":    { ... },
  "accountDetails":     { ... },
  "environmentDetails": { ... }
}
```

**Check `requestDetails` first**, before you look at anything else. It contains the package name and the nonce or request hash. If those do not match the request you issued, nothing else in the payload means anything — you may be looking at a replayed token from a different request or a different app.

### 9.2 Standard or classic — choosing properly

There are two request types and the choice is not cosmetic.

**Standard requests** suit any app and are what most developers should use. Latency is a few hundred milliseconds on average, reliability is high, and importantly, Google Play takes on some of the protection against replay and token exfiltration. They need a two-step flow: **prepare the token provider well in advance** (at app launch or in the background), then **request a token on demand** when you make the server call you want to verify.

**Classic requests** are more expensive to make, and **you** are responsible for correctly implementing protection against exfiltration and certain attack classes. Your server issues the nonce. They are intended as an occasional one-off check on a high-value action, not as a per-request mechanism.

The practical guidance: standard for nearly everything, classic for infrequent high-confidence checks where you want a server-issued nonce and are prepared to own the replay protection.

**Operational limits to design around.** Practitioner reporting puts classic requests around 5 per minute per app instance, standard warm-ups similarly, with a default daily ceiling near 10,000 token requests and 10,000 decodes *(reported)*. These figures are not a stable published table — verify yours in Play Console and request an increase early if you need one, rather than discovering the ceiling on launch day.

**One trap that costs people hours:** never decrypt the same token twice. Repeated decryption returns **cleared verdicts** — the device recognition verdict comes back empty, and the app recognition and licensing verdicts come back `UNEVALUATED`. If you are seeing mysteriously empty verdicts in production, check whether a retry path is decrypting a token that was already consumed.

### 9.3 Reading the verdicts like an engineer, not a bouncer

The device recognition verdict differentiates three labels, and Google strengthened all of them in May 2025:

**`MEETS_STRONG_INTEGRITY`** — on Android 13 and later, this now additionally requires a **security update installed within the last 12 months**.

**`MEETS_DEVICE_INTEGRITY`** — on Android 13 and later, this now **requires a hardware-backed, positive verified boot verdict**.

**`MEETS_BASIC_INTEGRITY`** — the weakest label, indicating a device that passes minimal checks.

The same May 2025 change reduced the device signals needed for the default verdict by roughly **90%** and improved worst-case latency by up to **80%**, while explicitly increasing the differentiation between the three labels. Verified boot became the anchor.

**Here is the consequence almost everyone gets wrong.** `MEETS_STRONG_INTEGRITY` failing does **not** mean the device is compromised. On Android 13+, it most often means a legitimate user has not received a security update in a year — which is extremely common on older or regionally-supported hardware, and entirely outside that user's control.

So treat the labels as a gradient, not a gate:

**Strong integrity** is a bonus signal for your very highest-risk actions. Never a baseline requirement, or you will lock out real customers on older devices.

**Device integrity** is a reasonable expectation for sensitive flows on modern hardware. When it fails, route the session into a higher-risk bucket rather than blocking: allow browsing, require step-up authentication for anything sensitive, cap limits, monitor.

**Basic integrity only** means treat with suspicion and escalate scrutiny — not refuse service.

### 9.4 How to roll it out without breaking your users

Google's own documentation recommends the sequence, and it is right: **implement without enforcement first.**

Ship the integration, collect verdicts from your real install base, and look at the actual distribution. Only then estimate the impact of each enforcement option and adjust your anti-abuse strategy accordingly. Enforcing on day one against an unknown distribution is how a team blocks a measurable slice of paying customers and finds out from app store reviews.

Then enforce incrementally, starting with your highest-value flows and leaving general use alone.

When you do refuse or restrict something, give the user a route out. Library version 1.5.0 (August 2025) added remediation dialogs, `GET_INTEGRITY` and `GET_STRONG_INTEGRITY`, precisely so that a user can fix their own problem rather than hitting a dead end that reads "device not supported."

- <https://developer.android.com/google/play/integrity/overview>
- <https://developer.android.com/google/play/integrity/standard>
- <https://developer.android.com/google/play/integrity/improvements>
- <https://developer.android.com/google/play/integrity/verdict>

### 9.5 The honest limits

Play Integrity proves that a request comes from your genuine, Play-installed, unmodified app binary, on a device meeting a stated integrity level, associated with a licensed account.

It does **not** prove that the user is legitimate. It is not a jailbreak oracle. It depends on Google Play services being present and functional, which excludes some legitimate devices and markets entirely. And independent commentary reasonably notes that quota and threshold behaviour is a real constraint at scale, which is part of why commercial alternatives exist.

Use it as one strong input to a backend risk decision. Not as the decision.

---

## Chapter 10: App Attest — Apple's model

Apple solves the same problem with a different structure, and the difference is worth understanding because it shapes your integration.

### 10.1 Attest once, assert often

The flow has two distinct phases, and conflating them is the most common implementation error.

**Registration, once per key.** Your app generates a key in the Secure Enclave and gets a key ID. It asks your server for a challenge. It calls `attestKey(keyId, clientDataHash:)`, which **contacts Apple's servers**. App Attest fetches the key pair along with attestation data derived from the Secure Enclave, which is a snapshot of the device's hardware properties taken at boot and cannot be modified. Apple validates the device data and returns an attestation. Your server validates that attestation and **stores the public key** against that user.

**Ongoing use, per protected request.** Your app calls `generateAssertion(keyId, clientDataHash:)`. Assertions are **generated locally with no round trip to Apple**. Your app embeds the assertion in the request payload, and your server verifies it.

That asymmetry dictates the design: attestation contacts Apple, assertions do not. Attest rarely. Assert as needed, on the requests that matter.

Assertions still perform real cryptographic work, so do not generate them in tight loops or on hot lifecycle paths. Use them for sensitive payloads: authentication-related requests, premium content access, transactions.

### 10.2 What your server must do

Three checks, and the third is the one people skip.

**Verify the assertion signature** using the authenticator data, the server challenge, and the public key you stored during attestation.

**Confirm the authenticator data contains the hash of your app ID.** This binds the assertion to your application.

**Track the assertion counter per key and require it to be strictly increasing.** Without this, assertions are replayable — and you have built an elaborate signature check that does not stop the attack it exists to prevent. This is the single most common App Attest implementation bug.

On the nonce: the challenge can be a server-issued random value, or predictably reconstructible data such as a request digest or timestamp. What matters is that your server can independently reconstruct it for that specific request, which is what eliminates replay.

### 10.3 What changed in 2026

WWDC26 Session 201 introduced material additions:

A **fraud metric** you can incorporate into your risk pipeline, rather than treating attestation as a binary.

**New signals in iOS 27** to strengthen validation.

**App Attest on macOS 27**, extending the model beyond iOS.

And one piece of operational guidance that deserves quoting because it prevents a real customer-harming bug: **do not reject every new key for an existing user.** Reinstalls, device migrations and restores legitimately produce new keys. A backend that treats "this user presented a key I have not seen" as fraud will punish honest customers for changing phones. Handle it as a re-registration event with appropriate risk scoring.

- <https://developer.apple.com/videos/play/wwdc2026/201/>

### 10.4 Errors you will actually meet

`DCError.invalidKey` and `serverUnavailable` are the two you will see, and they want different handling. For `invalidKey`, discard the key and generate a fresh one before retrying. For `serverUnavailable`, retry with the **same** key and the same client data hash, per Apple's own guidance. Cap your retries and back off.

Two known rough edges, from developer forum reports rather than documentation: a small subset of devices fail `attestKey` **persistently** with `invalidKey` *(reported)*, surviving reinstall, reboot and app update; and Apple has not confirmed whether throttling can surface as `invalidKey` rather than as a distinct error. Apple does not publish rate limits, and there is no documented process to request accommodation for a large-scale rollout.

The practical response: **stage your rollout.** Do not trigger simultaneous attestation across your entire install base. Use exponential backoff, honour `retryAfter`, and design a grace mode that lets a user continue with elevated scrutiny rather than being locked out because attestation failed on their particular handset.

### 10.5 Limits, and when to actually check

Apple publishes no thresholds for App Attest, which makes planning harder than it should be. Here is what is known, with the confidence level attached.

| Limit | Value | Confidence |
|---|---|---|
| Daily quota | Not publicly disclosed. No official SLA or quota documentation | Apple |
| Rate limit | Roughly 10–20 requests per second | *(reported)* — community observation, no Apple guarantee |
| `attestKey()` calls | Once per key. In practice that means once per app installation, since a fresh install generates a new key | Apple |
| Quota increase | Not available. Apple offers no mechanism to request one | Apple |
| Rollout | Onboard gradually, a percentage of users at a time, to avoid hitting undocumented limits | Apple guidance and practice |

Two notes on the `attestKey()` row, because the precise wording matters. The rule is **once per key**, and "once per installation" is the operational consequence rather than the rule itself. A reinstall, a device migration or a restore legitimately produces a new key — and per Chapter 10.3, Apple's own 2026 guidance is explicit that you should **not** treat a new key from an existing user as fraud.

#### When to check integrity

Because quotas are undocumented on iOS and metered on Android, you cannot attest everything. This table is the discriminator, and it applies to both platforms.

| User action | Check integrity? | Why |
|---|---|---|
| Payment or checkout | **Yes** | Financial transaction; highest risk |
| Add a payment method | **Yes** | Financial data at risk |
| Change password or email | **Yes** | The classic account-takeover vector |
| Delete account | **Yes** | Irreversible |
| Initial login | **Yes** | This is where the session is established |
| Product browsing | No | Low risk, high volume, would burn quota for nothing |
| Search | No | No sensitive data involved |
| View cart | No | No state change |
| View profile | No | **Already behind authentication** |

That last row is the most useful discriminator in the table, and it generalises: **if an action is already gated by something you trust, attesting it again buys little.** Attestation earns its cost at the boundary where trust is established or where state changes irreversibly, not on every screen behind the login.

### 10.6 The shared limit

Both platforms' attestation proves something about the **app and device**, not about the **user**. Apple states directly that the mechanism cannot guarantee your app is running on a system that is not jailbroken, which could enable an attacker to circumvent your checks.

Attestation belongs in a risk score, alongside authentication, account history, behaviour and velocity. Chapter 13 is about building that.

---

## Chapter 11: Biometrics, done so they cannot be bypassed

Biometric authentication is the control where the gap between a correct and an incorrect implementation is largest, and where the incorrect implementation looks identical to the user.

### 11.1 Decorative versus real

There are two ways to write biometric authentication. They look identical to the user. One of them stops an attacker and one does not.

**The decorative implementation.** You call the biometric prompt. It calls back with success. You branch on that boolean and unlock the feature.

An attacker with Frida hooks the callback and returns success without any biometric ever occurring. Total bypass, achievable in minutes, and MASWE-0020 exists precisely to name it.

**The real implementation.** You tie the biometric to a **cryptographic operation**. The prompt unlocks a Keystore or Keychain key that requires user authentication, and you use that key to sign or decrypt something your server verifies.

Now hooking the callback accomplishes nothing. The attacker can make your UI say "authenticated," but they cannot produce the signature, because the key is in hardware and hardware will not release it without a genuine authentication that Gatekeeper (or the Secure Enclave) vouches for.

That is the whole chapter, mechanically. Everything else is detail.

On Android, that means `BiometricPrompt` with a **`CryptoObject`** backed by a key created with `setUserAuthenticationRequired(true)`. MASTG-BEST-0036 names this directly: use cryptographic binding for biometric authentication.

On iOS, it means `LocalAuthentication` with a Secure Enclave key whose `SecAccessControl` requires biometry — and remember that access control lists are evaluated **inside** the Secure Enclave and released only when their constraints are met.

### 11.2 Biometric classes, and why Class 3 matters

Android grades biometric modalities by strength. **Class 3 (`BIOMETRIC_STRONG`)** is the tier strong enough to gate cryptographic operations — meaning it is the only tier that can back a `CryptoObject`. **Class 2 (`BIOMETRIC_WEAK`)** accepts weaker modalities and cannot.

For anything financial, require Class 3. MASTG-BEST-0031 says the same. If you accept Class 2 for a payment confirmation, you have accepted a modality the platform itself considers insufficient to protect a key.

### 11.3 The enrollment problem nobody thinks about

Here is a scenario worth sitting with. An attacker steals an unlocked phone, or a phone whose passcode they have observed. They go into settings and **add their own fingerprint**. Your app's biometric prompt now accepts them.

The defence is to invalidate biometric-bound keys when the enrolled set changes. On Android that is **`setInvalidatedByBiometricEnrollment(true)`**. On iOS it is **`kSecAccessControlBiometryCurrentSet`** rather than `biometryAny` — the "current set" wording is the whole point, and Apple documents that access can be limited by specifying that Face ID or Touch ID enrolment has not changed since the item was added, precisely to prevent an attacker adding their own fingerprint.

MASWE-0022 covers this and it is one of the most commonly missed weaknesses in the catalogue. MASTG-BEST-0037 is the corresponding practice.

The cost is real: a user who legitimately adds a fingerprint has to re-enrol in your app. For a banking app that is the correct trade. Decide it deliberately rather than by omission.

### 11.4 Fallbacks, and the tension inside them

Users lose fingerprints to bandages, cuts and cold weather; faces to sunglasses, masks and bad light. An app with no fallback locks people out of their own accounts.

But MASWE-0021 names the opposite failure: **fallback to non-biometric credentials allowed for sensitive transactions.** If your "use passcode instead" path bypasses the cryptographic binding, you have reintroduced the bypass through the back door.

Resolve it by making the fallback *equivalent in strength*, not weaker. Device credential fallback that still unlocks a hardware key is fine. Server-side step-up authentication is fine. A fallback that just sets `authenticated = true` is not a fallback; it is the vulnerability with a friendlier label.

Also require **explicit user confirmation** for high-value actions (MASTG-BEST-0038). Passive face recognition that authorises a transfer the moment the user glances at their phone is a usability decision with a security consequence.

### 11.5 Where to spend the friction

Require biometrics for: payments and transfers, adding a payee, changing a password or email address, viewing full card details, disabling security features, and high-value account changes.

Do **not** require them for: app launch on every cold start, browsing, reading, or anything a user does twenty times a day.

Friction spent where it does not buy security is friction users route around — by disabling the feature, by choosing a weaker option, or by abandoning the flow. A security control that users switch off protects nothing. This is not a UX concession; it is a security argument.

---

### 11.6 How to implement it

The whole point of §11.1: bind the prompt to a cryptographic operation so hooking the callback gains an attacker nothing.

#### Android: BiometricPrompt with a CryptoObject

```kotlin
// 1. A key that only exists while the user is authenticated, and dies if
//    the enrolled biometric set changes (Chapter 11.3).
val spec = KeyGenParameterSpec.Builder(
    "biometric_key",
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)
    .setInvalidatedByBiometricEnrollment(true)     // the stolen-phone defence
    .build()

// 2. Require Class 3. Class 2 cannot back a CryptoObject at all.
val promptInfo = BiometricPrompt.PromptInfo.Builder()
    .setTitle("Confirm transfer")
    .setSubtitle("Authenticate to authorise 5,000 EGP to Ahmed")
    .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG)
    .setNegativeButtonText("Cancel")
    .build()

// 3. Hand the Cipher to the prompt. This is the binding.
val cipher = Cipher.getInstance("AES/GCM/NoPadding").apply {
    init(Cipher.ENCRYPT_MODE, getBiometricKey())
}

biometricPrompt.authenticate(promptInfo, BiometricPrompt.CryptoObject(cipher))
```

In the callback, **use the crypto object** — do not merely observe that authentication succeeded:

```kotlin
override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
    // The cipher is now unlocked. Produce something the server verifies.
    val payload = result.cryptoObject?.cipher?.doFinal(transferRequest.toByteArray())
    api.authoriseTransfer(payload)   // server checks it; the client decides nothing
}
```

**The wrong version, which is extremely common:**

```kotlin
// DON'T: no CryptoObject, no server verification. One Frida hook and this returns success.
override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
    isAuthenticated = true
    performTransfer()
}
```

Check availability before you offer it, and handle the invalidation case, because a user who re-enrolled will hit `KeyPermanentlyInvalidatedException` on first use — that is the control working, and your code must treat it as "re-register", not as a crash:

```kotlin
when (BiometricManager.from(context)
        .canAuthenticate(BiometricManager.Authenticators.BIOMETRIC_STRONG)) {
    BiometricManager.BIOMETRIC_SUCCESS -> showBiometricPrompt()
    BiometricManager.BIOMETRIC_ERROR_NONE_ENROLLED -> offerEnrolment()
    else -> fallBackToServerSideStepUp()    // equivalent strength — Chapter 11.4
}
```

#### iOS: LocalAuthentication bound to a Secure Enclave key

Reuse the `SecAccessControl` from §6.5 with `.biometryCurrentSet`, then sign with it. Because the access control is evaluated **inside** the Secure Enclave, the biometric prompt appears as part of using the key — there is no boolean for an attacker to intercept:

```swift
// Using the key triggers the biometric prompt; the signature is the proof.
var error: Unmanaged<CFError>?
guard let signature = SecKeyCreateSignature(
    privateKey,                                    // Secure Enclave, biometryCurrentSet
    .ecdsaSignatureMessageX962SHA256,
    transferRequestData as CFData,
    &error
) as Data? else {
    // User cancelled, or biometrics changed and the key is gone.
    return fallBackToServerSideStepUp()
}
try await api.authoriseTransfer(request: transferRequestData, signature: signature)
```

That is the shape to aim for on both platforms: **the server verifies a signature it could only receive if a genuine authentication happened.**

---


#### Verify it

The whole point of §11.1 is that a hooked callback should gain an attacker nothing. Test exactly that.

**Hook the success callback and see what happens:**

```javascript
// frida -U -f com.example.app -l bypass.js
Java.perform(function () {
  var Prompt = Java.use("androidx.biometric.BiometricPrompt$AuthenticationCallback");
  Prompt.onAuthenticationSucceeded.implementation = function (result) {
    console.log("[*] forcing success");
    return this.onAuthenticationSucceeded(result);
  };
});
```

**Pass:** the UI may report success, but **the protected action still fails**, because no signature was produced and your server rejected the request. **Fail:** the transfer completes — which means you branched on a boolean and §11.1's decorative implementation is what you shipped.

**Then test enrollment invalidation.** Add a new fingerprint in device settings and use the feature again. **Pass:** `KeyPermanentlyInvalidatedException`, handled as a re-registration prompt. **Fail:** it still works, meaning `setInvalidatedByBiometricEnrollment` is not set and `MASWE-0022` applies.

Relevant tests: `MASTG-TEST-0018`, `0326`, `0328`.

## Chapter 12: The backend as the only real arbiter

Every control so far degrades gracefully when it fails. This one does not. Get it wrong and nothing else in the book matters.

### 12.1 The non-negotiables

Six rules. Unlike most of this book, these do not have a "it depends on your threat model" caveat.

**Validate everything server-side.** Prices, quantities, entitlements, balances, permissions, discounts, limits. The client proposes; the server decides. If your API accepts a price from the client, you do not have a pricing bug, you have a free store.

**Never trust a client-supplied identity claim.** Derive the acting user from the session token, never from a field in the request body. `{"userId": 12345}` is a suggestion.

**Bind tokens so they are not portable.** A bearer token that works from anywhere is a token worth stealing. Bind it to a device key, an attestation key, or a session, so that a stolen token is useless off the device it was issued to. This single measure devalues a whole category of attack.

**Rate limit per account and per device**, not only per IP. IP-based limiting is defeated by any residential proxy pool, which costs an attacker very little.

**Log security decisions with enough context to investigate later**, and never log the secrets themselves. "Denied step-up for user X on device Y at time Z because attestation returned basic integrity" is useful. The token that was presented is a liability.

### 12.2 Attestation as a signal, not a switch

The design that scales is a **risk score**. Attestation contributes to it; so do account age, device history, behavioural velocity, geography, transaction size, and time since last authentication.

The reason to build it this way is not elegance. A single binary signal is a single point of failure: when it is defeated, and Chapter 5 showed that attestation can be, you have nothing. A score degrades. Lose one input and the others still discriminate.

It also gives you proportionate responses rather than a binary. Instead of allow-or-block, you get: allow silently; allow with step-up authentication; allow with a lower limit; allow but flag for review; queue for manual review; refuse. Most fraud is better handled by the middle options, because they impose cost on the attacker without punishing the false positive.

### 12.3 The Backend-for-Frontend pattern

There is an architectural decision that makes most of this chapter easier, and it deserves naming because teams often reach it late.

A **Backend-for-Frontend**, or **BFF**, is a thin backend layer sitting between your mobile app and your core services. It owns every sensitive secret and makes every trust decision.

**Use it when** your app talks to third-party APIs, processes payments, or handles authentication. In practice that is most apps.

**How it works:**

1. The app authenticates to the BFF using short-lived tokens held in hardware-backed storage (Chapter 6).
2. The **BFF holds all third-party API keys**, payment credentials and service secrets. None of them ship in the app.
3. The BFF validates every request: authentication, authorization, input validation, rate limiting, integrity verification.
4. The BFF proxies to upstream services, attaching the real credentials **server-side**.

**What that buys you**, and each of these solves a problem that appears elsewhere in this book:

| Benefit | The problem it solves |
|---|---|
| Third-party keys never leave the server | Chapter 15.2's "restricted" class has nowhere safe to live on a client. The BFF is that place |
| Secrets rotate without an app release | Otherwise rotating a key means a store review and users who never update |
| Trust decisions happen where an attacker cannot reach them | Chapter 1's principle, expressed as architecture rather than discipline |
| One place for logging, auditing and rate limiting | Chapter 12.1's rate limiting and Chapter 24's incident logging get a single home |

**The honest cost.** A BFF is another service to build, deploy, monitor and secure. It adds a network hop and a latency budget. For a small app talking only to your own well-designed API, it is over-engineering. The question to ask is whether you currently have any third-party key in the client that you wish you did not — if the answer is yes, you already need a BFF and are paying for its absence in a different currency.

### 12.4 One test for any design

Ask this of every authenticated endpoint you own:

> If an attacker replays a valid request from a different device, what stops them?

If the answer is "nothing," you have found your next piece of work, and it is more important than anything on the client. Token binding, attestation assertions, and nonce or counter checks are the three mechanisms that answer that question properly.

### 12.5 Risk scoring, in practice

Chapter 12.2 argues for a risk score rather than a binary. Here is what one actually looks like, so the argument is concrete.

```kotlin
data class SecuritySignals(
    val attestationPassed: Boolean,
    val deviceIntegrityLevel: String,     // STRONG / DEVICE / BASIC / NONE
    val rootDetected: Boolean,
    val hookingDetected: Boolean,
    val debuggerDetected: Boolean,
    val emulatorDetected: Boolean
)

data class UserHistory(
    val accountAgeDays: Int,
    val knownDevice: Boolean,
    val failedAuthLast24h: Int,
    val transactionsLast1h: Int
)

/** Higher is riskier. Tune the weights against your own fraud data, not mine. */
fun calculateRiskScore(
    signals: SecuritySignals,
    history: UserHistory,
    amountMinorUnits: Long
): Int {
    var score = 0

    // Client-reported signals: inputs, never verdicts (Chapter 14.2)
    if (!signals.attestationPassed)          score += 40
    when (signals.deviceIntegrityLevel) {
        "NONE"  -> score += 30
        "BASIC" -> score += 20
        "DEVICE" -> score += 0
        "STRONG" -> score -= 5          // a small bonus, not a requirement
    }
    if (signals.hookingDetected)             score += 35
    if (signals.debuggerDetected)            score += 25
    if (signals.rootDetected)                score += 10   // deliberately low: often legitimate
    if (signals.emulatorDetected)            score += 15

    // Account and behavioural signals: these are yours, so trust them more
    if (history.accountAgeDays < 7)          score += 20
    if (!history.knownDevice)                score += 15
    score += history.failedAuthLast24h * 5
    if (history.transactionsLast1h > 5)      score += 15
    if (amountMinorUnits > HIGH_VALUE)       score += 20

    return score.coerceIn(0, 100)
}
```

Then map the score to a **graduated response**, which is the entire point:

```kotlin
when (calculateRiskScore(signals, history, amount)) {
    in 0..24  -> allow()
    in 25..49 -> allowWithStepUp()        // biometric confirmation (Chapter 11)
    in 50..74 -> allowWithReducedLimit()  // or queue for review
    else      -> denyAndFlagForReview()
}
```

Three design points worth taking from this.

**Root detection carries a low weight on purpose.** Rooted devices are common and frequently legitimate. Weighting root heavily is how you build a system that punishes power users and misses actual fraud.

**Server-derived signals outweigh client-reported ones.** Account age and failed-authentication counts come from your own database, so an attacker cannot forge them. Everything in `SecuritySignals` arrives from a client you do not control, which is why no single one of them is decisive.

**Tune the weights against real outcomes.** The numbers above are a starting shape, not a recommendation *(reasoned)*. A score that has never been compared against confirmed fraud is a guess with arithmetic on top.

#### Impossible travel

One cheap, high-signal backend check: did this account just move faster than physically possible?

```kotlin
data class GeoLocation(val latitude: Double, val longitude: Double, val timestamp: Long)

fun detectImpossibleTravel(current: GeoLocation, previous: GeoLocation?): Boolean {
    if (previous == null) return false

    val distanceKm = haversineDistance(
        current.latitude, current.longitude,
        previous.latitude, previous.longitude
    )
    val hours = (current.timestamp - previous.timestamp) / 3_600_000.0

    // 900 km/h ≈ commercial flight. Anything faster is not travel.
    return distanceKm > hours * 900
}

private fun haversineDistance(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Double {
    val r = 6371.0                                  // Earth radius, km
    val dLat = Math.toRadians(lat2 - lat1)
    val dLon = Math.toRadians(lon2 - lon1)
    val a = sin(dLat / 2).pow(2) +
            cos(Math.toRadians(lat1)) * cos(Math.toRadians(lat2)) * sin(dLon / 2).pow(2)
    return r * 2 * atan2(sqrt(a), sqrt(1 - a))
}
```

**Prefer backend-side IP geolocation over device GPS for this.** It needs no permission, it is harder for a user to spoof casually, and per Chapter 18.2 it keeps you out of a location-data declaration you would otherwise have to make and justify. Use coarse location if you must use the device at all.

---
