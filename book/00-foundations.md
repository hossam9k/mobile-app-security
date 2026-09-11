---
part: 00
last_verified: 2026-09-11
volatility: low
recheck_because: "Principles, not versions"
---

# Part 0: Foundations

You need five things before the rest of the book makes sense: the vocabulary, enough cryptography to make decisions, how authentication actually works, what the platforms protect for free, and how to think about threats systematically. That's this part.

---

## Chapter 0.1: The vocabulary

Security writing is dense with terms that sound interchangeable and aren't. Get these straight now and the rest of the book reads easily.

### The three properties you're protecting

Security protects three things. Naming which one a control protects is the fastest way to tell whether it is the right control.

**Confidentiality** means only the right people can read the data. Encryption gives you this.

**Integrity** means nobody changed the data without you noticing. Hashes, message authentication codes and signatures give you this.

**Availability** means the service works when users need it. It's why a pinning mistake that disconnects every user is a *security* failure, not just an outage — you broke a security property.

You'll see these called the CIA triad. When you evaluate a control, ask which of the three it actually protects. A lot of confused design comes from assuming encryption gives you integrity, or that a signature keeps data secret. Neither is true.

### Authentication versus authorization

These two words get used interchangeably in conversation. They are different jobs, and they fail separately.

**Authentication** answers "who are you?" Logging in, biometrics, a token that proves identity.

**Authorization** answers "are you allowed to do this?" Whether *this* authenticated user may read *that* record.

They fail differently and they fail independently. An app with perfect authentication and no authorization lets any logged-in user read every other user's data by changing an ID in a request. That bug class is extremely common and extremely serious, and it lives entirely on the server.

### Threat, vulnerability, risk

A **threat** is something bad that could happen: someone steals a session token.

A **vulnerability** is the weakness that allows it: the token is stored in plaintext.

**Risk** combines how likely it is with how much it would hurt.

Why bother distinguishing them? Because you have limited time, and risk is what you prioritise on. A severe vulnerability nobody can reach matters less than a mild one on your login screen.

### Attack surface, threat model, defence in depth

Your **attack surface** is every point where untrusted input or an untrusted actor meets your code: network responses, deep links, intents, WebView content, the clipboard, the camera, files a user picks, notifications, IPC from other apps.

A **threat model** is a structured answer to "what could go wrong here, and what do we do about it?" Chapter 0.5 shows you how to build one.

**Defence in depth** means layering controls so that one failure isn't total. The key word is *independent*: three controls that all fail when the device is rooted are one control wearing three hats.

### Client, server, and why it matters here

Your **client** is the app on the user's device. Your **server**, often called the backend, is the code you run.

The single most important sentence in this book: **you control the server; you do not control the client.** Everything in Part 1 follows from that.

### Terms you'll meet constantly

A quick pass through the words that appear on almost every page from here on.

**Plaintext** is data before encryption; **ciphertext** is after.

A **key** is the secret that makes encryption work. **Key material** means the actual bytes of a key.

A **nonce** is a "number used once" — a value you include in a request so an old copy of that request can't be reused. **Replay** is what happens when you don't.

**IPC** is inter-process communication: mechanisms that let separate apps or processes talk. On Android that's intents, content providers, services and broadcasts.

**Hooking** is replacing a function's behaviour at runtime, without changing the file on disk. It's how most client-side security gets bypassed.

**Rooting** (Android) and **jailbreaking** (iOS) mean removing the OS restrictions that normally keep apps isolated from each other and from the system.

**Attestation** is a cryptographic statement from a trusted party about the state of something — usually "this really is a genuine app on a genuine device."

---

## Chapter 0.2: Cryptography you actually need

You do not need to implement cryptography. You need to choose and use it correctly, and to recognise when someone else got it wrong. That's a much smaller topic, and this chapter is all of it.

**The first rule: never write your own.** Use the platform's implementation, or Google's Tink. Cryptographic code that looks right and is subtly wrong is the norm, not the exception, and the bugs are invisible in testing.

### Symmetric encryption

One key encrypts and decrypts. Fast, and what you use for bulk data.

The algorithm you want is **AES**. But AES alone isn't a decision — you also choose a **mode**, and the mode is where things go wrong.

**AES-GCM** is what you should use. GCM is an **AEAD** mode, short for Authenticated Encryption with Associated Data. That means it gives you confidentiality *and* integrity together. If someone tampers with the ciphertext, decryption fails loudly instead of returning garbage you then trust.

**AES-CBC** encrypts but does **not** authenticate. Use it and an attacker can modify ciphertext in ways that change the plaintext predictably. If you must use CBC, you have to add a MAC yourself, correctly, in the right order — which is exactly the kind of thing people get wrong. Prefer GCM.

**AES-ECB** is broken for anything real. It encrypts identical blocks to identical ciphertext, so structure leaks straight through. If you find ECB in your codebase, that's a finding. `MASTG-TEST-0232` and `MASTG-DEMO-0058` exist for exactly this.

**The IV/nonce rule that catches everyone.** Modes need an **initialization vector** or nonce — a value that makes the same plaintext encrypt differently each time. It doesn't need to be secret, but with GCM it must **never repeat under the same key**. Reuse a GCM nonce and you don't just leak data, you can leak the authentication key itself. Always generate it randomly per operation and store it alongside the ciphertext. Never hardcode it, never use a counter you might reset, never reuse "just for this one case." `MASTG-TEST-0309` and `0310` test for this, and `MASWE-0007` covers it.

### Asymmetric encryption

Two mathematically related keys: a **public key** you can share freely and a **private key** you protect. Anyone can encrypt to your public key; only your private key decrypts. Or: your private key signs, and anyone with your public key verifies.

Asymmetric crypto is slow, so it's used for small things — signing, key exchange, encrypting a symmetric key which then does the bulk work. That last pattern is called **hybrid encryption** and it's how TLS works.

The algorithms: **RSA** is the old standard, needs large keys (2048 bits minimum, 3072+ preferred). **Elliptic curve** (ECDSA for signing, ECDH for key agreement) gives equivalent strength with much smaller keys and better performance. Modern platforms prefer EC, and Apple's Secure Enclave supports **only** elliptic curve keys, which is a constraint you'll meet in Chapter 4.

### Hashing

A **hash** turns input of any size into a fixed-size fingerprint, one way. You can't reverse it. Change one bit of input and the output changes completely.

Use **SHA-256** or better. **MD5 and SHA-1 are broken** for security purposes — attackers can construct collisions, meaning two different inputs with the same hash. They're fine as non-security checksums; they are findings anywhere security depends on them (`MASWE-0008`).

**Hashing is not encryption.** Hashing is one-way and has no key. If you "hashed" something you need to read back later, you've lost it.

### Password hashing is a different problem

Here's a distinction that trips up a lot of engineers: general-purpose hashes are designed to be **fast**, which is exactly wrong for passwords, because fast means an attacker can try billions of guesses.

For passwords, use a **deliberately slow** function: **Argon2** (preferred), **scrypt**, **bcrypt**, or **PBKDF2** with a high iteration count. These are called key derivation functions, and they take a **salt** — a random per-password value that stops an attacker from precomputing results for common passwords.

Note that this is almost always a *server* concern. Your app should send the password over TLS and let the backend hash it. An app that hashes a password locally and sends the hash has just made the hash the password.

`MASWE-0014` covers improper key derivation.

### Message authentication codes and signatures

A **MAC** proves data wasn't modified *and* came from someone holding the shared key. **HMAC-SHA256** is the standard choice. Note that a MAC requires both parties to share a secret, so it can't prove *which* party — that's fine for client-server, useless for non-repudiation.

A **digital signature** uses asymmetric crypto: you sign with a private key, anyone verifies with the public key. This does prove origin, which is why app signing, JWT verification and attestation all use signatures.

**The verification trap:** generating a signature correctly and *verifying* it correctly are separate problems, and verification is where bugs live — accepting a token whose signature you didn't actually check, or accepting `alg: none`, or verifying against a key the attacker supplied. `MASWE-0011` is "improper verification of cryptographic signature" and it exists because this happens a lot.

### Randomness

Cryptography needs unpredictable random numbers. Your language's default random number generator is usually **not** suitable — it's designed for speed and statistical distribution, not unpredictability, and its output can often be predicted from a few samples.

Use `SecureRandom` on Android and `SecRandomCopyBytes` or `CryptoKit` on iOS. Never seed a secure generator with something predictable like a timestamp — that throws away the entire property you wanted. `MASWE-0012`, `MASTG-TEST-0204`, `MASTG-BEST-0001`.

### Key lifecycle

Keys have a life, and each stage is a place to fail (`MASVS-CRYPTO-2`):

**Generation** — in secure hardware where possible, with a secure random source, at an adequate size.

**Storage** — in the platform keystore, never in your source code, never in your app package. A hardcoded key is not a key; it's a public constant with extra steps. `MASWE-0003`, `MASWE-0004`.

**Use** — restricted to the purpose you generated it for. A key that both signs and encrypts creates attack paths that neither would alone (`MASTG-TEST-0307`).

**Rotation** — a plan for replacing a key without losing access to data encrypted under the old one. Most apps have no plan, which is why `MASWE-0015` exists.

**Destruction** — actually removed when it's no longer needed, including on logout.

### What to take away

Use AES-GCM for data, SHA-256 for hashes, Argon2 or bcrypt for passwords (server-side), elliptic curve for signing, a secure random generator always, and the platform keystore for keys. Never write your own primitives. Never reuse a GCM nonce. Never trust a signature you didn't verify properly.

That's enough cryptography to make good decisions for years.

---

## Chapter 0.3: Authentication, sessions and tokens

Most mobile security work touches authentication, and most mobile authentication bugs come from a handful of misunderstandings. This chapter clears them.

### What your app is holding

After a user logs in, your app holds something that proves the session. Usually two things:

An **access token** — short-lived (minutes to an hour), sent with each API request. Short life is the point: if it leaks, the window is small.

A **refresh token** — long-lived (days to months), used only to obtain new access tokens. This is the valuable one. It's why Chapter 6 tells you to keep access tokens in memory where you can, and give the refresh token real protection.

Many systems use **JWTs** (JSON Web Tokens) for access tokens: a base64-encoded JSON payload with a signature. Two things to know. First, **a JWT is signed, not encrypted** — anyone can read its contents, so never put anything secret in one. Second, **the signature only means something if you verify it**, and verification is a server job. An app that decodes a JWT to read the user ID and trusts it has trusted attacker-controlled data.

### OAuth 2.0 on mobile, done correctly

If your app signs users in through an identity provider, you're using OAuth 2.0, and mobile has specific rules. They're in **RFC 8252, "OAuth 2.0 for Native Apps"**, and they exist because mobile breaks assumptions the base spec made.

**Your app is a public client.** This is the foundational point. RFC 8252 states it plainly: secrets embedded in an app binary are not secret, because they can be extracted from the app package. So any flow requiring a client secret in the app is broken by design. (This is Chapter 1's principle, arriving early.)

**Use Authorization Code flow with PKCE.** PKCE, short for Proof Key for Code Exchange and pronounced "pixie", solves a specific attack. Your app generates a random secret verifier, sends a *hash* of it with the authorization request, and presents the *unhashed* verifier when redeeming the code. An app that intercepted your authorization code wouldn't have the verifier, so the code is useless to it. RFC 8252 **requires** both clients and servers to use PKCE for public native app clients, and says authorization servers should reject native-app requests that don't use it.

**Don't use the Implicit flow.** RFC 8252 marks it NOT RECOMMENDED for native apps, for two reasons: it can't be protected by PKCE, and its access tokens can't be refreshed without user interaction.

**Use the system browser, not a WebView.** This one surprises people, because an embedded WebView feels more polished. RFC 8252 requires an external user-agent, meaning the browser, and explicitly does not support embedded WebViews. The reasoning: a WebView is *your* code, so users can't verify what site they're on, you can read what they type, and you don't get the single sign-on session the browser holds. Use Chrome Custom Tabs on Android and `ASWebAuthenticationSession` on iOS.

**Don't build this yourself.** The **AppAuth** libraries for Android and iOS implement the RFC 8252 pattern including PKCE. Use them.

Why the redirect matters: a private-use URI scheme (`myapp://callback`) can be registered by *multiple* apps, so it's indeterminate which one receives your authorization code — that's the code interception attack PKCE was created to mitigate. Prefer app-claimed `https` redirects (App Links on Android, Universal Links on iOS), which are verified against a domain you control. Chapter 17 covers that verification.

- <https://www.rfc-editor.org/rfc/rfc8252.html>
- <https://oauth.net/2/native-apps/>

### Sessions, and ending them properly

A session begins at login and should genuinely end at logout. "Genuinely" is doing work in that sentence.

Logout must invalidate the token **server-side**. Deleting it from the client is not logout; it's hiding it. If the token still works when replayed, the user isn't logged out.

Logout must also clear **local data**: cached API responses, database rows, in-memory state, log entries, WebView storage and cookies. `MASWE-0024`, "sensitive data accessible after session termination", is common precisely because teams implement logout as an authentication concern rather than a data concern.

Set **timeouts** proportionate to risk: an inactivity timeout that requires re-authentication, and an absolute session lifetime. Shorter for financial flows.

### Step-up authentication

Not all actions deserve the same proof. **Step-up** means requiring additional authentication for sensitive operations even within a valid session — biometrics before a transfer, a password before changing an email address.

`MASVS-AUTH-3` asks for this, and `MASWE-0023` names its absence. Chapter 11 covers implementing it so it can't be hooked away.

### The bug class that isn't about tokens at all

Worth naming here because it's the most damaging authentication-adjacent bug and it isn't in the client: **missing authorization checks on the server.** Your app requests `/api/orders/12345`; the server returns it without checking whether it belongs to the calling user. Change the number, read someone else's order.

No client-side control fixes this. It's `MASVS-AUTH-1` and it's why Chapter 12 exists.

---

## Chapter 0.4: What the platforms give you for free

Before you add anything, understand what Android and iOS already do. A surprising amount of "security work" duplicates a platform guarantee, and a surprising amount of real risk comes from switching one off.

### The app sandbox

Both platforms isolate apps. Each app gets a private storage area other apps can't read, runs as its own user with its own process, and can only reach outside itself through defined channels.

This is the foundation of everything. It means your app's private files are protected from *other apps* by default — which is exactly why Chapter 6 argues that encrypting non-sensitive local data often buys nothing. The sandbox already handled the threat you were worrying about.

The sandbox does **not** protect you from the device's owner, or from an attacker who has rooted or jailbroken the device. Those cases remove the isolation.

### Storage encryption

Both platforms encrypt storage at rest, tied to device unlock. Android has enforced **file-based encryption** since Android 10. On iOS it's **Data Protection**, with classes controlling when the decryption key is available (Chapter 4.4 covers those in detail, because choosing the class is a decision you make).

So data written by your app to private storage is encrypted at rest and isolated from other apps, without you doing anything. What that doesn't cover: a device that's unlocked and compromised, a backup that travels somewhere, or a class you loosened.

### Code signing

Every app is cryptographically signed. The OS verifies the signature at install and refuses modified binaries. This is why repackaging your app requires re-signing it with a *different* key — and why your app can check its own signature to detect that (`MASTG-KNOW-0003`).

Signing also gates identity-based features: Android app links, keychain access groups on iOS, and the "restrict this API key to my app's signing certificate" protection in Chapter 15.

### Permissions

Access to sensitive resources such as the camera, location, contacts and microphone requires a declared permission and, for dangerous ones, explicit runtime consent. Users can revoke consent later. Chapter 18 covers using permissions well, because over-requesting is both a privacy finding and a conversion problem.

### Transport security defaults

Both platforms now require HTTPS by default. Android's **network security configuration** blocks cleartext unless you allow it; iOS's **App Transport Security** does the same. Modern Android also ignores **user-added certificate authorities** for app traffic by default, which is why proxying a modern app takes deliberate effort.

These defaults are strong. Most real network findings come from someone weakening them — a `cleartextTrafficPermitted="true"`, an ATS exception, a debug override that shipped.

### Verified boot

The device checks at startup that it's running an unmodified OS, backed by hardware. You don't interact with this directly, but it matters: since May 2025, Play Integrity's device integrity verdict on Android 13+ **requires** a hardware-backed positive verified boot result. Chapter 9 explains what that means for your users.

### Hardware key storage

Both platforms give you a place to put keys where your own process can't read them: the **Android Keystore** backed by a TEE or StrongBox, and the **iOS Keychain** backed by the Secure Enclave. This is the single most valuable thing the platform hands you, and Chapter 4 is devoted to how it works.

### The takeaway

The platform handles isolation, storage encryption at rest, code integrity, permission gating, transport defaults and hardware key storage. Your job is to *use* those correctly, avoid switching them off, and add protection for the threats they don't cover — a compromised device, a leaked credential, an attacker who is the user.

---

## Chapter 0.5: How to threat model a feature

Threat modelling sounds formal. In practice it's a forty-minute conversation with a whiteboard, and it's the highest-value security activity available to you because it's the only one that happens before the code exists.

Here's a method you can run on your next feature.

### Step 1: Draw what you're building

Sketch the components and the data moving between them. App, backend, third-party services, local storage, any other app you talk to.

Draw **trust boundaries** — lines where data crosses from something you control to something you don't. Every boundary is where you need a check. The app-to-backend line is one. The user-to-app line is one. The "content from a WebView reaches native code" line is one, and it's the one people forget.

### Step 2: Classify the data

For each piece of data, ask three questions. **How bad if it leaks?** **How bad if it's modified?** **How bad if it's unavailable?**

You'll find most data doesn't matter much, and one or two items matter enormously. That's the point: it tells you where to spend.

### Step 3: Ask what could go wrong

Use prompts rather than imagination. STRIDE is the classic set — **S**poofing (pretending to be someone else), **T**ampering (changing data), **R**epudiation (denying an action), **I**nformation disclosure (leaking), **D**enial of service, **E**levation of privilege.

For mobile specifically, the MASWE catalogue in Chapter 27 is a better prompt list, because it's seventy-eight things that actually go wrong in mobile apps rather than six abstractions. Read down it and ask "does this apply?"

Four questions worth asking every time:

- What happens if the device is rooted or jailbroken?
- What happens if an attacker can see and modify all network traffic?
- What happens if a valid request is replayed from a different device?
- What happens if this input is hostile rather than the well-formed thing we tested with?

### Step 4: Decide, and write it down

For each threat: **mitigate** it, **transfer** it (insurance, a third party's responsibility), **accept** it deliberately, or **eliminate** it by not building the risky thing.

Accepting is a legitimate choice, and writing down *why* is what makes it professional rather than negligent. "We accept that a rooted-device user can read their own cached order history, because it's their data and the value to an attacker is minimal" is a decision. Silence is not.

### Step 5: Turn it into work

Each mitigation becomes a ticket with an owner. Each acceptance becomes a line in a document someone can revisit when circumstances change.

### What good looks like

A one-page output: a diagram, a data classification, a short list of threats with decisions, and the accepted risks with reasons. Forty minutes. Revisited when the feature changes materially.

You'll notice this produces better results than any tool, because the hard part was never finding known vulnerability patterns — it was noticing that your new share-sheet feature lets another app hand you a file path you then read.

## Chapter 0.6: Classifying assets and ranking threats

Chapter 0.5 gives you a method. This gives you two tables to fill in while you use it, because "what could go wrong" is easier to answer against a list than against a blank page.

### Asset protection levels

Rate what you hold, because it tells you where to spend.

| Asset | Typical classification | Impact if compromised |
|---|---|---|
| Authentication tokens | **Critical** | Full account takeover; access to everything the user can do |
| Payment credentials | **Critical** | Financial fraud and regulatory liability |
| User PII — email, phone, address | **Critical** | Identity theft; GDPR and similar liability |
| Restricted API keys | **High** | Unauthorised API use, metered cost, possible data access |
| Session state | **High** | Session hijacking and impersonation |
| App configuration and feature flags | **Medium** | Feature manipulation; possible service disruption |
| Analytics data | **Low** | Competitive intelligence leak |
| Public content | **None** | No impact |

### Threat likelihood and impact

Then rank the threats. The point of the exercise is the right-hand column: a threat with no mitigation named is a decision you have not made yet.

| Threat | Likelihood | Impact | Mitigation, and where it is covered |
|---|---|---|---|
| API key extracted from the binary | Very high | High | Do not embed it. BFF pattern (Chapter 12.3); classification (Chapter 15.2) |
| Token theft from a compromised device | High | Critical | Hardware-backed storage and biometric binding (Chapters 6, 11) |
| Interception of traffic | High | Critical | TLS configuration, and pinning where justified (Chapters 7, 8) |
| App repackaged and redistributed | Medium | High | Attestation and signature verification (Chapters 9, 10) |
| Runtime hooking with Frida | Medium | High | Detection reported to a backend risk score (Chapters 12, 14) |
| Credential stuffing | High | High | Server-side rate limiting per account and device, plus attestation on login (Chapter 12) |
| Root or jailbreak exploitation | Medium | Medium | Detection and reporting; backend policy rather than a local block (Chapter 14.2) |
| Supply chain compromise | Medium | Critical | Dependency locking, SBOM, SDK audit, pipeline hardening (Chapter 15) |

Both tables are starting points, not answers. Change the ratings to match your app — a messaging app and a parcel-tracking app should not produce the same numbers, and if yours match this table exactly, you have not done the exercise.

---
