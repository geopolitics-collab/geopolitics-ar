#!/usr/bin/env python3
"""Phase 1 SEO fix — all 174 articles:
- Add JSON-LD NewsArticle structured data
- Replace military sidebar images with category-relevant ones
- Add og:locale + twitter:card meta tags
- Update sitemap <lastmod>
"""

import os
import re
import glob
from datetime import date
from bs4 import BeautifulSoup, Comment

ARTICLES_DIR = "/workspaces/geopolitics-ar/articles"
SITEMAP_PATH = "/workspaces/geopolitics-ar/sitemap.xml"
TODAY = date.today().isoformat()  # 2026-04-29

# Category-based Unsplash images (4 per category, topic-relevant)
CATEGORY_IMAGES = {
    "afrique": [
        ("https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=400&q=60", "أفريقيا وطبيعتها"),
        ("https://images.unsplash.com/photo-1489392191049-fc10c97e64b6?w=400&q=60", "مدينة أفريقية"),
        ("https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&q=60", "اجتماع أفريقي"),
        ("https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&q=60", "علم أفريقيا"),
    ],
    "amerique": [
        ("https://images.unsplash.com/photo-1485738422979-f5c462d49f74?w=400&q=60", "الأمريكتان"),
        ("https://images.unsplash.com/photo-1534430480872-3498386e7856?w=400&q=60", "واشنطن"),
        ("https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400&q=60", "أمريكا اللاتينية"),
        ("https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400&q=60", "الولايات المتحدة"),
    ],
    "europe": [
        ("https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=400&q=60", "أوروبا"),
        ("https://images.unsplash.com/photo-1491557345352-5929e343eb89?w=400&q=60", "برلين"),
        ("https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=400&q=60", "باريس"),
        ("https://images.unsplash.com/photo-1529539795054-3c162981d2de?w=400&q=60", "بروكسل"),
    ],
    "asie": [
        ("https://images.unsplash.com/photo-1480796927426-f609979314bd?w=400&q=60", "آسيا"),
        ("https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=60", "تكنولوجيا آسيا"),
        ("https://images.unsplash.com/photo-1536599018102-9f803c140fc1?w=400&q=60", "طوكيو"),
        ("https://images.unsplash.com/photo-1513415431021-b6a01a3e75b2?w=400&q=60", "شنغهاي"),
    ],
    "orient": [
        ("https://images.unsplash.com/photo-1569949381669-ecf31ae8e613?w=400&q=60", "الشرق الأوسط"),
        ("https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=400&q=60", "بغداد"),
        ("https://images.unsplash.com/photo-1586105449897-20b5efeb3233?w=400&q=60", "دبي"),
        ("https://images.unsplash.com/photo-1548686373-89e060871440?w=400&q=60", "القدس"),
    ],
    "default": [
        ("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&q=60", "جيوسياسة"),
        ("https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&q=60", "علاقات دولية"),
        ("https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=400&q=60", "تحليل استراتيجي"),
        ("https://images.unsplash.com/photo-1516738901171-8eb4fc13bd20?w=400&q=60", "خريطة العالم"),
    ],
}

# Military image patterns to detect and replace
MILITARY_SIDEBAR_PATTERNS = [
    r'<div class="sbl"><div class="stl">🎖 صور ميدانية</div><div class="pimgs">.*?</div></div>',
]

def detect_category(soup, filename):
    """Detect article category from active nav link or filename."""
    # Check active nav link
    active = soup.find("a", class_="active")
    if active and active.get("data-r"):
        return active["data-r"]
    # Fallback: detect from filename
    fn = os.path.basename(filename).lower()
    if any(k in fn for k in ["afrique", "africa", "sahel", "congo", "nigeria", "kenya", "maroc", "algerie", "ethiopie", "mali", "afr"]):
        return "afrique"
    if any(k in fn for k in ["amerique", "usa", "etats-unis", "bresil", "mexique", "venezuela", "colombie", "ame"]):
        return "amerique"
    if any(k in fn for k in ["europe", "france", "allemagne", "ukraine", "pologne", "otan", "eu"]):
        return "europe"
    if any(k in fn for k in ["asie", "chine", "japon", "coree", "inde", "tsmc", "samsung", "asean"]):
        return "asie"
    if any(k in fn for k in ["iran", "israel", "arabie", "liban", "syrie", "irak", "yemen", "qatar", "golfe", "orient", "proche", "oman", "jordanie", "palestine", "hamas", "hezbollah"]):
        return "orient"
    return "default"

def build_jsonld(title, description, image_url, canonical_url):
    """Build a NewsArticle JSON-LD block."""
    title_clean = title.replace('"', '\\"')
    desc_clean = description.replace('"', '\\"') if description else ""
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{title_clean}",
  "description": "{desc_clean}",
  "image": "{image_url}",
  "url": "{canonical_url}",
  "datePublished": "{TODAY}",
  "dateModified": "{TODAY}",
  "author": {{
    "@type": "Organization",
    "name": "geopolô",
    "url": "https://ar.geopolo.com"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "geopolô",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://ar.geopolo.com/favicon.ico"
    }}
  }},
  "inLanguage": "ar",
  "isAccessibleForFree": true
}}
</script>'''

def build_sidebar_images(category):
    """Build correct sidebar image block for category."""
    imgs = CATEGORY_IMAGES.get(category, CATEGORY_IMAGES["default"])
    imgs_html = "".join(
        f'<img src="{url}?w=400&q=60" alt="{alt}" loading="lazy"/>'
        if "?" not in url else
        f'<img src="{url}" alt="{alt}" loading="lazy"/>'
        for url, alt in imgs
    )
    return f'<div class="sbl"><div class="stl">🖼 صور ذات صلة</div><div class="pimgs">{imgs_html}</div></div>'

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    changed = False

    # --- 1. Add JSON-LD if missing ---
    if not soup.find("script", {"type": "application/ld+json"}):
        og_title = soup.find("meta", property="og:title")
        meta_desc = soup.find("meta", attrs={"name": "description"})
        og_image = soup.find("meta", property="og:image")
        canonical = soup.find("link", rel="canonical")

        title = og_title["content"] if og_title else (soup.title.string if soup.title else "geopolô")
        description = meta_desc["content"] if meta_desc else ""
        image_url = og_image["content"] if og_image else "https://ar.geopolo.com/og-default.jpg"
        url = canonical["href"] if canonical else f"https://ar.geopolo.com/{os.path.basename(filepath)}"

        jsonld = build_jsonld(title, description, image_url, url)
        # Insert before </head>
        content = content.replace("</head>", jsonld + "\n</head>", 1)
        changed = True

    # --- 2. Add og:locale if missing ---
    if not soup.find("meta", property="og:locale"):
        og_type = soup.find("meta", property="og:type")
        locale_tag = '<meta property="og:locale" content="ar_AR"/>'
        if og_type:
            content = content.replace(
                str(og_type),
                str(og_type) + "\n" + locale_tag,
                1
            )
        else:
            content = content.replace("</head>", locale_tag + "\n</head>", 1)
        changed = True

    # --- 3. Add twitter:card if missing ---
    if not soup.find("meta", attrs={"name": "twitter:card"}):
        twitter_tags = (
            '<meta name="twitter:card" content="summary_large_image"/>\n'
            '<meta name="twitter:site" content="@geopolo_ar"/>'
        )
        og_image_tag = soup.find("meta", property="og:image")
        if og_image_tag:
            content = content.replace(
                str(og_image_tag),
                str(og_image_tag) + "\n" + twitter_tags,
                1
            )
        else:
            content = content.replace("</head>", twitter_tags + "\n</head>", 1)
        changed = True

    # Re-parse after string replacements to detect category properly
    soup2 = BeautifulSoup(content, "html.parser")
    category = detect_category(soup2, filepath)

    # --- 4. Replace military sidebar images ---
    military_patterns = [
        # Pattern with alt="military"
        r'(<div class="sbl"><div class="stl">🎖 صور ميدانية</div><div class="pimgs">).*?(</div></div>)',
        # Pattern with alt="mil"
        r'(<div class="sbl"><div class="stl">🎖 صور ميدانية</div><div class="pimgs">).*?(</div></div>)',
    ]

    military_block_re = re.compile(
        r'<div class="sbl"><div class="stl">🎖 صور ميدانية</div><div class="pimgs">.*?</div></div>',
        re.DOTALL
    )

    if military_block_re.search(content):
        new_block = build_sidebar_images(category)
        content = military_block_re.sub(new_block, content)
        changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def update_sitemap():
    """Add <lastmod> to all sitemap entries that don't have one."""
    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Add lastmod after <loc>...</loc> if not present
    def add_lastmod(m):
        url_block = m.group(0)
        if "<lastmod>" not in url_block:
            url_block = url_block.replace("</loc>", f"</loc><lastmod>{TODAY}</lastmod>")
        return url_block

    new_content = re.sub(r"<url>.*?</url>", add_lastmod, content, flags=re.DOTALL)

    if new_content != content:
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def main():
    files = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.html")))
    print(f"📂 {len(files)} fichiers à traiter...")

    fixed = 0
    skipped = 0
    errors = []

    for i, fp in enumerate(files, 1):
        try:
            result = fix_file(fp)
            if result:
                fixed += 1
                print(f"  ✅ [{i:03d}/{len(files)}] {os.path.basename(fp)}")
            else:
                skipped += 1
                print(f"  — [{i:03d}/{len(files)}] {os.path.basename(fp)} (déjà correct)")
        except Exception as e:
            errors.append((fp, str(e)))
            print(f"  ❌ [{i:03d}/{len(files)}] {os.path.basename(fp)} — ERREUR: {e}")

    print(f"\n📊 Résultats:")
    print(f"  ✅ Corrigés  : {fixed}")
    print(f"  — Ignorés   : {skipped}")
    print(f"  ❌ Erreurs   : {len(errors)}")

    if update_sitemap():
        print(f"  🗺  Sitemap mis à jour avec <lastmod>{TODAY}</lastmod>")

    if errors:
        print("\n⚠️  Fichiers en erreur:")
        for fp, err in errors:
            print(f"  {os.path.basename(fp)}: {err}")

if __name__ == "__main__":
    main()
