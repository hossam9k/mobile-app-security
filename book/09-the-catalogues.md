---
part: 09
last_verified: 2026-09-11
volatility: medium
recheck_because: "MASTG v2 refactor ongoing"
---

# Part 9: The catalogues

The previous parts explain mechanisms. This part is the standard's own structure, so you can audit against it and speak its vocabulary. Everything here was read from `mas.owasp.org` on 10 September 2026. IDs and weakness titles are as published; where I add a one-line explanation of a control, that summary is mine, and the normative text is at the linked page.

## Chapter 26: The 24 MASVS controls

### MASVS-STORAGE — secure storage of sensitive data at rest

**MASVS-STORAGE-1** — the app securely stores sensitive data. This applies wherever the data lands, app-private internal storage or public locations such as Downloads, and covers data originating from the user, the backend, system services and other apps.

**MASVS-STORAGE-2** — the app prevents leakage of sensitive data to places you did not choose: logs, backups, screenshots, the keyboard cache, notifications and IPC. Chapter 6.4 is this control in practice.

<https://mas.owasp.org/MASVS/05-MASVS-STORAGE/>

### MASVS-CRYPTO — cryptography

**MASVS-CRYPTO-1** — the app uses strong, current cryptographic primitives with parameters following industry standards, typically defined externally in NIST SP 800-175B and SP 800-57.

**MASVS-CRYPTO-2** — the app manages keys properly across the whole lifecycle: generation, storage, use, rotation and destruction. Chapters 4 and 5.

<https://mas.owasp.org/MASVS/06-MASVS-CRYPTO/>

### MASVS-AUTH — authentication and authorization

**MASVS-AUTH-1** — the app uses secure authentication and authorization protocols and follows the relevant best practices.

**MASVS-AUTH-2** — the app performs local authentication securely, meaning it cannot be bypassed by hooking a boolean. Chapter 11.

**MASVS-AUTH-3** — the app secures sensitive operations with additional authentication. Step-up, per Chapter 11.5.

<https://mas.owasp.org/MASVS/07-MASVS-AUTH/>

### MASVS-NETWORK — network communication

**MASVS-NETWORK-1** — the app secures all network traffic according to current best practice.

**MASVS-NETWORK-2** — the app performs identity pinning for all remote endpoints under the developer's control. Read Chapter 8 before acting on this one, and note the scoping phrase.

<https://mas.owasp.org/MASVS/08-MASVS-NETWORK/>

### MASVS-PLATFORM — platform interaction

**MASVS-PLATFORM-1** — the app uses IPC mechanisms securely: intents, content providers, deep links, app extensions.

**MASVS-PLATFORM-2** — the app uses WebViews securely: no unnecessary native bridges, no untrusted content, no local file access.

**MASVS-PLATFORM-3** — the app uses the user interface securely: no sensitive data in screenshots, notifications, the clipboard or behind overlays.

<https://mas.owasp.org/MASVS/09-MASVS-PLATFORM/>

### MASVS-CODE — code quality

**MASVS-CODE-1** — the app requires an up-to-date platform version.
**MASVS-CODE-2** — the app has a mechanism to enforce updates.
**MASVS-CODE-3** — the app only uses software components without known vulnerabilities.
**MASVS-CODE-4** — the app validates and sanitizes all untrusted inputs.

<https://mas.owasp.org/MASVS/10-MASVS-CODE/>

### MASVS-RESILIENCE — resilience against reverse engineering and tampering

**MASVS-RESILIENCE-1** — the app validates the integrity of the platform. Root and jailbreak detection, attestation.
**MASVS-RESILIENCE-2** — the app implements anti-tampering mechanisms.
**MASVS-RESILIENCE-3** — the app implements anti-static-analysis mechanisms. Obfuscation.
**MASVS-RESILIENCE-4** — the app implements anti-dynamic-analysis mechanisms. Debugger and hook detection.

Read Chapter 14 alongside these, because this category is the one where a naive reading produces controls that report success while providing little.

<https://mas.owasp.org/MASVS/11-MASVS-RESILIENCE/>

### MASVS-PRIVACY — privacy, added in v2.1.0

**MASVS-PRIVACY-1** — the app minimizes access to sensitive data and resources.
**MASVS-PRIVACY-2** — the app prevents identification of the user.
**MASVS-PRIVACY-3** — the app is transparent about data collection and use.
**MASVS-PRIVACY-4** — the app offers the user control over their data.

<https://mas.owasp.org/MASVS/12-MASVS-PRIVACY/>

---

## Chapter 27: The 78 MASWE weaknesses

This is the most directly useful list in the standard, because these are the things that actually go wrong. Read it as an audit: for each line, ask whether your app does this.

**Storage** — 0001 sensitive data stored unencrypted in private storage · 0002 sensitive data stored unencrypted outside private storage · 0003 cryptographic keys stored outside the platform keystore · 0004 sensitive data hardcoded in the app package · 0005 insertion of sensitive data into logs · 0006 sensitive data not excluded from backup.

**Cryptography** — 0007 improper encryption · 0008 improper hashing · 0009 improper use of MAC · 0010 improper generation of cryptographic signatures · 0011 improper verification of cryptographic signature · 0012 improper random number generation · 0013 improper cryptographic key generation · 0014 improper cryptographic key derivation · 0015 key rotation not implemented · 0016 key access not restricted · 0017 device secure lock not enforced.

**Authentication** — 0018 lack of authentication or authorization on app components · 0019 lack of auto-fill support for credential providers · 0020 local authentication can be bypassed · 0021 fallback to non-biometric credentials allowed for sensitive transactions · 0022 crypto keys not invalidated on new biometric enrollment · 0023 step-up authentication not implemented for sensitive actions · 0024 sensitive data accessible after session termination · 0025 lack of non-repudiation for critical actions.

**Network** — 0026 network traffic not encrypted · 0027 insecure certificate validation · 0028 insecure identity pinning.

**Platform** — 0029 insecure deep links · 0030 improper use of the clipboard · 0031 allowing untrusted app extensions · 0032 insecure intents · 0033 sensitive native functionality exposed in WebViews · 0034 WebViews allow access to local resources with untrusted content · 0035 WebViews loading untrusted content · 0036 unnecessary exposure of sensitive data via the UI · 0037 unnecessary exposure via notifications · 0038 insufficient protection from screenshots or screen recordings · 0039 app vulnerable to overlay attacks · 0040 sensitive data leaked via accessibility services.

**Code** — 0041 running on a recent platform version not ensured · 0042 latest platform version not targeted · 0043 enforced updating not implemented · 0044 dependencies with known vulnerabilities · 0045 compiler-provided security features not used · 0046 use of deprecated APIs · 0047 non-standard APIs for security-critical functionality · 0048 malicious code included in the app · 0049 unsafe dynamic code loading · 0050 unsafe handling of untrusted data.

**Resilience** — 0051 root/jailbreak detection not implemented · 0052 app virtualization environment detection not implemented · 0053 emulated or virtual device detection not implemented · 0054 device attestation not implemented · 0055 malware detection not implemented · 0056 app attestation not implemented · 0057 app resources integrity not verified · 0058 runtime code integrity not verified · 0059 code obfuscation not implemented · 0060 resource obfuscation not implemented · 0061 debug artifacts not removed · 0062 no application-level payload encryption · 0063 debug mechanisms not disabled · 0064 debugger detection not implemented · 0065 dynamic analysis tools detection not implemented.

**Privacy** — 0066 inadequate permission management · 0067 lack of anonymization or pseudonymisation · 0068 incorrect use of identifiers for user tracking · 0069 usage of non-privacy-preserving functionality · 0070 inadequate awareness for privacy-relevant actions · 0071 inadequate defaults for privacy-relevant actions · 0072 inadequate privacy policy · 0073 inadequate data collection declarations · 0074 inadequate tracking domains declarations · 0075 non-reproducible builds · 0076 lack of proper data management controls · 0077 inadequate data visibility controls · 0078 inadequate or ambiguous user consent mechanisms.

<https://mas.owasp.org/MASWE/>

**Three that deserve special attention**, because engineers routinely miss them:

**MASWE-0022** — keys not invalidated on new biometric enrollment. Chapter 11.3 is the scenario. This is the highest-impact, lowest-awareness item in the catalogue.

**MASWE-0024** — sensitive data accessible after session termination. Logout that clears the token but leaves cached responses, database rows and log entries on disk is a finding, and it is extremely common because "logout" is usually implemented as an auth concern rather than a data concern.

**MASWE-0075** — non-reproducible builds. Filed under Privacy, which surprises everyone. It matters because nobody can verify what shipped if the build cannot be reproduced, which connects it directly to Part 6.

---

## Chapter 28: The tests, techniques and practices you will use

### The tests worth knowing by number

**Android storage:** TEST-0001 local storage · 0003, 0203, 0231 logs statically and at runtime · 0009, 0216 backups · 0011 memory · 0287 unencrypted data via `SharedPreferences` at runtime · 0305 unencrypted via DataStore.

**Android crypto:** TEST-0212 hardcoded keys in code · 0221, 0232, 0350 broken algorithms and modes · 0309, 0310 reused initialization vectors · 0208 insufficient key sizes.

**Android auth:** TEST-0018 biometric authentication · 0326 fallback to non-biometric · 0328 enrollment-change detection · 0330 keys with extended validity duration.

**Android network:** TEST-0020, 0217, 0218 TLS settings and insecure protocols · 0022, 0242, 0243, 0244 pinning presence, expiry and in live traffic · 0235, 0236 cleartext in config and on the wire · 0285, 0286 trust in user-added CAs · 0284 SSL error handling in WebViews.

**Android platform:** TEST-0031, 0033, 0334 JavaScript, Java objects and native code exposed through WebViews · 0028, 0393 deep links and unverified App Links · 0030, 0381 vulnerable and insecure `PendingIntent` · 0364, 0365, 0366 exported unprotected activities, services and receivers · 0289, 0291 screenshot exposure.

**Android code and resilience:** TEST-0272, 0274 vulnerable dependencies including via SBOM · 0339 SQL injection in content providers · 0038, 0224, 0225 signing correctness, scheme and key size · 0039, 0226, 0227 debuggable app, manifest and WebView debugging · 0045, 0324, 0325 root detection · 0341 hook detection · 0368, 0369 insufficient obfuscation of Java/Kotlin and native code.

**Android privacy:** TEST-0206 undeclared PII in captured traffic · 0254, 0255 dangerous and non-minimized permissions.

**iOS storage:** TEST-0052 local data storage · 0299 data protection classes in private storage · 0215, 0298 backup exclusion · 0055, 0313 keyboard cache · 0388 shared App Group containers.

**iOS crypto and auth:** TEST-0062 key management · 0213, 0214 hardcoded keys in code and files · 0064 biometric authentication · 0266, 0267 event-bound biometric auth · 0270, 0271 enrollment-change detection.

**iOS network:** TEST-0066, 0342, 0343 TLS settings, weak ATS exceptions, URLSession configuration · 0068, 0385 pinning and pinning in ATS · 0396, 0397 `URLSessionDelegate` and `WKNavigationDelegate` bypassing certificate validation.

**iOS platform:** TEST-0076, 0078 WebViews and exposed native methods · 0331, 0333 deprecated WebView APIs and broad file read access · 0070, 0075, 0370, 0371 universal links and custom URL schemes with missing input and source validation · 0276–0280 pasteboard use, contents, clearing, expiry and device scope · 0389, 0390 custom keyboard restrictions and full-access requests.

**iOS code and resilience:** TEST-0273, 0275 vulnerable dependencies · 0081, 0220 signing and outdated signature format · 0088, 0240, 0241 jailbreak detection · 0354 hook detection · 0391 insufficient native obfuscation.

<https://mas.owasp.org/MASTG/tests/>

### The techniques, in learning order

**Generic:** MASTG-TECH-0047 reverse engineering · 0048, 0049 static and dynamic analysis · 0050 binary analysis · 0051 tampering and runtime instrumentation · 0071 retrieving strings · 0119 intercepting HTTP by hooking network APIs at the application layer · 0120, 0121 intercepting HTTP and non-HTTP traffic with a proxy · 0122 passive eavesdropping · 0123, 0124 achieving MITM via ARP spoofing or a rogue access point.

**Android:** MASTG-TECH-0001, 0002 device shell and host-device transfer · 0003 obtaining and extracting apps · 0004 repackaging · 0007, 0008 exploring the package and app data directories · 0009 monitoring system logs · 0011 setting up an interception proxy · **0012 bypassing certificate pinning** · 0013–0018 reverse engineering, static and dynamic analysis, smali disassembly, Java decompilation, native disassembly.

<https://mas.owasp.org/MASTG/techniques/>

### The best practices worth putting in a PR template

Logging: BEST-0002 remove logging code, 0022 disable verbose and debug logging in production. Backups: 0004, 0023 exclude sensitive data. Crypto: 0005, 0009 secure encryption modes and algorithms, 0001 and 0025 secure random number generators. Signing and build: 0006 up-to-date APK signing schemes, 0007 debuggable disabled, 0008 WebView debugging disabled, 0010 up-to-date `minSdkVersion`.

Screens and input: 0014–0018 preventing screenshots and recording via `SECURE_FLAG`, `setRecentsScreenshotEnabled`, `setSecure` for SurfaceViews and `SecureFlagPolicy.SecureOn` for Compose · 0019, 0026, 0044 non-caching input types, keyboard-cache prevention and masking · 0027 notifications · 0069 keep sensitive input on the system keyboard.

Biometrics: **0031 enforce strong biometrics for sensitive operations · 0036 use cryptographic binding · 0037 invalidate keys on enrollment changes · 0038 require explicit user confirmation.**

Resilience: 0029 implement resilience and RASP signals · 0030 root detection · 0041 harden against runtime hooking · 0046, 0053 harden against emulation and virtual devices · 0047, 0074 continuous anti-debugging.

Network: 0042, 0043 strong TLS in ATS and where ATS does not apply · 0073 properly validate server trust in `URLSessionDelegate` and `WKNavigationDelegate`.

WebViews: 0011, 0033 securely load file content · 0012, 0013 disable JavaScript and content provider access where possible · 0035 prefer origin-scoped messaging over legacy bridges · 0058–0062 restrict native functionality via bridges, render sensitive UI natively over the WebView, use `WKContentWorld` isolation, and `WKScriptMessageHandlerWithReply` for returning data.

IPC and components: 0039 prevent SQL injection in content providers · 0040 prevent overlay attacks · 0049, 0052 restrict and validate access to exported components · 0056, 0057 explicit intents for internal IPC and sanitize external data · 0063 immutable `PendingIntent`s · 0064 safe deserialization APIs.

Integrity and links: 0065, 0066, 0067 storage and source-code integrity checks · 0070–0072 verify App Links with `autoVerify` and Digital Asset Links, validate deep link and universal link parameters.

Platform hygiene: 0051 minimize iOS permissions and entitlements · 0020 update the GMS security provider · 0021 proper error and exception handling · 0003 comply with privacy regulations.

<https://mas.owasp.org/MASTG/best-practices/>

---
