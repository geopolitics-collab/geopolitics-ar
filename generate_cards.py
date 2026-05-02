#!/usr/bin/env python3
"""Inject card grids into section pages — articles already exist on remote."""
import os, glob
from bs4 import BeautifulSoup

DIR      = "/workspaces/geopolitics-ar"
ARTICLES = os.path.join(DIR, "articles")

CARD_GRID_CSS = """
/* ── ARTICLE CARDS GRID v2 ── */
.article-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.2rem;margin:2rem 0}
.article-card{display:flex;flex-direction:column;background:#fff;border:1px solid #e8e4dc;overflow:hidden;transition:transform .22s cubic-bezier(.4,0,.2,1),box-shadow .22s cubic-bezier(.4,0,.2,1);text-decoration:none;color:inherit}
.article-card:hover{transform:translateY(-4px);box-shadow:0 8px 28px rgba(14,26,43,.1)}
.article-card__img-wrap{position:relative;height:0;padding-bottom:56.25%;overflow:hidden;background:#d0cfc8}
.article-card__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(.88);transition:filter .4s,transform .4s}
.article-card:hover .article-card__img{filter:saturate(1);transform:scale(1.04)}
.article-card__body{padding:1rem 1.1rem;flex:1;display:flex;flex-direction:column}
.article-card__tag{font-family:'Noto Naskh Arabic',sans-serif;font-size:.58rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#fff;padding:.18rem .55rem;border-radius:2px;display:inline-block;margin-bottom:.55rem;align-self:flex-start}
.article-card__title{font-family:'Noto Serif Arabic',Georgia,serif;font-size:.95rem;font-weight:700;line-height:1.4;color:#0A0C0E;margin-bottom:.5rem;flex:1}
.article-card__desc{font-family:'Noto Naskh Arabic',sans-serif;font-size:.78rem;color:#4A5568;line-height:1.6;margin-bottom:.8rem;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.article-card__footer{display:flex;justify-content:space-between;align-items:center;padding-top:.7rem;border-top:1px solid #EAE5D8}
.article-card__read{font-family:'Noto Naskh Arabic',sans-serif;font-size:.65rem;font-weight:700}
.article-card__time{font-family:'Noto Naskh Arabic',sans-serif;font-size:.62rem;color:#8A94A6}
.article-grid-header{display:flex;align-items:center;gap:.8rem;padding:.7rem 0;border-bottom:2px solid;margin-bottom:1.2rem}
.article-grid-header h2{font-family:'Noto Serif Arabic',Georgia,serif;font-size:1.1rem;font-weight:900;line-height:1}
.article-grid-header-line{flex:1;height:1px;background:#EAE5D8}
.article-grid-header a{font-family:'Noto Naskh Arabic',sans-serif;font-size:.65rem;font-weight:600;opacity:.8;transition:opacity .15s}
.article-grid-header a:hover{opacity:1}
@media(max-width:640px){.article-grid{grid-template-columns:1fr 1fr;gap:.8rem}}
@media(max-width:380px){.article-grid{grid-template-columns:1fr}}
"""

def get_article_meta(slug):
    fp = os.path.join(ARTICLES, f"{slug}.html")
    if not os.path.exists(fp):
        return None, None, None
    with open(fp, encoding="utf-8") as f: c = f.read()
    s = BeautifulSoup(c, "html.parser")
    og_t = s.find("meta", property="og:title")
    og_i = s.find("meta", property="og:image")
    og_d = s.find("meta", attrs={"name":"description"})
    title = og_t["content"] if og_t and og_t.get("content") else slug.replace("-"," ").title()
    img   = og_i["content"] if og_i and og_i.get("content") else "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=75"
    desc  = og_d["content"] if og_d and og_d.get("content") else ""
    return title, img, desc

def make_card(slug, color, tag_label):
    title, img, desc = get_article_meta(slug)
    if not title: return ""
    # Clean Unsplash URL
    if "unsplash.com" in img and "w=" not in img:
        img += "?w=600&q=75"
    elif "unsplash.com" in img:
        img = img.split("?")[0] + "?w=600&q=75"
    return f'''<a href="/articles/{slug}.html" class="article-card">
  <div class="article-card__img-wrap">
    <img class="article-card__img" src="{img}" alt="{title}" loading="lazy"/>
  </div>
  <div class="article-card__body">
    <span class="article-card__tag" style="background:{color}">{tag_label}</span>
    <h3 class="article-card__title">{title}</h3>
    <p class="article-card__desc">{desc[:120]}</p>
    <div class="article-card__footer">
      <span class="article-card__read" style="color:{color}">اقرأ التحليل ←</span>
      <span class="article-card__time">⏱ 8 دقائق</span>
    </div>
  </div>
</a>'''

def make_section_grid(sec_id, title_ar, color, page_url, slugs, tag_label):
    cards = "\n".join([make_card(s, color, tag_label) for s in slugs])
    return f'''
<section id="grid-{sec_id}" style="margin:3rem 0 2rem;max-width:1200px;margin-left:auto;margin-right:auto;padding:0 1.5rem">
  <div class="article-grid-header" style="border-color:{color};color:{color}">
    <h2 style="color:{color}">{title_ar}</h2>
    <div class="article-grid-header-line"></div>
    <a href="{page_url}" style="color:{color}">جميع المقالات ←</a>
  </div>
  <div class="article-grid">{cards}</div>
</section>'''

SECTIONS = [
    ("voyage",   "/voyage.html",    "#0891b2", "السفر والسياحة", "سفر",
     ["arabie-saoudite-tourisme-strategie-politique-2026",
      "bien-etre-wellness-moyen-orient-industrie-strategique",
      "deconnexion-digitale-desert-elites-mondiales",
      "dubai-capitale-mondiale-luxe-tourisme-2026",
      "expatries-golfe-qualite-vie-moyen-orient",
      "hammam-medecine-naturelle-traditions-moderne",
      "iles-secretes-resorts-mer-rouge-2026",
      "oman-secret-moyen-orient-tourisme-2026",
      "qatar-doha-tourisme-influence-soft-power-2026",
      "top-10-destinations-luxe-moyen-orient-2026",
      "tourisme-spirituel-modernite-traditions-moyen-orient",
      "voyager-moyen-orient-2026-visa-securite-cout",
      "voyage-aeroports-geopolitique","voyage-tourisme-geopolitique",
      "voyage-zones-tensions-conseils","destinations-incontournables-2026"]),
    ("sante",    "/sante.html",     "#2a9d5c", "الصحة والمجتمع", "صحة",
     ["ai-anxiety-tech-2026","burnout-wazifi-2026","inflation-stress-2026",
      "smartphone-addiction-2026","wars-mental-health-2026",
      "alimentation-securite-geopolitique","pandemie-prochaine-preparation-mondiale",
      "sante-mentale-guerre-conflit-monde","sante-mondiale-geopolitique-2026",
      "systemes-sante-pays-emergents"]),
    ("asie_ame", "/asie.html",      "#1a8a6e", "آسيا وأمريكا", "آسيا",
     ["japon-armement-pologne-philippines-2026","usa-blocus-maritime-iran-petrole-2026",
      "usa-iran-tanker-chinois-hormuz-2026","usa-japon-vente-armes-trump-allies-2026",
      "etats-unis-leadership-ou-repli","sun-tzu-strategies-indirectes-guerre-hybride"]),
    ("orient",   "/proche-or.html", "#8b3a8b", "الشرق الأوسط", "شرق أوسط",
     ["moyen-orient-iran-arabie-rivalite-structurante","afrique-nouvelle-grande-competition",
      "chine-taiwan-expansion-silencieuse","cyberguerre-front-invisible",
      "energie-petrole-gaz-armes-geopolitiques","guerre-du-futur-drones-ia-hypersonique",
      "nouvel-ordre-mondial-monde-multipolaire","strategies-maritimes-detroits-routes",
      "arabie-saoudite-golfe-securite","emirats-strategie-autonomie-securite",
      "iran-menaces-ponts-golfe-arabie-koweit-emirats","iran-nuclear-gulf-war-risk",
      "koweit-neutralite-strategique-iran-guerre"]),
    ("europe",   "/eu.html",        "#1e5fa8", "أوروبا", "أوروبا",
     ["ukraine-otan-guerre-mondiale-procuration","corps-controle-mobilisation-civile-europe",
      "crise-energetique-asie-dependance","etats-controle-populations-crise",
      "frontieres-biologiques-serpents-crocodiles","guerre-hybride-2026-tout-devient-arme",
      "guerre-hybride-europe-menaces-invisibles","guerre-hybride-faune-vivant",
      "iran-ormuz-guerre-energetique-mondiale","militarisation-energie-petrole-arme",
      "militarisation-frontieres-asie-sud","militarisation-vivant-guerre-futur",
      "monde-deux-energies-asie-chaos","moyen-orient-bord-escalade-totale",
      "orques-securite-maritime-europe","sebastopol-dauphins-mer-noire"]),
]

PAGE_MAP = {
    "voyage":   "voyage.html",
    "sante":    "sante.html",
    "asie_ame": "asie.html",
    "orient":   "proche-or.html",
    "europe":   "eu.html",
}

for sec_id, page_url, color, title_ar, tag_label, slugs in SECTIONS:
    page_file = PAGE_MAP[sec_id]
    fp = os.path.join(DIR, page_file)
    if not os.path.exists(fp):
        print(f"  ⚠️  {page_file} not found"); continue
    
    with open(fp, encoding="utf-8") as f: content = f.read()
    
    changed = False
    if "article-grid" not in content and "</style>" in content:
        content = content.replace("</style>", CARD_GRID_CSS + "\n</style>", 1)
        changed = True
    
    if f"id=\"grid-{sec_id}\"" not in content:
        grid = make_section_grid(sec_id, title_ar, color, page_url, slugs, tag_label)
        for anchor in ["</main>", "<footer", "</body>"]:
            if anchor in content:
                content = content.replace(anchor, grid + "\n" + anchor, 1)
                changed = True
                break
    
    if changed:
        with open(fp, "w", encoding="utf-8") as f: f.write(content)
        print(f"  ✅ {page_file} — {len(slugs)} cards injected")
    else:
        print(f"  — {page_file} already up to date")

print("Done.")
