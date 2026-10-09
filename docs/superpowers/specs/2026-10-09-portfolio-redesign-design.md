# Portfolio redesign: Home & Away Kit with Rookie Card

Date: 2026-10-09 · Status: awaiting review · Product context: `PRODUCT.md`

## Goal

Rebuild `index.html` (https://www.krishnanishad.com.np) in the "Home & Away Kit" world, with the holographic rookie card as its 3D centrepiece. A visitor from either audience (brand/social clients, dev employers) should understand within one viewport that Krishna does both, and reach projects or contact.

**Approved reference:** `.impeccable/mocks/decision/samples/kit-card.html` (serve over http to see the photo; `?kit=away`, `?back` for states). The build matches it in the first viewport and extends its grammar to every section below.

## What the user approved (do not change without asking)

- **Two kits, one switch.** HOME = crimson `#C8102E` + white, for brand & social. AWAY = navy `#0B1F4B` + volt `#D7FF3A`, for developer. Gold `#C9A227` is shared. One `data-kit` attribute on `<html>` swaps CSS custom properties for the whole page. The switch ripples the new kit out from the pressed button, and the card spins and recolours.
- **Kit-specific content.** The typed "Now playing" role jumps to match the kit: Home → Brand Identity Manager, Away → Developer. It then keeps cycling the three roles. The lede's second sentence changes per kit. In Away, dev projects come before brand experience.
- **Rookie card (Three.js).** Foil shader, penny sleeve, tilt toward the pointer, Flip button to the stats back. Front:
  - the original `krishna_profile.png` in natural colour, with a holographic ray sheen over its backdrop only (subject masked out using `assets/img/krishna_cutout.png`);
  - KN crest, RC shield, foil name plate, "BRAND × DEV", "NO. 21", #21/21.
  - The card frame takes the kit colours.
- **Back of the card:** +447% engagement, hundreds of posts, millions of engagements on top posts, since Oct 2022, career rows.
- **Kit grammar everywhere:** matchday-strip nav, KN crest, Anton drop-shadow display type, Barlow Condensed labels, Barlow body text, subtle mesh-weave texture, stitched patches.
- **Calm first viewport:** nav, "Now playing" patch, name, lede, kit switch, two actions, card. Nothing else.

## Page structure (one file, one page)

| Section | Kit treatment | Content (from current `index.html`, no invented facts) |
|---|---|---|
| Hero | as approved sample | name, typed roles, lede, kit switch, See the work / Write to me, card |
| About ("Player profile") | stat-sheet layout; portrait not repeated (it's on the card) | intro paragraph, birthday, phone, city, email; interests (8) as sleeve-patch chips |
| Experience ("Club career") | fixture rows: date · club · role · result | Availclouds, Wintries, Educational Consultancy, with the existing bullet points |
| Projects ("Dev fixtures") | rookie-card-style project cards, kit-coloured; Away moves this above Experience | Availclouds MSP Help Desk → `projects/availclouds.html`; Face Detection System and Unreal Engine Game → existing LinkedIn links; existing images |
| Education ("Academy") | one fixture row + certificate patch | Tribhuvan University BSc CSIT 2022–present, 3.5 GPA, Rotaract; Game Theory (Stanford/Coursera) link |
| Skills ("Squad attributes") | grouped patch chips | the 5 existing groups, verbatim |
| Contact ("Full time") | big closing block | email (mailto), phone (tel:), address line, LinkedIn / GitHub / Instagram, Resume (existing Drive link) |

The Resume link stays in the nav (opens the Drive PDF).

## Technical

- **Files:**
  - `index.html` is rewritten as a single file with inline CSS, and the card is an inline `<script type="module">`.
  - Three.js `0.160.0` comes from jsDelivr via an importmap, as in the sample.
  - Google Fonts: Anton, Barlow Condensed, Barlow.
- **Removed from index:** the music player and `<audio>`, Bootstrap, jQuery, all `assets/vendor` CSS/JS, `style.css`, `main.js`, typed.js (replaced by a few lines of JS), the defunct `UA-169007209-3` gtag, and dead commented-out blocks.
- **Kept:** GTM `GTM-5BB8W2X` (head and noscript), favicon, title/description meta (updated wording), the `CNAME`.
- **Deleted from repo:** `assets/audio/` (5.4 MB), the 10 legacy `projects/*.html` pages, `assets/vendor/`, `assets/css/style.css`, `assets/js/main.js`, and project images only those pages used.
- **New asset:** `assets/img/krishna_cutout.png` (already created; mask only).
- **Fallbacks:**
  - `prefers-reduced-motion`: one static card frame, no ripple or spin, instant kit swap.
  - No WebGL: a static DOM card (photo + name plate) in the same spot.
  - Photo load failure: big "21" in the card window.
  - All text lives in the DOM; nothing important exists only inside the canvas.
- **Responsive:**
  - 1440 and 1280 desktop: card on the right.
  - 1024 tablet: card on the right, scaled down.
  - Below 768: card stacks under the hero copy; no horizontal scroll at 390.
  - Tap targets ≥ 44px.
- **Accessibility:**
  - The kit switch is a radio group with arrow keys.
  - Flip is a `<button aria-pressed>`.
  - Visible focus rings.
  - WCAG AA contrast in both kits; gold is never used for small text.
- **Persistence:** the chosen kit is remembered in `localStorage` (try/catch), and `?kit=away` overrides it.

## Search indexing & SEO (added 2026-10-09, user request)

**Diagnosis (checked live):**
- The site is served at `https://www.krishnanishad.com.np` (Cloudflare → GitHub Pages) and isn't in search results.
- `http://` and `https://` both return 200 with no redirect, so Google sees duplicate URLs.
- The apex `https://krishnanishad.com.np` 301s to **http**://www.
- No `robots.txt` (404) and no sitemap.
- Generic title and description; no canonical, Open Graph or structured data.
- 10 legacy template pages by another person ("Prerak") live under `/projects/`.
- Googlebot is not blocked: Cloudflare returns 200 to the Googlebot UA.

**In code (this build):**
- `robots.txt`: allow all, disallow `/docs/`, plus a `Sitemap:` line.
- `sitemap.xml`: `/` only, with `lastmod`. `projects/availclouds.html` carries its own `noindex` and stays out.
- `<head>`:
  - `<link rel="canonical" href="https://www.krishnanishad.com.np/">`;
  - name-first title (≤60 chars) and a description (≤155 chars) built from real content;
  - `theme-color` per kit;
  - Open Graph and Twitter card tags;
  - `apple-touch-icon`.
- Share image `assets/img/og-card.png` (1200×630, Home-kit card art), rendered from HTML with headless Chrome.
- JSON-LD `@graph`:
  - `Person`: name, alternateName "krimy", jobTitle, worksFor Availclouds Hosting Services, alumniOf Tribhuvan University, address Rupandehi NP, email, image, sameAs LinkedIn/GitHub/Instagram, knowsAbout skills.
  - `WebSite`, and `ProfilePage` with `mainEntity` → Person.
- Semantic structure:
  - one `<h1>` (the name), `<h2>` per section, real `<nav>`, `<main>`, `<footer>`;
  - descriptive `alt` text; text links instead of icon-only links (or with `aria-label`).
- Performance:
  - images re-encoded to WebP via Pillow, with width/height set and `loading="lazy"` below the fold;
  - fonts `display=swap` with preconnect;
  - the Three.js module loads after first paint.
  - Target: LCP < 2.5 s, CLS < 0.1.
- **Legacy pages (user approved deletion):** delete the 10 legacy `projects/*.html` files plus `assets/vendor/`, `assets/css/style.css` and `assets/js/main.js` (11 MB). Nothing else uses them; `availclouds.html` is self-contained.

**Owner actions (outside the repo, I'll give exact steps):**
1. **Cloudflare:**
   - SSL/TLS → Edge Certificates → **Always Use HTTPS: On**.
   - Fix the apex redirect so `krishnanishad.com.np` → `https://www.krishnanishad.com.np` (a Redirect Rule, 301, preserving path).
2. **Google Search Console:**
   - Add a Domain property `krishnanishad.com.np` and verify by a DNS TXT record in Cloudflare.
   - Submit `sitemap.xml`, then URL Inspection → Request indexing for `/`.
3. **Bing Webmaster Tools:** import from Search Console. This also covers DuckDuckGo and Yahoo.
4. **Backlinks:** put the URL on LinkedIn (Contact info + Featured), GitHub profile README / website field, Instagram bio, and the Availclouds team page if one exists.

## Out of scope

`projects/availclouds.html` (unchanged), a blog, analytics changes beyond removing the dead UA tag.

## Verification

- **Screenshots:** headless Chrome over `python -m http.server` at 1440 (Home, Away, card back), 1024 and 390.
- **Live check in the browser pane:**
  - kit switch, card tilt and flip, typed roles, all nav anchors and external links;
  - no console errors;
  - no horizontal overflow at 390.
- **Impeccable:** detector once on `index.html`, then the finish reviewer and documenter (`DESIGN.md`).
