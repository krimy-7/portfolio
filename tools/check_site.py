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
