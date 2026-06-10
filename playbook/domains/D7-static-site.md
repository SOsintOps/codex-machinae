## D7 Static Site / Frontend-only

**Activation trigger.** The project renders entirely client-side or as a statically-generated
site, with no backend owned by the project itself. This includes single-page applications
(SPA), statically-generated sites (SSG), and hybrid frameworks (Next.js static export,
Astro, Nuxt generate) where no server runtime is deployed by the project.

**In addition to Core.** Core applies fully — requirements, code quality, testing pyramid,
documentation, CI/CD concepts, boundary contracts, change classification, remediation.
This appendix adds the patterns specific to client-side rendering, asset delivery, and
browser-environment constraints.

### D7.1 Build and bundle budgets

Every frontend project maintains explicit size budgets for production artefacts. Budgets
are committed as a baseline file (e.g. `.bundle-budget.json`) and enforced in CI via a
ratchet mechanism analogous to §5.3 coverage ratchet.

| Artefact | Budget metric | Suggested starting point |
|----------|--------------|--------------------------|
| **JS (compressed)** | Total gzip/brotli size of all JS bundles | ≤ 200 KB initial load |
| **CSS (compressed)** | Total gzip/brotli size of all CSS | ≤ 50 KB |
| **Images** | Largest single image (post-optimisation) | ≤ 200 KB; prefer modern formats (WebP, AVIF) |
| **Total page weight** | Sum of all assets for the critical path | ≤ 500 KB initial load |

**Rules:**

1. The budget ratchet only moves downward — if a build produces a smaller bundle, the
   baseline is updated automatically on merge to main.
2. A build that exceeds any budget fails CI. The developer must either optimise or
   request an escape valve (§5.3) with an expiry date and justification.
3. Tree-shaking verification: CI reports which dependencies contribute the most to
   bundle size. Dependencies that are imported but unused (or partially used with no
   tree-shaking) are flagged.
4. Code-splitting is mandatory for any route or feature that is not needed on initial
   load. Lazy-loaded chunks have their own individual budget.

### D7.2 Hosting and CDN contracts

The project's Boundary Contract Map (§8) includes the CDN and hosting provider as
outbound contracts on the `api` axis:

| Contract | Direction | What to document |
|----------|-----------|-----------------|
| CDN (e.g. Cloudflare, Vercel Edge, AWS CloudFront) | outbound | Cache TTLs per asset type, invalidation mechanism, edge-function limits (execution time, memory, request size) |
| Hosting (e.g. Vercel, Netlify, GitHub Pages, S3) | outbound | Build command, output directory, redirect/rewrite rules, environment variables |
| Analytics / third-party scripts | outbound | Each third-party script loaded on the page (tag managers, analytics, chat widgets) |

**Cache-invalidation strategy.** Static assets (JS, CSS, images) use content-hashed
filenames (`main.a1b2c3.js`) and are served with long-lived cache headers
(`Cache-Control: public, max-age=31536000, immutable`). HTML files are served with
short TTLs (`max-age=0, must-revalidate` or `s-maxage=60`) so deployments take effect
immediately.

**Edge functions.** If the project uses edge functions (middleware, A/B testing,
geolocation routing), they are treated as boundary contracts with their own tests.
Edge-function cold-start latency is monitored and budgeted.

### D7.3 Client-side error reporting

Errors that occur in the browser must be captured, reported, and triaged:

1. **Error-reporting service.** Integrate a service (Sentry, Bugsnag, Datadog RUM, or
   equivalent) that captures unhandled exceptions and unhandled promise rejections.
2. **Source maps.** Upload source maps to the error-reporting service on every
   deployment. Source maps are never served publicly — they are uploaded as a build
   step and associated with the release version.
3. **Session context.** Each error report includes: browser/OS, page URL, release
   version, user consent status. No PII is attached without explicit user consent.
   When M2 Security-sensitive is active, the PII exclusion is enforced by M2.2.
4. **Error budget.** Define an error-rate threshold (e.g. < 0.1% of sessions with an
   unhandled JS error). Exceeding the threshold triggers investigation, analogous to
   the coverage ratchet.
5. **Session replay** (optional). If enabled, replay is consent-gated and masks all
   form inputs by default. Replay recordings are retained for a maximum of 30 days
   unless a longer retention is justified and approved.

### D7.4 Accessibility

Accessibility is a non-negotiable quality dimension, not an optional enhancement.

**Baseline standard:** WCAG 2.2 Level AA. The project may target Level AAA for specific
criteria but Level AA is the minimum.

**Testing layers:**

| Layer | Tool examples | When |
|-------|--------------|------|
| **Automated lint** | eslint-plugin-jsx-a11y, axe-core, Lighthouse CI | Every PR (CI) |
| **Automated audit** | axe-core in integration tests, Pa11y | Every PR (CI) |
| **Manual audit** | Screen reader (VoiceOver, NVDA), keyboard-only navigation | Every release and after significant UI changes |

**Rules:**

1. Every interactive element is keyboard-accessible (focusable, operable, visible
   focus indicator).
2. Every image has an `alt` attribute. Decorative images use `alt=""` and
   `role="presentation"`.
3. Colour contrast meets WCAG AA ratios (4.5:1 for normal text, 3:1 for large text).
4. Form inputs have associated `<label>` elements. Error messages are programmatically
   associated with the input.
5. Dynamic content changes are announced to screen readers via ARIA live regions.
6. The page is usable at 200% zoom without horizontal scrolling.

Accessibility violations found by automated tools fail CI. Violations found by manual
audit are filed as bugs with severity proportional to impact.

### D7.5 Core Web Vitals

The project monitors [Core Web Vitals](https://web.dev/vitals/) and maintains
thresholds that trigger investigation when breached:

| Metric | What it measures | Threshold (good) | Threshold (needs improvement) |
|--------|-----------------|-------------------|-------------------------------|
| **LCP** (Largest Contentful Paint) | Loading performance | ≤ 2.5 s | ≤ 4.0 s |
| **INP** (Interaction to Next Paint) | Responsiveness | ≤ 200 ms | ≤ 500 ms |
| **CLS** (Cumulative Layout Shift) | Visual stability | ≤ 0.1 | ≤ 0.25 |

**Monitoring:**

1. **Lab data.** Lighthouse CI runs on every PR against a representative set of pages.
   Results are compared against the thresholds above. Regression beyond "needs
   improvement" fails CI.
2. **Field data.** Real-user monitoring (RUM) via the web-vitals library or the
   error-reporting service (D7.3). Field data is reviewed weekly; a sustained
   regression triggers investigation.
3. **Budget alerts.** When a metric crosses from "good" to "needs improvement" in
   field data, an alert is raised (issue, Slack notification, or equivalent).

CLS is particularly sensitive to layout shifts caused by late-loading images, fonts, or
third-party scripts. Every image has explicit `width` and `height` attributes (or CSS
`aspect-ratio`). Font loading uses `font-display: swap` or `optional` to prevent
invisible text.

---

