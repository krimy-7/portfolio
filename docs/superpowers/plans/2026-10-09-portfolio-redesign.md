# Portfolio Redesign (Home & Away Kit + Rookie Card + SEO) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `index.html` with the approved Home & Away Kit design (3D holographic rookie card, two colour kits), make the site indexable (robots, sitemap, canonical, structured data, share card), and delete the template leftovers.

**Architecture:** One static page with inline CSS and an inline Three.js module, served by GitHub Pages behind Cloudflare. The approved sample `.impeccable/mocks/decision/samples/kit-card.html` is the visual and behavioural source of truth: port it, don't reinvent it. A single Python check script (`tools/check_site.py`) is the regression test for structure, SEO and dead links. Visual checks are headless Chrome screenshots plus the browser pane.

**Tech Stack:** HTML/CSS, vanilla JS, Three.js 0.160.0 (jsDelivr importmap), Google Fonts (Anton, Barlow Condensed, Barlow), Python 3 + Pillow (assets and checks), headless Chrome (screenshots).

**Spec:** `docs/superpowers/specs/2026-10-09-portfolio-redesign-design.md` (product context: `PRODUCT.md`)

## Global Constraints

- Canonical origin: `https://www.krishnanishad.com.np` (the `CNAME` file holds `www.krishnanishad.com.np`; do not change it).
- No build step, no npm dependencies; Three.js only via `https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js`.
- Kits: HOME `#C8102E` + `#FFFFFF`; AWAY `#0B1F4B` + `#D7FF3A`; gold `#C9A227` in both, never for text under 24px.
- Typed roles exactly: "Brand Identity Manager", "Developer", "Twitch Streamer". Home jumps to "Brand Identity Manager", Away to "Developer".
- Keep GTM `GTM-5BB8W2X` (head snippet and noscript iframe). Remove the `UA-169007209-3` gtag.
- Phone `+977-9864951223` and birthday "21 October" stay public.
- No invented facts, metrics, clients or testimonials. Copy comes from the current `index.html` / `PRODUCT.md`.
- `projects/availclouds.html` is not modified.
- WCAG AA contrast in both kits; tap targets ≥ 44px; nothing important exists only in a canvas.
- Run every local server from the repo root: `python -m http.server 8765` (the `.claude/launch.json` config "site" does this).

## Review Focus

1. **Page opened with no WebGL or behind a slow CDN.** Copy, nav, kit switch and contact still work, and a static DOM card shows. Pinned in Task 5 Step 4.
2. **`prefers-reduced-motion: reduce`.** No ripple, spin or typing animation; the kit swaps instantly, the card renders one frame, and roles show statically. Pinned in Task 5 Step 4.
3. **`localStorage` blocked (private mode / Safari ITP).** The kit switch still works and nothing throws. Pinned in Task 5 Step 4.
4. **Every internal link and asset resolves after the deletions,** including the Availclouds page and all images. Pinned by `check_site.py` (Task 1), run in Tasks 2–6.
5. **390px phone.** No horizontal scroll, the card stacks under the copy, and the Flip button and kit radios are ≥ 44px. Pinned in Task 6 Step 2.

---

## File Structure

| Path | Action | Responsibility |
|---|---|---|
| `tools/check_site.py` | Create | Single regression check: SEO tags, JSON-LD, robots/sitemap, heading structure, local links/assets exist, removed things stay removed |
| `robots.txt` | Create | Crawl rules + sitemap pointer |
| `sitemap.xml` | Create | `/` with lastmod |
| `assets/img/*.webp`, `assets/img/og-card.png`, `apple-touch-icon.png` | Create | Optimised images, social share card, iOS icon |
| `tools/og-card.html` | Create | Source for rendering `og-card.png` (kept so the card can be re-rendered) |
| `index.html` | Rewrite | The page: head/SEO, sections, inline CSS, kit switch, typed roles, Three.js card |
| `projects/{blog,gan,iras,ml,musicplayer,recommender,resume,todo,twitteranalysis,vdg}.html`, `assets/vendor/`, `assets/css/`, `assets/js/`, `assets/audio/`, legacy-only images | Delete | Template leftovers |
| `DESIGN.md`, `.impeccable/design.json` | Create (Task 6, documenter) | Design system record |

---

### Task 1: Site check script (the regression test)

**Files:**
- Create: `tools/check_site.py`

**Interfaces:**
- Produces: `python tools/check_site.py` exits 0 and prints `OK` when the site is valid; it exits 1 and prints one `FAIL: <reason>` line per failure otherwise. Later tasks run this after each change.

- [ ] **Step 1: Write the check script**

```python
"""Regression check for the static site. Run from repo root: python tools/check_site.py"""
import json, re, sys, xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://www.krishnanishad.com.np"
fails = []
def check(cond, msg):
    if not cond: fails.append(msg)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags = []; self.refs = []; self.jsonld = []; self._ld = False; self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); self.tags.append((tag, a))
        if "id" in a: self.ids.add(a["id"])
        for k in ("href", "src", "srcset", "content"):
            if a.get(k): self.refs.append((tag, k, a[k]))
        self._ld = tag == "script" and a.get("type") == "application/ld+json"
    def handle_data(self, data):
        if self._ld and data.strip(): self.jsonld.append(data)
    def handle_endtag(self, tag):
        if tag == "script": self._ld = False

def meta(p, **kv):
    return [a for t, a in p.tags if t == "meta" and all(a.get(k) == v for k, v in kv.items())]

html = (ROOT / "index.html").read_text(encoding="utf-8")
p = Page(); p.feed(html)

# head / SEO
title = re.search(r"<title>(.*?)</title>", html, re.S)
check(title and "Krishna Nishad" in title.group(1) and len(title.group(1)) <= 60, "title missing name or > 60 chars")
desc = meta(p, name="description")
check(desc and 50 <= len(desc[0].get("content", "")) <= 155, "meta description missing or not 50-155 chars")
canon = [a for t, a in p.tags if t == "link" and a.get("rel") == "canonical"]
check(canon and canon[0].get("href") == ORIGIN + "/", "canonical must be " + ORIGIN + "/")
for prop in ("og:title", "og:description", "og:url", "og:image", "og:type"):
    check(meta(p, property=prop), f"missing {prop}")
check(meta(p, name="twitter:card", content="summary_large_image"), "missing twitter:card summary_large_image")
check(not meta(p, name="robots", content="noindex") and "noindex" not in html.lower(), "index.html must not be noindex")
check('lang="en"' in html[:200], 'html lang="en" missing')
check("GTM-5BB8W2X" in html, "GTM container missing")
check("UA-169007209" not in html, "dead UA tag still present")

# structured data
graph = []
for block in p.jsonld:
    try: data = json.loads(block); graph += data.get("@graph", [data])
    except json.JSONDecodeError as e: fails.append(f"JSON-LD does not parse: {e}")
person = next((n for n in graph if n.get("@type") == "Person"), None)
check(person and person.get("name") == "Krishna Nishad", "JSON-LD Person named Krishna Nishad missing")
if person:
    for k in ("jobTitle", "image", "sameAs", "worksFor", "alumniOf", "address", "url"):
        check(k in person, f"Person.{k} missing")
check(any(n.get("@type") == "ProfilePage" for n in graph), "JSON-LD ProfilePage missing")

# structure
check(sum(1 for t, _ in p.tags if t == "h1") == 1, "exactly one <h1> required")
for sec in ("about", "experience", "projects", "education", "skills", "contact"):
    check(sec in p.ids, f"section #{sec} missing")
for t, a in p.tags:
    if t == "img": check(a.get("alt") is not None, f"img without alt: {a.get('src')}")
    if t == "a" and (a.get("href") or "").startswith("#") and len(a["href"]) > 1:
        check(a["href"][1:] in p.ids, f"anchor target missing: {a['href']}")

# removed things stay removed
for gone in ("cyberpunk", "music-toggle", "assets/vendor", "bootstrap", "jquery", "style.css", "main.js", "typed.min.js"):
    check(gone not in html, f"removed reference still present: {gone}")

# every local reference resolves
def local(ref):
    u = urlparse(ref)
    return None if u.scheme or ref.startswith(("#", "//", "mailto:", "tel:", "data:")) else u.path
for t, k, v in p.refs:
    if k == "content" and not v.startswith(ORIGIN): continue
    for ref in ([s.strip().split(" ")[0] for s in v.split(",")] if k == "srcset" else [v]):
        path = urlparse(ref).path if ref.startswith(ORIGIN) else local(ref)
        if path and path != "/":
            check((ROOT / path.lstrip("/")).exists(), f"broken local reference: {ref}")

# robots + sitemap
robots = (ROOT / "robots.txt").read_text() if (ROOT / "robots.txt").exists() else ""
check("User-agent: *" in robots and f"Sitemap: {ORIGIN}/sitemap.xml" in robots, "robots.txt missing or lacks sitemap line")
check(not re.search(r"^Disallow:\s*/\s*$", robots, re.M), "robots.txt blocks the whole site")
try:
    locs = [e.text for e in ET.parse(ROOT / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    check(locs == [ORIGIN + "/"], f"sitemap locs should be [{ORIGIN}/], got {locs}")
except (FileNotFoundError, ET.ParseError) as e:
    fails.append(f"sitemap.xml invalid: {e}")

# leftovers deleted, kept page still there
for f in ("blog", "gan", "iras", "ml", "musicplayer", "recommender", "resume", "todo", "twitteranalysis", "vdg"):
    check(not (ROOT / "projects" / f"{f}.html").exists(), f"legacy page still present: projects/{f}.html")
check((ROOT / "projects/availclouds.html").exists(), "projects/availclouds.html must remain")
check((ROOT / "CNAME").read_text().strip() == "www.krishnanishad.com.np", "CNAME changed")

if fails:
    print("\n".join("FAIL: " + f for f in fails)); sys.exit(1)
print("OK")
```

- [ ] **Step 2: Run it and confirm it fails against the current site**

Run: `python tools/check_site.py`
Expected: exit 1 with many `FAIL:` lines, including `canonical must be…`, `JSON-LD Person… missing`, `removed reference still present: cyberpunk`, `robots.txt missing…` and `legacy page still present…`.

- [ ] **Step 3: Commit**

```bash
git add tools/check_site.py
git commit -m "test: add static site regression check"
```

---

### Task 2: Delete leftovers, add robots.txt and sitemap.xml

**Files:**
- Delete: `projects/{blog,gan,iras,ml,musicplayer,recommender,resume,todo,twitteranalysis,vdg}.html`, `assets/vendor/`, `assets/css/`, `assets/js/`, `assets/audio/`, `.DS_Store` files, `desktop.ini`
- Delete images used only by the deleted pages: `assets/img/project/{blog,ml,musicplayer,resume,todo,twitteranalysis,vdg,iras}.*`, `assets/img/background/`, `assets/img/education/`, and `assets/img/certification/{dai,ibm,ucsd}.jpg`. First check each with `grep -rl <name> index.html projects/availclouds.html`. Keep anything still referenced: `gan.jpg`, `recommender.jpg`, `availclouds.jpg`, `stanford.jpg`.
- Create: `robots.txt`, `sitemap.xml`

**Interfaces:**
- Consumes: `tools/check_site.py` (Task 1).
- Produces: a repo with no legacy pages; `robots.txt` and `sitemap.xml` at the root.

- [ ] **Step 1: Confirm nothing that stays references what's being deleted**

Run: `grep -nE "assets/(vendor|css|js|audio)|projects/(blog|gan|iras|ml|musicplayer|recommender|resume|todo|twitteranalysis|vdg)\.html" projects/availclouds.html`
Expected: no output. `index.html` still references them, but it is rewritten in Task 4.

- [ ] **Step 2: Delete**

```bash
git rm -r -q projects/blog.html projects/gan.html projects/iras.html projects/ml.html projects/musicplayer.html projects/recommender.html projects/resume.html projects/todo.html projects/twitteranalysis.html projects/vdg.html assets/vendor assets/css assets/js assets/audio
git rm -q --ignore-unmatch .DS_Store assets/.DS_Store assets/img/.DS_Store assets/img/project/.DS_Store desktop.ini
```

Then the legacy-only images, after the grep check above:

```bash
git rm -r -q assets/img/background assets/img/education assets/img/certification/dai.jpg assets/img/certification/ibm.jpg assets/img/certification/ucsd.jpg assets/img/project/blog.jpg assets/img/project/ml.jpg assets/img/project/musicplayer.jpg assets/img/project/resume.jpg assets/img/project/todo.jpg assets/img/project/twitteranalysis.jpg assets/img/project/vdg.jpg assets/img/project/iras.jpeg
```

- [ ] **Step 3: Create `robots.txt`**

```
User-agent: *
Allow: /

Sitemap: https://www.krishnanishad.com.np/sitemap.xml
```

- [ ] **Step 4: Create `sitemap.xml`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.krishnanishad.com.np/</loc>
    <lastmod>2026-10-09</lastmod>
  </url>
</urlset>
```

- [ ] **Step 5: Create `_config.yml` so dev files aren't published**

GitHub Pages runs Jekyll, which already skips dot-folders (`.impeccable/`, `.claude/`). This excludes the rest:

```yaml
exclude: [docs, tools, PRODUCT.md, DESIGN.md, README.md]
```

Do NOT add `.nojekyll`: it would publish the dot-folders.

- [ ] **Step 6: Run the check**

Run: `python tools/check_site.py`
Expected: still FAIL, but only `index.html`-related lines (canonical, JSON-LD, removed references, etc.). No `robots.txt`, `sitemap`, `legacy page` or `availclouds` failures.

- [ ] **Step 7: Commit**

```bash
git add robots.txt sitemap.xml _config.yml
git commit -m "chore: remove template leftovers, add robots.txt and sitemap"
```

---

### Task 3: Optimised images, share card, touch icon

**Files:**
- Create: `assets/img/krishna_profile.webp`, `assets/img/krishna_cutout.webp`, `assets/img/project/{availclouds,gan,recommender}.webp`, `assets/img/certification/stanford.webp`, `apple-touch-icon.png`, `tools/og-card.html`, `assets/img/og-card.png`
- Delete after conversion: `assets/img/me.jpg`, `assets/img/profile.jpeg` (unused by the new page; run `grep -rn "me.jpg\|profile.jpeg" index.html projects/availclouds.html` first and keep any file that still has a hit)

**Interfaces:**
- Produces: the WebP paths above (used by Task 4/5), `assets/img/og-card.png` (1200×630, used in `og:image`), `apple-touch-icon.png` (180×180).

- [ ] **Step 1: Convert to WebP with Pillow**

```bash
python -I - <<'EOF'
from PIL import Image
from pathlib import Path
jobs = {
 "assets/img/krishna_profile.png": (800, 85),
 "assets/img/krishna_cutout.png": (800, 90),   # keeps alpha; used only as the foil mask
 "assets/img/project/availclouds.jpg": (1280, 80),
 "assets/img/project/gan.jpg": (1270, 80),
 "assets/img/project/recommender.jpg": (1270, 80),
 "assets/img/certification/stanford.jpg": (800, 80),
}
for src, (w, q) in jobs.items():
    im = Image.open(src); im.thumbnail((w, w))
    out = Path(src).with_suffix(".webp"); im.save(out, "WEBP", quality=q, method=6)
    print(out, im.size, Path(src).stat().st_size // 1024, "KB ->", out.stat().st_size // 1024, "KB")
EOF
```

Expected: every `.webp` is smaller than its source.

- [ ] **Step 2: Touch icon from the favicon crest**

`apple-touch-icon.png` is a 180×180 kit-crimson square with the KN crest. Render it from `tools/og-card.html?icon` (Step 3) at `--window-size=180,180`.

- [ ] **Step 3: Share card source `tools/og-card.html`**

A 1200×630 page in the Home kit:
- the crimson field with the mesh weave;
- on the left, "KRISHNA NISHAD" in Anton with the drop shadow, then "Brand Identity Manager · Developer" and "krishnanishad.com.np" in Barlow Condensed;
- on the right, a flat (non-WebGL) rendering of the rookie card front: white stock, gold window border, `assets/img/krishna_profile.webp`, the black name plate with KRISHNA NISHAD, "NO. 21".

With `?icon`, render only the KN crest centred on crimson.

Reuse the CSS custom properties, crest SVG path and font stack from `.impeccable/mocks/decision/samples/kit-card.html` verbatim. Keep it under 120 lines.

- [ ] **Step 4: Render both with headless Chrome over http**

```bash
python -m http.server 8765 &   # from repo root, if not already running
P="$(cygpath -w "$PWD")"; C="/c/Program Files/Google/Chrome/Application/chrome.exe"
"$C" --headless=new --hide-scrollbars --window-size=1200,630 --virtual-time-budget=4000 --screenshot="$P\\assets\\img\\og-card.png" http://localhost:8765/tools/og-card.html
"$C" --headless=new --hide-scrollbars --window-size=500,500 --virtual-time-budget=4000 --screenshot="$P\\apple-touch-icon.png" "http://localhost:8765/tools/og-card.html?icon"
python -I -c "from PIL import Image; im=Image.open('apple-touch-icon.png').crop((0,0,180,180)); im.save('apple-touch-icon.png'); print(Image.open('assets/img/og-card.png').size)"
```

Headless Chrome won't go narrower than about 500px, so the icon is rendered at 500 and cropped. In `?icon` mode, the page must draw the 180×180 crest square at the top-left.

Expected: prints `(1200, 630)`. Open both PNGs with the Read tool and confirm the name is legible and nothing is clipped.

- [ ] **Step 5: Commit**

```bash
git add assets/img tools/og-card.html apple-touch-icon.png
git commit -m "feat: webp images, social share card, touch icon"
```

---

### Task 4: New `index.html`: head, content, layout, kit styling (no 3D yet)

**Files:**
- Rewrite: `index.html`
- Source to port from: `.impeccable/mocks/decision/samples/kit-card.html` (CSS custom properties, `[data-kit]` blocks, mesh weave, `.strip` nav, sleeve patch, hero, kit radio group, actions, `.record` fixture rows, crest SVG)

**Interfaces:**
- Consumes: Task 3 image paths; `tools/check_site.py`.
- Produces, for Task 5:
  - `<html lang="en" data-kit="home">`;
  - kit radios `input[name="kit"][value="home|away"]`;
  - the role element `#role`, with text set by JS;
  - `#card-stage` (an empty container where the canvas mounts) holding `#card-static`, a DOM fallback card shown until WebGL is ready;
  - the flip button `#flip` (`aria-pressed="false"`);
  - lede spans `.lede-home` and `.lede-away`, toggled by CSS via `[data-kit]`.

- [ ] **Step 1: Write `<head>`**

```html
<!doctype html>
<html lang="en" data-kit="home">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-5BB8W2X');</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Krishna Nishad · Developer & Brand Identity Manager</title>
<meta name="description" content="Krishna Nishad: developer and brand identity manager from Rupandehi, Nepal. Social Identity Manager at Availclouds; led a campaign that lifted engagement 447%.">
<link rel="canonical" href="https://www.krishnanishad.com.np/">
<meta name="theme-color" content="#C8102E">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Krishna Nishad">
<meta property="og:title" content="Krishna Nishad · Developer & Brand Identity Manager">
<meta property="og:description" content="Brand, social and code from Rupandehi, Nepal. Social Identity Manager & Dev at Availclouds.">
<meta property="og:url" content="https://www.krishnanishad.com.np/">
<meta property="og:image" content="https://www.krishnanishad.com.np/assets/img/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Krishna Nishad's rookie card on a crimson kit background">
<meta property="profile:first_name" content="Krishna">
<meta property="profile:last_name" content="Nishad">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Krishna Nishad · Developer & Brand Identity Manager">
<meta name="twitter:description" content="Brand, social and code from Rupandehi, Nepal.">
<meta name="twitter:image" content="https://www.krishnanishad.com.np/assets/img/og-card.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preload" as="image" href="/assets/img/krishna_profile.webp" type="image/webp">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap">
<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[
 {"@type":"Person","@id":"https://www.krishnanishad.com.np/#person","name":"Krishna Nishad","alternateName":"krimy",
  "url":"https://www.krishnanishad.com.np/","image":"https://www.krishnanishad.com.np/assets/img/krishna_profile.webp",
  "jobTitle":"Social Identity Manager & Developer","description":"Developer and brand identity manager from Rupandehi, Nepal.",
  "worksFor":{"@type":"Organization","name":"Availclouds Hosting Services"},
  "alumniOf":{"@type":"CollegeOrUniversity","name":"Tribhuvan University"},
  "address":{"@type":"PostalAddress","addressLocality":"Rupandehi","addressCountry":"NP"},
  "email":"mailto:krishna@availclouds.com","telephone":"+977-9864951223",
  "knowsAbout":["Brand identity","Social media management","Python","Unreal Engine 5","OpenCV","Android development","Graphic design","Video editing"],
  "sameAs":["https://www.linkedin.com/in/krishna-nishad/","https://github.com/krimy-7","https://www.instagram.com/krimy.7z/"]},
 {"@type":"WebSite","@id":"https://www.krishnanishad.com.np/#website","url":"https://www.krishnanishad.com.np/","name":"Krishna Nishad","inLanguage":"en"},
 {"@type":"ProfilePage","@id":"https://www.krishnanishad.com.np/#profile","url":"https://www.krishnanishad.com.np/","name":"Krishna Nishad · Developer & Brand Identity Manager",
  "isPartOf":{"@id":"https://www.krishnanishad.com.np/#website"},"mainEntity":{"@id":"https://www.krishnanishad.com.np/#person"},"dateModified":"2026-10-09"}
]}
</script>
<style>/* Step 2 */</style>
</head>
```

- [ ] **Step 2: CSS**

Port the `<style>` block from `kit-card.html`: tokens, the `[data-kit="away"]` overrides, weave, `.strip`, `.patch`, hero, `.kit` radio group, `.actions`, `.record`, and `.sr`.

Then add styles for the new sections using the same tokens and type roles:
- `.profile`: stat sheet;
- `.chips`: stitched patches;
- `.projects`: kit-coloured rookie-card tiles, laid out as an asymmetric grid (one large tile and two smaller ones, not three equal cards);
- `.academy`;
- `.attributes`: skills groups;
- `.fulltime`: contact.

Then:
- **Theme colour:** `[data-kit="away"]` doesn't change `<meta name=theme-color>` (CSS can't). Task 5's JS updates it.
- **Layout:** fluid with `clamp()`; the hero is two columns ≥ 900px and one column below.
- **Motion:** `@media (prefers-reduced-motion: reduce)` disables transitions and animations.
- **Focus:** a visible `:focus-visible` outline (3px, `var(--trim)`).

- [ ] **Step 3: Body markup, all content**

1. GTM `<noscript>` iframe directly after `<body>`.
2. Skip link `<a class="skip" href="#main">Skip to content</a>`.
3. `<header class="strip">` with the crest, "Krishna Nishad" as a link to `#main`, and a `<nav aria-label="Primary">` list:
   - About `#about`, Experience `#experience`, Projects `#projects`, Skills `#skills`, Contact `#contact`;
   - Resume → `https://drive.google.com/file/d/1W15wLaGuFef5gCKeO72DgxuK5pvEhblp/view?usp=sharing` with `target="_blank" rel="noopener"`.
4. `<main id="main">`, in this order:
   - **`<section class="hero" aria-labelledby="name">`:**
     - the patch "Now playing: <span id="role">Brand Identity Manager</span>";
     - `<h1 id="name"><span>Krishna</span> <span>Nishad</span></h1>`;
     - the lede: "Social Identity Manager | Dev at Availclouds Hosting Services." plus `<span class="lede-home">Home kit: brand identity, social campaigns, packaging and video, the work that took engagement up 447%.</span><span class="lede-away">Away kit: frontend UI and live tools, Python and OpenCV, Unreal Engine 5, Telegram bots.</span>`;
     - a `<fieldset class="kit">` with `<legend>Choose the kit</legend>` and two radios (`home` checked, `away`);
     - actions: See the work `#projects`, Write to me `mailto:krishna@availclouds.com`;
     - `<div id="card-stage">` holding `<div id="card-static">` (an `<img src="/assets/img/krishna_profile.webp" width="800" height="800" alt="Krishna Nishad smiling in sunglasses and a black shirt">` inside a CSS-drawn card frame with the name plate and "NO. 21"), followed by `<button id="flip" aria-pressed="false">Flip card</button>`;
     - a `.sr` card-back summary (copy from the sample).
   - **`<section id="about" class="profile">`, h2 "Player profile":**
     - the About paragraph verbatim from the current `index.html`;
     - a `<dl>` with Birthday 21 October, Phone `<a href="tel:+9779864951223">`, City Rupandehi, Nepal, Email mailto link;
     - Interests as a `<ul class="chips">` of the 8 items: Social Identity Management, Strategic Outreach, Brand Design, Content Creation, Software Development, UI/UX Design, Video Editing, Image Processing.
   - **`<section id="experience" class="record">`, h2 "Club career":** the three fixture rows from the sample, each with its bullet list verbatim from the current `index.html` in an `<ul>`. Use the dates from the current page: Oct. 2022 – Present, Feb. 2023, Jun. 2023 – Mar. 2024.
   - **`<section id="projects" class="projects">`, h2 "Dev fixtures":** three `<article>` tiles. Each has an image (webp, with `width`/`height`, `loading="lazy"` and alt), an `<h3>` and a link.
     - Availclouds MSP Help Desk: "Frontend UI & live tools", links to `projects/availclouds.html`.
     - Face Detection System: Python, OpenCV; links to the LinkedIn post URL copied verbatim from the current `index.html`.
     - Unreal Engine Game: Unreal Engine 5; links to its LinkedIn URL, likewise.
     - External links get `target="_blank" rel="noopener"`.
   - **`<section id="education" class="academy">`, h2 "Academy":**
     - Tribhuvan University, BSc. Computer Science & Information Technology, 2022 – Present, Bhairahawa Multiple Campus;
     - the three bullets verbatim;
     - the certificate patch "Game Theory · Stanford (Coursera)" → `https://coursera.org/share/1e8ab7c2e00713874c0bf5404fede8ff`, with the `stanford.webp` thumbnail.
   - **`<section id="skills" class="attributes">`, h2 "Squad attributes":** the five groups with `<h3>` headings and `<ul class="chips">`, items verbatim from the current `index.html`.
   - **`<section id="contact" class="fulltime">`, h2 "Full time":**
     - "Write to me" as a big mailto link;
     - the phone as a tel link;
     - "S.N.P.-08, Rupandehi, Nepal";
     - text links LinkedIn / GitHub / Instagram, each `rel="noopener me"`;
     - Resume (Drive).
5. `<footer>`: "© 2026 Krishna Nishad · Rupandehi, Nepal".

- [ ] **Step 4: Run the check**

Run: `python tools/check_site.py`
Expected: `OK`. Fix every `FAIL` before continuing.

- [ ] **Step 5: Visual check without JS**

Serve the site with `python -m http.server 8765`. Take a headless screenshot of `http://localhost:8765/` at 1440×900 and at full height, 1440×5000. Read both images. The page should be fully readable with the static card, in the Home kit, with no overlap.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "feat: rebuild index.html in the Home & Away kit design with SEO head"
```

---

### Task 5: Interactions: kit switch, typed roles, 3D rookie card

**Files:**
- Modify: `index.html` (add two scripts before `</body>`)
- Source to port from: `kit-card.html` lines ~170–320, covering the kit-switch script, the typed roles, and the importmap + module with the card textures, foil shader, sleeve, tilt/flip springs, and the holo-backdrop mask using `krishna_cutout`.

**Interfaces:**
- Consumes the Task 4 hooks: `html[data-kit]`, `input[name=kit]`, `#role`, `#card-stage`, `#card-static`, `#flip`, `meta[name=theme-color]`.
- Produces `window.setKit(kit, {animate})`, used by the radios and by `?kit=`. The module listens for `kitchange` (a `CustomEvent` on `document` with `detail.kit`) to repaint the card.

- [ ] **Step 1: Classic script: kit and roles (runs without the module)**

```html
<script>
(() => {
  const root = document.documentElement, roles = ["Brand Identity Manager", "Developer", "Twitch Streamer"];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches, theme = document.querySelector('meta[name="theme-color"]');
  const store = { get() { try { return localStorage.getItem("kit") } catch { return null } }, set(v) { try { localStorage.setItem("kit", v) } catch {} } };
  const roleEl = document.getElementById("role");
  let ri = 0, typing;
  function type(i) {                       // ponytail: simple typewriter, no library
    clearTimeout(typing); ri = i; const word = roles[i];
    if (reduce) { roleEl.textContent = word; typing = setTimeout(() => type((i + 1) % roles.length), 3000); return }
    let n = 0, back = false;
    (function step() {
      roleEl.textContent = word.slice(0, n);
      if (!back && n < word.length) n++; else if (!back) { back = true; return typing = setTimeout(step, 1800) }
      else if (n > 0) n--; else return type((ri + 1) % roles.length);
      typing = setTimeout(step, back ? 40 : 70);
    })();
  }
  window.setKit = (kit, { animate = true, from } = {}) => {
    if (kit !== "home" && kit !== "away") return;
    const apply = () => { root.dataset.kit = kit; theme.content = kit === "away" ? "#0B1F4B" : "#C8102E" };
    document.querySelector(`input[name=kit][value=${kit}]`).checked = true;
    store.set(kit); type(kit === "away" ? 1 : 0);
    if (animate && !reduce && document.startViewTransition) {
      const r = from?.getBoundingClientRect(); if (r) { root.style.setProperty("--rx", r.left + r.width / 2 + "px"); root.style.setProperty("--ry", r.top + r.height / 2 + "px") }
      document.startViewTransition(apply).finished.catch(() => {});
    } else apply();
    document.dispatchEvent(new CustomEvent("kitchange", { detail: { kit, animate: animate && !reduce } }));
  };
  document.querySelectorAll("input[name=kit]").forEach(r => r.addEventListener("change", () => setKit(r.value, { from: r.closest("label") })));
  const q = new URLSearchParams(location.search).get("kit");
  setKit(q || store.get() || "home", { animate: false });
})();
</script>
```

Add the ripple CSS to the Task 4 styles:

```css
::view-transition-new(root){animation:kit-in .6s cubic-bezier(.2,.7,.2,1)}
::view-transition-old(root){animation:none}
@keyframes kit-in{from{clip-path:circle(0 at var(--rx,50%) var(--ry,50%))}to{clip-path:circle(150vmax at var(--rx,50%) var(--ry,50%))}}
```

- [ ] **Step 2: Module: the 3D card**

Port the importmap and module from `kit-card.html`. Integrate it with the page as follows:

- **Mounting:** mount the renderer canvas into `#card-stage`. Hide `#card-static` only after the first successful `renderer.render`.
- **Fallback:** wrap renderer creation in `try/catch`. On failure, or when `!window.WebGLRenderingContext`, leave the static card visible and wire `#flip` to toggle a `.flipped` class on `#card-static`. The CSS back face shows the stats.
- **Image paths:** `/assets/img/krishna_profile.webp` and `/assets/img/krishna_cutout.webp`.
- **Kit changes:** replace the sample's own radio listener with `document.addEventListener("kitchange", e => …)`. On a kit change, repaint the textures, and when `detail.animate` is true, play the spin.
- **Flip button:** `#flip` toggles the flip and sets `aria-pressed`.
- **Rendering:** pause the render loop when the stage is off-screen (`IntersectionObserver`) or the tab is hidden. With reduced motion, render once per change and run no loop.
- **Load order:** keep the module at the end of `<body>` so it never blocks first paint.

- [ ] **Step 3: Run the check**

Run: `python tools/check_site.py`
Expected: `OK`.

- [ ] **Step 4: Behaviour checks in the browser pane** (`preview_start` name `site`, URL `http://localhost:8765/`)

Use `javascript_tool` and screenshots:

1. `document.documentElement.dataset.kit` is `"home"`. Click the Away label: the kit becomes `"away"`, `#role` starts typing "Developer", `meta[name=theme-color]` is `#0B1F4B`, and `localStorage.kit` is `"away"`. Reload: still away.
2. Click `#flip`: `aria-pressed` is `"true"`, and the screenshot shows the stats back.
3. `read_console_messages` with `onlyErrors`: none.
4. **No WebGL.** Take a headless screenshot with `--disable-webgl --disable-3d-apis` of `http://localhost:8765/`. Expected: the static card (photo, name plate, NO. 21) is visible in the card slot, and the hero copy and kit radios render normally.
5. **Reduced motion.** Take a headless screenshot with `--force-prefers-reduced-motion` and `--virtual-time-budget=1500`. Expected: `#role` shows the full word "Brand Identity Manager" (not a partial), and the card is drawn.
6. **localStorage blocked.** In the pane, run `Object.defineProperty(window, "localStorage", { get() { throw new Error("blocked") } })`, then call `setKit("away")`. Expected: no throw, and the kit changes.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: kit switch, typed roles, 3D holographic rookie card with fallbacks"
```

---

### Task 6: Responsive, audit, finish review, docs

**Files:**
- Modify: `index.html` (fixes only)
- Create: `DESIGN.md`, `.impeccable/design.json` (via the documenter)
- Write the direction contract with `impeccable surface-brief write index.html <file>` before the review.

**Interfaces:**
- Consumes everything above.

- [ ] **Step 1: Screenshots**

Capture the following into `.impeccable/review/`, over http, with headless Chrome:

| File | Size | URL |
|---|---|---|
| `desktop.png` | 1440×900 | `/` |
| `desktop-away.png` | 1440×900 | `/?kit=away` |
| `desktop-full.png` | 1440×6000 | `/` |
| `tablet.png` | 1024×768 | `/` |
| `mobile.png` | 390 wide | via an iframe wrapper page in the scratchpad (headless can't go narrower than about 500px) |

Read every file and confirm it shows what its name says.

- [ ] **Step 2: Responsive and accessibility pass**

At 390 in the browser pane (`resize_window` preset `mobile`), check:
- `document.documentElement.scrollWidth === 390`;
- `#flip` and the kit labels have a `getBoundingClientRect().height` of at least 44;
- the card sits under the hero copy.

Fix any failures in one batch, then recapture once.

- [ ] **Step 3: Detector**

Run `"C:/Users/Krishna/.claude/plugins/cache/impeccable/impeccable/4.5.0/skills/impeccable/scripts/impeccable" detect --json index.html` once. Fix the mechanical findings, and pass the rest to the reviewer.

- [ ] **Step 4: Finish review**

Spawn `impeccable:impeccable-finish-reviewer` fresh, with:
- the request and spec;
- the direction contract;
- the screenshot paths;
- the critique reference `.impeccable/mocks/decision/kit-card-holo-home.png` (the approved sample);
- the detector output;
- the craft-floor path.

Act on its disposition (ship, fix, rebuild or recapture). Allow at most two rounds.

- [ ] **Step 5: Documenter**

Spawn `impeccable:impeccable-documenter` with the project root, `index.html`, the direction contract, `PRODUCT.md` and the document.md path. Verify that `DESIGN.md` and `.impeccable/design.json` exist.

- [ ] **Step 6: Final check and commit**

Run: `python tools/check_site.py`. Expected: `OK`.

```bash
git add index.html DESIGN.md .impeccable/design.json
git commit -m "docs: design system record; polish from finish review"
```

- [ ] **Step 7: Hand the owner the launch steps**

Give the owner the Cloudflare and Search Console steps from the spec's "Owner actions" section, verbatim, with the order: push → Cloudflare HTTPS + apex redirect → Search Console verify + submit sitemap + request indexing → Bing import → profile links.

Don't push without the owner's go-ahead.
