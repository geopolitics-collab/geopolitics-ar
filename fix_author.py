#!/usr/bin/env python3
"""Replace generic GeoPolo author box with Nasser AL SABRI's photo card."""
import os, glob, re

DIR      = "/workspaces/geopolitics-ar"
ARTICLES = os.path.join(DIR, "articles")

PHOTO = "https://pub-a7b1a75f72ab40548a0709f708ca2678.r2.dev/geopolo.jpg"

AUTHOR_CSS = """
/* ── AUTHOR CARD v2 ── */
.author-card-v2{margin:2.5rem 0;display:flex;gap:1.5rem;align-items:flex-start;background:var(--surface,#fff);border:1px solid var(--rule,#ddd9d0);border-right:4px solid var(--brand,#0f4c81);padding:1.5rem;position:relative;overflow:hidden}
.author-card-v2::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--brand,#0f4c81),var(--accent,#c8920a),var(--brand,#0f4c81));background-size:200% 100%;animation:shimmer 3s infinite linear}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
.author-photo{width:88px;height:88px;border-radius:50%;object-fit:cover;object-position:top center;flex-shrink:0;border:3px solid var(--brand,#0f4c81);box-shadow:0 4px 16px rgba(15,76,129,.2)}
.author-info{flex:1;min-width:0}
.author-name-v2{font-family:var(--serif,'Noto Serif Arabic',serif);font-size:1.05rem;font-weight:900;color:var(--ink,#12131a);margin-bottom:.15rem;line-height:1.2}
.author-title-v2{font-family:var(--sans,'Noto Naskh Arabic',sans-serif);font-size:.68rem;font-weight:600;color:var(--brand,#0f4c81);letter-spacing:.04em;text-transform:uppercase;margin-bottom:.55rem}
.author-bio-v2{font-family:var(--sans,'Noto Naskh Arabic',sans-serif);font-size:.85rem;color:var(--ink-3,#5a5c72);line-height:1.7;margin-bottom:.8rem}
.author-links{display:flex;gap:.5rem;flex-wrap:wrap}
.author-link{display:inline-flex;align-items:center;gap:.3rem;font-family:var(--sans,'Noto Naskh Arabic',sans-serif);font-size:.65rem;font-weight:600;padding:.28rem .7rem;border:1px solid currentColor;border-radius:2px;transition:background .2s,color .2s;text-decoration:none}
.author-link.x-link{color:#000}.author-link.x-link:hover{background:#000;color:#fff}
.author-link.site-link{color:var(--brand,#0f4c81)}.author-link.site-link:hover{background:var(--brand,#0f4c81);color:#fff}
@media(max-width:480px){.author-card-v2{flex-direction:column;align-items:center;text-align:center}.author-links{justify-content:center}}
"""

NEW_AUTHOR_HTML = f"""<div class="author-card-v2">
  <img class="author-photo" src="{PHOTO}" alt="ناصر الصبري — محلل جيوسياسي" loading="lazy"/>
  <div class="author-info">
    <div class="author-name-v2">ناصر الصبري</div>
    <div class="author-title-v2">محلل جيوسياسي · مؤسس GeoPolo</div>
    <p class="author-bio-v2">محلل في الجيوسياسة والاستراتيجية الدولية. يتابع ملفات الشرق الأوسط وآسيا والقوى الكبرى. مؤسس مجلة GeoPolo للتحليلات الاستراتيجية المستقلة.</p>
    <div class="author-links">
      <a class="author-link x-link" href="https://x.com/geopolo_ar" target="_blank" rel="noopener">𝕏 Twitter</a>
      <a class="author-link site-link" href="https://ar.geopolo.com" target="_blank" rel="noopener">🌐 GeoPolo</a>
    </div>
  </div>
</div>"""

# Patterns to detect and replace old author boxes
OLD_AU_PATTERNS = [
    # Pattern 1: full .au div with Geo Polo avatar
    re.compile(r'<div class="au">.*?</div>\s*</div>', re.DOTALL),
    # Pattern 2: .author-card variant
    re.compile(r'<div class="author-card">.*?</div>\s*</div>', re.DOTALL),
]

def fix_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if 'lang="ar"' not in content:
        return False, "skip"

    changed = []

    # 1. Add CSS if not present
    if "author-card-v2" not in content and "</style>" in content:
        content = content.replace("</style>", AUTHOR_CSS + "\n</style>", 1)
        changed.append("css")

    # 2. Replace old author box — try exact known patterns first
    replacements = [
        # Pattern from apply_template_v2.py output
        ('<div class="au"><div class="av" style="font-size:.72rem;letter-spacing:-.03em">Geo<br/>Polo</div>',
         None),  # Will be handled below
    ]

    # Find and replace .au block
    au_pattern = re.compile(
        r'<div class="au">.*?</div>\s*</div>(?=\s*(?:</article>|</div>|<div class="rel|<div class="nl-cta|<script))',
        re.DOTALL
    )
    if au_pattern.search(content):
        content = au_pattern.sub(NEW_AUTHOR_HTML, content, count=1)
        changed.append("author-replaced")

    # Also fix pages that have old .au without article wrapper
    if "author-card-v2" not in content and 'class="au"' in content:
        # More aggressive: find .au to end of its enclosing block
        au_simple = re.compile(r'<div class="au">[\s\S]{20,600}?</div>\s*</div>', re.DOTALL)
        m = au_simple.search(content)
        if m:
            content = content[:m.start()] + NEW_AUTHOR_HTML + content[m.end():]
            changed.append("author-replaced-v2")

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return bool(changed), ", ".join(changed)


def main():
    files = sorted(glob.glob(os.path.join(ARTICLES, "*.html")))
    print(f"🎨 Redesign carte auteur — {len(files)} articles\n")
    fixed = skipped = err = 0

    for fp in files:
        try:
            ok, msg = fix_file(fp)
            if ok:
                fixed += 1
                print(f"  ✅ {os.path.basename(fp)}")
            else:
                skipped += 1
        except Exception as e:
            err += 1
            print(f"  ❌ {os.path.basename(fp)}: {e}")

    print(f"\n✅ {fixed} fixés | — {skipped} ignorés | ❌ {err} erreurs")

    # Verify
    sample = files[:3]
    print("\n🔍 Vérification:")
    for fp in sample:
        with open(fp, encoding="utf-8") as f: c = f.read()
        has_photo  = PHOTO in c
        has_name   = "ناصر الصبري" in c
        has_card   = "author-card-v2" in c
        has_old_au = 'class="av"' in c
        print(f"  {os.path.basename(fp)}: photo={has_photo} nom={has_name} card={has_card} old={has_old_au}")


if __name__ == "__main__":
    main()
