#!/usr/bin/env python3
"""Phase 2 SEO — révision fichier par fichier (174 articles):
  1. Titre <title> raccourci à 65 car max (Google tronque au-delà)
  2. Meta description corrigée à 120-155 car
  3. Maillage interne : injection de 4 liens contextuels par article
  4. Fix liens relatifs dans .rel section (ajout /articles/)
  5. Fix alt manquants/mauvais sur images
  6. Rapport final avec liste des articles thin content à traiter manuellement
"""

import os, re, glob, unicodedata
from bs4 import BeautifulSoup

ARTICLES_DIR = "/workspaces/geopolitics-ar/articles"

# ─── Détection de catégorie ───────────────────────────────────────────────────
CAT_KEYWORDS = {
    "afrique":  ["afrique","africa","sahel","congo","nigeria","kenya","maroc","algerie","ethiopie","mali","soudan","libye","ghana","senegal","tunisie","egypte","afr"],
    "amerique": ["amerique","usa","etats-unis","bresil","mexique","venezuela","colombie","argentine","canada","panama","ame"],
    "europe":   ["europe","france","allemagne","ukraine","pologne","otan","finlande","hongrie","roumanie","royaume-uni","eu"],
    "asie":     ["asie","chine","japon","coree","inde","tsmc","samsung","asean","mongolie","indonesie","taiwan","pakistan","afghanistan","biotech","aukus","quad"],
    "orient":   ["iran","israel","arabie","liban","syrie","irak","yemen","qatar","golfe","proche","oman","jordanie","palestine","hamas","hezbollah","idlib","bab-mandeb","egypte-canal","egypte-vs"],
}

def detect_cat(soup, filepath):
    a = soup.find("a", class_="active")
    if a and a.get("data-r"):
        return a["data-r"]
    fn = os.path.basename(filepath).lower()
    for cat, kws in CAT_KEYWORDS.items():
        if any(k in fn for k in kws):
            return cat
    return "default"

# ─── Catalogue de tous les articles ───────────────────────────────────────────
def build_catalog():
    catalog = {}  # basename → {title, cat, url}
    for fp in sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.html"))):
        with open(fp, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        og = soup.find("meta", property="og:title")
        title_tag = soup.title
        title = og["content"] if og else (title_tag.string if title_tag else os.path.basename(fp))
        # Remove trailing site name
        title = re.sub(r"\s*[—\-–|·]\s*(تحليلات جيوسياسية|geopolô)\s*$", "", title).strip()
        cat = detect_cat(soup, fp)
        catalog[os.path.basename(fp)] = {"title": title, "cat": cat, "file": fp}
    return catalog

# ─── Raccourcir le <title> à 65 car ──────────────────────────────────────────
def shorten_title(raw, limit=65):
    """Strip site suffix, then truncate at word boundary."""
    t = re.sub(r"\s*[—\-–|·]\s*(تحليلات جيوسياسية|geopolô)\s*$", "", raw).strip()
    if len(t) <= limit:
        return t
    # Truncate at last space before limit
    t = t[:limit].rsplit(" ", 1)[0].rstrip("،,:") + "…"
    return t

# ─── Corriger la meta description ─────────────────────────────────────────────
def fix_desc(text, lo=120, hi=155):
    if not text:
        return text
    if len(text) <= hi:
        return text
    # Truncate at last word before hi
    return text[:hi].rsplit(" ", 1)[0].rstrip("،,:") + "..."

# ─── Construire le bloc .also avec 4 liens ────────────────────────────────────
def build_also(current_file, catalog, cat, n=4):
    candidates = [
        (bn, info) for bn, info in catalog.items()
        if bn != current_file and info["cat"] == cat
    ]
    # Fallback to default if not enough
    if len(candidates) < n:
        candidates += [
            (bn, info) for bn, info in catalog.items()
            if bn != current_file and info["cat"] != cat
        ]
    selected = candidates[:n]
    items = ""
    for bn, info in selected:
        href = f"/articles/{bn}"
        items += f'<li><a href="{href}">{info["title"]}</a></li>\n'
    return (
        '<div class="also">\n'
        '<h4>📚 اقرأ أيضاً</h4>\n'
        '<ul>\n' + items + '</ul>\n'
        '</div>\n'
    )

# ─── Fix liens relatifs dans .rel ────────────────────────────────────────────
def fix_rel_links(content):
    """In .rel section, fix href="article.html" → href="/articles/article.html"."""
    def replacer(m):
        href = m.group(1)
        if href.startswith("/") or href.startswith("http"):
            return m.group(0)
        if href.endswith(".html") and "/" not in href:
            return f'href="/articles/{href}"'
        return m.group(0)

    # Only within rel section
    def fix_section(sec_match):
        sec = sec_match.group(0)
        sec = re.sub(r'href="([^"]+)"', replacer, sec)
        return sec

    return re.sub(
        r'<div class="rel">.*?</div>\s*</article>',
        fix_section,
        content,
        flags=re.DOTALL
    )

# ─── Traitement principal d'un fichier ────────────────────────────────────────
def fix_file(filepath, catalog):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    basename = os.path.basename(filepath)
    cat = detect_cat(soup, filepath)
    changes = []

    # 1. Fix <title>
    title_tag = soup.title
    if title_tag and title_tag.string:
        short = shorten_title(title_tag.string)
        if short != title_tag.string:
            content = content.replace(
                f"<title>{title_tag.string}</title>",
                f"<title>{short}</title>",
                1
            )
            changes.append("title")

    # 2. Fix meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        fixed_desc = fix_desc(meta_desc["content"])
        if fixed_desc != meta_desc["content"]:
            content = content.replace(
                f'content="{meta_desc["content"]}"',
                f'content="{fixed_desc}"',
                1
            )
            changes.append("desc")

    # 3. Maillage interne — ajouter/remplacer bloc .also
    re_soup = BeautifulSoup(content, "html.parser")
    also_block = re_soup.find(class_="also")
    new_also = build_also(basename, catalog, cat, n=4)

    if also_block:
        # Replace existing .also
        old_also_str = str(also_block)
        if old_also_str in content:
            content = content.replace(old_also_str, new_also, 1)
            changes.append("also-updated")
    else:
        # Insert before .au (author box) or before </article>
        if '<div class="au">' in content:
            content = content.replace('<div class="au">', new_also + '<div class="au">', 1)
        elif '</article>' in content:
            content = content.replace('</article>', new_also + '</article>', 1)
        changes.append("also-added")

    # 4. Fix liens relatifs dans .rel
    fixed_rel = fix_rel_links(content)
    if fixed_rel != content:
        content = fixed_rel
        changes.append("rel-links")

    # 5. Fix alt mauvais sur images (alt="military" ou alt="mil")
    content = re.sub(r'alt="(military|mil)"', 'alt="صورة ذات صلة"', content)
    if 'alt=""' in content:
        content = content.replace('alt=""', 'alt="صورة"')
        changes.append("alt-fix")

    # 6. Vérifier H1 manquant (log seulement)
    h1s = re_soup.find_all("h1")
    if not h1s:
        changes.append("⚠ H1-manquant")

    if changes:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return changes

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    files = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.html")))
    print(f"📂 Construction du catalogue ({len(files)} articles)...")
    catalog = build_catalog()
    print(f"   ✅ Catalogue prêt — catégories: { {c: sum(1 for v in catalog.values() if v['cat']==c) for c in ['afrique','amerique','europe','asie','orient','default']} }")

    print(f"\n🔧 Traitement fichier par fichier...")
    total_changes = {"title": 0, "desc": 0, "also-added": 0, "also-updated": 0, "rel-links": 0, "alt-fix": 0}
    thin_content = []
    no_h1 = []
    errors = []

    for i, fp in enumerate(files, 1):
        try:
            with open(fp, encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            body = soup.find("article") or soup.find(class_="body")
            words = len(body.get_text(" ", strip=True).split()) if body else 0
            if words < 300:
                thin_content.append((os.path.basename(fp), words))

            changes = fix_file(fp, catalog)
            for k in total_changes:
                if k in changes:
                    total_changes[k] += 1
            if "⚠ H1-manquant" in changes:
                no_h1.append(os.path.basename(fp))

            tag = " | ".join(c for c in changes if not c.startswith("⚠")) or "—"
            print(f"  [{i:03d}/{len(files)}] {os.path.basename(fp):55s} {tag}")
        except Exception as e:
            errors.append((os.path.basename(fp), str(e)))
            print(f"  ❌ [{i:03d}/{len(files)}] {os.path.basename(fp)} — {e}")

    print(f"""
╔══════════════════════════════════════════════════════╗
║               PHASE 2 — RÉSULTATS                   ║
╠══════════════════════════════════════════════════════╣
║  ✅ Titres raccourcis          : {total_changes['title']:>4}                 ║
║  ✅ Descriptions corrigées     : {total_changes['desc']:>4}                 ║
║  ✅ Blocs also ajoutés         : {total_changes['also-added']:>4}                 ║
║  ✅ Blocs also mis à jour      : {total_changes['also-updated']:>4}                 ║
║  ✅ Liens .rel corrigés        : {total_changes['rel-links']:>4}                 ║
║  ✅ Alt images fixés           : {total_changes['alt-fix']:>4}                 ║
║  ❌ Erreurs                    : {len(errors):>4}                 ║
╚══════════════════════════════════════════════════════╝""")

    if thin_content:
        print(f"\n⚠️  {len(thin_content)} articles thin content (< 300 mots) — à enrichir manuellement:")
        for fn, w in sorted(thin_content, key=lambda x: x[1])[:15]:
            print(f"   {fn:55s} {w:>4} mots")

    if no_h1:
        print(f"\n⚠️  {len(no_h1)} articles sans H1:")
        for fn in no_h1:
            print(f"   {fn}")

    if errors:
        print(f"\n❌ Erreurs:")
        for fn, err in errors:
            print(f"   {fn}: {err}")

if __name__ == "__main__":
    main()
