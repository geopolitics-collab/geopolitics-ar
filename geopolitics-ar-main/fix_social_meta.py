#!/usr/bin/env python3
"""
Fix all social meta tags (OG + Twitter Cards) across 178 articles + index.html

Issues fixed:
1. index.html line 20: broken twitter:image tag (missing closing quote)
2. All articles: missing twitter:image, twitter:title, twitter:description
3. 22 articles: missing og:image → assign category fallback
4. 36 articles: empty canonical URL → reconstruct from filename
5. 11 articles: Unsplash without w/q params → add ?w=1200&q=80
6. Add og:image:width + og:image:height for Facebook
"""
import os, glob, re
from bs4 import BeautifulSoup

DIR      = "/workspaces/geopolitics-ar"
ARTICLES = os.path.join(DIR, "articles")
BASE_URL = "https://ar.geopolo.com"

# Category-based fallback Unsplash images (1200×630 ratio OK for OG)
CAT_IMAGES = {
    "afrique":  "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80",
    "amerique": "https://images.unsplash.com/photo-1485738422979-f5c462d49f74?w=1200&q=80",
    "europe":   "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=1200&q=80",
    "asie":     "https://images.unsplash.com/photo-1480796927426-f609979314bd?w=1200&q=80",
    "orient":   "https://images.unsplash.com/photo-1569949381669-ecf31ae8e613?w=1200&q=80",
    "default":  "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&q=80",
}

CAT_KEYWORDS = {
    "afrique":  ["afrique","africa","sahel","congo","nigeria","kenya","maroc","algerie","ethiopie","soudan","libye"],
    "amerique": ["amerique","usa","bresil","mexique","argentine","colombie","canada","panama","venezuela"],
    "europe":   ["europe","france","allemagne","ukraine","pologne","otan","finlande","hongrie","roumanie","eu","royaume","brexit","russie","odessa"],
    "asie":     ["asie","chine","japon","coree","inde","tsmc","samsung","taiwan","indonesia","mongolie","vietnam","philippines","biotech","ia-militaire","cyber","aukus","quad"],
    "orient":   ["iran","israel","arabie","liban","syrie","irak","yemen","qatar","golfe","oman","jordanie","palestine","egypte","proche","moyen-orient","hezbollah","hamas","idlib","bab-mandeb"],
}

def detect_cat(slug):
    slug = slug.lower()
    for cat, kws in CAT_KEYWORDS.items():
        if any(k in slug for k in kws):
            return cat
    return "default"

def fix_img_url(url):
    """Add Unsplash params if missing, ensure HTTPS."""
    if not url:
        return url
    if "unsplash.com" in url and "w=" not in url:
        sep = "&" if "?" in url else "?"
        url = url + sep + "w=1200&q=80"
    # Ensure HTTPS
    if url.startswith("http://"):
        url = "https://" + url[7:]
    return url

def build_social_meta(title, description, image_url, page_url, site_name="geopolô"):
    """Return dict of all required social meta tags."""
    # Cap lengths per platform requirements
    tw_title = title[:70] if len(title) > 70 else title
    tw_desc  = description[:200] if len(description) > 200 else description
    og_desc  = description[:300] if len(description) > 300 else description

    return {
        "og:title":            title,
        "og:description":      og_desc,
        "og:image":            image_url,
        "og:image:width":      "1200",
        "og:image:height":     "630",
        "og:image:alt":        title,
        "og:url":              page_url,
        "og:type":             "article",
        "og:locale":           "ar_AR",
        "og:site_name":        site_name,
        "twitter:card":        "summary_large_image",
        "twitter:title":       tw_title,
        "twitter:description": tw_desc,
        "twitter:image":       image_url,
        "twitter:site":        "@geopolo_ar",
    }

def inject_meta_tags(content, meta_dict):
    """Replace/add all social meta tags using string replacement (fast, safe)."""

    def set_property_meta(content, prop, value):
        # Replace existing
        pattern = rf'<meta\s+property="{re.escape(prop)}"\s+content="[^"]*"\s*/?>'
        replacement = f'<meta property="{prop}" content="{value}"/>'
        new, n = re.subn(pattern, replacement, content)
        if n:
            return new
        # Add after og:type or before </head>
        insert_after = '<meta property="og:type"'
        if insert_after in content:
            pos = content.find('>', content.find(insert_after)) + 1
            return content[:pos] + f'\n<meta property="{prop}" content="{value}"/>' + content[pos:]
        return content.replace('</head>', f'<meta property="{prop}" content="{value}"/>\n</head>', 1)

    def set_name_meta(content, name, value):
        pattern = rf'<meta\s+name="{re.escape(name)}"\s+content="[^"]*"\s*/?>'
        replacement = f'<meta name="{name}" content="{value}"/>'
        new, n = re.subn(pattern, replacement, content)
        if n:
            return new
        # Add after twitter:card or before </head>
        insert_after = '<meta name="twitter:card"'
        if insert_after in content:
            pos = content.find('>', content.find(insert_after)) + 1
            return content[:pos] + f'\n<meta name="{name}" content="{value}"/>' + content[pos:]
        return content.replace('</head>', f'<meta name="{name}" content="{value}"/>\n</head>', 1)

    for key, value in meta_dict.items():
        if key.startswith("twitter:"):
            content = set_name_meta(content, key, value)
        else:
            content = set_property_meta(content, key, value)

    return content

# ════════════════════════════════════════════════════════════
# FIX 0: index.html broken twitter:image + all other pages
# ════════════════════════════════════════════════════════════
def fix_index():
    fp = os.path.join(DIR, "index.html")
    with open(fp, encoding="utf-8") as f:
        content = f.read()

    # Critical fix: broken twitter:image tag (missing closing quote on line 20)
    # Pattern: content="URL/> without closing "
    broken = re.compile(r'<meta\s+name="twitter:image"\s+content="([^"]+)/>\s*\n\s*<link')
    def fix_broken(m):
        url = m.group(1).rstrip('/>')
        return f'<meta name="twitter:image" content="{url}"/>\n  <link'
    content = broken.sub(fix_broken, content)

    # Also fix any other unclosed twitter:image patterns (missing closing quote)
    content = re.sub(
        r'(<meta\s+name="twitter:image"\s+content="[^"<]+)([^"/])(\s*\n)',
        r'\1\2"/>\3',
        content
    )

    # Add og:image dimensions if missing
    if 'og:image:width' not in content:
        og_img = re.search(r'<meta property="og:image" content="([^"]+)"', content)
        if og_img:
            img_url = og_img.group(1)
            content = content.replace(
                og_img.group(0),
                og_img.group(0) +
                '\n  <meta property="og:image:width" content="1200"/>' +
                '\n  <meta property="og:image:height" content="630"/>' +
                f'\n  <meta property="og:image:alt" content="geopolô — تحليلات جيوسياسية"/>'
            )

    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✅ index.html — broken twitter:image fixed + og:image dimensions added")


# ════════════════════════════════════════════════════════════
# FIX ARTICLES
# ════════════════════════════════════════════════════════════
def fix_article(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if 'lang="ar"' not in content:
        return False, "not arabic"

    slug = os.path.basename(filepath).replace(".html", "")
    cat  = detect_cat(slug)
    changes = []

    # Parse for extracting values
    soup = BeautifulSoup(content, "html.parser")

    # ── Extract current values ──────────────────────────────────────
    og_title_tag = soup.find("meta", property="og:title")
    og_desc_tag  = soup.find("meta", property="og:description")
    og_img_tag   = soup.find("meta", property="og:image")
    canonical_tag= soup.find("link", rel="canonical")
    title_tag    = soup.title

    og_title = og_title_tag["content"].strip() if og_title_tag and og_title_tag.get("content") else (title_tag.string.strip() if title_tag else slug)
    og_desc  = og_desc_tag["content"].strip()  if og_desc_tag  and og_desc_tag.get("content")  else ""
    og_img   = og_img_tag["content"].strip()   if og_img_tag   and og_img_tag.get("content")   else ""
    canonical= canonical_tag["href"].strip()   if canonical_tag and canonical_tag.get("href")   else ""

    # ── Fix 1: empty og:image ───────────────────────────────────────
    if not og_img or og_img in ("", "https://ar.geopolo.com/og-default.jpg"):
        og_img = CAT_IMAGES[cat]
        changes.append("og:image-added")

    # ── Fix 2: Unsplash without params ─────────────────────────────
    if "unsplash.com" in og_img and "w=" not in og_img:
        og_img = fix_img_url(og_img)
        changes.append("img-params")

    # ── Fix 3: empty canonical ─────────────────────────────────────
    if not canonical:
        # Detect path: article or root
        if "/articles/" in filepath:
            canonical = f"{BASE_URL}/articles/{slug}.html"
        else:
            canonical = f"{BASE_URL}/{slug}.html"
        changes.append("canonical-fixed")

    # ── Fix 4: page URL ────────────────────────────────────────────
    if "/articles/" in filepath:
        page_url = f"{BASE_URL}/articles/{slug}.html"
    else:
        page_url = f"{BASE_URL}/{slug}.html"

    # ── Detect missing twitter tags BEFORE injection ───────────────
    if 'twitter:image' not in content:       changes.append("tw:image-added")
    if 'twitter:title' not in content:       changes.append("tw:title-added")
    if 'twitter:description' not in content: changes.append("tw:desc-added")
    if 'og:image:width' not in content:      changes.append("og:dims-added")
    if 'og:site_name' not in content:        changes.append("og:site-added")

    # ── Build complete social meta dict ────────────────────────────
    meta = build_social_meta(og_title, og_desc, og_img, page_url)

    # ── Apply fixes ────────────────────────────────────────────────
    # Fix og:image first (string replace for accuracy)
    old_og = og_img_tag["content"] if og_img_tag and og_img_tag.get("content") else None
    if old_og and old_og != og_img:
        content = content.replace(f'content="{old_og}"', f'content="{og_img}"', 1)
        changes.append("og:image-fixed")

    # Fix canonical
    if canonical_tag:
        old_can = canonical_tag.get("href", "")
        if old_can != canonical:
            content = content.replace(
                f'<link rel="canonical" href="{old_can}"',
                f'<link rel="canonical" href="{canonical}"'
            )
            if not old_can:
                changes.append("canonical-set")

    # Inject all twitter: and missing og: tags
    content = inject_meta_tags(content, meta)

    # Verify twitter:image is properly closed (guard against broken tags)
    content = re.sub(
        r'(<meta\s+name="twitter:image"\s+content="[^"]+)(?<!["/])(\s*\n)',
        r'\1"/>\2',
        content
    )

    if changes or 'twitter:image' not in content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True, ", ".join(changes) if changes else "tw-tags-added"
    return False, "already ok"


def main():
    print("═" * 60)
    print("  SOCIAL META FIX — OG + Twitter Cards")
    print("═" * 60 + "\n")

    # Fix index.html
    print("📄 index.html:")
    fix_index()

    # Fix all articles
    article_files = sorted(glob.glob(os.path.join(ARTICLES, "*.html")))
    print(f"\n📰 Articles ({len(article_files)} fichiers):")

    fixed = skipped = 0
    stats = {"og:image-added":0,"img-params":0,"canonical-fixed":0,"canonical-set":0,"og:image-fixed":0}

    for fp in article_files:
        ok, msg = fix_article(fp)
        if ok:
            fixed += 1
        else:
            skipped += 1
        # Count fix types
        for k in stats:
            if k in msg:
                stats[k] += 1

    print(f"\n  ✅ Fixed    : {fixed}")
    print(f"  — Skipped  : {skipped}")
    print(f"\n  Fix breakdown:")
    for k, v in stats.items():
        if v: print(f"    {k:25s}: {v}")

    # Verification
    print("\n🔍 Vérification post-fix:")
    missing_tw = []
    missing_og = []
    for fp in article_files:
        with open(fp, encoding="utf-8") as f:
            c = f.read()
        if 'twitter:image' not in c:
            missing_tw.append(os.path.basename(fp))
        soup = BeautifulSoup(c, "html.parser")
        og = soup.find("meta", property="og:image")
        if not og or not og.get("content"):
            missing_og.append(os.path.basename(fp))

    print(f"  Articles sans twitter:image : {len(missing_tw)}")
    print(f"  Articles sans og:image      : {len(missing_og)}")
    if missing_tw[:5]:
        print(f"  Exemples manquants: {missing_tw[:3]}")


if __name__ == "__main__":
    main()
