---
part: 08
last_verified: 2026-09-11
volatility: low
recheck_because: "Method, not versions"
---

# Part 8: Practice

You learn this by doing it. Build a lab, run an assessment on your own app, write it up — and know what to do on the day something goes wrong.

---

## Chapter 22: Build your test lab

You can't learn this from reading. This chapter gets you to a working setup where you can attack your own app safely and legally.

**One rule before you start: only test apps you own or have written permission to test.** Testing someone else's app without authorisation is illegal in most jurisdictions, regardless of intent. Your own app, your employer's app with sign-off, and OWASP's deliberately vulnerable practice apps are all fine.

### 22.1 What you need

You can get useful results with free tools and an emulator. Here is the shopping list, in order of how much you will use each thing.

**A rooted Android device or emulator.** An emulator is easiest and free: create an Android Virtual Device with a **Google APIs** image rather than a Play Store image, because Play Store images are locked and you can't get root. Then `adb root` works. A physical rooted device is closer to reality and worth having eventually — a cheap second device is a reasonable investment. Note the trade-off: rooting changes the environment you're measuring, which matters when you're testing detection.

**For iOS**, this is harder. A jailbroken device is the full experience and increasingly difficult on current hardware. Without one you can still do a great deal — static analysis of the binary, checking entitlements and `Info.plist`, inspecting a simulator's file system, and reviewing your own source. Start there rather than not starting.

**Tools, in rough order of usefulness:**

`adb` — the Android Debug Bridge, from the platform tools. Your shell into the device.

**JADX** — decompiles an APK into readable Java. Use `jadx-gui` and browse your own app for twenty minutes; it's an education.

**Frida** — runtime instrumentation. Install the Python package on your machine and push the matching `frida-server` binary to the device. Version match matters and is the most common setup problem.

**objection** — Frida-powered, with commands for the common tasks so you don't write scripts on day one. `objection -g <package> explore` then `android sslpinning disable` is your first real experiment.

**mitmproxy** — a proxy you can read. Install its CA certificate on the device, point the device's proxy at your machine, and watch your own traffic. On modern Android you'll also need to allow user-added CAs in a *debug* network security configuration, which is itself a useful lesson in why that setting matters.

**semgrep** — pattern-based static analysis. Many MASTG demos use it, and it's how you find a class of issue across a whole codebase rather than one instance.

**apktool** for repackaging, **radare2** or `rabin2` for iOS binaries, and `strings` — which you already have.

### 22.2 Practice targets before your own app

Learn the tools on something designed for it, so you're debugging one thing at a time.

The **OWASP MAS Test Apps** for Android and iOS embed code samples so every MASTG demo is reproducible on a real device. Start here — each demo tells you what to run and what you should see.

The **MAS Crackmes** are deliberately protected apps for reverse-engineering practice: <https://mas.owasp.org/crackmes/>

### 22.3 Your first five experiments

Do these in order on your own app. Each takes minutes and each will teach you something you didn't expect.

**One: `strings` on your release APK.** Not the debug build. Read what comes out. Write down anything sensitive.

**Two: open it in JADX.** Find your API base URL. Find one security decision — a root check, a feature flag, a validation. Ask yourself how long it would take to change it.

**Three: read your own app's data directory.** `adb shell` then `run-as <package>` (or root) and look in `/data/data/<package>/`. Open the shared preferences files and any SQLite database. Look for tokens and personal data in plaintext.

**Four: proxy your traffic.** Get mitmproxy in front of the app and read a request. If pinning is enabled, note that it fails — then use `objection` to disable pinning and note that it now succeeds. That contrast is the single most clarifying experience in mobile security.

**Five: hook something.** With Frida, hook your root-detection function and make it return `false`. Then hook `Cipher.doFinal` and log the arguments — `MASTG-DEMO-0106` shows you how. Watching your own plaintext scroll past changes how you design.

### 22.4 What to do when a step fails

Each of these will happen to you. None of them means you have done something wrong.

**Frida won't connect.** Version mismatch between the client and `frida-server`, or the server isn't running, or you're not root. Check versions first.

**Proxy shows no traffic.** The app may be ignoring the system proxy (some HTTP clients do), or using a non-HTTP protocol, or pinning is rejecting the connection before you see it. Check the app's logs.

**Certificate errors everywhere.** The device doesn't trust your proxy CA, or the app doesn't trust user-added CAs — which on modern Android is the default and correct behaviour. Use a debug network security configuration.

**Nothing in the data directory.** You might be looking at the wrong user profile, or the app genuinely stores little locally — which would be good news.

Each of these failures is itself information about your app's posture. Note it rather than fighting it.

---

## Chapter 23: Running an assessment and writing it up

Now you have a lab. This chapter is the method, and then how to communicate what you found — which is the part that determines whether anything changes.

### 23.1 Scope it first

Write down, before you start: which app and build, which platforms, which device and OS versions, which flows are in scope, and what you're *not* looking at. Ten minutes of scoping saves you from a report that's impossible to interpret later.

Pick a **testing profile** to aim at (Chapter 3.2): **MAS-L1** for a basic level on an app handling sensitive data, **MAS-L2** for highly sensitive data, **MAS-R** if resilience against reverse engineering matters. This sets your expectations so you're not writing up a missing anti-debugging control on a content app.

### 23.2 Work the standard, not your instincts

Take the MASWE catalogue in Chapter 27 — seventy-eight weaknesses — and go down it, marking each **yes**, **no**, or **not applicable** for your app. For each *yes*, find the matching MASTG test and run it.

This is slower than poking around and dramatically better, for two reasons. You cover the things you'd never have thought of, and your output maps to a standard someone else recognises.

Each MASTG test page tells you what to look for, which tools to use, how to reproduce it on each platform, and what a passing implementation looks like. Use the URL pattern from the ID:

`https://mas.owasp.org/MASTG/tests/android/MASVS-STORAGE/MASTG-TEST-0001/`

### 23.3 Rate what you find

Severity is likelihood combined with impact, and both need thinking about.

For **impact**, ask what an attacker gains. Reading their own cached data is not the same as reading another user's account, which is not the same as moving money.

For **likelihood**, ask what the attack requires. Something exploitable remotely with no special access is far more likely than something requiring a rooted device and physical possession. "Requires root" is a genuine mitigating factor and stating it honestly builds trust — as does not using it to dismiss something that matters.

Be consistent, and be prepared to defend each rating. A report where everything is critical gets ignored entirely.

### 23.4 Write the report

Structure it so a reader can act:

**Scope and date.** What you tested, which build, which devices and OS versions. Without this the report ages into uselessness.

**Summary.** Three or four sentences: what you assessed, what the overall posture looks like, and the two or three things that matter most. Assume this is all a senior stakeholder reads, and write it accordingly.

**Findings.** For each one: a clear title, the MASVS control and MASWE weakness, severity, reproduction steps precise enough that someone else gets the same result, evidence, and **impact in business terms.**

That last part is what gets work funded. Compare:

> *Token stored in plaintext in SharedPreferences.*

with:

> *An attacker with brief physical access to an unlocked phone, or malware on a rooted device, can extract a session token that remains valid for 90 days and is not bound to the device — allowing full account access from the attacker's own machine, with no further interaction from the user.*

Both describe one bug. Only one of them gets prioritised.

**What held.** List the controls you tested that worked. This is counterintuitive and it's what makes your report credible. "Pinning held against objection's standard bypass and required a custom Frida script" tells a reader you understand the difference between a tool's output and an assessment.

**Remediations.** Specific, with before and after where you can. Link the relevant `MASTG-BEST` practice so the developer has the pattern, not just the problem.

**Residual risk.** What you're accepting and why. Senior reviewers read this section first, because it shows whether you understand trade-offs or merely found things.

### 23.5 Getting it fixed

A report nobody acts on was a waste of a week. Two things help.

**Turn findings into tickets** yourself, with owners, rather than handing over a document and hoping. Include the reproduction steps in the ticket so the developer doesn't have to open the report.

**Retest and record it.** A finding isn't closed because someone pushed a commit; it's closed because you ran the test again and it passed. Note the date and the build. That retest history is what turns an assessment into a security programme.

### 23.6 Make it a habit

An annual assessment finds a year of accumulated problems at the worst possible moment. Instead:

Pick **one MASWE weakness a week.** Find the matching test. Run it against your app. Write down the result. Fifty-two weeks of that and you have covered the catalogue, built the skill, and produced a documented history — and you become the person the team asks.

---

## Chapter 24: When something goes wrong

Every other chapter is about prevention. This one is about the day prevention failed, because that day arrives and mobile has specific constraints that make it different from a server incident.

### 24.1 The constraint that shapes everything

Mobile incident response differs from server incident response for one reason, and everything else follows from it.

**You cannot patch a mobile app quickly.** A server fix deploys in minutes. A mobile fix needs a build, a store review, and then *users choosing to update* — and a meaningful share of your install base won't update for weeks, or ever.

So mobile incident response leans on things you can change *without* a release:

**Server-side mitigation.** Reject the vulnerable request pattern, tighten validation, revoke credentials, disable an endpoint. Almost always your fastest lever, and often sufficient.

**Feature flags and remote configuration.** If you can turn the affected feature off remotely, you can stop the bleeding in minutes. This is why remote kill switches are a security capability and not just a product one — and why Chapter 8 asks for one on pinning specifically.

**Forced update.** `MASVS-CODE-2` and `MASWE-0043` exist for this moment. If you have a mechanism to require a minimum version, you can compel the fix. If you don't, build one before you need it — during an incident is a bad time to discover you can't.

### 24.2 Prepare before you need it

Four things, none of which take long, all of which are painful to arrange under pressure:

**Know who to call.** Who decides to disable a feature? Who talks to the regulator? Who approves an emergency release? Write down names, not roles.

**Know what your logs contain.** During an incident you need to answer "who was affected and when," and you can only answer it from data you were already collecting. Log security decisions with enough context to investigate — and, per Chapter 12, never the secrets themselves.

**Have a rotation runbook.** Which credentials exist, where they live, and how to rotate each one. Chapter 15's discipline pays off here.

**Know your notification obligations.** GDPR requires breach notification within 72 hours. That clock starts before you finish understanding the problem, which is exactly why you find out the requirement now rather than then.

### 24.3 The sequence

Five steps, in this order. The ordering matters more than the detail.

**Contain.** Stop it getting worse. Revoke the leaked credential, disable the endpoint, turn off the feature. Resist the urge to investigate first — containment is cheap and reversible; a widening breach is not.

**Assess.** What was accessed, by whom, how many users, over what window. Be careful about early numbers; the first estimate is usually wrong and it's the one that ends up in the notification.

**Notify.** Follow your legal obligations and tell your users the truth. Vagueness reads as concealment and costs more trust than the incident did.

**Fix.** Server-side first because it's fast. Then the client fix, with a forced update if warranted.

**Learn.** A blameless post-mortem: what happened, why the control that should have caught it didn't, and what changes. The output is a change to your process, not a person to blame — teams that blame individuals stop reporting problems early, which is the one thing you cannot afford.

### 24.4 The specific mobile cases

Five scenarios you are most likely to meet, and what each one actually demands of you.

**A signing key is compromised.** With Play App Signing, your upload key is recoverable — register a new one (Chapter 15.6). Without it, an attacker can ship code as you, and you're into store escalation and possibly a new listing. This is the strongest argument for the split key model, and it's much better made before the incident.

**A secret leaked in your app package.** Rotate immediately and assume it's public. Then ask why it was in the package, because that's the actual fix — the leak is a symptom of Chapter 15.2's classification not being applied.

**Certificate pinning broke.** Users can't connect. Use your kill switch. If you don't have one, you're shipping an emergency release and waiting for review — which is precisely the outage risk that Chapter 8's critics were talking about.

**A vulnerable dependency lands in a shipped version.** Mitigate server-side if you can, ship the update, and consider a forced update if the exploit is remote and unauthenticated.

**A cloned version of your app appears.** Store takedown, and check whether attestation would have prevented the clone from reaching your API. Often it would (Chapter 9).

### 24.5 The uncomfortable value of an incident

An incident gives you organisational attention you cannot otherwise buy. The security work that was deprioritised for two quarters becomes fundable in a week.

Use it well and use it honestly: bring the plan you already wrote, name the controls that would have prevented this specific event, and don't overreach into unrelated wishes. Credibility spent well here lasts for years — and credibility spent badly, on an inflated ask, does not come back.

---


## Chapter 25: Reference — testing method at a glance

Building controls is the easy half. Proving they hold is what separates an engineer who has read about security from one who can be trusted with it. This chapter is a method, not a checklist — the difference being that you are meant to think while doing it.

### 25.1 Where the material is

Work the **MASTG** test cases rather than the theory. Since the v2 refactor, every test is individually referenceable with structured metadata and reproducible demos, so you can go directly to what you need instead of reading a book-length guide front to back.

Each MASVS control links to specific tests. `MASVS-STORAGE-1`, for instance, maps to tests covering `SharedPreferences` analysis, Keychain inspection, SQLite checks and log review. A test case tells you what to look for, which tools to use, how to reproduce on both platforms, and what a passing implementation looks like. The mapping table is the thing to bookmark.

Two practice environments exist so that you are not learning tooling and auditing production simultaneously. The **MAS Test Apps** for Android and iOS are purpose-built skeleton apps with code samples embedded, so every demo is reproducible on a real device. The **MAS Crackmes** are deliberately protected apps for reverse-engineering practice.

### 25.2 Your toolkit

Everything here is free. Chapter 22 covers installing and using them; this is what each one is for.

**JADX** decompiles an APK so you read your own logic as an attacker sees it. **radare2** and `rabin2` do the equivalent for iOS binaries, and appear throughout the MASTG's iOS demos. **Frida** attaches to a running process for hooking and instrumentation. **objection** is Frida-powered and gives you storage inspection and pinning bypass without writing scripts. **adb** and `sqlite3` let you inspect `/data/data/<package>/`. **mitmproxy** or **Burp** intercept traffic to confirm whether pinning actually holds. **semgrep** appears across the MASTG demos for static pattern matching, which is how you find a class of issue across a codebase rather than one instance. **`strings`** is the thirty-second test that finds embedded secrets. **`trufflehog`** and **GitGuardian** scan history and commits.

### 25.3 A first assessment, in order

Do these in sequence on your own app. Each step informs the next.

**One.** Build a release artifact. Run `strings`. Write down everything sensitive that appears. Do not skip this because you are sure it is clean.

**Two.** Decompile with JADX. Find your API endpoints and any security-relevant logic. Ask honestly how long it would take you to change one of those decisions and repackage.

**Three.** Install on a rooted device or emulator. Inspect app storage for plaintext tokens, cached personal data, and log files.

**Four.** Put a proxy in front of it. Does traffic intercept? If pinning is enabled, does it hold?

**Five.** Attach Frida. Bypass your own root detection. Bypass your own pinning. Hook your own biometric callback. Note how long each took.

**Six.** Replay a valid authenticated request from a different device. What stops you? (Chapter 12.3.)

**Seven.** Write it up.

### 25.4 Writing findings properly

The findings document is the artifact that changes how people see you, so write it as a document rather than as a dump.

Open with **scope and date**: what you tested, which build, which device and OS version. Without this the document ages badly and nobody can tell whether it still applies.

For each **finding**, give the MASVS control and MASWE weakness it maps to, a severity, reproduction steps precise enough that someone else gets the same result, evidence, and, most importantly, **impact stated in business terms**. "Token readable from app storage on a rooted device" is a fact. "An attacker with brief physical access to an unlocked phone can extract a credential that remains valid for 90 days and is not bound to the device" is a finding someone will fund.

Include **what held**. This is counterintuitive and it is what makes the document credible. A report that only lists failures reads like a tool output; one that says "pinning held against objection's standard bypass and required a custom Frida script" reads like it was written by someone who understands the difference.

Then **remediations** with before and after, and **residual risk** — what you accepted, and why. That last section is the one senior reviewers read first, because it tells them whether you understand trade-offs or just found things.

### 25.5 The claim this earns you

There is a specific sentence that gets people hired into mobile security, and it is not "I know which controls to specify."

It is: **"I attacked my own app, here is what I found, here is what I changed, and here is what I decided to accept."**

Those are different claims and interviewers can tell them apart within two questions.

---
