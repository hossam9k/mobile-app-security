---
part: 05
last_verified: 2026-09-11
volatility: medium
recheck_because: "Tooling and bypass techniques move"
---

# Part 5: Resilience

## Chapter 13: How reverse engineering actually works

You cannot reason about anti-tampering without knowing what you are defending against, at the level of the actual commands. This chapter is the attacker's workflow — which is also your testing workflow, because Chapter 22 asks you to run it against your own app.

### 13.1 Static analysis

Static analysis reads the app without running it.

**Obtain the artifact.** Pull the APK from a device or the store; extract the IPA. MASTG covers this as MASTG-TECH-0003.

**Explore the package.** The manifest tells an attacker your components, permissions, exported activities, deep link schemes, and whether you are debuggable. This is a map of your attack surface, and it is the first thing anyone reads.

**Retrieve strings** (MASTG-TECH-0071). This is where hardcoded keys, internal hostnames, and debug flags fall out. Thirty seconds of work.

**Decompile.** JADX turns Dalvik bytecode into readable Java. For Android you can also disassemble to smali, which is what you edit if you intend to repackage. On iOS, radare2 and similar tools disassemble the Mach-O binary; Swift and Objective-C metadata gives up class and method names generously.

**Read the security logic.** Root detection, pinning configuration, license checks — all of it is now visible, and its structure tells the attacker exactly what to hook.

### 13.2 Dynamic analysis

Dynamic analysis runs the app and interferes.

**Get a shell and reach the data directory** (MASTG-TECH-0001, MASTG-TECH-0008). `/data/data/<package>/` holds your preferences, databases and caches. This is where "we encrypt sensitive data" gets verified or falsified in about a minute.

**Monitor logs** (MASTG-TECH-0009). Release builds that still log are found here.

**Set up an interception proxy** (MASTG-TECH-0011). Route traffic through mitmproxy or Burp with the attacker's CA installed.

**Bypass certificate pinning** (MASTG-TECH-0012). This is the step that tells you whether your pinning is real. `objection` will do it with one command for common implementations; a Frida script handles the rest. **Every engineer who has shipped pinning should have done this to their own app**, because until you have, you do not know whether your pinning survives contact.

**Hook methods with Frida** (MASTG-TECH-0051). Replace any function's behaviour at runtime. Return `false` from your root check. Return `true` from your biometric callback. Log the arguments to `Cipher.doFinal` and watch your own plaintext go past.

**Repackage** (MASTG-TECH-0004). Modify smali, rebuild, re-sign with the attacker's key, install. This is the cloning attack, and it is why signature verification exists.

#### The tools an attacker uses, and what each one gives them

You will see these names in every discussion of mobile security. Knowing what each actually does makes the rest of this chapter concrete.

| Tool | What it does | What it gives an attacker |
|---|---|---|
| **JADX** | Decompiles an APK to readable Java-like source | Your logic, endpoints, and where your security decisions live |
| **Frida** | Runtime instrumentation — hooks and replaces any method in a live process | The ability to change what your code does without changing the file |
| **objection** | Frida-powered toolkit with prebuilt commands | Storage inspection and pinning bypass without writing a script |
| **Xposed / LSPosed** | System-wide hooking framework on rooted Android | Persistent modification across apps |
| **Cydia Substrate / Cycript** | The iOS equivalents of runtime hooking and inspection | The same capability on jailbroken iOS |
| **radare2 / Hopper** | Disassemblers for native and Mach-O binaries | Your native code, including logic you moved there for protection |
| **apktool** | Decodes and rebuilds an APK | Repackaging: change something, re-sign, redistribute |
| **mitmproxy / Burp Suite** | Intercepting proxies | All your traffic, in cleartext, on a device they control |
| **`strings`** | Prints printable strings in a binary | Every constant you embedded, in about thirty seconds |

Two observations worth carrying. Every one of these is **free and documented**, so none of your protection can assume scarcity of tooling. And you should be running all of them against your own app (Chapter 22) — an attacker's toolkit and your test toolkit are the same toolkit.

### 13.3 The three demos that make the argument

The MASTG ships runnable demos, and one sequence is worth more than any amount of prose on this topic. Read them in order:

**MASTG-DEMO-0106** — extracting sensitive data from `Cipher.doFinal` via Frida hooking. The attack works.

**MASTG-DEMO-0107** — detecting Frida hooks and terminating the application in response. The defence works.

**MASTG-DEMO-0108** — bypassing that Frida detection in `/proc/self/maps` and extracting the data anyway. The defence is defeated.

Protect, detect, bypass. That progression, published by the standard itself, is the strongest available argument for the position in the next chapter. Two more demos make the same point about obfuscation: MASTG-DEMO-0132 and 0133 show root detection defeated when it is protected only by identifier renaming, in the Java and native layers respectively.

- <https://mas.owasp.org/MASTG/techniques/>

---

## Chapter 14: Obfuscation and tamper detection — the honest chapter

This is where security writing usually oversells, so let me be direct: **everything in this chapter can be bypassed by a competent attacker with device access.** You are buying time and raising cost, not achieving prevention.

That is not an argument against doing it. Time and cost are real currency against three of the four adversaries in Chapter 1. It is an argument against *believing your own marketing*, and against designing as though these controls hold.

### 14.1 The cheap things, which you should simply do

Start here. Every item below costs close to nothing and removes the easiest tier of attacker.

**Enable R8 with obfuscation and resource shrinking** on Android; **strip symbols** on iOS. Free, automatic, and it removes the trivial-effort tier of attacker.

**Remove all logging from release builds**, and verify by inspecting the artifact rather than trusting the build flag. MASTG-BEST-0002 and 0022.

**Ensure `debuggable` is false** and no debug configuration shipped. MASTG-BEST-0007. A debuggable production build is not a hardening gap, it is an open door.

**Disable WebView debugging** in release. MASTG-BEST-0008.

**Prevent screenshots on sensitive screens.** `FLAG_SECURE`, `setRecentsScreenshotEnabled`, `setSecure` for SurfaceViews, and `SecureFlagPolicy.SecureOn` for Compose dialogs — that last one catches people who did everything else right.

**Use up-to-date signing schemes** (MASTG-BEST-0006) and a current `minSdkVersion` (MASTG-BEST-0010). Old signature schemes and old API levels both reopen closed attack classes.

**Set sensible session timeouts**, shorter for financial flows.

None of this is clever. All of it is worth more than most clever things.

### 14.2 Detection: report, never block

Detect what you can — root and jailbreak indicators, hooking frameworks (Frida, Xposed, Substrate, Cycript), debuggers, emulators and virtual devices, repackaging via your own signature check, and storage or code integrity failures.

Then **send those findings to your backend as risk inputs, and let the session continue.**

Three reasons, and they compound.

**Local blocks are trivially removed.** The attacker is already running your code under a debugger with the ability to hook any method. Your `if (isRooted()) exit()` is one hook away from `if (false) exit()`. You have built a speed bump and paid for a wall. MASTG-DEMO-0108 is this argument, demonstrated.

**You generate false positives against real people.** Developers, power users, users of custom ROMs in regions where that is normal, users of legitimate accessibility tooling. A hard local block converts these into support tickets and one-star reviews, for no security gain.

**You destroy your own intelligence.** A backend that receives "hooking framework detected on this session" can require step-up authentication, cap transaction limits, flag the account, and correlate across sessions to find the actual attacker. An app that shows a "device not supported" dialog has taught the attacker exactly which check to remove next, and told you nothing.

MASTG-BEST-0029 frames this correctly as implementing resilience and **RASP signals** — signals being the operative word.

### 14.3 Where obfuscation genuinely helps

Two places, and it is worth knowing them so you spend effort well.

**Raising the floor.** Against automated tooling and the opportunist, obfuscation plus resource shrinking is often enough to make your app not worth the trouble relative to the next one.

**Protecting detection logic itself.** If your root detection is legible, it is removable. MASTG-DEMO-0132 shows detection logic in the Java layer defeated when protected only by identifier renaming; MASTG-DEMO-0133 shows the same in native code with insufficient obfuscation. Moving security-critical logic to native code with real obfuscation raises the cost of removing it — MASTG-TEST-0368 and 0369 test exactly this.

What obfuscation does not do is protect a secret. An obfuscated key is a key. Chapter 1's principle still governs.

### 14.4 Detection, in code

Chapter 14.2 argues for detecting and reporting rather than blocking. This section is what the detecting part looks like, so the advice is actionable rather than abstract.

**The shape to aim for on both platforms** *(reasoned)*: collect named signals, return them as data, send them to your backend. No branching on the result locally.

#### Android: root indicators

```kotlin
object RootDetector {

    fun signals(): List<String> = buildList {
        if (checkSuBinaries())   add("SU_BINARY")
        if (checkRootPackages()) add("ROOT_PACKAGE")
        if (checkBuildTags())    add("TEST_KEYS")
        if (checkRwPaths())      add("SYSTEM_WRITABLE")
    }

    private fun checkSuBinaries() = listOf(
        "/system/bin/su", "/system/xbin/su", "/sbin/su",
        "/system/app/Superuser.apk", "/data/local/bin/su"
    ).any { java.io.File(it).exists() }

    private fun checkRootPackages() = listOf(
        "com.topjohnwu.magisk", "eu.chainfire.supersu", "com.koushikdutta.superuser"
    ).any { pkg -> runCatching { context.packageManager.getPackageInfo(pkg, 0) }.isSuccess }

    private fun checkBuildTags() =
        android.os.Build.TAGS?.contains("test-keys") == true

    private fun checkRwPaths() = listOf("/system", "/system/bin", "/vendor")
        .any { java.io.File(it).canWrite() }
}
```

#### Android: debugger and emulator

```kotlin
object DebugDetector {

    data class Result(val isDebugged: Boolean, val isEmulator: Boolean, val signals: List<String>)

    fun detect(): Result {
        val signals = mutableListOf<String>()

        if (android.os.Debug.isDebuggerConnected()) signals += "DEBUGGER_CONNECTED"
        if (tracerAttached())                       signals += "TRACER_ATTACHED"
        if (debuggableBuild())                      signals += "DEBUGGABLE_BUILD"
        if (emulatorFingerprint())                  signals += "EMULATOR_FINGERPRINT"

        return Result(
            isDebugged = signals.any { it.startsWith("DEBUGGER") || it.startsWith("TRACER") },
            isEmulator = signals.any { it.startsWith("EMULATOR") },
            signals    = signals
        )
    }

    /** A non-zero TracerPid means something is attached to this process. */
    private fun tracerAttached(): Boolean = runCatching {
        java.io.File("/proc/self/status").readLines()
            .firstOrNull { it.startsWith("TracerPid:") }
            ?.substringAfter(":")?.trim()?.toIntOrNull() ?: 0
    }.getOrDefault(0) != 0

    private fun debuggableBuild(): Boolean =
        (appInfo.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0

    private fun emulatorFingerprint(): Boolean = with(android.os.Build) {
        FINGERPRINT.startsWith("generic") || FINGERPRINT.contains("vbox") ||
        MODEL.contains("Emulator") || MODEL.contains("Android SDK built for") ||
        HARDWARE.contains("goldfish") || HARDWARE.contains("ranchu") ||
        PRODUCT == "sdk" || PRODUCT == "google_sdk"
    }
}
```

`TracerPid` is the most useful of these. A debugger or Frida attaching shows up there, and it needs no permission to read.

#### iOS: jailbreak and hooking indicators

```swift
enum JailbreakDetector {

    static func signals() -> [String] {
        var out: [String] = []
        if suspiciousPathsExist() { out.append("SUSPICIOUS_PATH") }
        if canOpenCydiaScheme()   { out.append("URL_SCHEME") }
        if canWriteOutsideSandbox() { out.append("SANDBOX_WRITABLE") }
        if canFork()              { out.append("FORK_ALLOWED") }
        if suspiciousDylibLoaded() { out.append("HOOKING_DYLIB") }
        return out
    }

    private static func suspiciousPathsExist() -> Bool {
        ["/Applications/Cydia.app", "/bin/bash", "/usr/sbin/sshd",
         "/etc/apt", "/private/var/lib/apt/", "/usr/lib/libsubstrate.dylib"]
            .contains { FileManager.default.fileExists(atPath: $0) }
    }

    private static func canOpenCydiaScheme() -> Bool {
        guard let url = URL(string: "cydia://package/com.example") else { return false }
        return UIApplication.shared.canOpenURL(url)
    }

    /// A sandboxed app cannot write outside its container.
    private static func canWriteOutsideSandbox() -> Bool {
        let path = "/private/\(UUID().uuidString)"
        guard (try? "test".write(toFile: path, atomically: true, encoding: .utf8)) != nil
        else { return false }
        try? FileManager.default.removeItem(atPath: path)
        return true
    }

    /// fork() succeeding indicates the sandbox is not being enforced.
    private static func canFork() -> Bool {
        let pid = fork()
        if pid >= 0 { if pid > 0 { kill(pid, SIGTERM) }; return true }
        return false
    }

    /// Substrate, Frida's gadget and similar arrive as loaded images.
    private static func suspiciousDylibLoaded() -> Bool {
        for i in 0..<_dyld_image_count() {
            guard let name = _dyld_get_image_name(i) else { continue }
            let path = String(cString: name)
            if ["MobileSubstrate", "libsubstrate", "SubstrateLoader",
                "frida", "cycript", "cynject"].contains(where: { path.contains($0) }) {
                return true
            }
        }
        return false
    }
}
```

#### Reporting, which is the whole point

```kotlin
suspend fun reportSecuritySignals() {
    val payload = SecurityReport(
        rootSignals  = RootDetector.signals(),
        debugSignals = DebugDetector.detect().signals,
        appSignature = currentSignatureHash(),
        timestamp    = System.currentTimeMillis()
    )
    runCatching { api.reportSignals(payload) }   // never block the user on this call
}
```

Three rules for this code. **Send, never branch**: the backend decides (Chapter 14.2). **Fail silently**: a detection report that crashes the app or blocks a flow has converted a security feature into an outage. And **do not name your detection classes `RootDetector`** in a release build: §15.8 shows the R8 configuration that stops you handing an attacker a search term.


#### Verify it

Detection code has two failure modes, and you should test for both.

**False negatives.** Run the app on a rooted device or emulator with Magisk and confirm your signals actually fire. Reaching your backend with an empty signal list from an obviously rooted device means the detection is not running, not that the device is clean.

**False positives, which matter more.** Run on a clean, stock, unrooted device. **Pass:** no signals. **Fail:** any signal at all — you are about to apply risk scoring to ordinary users. Test on at least one non-Google-Play device and one custom ROM if your market includes them.

**Then confirm you are not blocking.** Grep your own codebase:

```
grep -rn "isRooted\|isJailbroken\|isDebugged" --include=*.kt --include=*.swift .
```

Every hit should feed a report, not a branch that exits or refuses. A hit inside an `if` that ends a flow is §14.2's mistake.

**And confirm the names are gone from release.** Decompile your release build and search for `RootDetector`. Finding it means your R8 configuration is keeping what §15.8 tells you to let it obfuscate.

### 14.5 The hygiene controls, in code

Five small controls that appear in every real assessment. Each is a few lines and each maps to a MASWE weakness.

#### Screenshot and recents protection

`MASWE-0038`. On Android, apply the flag per screen rather than app-wide, so you are not degrading the recents experience everywhere:

```kotlin
class PaymentActivity : AppCompatActivity() {
    override fun onResume() {
        super.onResume()
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
    }
    override fun onPause() {
        super.onPause()
        window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
    }
}
```

For Compose dialogs, remember `SecureFlagPolicy.SecureOn` — `FLAG_SECURE` on the activity does not cover a dialog in its own window.

On iOS there is no direct equivalent, so there are two practical approaches. Detect that a capture happened and react:

```swift
NotificationCenter.default.addObserver(
    forName: UIScreen.capturedDidChangeNotification, object: nil, queue: .main
) { _ in
    if UIScreen.main.isCaptured { self.blurSensitiveContent() }
}
```

Or use the long-standing `isSecureTextEntry` trick: place your sensitive view inside the layer of a secure `UITextField`, which the OS excludes from screenshots. It works, and it is a workaround rather than an API, so test it after each iOS release.

#### Secure logging

`MASWE-0005`. The robust pattern is a logging tree that drops everything below error in release:

```kotlin
// Application.onCreate
if (BuildConfig.DEBUG) {
    Timber.plant(Timber.DebugTree())
} else {
    Timber.plant(object : Timber.Tree() {
        override fun log(priority: Int, tag: String?, message: String, t: Throwable?) {
            if (priority >= Log.ERROR) crashReporter.log(message)   // no verbose/debug/info
        }
    })
}
```

This beats scattering `if (BuildConfig.DEBUG)` at call sites, because it cannot be forgotten at one of them. Pair it with the `-assumenosideeffects` rule in §15.8, and verify by inspecting the artifact.

#### Clipboard

`MASWE-0030`. Both platforms have a flag for this and almost nobody sets it.

```kotlin
val clip = ClipData.newPlainText("", sensitiveValue).apply {
    description.extras = PersistableBundle().apply {
        putBoolean(ClipDescription.EXTRA_IS_SENSITIVE, true)   // API 33+
    }
}
clipboard.setPrimaryClip(clip)
```

```swift
UIPasteboard.general.setItems(
    [[UTType.plainText.identifier: sensitiveValue]],
    options: [
        .localOnly: true,                                     // do not sync to other devices
        .expirationDate: Date().addingTimeInterval(60)        // clears itself
    ]
)
```

The iOS `localOnly` option matters more than it looks: without it, a copied value can travel to the user's other devices through Universal Clipboard.

#### Session timeout

`MASWE-0024`. Time the background period, not just user inactivity, because a phone in a pocket is not an active session:

```kotlin
class SessionTimeoutManager(
    private val timeoutMinutes: Int,
    private val onTimeout: () -> Unit
) : DefaultLifecycleObserver {

    private var backgroundedAt: Long? = null

    override fun onStop(owner: LifecycleOwner) {
        backgroundedAt = System.currentTimeMillis()
    }

    override fun onStart(owner: LifecycleOwner) {
        val since = backgroundedAt ?: return
        if (System.currentTimeMillis() - since > timeoutMinutes * 60_000L) onTimeout()
        backgroundedAt = null
    }
}
```

Reasonable starting points *(reasoned)*: 15 minutes for banking and payments, 30 for health and enterprise, hours or none for content and social. And "timeout" must mean invalidating the session **server-side** and clearing local data, per Chapter 0.3 — not just showing a login screen over cached content.

#### Encrypting the database

Following §6.7, the Android implementation with Room:

```kotlin
// build.gradle.kts
// implementation("net.zetetic:sqlcipher-android:4.x")
// implementation("androidx.sqlite:sqlite-ktx:2.x")

val passphrase = SQLiteDatabase.getBytes(getOrCreateDatabaseKey())   // from Keystore, §6.6
val factory = SupportOpenHelperFactory(passphrase)

val db = Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .openHelperFactory(factory)
    .build()
```

`getOrCreateDatabaseKey()` must come from a Keystore-backed key. A hardcoded passphrase turns database encryption into an obfuscation exercise, and `strings` will find it.

---
