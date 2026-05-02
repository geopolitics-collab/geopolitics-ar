#!/usr/bin/env python3
"""
Fix all tasks:
1. Fix eu.html (broken links, structure)
2. Create abonnement.html
3. Replace PoloGeo → Geopolo everywhere
4. Add 12 social share buttons to all articles
5. Redesign tags (kwb/kw) and Also section
"""
import os, glob, re

DIR      = "/workspaces/geopolitics-ar"
ARTICLES = os.path.join(DIR, "articles")

# ═══════════════════════════════════════════════════════════════
# TASK 3-4: Replace PoloGeo everywhere
# ═══════════════════════════════════════════════════════════════
def fix_pologeo(content):
    replacements = [
        ("PoloGeo", "Geopolo"), ("polo.geo", "geopolo"),
        ("Polo Geo", "Geopolo"), ("polo geo", "geopolo"),
        ("POLO GEO", "GEOPOLO"), ("GeoPolo", "Geopolo"),
    ]
    for old, new in replacements:
        content = content.replace(old, new)
    return content

# ═══════════════════════════════════════════════════════════════
# TASK 5: New 12-platform share bar HTML + JS
# ═══════════════════════════════════════════════════════════════
SHARE_CSS = """
/* ── SHARE BAR v2 — 12 platforms ── */
.share-bar-v2{background:var(--paper-2,#f3f0e8);border-top:1px solid var(--rule,#e2ddd8);border-bottom:1px solid var(--rule,#e2ddd8);padding:.6rem 1.5rem}
.share-bar-v2 .share-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:.4rem;flex-wrap:wrap}
.share-bar-v2 .share-label{font-family:var(--sans,'Noto Naskh Arabic',sans-serif);font-size:.6rem;color:var(--ink-3,#5a5870);margin-left:.3rem;white-space:nowrap}
.sbtn{display:inline-flex;align-items:center;gap:.25rem;padding:.28rem .6rem;font-family:var(--sans,'Noto Naskh Arabic',sans-serif);font-size:.6rem;font-weight:700;cursor:pointer;border:none;transition:opacity .15s,transform .15s;white-space:nowrap}
.sbtn:hover{opacity:.88;transform:translateY(-1px)}.sbtn:active{transform:translateY(0)}
.sb-x{background:#000;color:#fff}
.sb-wa{background:#25d366;color:#fff}
.sb-fb{background:#1877f2;color:#fff}
.sb-tg{background:#2ca5e0;color:#fff}
.sb-li{background:#0a66c2;color:#fff}
.sb-rd{background:#ff4500;color:#fff}
.sb-bk{background:#0085ff;color:#fff}
.sb-em{background:#5a5870;color:#fff}
.sb-ms{background:#0078ff;color:#fff}
.sb-tt{background:#010101;color:#fff}
.sb-sc{background:#fffc00;color:#000}
.sb-sg{background:#3a76f0;color:#fff}
.sb-cp{background:#2e3040;color:#fff}
@media(max-width:640px){.share-bar-v2{padding:.5rem 1rem}.sbtn{font-size:.55rem;padding:.22rem .5rem}}
"""

SHARE_HTML = """<div class="share-bar-v2">
  <div class="share-inner">
    <span class="share-label">شارك:</span>
    <button class="sbtn sb-x"  onclick="shr('x')"  title="X / Twitter">𝕏</button>
    <button class="sbtn sb-wa" onclick="shr('wa')" title="WhatsApp">WhatsApp</button>
    <button class="sbtn sb-fb" onclick="shr('fb')" title="Facebook">Facebook</button>
    <button class="sbtn sb-tg" onclick="shr('tg')" title="Telegram">Telegram</button>
    <button class="sbtn sb-li" onclick="shr('li')" title="LinkedIn">LinkedIn</button>
    <button class="sbtn sb-rd" onclick="shr('rd')" title="Reddit">Reddit</button>
    <button class="sbtn sb-bk" onclick="shr('bk')" title="Bluesky">Bluesky</button>
    <button class="sbtn sb-ms" onclick="shr('ms')" title="Messenger">Messenger</button>
    <button class="sbtn sb-tt" onclick="shr('tt')" title="TikTok">TikTok</button>
    <button class="sbtn sb-sc" onclick="shr('sc')" title="Snapchat">Snapchat</button>
    <button class="sbtn sb-sg" onclick="shr('sg')" title="Signal">Signal</button>
    <button class="sbtn sb-em" onclick="shr('em')" title="Email">Email</button>
    <button class="sbtn sb-cp" onclick="shr('cp')" title="نسخ الرابط">🔗 نسخ</button>
  </div>
</div>"""

SHARE_JS = """
function shr(p){
  var u=encodeURIComponent(location.href);
  var t=encodeURIComponent(document.title);
  var urls={
    x:'https://twitter.com/intent/tweet?url='+u+'&text='+t,
    wa:'https://wa.me/?text='+t+'%20'+u,
    fb:'https://www.facebook.com/sharer/sharer.php?u='+u,
    tg:'https://t.me/share/url?url='+u+'&text='+t,
    li:'https://www.linkedin.com/shareArticle?mini=true&url='+u+'&title='+t,
    rd:'https://reddit.com/submit?url='+u+'&title='+t,
    bk:'https://bsky.app/intent/compose?text='+t+'%20'+decodeURIComponent(u),
    ms:'https://www.facebook.com/dialog/send?link='+u+'&app_id=291494419107518&redirect_uri='+u,
    tt:'https://www.tiktok.com/share?url='+u,
    sc:'https://www.snapchat.com/share?url='+u,
    sg:'https://signal.me/#p/'+u,
    em:'mailto:?subject='+t+'&body='+u
  };
  if(p==='cp'){
    navigator.clipboard.writeText(location.href).then(function(){
      var b=document.querySelector('.sb-cp');
      if(b){var o=b.textContent;b.textContent='✓ تم';setTimeout(function(){b.textContent=o;},1500);}
    });
    return;
  }
  if(p==='sg'&&navigator.share){navigator.share({title:document.title,url:location.href});return;}
  if(urls[p])window.open(urls[p],'_blank','width=600,height=500,noopener');
}
"""

# ═══════════════════════════════════════════════════════════════
# TASK 6: Redesigned Tags + Also section CSS
# ═══════════════════════════════════════════════════════════════
DESIGN_UPGRADE_CSS = """
/* ── TAGS (kwb/kw) REDESIGN ── */
.kwb{background:linear-gradient(135deg,var(--paper-2,#f3f0e8) 0%,var(--cream,#f3f0e8) 100%);border:1px solid var(--rule,#e2ddd8);border-right:3px solid var(--nav-accent,var(--brand,#0f4c81));padding:.75rem 1.1rem;margin-bottom:2rem;display:flex;flex-wrap:wrap;gap:.4rem .35rem;align-items:center;border-radius:0 4px 4px 0}
.kwl{font-family:var(--sans);font-size:.6rem;font-weight:800;color:var(--nav-accent,var(--brand,#0f4c81));margin-left:.6rem;letter-spacing:.1em;text-transform:uppercase;flex-shrink:0}
.kw{font-family:var(--sans);font-size:.62rem;font-weight:600;padding:.22rem .65rem;border:1px solid var(--rule,#e2ddd8);background:var(--surface,#fff);color:var(--ink-3,#5a5870);border-radius:20px;transition:background .15s,color .15s,border-color .15s;cursor:default;letter-spacing:.01em}
.kw:hover{background:var(--nav-accent,var(--brand,#0f4c81));color:#fff;border-color:var(--nav-accent,var(--brand,#0f4c81))}

/* ── ALSO / اقرأ أيضاً REDESIGN ── */
.also{margin:2.5rem 0;background:var(--surface,#fff);border:1px solid var(--rule,#e2ddd8);overflow:hidden;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.also h4{font-family:var(--sans);font-size:.65rem;font-weight:800;color:#fff;background:var(--nav-accent,var(--brand,#0f4c81));padding:.6rem 1.2rem;margin:0;letter-spacing:.1em;text-transform:uppercase;display:flex;align-items:center;gap:.5rem}
.also h4::before{content:'📚';font-size:.9rem}
.also ul{list-style:none;padding:.3rem 0;margin:0}
.also li{border-bottom:1px solid var(--rule,#e2ddd8);transition:background .15s}
.also li:last-child{border:none}
.also li:hover{background:var(--paper-2,#f3f0e8)}
.also a{font-family:var(--serif);font-size:.92rem;font-weight:600;color:var(--nav-accent,var(--brand,#0f4c81));display:flex;justify-content:space-between;align-items:center;padding:.7rem 1.2rem;transition:color .15s}
.also a:hover{color:var(--accent,#c8920a)}
.also a::before{content:'←';font-size:.75rem;opacity:.5;margin-right:auto;margin-left:.5rem;transition:opacity .15s,transform .15s}
.also a:hover::before{opacity:1;transform:translateX(-3px)}
"""

# ═══════════════════════════════════════════════════════════════
# APPLY TO ARTICLES
# ═══════════════════════════════════════════════════════════════
def update_article(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if 'lang="ar"' not in content:
        return False

    changes = []

    # Fix PoloGeo
    new = fix_pologeo(content)
    if new != content:
        content = new
        changes.append("pologeo")

    # Add share CSS
    if "share-bar-v2" not in content and "</style>" in content:
        content = content.replace("</style>", SHARE_CSS + "\n</style>", 1)
        changes.append("share-css")

    # Add design upgrade CSS (tags + also)
    if "kwb/kw) REDESIGN" not in content and "</style>" in content:
        content = content.replace("</style>", DESIGN_UPGRADE_CSS + "\n</style>", 1)
        changes.append("design-css")

    # Replace old share-bar with new v2 (remove old, add new)
    old_share_re = re.compile(
        r'<div class="share-bar">.*?</div>\s*</div>',
        re.DOTALL
    )
    if old_share_re.search(content):
        content = old_share_re.sub(SHARE_HTML, content, count=1)
        changes.append("share-html")
    elif "share-bar-v2" not in content and "<div class=\"meta-bar\">" in content:
        # Insert after meta-bar
        content = content.replace(
            '</div>\n<div class="page-layout">',
            f'</div>\n{SHARE_HTML}\n<div class="page-layout">',
            1
        )
        changes.append("share-inserted")

    # Add/replace share JS function
    if "function shr(" not in content:
        if "function shareX()" in content:
            # Remove old share functions and replace
            old_js_re = re.compile(
                r'function shareX\(\).*?function copyLink\(\)\{[^}]+\}',
                re.DOTALL
            )
            content = old_js_re.sub(SHARE_JS.strip(), content)
        elif "</script>" in content:
            content = content.replace("</script>", SHARE_JS + "\n</script>", 1)
        changes.append("share-js")

    if changes:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return bool(changes)

# ═══════════════════════════════════════════════════════════════
# FIX eu.html
# ═══════════════════════════════════════════════════════════════
def fix_eu_html():
    fp = os.path.join(DIR, "eu.html")
    with open(fp, encoding="utf-8") as f:
        content = f.read()

    # Fix PoloGeo
    content = fix_pologeo(content)

    # Add share CSS + design CSS if missing
    if "share-bar-v2" not in content and "</style>" in content:
        content = content.replace("</style>", SHARE_CSS + DESIGN_UPGRADE_CSS + "\n</style>", 1)

    # Fix broken article links (ensure /articles/ prefix)
    content = re.sub(
        r'href="([a-z][a-z0-9-]+\.html)"(?!\s*class)',
        lambda m: f'href="/articles/{m.group(1)}"' if not m.group(1).startswith(('index','eu','afr','ame','proche','asie','newsletter','abonnement','magazine','culture','voyage','sante','opinion')) else m.group(0),
        content
    )

    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✅ eu.html fixed")

# ═══════════════════════════════════════════════════════════════
# CREATE abonnement.html
# ═══════════════════════════════════════════════════════════════
def create_abonnement():
    html = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>الاشتراك المميز — Geopolo · تحليلات جيوسياسية</title>
<meta name="description" content="اشترك في Geopolo للحصول على تحليلات جيوسياسية معمّقة وحصرية — النشرة الأسبوعية مجاناً."/>
<meta property="og:title" content="الاشتراك المميز — Geopolo"/>
<meta property="og:image" content="https://pub-a7b1a75f72ab40548a0709f708ca2678.r2.dev/le-monde.png"/>
<meta property="og:type" content="website"/>
<meta property="og:locale" content="ar_AR"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="canonical" href="https://ar.geopolo.com/abonnement.html"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Arabic:wght@400;700;900&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap" rel="stylesheet"/>
<style>
:root{--navy:#0E1A2B;--gold:#C4952A;--gold-l:#FBF3DC;--paper:#F9F7F2;--ink:#0A0C0E;--ink-2:#1E2630;--ink-3:#4A5568;--rule:#EAE5D8;--serif:'Noto Serif Arabic',Georgia,serif;--sans:'Noto Naskh Arabic',sans-serif;--danger:#b83232}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);background:var(--paper);color:var(--ink-2);direction:rtl;line-height:1.8;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}

/* TOPBAR */
.topbar{background:var(--navy);color:rgba(255,255,255,.5);font-size:.65rem;padding:.35rem 1.5rem;display:flex;justify-content:space-between}
.topbar a{color:rgba(255,255,255,.55);transition:color .2s}.topbar a:hover{color:var(--gold)}

/* HEADER */
.site-header{background:#fff;border-bottom:2px solid var(--navy);padding:.9rem 1.5rem;display:flex;justify-content:space-between;align-items:center}
.logo{font-family:var(--serif);font-size:1.7rem;font-weight:900;color:var(--navy);letter-spacing:-.02em}
.logo em{font-style:normal;color:var(--gold)}
.logo-sub{font-family:var(--sans);font-size:.55rem;color:var(--ink-3);letter-spacing:.14em;text-transform:uppercase;margin-top:.1rem}

/* NAV */
.site-nav{background:var(--navy);border-bottom:3px solid var(--gold);position:sticky;top:0;z-index:200;overflow-x:auto}
.nav-inner{display:flex;min-width:max-content}
.nav-inner a{display:flex;align-items:center;gap:.35rem;padding:.65rem 1rem;font-family:var(--sans);font-size:.76rem;color:#9a96b4;border-left:1px solid #252535;transition:background .15s,color .15s;white-space:nowrap}
.nav-inner a:hover,.nav-inner a.active{background:#14213a;color:var(--gold)}
.nav-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.nav-sub{margin-right:auto}.nav-sub a{background:var(--danger);color:#fff;font-weight:700;border:none}

/* HERO */
.sub-hero{background:linear-gradient(135deg,var(--navy) 0%,#1E2F45 60%,#263B54 100%);padding:4rem 2rem;text-align:center;position:relative;overflow:hidden}
.sub-hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at 60% 40%,rgba(196,149,42,.12),transparent 60%);pointer-events:none}
.sub-hero-badge{display:inline-block;font-family:var(--sans);font-size:.58rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);border:1px solid rgba(196,149,42,.4);padding:.25rem .8rem;margin-bottom:1.2rem}
.sub-hero h1{font-family:var(--serif);font-size:clamp(1.8rem,4vw,3rem);font-weight:900;color:#fff;line-height:1.15;margin-bottom:1rem}
.sub-hero h1 em{font-style:normal;color:var(--gold)}
.sub-hero p{font-family:var(--sans);font-size:1rem;color:rgba(255,255,255,.65);max-width:560px;margin:0 auto 2rem;line-height:1.75}

/* FREE CTA */
.free-cta{display:inline-flex;flex-direction:column;align-items:center;gap:.4rem;background:var(--gold);color:var(--navy);font-family:var(--sans);padding:1rem 2.5rem;transition:background .2s;cursor:pointer;border:none;font-size:.88rem;font-weight:700}
.free-cta:hover{background:#D4AA4A}
.free-cta small{font-size:.62rem;font-weight:400;opacity:.75}

/* MAIN LAYOUT */
.sub-main{max-width:1100px;margin:0 auto;padding:3rem 1.5rem}

/* PLANS */
.plans{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.5rem;margin-bottom:3rem}
.plan{background:#fff;border:1px solid var(--rule);padding:2rem;position:relative;transition:transform .2s,box-shadow .2s}
.plan:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(14,26,43,.08)}
.plan.featured{border:2px solid var(--gold);border-top:4px solid var(--gold)}
.plan-badge{position:absolute;top:-1px;right:2rem;background:var(--gold);color:var(--navy);font-family:var(--sans);font-size:.58rem;font-weight:800;padding:.2rem .7rem;letter-spacing:.1em;text-transform:uppercase}
.plan-name{font-family:var(--serif);font-size:1.3rem;font-weight:900;color:var(--ink);margin-bottom:.3rem}
.plan-price{font-family:var(--serif);font-size:2.5rem;font-weight:900;color:var(--navy);line-height:1;margin:.8rem 0}
.plan-price small{font-size:.75rem;font-weight:400;color:var(--ink-3)}
.plan-desc{font-family:var(--sans);font-size:.82rem;color:var(--ink-3);line-height:1.65;margin-bottom:1.2rem}
.plan-features{list-style:none;margin-bottom:1.5rem}
.plan-features li{font-family:var(--sans);font-size:.82rem;color:var(--ink-2);padding:.45rem 0;border-bottom:1px solid var(--rule);display:flex;gap:.5rem;align-items:flex-start}
.plan-features li:last-child{border:none}
.plan-features li::before{content:'✓';color:var(--gold);font-weight:800;flex-shrink:0}
.plan-btn{display:block;width:100%;padding:.7rem;text-align:center;font-family:var(--sans);font-size:.82rem;font-weight:700;cursor:pointer;border:none;transition:background .2s}
.plan-btn-primary{background:var(--navy);color:#fff}.plan-btn-primary:hover{background:#1E2F45}
.plan-btn-secondary{background:transparent;color:var(--navy);border:1.5px solid var(--navy)}.plan-btn-secondary:hover{background:var(--navy);color:#fff}

/* FREE SECTION */
.free-section{background:var(--navy);color:#fff;padding:2.5rem;margin-bottom:3rem;text-align:center;position:relative;overflow:hidden}
.free-section::before{content:'';position:absolute;top:-50%;right:-20%;width:300px;height:300px;background:radial-gradient(circle,rgba(196,149,42,.1),transparent);pointer-events:none}
.free-section h2{font-family:var(--serif);font-size:1.6rem;font-weight:900;margin-bottom:.5rem}
.free-section h2 em{font-style:normal;color:var(--gold)}
.free-section p{font-family:var(--sans);font-size:.88rem;color:rgba(255,255,255,.6);margin-bottom:1.5rem;max-width:480px;margin-left:auto;margin-right:auto}
.nl-form-ab{display:flex;gap:.5rem;max-width:440px;margin:0 auto;flex-direction:row-reverse}
.nl-form-ab input{flex:1;padding:.7rem 1rem;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);color:#fff;font-family:var(--sans);font-size:.85rem;text-align:right;outline:none}
.nl-form-ab input:focus{border-color:var(--gold)}
.nl-form-ab input::placeholder{color:rgba(255,255,255,.35)}
.nl-form-ab button{padding:.7rem 1.3rem;background:var(--gold);color:var(--navy);border:none;font-family:var(--sans);font-size:.82rem;font-weight:700;cursor:pointer}
.nl-form-ab button:hover{background:#D4AA4A}
.nl-msg-ab{margin-top:.6rem;font-family:var(--sans);font-size:.8rem;min-height:1.2rem}
.nl-note-ab{font-family:var(--sans);font-size:.6rem;color:rgba(255,255,255,.35);margin-top:.6rem}

/* BENEFITS */
.benefits{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem;margin-bottom:3rem}
.benefit{background:#fff;border:1px solid var(--rule);padding:1.3rem;text-align:center}
.benefit-icon{font-size:1.8rem;margin-bottom:.6rem}
.benefit-title{font-family:var(--serif);font-size:.92rem;font-weight:700;color:var(--ink);margin-bottom:.3rem}
.benefit-text{font-family:var(--sans);font-size:.78rem;color:var(--ink-3);line-height:1.6}

/* FAQ */
.faq-ab{margin-bottom:3rem}
.faq-ab h2{font-family:var(--serif);font-size:1.3rem;font-weight:800;color:var(--ink);border-bottom:2px solid var(--navy);padding-bottom:.5rem;margin-bottom:1rem}
.faq-item-ab{border-bottom:1px solid var(--rule);padding:.8rem 0}
.faq-item-ab:last-child{border:none}
.faq-q-ab{font-family:var(--serif);font-size:.95rem;font-weight:700;color:var(--ink);cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:.8rem}
.faq-q-ab::after{content:'+';font-size:1.2rem;font-weight:400;color:var(--gold);flex-shrink:0;transition:transform .2s}
.faq-q-ab.open::after{transform:rotate(45deg)}
.faq-a-ab{font-family:var(--sans);font-size:.85rem;color:var(--ink-3);line-height:1.7;max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s}
.faq-a-ab.open{max-height:200px;padding-top:.5rem}

/* RESPONSIVE */
@media(max-width:640px){.plans{grid-template-columns:1fr}.nl-form-ab{flex-direction:column}.sub-hero{padding:2.5rem 1rem}}
</style>
</head>
<body>
<div class="topbar">
  <span>Geopolo · تحليلات جيوسياسية استراتيجية مستقلة</span>
  <span><a href="https://geopolo.com">🇫🇷 Français</a> · <a href="/">الرئيسية</a></span>
</div>
<header class="site-header">
  <div>
    <div class="logo">geo<em>polô</em></div>
    <div class="logo-sub">مجلة جيوسياسية مستقلة · ar.geopolo.com</div>
  </div>
</header>
<nav class="site-nav"><div class="nav-inner">
  <a href="/">الرئيسية</a>
  <a href="/proche-or.html"><span class="nav-dot" style="background:#B84A0C"></span>الشرق الأوسط</a>
  <a href="/eu.html"><span class="nav-dot" style="background:#1A4E8C"></span>أوروبا</a>
  <a href="/afr.html"><span class="nav-dot" style="background:#A0461A"></span>أفريقيا</a>
  <a href="/asie.html"><span class="nav-dot" style="background:#0B6B5A"></span>آسيا</a>
  <div class="nav-sub"><a href="/abonnement.html">الاشتراك ←</a></div>
</div></nav>

<!-- HERO -->
<section class="sub-hero">
  <div class="sub-hero-badge">الاشتراك المميز</div>
  <h1>تحليلات جيوسياسية<br><em>معمّقة وحصرية</em></h1>
  <p>انضم إلى آلاف القراء الذين يثقون بـGeopolo لفهم العالم — النشرة الأسبوعية مجاناً، والتحليلات الحصرية للمشتركين.</p>
  <button class="free-cta" onclick="document.getElementById('free-nl').scrollIntoView({behavior:'smooth'})">
    اشترك في النشرة مجاناً
    <small>بدون بطاقة ائتمانية · بدون إلزام</small>
  </button>
</section>

<div class="sub-main">

  <!-- PLANS -->
  <div class="plans">
    <div class="plan">
      <div class="plan-name">مجاني</div>
      <div class="plan-price">٠<small> ر.س / شهر</small></div>
      <p class="plan-desc">الوصول إلى جميع المقالات المنشورة والنشرة الأسبوعية.</p>
      <ul class="plan-features">
        <li>جميع المقالات العامة</li>
        <li>النشرة الأسبوعية</li>
        <li>أرشيف المقالات العامة</li>
      </ul>
      <button class="plan-btn plan-btn-secondary" onclick="document.getElementById('free-nl').scrollIntoView({behavior:'smooth'})">ابدأ مجاناً</button>
    </div>
    <div class="plan featured">
      <span class="plan-badge">الأكثر شيوعاً</span>
      <div class="plan-name">مميز شهري</div>
      <div class="plan-price">٤٩<small> ر.س / شهر</small></div>
      <p class="plan-desc">وصول كامل إلى جميع التحليلات الحصرية والأرشيف الكامل.</p>
      <ul class="plan-features">
        <li>كل مزايا الخطة المجانية</li>
        <li>التحليلات الحصرية</li>
        <li>الأرشيف الكامل</li>
        <li>تحليلات السيناريوهات المتقدمة</li>
        <li>الوصول قبل النشر العام</li>
      </ul>
      <button class="plan-btn plan-btn-primary" onclick="subscribeGeo(document.querySelector('#nl-form-sub'),\'ar\')">اشترك الآن</button>
    </div>
    <div class="plan">
      <div class="plan-name">سنوي</div>
      <div class="plan-price">٤٢٠<small> ر.س / سنة</small></div>
      <p class="plan-desc">وفّر ٢٩٪ مقارنة بالاشتراك الشهري — كل المزايا المميزة.</p>
      <ul class="plan-features">
        <li>كل مزايا الخطة المميزة</li>
        <li>توفير ٢٩٪ على السعر الشهري</li>
        <li>أولوية في الردود والاستفسارات</li>
        <li>تقارير خاصة موسعة</li>
      </ul>
      <button class="plan-btn plan-btn-secondary">اشترك سنوياً</button>
    </div>
  </div>

  <!-- FREE NEWSLETTER -->
  <section class="free-section" id="free-nl">
    <h2>النشرة الأسبوعية <em>مجاناً</em></h2>
    <p>تحليلات جيوسياسية معمّقة كل أحد في بريدك — بدون إلزام، بدون بطاقة ائتمانية.</p>
    <form class="nl-form-ab" id="nl-form-sub" onsubmit="return subscribeGeo(this,\'ar\')" novalidate>
      <input type="email" name="email" placeholder="بريدك الإلكتروني" autocomplete="email" required/>
      <button type="submit">اشترك</button>
    </form>
    <p class="nl-msg-ab" aria-live="polite"></p>
    <p class="nl-note-ab">بدون إزعاج · يمكنك إلغاء الاشتراك في أي وقت · نحترم خصوصيتك</p>
  </section>

  <!-- BENEFITS -->
  <div class="benefits">
    <div class="benefit"><div class="benefit-icon">🎯</div><div class="benefit-title">تحليل معمّق</div><p class="benefit-text">لا اكتفاء بالأخبار — تحليل الأسباب والتداعيات والسيناريوهات</p></div>
    <div class="benefit"><div class="benefit-icon">🌍</div><div class="benefit-title">تغطية شاملة</div><p class="benefit-text">الشرق الأوسط · أفريقيا · آسيا · أوروبا · الأمريكتان</p></div>
    <div class="benefit"><div class="benefit-icon">📅</div><div class="benefit-title">كل أسبوع</div><p class="benefit-text">نشرة أسبوعية منتظمة بأهم التطورات الجيوسياسية</p></div>
    <div class="benefit"><div class="benefit-icon">🔒</div><div class="benefit-title">مستقل ومحايد</div><p class="benefit-text">لا ولاءات سياسية — تحليل قائم على الحقائق والمصادر الموثوقة</p></div>
    <div class="benefit"><div class="benefit-icon">📱</div><div class="benefit-title">متاح دائماً</div><p class="benefit-text">اقرأ في أي مكان — جوال أو حاسوب أو تابلت</p></div>
    <div class="benefit"><div class="benefit-icon">✉️</div><div class="benefit-title">مباشرة لبريدك</div><p class="benefit-text">لا تفوّت تحليلاً — وصول مباشر بدون خوارزميات</p></div>
  </div>

  <!-- FAQ -->
  <div class="faq-ab">
    <h2>أسئلة شائعة</h2>
    <div class="faq-item-ab">
      <div class="faq-q-ab" onclick="toggleFaqAb(this)">هل النشرة الأسبوعية مجانية فعلاً؟</div>
      <div class="faq-a-ab">نعم، النشرة الأسبوعية مجانية تماماً بدون قيود. فقط تحليلاتنا الحصرية المتعمقة تتطلب اشتراكاً مميزاً.</div>
    </div>
    <div class="faq-item-ab">
      <div class="faq-q-ab" onclick="toggleFaqAb(this)">هل يمكنني إلغاء الاشتراك في أي وقت؟</div>
      <div class="faq-a-ab">نعم، يمكنك إلغاء الاشتراك في أي وقت بضغطة زر من إعدادات حسابك أو من رابط الإلغاء في أسفل أي رسالة بريدية.</div>
    </div>
    <div class="faq-item-ab">
      <div class="faq-q-ab" onclick="toggleFaqAb(this)">ما الفرق بين المجاني والمميز؟</div>
      <div class="faq-a-ab">الخطة المجانية تشمل جميع المقالات العامة والنشرة الأسبوعية. الخطة المميزة تضيف التحليلات الحصرية والأرشيف الكامل والوصول المبكر للتحليلات الجديدة.</div>
    </div>
  </div>

</div>

<script>
function toggleFaqAb(el) {
  var ans = el.nextElementSibling;
  var isOpen = el.classList.contains('open');
  document.querySelectorAll('.faq-q-ab.open').forEach(function(q){
    q.classList.remove('open');
    q.nextElementSibling.classList.remove('open');
  });
  if (!isOpen) { el.classList.add('open'); ans.classList.add('open'); }
}

function subscribeGeo(form, lang) {
  lang = lang || 'ar';
  var input = form.querySelector('input[type="email"]');
  var btn = form.querySelector('button[type="submit"]');
  var msg = form.parentElement.querySelector('.nl-msg-ab') || form.nextElementSibling;
  var email = input ? input.value.trim() : '';
  if (!email || !/^[^@]+@[^@]+\\.[^@]+$/.test(email)) {
    if(msg) msg.innerHTML = '<span style="color:#B84A0C">⚠️ يرجى إدخال بريد إلكتروني صحيح</span>';
    if(input) input.focus();
    return false;
  }
  var orig = btn ? btn.textContent : '';
  if(btn){btn.textContent='⏳';btn.disabled=true;}
  if(msg) msg.innerHTML='';
  fetch('https://floral-math-8fc3.nasseralsabri.workers.dev/subscribe',{
    method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({email:email,lang:lang})
  })
  .then(function(r){return r.json();})
  .then(function(d){
    if(d.message||d.success){
      if(msg) msg.innerHTML='<span style="color:#0B6B5A;font-weight:600">✅ تم الاشتراك بنجاح — شكراً!</span>';
      if(input) input.value='';
      if(btn){btn.textContent='✓ تم';btn.style.background='#0B6B5A';btn.style.color='#fff';}
    } else {
      var e = d.error||'حدث خطأ';
      if(e.includes('already')||e.includes('موجود')){
        if(msg) msg.innerHTML='<span style="color:#C4952A">ℹ️ هذا البريد مشترك بالفعل</span>';
      } else {
        if(msg) msg.innerHTML='<span style="color:#B84A0C">⚠️ '+e+'</span>';
      }
      if(btn){btn.textContent=orig;btn.disabled=false;}
    }
  })
  .catch(function(){
    if(msg) msg.innerHTML='<span style="color:#B84A0C">❌ خطأ في الاتصال</span>';
    if(btn){btn.textContent=orig;btn.disabled=false;}
  });
  return false;
}
</script>
</body>
</html>'''
    with open(os.path.join(DIR, "abonnement.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✅ abonnement.html created")

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    print("🚀 Running all fixes...\n")

    # Fix eu.html
    print("📄 Fixing eu.html...")
    fix_eu_html()

    # Create abonnement.html
    print("📄 Creating abonnement.html...")
    create_abonnement()

    # Update all articles
    files = sorted(glob.glob(os.path.join(ARTICLES, "*.html")))
    print(f"\n📰 Updating {len(files)} articles...")
    fixed = 0
    for fp in files:
        if update_article(fp):
            fixed += 1
    print(f"  ✅ {fixed} articles updated")

    # Also fix root HTML pages
    root_pages = [f for f in glob.glob(os.path.join(DIR, "*.html"))
                  if os.path.basename(f) not in ("footer-worldmap.html","template-article-v2.html","design-system.html")]
    print(f"\n📄 Updating {len(root_pages)} root pages...")
    fixed_root = 0
    for fp in root_pages:
        with open(fp, encoding="utf-8") as f: content = f.read()
        new = fix_pologeo(content)
        if new != content:
            with open(fp, "w", encoding="utf-8") as f: f.write(new)
            fixed_root += 1
    print(f"  ✅ {fixed_root} root pages cleaned")

    print("\n✅ All done.")

if __name__ == "__main__":
    main()
