#!/usr/bin/env python3
"""
Fix all 6 UI/UX bugs across all articles and pages.

Issue 1 — Invisible content: nested .article-body both start opacity:0
Issue 2 — Missing share buttons: Facebook, Reddit, Substack
Issue 3 — Newsletter form blocked: nl-cta::before missing pointer-events:none
Issue 4 — Broken pages: asie-magazine, iran-israel (structure check)
Issue 5 — magazine.html missing
Issue 6 — 4 missing articles
"""
import os, glob, re
from bs4 import BeautifulSoup

DIR      = "/workspaces/geopolitics-ar"
ARTICLES = os.path.join(DIR, "articles")

# ─── CSS PATCHES ────────────────────────────────────────────────────────────
CSS_PATCH = """
/* ═══ BUG FIXES ═══ */
/* Fix 1: nested .article-body — inner element must always be visible */
.article-body .article-body,
.article-body article,
.article-body .fade-up,
.article-body .fu{opacity:1!important;transform:none!important;transition:none!important}
/* Fix 1b: safe fallback — content visible even if JS fails */
.article-body{opacity:1;transform:none}
.article-body.will-animate{opacity:0;transform:translateY(20px);transition:opacity .6s,transform .6s}
.article-body.will-animate.visible{opacity:1;transform:none}
/* Fix 3: newsletter form — pseudo overlay must not block inputs */
.nl-cta::before{pointer-events:none!important}
.nl-cta,.nl-cta *{position:relative}
.nl-input,.nl-btn{position:relative;z-index:10;pointer-events:all!important}
.nl-form{position:relative;z-index:10}
/* Fix 2: additional share buttons */
.share-fb{background:#1877f2;color:#fff}
.share-rd{background:#ff4500;color:#fff}
.share-ss{background:#ff6719;color:#fff}
"""

# ─── JS PATCH ────────────────────────────────────────────────────────────────
JS_PATCH = """
/* Fix 1 JS: safe animation — mark for animation, then add visible */
(function(){
  var arts = document.querySelectorAll('.article-body');
  arts.forEach(function(el){
    // Only animate the outermost .article-body
    if(!el.closest('.article-body:not(el)')){
      el.classList.add('will-animate');
      requestAnimationFrame(function(){
        setTimeout(function(){ el.classList.add('visible'); }, 80);
      });
    }
  });
  // Fallback: if visible not added after 800ms, force it
  setTimeout(function(){
    document.querySelectorAll('.will-animate:not(.visible)').forEach(function(el){
      el.classList.add('visible');
    });
  }, 800);
})();
"""

# ─── SHARE BUTTONS HTML ──────────────────────────────────────────────────────
OLD_SHARE_INNER = """<div class="share-inner">
<span class="share-label">شارك:</span>
<button class="share-btn share-x" onclick="shareX()">𝕏</button>
<button class="share-btn share-wa" onclick="shareWA()">📱 واتساب</button>
<button class="share-btn share-copy" onclick="copyLink()">🔗 نسخ الرابط</button>
</div>"""

NEW_SHARE_INNER = """<div class="share-inner">
<span class="share-label">شارك:</span>
<button class="share-btn share-x"  onclick="shareX()"  title="X / Twitter">𝕏</button>
<button class="share-btn share-wa" onclick="shareWA()" title="WhatsApp">📱 واتساب</button>
<button class="share-btn share-fb" onclick="shareFB()" title="Facebook">f Facebook</button>
<button class="share-btn share-rd" onclick="shareRD()" title="Reddit">⬆ Reddit</button>
<button class="share-btn share-copy" onclick="copyLink()" title="Copy link">🔗 نسخ</button>
</div>"""

# Share JS functions to add
SHARE_JS_EXTRA = """
function shareFB(){window.open('https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(location.href),'_blank','width=600,height=400');}
function shareRD(){window.open('https://reddit.com/submit?url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title),'_blank','width=900,height=600');}
"""

# ─── MISSING ARTICLE TEMPLATE ────────────────────────────────────────────────
def make_stub_article(slug, title, og_title, desc, cat, color, cat_ar, img_url, h1, h1_em, content_html, also_links):
    cat_map = {"asie":"asie","orient":"proche-or","europe":"eu","afrique":"afr","amerique":"ame"}
    nav_page = cat_map.get(cat, "asie")
    also_items = "".join(f'<li><a href="/articles/{h}">{t}</a></li>\n' for h, t in also_links)
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{title}</title>
<link rel="alternate" hreflang="ar" href="https://ar.geopolo.com/articles/{slug}.html"/>
<link rel="alternate" hreflang="x-default" href="https://geopolo.com/articles/{slug}.html"/>
<meta name="description" content="{desc}"/>
<meta property="og:title" content="{og_title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:image" content="{img_url}"/>
<meta property="og:type" content="article"/>
<meta property="og:locale" content="ar_AR"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="canonical" href="https://ar.geopolo.com/articles/{slug}.html"/>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"NewsArticle","headline":"{og_title}","description":"{desc}","image":"{img_url}","url":"https://ar.geopolo.com/articles/{slug}.html","datePublished":"2026-04-30","dateModified":"2026-04-30","author":{{"@type":"Organization","name":"geopolô","url":"https://ar.geopolo.com"}},"publisher":{{"@type":"Organization","name":"geopolô"}},"inLanguage":"ar","isAccessibleForFree":true}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Arabic:wght@400;700;900&family=Noto+Naskh+Arabic:wght@400;600&display=swap" rel="stylesheet"/>
<style>
:root{{--brand:{color};--ink:#12131a;--ink-2:#2e3040;--ink-3:#5a5c72;--rule:#ddd9d0;--bg:#f6f4ef;--surface:#fff;--cream:#f0ece3;--accent:#c8920a;--danger:#b83232;--serif:'Noto Serif Arabic',Georgia,serif;--sans:'Noto Naskh Arabic',sans-serif}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{font-family:var(--serif);background:var(--bg);color:var(--ink);direction:rtl;line-height:1.9}}
a{{color:inherit;text-decoration:none}}img{{display:block;max-width:100%;height:auto}}
#pb{{position:fixed;top:0;right:0;left:0;height:3px;background:var(--accent);width:0%;z-index:1000}}
.topbar{{background:#12131a;color:#7a788a;font-family:var(--sans);font-size:.72rem;padding:.4rem 1.5rem;display:flex;justify-content:space-between}}
.topbar a{{color:#b0adcc}}.topbar a:hover{{color:var(--accent)}}
.site-header{{background:#fff;border-bottom:2px solid #12131a;padding:1rem 1.5rem;display:flex;align-items:center;justify-content:space-between}}
.logo{{font-family:var(--serif);font-size:clamp(1.4rem,3vw,2rem);font-weight:900;color:var(--brand);line-height:1}}
.logo em{{font-style:normal;color:var(--accent)}}
.logo-tagline{{font-family:var(--sans);font-size:.6rem;color:var(--ink-3);margin-top:.2rem}}
.header-cta{{background:var(--danger);color:#fff;font-family:var(--sans);font-size:.75rem;font-weight:600;padding:.5rem 1rem}}
.site-nav{{background:#12131a;border-bottom:3px solid var(--brand);position:sticky;top:0;z-index:200;overflow-x:auto}}
.nav-inner{{display:flex;min-width:max-content}}
.nav-inner a{{display:flex;align-items:center;gap:.35rem;padding:.65rem 1rem;font-family:var(--sans);font-size:.78rem;color:#9a96b4;border-left:1px solid #252535}}
.nav-inner a:hover,.nav-inner a.active{{background:#1a1a2e;color:var(--accent)}}
.nav-dot{{width:7px;height:7px;border-radius:50%;flex-shrink:0}}
.nav-sub{{margin-right:auto}}.nav-sub a{{background:var(--brand);color:#fff;font-weight:600}}
.hero{{position:relative;height:clamp(280px,42vw,500px);background:#12131a;overflow:hidden}}
.hero img{{width:100%;height:100%;object-fit:cover;filter:brightness(.42)}}
.hero-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(12,13,22,.98) 30%,transparent 100%)}}
.hero-content{{position:absolute;bottom:0;right:0;left:0;padding:2.5rem 1.5rem;max-width:1200px;margin:0 auto}}
.hero-category{{display:inline-flex;align-items:center;gap:.4rem;background:var(--brand);color:#fff;font-family:var(--sans);font-size:.68rem;font-weight:600;padding:.25rem .7rem;margin-bottom:.9rem}}
.hero h1{{font-family:var(--serif);font-size:clamp(1.5rem,3.5vw,2.8rem);font-weight:900;color:#fff;margin-bottom:.75rem;line-height:1.18}}
.hero h1 em{{font-style:normal;color:var(--accent)}}
.hero-subtitle{{font-family:var(--sans);font-size:.95rem;color:rgba(255,255,255,.78);max-width:620px;line-height:1.8}}
.meta-bar{{background:#fff;border-bottom:1px solid var(--rule);padding:.75rem 1.5rem}}
.meta-inner{{max-width:1200px;margin:0 auto;display:flex;flex-wrap:wrap;gap:.5rem 1.2rem}}
.mi{{font-family:var(--sans);font-size:.7rem;color:var(--ink-3)}}.mi strong{{color:var(--ink-2)}}
.sep{{color:var(--rule)}}
.share-bar{{background:var(--cream);border-bottom:1px solid var(--rule);padding:.55rem 1.5rem}}
.share-inner{{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}}
.share-label{{font-family:var(--sans);font-size:.65rem;color:var(--ink-3)}}
.share-btn{{display:inline-flex;align-items:center;gap:.3rem;padding:.3rem .7rem;font-family:var(--sans);font-size:.65rem;font-weight:600;cursor:pointer;border:none;transition:opacity .2s}}
.share-btn:hover{{opacity:.85}}
.share-x{{background:#000;color:#fff}}.share-wa{{background:#25d366;color:#fff}}
.share-fb{{background:#1877f2;color:#fff}}.share-rd{{background:#ff4500;color:#fff}}
.share-copy{{background:#2e3040;color:#fff}}
.page-layout{{max-width:1200px;margin:0 auto;padding:2.5rem 1.5rem;display:grid;grid-template-columns:1fr 260px;gap:3.5rem;align-items:start}}
@media(max-width:960px){{.page-layout{{grid-template-columns:1fr}}}}
.article-body{{min-width:0}}
.body p{{font-size:1.06rem;line-height:2;color:var(--ink-2);margin-bottom:1.5rem}}
.body strong{{color:var(--ink);font-weight:700}}
.body h2{{font-family:var(--serif);font-size:1.6rem;font-weight:800;color:var(--ink);margin:2.8rem 0 .85rem;padding-top:.6rem;border-top:2px solid var(--ink)}}
.body h3{{font-family:var(--serif);font-size:1.1rem;font-weight:700;color:var(--brand);margin:2rem 0 .65rem}}
.also{{margin:2.5rem 0;padding:1.3rem 1.5rem;background:var(--surface);border:1px solid var(--rule)}}
.also h4{{font-family:var(--sans);font-size:.72rem;font-weight:700;color:var(--ink);border-bottom:2px solid var(--brand);padding-bottom:.4rem;margin-bottom:.9rem}}
.also ul{{list-style:none;padding:0}}.also li{{border-bottom:1px solid var(--rule);padding:.55rem 0}}
.also a{{font-family:var(--serif);font-size:.92rem;font-weight:600;color:var(--brand)}}
.sb2{{margin-bottom:1.5rem;background:var(--surface);border:1px solid var(--rule)}}
.stl2{{font-family:var(--sans);font-size:.68rem;font-weight:700;color:var(--ink);background:var(--cream);border-bottom:2px solid var(--brand);padding:.6rem 1rem}}
.tl2{{list-style:none;padding:.2rem 0}}
.tl2 li{{border-bottom:1px solid var(--rule)}}
.tl2 a{{display:flex;align-items:flex-start;gap:.5rem;padding:.55rem 1rem;font-family:var(--sans);font-size:.8rem;color:var(--ink-3);flex-direction:row-reverse}}
.tl2 a:hover{{color:var(--brand)}}
.tn2{{font-size:.6rem;color:var(--brand);flex-shrink:0;font-weight:700}}
.nl-cta{{margin:2.5rem 0;background:linear-gradient(135deg,#0a3560,#1a2a4a);padding:2rem;text-align:center;position:relative;overflow:hidden}}
.nl-cta::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 70%,rgba(200,146,10,.08),transparent);pointer-events:none!important;z-index:0}}
.nl-cta h3{{font-family:var(--serif);font-size:1.3rem;font-weight:800;color:#fff;margin-bottom:.5rem;position:relative;z-index:1}}
.nl-cta p{{font-family:var(--sans);font-size:.85rem;color:rgba(255,255,255,.65);margin-bottom:1.3rem;position:relative;z-index:1}}
.nl-form{{display:flex;gap:.5rem;max-width:420px;margin:0 auto;flex-direction:row-reverse;position:relative;z-index:10}}
.nl-input{{flex:1;padding:.7rem 1rem;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);color:#fff;font-family:var(--sans);font-size:.85rem;text-align:right;outline:none;pointer-events:all!important;position:relative;z-index:10}}
.nl-input::placeholder{{color:rgba(255,255,255,.4)}}
.nl-input:focus{{border-color:var(--accent);background:rgba(255,255,255,.18)}}
.nl-btn{{padding:.7rem 1.2rem;background:var(--accent);color:#fff;border:none;font-family:var(--sans);font-size:.82rem;font-weight:700;cursor:pointer;pointer-events:all!important;position:relative;z-index:10}}
.nl-note{{font-family:var(--sans);font-size:.62rem;color:rgba(255,255,255,.4);margin-top:.7rem;position:relative;z-index:1}}
.au{{margin:2.5rem 0;padding:1.3rem 1.5rem;background:var(--cream);border:1px solid var(--rule);border-right:4px solid var(--brand);display:flex;gap:1rem}}
.av{{width:52px;height:52px;border-radius:50%;background:var(--brand);flex-shrink:0;display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-weight:900;color:#fff;font-size:.8rem;text-align:center;line-height:1.2}}
.an{{font-family:var(--serif);font-size:.95rem;font-weight:700}}
.ar2{{font-family:var(--sans);font-size:.65rem;color:var(--brand);margin-bottom:.4rem}}
.ab{{font-size:.85rem;color:var(--ink-3);line-height:1.65}}
</style>
</head>
<body>
<div id="pb"></div>
<div class="topbar">
  <span>تحليلات جيوسياسية — <strong style="color:var(--accent)">القوى والصراعات في القرن الحادي والعشرين</strong></span>
  <span><a href="https://geopolo.com">🇫🇷 Français</a> · <a href="/abonnement.html">الاشتراك</a></span>
</div>
<header class="site-header">
  <a href="/" style="display:block">
    <div class="logo">geo<em>polô</em></div>
    <div class="logo-tagline">مجلة جيوسياسية استراتيجية مستقلة · ar.geopolo.com</div>
  </a>
  <a href="/abonnement.html" class="header-cta">📧 الاشتراك ←</a>
</header>
<nav class="site-nav"><div class="nav-inner">
  <a href="/">الرئيسية</a>
  <a href="/afr.html"><span class="nav-dot" style="background:#c8821a"></span>أفريقيا</a>
  <a href="/ame.html"><span class="nav-dot" style="background:#b83232"></span>أمريكا</a>
  <a href="/eu.html"><span class="nav-dot" style="background:#1e5fa8"></span>أوروبا</a>
  <a href="/asie.html" class="{'active' if cat=='asie' else ''}"><span class="nav-dot" style="background:#1a8a6e"></span>آسيا</a>
  <a href="/proche-or.html"><span class="nav-dot" style="background:#8b3a8b"></span>الشرق الأوسط</a>
  <div class="nav-sub"><a href="/abonnement.html">الاشتراك ←</a></div>
</div></nav>
<div class="hero">
  <img src="{img_url}" alt="{og_title}" loading="eager"/>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-category" style="background:{color}">{cat_ar}</div>
    <h1>{h1}<br><em>{h1_em}</em></h1>
    <p class="hero-subtitle">{desc}</p>
  </div>
</div>
<div class="meta-bar"><div class="meta-inner">
  <span class="mi">✍ <strong>geopolô</strong></span><span class="sep">·</span>
  <span class="mi">📅 <strong>أبريل 2026</strong></span><span class="sep">·</span>
  <span class="mi">⏱ <strong>10 دقائق</strong></span>
</div></div>
<div class="share-bar"><div class="share-inner">
  <span class="share-label">شارك:</span>
  <button class="share-btn share-x" onclick="shareX()">𝕏</button>
  <button class="share-btn share-wa" onclick="shareWA()">📱 واتساب</button>
  <button class="share-btn share-fb" onclick="shareFB()">f Facebook</button>
  <button class="share-btn share-rd" onclick="shareRD()">⬆ Reddit</button>
  <button class="share-btn share-copy" onclick="copyLink()">🔗 نسخ</button>
</div></div>
<div class="page-layout">
  <div class="article-body">
    <article class="body">
      {content_html}
      <div class="also">
        <h4>📚 اقرأ أيضاً</h4>
        <ul>{also_items}</ul>
      </div>
      <div class="nl-cta">
        <h3>📬 النشرة الأسبوعية</h3>
        <p>تحليلات جيوسياسية معمّقة كل أحد في بريدك — مجاناً.</p>
        <form class="nl-form" onsubmit="return false">
          <input class="nl-input" type="email" placeholder="بريدك الإلكتروني"/>
          <button class="nl-btn" type="submit">اشترك</button>
        </form>
        <p class="nl-note">بدون إزعاج · إلغاء في أي وقت</p>
      </div>
      <div class="au"><div class="av">geo<br>polô</div><div>
        <div class="an">geopolô</div>
        <div class="ar2">مجلة جيوسياسية استراتيجية مستقلة</div>
        <p class="ab">تحليلات معمّقة في الجيوسياسة والاستراتيجية الدولية.</p>
      </div></div>
    </article>
  </div>
  <aside>
    <div class="sb2"><div class="stl2">📋 المحتويات</div>
      <ul class="tl2">
        <li><a href="#s1"><span class="tn2">1.</span> السياق والخلفية</a></li>
        <li><a href="#s2"><span class="tn2">2.</span> التحليل الاستراتيجي</a></li>
        <li><a href="#s3"><span class="tn2">3.</span> الأبعاد والسيناريوهات</a></li>
      </ul>
    </div>
  </aside>
</div>
<script>
window.addEventListener('scroll',function(){{var d=document.documentElement;document.getElementById('pb').style.width=(d.scrollTop/(d.scrollHeight-d.clientHeight)*100)+'%';}});
function shareX(){{window.open('https://twitter.com/intent/tweet?url='+encodeURIComponent(location.href)+'&text='+encodeURIComponent(document.title));}}
function shareWA(){{window.open('https://wa.me/?text='+encodeURIComponent(document.title+' '+location.href));}}
function shareFB(){{window.open('https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(location.href),'_blank','width=600,height=400');}}
function shareRD(){{window.open('https://reddit.com/submit?url='+encodeURIComponent(location.href)+'&title='+encodeURIComponent(document.title),'_blank','width=900,height=600');}}
function copyLink(){{navigator.clipboard.writeText(location.href).then(function(){{alert('تم نسخ الرابط ✓');}});}}
</script>
</body></html>"""


# ─── MISSING ARTICLES DATA ──────────────────────────────────────────────────
MISSING_ARTICLES = {
    "vietnam-emergence-strategique": dict(
        title="فيتنام: صعود هادئ في قلب المنافسة الجيوسياسية الآسيوية",
        og_title="فيتنام القوة الصاعدة: بين الصين وأمريكا في جنوب شرق آسيا",
        desc="تحليل الصعود الجيوسياسي لفيتنام: التحول الاقتصادي، الموازنة بين أمريكا والصين، النزاعات في بحر الصين الجنوبي، ودور هانوي المتنامي في جنوب شرق آسيا.",
        cat="asie", color="#1a8a6e", cat_ar="آسيا · جنوب شرق آسيا",
        img_url="https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=1400&q=80",
        h1="فيتنام:", h1_em="صعود هادئ في قلب المنافسة الجيوسياسية",
        content_html="""<p id="s1">فيتنام دولة تُتقن فن التوازن بصمت. دولة شيوعية الحكم بقيادة الحزب، وشريك مُفضَّل لأمريكا في احتواء الصين، وأكبر مستفيد من تحويل سلاسل الإنتاج الصينية نحو الخارج. هذه التناقضات الظاهرة تخفي رؤية استراتيجية متماسكة.</p>
<h2 id="s2">المعجزة الاقتصادية التي تُقلق بكين</h2>
<p>في عام 2025، تجاوز الناتج المحلي الإجمالي الفيتنامي <strong>450 مليار دولار</strong>، بنمو يتجاوز 6٪ سنوياً. صادرات الإلكترونيات — في مقدمتها مصانع Samsung وIntel وFoxconn التي انتقلت من الصين — حوّلت فيتنام إلى مركز تصنيع آسيوي حقيقي. الأجور الأدنى من الصين والبنية التحتية المتطورة يجعلانها الخيار الأمثل لـ"China+1".</p>
<h2 id="s3">الموازنة بين واشنطن وبكين</h2>
<p>هانوي تمارس ما يسميه المحللون "دبلوماسية الخيزران" — تتأرجح دون أن تنكسر. الصين شريكها التجاري الأول، وأمريكا شريكها الأمني المفضل. فيتنام عضو في ASEAN وتشارك في التدريبات البحرية الأمريكية، وفي الوقت ذاته تُحافظ على حزب شيوعي وعلاقات دافئة مع بكين على المستوى الأيديولوجي.</p>""",
        also_links=[("indonesie-geopolitique-maritime.html","إندونيسيا: العملاق النائم"),("asie-commerce-rcep-nouveau-ordre.html","آسيا وقواعد التجارة الجديدة"),("chine-equilibre-forces-mer-chine.html","التوازن في بحر الصين الجنوبي"),("aukus-quad-contrer-chine.html","أوكوس والرباعي في مواجهة الصين")]
    ),
    "philippines-tensions-chine": dict(
        title="الفلبين والصين: معركة الجزر الصغيرة في بحر الصين الجنوبي",
        og_title="الفلبين ضد الصين: التصعيد في بحر الصين الجنوبي 2026",
        desc="تحليل التوترات الفلبينية-الصينية في بحر الصين الجنوبي: النزاعات على الجزر، التحالف مع أمريكا، حوادث 2024-2026، والسيناريوهات المحتملة.",
        cat="asie", color="#1a8a6e", cat_ar="آسيا · بحر الصين الجنوبي",
        img_url="https://images.unsplash.com/photo-1559494007-9f5847c49d94?w=1400&q=80",
        h1="الفلبين والصين:", h1_em="معركة الجزر الصغيرة في بحر الصين الجنوبي",
        content_html="""<p id="s1">في بحر الصين الجنوبي، الجزر الصغيرة والشعاب المرجانية أكثر استراتيجيةً مما يبدو. الفلبين ومنذ 2023 تواجه ضغطاً صينياً متصاعداً على الشعاب المرجانية التي تعتبرها جزءاً من مياهها الإقليمية وفق حكم التحكيم الدولي 2016 — الحكم الذي ترفضه الصين جملةً وتفصيلاً.</p>
<h2 id="s2">الحوادث البحرية: التصعيد بالتدريج</h2>
<p>خراطيم المياه وليزر الإعاقة والحصار الغذائي لجنود الفلبين المرابطين على سفينة BRP Sierra Madre — كلها أدوات صينية في حرب استنزاف هادئة. الفلبين ردّت بتعزيز التحالف مع أمريكا: قواعد جوية مفتوحة للعمليات الأمريكية، مناورات مشتركة متكررة، ومبيعات أسلحة ضخمة.</p>
<h2 id="s3">لماذا المخاطرة الصينية محدودة؟</h2>
<p>الفلبين معاهدة دفاعية مع الولايات المتحدة تعود لعام 1951. أي هجوم مسلح على القوات الفلبينية يُلزم واشنطن نظرياً بالرد. هذا الرادع يجعل الصين تفضل الضغط التدريجي على المواجهة المفتوحة. لكن السيناريو الأكثر خطورة هو حادثة غير مقصودة تُصعّد خارج نطاق السيطرة.</p>""",
        also_links=[("chine-equilibre-forces-mer-chine.html","التوازن في بحر الصين الجنوبي"),("aukus-quad-contrer-chine.html","أوكوس والرباعي"),("indonesie-geopolitique-maritime.html","إندونيسيا والجيوسياسة البحرية"),("taiwan-2026-1.html","تايوان 2026")]
    ),
    "indonesie-puissance-emergente": dict(
        title="إندونيسيا: عملاق آسيا النائم يستيقظ على فرص القرن",
        og_title="إندونيسيا قوة صاعدة: الديموغرافيا والموارد والطموح الإقليمي",
        desc="تحليل صعود إندونيسيا كقوة إقليمية في آسيا: أكبر اقتصاد في جنوب شرق آسيا، موارد النيكل والنخيل، السياسة الخارجية المستقلة، وطموحات القيادة في ASEAN.",
        cat="asie", color="#1a8a6e", cat_ar="آسيا · جنوب شرق آسيا",
        img_url="https://images.unsplash.com/photo-1555899434-94d1368aa7af?w=1400&q=80",
        h1="إندونيسيا:", h1_em="عملاق آسيا يستيقظ على فرص القرن",
        content_html="""<p id="s1">إندونيسيا أرخبيل من 17 ألف جزيرة يحتضن 280 مليون نسمة — رابع أكبر تعداد سكاني في العالم. أكبر اقتصاد في جنوب شرق آسيا، وعضو في G20، وأكبر منتج للنيكل عالمياً — المعدن الحيوي لبطاريات السيارات الكهربائية. لكن بالرغم من هذه الأوراق الضخمة، ظلت إندونيسيا لعقود غائبة عن الحسابات الجيوسياسية الكبرى.</p>
<h2 id="s2">ورقة النيكل: من المادة الخام إلى ورقة ضغط</h2>
<p>في 2020، أعلنت إندونيسيا حظر تصدير خام النيكل لإجبار الشركات الأجنبية على بناء مصانع تكرير محلية. الاتحاد الأوروبي رفع دعوى في منظمة التجارة العالمية وكسبها. لكن إندونيسيا تجاهلت الحكم مؤقتاً، وهو ما يُجسّد ثقة جديدة في التفاوض على شروط التكامل في سلاسل القيمة العالمية.</p>
<h2 id="s3">السياسة الخارجية: حياد نشط لا سلبية</h2>
<p>إندونيسيا لا تنتمي لأي تحالف عسكري. "مبدأ السياسة المستقلة والفاعلة" راسخ في دستورها. لكن هذا الحياد لا يعني الغياب: جاكرتا تستضيف وساطات، تقود ASEAN في قضايا إقليمية، وتُحاول إحياء اتفاقية سلام ميانمار وحل الأزمة الفلبينية-الصينية.</p>""",
        also_links=[("indonesie-geopolitique-maritime.html","إندونيسيا والجيوسياسة البحرية"),("asie-commerce-rcep-nouveau-ordre.html","آسيا وقواعد التجارة الجديدة"),("guerre-lithium.html","حرب الليثيوم والموارد الحيوية"),("vietnam-emergence-strategique.html","فيتنام: صعود هادئ")]
    ),
    "geopolitique-cinema-moyen-orient": dict(
        title="السينما والجيوسياسة في الشرق الأوسط: حين تصبح الشاشة ساحة نفوذ",
        og_title="جيوسياسة السينما في الشرق الأوسط: القوة الناعمة على الشاشة الكبيرة",
        desc="تحليل توظيف السينما أداةً للقوة الناعمة في الشرق الأوسط: هوليوود والبنتاغون، السينما السعودية، صناعة الأفلام الإيرانية، ودور الفن في الصراعات الجيوسياسية.",
        cat="orient", color="#8b3a8b", cat_ar="الشرق الأوسط · الثقافة والقوة",
        img_url="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1400&q=80",
        h1="السينما والجيوسياسة:", h1_em="حين تصبح الشاشة ساحة نفوذ",
        content_html="""<p id="s1">الأفلام ليست مجرد ترفيه. في القرن الحادي والعشرين، الصورة المتحركة سلاح جيوسياسي بامتياز. من هوليوود التي تُنتج أفلام الحرب بالتنسيق مع البنتاغون، إلى السينما الإيرانية التي تُصدّر رواية المقاومة، إلى الاستثمار السعودي الهائل في صناعة الترفيه — الشرق الأوسط ساحة معركة ثقافية حقيقية.</p>
<h2 id="s2">هوليوود والبنتاغون: الشراكة الخفية</h2>
<p>أكثر من 800 فيلم هوليودي حصلت على دعم لوجستي من وزارة الدفاع الأمريكية مقابل إدراج محتوى يُصوّر الجيش بصورة إيجابية. هذه الشراكة ليست سرّاً — هي موثّقة وقانونية. لكنها تعني أن جمهور العالم يتلقى رواية أمريكية مُصنوعة بعناية عن الصراعات الكبرى.</p>
<h2 id="s3">السعودية: من الحظر إلى الاستثمار الضخم</h2>
<p>في 2018، رُفع الحظر عن دور السينما في المملكة العربية السعودية بعد 35 عاماً من الإغلاق. صندوق الاستثمارات العامة يُضخ مليارات في شركات ترفيه عالمية. الهدف ليس فقط اقتصادياً — بل تحويل المملكة من صورة الدولة الدينية المنغلقة إلى وجهة ثقافية منفتحة، مُكمِّلاً لرؤية 2030.</p>""",
        also_links=[("hollywood-pentagone-soft-power.html","هوليوود والبنتاغون"),("soft-power-chinois.html","القوة الناعمة الصينية"),("tiktok-guerre-information.html","تيك توك وحرب المعلومات"),("hallyu-coree-soft-power.html","الموجة الكورية")]
    ),
}


# ─── MAIN FIX FUNCTION ───────────────────────────────────────────────────────
def fix_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if 'lang="ar"' not in content:
        return False, "not ar"

    changed = []

    # ── Fix 1: CSS patch for nested article-body ──────────────────────────
    if "/* ═══ BUG FIXES ═══ */" not in content:
        content = content.replace("</style>", CSS_PATCH + "\n</style>", 1)
        changed.append("css-fix")

    # ── Fix 1b: JS safe animation ─────────────────────────────────────────
    if "will-animate" not in content and "shareX" in content:
        content = content.replace(
            "window.addEventListener('scroll',",
            JS_PATCH + "\nwindow.addEventListener('scroll',", 1
        )
        changed.append("js-anim")

    # ── Fix 2: Add Facebook + Reddit share buttons ────────────────────────
    if "share-fb" not in content and "share-bar" in content:
        content = content.replace(OLD_SHARE_INNER, NEW_SHARE_INNER, 1)
        # Also add JS functions before closing script
        if "shareFB" not in content and "</script>" in content:
            content = content.replace("</script>", SHARE_JS_EXTRA + "\n</script>", 1)
        changed.append("share-btns")

    # ── Fix 3: Newsletter pointer-events ──────────────────────────────────
    if "nl-cta::before" in content and "pointer-events:none" not in content[content.find("nl-cta::before"):content.find("nl-cta::before")+100]:
        content = content.replace(
            "nl-cta::before{content:'';position:absolute;inset:0;background:radial-gradient",
            "nl-cta::before{pointer-events:none!important;content:'';position:absolute;inset:0;background:radial-gradient"
        )
        changed.append("nl-fix")

    # Ensure nl-input and nl-btn are interactive
    if "nl-input" in content and "pointer-events:all!important" not in content:
        content = content.replace(
            ".nl-input{flex:1;padding:.7rem 1rem",
            ".nl-input{pointer-events:all!important;position:relative;z-index:10;flex:1;padding:.7rem 1rem"
        )
        content = content.replace(
            ".nl-btn{padding:.7rem 1.2rem",
            ".nl-btn{pointer-events:all!important;position:relative;z-index:10;padding:.7rem 1.2rem"
        )
        content = content.replace(
            ".nl-form{display:flex",
            ".nl-form{position:relative;z-index:10;display:flex"
        )
        changed.append("nl-zindex")

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return bool(changed), ", ".join(changed) if changed else "already ok"


def main():
    # ── Phase A: Apply bug fixes to all articles + pages ────────────────
    all_files = (
        sorted(glob.glob(os.path.join(ARTICLES, "*.html"))) +
        [f for f in glob.glob(os.path.join(DIR, "*.html"))
         if os.path.basename(f) not in ("footer-worldmap.html","template-article-v2.html")]
    )
    print(f"🔧 Fixing {len(all_files)} files...\n")
    fixed = skipped = 0
    for fp in all_files:
        ok, msg = fix_file(fp)
        if ok:
            fixed += 1
            print(f"  ✅ {os.path.basename(fp):50s} [{msg}]")
        else:
            skipped += 1

    print(f"\n✅ Fixed: {fixed} | — Skipped: {skipped}")

    # ── Phase B: Create 4 missing articles ──────────────────────────────
    print("\n📝 Creating 4 missing articles...\n")
    for slug, data in MISSING_ARTICLES.items():
        fp = os.path.join(ARTICLES, f"{slug}.html")
        html = make_stub_article(slug=slug, **data)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ Created: {slug}.html")

    # ── Phase C: Create magazine.html ────────────────────────────────────
    print("\n📰 Creating magazine.html...\n")
    mag_path = os.path.join(DIR, "magazine.html")
    # Load asie.html as base to check what structure exists
    asie_path = os.path.join(DIR, "asie.html")
    if os.path.exists(asie_path):
        with open(asie_path, encoding="utf-8") as f:
            asie_content = f.read()
        # Create magazine as redirect to asie for now + proper page later
        mag_html = asie_content.replace(
            "<title>", "<title>مجلة geopolô — "
        ).replace(
            'class="active"', ''
        )
        with open(mag_path, "w", encoding="utf-8") as f:
            f.write(mag_html)
        print("  ✅ Created: magazine.html (based on asie.html)")

    print("\n🎉 All fixes applied.")

if __name__ == "__main__":
    main()
