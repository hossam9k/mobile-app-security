---
part: 03
last_verified: 2026-09-11
volatility: high
recheck_because: "Certificate lifetimes step down 2027 and 2029"
---

# Part 3: Data in transit

## Chapter 7: What TLS gives you, and what pinning adds

To reason about pinning you first need a clear picture of what standard TLS already does, because most pinning arguments are really arguments about a gap that people cannot describe precisely.

### 7.1 The baseline

When your app connects over HTTPS, the server presents a certificate chain: a leaf certificate for your domain, one or more intermediate CA certificates, and a root. Your device validates that chain against a **trust store** of root certificates shipped and maintained by the platform. It checks that the chain is cryptographically valid, that the leaf covers the hostname you asked for, and that nothing has expired or been revoked.

This is genuinely strong, and it is free. It defeats the coffee-shop attacker completely.

Before you consider anything more exotic, get the free things right, because most apps still do not:

**Require TLS 1.2 minimum, prefer 1.3.** Configure it explicitly rather than inheriting a default that an old library overrides.

**Forbid cleartext.** On Android that is `cleartextTrafficPermitted="false"` in `network_security_config.xml`; on iOS it is App Transport Security. Then check for the hardcoded `http://` URL that some SDK is using anyway.

**Do not trust user-added certificate authorities for your own domains.** This is the single most valuable line in an Android network security configuration. By default, apps targeting modern Android already ignore user-added CAs, which is why proxying a modern app requires more effort — but if you have loosened this for debugging, make sure that configuration cannot ship.

**Ship no debug network configuration.** A `debug-overrides` block that reaches production is a hole with an audit trail.

**Handle TLS errors correctly, especially in WebViews.** `onReceivedSslError` with a call to `proceed()` is a complete bypass of everything above, and it appears in real apps because it makes a certificate warning go away during development.

### 7.2 So what is left for pinning to do?

Standard validation trusts **any** root in the device trust store. That means roughly a hundred organisations, plus anything an administrator or user has added, can issue a certificate for your domain that your app will accept.

Pinning narrows that set. Instead of "any trusted CA," your app accepts only a specific cryptographic identity you nominated. The threat it addresses is a **rogue or compromised CA**, or a certificate a device administrator has installed — including the enterprise MDM case and the "user tapped through a profile install" case.

That is a real threat, and it is a narrower threat than it was ten years ago. Which brings us to the argument.

---

## Chapter 8: The pinning debate, argued properly

This is the most contested question in mobile security. You should be able to argue either side, because your interviewer might hold either position and both are defensible.

### 8.1 The case against pinning

Four arguments, and they are stronger than most pinning advocates admit.

**OWASP's own Pinning Cheat Sheet is blunt about it.** Its position is that for most applications the answer is probably never, because the risk of outages almost always outweighs the security benefit given advances elsewhere.

**Google's Android documentation cautions against it**, on the grounds that future server configuration changes carry a high risk of breaking the app.

**The environment improved underneath the threat.** Certificate Transparency means misissued certificates for your domain are publicly logged and detectable. Certificate lifetimes are collapsing, limiting the value of any single compromise. Automated issuance via ACME removed most of the human error that used to produce mistakes. Together these narrowed pinning's marginal benefit while leaving its operational risk untouched.

**The failure mode is catastrophic and asymmetric.** A pinning mistake does not degrade your app; it disconnects every user on that build simultaneously, and the only fix is an app store update — which takes hours at best, and which users must then install.

### 8.2 The case for pinning

Four arguments the other way, and they are stronger than most pinning critics admit.

**MASTG treats it as recommended practice**, especially for MAS-L2 apps handling financial or health data, and MASVS-NETWORK-2 asks for identity pinning on remote endpoints under the developer's control.

**MASTG explicitly addresses the Google warning**, noting that it can be mistakenly interpreted as saying Google does not recommend certificate pinning, when the actual recommendation is to take the necessary precautions — backup pins and a rotation plan.

**Mobile is not the web.** The strongest technical argument. A web client cannot be updated on your schedule; a mobile client can be force-updated through the stores. The operational objection that kills pinning for browsers is materially weaker for apps.

**Regulated industries do it anyway.** Banking apps pin, frequently because a regulator or an auditor requires defence in depth rather than because the engineering team chose it. If you work in that world, "OWASP says don't" will not end the conversation.

### 8.3 The honest synthesis *(contested)*

The debate is not "pinning good" versus "pinning bad." It is about operational maturity.

**Pinning done badly is worse than not pinning at all** — one pin, no backup, no rotation plan, no monitoring —, because you have added a self-inflicted outage risk without meaningfully raising an attacker's cost.

**Pinning done properly adds a real layer**, and for a payment or health application that layer is worth the operational weight.

The question to ask is therefore not "should we pin?" but "**can this team operate a pinset for the next three years without locking users out?**" That is a question about runbooks, ownership, and monitoring, not about cryptography. If the answer is no, the correct decision is not to pin — and to say so plainly, rather than pinning badly to satisfy a checklist.

### 8.4 What to pin, and why SPKI

#### First: three different things people all call "pinning"

"SSL pinning" in a job description or a blog post can mean any of three things. You will meet all three names, so learn them now.

| Type | What the app stores | What it compares against |
|---|---|---|
| **Certificate pinning** | The whole certificate, or a hash of it | The certificate the server presents, in full |
| **Public key pinning**, also called **SPKI pinning** | A SHA-256 hash of the Subject Public Key Info | The public key taken from a certificate in the chain |
| **CA pinning** | The identity of an issuing authority | Whether the presented chain passes through that authority |

**Certificate pinning is not just weaker — it is differently broken.** Because it matches the whole certificate, it also pins the expiry date and the serial number. So it breaks on **every** renewal, even when the server reuses the same key pair. There is no situation where this is the right choice for a mobile app.

**Public key pinning is the one you want**, and the rest of this chapter assumes it.

**CA pinning** is really public key pinning applied further up the chain. It appears below as the "intermediate" and "root" options.

#### Now the rule

Always pin the hash of the **SPKI**, or Subject Public Key Info. Never pin the full certificate.

The reason is renewal. A certificate expires and is reissued regularly. If the new certificate carries **the same public key**, then its SPKI hash is unchanged and an SPKI pin still validates. A full-certificate pin breaks on every renewal without exception.

That gives you a choice of pin target, and the trade-off is trust breadth against operational resilience:

| Pin target | Survives renewal? | What you are trusting |
|---|---|---|
| Leaf SPKI | Only if the key pair is reused | Exactly one key. Tightest, most fragile |
| Intermediate CA SPKI | Yes, across leaf renewals | Anything that CA issues for you |
| Root CA SPKI | Yes, for years | That CA's entire issuance surface. Weakest protection |

#### Three questions this raises

**Which hash algorithm?** SHA-256. On Android's network security configuration it is the only value `pin digest` accepts, and it is why you see `sha256/` prefixes in OkHttp and in iOS configuration.

**Does a more expensive certificate help?** No. Domain-validated, organisation-validated and extended-validation certificates differ in how much the CA checked about *your organisation*, not in cryptographic strength. You are pinning a public key, so the validation level buys you nothing here. People assume otherwise, and it is worth correcting in a design review.

**What about a self-signed certificate or your own private CA?** For an internal or enterprise app where you control both ends, pinning your own self-signed certificate or private CA is legitimate and common. It shifts the calculus in both directions. There is no public CA that could misissue for you, which removes the very threat pinning exists to stop. But there are also no Certificate Transparency logs to fall back on, because CT only covers publicly trusted certificates. If you go this route, pinning is carrying more of the load, so the rotation runbook in §8.7 matters more rather than less.

**Ship at least one backup pin. Always.** A pinset with a single pin is one certificate incident away from a total outage that only an app store release can repair. The backup should be a pin you can actually switch to — a key you hold, or an intermediate you have verified.

### 8.5 The 2026 development that changes the arithmetic

Two clocks are shrinking, not one. Before the table makes sense, you need the concept behind the second column.

#### What domain validation is

Before a certificate authority gives you a certificate for `api.example.com`, it has to check that you actually control that domain. Otherwise anyone could request a certificate for your site. That check is **Domain Control Validation**, usually shortened to **DCV**.

You prove control in one of a few ways. You publish a specific DNS record the CA asks for (`DNS-01`). You place a specific file at a URL on the domain (`HTTP-01`). Historically you could also reply to an email at an address on the domain, though **WHOIS-based email validation was discontinued on 15 July 2025.**

Now the part that matters. Once a CA has validated your control, it does not re-check every single time it issues you a certificate. It can **reuse** that proof for a period. That period is the second column in the table, and it runs on a completely separate clock from the certificate's own lifetime.

So, two clocks doing two different jobs:

- **Certificate lifetime** — how often you must **replace the certificate**.
- **DCV reuse window** — how often you must **re-prove that you own the domain**.

#### The schedule

Both are shortening under CA/Browser Forum **Ballot SC-081v3**, approved in April 2025. Apple originally proposed it, and it was adopted with no votes against.

| From | Maximum certificate lifetime<br>*how often you replace it* | DCV reuse window<br>*how often you re-prove ownership* |
|---|---|---|
| Until 15 March 2026 | 398 days | 398 days |
| **15 March 2026** (in force now) | **200 days** | **200 days** |
| 15 March 2027 | 100 days | 100 days |
| 15 March 2029 | **47 days** | **10 days** |

#### What that means for your workload

Take the 2029 row and work it through.

**Certificates.** A 47-day maximum means replacing each one every six to seven weeks, about eight times a year. Most teams do this once a year today. That is roughly an eightfold increase in renewal events. For an estate of 1,000 certificates, about 1,000 renewals a year becomes more than 8,000.

**Validation.** Here is the part that catches people, and it is why the second column is not a footnote. The 10-day reuse window means your proof of domain ownership **expires every 10 days, whether or not you are renewing a certificate.** You are not doing one validation per certificate. You are re-proving ownership on a rolling 10-day cycle, which works out at roughly **35 to 37 validations per year, per domain** — even though you only replace the certificate eight times.

That asymmetry is the whole point. A team that automates certificate renewal but not validation still fails, because the CA challenge step will hit an expired authorization.

**The consequence.** Manual validation stops working. Email replies and one-off file placement cannot run at a 10-day cadence. Automated validation through ACME becomes the only sustainable route.

#### The mechanism that makes it bearable

One newer option is worth knowing, because it exists precisely to solve this: **persistent DCV**, the `DNS-PERSIST-01` method introduced by Ballot SC-088v3 and permitted since November 2025.

Rather than changing a DNS record for every validation, you publish a single TXT record once, at `_validation-persist` on your domain. The CA then re-validates against that standing record with no per-renewal DNS change. If you own your DNS, ask your CA whether they support it. It turns 35 DNS changes a year into one.

#### One caveat on ACME

Since this section pushes you toward automation, here is the honest counterweight. Research presented at the ACM Web Conference in 2025 showed that **stolen ACME account credentials can produce fraudulent certificates without the attacker ever controlling the domain**, because of validation caching. Automating validation moves your risk from "we forgot to renew" to "our ACME account credentials are now a high-value target." Protect them the way you protect a signing key (Chapter 15.6).

**Here is why this decides your pinning design.** Automated renewal usually generates a **fresh key pair** each time. If it does, your leaf SPKI changes on every renewal — which was survivable at 398 days and is untenable at 47. Two ways out:

**Pin the intermediate CA SPKI**, which survives leaf rotation entirely. You widen your trust to that CA's issuance for your domain, and you accept that.

**Or reuse the key pair across renewals**, so the SPKI stays stable while the certificate rotates.

Either is defensible. What is not defensible is not knowing which one your infrastructure does. Go and ask whoever owns your certificates, today, before you ship a pin.

And to restate the trap in one line, because teams keep walking into it: **plan against both columns.** A team that reads only the certificate-lifetime column builds something that works in 2027 and falls over in 2029, when validation starts expiring four times faster than the certificate it supports.

- <https://www.digicert.com/blog/tls-certificate-lifetimes-will-officially-reduce-to-47-days>
- <https://shop.sslinsights.com/blog/ca-browser-forum-47-day-certificate-roadmap/>
- DCV explained, with the workload arithmetic — <https://www.encryptionconsulting.com/understanding-10-day-domain-validation/>
- Persistent DCV and `DNS-PERSIST-01` — <https://www.encryptionconsulting.com/persistent-dcv-dns-validation/>
- SC-081v3 in full, including the ACME research — <https://www.captaindns.com/en/blog/tls-certificate-validity-reduction-47-days>

### 8.6 Where the pins live: static, dynamic and hybrid

Everything above tells you *what* to pin. This section is about *where the pin lives*, and it is the decision that determines whether pinning is operationally survivable.

#### Static pinning

The pins are baked into the app at build time — an Android network security configuration file, or a trust-evaluation callback on iOS.

It is easy to audit and easy to reason about. You can read the file and know exactly what your app trusts. And it **welds your network operations to your app release cycle**: when a certificate changes, you ship a release. That clause is the whole problem, and §8.5's shrinking certificate lifetimes make it sharper every year.

The failure story is concrete. A certificate rotates, the old pin no longer matches, and every user on that build loses connectivity until they install an update. Some never will.

#### Dynamic pinning

The app ships with **bootstrap pins**, then fetches a **signed pin manifest** from a management endpoint at runtime.

Here is the essential detail, and if you take one thing from this section, take this: **the manifest is signed with a key that has nothing to do with the web PKI.** Think about why. If you validated the connection that delivers your pins using the pins it delivers, you would have circular trust and no security at all. So the manifest carries its own signature, verified against a public key compiled into the app, independent of TLS. TLS gets you a connection; the signature gets you authenticity.

What this buys you: rotation without a release. Your certificate changes, you publish a new manifest, and apps in the field pick it up. The problem static pinning has with 47-day certificates disappears.

Open-source implementations exist, such as Wultra's `ssl-pinning-ios` and its Android counterpart, and several commercial platforms sell it as a managed service. The motivation they all state is the same: certificate expiry forces app updates, some percentage of users never update, and those users lose access.

#### The honest cost of going dynamic

Vendor material tends to present dynamic pinning as strictly better. It isn't, and you should know the trade before you choose it.

**You have moved your trust root, not removed it.** That manifest signing key now needs protecting for the lifetime of your app, in an HSM or equivalent, with a rotation story of its own. You have swapped a certificate-rotation problem for a signing-key-custody problem. For some teams that is a clear win; for others it is the same problem wearing a different hat.

**You have added a runtime dependency.** If your management endpoint is down or unreachable, what does your app do? Fail closed and you have invented a new outage. Fail open and you have invented a bypass. You need an answer, and it needs a cached manifest with a defined staleness window.

**You still need backup pins.** Dynamic delivery does not remove that requirement; it just moves where the backups live.

**You have stepped outside the standard.** OWASP's guidance and the MASTG's tests are written around static pinning. `MASTG-KNOW-0015` describes the platform mechanisms; there is no equivalent normative treatment of signed manifests. An auditor may not recognise your design, and you will be explaining it rather than pointing at a control ID.

**My view, stated plainly** *(reasoned)*: for a small team, static pinning on an intermediate CA SPKI with a documented runbook and a real backup pin is usually the better engineering decision. Dynamic pinning earns its complexity when you have many endpoints, frequent rotation you do not control, a install base that updates slowly, or a security team that can actually own a signing key.

#### How this differs on Android and iOS

Dynamic pinning is not equally easy on the two platforms, and the reason is the same on both: **the declarative mechanism cannot be updated at runtime.** So on each platform, choosing dynamic means giving up the declarative option and its advantages.

| | **Android** | **iOS** |
|---|---|---|
| Declarative mechanism | `network_security_config.xml`, API 24+ | `NSPinnedDomains` in `Info.plist`, iOS 14+ |
| Can it be updated at runtime? | **No** — compiled into the app | **No** — Apple documents no way to change it |
| Programmatic mechanism | OkHttp `CertificatePinner`, or a custom `X509TrustManager` | `URLSessionDelegate` trust evaluation |
| So dynamic pinning means | Rebuilding the pinner, or a custom trust manager | Implementing the delegate yourself |
| Covers WebView traffic? | **Declarative: yes. Programmatic: no** | **Neither** |

Three consequences follow, and the third is the one that catches teams out.

**On Android, going dynamic costs you WebView coverage.** This is the important one. Android applies network security configuration rules to WebView traffic in the same app automatically, so static pinning protects your WebView for free. OkHttp's `CertificatePinner` does not — it only governs traffic through that OkHttp client. Move to dynamic pinning and your WebView silently stops being pinned. If you have a WebView loading anything sensitive, you either keep a static configuration alongside the dynamic path, or you intercept WebView requests yourself with `shouldInterceptRequest` and a custom trust manager. Neither is free, and the choice needs making deliberately rather than discovered in an audit.

**On iOS, WebView was never covered anyway.** `NSPinnedDomains` does not apply to `WKWebView` or `SFSafariViewController`, and neither does your `URLSessionDelegate`, because `WKWebView` does not route through your session. So iOS gives you no supported way to pin `WKWebView` traffic. That is a real limitation, not an oversight on your part, and the mitigation is architectural: do not load sensitive content in a WebView (Chapter 16.5).

**`CertificatePinner` is immutable once built.** You cannot add a pin to a live instance. Dynamic pinning on Android therefore means rebuilding the pinner and the client when a new manifest arrives, or wrapping the whole thing in a custom `X509TrustManager` that reads its pin set from a mutable source. The rebuild approach is simpler and usually correct; the trust manager approach is more code and more ways to be wrong.

**One security trade-off worth naming.** Declarative pinning is easy to audit, which is genuinely valuable — a reviewer reads one file. It is also easy to strip. Researchers have demonstrated removing `NSPinnedDomains` from an `Info.plist`, re-signing the app, and installing it with pinning simply gone; the same applies to editing a network security configuration in a repackaged APK. Pinning implemented in code, especially native code, costs an attacker more to remove. That is not an argument against declarative pinning, since an attacker on their own device wins either way (Chapter 1). But if your threat model includes redistributing a modified build to other users, it is a point in favour of the programmatic route.

#### Hybrid, which is what most mature apps do

Ship a **static backup pin** in the binary, and rely primarily on **dynamically fetched pins**.

You get rotation flexibility from the dynamic path and a floor under you if the management endpoint fails. This is increasingly the default in practice, for the obvious reason that it has the smaller failure surface of the two.

#### The safety valve people forget: expiration

Android's `pin-set` takes an optional `expiration` attribute, and it is worth understanding exactly what it does, because it is counter-intuitive.

**After the expiration date, pinning stops being enforced.** The connection still validates normally against the platform trust store, but your pins are ignored. It is a deliberate fail-open: it trades security for availability, so that a forgotten pin does not brick your app forever.

That is a genuine safety valve and it is also a silent downgrade. Set a date, and put a calendar reminder well before it — otherwise your app will quietly stop pinning one morning and nothing will tell you. OWASP's own guidance on this is to set an appropriate expiration date *and* ensure timely updates, precisely so the app does not end up bypassing pinning after the date has passed.

#### Side by side

The prose above gives you the reasoning. This gives you the comparison in one place.

| | **Static** | **Dynamic** | **Hybrid** |
|---|---|---|---|
| **Pros** | Easy to audit — a reviewer reads one file. No runtime dependency. Recognised by the standard and by auditors. On Android, covers WebView traffic | Rotation without an app release. Survives 47-day certificates. Users on old builds keep working | Rotation flexibility with a floor under you. Smallest failure surface of the three |
| **Cons** | Rotation needs a release, and users who do not update lose access. Trivially stripped from a repackaged build | A signing key you must now protect for years. New runtime dependency and failure mode. Outside the standard, so you explain rather than cite. On Android, loses WebView coverage | Most moving parts. Two mechanisms to test and keep correct |
| **Best for** | One or two endpoints you control, and you can ship releases | Many endpoints, rotation you do not control, or a slow-updating install base | Most mature apps at scale |
| **Worst for** | Estates with frequent uncontrolled rotation | Small teams with no key-custody capability | Teams that will only maintain one path properly |

#### Choosing

| Situation | Approach |
|---|---|
| One or two endpoints, certificates you control, you can ship releases | **Static**, intermediate SPKI, backup pin, expiration set, runbook written |
| Frequent rotation you don't control, or slow-updating install base | **Hybrid**: static backup plus signed dynamic manifest |
| Many endpoints, a security team that can own a signing key | **Dynamic**, with a cached manifest and a defined staleness policy |
| You can't securely update the pinset, or don't control both ends | **Don't pin.** CT plus HSTS (§8.9) |

### 8.7 What pinning costs you operationally

If you pin, you owe your team all of the following. This is the list that determines whether pinning helps or hurts.

A **documented rotation runbook** with a named owner, describing exactly what happens when a certificate changes. **Backup pins in every release.** A **monitoring alert on pin validation failures**, so you learn from telemetry rather than from app store reviews. **Certificate Transparency monitoring** for your domains, so you detect misissuance — which is the threat you pinned against in the first place. A **remote kill switch** to disable pinning without a release, because the alternative is waiting for store review during an outage. And an **explicit agreement with whoever manages certificates** that changes require a coordinated app release.

Missing any one of these is how pinning causes the outage it was supposed to prevent.

### 8.8 The decision, by application type

Reason from the threat, not the table — but the table encodes the reasoning.

**Banking, fintech, trading:** SPKI pinning on an intermediate with a backup, plus CT monitoring. Frequently a compliance requirement, and the value of the transactions justifies the operational weight.

**Health and medical:** the same. Patient data is high-value and long-lived, and the regulatory environment rewards defence in depth.

**E-commerce:** depends on where payment happens. Handle cards in-app and you are in the first category. Delegate to a gateway and CT plus HSTS is a reasonable position.

**Ride-sharing, delivery, marketplaces:** CT plus HSTS plus backend fraud detection. Payment is usually tokenised elsewhere, and the operational overhead of pinning buys little.

**Social, messaging, content:** CT plus HSTS. Platform defaults with a strict configuration are sufficient. Pinning a news feed adds risk and no security.

**Enterprise and internal:** pin only if you control both client and server. If a customer's MDM is legitimately inspecting traffic, pinning breaks your own deployment.

**The rule that decides it, from OWASP's cheat sheet:** if you do not control both ends of the connection, or you cannot securely update the pinset, do not pin.

### 8.9 The alternatives, properly described

"Use CT and HSTS instead" is easy to say and worth unpacking, because they do different jobs.

**Certificate Transparency** is a set of public, append-only logs of issued certificates. Every publicly trusted certificate must be logged. You monitor the logs for your own domains and get alerted when a certificate you did not request appears. Note what this is: **detection, not prevention.** It does not stop a misissued certificate from working; it tells you one exists, quickly, so you can revoke.

#### How to actually monitor Certificate Transparency

"Monitor CT" is easy to say. Concretely, you want to know when a certificate exists for your domain that you did not request.

The quickest manual check is a CT search service — `crt.sh` lets you query every logged certificate for a domain. Run it once now for your own domains; teams are routinely surprised by forgotten subdomains and certificates issued by providers they no longer use.

For ongoing monitoring you want alerts rather than a manual check: most commercial CT monitoring services and several CAs offer this, and you can build it by polling a CT log API for your domains and diffing against a known-good inventory. The requirement is not sophistication, it is **someone receiving the alert and knowing what to do with it** — which is a runbook question, not a tooling question.

Worth pairing with the inventory problem: you cannot detect an unexpected certificate for your domain if you do not know which certificates are expected.

**HSTS** tells clients to use HTTPS only for your domain, preventing protocol downgrade. It closes the "attacker strips TLS" path. It does nothing about a fraudulently issued certificate.

**Backend anomaly detection** catches the traffic pattern of an interception attempt — a client whose behaviour changes, requests arriving from unexpected paths, sudden shifts in device signals.

Together these give you fast detection and a narrowed attack surface without the outage risk. For most applications that is the correct trade. For the ones handling money or health records, layering pinning on top is worth it — if, and only if, §8.6 is genuinely in place.

---
### 8.10 How to implement it

Minimal, correct implementations. Both platforms, static first, then the dynamic manifest shape.

#### Android: network security configuration (declarative, API 24+)

This is the first choice if your networking is not centred on OkHttp. One useful property: **Android applies these rules to WebView traffic in the same app automatically**, so your pins cover WebView requests without extra work.

```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
  <domain-config cleartextTrafficPermitted="false">
    <domain includeSubdomains="true">api.example.com</domain>
    <!-- SHA-256 hashes of the SPKI, not of the whole certificate -->
    <pin-set expiration="2027-12-31">
      <!-- Primary: intermediate CA SPKI -->
      <pin digest="SHA-256">YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg=</pin>
      <!-- Backup: never ship without one -->
      <pin digest="SHA-256">Vjs8r4z+80wjNcr1YKepWQboSIRi63WsWXhIMN+eWys=</pin>
    </pin-set>
  </domain-config>
</network-security-config>
```

Reference it from the manifest:

```xml
<application android:networkSecurityConfig="@xml/network_security_config" ... >
```

Three things to notice. The `expiration` attribute is the fail-open valve from §8.6 — after that date pinning is silently off. `includeSubdomains` is convenient and widens what you are pinning, so be deliberate. And this mechanism needs API 24 or higher; below that you need the programmatic route.

#### Android: OkHttp CertificatePinner (programmatic, all API levels)

Choose this if your stack is already OkHttp-centric. It works on every API level, and under the hood it installs a custom `TrustManager`.

```kotlin
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg=") // primary
    .add("api.example.com", "sha256/Vjs8r4z+80wjNcr1YKepWQboSIRi63WsWXhIMN+eWys=") // backup
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

A trick worth knowing for getting the values: give `CertificatePinner` a deliberately wrong pin, make one request, and read the correct hashes out of the exception message. Faster than the OpenSSL incantation and less error-prone than copying from a blog.

#### Choosing an Android approach

| | **Network Security Config** | **OkHttp CertificatePinner** | **Both together** |
|---|---|---|---|
| **Pros** | Declarative and auditable. Covers **all** app traffic including WebView. No code | Works on every API level. Programmatic, so it can be made dynamic. Clear failure exceptions | Defence in depth; if one is misconfigured the other still holds |
| **Cons** | API 24+ only. Cannot change at runtime. Stripped by editing one file in a repackaged APK | Only governs traffic through that client — **WebView is not covered**. Immutable once built | Two places to update; a mismatch between them is confusing to debug |
| **Use when** | Most apps, and any app with a WebView reaching a pinned host | Your stack is OkHttp-centric, or you need dynamic pins | Financial and health apps where the extra check is worth the maintenance |

#### Android: making the programmatic path dynamic

`CertificatePinner` is **immutable once built**, so "update the pins" means build a new one and a new client:

```kotlin
class PinnedClientProvider(private val manifestStore: ManifestStore) {

    @Volatile private var cached: Pair<Int, OkHttpClient>? = null   // manifest version -> client

    fun client(): OkHttpClient {
        val manifest = manifestStore.current()          // verified signature, checked version
        cached?.let { (version, c) -> if (version == manifest.version) return c }

        val pinner = CertificatePinner.Builder().apply {
            manifest.entries.forEach { entry ->
                entry.pins.forEach { pin -> add(entry.host, pin) }   // "sha256/…"
            }
            // Always keep the bootstrap pins as a floor.
            BOOTSTRAP_PINS.forEach { (host, pin) -> add(host, pin) }
        }.build()

        val built = OkHttpClient.Builder().certificatePinner(pinner).build()
        cached = manifest.version to built
        return built
    }
}
```

Two things this deliberately does. It keeps the **bootstrap pins** in the set rather than replacing them, so a bad manifest cannot lock you out of your own backend. And it keys the cache on manifest **version**, so the client is rebuilt only when the pin set actually changes — rebuilding per request would throw away your connection pool.

Remember from §8.6 that this path does **not** cover WebView traffic. If you have a WebView reaching a pinned host, keep a static `network_security_config.xml` entry for it as well.

#### iOS: NSPinnedDomains (declarative, iOS 14+)

Apple calls this **Identity Pinning**, and it is the iOS counterpart to Android's network security configuration. It arrived in iOS 14 and macOS 11, and a surprising number of teams do not know it exists.

```xml
<!-- Info.plist -->
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSAllowsArbitraryLoads</key>
  <false/>
  <key>NSPinnedDomains</key>
  <dict>
    <key>api.example.com</key>
    <dict>
      <key>NSIncludesSubdomains</key>
      <true/>
      <!-- Pin the intermediate or root CA. Use NSPinnedLeafIdentities
           instead to pin the leaf. -->
      <key>NSPinnedCAIdentities</key>
      <array>
        <dict>
          <key>SPKI-SHA256-BASE64</key>
          <string>YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg=</string>
        </dict>
        <dict>
          <!-- Backup pin -->
          <key>SPKI-SHA256-BASE64</key>
          <string>Vjs8r4z+80wjNcr1YKepWQboSIRi63WsWXhIMN+eWys=</string>
        </dict>
      </array>
    </dict>
  </dict>
</dict>
```

**Note the value format, because it is a useful cross-check.** `SPKI-SHA256-BASE64` is the base64-encoded SHA-256 digest of the certificate's DER-encoded ASN.1 Subject Public Key Info structure — **exactly the same value you put in Android's `pin digest`.** If your Android and iOS pins differ for the same endpoint, one of them is wrong.

**Choose the right key.** `NSPinnedCAIdentities` pins an intermediate or root authority; `NSPinnedLeafIdentities` pins the leaf certificate. Everything in §8.4 about chain position applies here, so `NSPinnedCAIdentities` on an intermediate is usually the right choice.

**Five documented limitations, all of which have bitten someone:**

`NSIncludesSubdomains` only covers **one** subdomain level. Deeper hosts need their own entries.

Values must be **duplicated in every `Info.plist`** you ship, and again for every distinct host. There is no shared configuration.

You **cannot use User Defined Settings variables** in a localized `Info.plist`, so you cannot parameterise pins per build configuration the way you might expect.

It does **not apply to `WKWebView` or `SFSafariViewController`**, despite both sitting on CFNetwork. Your WebView traffic is unpinned.

During development, changing or removing an entry may require **reinstalling the app** before ATS invalidates the cached trust settings and stops trusting the old identity. Otherwise you will think your change did nothing.

**And the honest caveat.** Its declarative nature is its strength and its weakness. A security auditor can read one file, which is a real advantage. But an attacker can edit that file, re-sign the app and install it with pinning gone — Guardsquare published a walkthrough doing exactly that, and the same result is achievable in memory with Frida. Pinning in code costs more to remove. See §8.6 for when that distinction matters.

#### iOS: URLSessionDelegate, done in the right order

The order of operations here is the part people get wrong, so read the comments.

```swift
import Foundation
import Security
import CryptoKit

final class PinningDelegate: NSObject, URLSessionDelegate {

    // SHA-256 hashes of pinned SPKI — primary and backup
    private let pinnedKeyHashes: Set<String> = [
        "YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg=",
        "Vjs8r4z+80wjNcr1YKepWQboSIRi63WsWXhIMN+eWys="
    ]

    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void
    ) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // 1. Set the SSL policy for this host, so hostname validation happens.
        let policies = [SecPolicyCreateSSL(true, challenge.protectionSpace.host as CFString)]
        SecTrustSetPolicies(serverTrust, policies as CFArray)

        // 2. Let the system validate the chain FIRST. Skipping this is the classic
        //    mistake: you would accept an expired or untrusted certificate that
        //    happens to match your pin.
        var error: CFError?
        guard SecTrustEvaluateWithError(serverTrust, &error) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // 3. Only now compare pins, against the whole chain so an intermediate pin works.
        guard let chain = SecTrustCopyCertificateChain(serverTrust) as? [SecCertificate] else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        for certificate in chain {
            guard let publicKey = SecCertificateCopyKey(certificate),
                  let keyData = SecKeyCopyExternalRepresentation(publicKey, nil) as Data? else {
                continue
            }
            let hash = Data(SHA256.hash(data: keyData)).base64EncodedString()
            if pinnedKeyHashes.contains(hash) {
                completionHandler(.useCredential, URLCredential(trust: serverTrust))
                return
            }
        }

        // 4. No pin matched. Refuse — never fall through to default handling here.
        completionHandler(.cancelAuthenticationChallenge, nil)
    }
}
```

Four notes. **Use `SecTrustCopyCertificateChain`**; `SecTrustGetCertificateAtIndex` and `SecTrustCopyPublicKey` are deprecated on current SDKs. **Hash the SPKI, not the certificate** — that is what `SecKeyCopyExternalRepresentation` gives you. **Iterate the whole chain** so that pinning an intermediate works. And **never call `completionHandler(.performDefaultHandling, nil)` in your failure path** — that is a pinning implementation that does not pin, and it appears in production apps.

For the equivalent value-extraction on the server side, note that your pin is the base64 of the SHA-256 of the SPKI — the same value in both platforms' configuration, which is a useful sanity check when they disagree.

#### Choosing an iOS approach

| | **NSPinnedDomains** | **URLSessionDelegate** | **TrustKit** |
|---|---|---|---|
| **What it is** | Declarative, in `Info.plist`, iOS 14+ | Your own trust evaluation in code | A long-standing third-party pinning library |
| **Pros** | Simplest to add. Auditable — one file. No code to get wrong | Full control of chain position and pin logic. Can be made dynamic. Harder to strip | Handles the fiddly parts for you, with reporting built in. Good first step for a team new to pinning |
| **Cons** | Cannot change at runtime. `NSIncludesSubdomains` covers one level only. Values duplicated per `Info.plist`. Does not cover `WKWebView`. Trivially stripped by editing the plist and re-signing | Easy to implement wrongly — see the four traps in this section. More code to maintain | A dependency in your trust path, which is itself a supply-chain consideration (Chapter 15.4) |
| **Use when** | You want pinning today with minimal risk of implementation error | You need intermediate pinning, dynamic pins, or resistance to stripping | Your team wants pinning working correctly before it wants it perfect |

#### Kotlin Multiplatform: pinning with Ktor

If you share networking through Ktor, there is one thing to know before anything else: **Ktor does not handle pinning for you.** Pinning is enforced by the underlying engine, and each engine needs configuring separately. A project that configures Android and forgets iOS is pinned on one platform and open on the other, which is worse than it sounds because it will pass a test suite.

The shape that works: **pin values in `commonMain`, enforcement in each platform's `actual`.** The hashes are the same value on both platforms (§8.10), so sharing them removes the most common source of drift.

```kotlin
// commonMain — the pins themselves are shared
object CertificatePins {
    const val DOMAIN      = "api.example.com"
    const val CURRENT_PIN = "sha256/YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg="
    const val BACKUP_PIN  = "sha256/Vjs8r4z+80wjNcr1YKepWQboSIRi63WsWXhIMN+eWys="
}

expect fun createPinnedHttpClient(): HttpClient
```

```kotlin
// androidMain — OkHttp engine, so CertificatePinner applies
actual fun createPinnedHttpClient(): HttpClient = HttpClient(OkHttp) {
    engine {
        preconfigured = OkHttpClient.Builder()
            .certificatePinner(
                CertificatePinner.Builder()
                    .add(CertificatePins.DOMAIN, CertificatePins.CURRENT_PIN, CertificatePins.BACKUP_PIN)
                    .build()
            )
            .build()
    }
}
```

```kotlin
// iosMain — Darwin engine, so you implement the challenge handler,
// which is the URLSessionDelegate logic from earlier in this section
// ported to Kotlin/Native: evaluate the chain first, then compare SPKI hashes.
actual fun createPinnedHttpClient(): HttpClient = HttpClient(Darwin) {
    engine {
        handleChallenge { _, _, challenge, completionHandler ->
            // 1. SecTrustSetPolicies + SecTrustEvaluateWithError  (chain first)
            // 2. SecTrustCopyCertificateChain → SecCertificateCopyKey
            //    → SecKeyCopyExternalRepresentation → SHA-256 → base64
            // 3. Compare against CertificatePins; useCredential or cancel
        }
    }
}
```

Two mistakes to avoid, and they are the ones that actually happen. **Configuring one platform and forgetting the other** — put both `actual` implementations in the same pull request, and test both. And **assuming Ktor pins automatically** because the shared code looks like it is doing something; it is not, until an engine enforces it.

Note also that this only covers traffic through your Ktor client. Per §8.6, WebView traffic on Android needs a network security configuration entry as well, and on iOS cannot be pinned at all.

#### The dynamic manifest, in shape

Not a library, just the structure, so you can evaluate one or build one:

```json
{
  "manifest": {
    "version": 42,
    "issuedAt": "2026-09-10T00:00:00Z",
    "expiresAt": "2026-10-10T00:00:00Z",
    "entries": [
      { "host": "api.example.com",
        "pins": ["sha256/YLh1dUR9y...=", "sha256/Vjs8r4z+8...="] }
    ]
  },
  "signature": "base64(ECDSA-P256-SHA256 over canonical bytes of `manifest`)"
}
```

The client logic that makes it safe:

1. Fetch over TLS with the **bootstrap pins** still enforced.
2. **Verify `signature`** against a public key compiled into the app. This is the trust anchor, and it is not a web PKI key.
3. Reject if `version` is **lower** than the cached version *(reasoned)* — otherwise an attacker replays an old manifest containing a pin they have since compromised. This is the same monotonic-counter idea as App Attest's assertion counter in Chapter 10.
4. Reject if past `expiresAt`, and define what happens then: fall back to bootstrap pins, not to no pinning.
5. Cache the manifest, and define a **staleness window** — how long you will run on a cached manifest before you require a fresh one.

Step 3 is the one that gets missed, and it is the difference between dynamic pinning and a downgrade attack.

#### Testing that any of this works

Do not trust the code review. Put mitmproxy in front of the app with its CA installed and confirm the connection **fails**. Then use `objection`'s `android sslpinning disable` and confirm it now succeeds — which tells you your pinning was real and also how easily a determined attacker removes it on a device they control. `MASTG-TECH-0012` is the technique; `MASTG-TEST-0022`, `0242`, `0243` and `0244` are the tests.

---


#### Verify it

Pinning is the control most often believed-in and least often tested, because a working app proves nothing — an unpinned app also works.

**Step 1 — confirm pinning is actually on.** Put a proxy in front of the app with its CA installed on the device. **Pass:** the connection fails. **Fail:** you can read the traffic, which means pinning is absent, misconfigured, or not applied to that client.

**Step 2 — confirm it can be bypassed, and note how easily.**

```
objection -g com.example.app explore
android sslpinning disable
```

**Expected:** traffic now intercepts. That is not a failure of your implementation — it is §14.2's point demonstrated on your own app. What you are measuring is the *cost* to an attacker: whether `objection`'s generic bypass was enough, or whether they needed a custom Frida script for your specific implementation.

**Step 3 — confirm the backup pin works**, which nobody tests until the outage. Temporarily make your primary pin invalid and confirm the app still connects on the backup. If it does not, you have one pin, not two, and §8.4's mandatory backup is decorative.

**Step 4 — confirm both platforms pin the same thing.** The `SPKI-SHA256-BASE64` value on iOS and the `pin digest` value on Android are the same string. If they differ for one endpoint, one is wrong.

Relevant tests: `MASTG-TEST-0022`, `0242`, `0243`, `0244`; technique `MASTG-TECH-0012`.

### 8.11 When pinning breaks: troubleshooting

Pinning failures are opaque by design — the connection simply refuses. Work down this table.

| Symptom | Likely cause | What to do |
|---|---|---|
| App cannot connect after a certificate renewal | The new certificate's SPKI does not match any pin you shipped | Confirm whether your renewal reuses the key pair (§8.5). If not, your backup pin should have matched — check why it did not |
| `SSLPeerUnverifiedException` from OkHttp | Pin hash mismatch | Re-extract the SPKI hash from the live server and compare it byte for byte with the embedded value. The exception message contains the hash the server actually presented |
| `NSURLErrorServerCertificateUntrusted` on iOS | Pin validation failed in your delegate | Check which certificate in the chain you are extracting from. Pinning an intermediate while reading index 0 is the usual cause |
| Works on Android, fails on iOS (or the reverse) | Different certificate chains served per platform, usually via SNI or a CDN | Verify with `openssl s_client -servername`. Make sure the same chain is served to all clients |
| Pinning blocks every request, including in development | No debug bypass configured | Android: a `debug-overrides` block in the network security configuration. iOS: skip pinning under `#if DEBUG`. Make certain neither reaches release |
| Users locked out after an emergency rotation | No backup pin shipped, and no force-update mechanism | This is why backup pins are mandatory (§8.4) and why `MASVS-CODE-2` asks for enforced updates. Ship a hotfix and force the update |
| Works on Wi-Fi, fails on cellular | A carrier transparent proxy. Rare, but it happens | Test across carriers. Note that if this is real, pinning is doing exactly the job you added it for |
| A cloud provider's rotation broke pinning | Your provider rotated the intermediate CA | Pin the intermediate rather than the leaf, or move to dynamic pins (§8.6). Cloud-hosted endpoints rotate on someone else's schedule |
| Works in staging, fails in production | The two environments serve different chains | Extract hashes from both and make sure your pinset covers both, or pin per-environment by build variant |
| Broke immediately after a store release | A build-variant mix-up — debug trust configuration leaked into release | Inspect the release artifact, not the source (Chapter 15.7) |

**The pattern across most of these:** the failure is almost never in the pinning code. It is in the assumption that the certificate you tested against is the certificate your users receive.

---
