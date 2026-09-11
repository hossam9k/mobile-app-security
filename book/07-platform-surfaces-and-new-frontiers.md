---
part: 07
last_verified: 2026-09-11
volatility: medium
recheck_because: "API deprecations at each OS release"
---

# Part 7: Platform surfaces and new frontiers

This part covers the components where most real findings live: WebViews, IPC and deep links, permissions. Plus secure coding, and the two newest surfaces: AI features and Kotlin Multiplatform.

---

## Chapter 16: WebViews — the most under-secured component in mobile

A **WebView** is a browser engine embedded in your app. It's convenient: you reuse web content, ship changes without a release, and support both platforms with one implementation.

It is also, consistently, the weakest part of most mobile apps. The reason is structural rather than accidental: a WebView takes untrusted content from the internet and runs it *inside your app's security context*. Everything your app can do, that content is one mistake away from doing.

`MASVS-PLATFORM-2` covers WebViews, and eight MASWE weaknesses relate to them. That ratio tells you something.

### 16.1 Why a WebView is different from a browser

When Chrome loads a hostile page, the page is confined by the browser's sandbox and the same-origin policy. It can't read your files or call your code.

When *your WebView* loads a hostile page, the page sits inside an app that has your permissions, your storage, your session tokens and, if you added one, a bridge into your native code. The confinement you're relying on is whatever you configured, and the defaults are convenient rather than safe.

### 16.2 The JavaScript bridge, and why it's the sharpest edge

A **JavaScript bridge** lets web content call native functions. On Android that's `addJavascriptInterface`; on iOS it's `WKScriptMessageHandler`.

Consider what you've built when you add one. Any JavaScript running in that WebView can now call your native method. If the WebView ever loads content you don't fully control — a third-party page, a URL from a deep link, an ad, a page that includes a compromised script — that content calls your native code.

`MASWE-0033` is "sensitive native functionality exposed in WebViews," and `MASTG-TEST-0033` and `0334` test for it on Android, `MASTG-TEST-0078` and `0376` on iOS.

**How to do it safely, if you must:**

Expose the **narrowest possible surface**. Not a general `invoke(methodName, args)` gateway — one function that does one thing, validating its inputs. Every parameter arriving from JavaScript is untrusted input, exactly like a network response.

Never expose anything that reads files, returns credentials, or performs a privileged action without independent authorisation. "The web page will only call this correctly" is not a security property.

On iOS, prefer **`WKScriptMessageHandlerWithReply`** for returning data to JavaScript rather than calling `evaluateJavaScript` — `MASTG-BEST-0062`. And use **`WKContentWorld` isolation** when you inject scripts for DOM inspection, so page JavaScript can't see or interfere with your script (`MASTG-BEST-0061`, tested by `MASTG-TEST-0379`).

Prefer **origin-scoped messaging** over legacy bridges (`MASTG-BEST-0035`).

### 16.3 File access: the setting nobody remembers changing

WebViews can be configured to read local files, and on Android they historically could read content providers too. Combine that with a page that can be influenced by an attacker and you have local file exfiltration from inside your own app.

The relevant settings on Android are `setAllowFileAccess`, `setAllowFileAccessFromFileURLs`, `setAllowUniversalAccessFromFileURLs` and `setAllowContentAccess`. Turn off what you don't need. `MASWE-0034` covers this; `MASTG-TEST-0250` through `0253` test both the static configuration and the runtime behaviour.

On iOS, watch for relaxed file origin policies (`MASTG-TEST-0335` and `0336`) and overly broad file read access, `MASTG-TEST-0333`.

If you need to load local content, do it properly: `MASTG-BEST-0011` and `0033` describe securely loading file content in a WebView. On Android that generally means a content-URI–based loader rather than `file://` with universal access.

### 16.4 Loading untrusted content

`MASWE-0035` is "WebViews loading untrusted content," and the failure usually arrives through a chain: a deep link carries a URL parameter, your code passes it to `loadUrl`, and now an attacker chooses what runs in your WebView.

**Validate any URL before loading it**, against an allowlist of hosts you control — not a blocklist, and not a `contains("mydomain.com")` check, which `https://evil.com/?x=mydomain.com` passes.

**Handle navigation.** Intercept it (`shouldOverrideUrlLoading` on Android, `WKNavigationDelegate` on iOS) and decide whether each navigation is permitted, rather than letting the page take your WebView anywhere. `MASTG-TEST-0398` and `0400` cover this.

**Never ignore TLS errors.** `onReceivedSslError` calling `proceed()` disables certificate validation for that WebView entirely. It gets added to silence a development warning and it survives to production because nothing visibly breaks. `MASTG-TEST-0284`, `MASTG-DEMO-0056`. On iOS the equivalent is a `WKNavigationDelegate` that accepts any server certificate — `MASTG-TEST-0397`, `MASTG-DEMO-0155`. If you take one thing from this chapter, take this one.

**Disable JavaScript when you don't need it** (`MASTG-BEST-0012`), and content provider access on Android (`MASTG-BEST-0013`).

### 16.5 Sensitive UI inside a WebView

If you render a password field in a WebView, the value lives in the page DOM, where any injected script can read it, and where your app's own `evaluateJavaScript` calls might write it (`MASTG-TEST-0378`, `0380`).

The guidance is direct: **render sensitive UI as native views over the WebView** (`MASTG-BEST-0059`) and **use native views for sensitive text entry** (`MASTG-BEST-0060`). This is also, not coincidentally, why RFC 8252 tells you to run OAuth in the system browser rather than a WebView.

### 16.6 Cleanup and hygiene

WebViews keep cookies, local storage, caches and session data. On logout, clear them — `MASTG-BEST-0028`, `MASTG-TEST-0320`, `MASTG-DEMO-0082`. This is part of the `MASWE-0024` problem from Chapter 0.3.

Disable WebView debugging in release builds (`MASTG-BEST-0008`). A debuggable WebView lets anyone with the device inspect your page and call your bridge from a console.

On iOS, migrate off **`UIWebView`** if you still have it. It's deprecated and less secure than `WKWebView`, which runs content out-of-process. `MASTG-BEST-0032`, `MASTG-TEST-0331`.

### 16.7 A short checklist you can hold in your head

Does this WebView load only content I control? Does it have a bridge, and if so is the surface minimal and validated? Is file access off? Is JavaScript needed? Do I intercept navigation? Do I ever proceed past a TLS error? Is sensitive input native rather than in the page? Do I clear state on logout? Is debugging off in release?

If you can answer those nine questions about every WebView in your app, you're ahead of most teams.

---

### 16.8 How to implement it

#### Android: a WebView configured defensively

```kotlin
webView.settings.apply {
    javaScriptEnabled = false          // turn on only if the page needs it
    allowFileAccess = false            // §16.3
    allowContentAccess = false
    @Suppress("DEPRECATION")
    allowFileAccessFromFileURLs = false
    @Suppress("DEPRECATION")
    allowUniversalAccessFromFileURLs = false
    domStorageEnabled = false          // on only if needed
}

if (!BuildConfig.DEBUG) {
    WebView.setWebContentsDebuggingEnabled(false)   // MASTG-BEST-0008
}
```

Allowlist navigation, and never proceed past a TLS error:

```kotlin
webView.webViewClient = object : WebViewClient() {

    private val allowedHosts = setOf("app.example.com", "help.example.com")

    override fun shouldOverrideUrlLoading(
        view: WebView, request: WebResourceRequest
    ): Boolean {
        val host = request.url.host
        // Exact host match. NOT `host.contains("example.com")`, which
        // https://evil.com/?x=example.com would pass.
        return if (host != null && host in allowedHosts) {
            false                      // we handle it: let the WebView load it
        } else {
            true                       // blocked; optionally open in the system browser
        }
    }

    override fun onReceivedSslError(
        view: WebView, handler: SslErrorHandler, error: SslError
    ) {
        handler.cancel()               // NEVER handler.proceed(). See §16.4.
    }
}
```

If you need a bridge, make the surface narrow and validate every argument:

```kotlin
class NarrowBridge(private val onRedeem: (String) -> Unit) {
    @JavascriptInterface
    fun redeemVoucher(code: String) {
        // Untrusted input, exactly like a network response.
        if (!code.matches(Regex("^[A-Z0-9]{8}$"))) return
        onRedeem(code)                 // server authorises; the bridge does not
    }
}
webView.addJavascriptInterface(NarrowBridge(::redeem), "AppBridge")
```

**The wrong version:**

```kotlin
// DON'T: a general gateway into native code. Any script in the WebView owns your app.
@JavascriptInterface
fun invoke(method: String, args: String): String = reflectivelyCall(method, args)
```

#### iOS: WKWebView with reply-based messaging

```swift
let config = WKWebViewConfiguration()
config.defaultWebpagePreferences.allowsContentJavaScript = false   // enable only if needed

// Reply-based handler, per MASTG-BEST-0062 — avoids evaluateJavaScript round-trips
config.userContentController.addScriptMessageHandler(
    self, contentWorld: .defaultClient, name: "appBridge"          // isolated world
)

let webView = WKWebView(frame: .zero, configuration: config)
webView.navigationDelegate = self
```

```swift
extension MyController: WKNavigationDelegate {
    func webView(_ webView: WKWebView,
                 didReceive challenge: URLAuthenticationChallenge,
                 completionHandler: @escaping (URLSession.AuthChallengeDisposition,
                                               URLCredential?) -> Void) {
        // Do not accept arbitrary server trust here — MASTG-TEST-0397.
        completionHandler(.performDefaultHandling, nil)
    }

    func webView(_ webView: WKWebView,
                 decidePolicyFor navigationAction: WKNavigationAction,
                 decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        let allowed = ["app.example.com", "help.example.com"]
        guard let host = navigationAction.request.url?.host, allowed.contains(host) else {
            decisionHandler(.cancel)
            return
        }
        decisionHandler(.allow)
    }
}
```

And on logout, clear the state (§16.6):

```swift
let store = WKWebsiteDataStore.default()
store.removeData(ofTypes: WKWebsiteDataStore.allWebsiteDataTypes(),
                 modifiedSince: .distantPast) { }
```

---


#### Verify it

```
# Is WebView debugging still enabled in release?
adb shell am start -a android.intent.action.VIEW -d "chrome://inspect"
```

With the release build running, `chrome://inspect` on a connected machine should show **no inspectable WebView**. If it does, `setWebContentsDebuggingEnabled(false)` is not taking effect and anyone with the device can call your bridge from a console.

**Test the allowlist with a hostile URL.** Send the app a deep link carrying `https://evil.example.com/?x=app.example.com` and confirm the WebView refuses it. A `contains()` check passes this and an exact-host check rejects it — which is the difference §16.4 is about.

**Test the TLS error path.** Point the WebView at a host with an invalid certificate. **Pass:** the load fails. **Fail:** the page renders, meaning something calls `proceed()`.

**Confirm bridge scope.** In a debug build, from the WebView console: `Object.keys(AppBridge)`. What comes back is your entire native attack surface. If it lists more than you intended, narrow it.

Relevant tests: `MASTG-TEST-0284`, `0031`, `0033`, `0334`.

## Chapter 17: IPC, deep links and app components

**IPC**, or inter-process communication, is how apps talk to each other and to the system. It's genuinely useful and it's a door into your app, which means every door needs a lock and a check on who's knocking.

`MASVS-PLATFORM-1` covers this, and twelve MASWE weaknesses live here.

### 17.1 Android app components, and the word "exported"

Android apps are built from four component types: **activities** (screens), **services** (background work), **broadcast receivers** (event listeners) and **content providers** (data interfaces).

Each is either **exported**, meaning other apps can start or query it, or not. This single attribute decides whether a component is internal plumbing or public API.

The rule: **export nothing you don't need to.** Declare `android:exported="false"` explicitly. Since Android 12 you must declare it explicitly when you have an intent filter, which was a welcome change because the old implicit default caught many people out.

When you *do* export something, protect it: require a permission, verify the caller, and validate every input as untrusted. `MASTG-TEST-0364`, `0365` and `0366` test for exported and unprotected activities, services and receivers respectively; `MASTG-BEST-0052` describes restricting access.

The failure looks like this: an activity that displays account details, exported because it needed a deep link, launched directly by a malicious app, skipping your login screen. Or an exported service that performs a transfer, invoked by any app on the device. `MASWE-0018` — "lack of authentication or authorization on app components."

### 17.2 Intents: explicit versus implicit

An **explicit intent** names its destination component. An **implicit intent** describes an action and lets the system choose who handles it.

Implicit intents are the risk. For internal communication, always use explicit intents (`MASTG-BEST-0056`), because an implicit intent for internal work can be intercepted by another app that registered for the same action — `MASTG-TEST-0372`, `MASTG-DEMO-0136`, `MASTG-DEMO-0140`.

Two related failures. **Sensitive data in implicit intent extras** (`MASTG-TEST-0374`, `MASTG-DEMO-0138`): whatever you attached is now readable by whichever app received it. And **not validating what comes back** (`MASTG-TEST-0375`): if you fire an implicit intent to pick a file and a malicious app returns a crafted path, you now read a file of the attacker's choosing (`MASTG-DEMO-0139`, `MASTG-DEMO-0141`).

`MASTG-BEST-0057`, sanitize data coming from external components, is the general fix. Treat every intent extra like a query parameter from the internet.

### 17.3 PendingIntent: the one that looks harmless

A **`PendingIntent`** wraps an intent and hands another app the right to fire it **as you**, with your identity and permissions.

If you create a mutable `PendingIntent` with an implicit base intent, the receiving app can fill in the blanks, changing the destination, the action or the data, and the resulting call executes with your app's privileges.

**Always use immutable `PendingIntent`s with explicit intents.** `FLAG_IMMUTABLE` exists for this, `MASTG-BEST-0063` says it, and `MASTG-TEST-0030` and `0381` test for it.

### 17.4 Content providers

A **content provider** exposes structured data through a URI interface, usually backed by a database. Two failure modes.

**SQL injection.** If you build a query by concatenating a caller-supplied selection string, a caller controls your SQL. Use parameterised queries — `MASTG-BEST-0039`, `MASTG-TEST-0339`, `MASTG-DEMO-0102`.

**Path traversal via `FileProvider`.** `FileProvider` shares files by granting URI permissions. Configure the shared paths too broadly and a caller can request a URI outside the intended directory, exfiltrating private files. `MASTG-DEMO-0122` and `0123` demonstrate both the oversharing configuration and the exfiltration. Scope your `file_paths.xml` to the narrowest directory that works, and validate requested filenames.

### 17.5 Deep links, and the verification that makes them safe

A **deep link** opens your app at a specific screen from a URL. There are two kinds and the difference is the whole security story.

A **custom URI scheme** (`myapp://profile/123`) can be registered by **any** app. Multiple apps can claim the same scheme, and which one wins is not defined. So a malicious app can register your scheme and intercept links intended for you — which, as Chapter 0.3 noted, is the code interception attack against OAuth.

A **verified https link**, called **App Links** on Android and **Universal Links** on iOS, is cryptographically tied to a domain you control. Android uses `android:autoVerify="true"` plus a Digital Asset Links file hosted on your domain; iOS uses an `apple-app-site-association` file. The OS fetches that file and confirms your app is authorised. No other app can claim your verified link.

**Use verified https links.** `MASTG-BEST-0070` covers `autoVerify` and Digital Asset Links; `MASTG-TEST-0393` tests for unverified App Links; `MASWE-0029` is "insecure deep links."

**Then validate the contents anyway.** A verified link proves the *link* came to the right app; it says nothing about the *parameters*. Every deep link parameter is attacker-supplied — someone can send your user a crafted link. So:

Validate every parameter (`MASTG-BEST-0071`, `0072`; `MASTG-TEST-0394`, `0395`, `0370`).

Never let a deep link parameter become a URL you load in a WebView without allowlisting (Chapter 16.4).

Never let a deep link bypass authentication. If `myapp://transfer?to=X&amount=Y` works while logged in, an attacker sends that link and the user taps it. Sensitive actions require confirmation and step-up authentication regardless of how the screen was reached.

On iOS, also validate the **source application** where the API allows (`MASTG-BEST-0055`, `MASTG-TEST-0371`).

### 17.6 The other channels people forget

**The clipboard.** Shared across apps. On iOS the general pasteboard has historically synced across a user's devices. Don't copy secrets to it; if you must, restrict to the local device, set an expiry, and clear after use. `MASWE-0030`, `MASTG-TEST-0276` through `0280`.

**App extensions and App Groups (iOS).** Extensions run in separate processes and share data with your app through App Groups. Data in a shared container is readable by every member. `MASWE-0031`, `MASTG-TEST-0388`, `MASTG-BEST-0068`.

**Accessibility services.** A malicious accessibility service can read your screen content and inject events. You can't fully prevent this, but you can avoid putting secrets in accessible text where it isn't needed. `MASWE-0040`.

**Overlay attacks.** Another app draws over yours, so the user thinks they're tapping your button and they're tapping something else — tapjacking. Protect sensitive screens with `setHideOverlayWindows` or `filterTouchesWhenObscured`. `MASWE-0039`, `MASTG-BEST-0040`, `MASTG-TEST-0035`, `MASTG-DEMO-0103`.

**Notifications.** Lock-screen notifications are visible without unlocking. A notification containing a one-time code defeats the code. `MASWE-0037`, `MASTG-BEST-0027`.

**Custom keyboards (iOS).** A third-party keyboard with full access sees what users type. For sensitive fields, keep input on the system keyboard (`MASTG-BEST-0069`) or restrict custom keyboards app-wide (`MASTG-TEST-0389`).

### 17.7 The pattern behind all of it

Every item in this chapter is the same idea in a different costume: **a channel exists, another app can use it, and your code trusted what came through.**

So the question to ask of any component, link or share point is: *if a hostile app on this device used this, what could it do?* Answer that for each door and you've covered the category.

---

### 17.8 How to implement it

#### Components: closed by default

```xml
<!-- AndroidManifest.xml -->
<activity android:name=".InternalActivity" android:exported="false" />

<!-- Exported because it handles a deep link — so it must verify state itself -->
<activity android:name=".TransferActivity" android:exported="true">
    <intent-filter android:autoVerify="true">      <!-- App Links, §17.5 -->
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="https" android:host="app.example.com" />
    </intent-filter>
</activity>
```

The Digital Asset Links file that makes `autoVerify` real, served at `https://app.example.com/.well-known/assetlinks.json`:

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.app",
    "sha256_cert_fingerprints": ["AA:BB:CC:..."]
  }
}]
```

Then treat the link's contents as hostile anyway:

```kotlin
// TransferActivity.onCreate
val amount = intent.data?.getQueryParameter("amount")?.toLongOrNull()
val payee  = intent.data?.getQueryParameter("to")

// A verified link proves it reached the right app. It proves nothing about who sent it.
if (amount == null || amount <= 0 || payee == null || !isKnownPayee(payee)) {
    finish(); return
}
if (!session.isAuthenticated) { routeToLogin(); return }

// Never auto-execute. Confirm, then step up (Chapter 11).
showConfirmation(amount, payee, onConfirm = { requireBiometricThenTransfer(amount, payee) })
```

#### PendingIntent: immutable, explicit

```kotlin
val intent = Intent(context, ResultReceiverActivity::class.java)   // explicit
val pendingIntent = PendingIntent.getActivity(
    context, 0, intent,
    PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT   // §17.3
)
```

`FLAG_MUTABLE` with an implicit base intent is the combination to avoid — it lets the recipient redirect the call and have it execute with your identity.

#### Content provider: parameterised, always

```kotlin
// Safe: the selection is a fixed string; values are bound separately.
override fun query(
    uri: Uri, projection: Array<String>?, selection: String?,
    selectionArgs: Array<String>?, sortOrder: String?
): Cursor = db.query(
    "orders",
    projection,
    "user_id = ?",                       // our own selection, not the caller's
    arrayOf(currentUserId),              // bound value
    null, null, sortOrder
)
```

**The wrong version:**

```kotlin
// DON'T: the caller controls your SQL. MASTG-TEST-0339.
db.rawQuery("SELECT * FROM orders WHERE $selection", null)
```

---


#### Verify it

Exported components are testable from the shell, which is exactly how an attacker enumerates them.

```
# What is exported?
aapt dump xmltree app-release.apk AndroidManifest.xml | grep -B4 "exported.*true"

# Can a component be launched directly, skipping your login flow?
adb shell am start -n com.example.app/.TransferActivity \
  -a android.intent.action.VIEW -d "https://app.example.com/transfer?to=x&amount=1"
```

**Pass:** the activity either refuses to start or lands on your login screen. **Fail:** you reach the transfer screen with an authenticated session absent, which is `MASWE-0018`.

**Verify App Links are actually verified**, not merely declared:

```
adb shell pm get-app-links com.example.app
```

**Pass:** the domain shows `verified`. **Fail:** `legacy_failure` or `none`, which means your `assetlinks.json` is missing, malformed, or served from the wrong path — and your links can be claimed by another app.

**Probe the content provider:**

```
adb shell content query --uri content://com.example.app.provider/orders \
  --where "1=1 OR id=1"
```

**Pass:** permission denied, or only the calling user's rows. **Fail:** other users' data, which is `MASTG-TEST-0339`.

## Chapter 18: Permissions and privacy

Privacy joined MASVS as a full category in v2.1.0, with four controls and thirteen weaknesses. It arrived because regulation arrived, and because "we collect this because it was easy" stopped being acceptable.

This chapter is short and practical. Most of it is about asking for less.

### 18.1 Permissions: ask for less, later, and explain why

Five habits. The theme running through all of them is asking for less.

**Request only what the feature needs** (`MASVS-PRIVACY-1`, `MASWE-0066`). Every permission is attack surface, a privacy commitment, and a conversion cost — users decline, and some uninstall.

**Check the merged manifest, not just yours.** Third-party SDKs declare their own permissions, and those merge into your app. An analytics library that quietly adds location access has made a privacy declaration on your behalf. `MASTG-TEST-0254` looks for dangerous permissions; `0255` for permissions that aren't minimised.

**Request at the point of use, with a rationale.** Asking for camera access when the user taps "take photo" gets granted far more often than asking at first launch, and it's honest. `MASTG-TEST-0256` tests for a missing rationale.

**Handle denial gracefully.** A feature that breaks or nags when a permission is declined is a bug. Users may also revoke later, and Android auto-resets unused permissions (`MASTG-TEST-0257`).

**On iOS, minimise entitlements too** (`MASTG-BEST-0051`, `MASTG-TEST-0362`) and write accurate purpose strings — the text users see when you ask. A vague or wrong purpose string is both an App Review problem and a `MASTG-TEST-0360` finding.

### 18.2 Identifiers and tracking

`MASWE-0068` is "incorrect use of identifiers for user tracking," and the substance is: **use the right identifier for the job, and the most privacy-preserving one that works.**

Use a **resettable, purpose-scoped** identifier where you can — Android's advertising ID or app set ID, iOS's `identifierForVendor`. Don't use hardware identifiers to build a persistent profile the user can't reset, and don't attempt to fingerprint a device to defeat the reset the platform gave them. Both platforms treat that as a policy violation, not just a privacy concern.

Where you don't need identity, **anonymise or pseudonymise** (`MASWE-0067`). Aggregate counts rather than per-user events. Truncate what you don't need at full precision — coarse location rather than exact coordinates, if coarse answers your question.

### 18.3 Transparency and control

`MASVS-PRIVACY-3` asks you to be transparent about collection and use; `MASVS-PRIVACY-4` asks you to give users control.

Practically: your **store data declaration** must match what your app actually does (`MASWE-0073`), including what your SDKs do. Your **tracking domain declarations** must be complete (`MASWE-0074`). Your privacy policy must be accurate and reachable (`MASWE-0072`). Consent must be unambiguous and not pre-checked (`MASWE-0078`, `MASWE-0071`), and users need a real way to see and delete their data (`MASWE-0076`, `MASWE-0077`).

The engineering consequence people miss: **you can't declare accurately unless you know what leaves the device.** `MASTG-TEST-0206` is "undeclared PII in network traffic capture," and `MASTG-DEMO-0009` shows how to detect it. Run that on your own app and compare what you see against your declaration. Teams are routinely surprised, usually by an SDK.

### 18.4 Third-party SDKs are your responsibility

An analytics, ads, crash or attribution SDK runs inside your app with your permissions, and its network calls are your data flows. `MASWE-0069` and `MASTG-TEST-0318`/`0319` cover SDK APIs known to handle sensitive user data.

Before adding one, ask: what does it collect, where does it send it, can I configure it down, and does my declaration cover it? After adding one, capture its traffic and confirm the answers. `MASTG-DEMO-0081` demonstrates sensitive user data reaching an analytics SDK, caught with Frida.

#### Catching an SDK in the act

Chapter 18.4 says to verify what your SDKs collect. On Android 11 and later there is a way to have the OS tell you, which is more reliable than reading documentation:

```kotlin
// Application.onCreate, debug builds
val appOps = getSystemService(AppOpsManager::class.java)
appOps.setOnOpNotedCallback(mainExecutor, object : AppOpsManager.OnOpNotedCallback() {
    override fun onNoted(op: SyncNotedAppOp) {
        Log.d("DataAudit", "sensitive access: ${op.op} from ${Thread.currentThread().stackTrace.joinToString()}")
    }
    override fun onSelfNoted(op: SyncNotedAppOp) = onNoted(op)
    override fun onAsyncNoted(op: AsyncNotedAppOp) {
        Log.d("DataAudit", "async sensitive access: ${op.op} — ${op.message}")
    }
})
```

Every access to a permission-guarded resource is now logged with a stack trace. Run your app through its flows and read the output: you will find out which SDK reads location, which reads the clipboard, and when. That output is also what makes your store data declaration accurate rather than aspirational (Chapter 18.3).

Pair it with `MASTG-TEST-0206` — capture your own network traffic and compare what leaves the device against what you declared.

### 18.5 The regulatory frame, briefly

You don't need to be a lawyer, but you should know the shape:

**GDPR** (EU) and similar laws require a lawful basis for processing, data minimisation, purpose limitation, user rights of access and deletion, and breach notification. Fines reach a percentage of global revenue.

**Store policies** are enforced faster than laws. Both Apple and Google will reject or remove an app whose data declarations don't match its behaviour — and that lands on you in days, not years.

**Sector rules** — HIPAA for health data in the US, PCI-DSS for payment card data, plus local banking regulation — add specific technical requirements. If you work in one of these, someone in your organisation owns those requirements; find them before you design, not after.

The practical takeaway: collect less, declare accurately, verify what actually leaves the device, and talk to whoever owns compliance *before* you ship a feature that changes any of it.

---

## Chapter 19: Input validation and unsafe handling

`MASVS-CODE-4` asks you to validate and sanitize all untrusted inputs. That sentence is easy to nod at and hard to apply, because the difficult part is recognising what counts as untrusted.

### 19.1 What "untrusted input" actually includes

Everything on this list is attacker-controllable, and each one is a real finding class:

Network responses — **including from your own backend**, which could be compromised or proxied. Deep link and URL parameters. Intent extras and IPC payloads. Content read through a content provider. Files the user picks or another app hands you. QR codes and NFC tags. Clipboard contents. WebView messages. Push notification payloads. Model output from an LLM (Chapter 20). And user-typed text, which is the one everybody remembers.

If you only validate the last item, you've validated the least likely attack.

### 19.2 Validate positively, at the boundary

Four habits that turn validation from a chore into something that actually holds.

**Allowlist, don't blocklist.** Define what's acceptable and reject everything else. Blocklists fail because you have to think of every bad case and the attacker only has to find one you missed.

**Validate at the trust boundary**, as soon as data enters — not deep inside business logic where three call sites bypass the check.

**Validate type, range, length, format and meaning.** A quantity should be a positive integer within a sane bound. A file path should resolve inside the directory you expect. A URL should have a host on your allowlist.

**Fail closed.** When validation fails, reject; don't proceed with a "sensible default."

### 19.3 Injection: the shape of the bug

Injection has a reputation for being many different bugs. It is really one bug wearing different clothes, which is good news, because one fix generalises.

**Injection** happens when data gets interpreted as code or as a command. Same shape everywhere: you built a string, and part of the string came from an attacker.

**SQL injection** — build a query with concatenation and the input changes the query. Fix: parameterised queries, always. Room's `@Query` with bound parameters is safe; string concatenation in a raw query is not. `MASTG-TEST-0339`.

**Path traversal** — a filename containing `../` escapes the directory you meant. Fix: canonicalise the path and confirm it's still inside your intended directory before opening it.

**Command injection** — passing input into a shell. Fix: don't invoke shells with user data; if you must, use argument arrays rather than a command string.

**Cross-site scripting in WebViews** — input rendered into HTML executes as JavaScript. Fix: escape on output, and see Chapter 16.

**Log injection** — input containing newlines forges log entries. Fix: sanitise before logging, and don't log user content you don't need.

The generalisation worth internalising: **separate code from data.** Every injection fix is a version of that. Parameterised queries separate SQL from values. Argument arrays separate the command from its arguments. Escaping separates markup from text.

### 19.4 Deserialization

This one is less famous than injection and can be more severe, because it can hand an attacker code execution rather than data.

**Deserialization** turns bytes back into objects. If those bytes are attacker-controlled, deserialization can construct objects you never intended and, with the right classes present, execute code.

`MASWE-0050` covers unsafe handling of untrusted data; `MASTG-TEST-0337` and `0386` test for untrusted deserialization on Android and iOS; `MASTG-BEST-0064` says use safe APIs.

Practically: prefer explicit, schema-driven formats such as JSON parsed into declared data classes, or Protobuf, over Java `Serializable` or `NSKeyedUnarchiver` on arbitrary input. On iOS, use `NSSecureCoding` with an explicit allowed-class list. Never deserialize data that arrived from an intent, a deep link or a file picker without constraining the types.

### 19.5 Dynamic code loading

`MASWE-0049` — unsafe dynamic code loading. Loading code at runtime from anywhere other than your signed app package means your app now runs code the OS never verified, and your signature covers nothing.

Both stores restrict this, and the security reasoning is straightforward: it defeats code signing, which is one of the platform guarantees from Chapter 0.4. If you're loading a DEX file, a dynamic library or a script from the network, that's a design to revisit.

### 19.6 Free compiler protections, and platform currency

`MASWE-0045` is "compiler-provided security features not used," and the fix is usually flipping a build setting. **Position-independent code** and **stack canaries** for native code (`MASTG-TEST-0222`, `0223`, `0228`, `0229`), **ARC** on iOS (`MASTG-TEST-0230`). These cost nothing and blunt whole classes of memory-corruption exploitation. You may see the older `MASTG-TEST-0044` and `MASTG-TEST-0087` ("Make Sure That Free Security Features Are Activated") cited for this — **both are deprecated v1 tests**, superseded by the atomic v2 tests above. The title is a hint about how often these protections aren't switched on.

Related, and easy to defer forever: **keep your platform floor current.** `MASWE-0041` and `0042` cover running on and targeting recent platform versions, and `MASTG-BEST-0010` covers `minSdkVersion`. Old API levels reopen attack classes the platform already closed — and an old `minSdkVersion` means your security code has to handle devices where the modern primitive doesn't exist.

And keep the **update path** working: `MASWE-0043` and `MASVS-CODE-2` ask for a mechanism to enforce updates. When you ship a security fix, you need users to actually receive it — which, as Chapter 8 noted, is the one real advantage mobile has over the web.

### 19.7 Dependencies

`MASVS-CODE-3` says use only components without known vulnerabilities. `MASWE-0044` names the failure. Chapter 15 covers the pipeline side, including locking, SBOM generation and scanning, and `MASTG-TEST-0272` through `0275` test it on both platforms.

The mobile-specific point: your dependency tree is larger than you think, most of it is transitive, and any one library can bring permissions, network calls and privacy obligations with it. Read the merged manifest occasionally.

---


### 19.8 How to implement it

#### Path traversal: canonicalise, then confirm containment

```kotlin
fun openInAppStorage(base: File, userSuppliedName: String): File {
    val target = File(base, userSuppliedName).canonicalFile   // resolves "../"
    // The check that matters: is it still inside where we meant?
    require(target.path.startsWith(base.canonicalFile.path + File.separator)) {
        "path escapes base directory"
    }
    return target
}
```

#### iOS deserialization: allow-list the classes

```swift
// Safe: only the types you expect can be constructed.
let unarchiver = try NSKeyedUnarchiver(forReadingFrom: data)
unarchiver.requiresSecureCoding = true
let order = unarchiver.decodeObject(of: [Order.self, NSString.self], forKey: "order")
```

```swift
// DON'T: constructs whatever the data asks for. MASTG-TEST-0386.
let order = NSKeyedUnarchiver.unarchiveObject(with: data)
```

#### Server-side is where validation counts

A reminder from Chapter 12, because client validation is a usability feature and server validation is the control:

```kotlin
// Client: reject obvious nonsense early, for the user's benefit.
if (amount <= 0 || amount > dailyLimitShownInUi) return showError()

// Server: re-derive everything. The client's numbers are a request, not a fact.
//   - is `payee` actually linked to this account?
//   - is `amount` within THIS user's real limit, read from our own database?
//   - does the balance cover it, checked transactionally?
//   - has an identical request arrived in the last 30 seconds? (replay)
```

---


#### Verify it

Validation is best tested with input you would not think to write.

**Path traversal.** Feed your file handler `../../../../data/data/com.example.app/shared_prefs/prefs.xml` and confirm it is rejected rather than resolved. A canonicalisation check passes this; string matching on `..` does not, because encodings differ.

**Injection.** Feed your content provider and any raw query path `' OR '1'='1` and a value containing a semicolon. **Pass:** parameterised queries treat them as literal data.

**Deserialization.** Hand your unarchiver a payload declaring a class you never expected. **Pass:** rejection, because `requiresSecureCoding` and an explicit allowed-class list are set.

**And check the server, not the client.** Take a valid request, change the price or quantity in a proxy, and replay it. **Pass:** the server rejects it. **Fail:** you have found the most consequential bug class in this book, and no client-side validation would have prevented it.

## Chapter 20: Securing AI features in mobile apps

Almost every mobile team is now shipping an AI feature, and almost none are threat modelling it. Published guidance is thin, which makes this both a genuine risk and, if you are looking for a place to build expertise, an unusually open field.

### 20.1 If the user can influence the prompt, what can the prompt influence?

This is the question that matters most, and it has a precise shape.

A language model with **tool access** is a new execution path into your system. Content the model reads becomes, in effect, instructions it may act on. That is **indirect prompt injection**: the attack arrives not in the user's own message but in something the model consumes — a scanned document, a shared file, a web page in a WebView, a message from another user, an email body.

The correct mental model is one you already have: **treat model output exactly as you treat WebView content.** Untrusted. Validated before it reaches anything that mutates state. Never interpolated into a privileged call without checks.

This is recognised at platform level now. Apple's WWDC26 material covers threat modelling agentic app features and applying deterministic mitigations for indirect prompt injection in Foundation Models and App Intents, and the MASTG has added a knowledge entry on **App Intents and AI agent exposure** (MASTG-KNOW-0129). The surface is being formalised as you read this.

Note also why this is specifically a *mobile* problem rather than only a backend one: the mobile client is where untrusted content enters — the camera, the share sheet, the clipboard, the WebView, the file picker. Your existing input validation was designed for form fields, not for content a model will interpret.

### 20.2 What must never leave the device?

Once user data is in a request body to a third-party model provider, your data-residency and processing story has changed — regardless of what your privacy policy says.

If you have signed commitments with a regulator, or hold obligations under GDPR, HIPAA or a banking supervisor, whoever owns those commitments needs to know **before** you ship, not after. This is a five-minute conversation that occasionally prevents a nine-month remediation.

Practically: classify what the feature needs, send the minimum, and consider whether an on-device model gets you enough. Redact before transmission where you can. And decide deliberately whether provider-side retention and training settings match what you have promised your users.

### 20.3 Where does the model key live?

If it is in the app, it is public. Chapter 15's problem with a new cost dimension: leaked model keys are billed to you by the token, and the bill arrives faster than your monitoring.

Proxy through your backend, always. There is no configuration of client-side key storage that makes an in-app model provider key safe, because Chapter 1.

### 20.4 Can you distinguish a real client from a script?

An unattested endpoint behind a metered model is a billing incident waiting to happen.

This is the clearest business case for attestation you will ever get to write, and it is worth using: **an attacker does not need to steal any data to hurt you here. They only need to spend your inference budget.** That reframing lands with finance stakeholders in a way that "defence in depth" does not.

Rate limit per account and per device, require assertions or integrity tokens on the inference path, and alert on volume anomalies rather than discovering them on the invoice.

### 20.5 What happens when the model is wrong?

Not *if*. Define the fallback path, the timeout, and the user-visible behaviour when the model fails, times out, or returns something unusable. A feature with no fallback is an outage with a friendlier name.

For anything consequential, keep a human in the loop, and make the model's role legible to the user so they can apply their own judgement.

### 20.6 What are you logging?

Prompts and completions frequently contain user data. If your observability pipeline captures them, and by default it probably does, that pipeline is now in scope for every privacy commitment you hold, and your log retention policy just became a data retention policy.

### 20.7 The eval question, which is a security question

One more, less obvious. Without an **eval set**, you cannot tell whether a change to your prompt, your retrieval, or your model version broke a safety property you were relying on. Evaluation is usually framed as a quality practice. It is also how you detect regressions in behaviour you are treating as a control.

---

## Chapter 21: Kotlin Multiplatform — what can be shared

KMP adoption grew from roughly 7% to 18–23% in a single year, and this question comes up on every project that adopts it. Published security guidance for it is close to nonexistent, which makes this chapter unusually useful and also a good thing to write about publicly.

### 21.1 The line, and the reasoning behind it

The rule is: **share the logic and the contracts; keep the platform trust primitives native.**

The reasoning is what matters, because it lets you classify anything not on the list. **Anything whose security derives from platform hardware or a vendor's attestation service cannot be abstracted without losing the property that made it valuable.** A Keystore key is protected because a specific trusted application in a specific TEE enforces its authorizations. There is no cross-platform abstraction of that; there are two different mechanisms with a similar shape.

What you *can* share is everything around it — and that turns out to be most of the code.

**Shareable:** token storage *interfaces* via `expect`/`actual`; encryption utilities behind a shared interface with Tink on Android and CryptoKit on iOS; API security header construction, nonce generation and encoding; input validation patterns; risk-signal data models.

**Must stay native:** Keystore and Keychain access; `BiometricPrompt` and `LocalAuthentication`; Play Integrity and App Attest; network security configuration (Android XML, iOS `Info.plist` and URLSession delegate).

### 21.2 The mistake that will bite you

Define your `expect` declarations around **intent**, not mechanism.

`expect fun getKeystoreKey(alias: String): Key` leaks Android's model into shared code and will not map cleanly onto the Secure Enclave — which, remember from Chapter 4, supports elliptic curves only and does not do direct encryption.

`expect suspend fun storeToken(token: String, requiringUserAuth: Boolean)` describes what you want and implements cleanly on both platforms, because it leaves each `actual` free to use the right primitive.

This sounds like an API design point. It is a security point: an abstraction that forces one platform's mechanism onto the other produces implementations that quietly weaken to fit the interface.

### 21.3 Two practical cautions

**Your `actual` implementations need equivalent review.** Shared code gets read by everyone; platform-specific code often gets read by one person. The iOS `actual` that stores a token with `kSecAttrAccessibleAlways` because it fixed a background bug is exactly the kind of thing that survives in a KMP codebase, because the Android reviewers never opened that file.

**Budget for CI cost.** Multiplatform builds need macOS runners for the iOS targets, which is a real line item rather than an afterthought — and, per Chapter 15, another runner to harden and monitor.

---
