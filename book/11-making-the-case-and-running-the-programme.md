---
part: 11
last_verified: 2026-09-11
volatility: medium
recheck_because: "Breach-cost figures update annually"
---

# Part 11: Making the case and running the programme

Everything before this part is for engineers. This part is for the conversation where you ask for time and budget, and for the plan you run once you get it.

**If you are a stakeholder rather than an engineer, you can read this part on its own.** It is written to stand alone. Chapters 29 and 30 give you the risk and the regulatory position, Chapter 31 shows what comparable teams do, and Chapter 32 is the plan with costs, phases, owners and success criteria.

**If you are the engineer making the case,** the most useful thing in this part is Chapter 29.4 — how to scope your *own* exposure instead of quoting an industry average. Quoting averages is how security people lose credibility, and you only get to lose it once.

---

## Chapter 29: The business case

### 29.1 Why mobile, and why now

Your mobile app is the main way customers reach you. It is also the largest and most accessible attack surface you have, for one structural reason: **the app runs on hardware you do not control.** A server sits in a data centre you own. Your app sits in the hands of anyone who downloads it, including anyone who wants to take it apart. Chapter 1 covers what that means technically.

### 29.2 What the current numbers say

All figures below are from the IBM *Cost of a Data Breach Report 2026*, released 29 July 2026, covering 602 organisations breached between March 2025 and February 2026, and GitGuardian's *State of Secrets Sprawl 2026*, published 17 March 2026.

| Finding | Figure |
|---|---|
| Global average cost of a breach | **$4.99M** — up 12%, a record across the study's 21 years |
| United States average | **$11.5M** — more than double the global figure |
| Healthcare | **$6.64M** — costliest sector for the 13th consecutive year, though down 10.5% from $7.42M |
| Financial services | **$6.29M** — second, and closing the gap |
| Mean time to identify and contain | **247 days** — up, reversing five consecutive years of improvement |
| AI-enabled breaches | **One in four** malicious breaches, up 56% year over year, averaging about **$6M** |
| Ransomware | **39%** of breached organisations hit at least once, up from 24% in 2023 |
| Cost of customer PII | **$192 per record** — and customer PII appeared in 52% of breaches |
| New secrets leaked on public GitHub | **28.65 million** in 2025, up 34% — the largest single-year jump recorded |
| Secrets still live | **64%** of secrets validated in 2022 remain active today |
| AI-assisted commits | Leak secrets at **3.2%** versus a **1.5%** human-only baseline |

**Read the trend, not just the headline.** 2024 was $4.88M. 2025 *fell* to $4.44M — the first decline in five years. 2026 rose to a record. If a document quotes $4.88M today, it is two reports behind. If it quotes the 2025 decline as evidence that things are improving, it is one behind.

**Two findings deserve extra weight in a mobile conversation.** The 247-day detection figure means a breach you have not noticed is the normal case, not the exception — which is an argument for backend monitoring rather than client-side controls. And the secrets figures are directly about your build pipeline, which is Part 6.

### 29.3 What you are risking, with real precedents

Abstract risk does not get funded. Each row below pairs a category with something that actually happened and was publicly documented.

| Risk | What it looks like | A documented precedent |
|---|---|---|
| **Account takeover** | Stolen tokens replayed from attacker devices; fraud losses, remediation cost, support load | Regulatory action follows failures here, not just fraud losses |
| **Payment fraud** | Business logic abused at scale — replayed requests, manipulated amounts, promotion abuse | Financial services now sits second on breach cost at $6.29M |
| **Data breach** | Personal data exposed through storage, logging, or a leaked credential | Global average $4.99M; customer PII at $192 per record |
| **Regulatory penalty** | Fines up to 4% of global annual turnover under GDPR | **Meta: €1.2 billion**, Irish Data Protection Commission, May 2023 — the largest GDPR fine to date, for transferring EU user data to the US without adequate safeguards. Meta appealed. Cumulative GDPR fines have passed **€7.1 billion** since 2018 |
| **Private litigation** | Class actions now rival regulators | **Capital One: $190 million** class-action settlement. **T-Mobile: $350 million**. **Equifax: at least $575 million** with the FTC, CFPB and 50 states |
| **Reputation** | Churn, acquisition cost, brand damage | **41%** of 2026 ransomware attacks included brand-reputation threats such as public shaming and data leaks |

Two honesty notes on this table, because you will be challenged on it.

**The Meta fine was about data transfers, not a mobile security failure.** It is the right example for the *scale* of regulatory risk and the wrong example for "this is what happens if we skip certificate pinning." Use it precisely or someone will correct you.

**Capital One's $190 million was a settlement, not a fine.** The distinction matters because it shows private litigation is a separate exposure from regulatory action — you can face both.

### 29.4 How to scope your own exposure — do this instead of quoting averages

This is the most important section in the chapter.

An industry average is a sample of enterprises with enterprise legal teams, enterprise notification obligations and enterprise breach volumes. A mobile incident at a mid-sized company usually costs far less. **Present the average as your exposure and, when someone eventually notices, every future request you make gets discounted.**

So derive your own number. You need four inputs, and you already have three:

**Users affected.** Not your whole install base — the population reachable by the specific weakness. "Tokens readable on rooted devices" is not all users.

**Notification cost.** Per-user, from whoever handles your compliance. GDPR gives you 72 hours from becoming aware, so this cost is real and near-term.

**Response cost.** Engineering days to investigate and fix, plus the support load, plus any forensic help. Your team knows its own day rate.

**Regulatory exposure.** The applicable penalty schedule, from whoever owns compliance. A percentage of turnover is a ceiling, not a forecast.

Then say it like this:

> "The industry average for a full enterprise breach is $4.99 million. That is not our exposure. Ours is approximately X, derived as follows — and here is what reduces it."

That sentence is more persuasive than any borrowed statistic, because it survives scrutiny.

**And resist inventing ranges.** Any "$50,000 to $500,000 per incident" figure you have seen is an estimate someone made up and everyone repeated. If you need a range, derive it and show your working.

### 29.5 The return side, stated carefully

The strongest honest argument is not a single ROI number. It is three points:

**Prevention is cheap relative to response.** Chapter 32 estimates the programme at 18–26 engineering days. Compare that to the response cost you derived in §29.4 — for most teams, one prevented moderate incident covers it. Say "for most teams" rather than asserting it as certain.

**Detection time drives cost.** With mean time to identify and contain at 247 days and rising, monitoring and logging are not overhead — they are the lever with the clearest cost link in the whole report.

**Some of this is not optional.** Where a regulator or an auditor requires a control, the business case is compliance, not risk reduction, and arguing risk numbers wastes everyone's time. Know which of your controls are in which category before you walk into the room.

---

## Chapter 30: The regulatory landscape

You do not need to be a lawyer. You do need to know which rules apply to you, who in your organisation owns them, and what they require of your app. That last part is short.

### 30.1 The frameworks you are most likely to meet

Six frameworks cover most situations. Find the rows that apply to you and ignore the rest.

| Framework | Applies when | What it requires of your app |
|---|---|---|
| **GDPR** (EU/EEA) | You have any EU users | A lawful basis for processing, data minimisation, purpose limitation, user rights of access and deletion, and breach notification within **72 hours** of becoming aware. Fines up to **4% of global annual turnover** or €20 million, whichever is higher |
| **PCI-DSS** | You handle payment card data | Encryption of cardholder data at rest and in transit, restricted access, logging. Most apps avoid scope entirely by tokenising through a payment provider — **that is the cheapest compliance decision available to you** |
| **SOC 2** | Enterprise or B2B customers ask for it | Access controls, audit logging, monitoring, and evidence that your controls operate over time. It is an audit of process, not a technical standard |
| **HIPAA** (US) | You handle protected health information | PHI encrypted at rest and in transit, access controls, audit trails, breach notification |
| **Regional financial regulation** | You operate in a supervised market | Varies widely and is often prescriptive about specific controls. Central-bank certification programmes typically test the app directly against a defined test suite |
| **Store policies** | Always | Data declarations that match actual behaviour, permission justification, no undisclosed tracking |

### 30.2 Store policy is the fastest-moving regulator

Worth saying plainly, because engineers systematically underrate it: **Apple and Google will act in days, where a regulator takes years.** An app whose data declaration does not match its behaviour gets rejected or removed, and that is a revenue interruption rather than a future fine.

Chapter 18.3 covers the engineering consequence: you cannot declare accurately unless you know what actually leaves the device, which means capturing your own traffic and checking it against your declaration. `MASTG-TEST-0206` is the test. Teams are routinely surprised, usually by a third-party SDK.

### 30.3 How to use this chapter

Three actions, in order:

**Find the owner.** Someone in your organisation already owns compliance. Find them before you design a feature that touches regulated data, not after. This is a fifteen-minute conversation that occasionally prevents a nine-month remediation.

**Map your controls to their requirements.** When a control exists because a regulator requires it, label it that way in your own planning. It changes how the prioritisation conversation goes.

**Separate "required" from "advisable."** Mixing them is why security proposals get cut wholesale. If three of your ten items are mandatory, say so and defend the other seven on their merits.

---

## Chapter 31: What comparable teams do

Useful for calibration: you are not proposing anything exotic. A caution first, though, and please keep it when you reuse this material.

**These are patterns observable from the outside** *(reasoned)* — from platform documentation, published engineering writing, app behaviour, and what the stores and regulators require. They are **not** confirmed descriptions of any named company's internal architecture, and you should not present them as such. If someone in the room has worked at one of these companies, an overstated claim will be corrected in public.

### 31.1 The patterns, by category

Different app categories converge on different configurations, and the reasoning behind each is worth borrowing even when the category is not yours.

**Banking and payment apps** cluster around the strongest configuration available: hardware-backed key storage, biometric authentication bound to cryptographic operations for transactions, certificate pinning, and device attestation. Two forces drive this rather than one — the value of a successful attack, and regulators who require demonstrable defence in depth. If you work in this category, "OWASP says most apps should not pin" will not end the conversation, because your auditor is not reading OWASP.

**Ride-sharing, delivery and marketplace apps** typically use **progressive security**: minimal friction for browsing and discovery, full controls at the payment and account-change boundary. The reasoning is sound and worth borrowing — friction spent where it buys nothing gets routed around by users, which leaves you less secure than before (Chapter 11.5). Payment is usually tokenised through a provider, which takes PCI scope off the app entirely.

**Messaging apps** with end-to-end encryption pair it with pinning and tamper detection, because their threat model includes network-level adversaries and the content is the product.

**Large e-commerce apps** lean on platform attestation combined with backend fraud scoring and rate limiting rather than heavy client-side hardening — consistent with Chapter 12's argument that the backend is the only real arbiter.

### 31.2 The pattern behind the patterns

Read down that list and one thing generalises: **the strongest teams put their weight on the server, and use client-side controls to produce signals rather than verdicts.** Nobody serious is betting on obfuscation. They are betting on attestation, risk scoring and server-side validation, with client hardening as the layer that raises cost for the opportunist.

That is the same conclusion Chapters 12 and 14 reach from first principles. It is reassuring when the theory and the observable behaviour agree.

---

## Chapter 32: The plan

A phased programme you can put in front of a manager. Adjust the effort to your team; the sequence is the part that matters, because each phase makes the next one cheaper.

### 32.1 Why this order

**Phase 1 first because a live credential in your repository makes everything else pointless.** There is no sense hardening a client while a working key sits in git history. Phases 2 and 3 need Phase 1's foundations in place. Phase 4 is genuinely last, because it is the phase with the worst ratio of effort to risk reduction — which is also why it is the phase to cut if you are squeezed.

### 32.2 The phases

Ten weeks, four phases. Each phase delivers something testable on its own, so the programme survives being paused.

| Phase | Weeks | Scope | Why here |
|---|---|---|---|
| **1 — Foundations** | 1–3 *(estimate)* | Secret audit and rotation; CI secret injection and commit scanning; move tokens to Keystore/Keychain-backed storage; TLS configuration hardening; make the pinning decision (Chapter 8) | Highest risk removed per day spent. Nothing else matters while a credential is exposed |
| **2 — Verification** | 4–6 | Play Integrity and App Attest integrated **in report-only mode**; backend verdict verification; risk scoring; token binding | Moves the trust decision to your server. Report-only first is not caution, it is the documented rollout (Chapter 9.4) |
| **3 — Authentication** | 7–8 | Biometric authentication bound to a `CryptoObject` / Secure Enclave key for sensitive actions; step-up authentication; enrollment-change invalidation | Depends on Phase 1's key storage |
| **4 — Hardening** | 9–10 | Tamper and hook detection reporting to the backend; R8 obfuscation; release logging removal; screenshot protection | Lowest ratio of risk reduced to effort. Cut this first if squeezed |

### 32.3 Effort and maintenance

What to put in the plan, and what to say about how reliable these numbers are.

| Item | Estimate | Basis |
|---|---|---|
| Initial implementation | **18–26 engineering days** *(estimate)*, across Android, iOS and backend | Planning estimate for a team already shipping both platforms; scale to your own team's velocity |
| Ongoing maintenance | **~6 engineering days per year** *(estimate)* | Certificate and pin rotation, SDK updates, quota monitoring, verdict-distribution review |
| Assessment cadence | **~1 day per month** *(estimate)* | One MASWE weakness per week, per Chapter 23.6 |

**Be honest that these are estimates, not measurements.** They assume a team that already ships on both platforms and has a working CI. If you are also building the CI, or if this is your first attestation integration, the number goes up. Say that in the room rather than being asked about it in week seven.

**And note what the shrinking certificate lifetimes do to the maintenance line.** With maximum TLS certificate lifetimes reaching 47 days by 2029 (Chapter 8.5), the rotation component of that six days grows unless you automate it or pin an intermediate. Put that in the plan now.

### 32.4 Ownership

Name people, not roles. A plan with role names has no owner.

| Responsibility | Typically owned by |
|---|---|
| Android implementation | Android lead |
| iOS implementation | iOS lead |
| Backend verdict verification, risk scoring, token binding | Backend lead |
| CI secrets pipeline, signing key custody, runner hardening | DevOps / platform engineer |
| Certificate and pin rotation runbook | DevOps, with a named deputy |
| Data declarations and privacy review | Whoever owns compliance |
| Security review and sign-off | Engineering manager |

The two that go missing most often are **pin rotation** and **data declarations**. Both cause incidents when unowned, and both sit between teams, which is exactly why nobody picks them up.

### 32.5 Success criteria

Write these as things you can test, not things you can claim.

- **Zero** hardcoded secrets in source control, verified by a scanner that runs on every commit and blocks.
- **100%** of authentication tokens in Keystore or Keychain-backed storage, verified by inspecting app storage on a rooted device — not by code review.
- All payment and account-modification flows require attestation signals **and** biometric confirmation, verified by attempting the flow with each disabled.
- The pinning decision is **documented**, and if pinning is on: backup pins ship in every release, an expiration date is set with a calendar reminder, a rotation runbook has a named owner, and pin-validation failures raise an alert.
- Every security decision is validated server-side, verified by replaying a valid request from a second device (Chapter 12.3).
- A findings document exists from an assessment against the MAS-L1 or MAS-L2 profile, with retest dates.

Notice that each one names **how it is verified.** A success criterion you cannot test is a statement of intent.

### 32.6 This week

Five things you can do before anyone approves anything.

1. Run a secret scan across the repository and its history. Rotate anything live. This is hours, not days, and it is the highest-value thing on the list.
2. Run `strings` on your release artifact and read the output.
3. Get the compliance owner's name.
4. Book 40 minutes for a threat model on the next feature (Chapter 0.5).
5. Pick the pinning approach and write down the decision and the reasoning, even if the decision is "not yet."

None of that needs approval, and doing it gives you evidence for the conversation where you ask for the rest.

### 32.7 Questions you will be asked, and how to answer them

Taking a security proposal into a room means answering the same handful of objections. Most of them are reasonable. Here are straight answers.

**"Isn't StrongBox overkill?"**
It depends on your risk profile, and the honest answer differs by sector. For banking or health, hardware-backed key storage is frequently a compliance requirement rather than an engineering choice. For e-commerce, the TEE is generally sufficient. For a social or content app, standard Keystore or Keychain protection is fine. The decision belongs in Chapter 6.4's threat-model framing — and remember from Chapter 4.2 that StrongBox is not available on every device, so the real question is what your fallback does.

**"Should we block rooted devices?"**
Generally no, and Chapter 14.2 gives the full reasoning. A meaningful share of Android users run rooted devices or custom ROMs, often for entirely legitimate reasons, and a local block is trivially removed by the attacker you were worried about while reliably annoying the users you were not. Report the signal to your backend and apply a risk-based policy. Hard blocking is defensible only for the highest-security applications, and even then it is a business decision about lost customers, not a security win.

**"How do we handle certificate rotation?"**
Ship at least two pins — current and backup. Rotate the server side first, then update pins in a subsequent release. And answer the question in §8.5 before you ship anything: does your renewal reuse the key pair, or generate a new one? That single fact determines whether your pinning survives 2029.

**"Will attestation slow down the app?"**
Standard Play Integrity requests add a few hundred milliseconds on average after warm-up, which is why Chapter 9.2 recommends preparing the token provider ahead of time. Classic requests are slower and are meant for occasional high-value checks, not per-request use. On iOS, attestation contacts Apple but assertions are generated locally, so the recurring cost is small (Chapter 10.1).

**"Do we need all of this for an MVP?"**
No. The minimum that is genuinely irresponsible to skip: encrypted token storage, correct TLS configuration, secrets out of the repository with commit scanning, and server-side validation. That is Phase 1 in §32.2, and it is roughly three weeks. Attestation, biometrics and hardening are Phase 2 onward and can wait for real users.

**"What if we exceed the Play Integrity quota?"**
Request an increase through Play Console, and design attestation to trigger on high-value actions rather than every API call. Do this before launch rather than during it — and note from Chapter 9.2 that the published quota figures are practitioner-reported, so verify yours in Play Console rather than trusting a blog.

**"What about location privacy?"**
Collect the coarsest signal that answers your question — coarse location rather than precise, where that suffices. For fraud detection specifically, consider backend-side IP geolocation instead of device GPS: it is harder for a user to spoof casually, it needs no permission prompt, and it keeps you out of a privacy declaration you would otherwise have to make (Chapter 18).

**"Can't we just obfuscate it?"**
No, and Chapter 14 is the long answer. Obfuscation raises cost against opportunistic attackers and automated tooling. It does not protect a secret, because an obfuscated key is still a key. If the proposal on the table is obfuscation *instead of* server-side validation, it is not a security measure, it is a delay.

**"Our app isn't a target."**
Possibly true for a targeted adversary, and irrelevant to the other three in Chapter 1.3. Opportunists run automated scans across many apps looking for an exposed key or an unauthenticated endpoint; they do not need a reason to pick you. That is also the category most cheaply defended against, which makes this objection an argument for doing Phase 1 rather than for doing nothing.

---
