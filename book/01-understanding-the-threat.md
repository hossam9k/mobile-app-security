---
part: 01
last_verified: 2026-09-11
volatility: medium
recheck_because: "Annual reports supersede each other"
---

# Part 1: Understanding the threat

## Chapter 1: What an attacker can actually do

Every design decision in mobile security follows from an accurate picture of the adversary's capabilities. Most bad designs come from an inaccurate one — usually from imagining the attacker is a stranger on a network, when in fact the attacker owns the device your code is running on.

### 1.1 The device is not yours

When your app runs on a user's phone, you are executing code inside an environment that person fully controls. If that person is an attacker, or the device is rooted, jailbroken, emulated or simply instrumented, then every assumption you inherited from server-side development stops holding.

Concretely, assume an attacker can do all of the following, on both platforms, at will:

**Read your code.** A production APK decompiles to readable Java or Kotlin-like source in minutes with JADX. An IPA yields to radare2 and Hopper. Your class names, method flow, API endpoint structure, and any logic you wrote to make security decisions are all legible. Obfuscation renames things; it does not hide control flow from someone willing to spend an afternoon.

**Read every constant in the binary.** Run `strings` on your own release build. Whatever comes out, an attacker already has: API keys, endpoint URLs, encryption keys, debug flags, internal hostnames. This takes thirty seconds and it is the single most educational experiment in this book.

**See all your traffic in cleartext.** On a device they control, an attacker installs their own certificate authority and proxies your traffic through mitmproxy or Burp. TLS protects you from a stranger on the coffee shop network. It does not protect you from the person holding the phone.

**Modify behaviour at runtime.** Frida attaches to your process and lets an attacker replace any method's implementation while the app runs. A function that returns `true` when the device is rooted can be made to return `false`. A biometric callback can be invoked without any biometric. A certificate validator can be replaced with one that accepts everything.

**Read process memory.** Anything you decrypt "temporarily" exists in memory, and memory is readable. This is why "we decrypt it just before use" is not a mitigation.

**Read local storage.** On a rooted or jailbroken device, `/data/data/<package>/` and the app sandbox are open. SQLite databases, preference files, cached responses, and log files are all available.

**Repackage and redistribute.** Your app can be modified, re-signed with a different key, and distributed. Users who sideload will not notice.

### 1.2 What follows from this

Once you accept that list, one principle organises everything else:

> **Make secrets useless if found, not impossible to find.**

Do not spend your budget trying to prevent extraction. You will lose, and the loss is not close. Spend it ensuring that what gets extracted has no value without a server-side check that the attacker does not control.

Three consequences deserve stating explicitly, because teams violate them constantly.

**The client is never the trust boundary.** Your server is. Any decision that matters — whether this user may transfer money, what this item costs, whether this account may be modified — happens server-side or does not happen securely at all.

**Client-side checks produce signals, not verdicts.** Root detection tells your backend "this session looks unusual." It does not tell your app "refuse this user." The distinction sounds pedantic and is load-bearing; Chapter 14 explains exactly why.

**Defence in depth means genuinely independent layers.** Each layer must reduce risk on its own, because you must assume any single layer will be defeated. Layers that all fail together are one layer wearing a costume.

### 1.3 Who is actually attacking you

"The attacker" is not one person, and treating them as one leads to spending money in the wrong places. In practice you face four groups with very different economics.

**The opportunist** runs automated tooling against many apps looking for cheap wins: an exposed API key, an unauthenticated endpoint, a token in cleartext. They will not spend an hour on you. Almost every control in this book stops them, and this is where obfuscation and basic hygiene pay for themselves.

**The cloner** repackages your app to inject ads, steal credentials, or bypass payment. They need your binary to run modified. Signature verification, attestation, and integrity checks raise their cost materially.

**The fraudster** uses your app as intended, at scale, against your business logic — creating accounts, abusing promotions, laundering transactions, exhausting a metered resource. Client-side controls barely touch them. Backend risk scoring, rate limiting, and attestation-as-signal are what work.

**The targeted adversary** wants one specific thing badly and has time and money. They will defeat every client-side control you ship. What you can do is ensure that defeating them yields nothing without also compromising your backend, and that you detect them.

The reason to name these separately is triage. A news app worries about the opportunist. A banking app worries about all four. Knowing which one a control addresses stops you from arguing about obfuscation when your real problem is that your API trusts a client-supplied user ID.

---

## Chapter 2: The economics of the numbers

You will be asked to justify security work in money. Use current figures and understand what they measure, because a stakeholder who catches you citing a stale number will discount everything else you say.

### 2.1 What breaches cost

IBM's *Cost of a Data Breach* report is the standard reference. The 2026 edition, released 29 July 2026, covers 602 organisations breached between March 2025 and February 2026.

The global average reached **$4.99 million**, up 12% year over year and a record. The United States averaged **$11.5 million**, more than double the global figure. Mean time to identify and contain rose to **247 days**, reversing five consecutive years of improvement.

Watch the trajectory, because people quote whichever year suits them: 2024 was $4.88M, 2025 *fell* to $4.44M — the first decline in five years — and 2026 rose to a record. If someone cites $4.88M in 2026, they are two reports behind.

For the first time, IBM broke out AI-enabled breaches: **one in four** malicious breaches involved AI, and those averaged roughly **$6 million**, about $1 million above the mean. Deepfake and impersonation attacks drove the largest share of those incidents.

- <https://www.ibm.com/think/insights/cost-of-a-data-breach-industrial-sector>
- <https://databreachcost.com/report/2026>

### 2.2 What leaks look like

GitGuardian's *State of Secrets Sprawl 2026*, the fifth edition, published 17 March 2026, found **28.65 million** new hardcoded secrets added to public GitHub in 2025 — up 34%, the largest single-year jump recorded. Hardcoded secrets on public GitHub grew 152% between 2021 and 2025.

More usefully, it found that **64%** of secrets validated back in 2022 are still active. Leaking is common; remediating is rare. That asymmetry is the actual problem.

Two findings matter specifically to modern teams. **AI-assisted commits leak secrets at roughly double the rate of human-only commits, 3.2% versus a 1.5% baseline** — and eight of the ten fastest-growing leak categories are tied to AI services. Separately, **MCP configuration files alone exposed 24,008 unique secrets**, partly because official documentation encouraged hardcoding patterns.

And the location of leaks has shifted: **59%** of compromised machines in one analysed supply-chain attack were CI/CD runners rather than developer laptops, and about **28%** of secret incidents originate outside code repositories entirely, in Slack, Jira and Confluence. Those out-of-code leaks were 13 percentage points more likely to be rated critical.

- <https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/>
- <https://www.gitguardian.com/state-of-secrets-sprawl-report-2026>

### 2.3 How to use these honestly

Two cautions, because misusing these numbers costs you credibility permanently.

First, these are enterprise averages. A mobile security incident at a mid-sized company usually costs far less than $4.99 million. If you present the average as your exposure, someone will eventually notice, and every future request you make will be discounted. Say "the industry average for a full enterprise breach is X; our realistic exposure is Y, and here is how I derived Y."

Second, resist the temptation to invent ranges. Any "$50,000 to $500,000 per incident" figure you have seen is an estimate someone made up and everyone repeated. If you need a number for your own organisation, derive it: users affected × notification cost, plus support load, plus engineering time, plus whatever your regulator's penalty schedule says. That number will be defensible. The borrowed one will not.

---

## Chapter 3: The standard, and how its pieces fit

There are four OWASP artifacts in this space and people conflate them constantly. Getting them straight is worth twenty minutes, because it is the vocabulary that security teams, auditors and interviewers use.

### 3.1 The four pieces

OWASP publishes four separate things for mobile security. Here is what each one is for.

**The Mobile Top 10** is an awareness list of commonly observed risks, maintained by its own working group. It was updated in late 2024 — the first update in eight years. Its job is to make risk legible to people who are not specialists. It is not a standard and you cannot verify against it.

**MASVS**, the Mobile Application Security Verification Standard, is the standard: what must be true of a secure app. The current version is **v2.1.0**, released 18 January 2024, still current in 2026. It contains **eight categories holding twenty-four controls**, each with an ID like `MASVS-STORAGE-1` that a finding can point at.

**MASWE**, the Mobile App Security Weakness Enumeration, was introduced in July 2024 to fill the gap between high-level controls and low-level tests. It enumerates seventy-eight specific weaknesses — the things that actually go wrong.

**MASTG**, the Mobile Application Security Testing Guide, is how you verify all of it: test cases, techniques, background knowledge, best practices, and runnable demos, per platform. **v2.0.0** is the first stable non-beta release, completing a multi-year refactor that broke the old monolithic guide into individually referenceable, machine-readable components.

The chain runs:

```
MASVS control        →  MASWE weakness       →  MASTG test         →  MASTG demo
what must be true       what goes wrong         how to check it       a runnable example

MASVS-STORAGE-1      →  MASWE-0001           →  MASTG-TEST-0001    →  MASTG-DEMO-0059
"securely stores        "Sensitive Data         "Testing Local        "Using SharedPreferences
sensitive data"          Stored Unencrypted      Storage for           to Write Sensitive Data
                         in Private Storage"     Sensitive Data"       Unencrypted"
```

Learn that chain. It is how you turn "make the app secure" into something a developer can fix and a tester can confirm.

**One thing to watch when you look tests up.** The v2 refactor is still in progress. Low-numbered tests (roughly `MASTG-TEST-0001` to `0100`) are the original v1 tests, and the project is progressively splitting them into smaller "atomic" v2 tests with higher numbers. Some v1 tests are already marked deprecated on their own page, with links to the v2 tests that replace them — `MASTG-TEST-0044` is one example.

So when you open a test page, **check for a deprecation banner first.** If you see one, follow it to the current test. Throughout this book, where a v1 ID is still the clearest way to point at a topic, it is used — but the page is the authority, not the book.

### 3.2 The levels that are not levels any more

This is the single most common way to date yourself in a security conversation.

Before MASVS v2.0.0 (April 2023), the standard contained verification levels: L1 as a baseline, L2 adding defence in depth for apps handling sensitive data, and R for resilience against reverse engineering.

Those levels **no longer live in MASVS**. They moved into the MASTG as *testing profiles*: **MAS-L1** for apps handling sensitive data at a basic level, **MAS-L2** for highly sensitive data requiring a higher level, and **MAS-R** for apps needing resilience against reverse engineering and tampering, independent of security level.

So the correct phrasing is "the MAS-L2 profile," not "MASVS L2." Likewise, if a blog post says "MSTG" rather than "MASTG," or cites L1/L2/R as MASVS levels, it predates the refactor and its API-level detail is probably stale too.

### 3.3 What OWASP will not do for you

OWASP states plainly that it **cannot certify** mobile applications, and does not accredit third parties to do so. Anyone selling "OWASP certification" is selling something that does not exist. What you can do is publish a *certification statement* — your own claim, verifiable by anyone with the MASTG, about which controls you meet and how you tested. That is more credible than a badge anyway, because it is falsifiable.

The MASVS is licensed under Creative Commons Attribution-ShareAlike 4.0, with no fee.

### 3.4 The tension inside the standard

Worth knowing early, because it will confuse you otherwise: **MASVS-NETWORK-2 asks for identity pinning on all remote endpoints under the developer's control, while OWASP's own Pinning Cheat Sheet argues that most apps should probably never pin.**

Both are OWASP. Both are current. They are not actually contradictory. The scoping phrase "under the developer's control" does the work, and Chapter 8 unpacks it. But discovering the apparent conflict mid-audit is disorienting. Now you know.

Primary sources:
- MASVS — <https://mas.owasp.org/MASVS/>
- MASWE — <https://mas.owasp.org/MASWE/>
- MASTG — <https://mas.owasp.org/>
- Release history — <https://github.com/OWASP/mastg/releases>

---
