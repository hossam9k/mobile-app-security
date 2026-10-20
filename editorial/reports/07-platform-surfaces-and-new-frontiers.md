# book/07-platform-surfaces-and-new-frontiers.md

## Summary
- Words before / after: 14,983 / 15,051 (the small increase comes from two added source links, the XSS caveat in the §16.2 Trap, the Play extension note, and the UK GDPR cap)
- Edits: clarity 34, filler 16, voice 14, spelling 98 (60 British-to-American conversions, about 37 serial commas, plus "any more" changed to "anymore"), explanation 4, code 6 (comments only: "Belt and braces", "owns", "our" changed to "your" twice, "actually", "cancelled")
- Facts checked: 262 · correct 241 · corrected 14 · unverified 7
  - MAS identifiers: 125 MASTG test, best-practice, demo, app, and knowledge IDs. I read the front matter of each one from the OWASP/mastg repo on 2026-10-20. All exist, all titles match, and deprecation status is as stated: 0030, 0033, 0035, 0044, 0078, and 0087 are deprecated with the stated replacements; APP-0014 is deprecated; TEST-0255, 0256, and 0257 are still placeholders. I checked 31 MASWE IDs and titles against mas.owasp.org/MASWE (v1.0.0 numbering), confirmed 12 PLATFORM weaknesses (0029–0040) and 13 PRIVACY weaknesses (0066–0078), and confirmed that MASWE-0018 maps to PLATFORM-1 and MASWE-0063 to PLATFORM-2. I checked 9 MASVS control statements against the OWASP/masvs repo.
  - Vendor and other claims: about 97, covering Android behavior-change pages for 12, 14, 15, 16, and 17, WebSettings, WebViewClient, WebView, the JS bridge guide, App Links, Dynamic App Links, the Play target-SDK page, the photo picker, Play photo policy, AD_ID, data-access auditing, 16 KB pages, tapjacking, FileProvider, intent redirection, SQLiteQueryBuilder, Apple associated domains, privacy manifest, App Review 2.5.2, WebKit blogs, Apple docs JSON for API availability, WWDC26 sessions 241 and 347, NVD (both CVEs), FTC, Snyk, Microsoft (TikTok, Dirty Stream), the OWASP LLM 2026 coverage, Kotlin docs, cryptography-kotlin releases, and the Apple MIE blog.

## Corrections (factual)
| § | Old | New | Source | Checked |
|---|---|---|---|---|
| 16.2 (table) | `postWebMessage` / `WebMessagePort`: "An alternative, origin-aware" | "An alternative, not recommended. Google suggests it only for older WebView versions that lack `addWebMessageListener`" | https://developer.android.com/develop/ui/views/layout/webapps/native-api-access-jsbridge (comparison table marks it "Recommended: No") | 2026-10-20 |
| 16.2 Trap | Gave only Google's "generally rely upon" line | Adds that the same page warns origin rules don't protect against XSS in your own domain (both sides now shown) | same page | 2026-10-20 |
| 16.2 | App-Bound Domains: non-opted-in WebViews lose "cookie access" | "cookie manipulation" (WebKit's wording) | https://webkit.org/blog/10882/app-bound-domains/ | 2026-10-20 |
| 17.3 | "every row above is now enforced, not optional (Wear OS, Automotive, TV and XR apps have lower floors)" | Adds "Apps granted an extension have until 1 November 2026" | https://developer.android.com/google/play/requirements/target-sdk | 2026-10-20 |
| 17.8 | Play Console path "Protected with Play → Play Store protection → Manage Play app signing" | "Protected with Play → Play Store distribution → Go to Play app signing", **App signing key certificate** section, with a source link | https://support.google.com/googleplay/android-developer/answer/9842756 | 2026-10-20 |
| 17.8 | `setStrictColumns(true)` "on API 29+" | "on API 30+", with a reference link | https://developer.android.com/reference/android/database/sqlite/SQLiteQueryBuilder ("Added in API level 30") | 2026-10-20 |
| 18.1 (table) | Photo picker "built in from Android 11 and backported to Android 4.4+ through Google Play" | "ships with Android 11+ devices that receive Google System Updates and is backported to Android 4.4+ through Google Play services" | https://developer.android.com/training/data-storage/shared/photopicker | 2026-10-20 |
| 18.4 | "`MASWE-0069` and `MASTG-TEST-0318`/`0319` cover SDK APIs known to handle sensitive user data" | Tests 0318 and 0319 are filed under `MASWE-0073` (inadequate data collection declarations). MASWE-0069 is "Usage of Non-Privacy-Preserving Functionality" (pickers, auth sessions), not SDKs | OWASP/mastg `tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0318.md` and `0319.md` (`maswe: [MASWE-0073]`); OWASP/maswe `MASWE-0069.md`, `MASWE-0073.md` | 2026-10-20 |
| 18.5 | GDPR "(EU and UK variants)… fines… reach €20 million or 4%" | EU GDPR €20M or 4%; "the UK version caps them at £17.5 million or 4%" | ICO fining guidance, via search (nibusinessinfo.co.uk, bdo.co.uk) | 2026-10-20 |
| 19 intro | Android 14 `ZipFile`/`ZipInputStream` reject entries containing `..` | "containing `..` or starting with `/`" | https://developer.android.com/about/versions/14/behavior-changes-14 | 2026-10-20 |
| 19.6 | NDK r27 and older need "the linker flag `-Wl,-z,max-page-size=16384`" | "the linker flags `-Wl,-z,max-page-size=16384` and `-Wl,-z,common-page-size=16384`" | https://developer.android.com/guide/practices/page-sizes | 2026-10-20 |
| 20.1 | OWASP LLM Top 10 2026 "published in August 2026" | "published on 3 August 2026" | genai.owasp.org resource page (dated August 3, 2026); Imperva coverage | 2026-10-20 |
| 20.2 | ML Kit GenAI APIs: summarization, proofreading, rewriting, image description, Prompt API | Adds speech recognition | https://developer.android.com/ai/gemini-nano | 2026-10-20 |
| 20.4 | LLM06 moved up "because newer reasoning models make abuse more expensive" (unmarked) | "reportedly because reasoning models and agent loops make abuse more expensive *(reported)*". Help Net Security and Imperva give other reasons; only Aembit names reasoning models | helpnetsecurity.com 2026-08-06; imperva.com; aembit.io | 2026-10-20 |

## Unverified
| § | Claim | What I tried | Suggested marker |
|---|---|---|---|
| 20.1 | Full OWASP LLM 2026 ranking and the "Hidden Context Exposure" rename | The official genai.owasp.org page doesn't render the list. Four secondary sources agree on the order | Keep the existing *(reported: the ranking as given in OWASP's release coverage)* |
| 20.5 | 2026 edition says the safety check shouldn't be the same model that proposed the action | Found only in Aembit's coverage, not in Help Net Security or Imperva | Keep *(reported)* |
| 20.5 | LLM07 rose because incident data showed wrong answers driving decisions | Help Net Security supports it (incident record ranked it high). Official text not readable | Added "reportedly" |
| 20 intro | WWDC26 session 347 example: the agent "pays for something, posts private data publicly, or deletes content" | The transcript confirms the tea-ordering tool, public posting, and "deleting sensitive user data" as the calendar-injection example. Payment is implied by the order tool, not stated as the injection outcome | Acceptable as written; optional *(reported)* |
| 17.8 | `SQLiteQueryBuilder` passes caller columns containing ` AS ` without strict columns | Not in the reference docs. This is AOSP `computeSingleProjection` behavior | Reworded to "the platform's implementation"; consider *(reasoned)* |
| 16.4 In practice | "On iOS, nothing you configure pins `WKWebView` traffic" | The ATS/NSPinnedDomains docs don't say either way. The claim belongs to §8.6 | Owner of §8.6 should verify |
| 18.1 | Point-of-use permission requests get granted far more often | Already *(reported)*. No primary source | Keep *(reported)* |

## Explanations added
| § | What was missing | What I added |
|---|---|---|
| 16.1 | The same-origin policy and "the page" were tangled in one sentence | Split it: the browser's sandbox and the policy confine the page; then defined the policy |
| 16.2 Trap | Google's counter-caveat about XSS was missing, so the Trap read as one-sided | Added Google's own XSS warning, then the book's conclusion |
| 18.4 | Why the SDK tests sit under a declarations weakness | One clause: MASWE-0073 makes you responsible for what your SDKs collect |
| 17.3 | Readers might assume every Play app already targets API 36 | Added the extension window to 1 November 2026 |

## Needs a change in another file
| File | § | Change | Why |
|---|---|---|---|
| book/12-verification.md | Changelog | Add an entry: "2026-10-20 — Part 7: editorial and fact pass. MASWE-0069 → MASWE-0073 for SDK tests 0318/0319; setStrictColumns API 30; Play app-signing menu path; Play API 36 extension to 1 Nov 2026; ML Kit adds speech recognition; GDPR UK cap; 16 KB linker flags; postWebMessage not recommended; OWASP LLM06 rationale marked (reported)." | CONTRIBUTING step 2 |
| book/12-verification.md | Glossary | "Embedding" points to §20.1, but this chapter defines it in §20.2 | Wrong section reference |
| book/07 (frontmatter) | `recheck_because` | Still says "behaviour". I left it because the rules allow changing this field only when a fact changes | Spelling consistency; the coordinator may want a global fix |
| book/07 (headings) | 17.8 "Content provider: parameterised, always", 19.4 "Deserialisation", 19.8 "iOS deserialisation: allow-list…" | British spellings left in headings because heading text is frozen | Needs a coordinated global change if the book switches to American spelling in headings |
| book/03-data-in-transit.md | 8.6 | Verify that iOS ATS `NSPinnedDomains` doesn't apply to `WKWebView` | Claim repeated here in §16.4 |

## New glossary terms
| Term | Definition | Defined in § |
|---|---|---|
| Eval set | A fixed collection of test prompts with expected behavior, used to catch regressions in model behavior you treat as a control | §20.7 |
| Dirty Stream | Microsoft's 2024 name for path traversal through a file name returned by another app's content provider | Chapter 17 intro, §17.2 |
| Attribution tag | A label created with `createAttributionContext` so data-access audit callbacks report which feature made the access | §18.4 |
| `expect`/`actual` | KMP mechanism: common code declares an `expect`, and each platform source set supplies the `actual` | Chapter 21 intro |

## Judgment calls
- **Spelling.** I followed PROMPT.md and the updated CONTRIBUTING (American spelling, serial comma) in prose and code comments. Headings and the frontmatter keep the British forms.
- **§20 intro.** "Almost every mobile team is now shipping an AI feature, and many aren't threat modeling it" became "Many mobile teams now ship an AI feature, and not all of them threat model it." The original was an unsourced universal claim.
- **§21 intro.** "Published security guidance… is close to nonexistent, which makes this chapter unusually useful" became "…is scarce, so this chapter works from the platform mechanisms up *(reasoned)*." I removed the self-promotion and marked the claim.
- **Idioms replaced with literal statements.** "feed it a lie", "carry the weight", "caught many people out", "costume", "wearing different clothes", "nod at", "Belt and braces", "owns your app", "data-flow and cost story". The "doors" framing in the Part intro stays because it's the part's organizing image, but Chapter 17 now says "entry point" instead of extending the lock-and-door metaphor.
- **§17.8.** The comment "our own selection" became "your own selection", and "our own database" became "your own database" (no "we" or "our" voice).
- **Unchanged dates.** I kept `last_verified` at 2026-10-20 because Pass 3 covered the whole file.
- **Structure.** No section numbers, headings, figure numbers, Mermaid structure, callout labels, or confidence markers were changed. Only one Mermaid label changed: "the real authorisation" became "authorization" through the spelling pass. `python3 scripts/check.py` passes.
