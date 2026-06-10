## D6 Mobile App

**Activation trigger.** The project ships to iOS App Store, Google Play, or any
vendor-gated mobile distribution channel. This includes native apps (Swift/Kotlin),
cross-platform frameworks (Flutter, React Native, .NET MAUI), and hybrid apps
(Capacitor, Cordova).

**In addition to Core.** Core applies fully — requirements, code quality, testing pyramid,
documentation, CI/CD concepts, boundary contracts, change classification, remediation.
This appendix adds the patterns specific to mobile distribution, device fragmentation,
and platform-mandated constraints.

### D6.1 App-store submission and review

Every release destined for a store follows a structured submission workflow:

| Step | Action |
|------|--------|
| **1. Pre-submission checklist** | All tests pass, CHANGELOG updated, version and build number bumped, store metadata updated (screenshots, description, what's new) |
| **2. Build** | CI produces a signed artefact: `.ipa` (iOS) or `.aab` (Android). Signing credentials are stored in CI secrets, never on developer machines |
| **3. Upload** | Artefact uploaded to App Store Connect / Google Play Console via CI (Fastlane, Gradle Play Publisher, or equivalent) |
| **4. Internal testing** | Distribute to internal testers (TestFlight internal group, Google Play internal track) for smoke testing |
| **5. External testing** | Distribute to external beta testers (TestFlight external group, Google Play open/closed track) for broader validation |
| **6. Submit for review** | Submit to Apple App Review / Google Play review. Include review notes explaining any non-obvious functionality |
| **7. Staged rollout** | After approval, release to a percentage of users (see D6.2) |

**Review rejection protocol.** If the store rejects the build:

1. Record the rejection reason in the project's issue tracker.
2. Fix the issue in a patch release (do not resubmit the same build with metadata-only changes unless the rejection was metadata-related).
3. Re-submit with review notes explaining the fix.
4. If the rejection is disputed, file an appeal through the store's dispute channel and document the outcome.

### D6.2 Staged rollouts

Never release to 100% of users immediately. Use the store's staged-rollout mechanism:

| Phase | Percentage | Duration | Gate |
|-------|-----------|----------|------|
| **Canary** | 1–5% | 24–48 hours | No crash-rate spike (D6.4), no critical bug reports |
| **Early adopters** | 10–25% | 48–72 hours | Crash rate stable, no P0/P1 issues |
| **Wide** | 50% | 24–48 hours | Metrics stable, user feedback reviewed |
| **Full** | 100% | — | All gates passed |

**Halt criteria.** Roll back (or pause the rollout) immediately if:

- Crash-free rate drops below the project's threshold (suggested: < 99.5%).
- A P0 or P1 bug is confirmed by more than one user.
- A store-policy violation is discovered post-release.

Rolling back on mobile means halting the staged rollout and, if necessary, publishing a
hotfix. Unlike server-side rollback, a published mobile binary cannot be removed from
devices that already installed it — the fix must go forward.

### D6.3 Device and OS compatibility

Mobile projects maintain an explicit support matrix:

| Dimension | Policy |
|-----------|--------|
| **Minimum OS version** | Support at least the two most recent major OS versions (e.g. iOS 17+ / Android 14+). Document the policy in the README and in the store listing |
| **Target SDK** | Always target the latest stable SDK to access new APIs and satisfy store requirements |
| **Screen sizes** | Test on at least three form factors: small phone, large phone, tablet (if supported) |
| **Hardware variation** | Test on at least one low-end and one high-end device per platform |

**Deprecating an OS version.** When dropping support for an OS version:

1. Announce in the CHANGELOG at least one minor release before the drop.
2. Show an in-app notice to users on the deprecated OS version.
3. Remove the OS from the CI test matrix only after the deprecation release ships.

### D6.4 Crash reporting and on-device telemetry

Every mobile app integrates a crash-reporting and analytics service:

| Capability | Recommended tools | Requirements |
|------------|-------------------|--------------|
| **Crash reporting** | Firebase Crashlytics, Sentry, Bugsnag | Automatic symbolication (dSYM for iOS, mapping file for Android), uploaded in CI on every release build |
| **Analytics** | Firebase Analytics, Amplitude, Mixpanel | Consent-gated (GDPR/CCPA). No tracking fires before the user grants consent |
| **Performance monitoring** | Firebase Performance, Sentry Performance | App start time, screen rendering time, network latency |

**Rules:**

1. **Symbolication files** (dSYM, ProGuard/R8 mapping) are uploaded to the crash-reporting service as a CI step on every release build. Without them, crash reports are unreadable.
2. **Consent.** Analytics and non-essential telemetry require explicit user consent. Crash reporting may run without consent if it collects no PII (stack traces only, no user identifiers). When M2 Security-sensitive is active, the consent implementation is reviewed against M2.2.
3. **Crash-free rate.** The project defines a target crash-free rate (suggested: ≥ 99.5% of sessions). The rate is monitored daily; a drop below threshold triggers investigation.
4. **No PII in crash reports.** User identifiers, email addresses, and authentication tokens must never appear in crash logs. Breadcrumbs (user actions leading to a crash) are anonymised.

### D6.5 Offline-first and data synchronisation

Mobile apps must handle network absence gracefully:

1. **Offline-capable by default.** Core functionality works without a network connection. Features that require network connectivity degrade gracefully with a clear user message — not a crash or a blank screen.
2. **Local storage.** Data that the user creates or modifies offline is persisted locally (SQLite, Core Data, Room, or equivalent). The local store is the source of truth until sync completes.
3. **Conflict resolution.** When the user modifies data offline and the server state has changed, the app applies a documented conflict-resolution strategy:
   - **Last-write-wins** for low-risk fields (preferences, display settings).
   - **Manual merge** for high-risk fields (financial data, shared documents). The app presents both versions and lets the user choose.
4. **Sync indicator.** The UI shows the sync state: synced, pending, syncing, conflict. The user always knows whether they are looking at local or server data.

### D6.6 Over-the-air (OTA) vs store updates

Some frameworks (React Native, Flutter via Shorebird, Expo) support OTA code updates
that bypass the store review cycle. OTA is powerful but carries risk:

| Aspect | Store update | OTA update |
|--------|-------------|------------|
| **Review** | Store-reviewed | Not reviewed by the store |
| **Rollback** | Halt staged rollout | Instant rollback to previous bundle |
| **Scope** | Any change (native + JS) | JS/Dart-only changes (no native code) |
| **Compliance** | Always compliant | Must comply with store policies (Apple §3.3.2, Google Play Developer Policy §8.6) |
| **Latency** | Hours to days (review queue) | Minutes |

**Rules:**

1. OTA is permitted only for bug fixes and minor UI adjustments — never for new features that would require store review.
2. Every OTA update is versioned and logged in the project's release history (M3.2).
3. The app includes a mechanism to force a store update when a native-code change is required (minimum-version check against a server-side flag).
4. OTA rollback is tested as part of the release process. If the rollback mechanism fails, OTA is disabled until it is fixed.

