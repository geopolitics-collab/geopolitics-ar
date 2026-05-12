#!/usr/bin/env python3
"""Rebuild 12 thin/French articles as proper Arabic articles."""

import os

DIR = "/workspaces/geopolitics-ar/articles"

def make_article(slug, cat, color, title, og_title, desc, keywords, img_url,
                 badge, h1, h1_em, hsub, sections, also_links, faq_items,
                 verdict=None):
    nav_active = {
        "afrique": "afr", "amerique": "ame", "europe": "eu",
        "asie": "asie", "orient": "proche-or", "default": ""
    }
    nav_html = f"""<nav>
  <a href="/">الرئيسية</a>
  <a href="/afr.html" data-r="afrique"><span class="dot"></span>أفريقيا</a>
  <a href="/ame.html" data-r="amerique"><span class="dot"></span>أمريكا</a>
  <a href="/eu.html" data-r="europe"><span class="dot"></span>أوروبا</a>
  <a href="/asie.html" data-r="asie"{"  class=\"active\"" if cat=="asie" else ""}><span class="dot"></span>آسيا</a>
  <a href="/proche-or.html" data-r="orient"{"  class=\"active\"" if cat=="orient" else ""}><span class="dot"></span>الشرق الأوسط</a>
  <a href="/afr.html" data-r="afrique"{"  class=\"active\"" if cat=="afrique" else ""}><span class="dot"></span>أفريقيا</a>
  <a href="/abonnement.html" class="nav-cta">الاشتراك ←</a>
</nav>"""

    body_html = ""
    for sec in sections:
        body_html += sec

    also_items = ""
    for href, text in also_links:
        also_items += f'<li><a href="{href}">{text}</a></li>\n'

    faq_html = ""
    for q, a in faq_items:
        faq_html += f'<div class="fqi"><div class="fqq">{q}</div><div class="fqa">{a}</div></div>\n'

    verdict_html = ""
    if verdict:
        verdict_html = f"""<div class="verdict">
  <div class="vt">📌 تقييم geopolô</div>
  <div class="vc"><p>{verdict}</p></div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{title}</title>
  <link rel="alternate" hreflang="fr" href="https://geopolo.com/articles/{slug}.html"/>
  <link rel="alternate" hreflang="ar" href="https://ar.geopolo.com/articles/{slug}.html"/>
  <link rel="alternate" hreflang="x-default" href="https://geopolo.com/articles/{slug}.html"/>
<meta name="description" content="{desc}"/>
<meta name="keywords" content="{keywords}"/>
<meta property="og:title" content="{og_title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:image" content="{img_url}"/>
<meta property="og:type" content="article"/>
<meta property="og:locale" content="ar_AR"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:site" content="@geopolo_ar"/>
<link rel="canonical" href="https://ar.geopolo.com/articles/{slug}.html"/>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{og_title}",
  "description": "{desc}",
  "image": "{img_url}",
  "url": "https://ar.geopolo.com/articles/{slug}.html",
  "datePublished": "2026-04-29",
  "dateModified": "2026-04-29",
  "author": {{"@type": "Organization","name": "geopolô","url": "https://ar.geopolo.com"}},
  "publisher": {{"@type": "Organization","name": "geopolô","logo": {{"@type": "ImageObject","url": "https://ar.geopolo.com/favicon.ico"}}}},
  "inLanguage": "ar",
  "isAccessibleForFree": true
}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Arabic:wght@400;700;900&family=Noto+Naskh+Arabic:wght@400;600&display=swap" rel="stylesheet"/>
<style>
:root{{--a:{color};--ink:#1a1a2a;--bg:#f8f7f4;--paper:#fff;--cream:#f3f0e8;--mid:#5a5870;--rule:#e2ddd8;--or:#d4a843;--afrique:#c8821a;--amerique:#b83232;--europe:#1e5fa8;--asie:#1a8a6e;--orient:#8b3a8b}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{font-family:'Noto Serif Arabic',Georgia,serif;background:var(--bg);color:var(--ink);direction:rtl;line-height:1.9}}
a{{color:inherit;text-decoration:none}}
#pb{{position:fixed;top:0;right:0;left:0;height:3px;background:var(--a);width:0%;z-index:9999;transition:width .1s}}
.top{{background:#1a1a2a;color:#8a87a0;font-family:'Noto Naskh Arabic',sans-serif;font-size:.75rem;padding:.4rem 2rem;display:flex;justify-content:space-between;align-items:center}}
.top a{{color:#b8b4d0}}.top a:hover{{color:var(--or)}}
.mast{{background:var(--paper);border-bottom:3px solid var(--ink);padding:1.2rem 2rem;display:flex;justify-content:space-between;align-items:flex-end}}
.logo{{font-family:'Noto Serif Arabic',serif;font-size:clamp(1.3rem,3vw,2.2rem);font-weight:900;color:var(--a)}}
.logo span{{display:block;font-size:.52em;font-weight:400;color:var(--mid)}}
.msub{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.7rem;color:var(--mid);text-align:left}}
nav{{background:#1a1a2a;display:flex;flex-wrap:wrap;position:sticky;top:0;z-index:100;border-bottom:3px solid var(--a)}}
nav a{{display:flex;align-items:center;gap:.4rem;padding:.65rem .9rem;font-family:'Noto Naskh Arabic',sans-serif;font-size:.78rem;color:#9a96b0;border-left:1px solid #2a2a3a;transition:all .2s}}
nav a:hover,nav a.active{{background:#252535;color:var(--or)}}
nav a .dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0}}
nav a[data-r="afrique"] .dot{{background:var(--afrique)}}nav a[data-r="amerique"] .dot{{background:var(--amerique)}}
nav a[data-r="europe"] .dot{{background:var(--europe)}}nav a[data-r="asie"] .dot{{background:var(--asie)}}nav a[data-r="orient"] .dot{{background:var(--orient)}}
nav a.nav-cta{{margin-right:auto;background:var(--amerique);color:#fff;border:none;font-weight:600}}
.hero{{position:relative;height:clamp(300px,45vw,520px);overflow:hidden;background:#1a1a2a}}
.hero img{{width:100%;height:100%;object-fit:cover;filter:brightness(.48)}}
.hero__ov{{position:absolute;inset:0;background:linear-gradient(to top,rgba(26,26,42,.97) 35%,rgba(26,26,42,.1) 100%)}}
.hero__c{{position:absolute;bottom:0;left:0;right:0;padding:2.5rem 2rem;max-width:900px;margin:0 auto}}
.hbadge{{display:inline-block;font-family:'Noto Naskh Arabic',sans-serif;font-size:.7rem;padding:.22rem .7rem;color:#fff;margin-bottom:.8rem;border:1px solid rgba(255,255,255,.3)}}
.hero h1{{font-family:'Noto Serif Arabic',serif;font-size:clamp(1.6rem,3.5vw,2.8rem);font-weight:900;line-height:1.15;color:#fff;margin-bottom:.8rem}}
.hero h1 em{{font-style:normal;color:var(--or)}}
.hsub{{font-size:.98rem;color:rgba(255,255,255,.72);max-width:650px;line-height:1.85}}
.meta{{background:var(--paper);border-bottom:1px solid var(--rule);padding:.8rem 2rem}}
.metai{{max-width:1060px;margin:0 auto;display:flex;flex-wrap:wrap;gap:1rem;align-items:center}}
.mi{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.7rem;color:#9a96b0}}.mi strong{{color:var(--mid)}}
.sep{{color:var(--rule)}}
.layout{{max-width:1200px;margin:0 auto;padding:2.5rem 1.5rem;display:grid;grid-template-columns:1fr 290px;gap:4rem;align-items:start}}
@media(max-width:960px){{.layout{{grid-template-columns:1fr;gap:2rem}}}}
.kwb{{background:var(--cream);border:1px solid var(--rule);border-right:3px solid var(--a);padding:.65rem 1rem;margin-bottom:2rem;display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}}
.kwl{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.65rem;font-weight:700;color:var(--a);margin-left:.5rem}}
.kw{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.65rem;padding:.18rem .55rem;border:1px solid var(--rule);background:var(--paper);color:var(--mid)}}
.body>p:first-of-type::first-letter{{font-size:3.8rem;font-weight:900;float:right;line-height:.85;margin:.05em 0 -.05em .15em;color:var(--a)}}
.body p{{font-size:1.05rem;line-height:1.95;margin-bottom:1.6rem;color:#2a2a3a}}
.body strong{{font-weight:700;color:var(--ink)}}
.body ul{{margin:1rem 0 1.5rem;padding-right:1.6rem}}.body li{{font-size:1rem;line-height:1.85;margin-bottom:.55rem;color:#2a2a3a}}
.chl{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.68rem;color:var(--a);margin-bottom:.25rem;display:flex;align-items:center;gap:.7rem;flex-direction:row-reverse}}
.chl::before{{content:'';flex:1;height:1px;background:var(--rule)}}
.body h2{{font-family:'Noto Serif Arabic',serif;font-size:1.6rem;font-weight:700;margin:2.8rem 0 .9rem;padding-top:.6rem;border-top:2px solid var(--ink);color:var(--ink)}}
.body h3{{font-family:'Noto Serif Arabic',serif;font-size:1.08rem;font-weight:600;margin:1.8rem 0 .7rem;color:var(--a)}}
.body blockquote{{margin:2rem 0;padding:1.5rem 1.8rem;border-right:4px solid var(--a);background:var(--cream);font-family:'Noto Serif Arabic',serif;font-size:1.05rem;font-weight:600;line-height:1.65;color:var(--ink)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin:2rem 0}}
.sc{{background:var(--paper);padding:1.1rem;text-align:center}}
.scn{{font-family:'Noto Serif Arabic',serif;font-size:1.7rem;font-weight:900;color:var(--a);line-height:1}}
.scl{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.6rem;color:var(--mid);margin-top:.25rem;line-height:1.4}}
.box{{margin:2.2rem 0;padding:1.4rem 1.6rem;background:var(--cream);border:1px solid var(--rule);border-right:4px solid var(--a)}}.box h4{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.72rem;font-weight:700;color:var(--a);margin-bottom:.75rem}}.box p{{font-size:.95rem;line-height:1.85;color:#2a2a3a;margin-bottom:.6rem}}.box p:last-child{{margin-bottom:0}}
.verdict{{margin:2.5rem 0;border:2px solid var(--a);background:var(--paper);overflow:hidden}}
.vt{{background:var(--a);color:#fff;font-family:'Noto Naskh Arabic',sans-serif;font-size:.76rem;padding:.7rem 1.2rem;font-weight:700}}
.vc{{padding:1.3rem 1.5rem}}.vc p{{font-size:.93rem;line-height:1.75;margin-bottom:.6rem;color:#2a2a3a}}
.faq{{margin:2.5rem 0;background:var(--paper);border:1px solid var(--rule);overflow:hidden}}
.faqt{{background:var(--ink);color:#fff;font-family:'Noto Naskh Arabic',sans-serif;font-size:.76rem;padding:.75rem 1.2rem;font-weight:700}}
.fqi{{border-bottom:1px solid var(--rule);padding:.9rem 1.2rem}}.fqi:last-child{{border:none}}
.fqq{{font-family:'Noto Serif Arabic',serif;font-size:.92rem;font-weight:700;color:var(--ink);margin-bottom:.35rem}}
.fqa{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.85rem;color:var(--mid);line-height:1.65}}
.also{{margin:2.5rem 0;padding:1.3rem 1.5rem;background:var(--paper);border:1px solid var(--rule)}}.also h4{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.72rem;font-weight:700;color:var(--ink);border-bottom:2px solid var(--a);padding-bottom:.4rem;margin-bottom:.9rem}}.also ul{{list-style:none;padding:0}}.also li{{border-bottom:1px solid var(--rule);padding:.55rem 0}}.also li:last-child{{border-bottom:none}}.also a{{font-family:'Noto Serif Arabic',serif;font-size:.92rem;font-weight:600;color:var(--a)}}.also a:hover{{color:var(--orient)}}
.au{{margin:2.5rem 0;padding:1.3rem 1.5rem;background:var(--cream);border:1px solid var(--rule);border-right:4px solid var(--a);display:flex;gap:1rem}}
.av{{width:48px;height:48px;border-radius:50%;background:var(--a);flex-shrink:0;display:flex;align-items:center;justify-content:center;font-family:'Noto Serif Arabic',serif;font-size:1.1rem;font-weight:900;color:#fff}}
.an{{font-family:'Noto Serif Arabic',serif;font-size:.95rem;font-weight:700;color:var(--ink)}}
.ar2{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.65rem;color:var(--a);margin-bottom:.4rem}}
.ab{{font-size:.85rem;color:var(--mid);line-height:1.65;margin:0!important}}
.sb{{position:sticky;top:80px}}
.sbl{{margin-bottom:2rem;background:var(--paper);border:1px solid var(--rule);padding:1.2rem}}
.stl{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.72rem;color:var(--ink);border-bottom:2px solid var(--a);padding-bottom:.35rem;margin-bottom:.9rem;font-weight:700}}
.tl{{list-style:none}}.tl li{{border-bottom:1px solid var(--rule);padding:.5rem 0;font-size:.85rem}}
.tl li a{{color:var(--mid);transition:color .2s;display:flex;gap:.4rem;align-items:flex-start;flex-direction:row-reverse}}
.tl li a:hover{{color:var(--a)}}
.tn{{font-family:'Noto Naskh Arabic',sans-serif;font-size:.62rem;color:var(--a);flex-shrink:0}}
.fu{{opacity:0;transform:translateY(16px);transition:opacity .55s,transform .55s}}.fu.vis{{opacity:1;transform:none}}
footer{{background:#1a1a2a;color:#5a5870;padding:2rem;font-family:'Noto Naskh Arabic',sans-serif;font-size:.72rem;border-top:3px solid var(--a)}}
.fi{{max-width:1280px;margin:0 auto;display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem}}
.fl{{display:flex;gap:1.3rem}}.fl a{{color:#5a5870}}.fl a:hover{{color:var(--or)}}
@media(max-width:640px){{.mast{{flex-direction:column}}.layout{{padding:1.5rem 1rem}}.hero__c{{padding:1.5rem 1rem}}}}
</style>
</head>
<body>
<div id="pb"></div>
<div class="top">
  <span>تحليلات جيوسياسية — <strong style="color:var(--or)">القوى والصراعات في القرن الحادي والعشرين</strong></span>
  <span><a href="https://geopolo.com">🇫🇷 Français</a> · <a href="/abonnement.html">الاشتراك</a></span>
</div>
<header class="mast">
  <a href="/" class="logo">geopolô<span>مجلة جيوسياسية استراتيجية مستقلة</span></a>
  <div class="msub">ar.geopolo.com · 2026</div>
</header>
{nav_html}
<div class="hero">
  <img src="{img_url}?w=1400&q=80" alt="{og_title}"/>
  <div class="hero__ov"></div>
  <div class="hero__c">
    <div class="hbadge" style="background:{color}">{badge}</div>
    <h1>{h1}<br><em>{h1_em}</em></h1>
    <p class="hsub">{hsub}</p>
  </div>
</div>
<div class="meta"><div class="metai">
  <span class="mi">✍ <strong>geopolô</strong></span><span class="sep">·</span>
  <span class="mi">📅 <strong>أبريل 2026</strong></span><span class="sep">·</span>
  <span class="mi">⏱ <strong>10 دقائق</strong></span>
</div></div>
<div class="layout">
  <article class="body fu">
{body_html}
{verdict_html}
<div class="also">
<h4>📚 اقرأ أيضاً</h4>
<ul>
{also_items}</ul>
</div>
<div class="faq"><div class="faqt">❓ أسئلة شائعة</div>
{faq_html}</div>
<div class="au"><div class="av" style="font-size:.72rem;letter-spacing:-.03em">geo<br>polô</div><div>
  <div class="an">geopolô</div>
  <div class="ar2">مجلة جيوسياسية استراتيجية مستقلة · ar.geopolo.com</div>
  <p class="ab">تحليلات معمّقة في الجيوسياسة والاستراتيجية الدولية — نقرأ العالم بعيون مستقلة.</p>
</div></div>
  </article>
  <aside class="sb">
    <div class="sbl"><div class="stl">📋 المحتويات</div><ul class="tl">
      <li><a href="#s1"><span class="tn">1.</span> السياق والخلفية</a></li>
      <li><a href="#s2"><span class="tn">2.</span> التحليل المعمّق</a></li>
      <li><a href="#s3"><span class="tn">3.</span> الأبعاد الاستراتيجية</a></li>
      <li><a href="#s4"><span class="tn">4.</span> السيناريوهات والتوقعات</a></li>
    </ul></div>
  </aside>
</div>
<footer><div class="fi">
  <span>© 2026 geopolô · ar.geopolo.com</span>
  <div class="fl"><a href="/">الرئيسية</a><a href="/asie.html">آسيا</a></div>
</div></footer>
<script>
window.addEventListener('scroll',()=>{{const d=document.documentElement;document.getElementById('pb').style.width=(d.scrollTop/(d.scrollHeight-d.clientHeight)*100)+'%'}});
const obs=new IntersectionObserver(e=>{{e.forEach(x=>{{if(x.isIntersecting){{x.target.classList.add('vis');obs.unobserve(x.target)}}}});}},{{threshold:.06}});
document.querySelectorAll('.fu').forEach(el=>obs.observe(el));
</script>
</body></html>"""

# ── Article definitions ────────────────────────────────────────────────────────

ARTICLES = {}

# 1. afrique-strategique-2026
ARTICLES["afrique-strategique-2026"] = dict(
    cat="afrique", color="#c8821a",
    title="لماذا باتت أفريقيا ساحة المنافسة الكبرى في 2026",
    og_title="أفريقيا الاستراتيجية 2026: موارد وقوى كبرى ورهانات جيوسياسية",
    desc="تحليل لأسباب تحوّل أفريقيا إلى ساحة المنافسة بين القوى الكبرى في 2026: الموارد الحيوية، الحضور الصيني والروسي والأمريكي، وتحولات ميزان القوى.",
    keywords="أفريقيا الاستراتيجية 2026, المنافسة الكبرى في أفريقيا, الصين روسيا أفريقيا, موارد أفريقيا الحيوية, جيوسياسة أفريقيا",
    img_url="https://images.unsplash.com/photo-1547471080-7cc2caa01a7e",
    badge="🌍 أفريقيا · استراتيجية",
    h1="لماذا باتت أفريقيا", h1_em="ساحة المنافسة الكبرى في 2026؟",
    hsub="القارة التي تجاهلها العالم لعقود باتت اليوم مركز ثقل للموارد الحيوية والنفوذ الجيوسياسي. الصين وروسيا وأمريكا وأوروبا يتنافسون على حضورها.",
    sections=[
        """<p id="s1">ثلاثة عقود من الإهمال الاستراتيجي النسبي انتهت. أفريقيا لم تعد هامشاً في حسابات القوى الكبرى، بل باتت محور تنافس متعدد الأبعاد يجمع الاقتصاد والأمن والنفوذ السياسي في معادلة واحدة معقدة. ما الذي تغيّر؟</p>
<h2 id="s2">الموارد التي تُعيد رسم الخرائط</h2>
<p>أفريقيا تحتضن <strong>60٪ من الأراضي الزراعية غير المستغلة</strong> في العالم، و30٪ من احتياطيات المعادن الحيوية عالمياً. الكوبالت الكونغولي ضروري لبطاريات السيارات الكهربائية. المانغنيز الغابوني يدخل في صناعة الصلب. الليثيوم الزيمبابوي والتنزاني يُحدّد من يسيطر على ثورة الطاقة القادمة. هذه الموارد تحوّلت من مجرد سلع إلى أدوات نفوذ جيوسياسي.</p>
<p>الصين فهمت هذا مبكراً. منذ مطلع الألفية الثالثة، استثمرت بكين أكثر من <strong>300 مليار دولار</strong> في البنية التحتية الأفريقية عبر مبادرة الحزام والطريق، مقابل ضمان الوصول إلى الموارد. الموانئ والسكك الحديدية والطرق السريعة التي بنتها الصين ليست مجرد مشاريع تنموية، بل شبكة نفوذ تجعل كثيراً من الحكومات الأفريقية مُدانة لبكين.</p>
<h2 id="s3">لاعبون جدد في ساحة قديمة</h2>
<p>روسيا دخلت بأسلوب مختلف: الأمن والسلاح والمرتزقة. مجموعة فاغنر (المُعاد هيكلتها باسم فيلق أفريقيا) نشرت قواتها في مالي وبوركينا فاسو وأفريقيا الوسطى والنيجر. الرسالة واضحة: موسكو تحمي الأنظمة التي تواجه ضغطاً غربياً، مقابل حقوق التنقيب والحضور العسكري. هذا الأسلوب نجح في تهميش التأثير الفرنسي في منطقة الساحل بشكل ملحوظ.</p>
<p>أمريكا تعيد إحياء حضورها بعد سنوات من الانكفاء. مبادرة Partnership for Global Infrastructure تحاول تقديم بديل للنموذج الصيني، مع التركيز على الشفافية وحقوق العمل ومعايير البيئة. لكن التمويل الأمريكي لا يزال أقل بكثير من الصيني، والثقة الأفريقية في الغرب تآكلت بعد عقود من الشروط والوعود غير المنجزة.</p>
<h2 id="s4">الأجيال الجديدة والمعادلة المتغيرة</h2>
<p>العامل الأهم الذي يغيّر الحسابات هو الديموغرافيا. في 2050، ستضم أفريقيا نحو <strong>2.5 مليار نسمة</strong>، يعيش نصفهم في المدن، وأكثر من نصفهم دون سن الثلاثين. هذه الأجيال الجديدة تضغط على حكوماتها لتحويل الموارد الطبيعية إلى رفاه حقيقي، وتعبّر عن رفضها للنماذج الاستعمارية القديمة سواء أكانت غربية أم شرقية.</p>
<p>المفارقة أن القوى الكبرى تتنافس على أفريقيا في الوقت الذي تعيد فيه الشعوب الأفريقية النظر في شروط هذه الشراكات. الساحل شهد موجة انقلابات رفعت شعار «الاستقلال عن فرنسا» مع فتح الأبواب لروسيا. هذه المفارقة تعكس تعقيد المشهد الأفريقي الذي لا يمكن اختزاله في سردية استعمارية-مناهضة للاستعمار بسيطة.</p>""",
    ],
    verdict="أفريقيا 2026 ليست ضحية المنافسة الكبرى بل لاعب يتعلم تشغيل التوازن لصالحه. الدول التي تُجيد إدارة التنافس بين القوى الكبرى — كإثيوبيا وكينيا والمغرب — تحصل على أفضل الشروط. التحدي هو تحويل هذه الفرص إلى تنمية حقيقية تصل إلى المواطن العادي.",
    also_links=[
        ("/articles/guerre-sahel-situation-saggrave.html", "الحرب في الساحل: لماذا يزداد الوضع سوءاً؟"),
        ("/articles/afrique-du-sud-brics.html", "جنوب أفريقيا في بريكس"),
        ("/articles/soudan-or-genocide-eau.html", "السودان: الذهب والإبادة والماء"),
        ("/articles/brics-dedollarisation-economie-mondiale.html", "بريكس وتراجع الدولار"),
    ],
    faq_items=[
        ("ما أهم مورد طبيعي تتنافس عليه القوى الكبرى في أفريقيا؟", "الكوبالت الكونغولي يتصدر القائمة لأهميته في صناعة بطاريات السيارات الكهربائية، يليه الليثيوم والمانغنيز والذهب. لكن الأراضي الزراعية الشاسعة باتت هي الأصل الاستراتيجي الأكثر أهمية على المدى البعيد."),
        ("هل نجحت روسيا في تهميش فرنسا في منطقة الساحل؟", "نعم جزئياً. مالي وبوركينا فاسو والنيجر طردت القوات الفرنسية وفتحت الباب لمجموعة فاغنر الروسية. لكن هذا التحول لم يُحسّن الأوضاع الأمنية؛ حالات العنف ازدادت في المنطقة منذ الانقلابات."),
    ]
)

# 2. chine-soutient-russie
ARTICLES["chine-soutient-russie"] = dict(
    cat="asie", color="#1a8a6e",
    title="لماذا تدعم الصين روسيا في 2026؟ تحليل استراتيجي",
    og_title="لماذا تدعم الصين روسيا: تحالف المصلحة لا المبدأ",
    desc="تحليل أسباب دعم الصين لروسيا رغم الحرب على أوكرانيا: المصالح الاقتصادية، الموقف من النظام الدولي، حدود الدعم الصيني، وما يعنيه هذا للجيوسياسة العالمية.",
    keywords="الصين تدعم روسيا, التحالف الصيني الروسي 2026, بكين وموسكو, حرب أوكرانيا الموقف الصيني, جيوسياسة الصين روسيا",
    img_url="https://images.unsplash.com/photo-1553729784-e91953dec042",
    badge="🇨🇳 الصين · روسيا · التحالفات",
    h1="لماذا تدعم الصين روسيا:", h1_em="تحالف المصلحة لا المبدأ",
    hsub="بكين تؤكد حيادها وتنتقد العقوبات الغربية في الوقت ذاته. خطابان متناقضان يخفيان حساباً استراتيجياً دقيقاً.",
    sections=[
        """<p id="s1">منذ الغزو الروسي لأوكرانيا في فبراير 2022، تسير الصين على حبل دقيق: تُعلن الحياد وتحترم سيادة أوكرانيا من جهة، وترفض العقوبات الغربية على روسيا وتواصل تبادلها التجاري معها من جهة أخرى. هذا ليس تناقضاً، بل سياسة مدروسة تخدم مصالح بكين الاستراتيجية على عدة محاور.</p>
<h2 id="s2">المصالح الاقتصادية: الرابح الأكبر</h2>
<p>منذ العقوبات الغربية، أصبحت الصين المشتري الرئيسي للنفط الروسي المخفَّض السعر. في 2025، استوردت الصين ما يزيد على <strong>2.4 مليون برميل يومياً</strong> من روسيا بأسعار تقل 15-20٪ عن أسعار السوق. هذا يوفر على الصين عشرات المليارات سنوياً ويُعزز احتياطياتها الاستراتيجية من الطاقة. في المقابل، صادرات السلع الصينية لروسيا ارتفعت بنسبة 40٪ لتملأ الفراغ الذي تركته الشركات الغربية.</p>
<p>الاتحاد الاقتصادي الضمني بين موسكو وبكين يبدو رابحاً للطرفين في الأمد القصير. لكن بكين تعي أن هذا الاعتماد الروسي المتزايد عليها يُقوّي أوراقها في أي تفاوض مستقبلي مع موسكو.</p>
<h2 id="s3">الموقف الأيديولوجي: رفض الأحادية الغربية</h2>
<p>الصين وروسيا تتشاركان رؤية جيوسياسية جوهرية: رفض النظام الدولي أحادي القطب الذي يضع أمريكا في مركزه. إعلان الشراكة «بلا حدود» في فبراير 2022 لم يكن مجرد بيان دبلوماسي، بل تعبير عن رغبة مشتركة في إعادة رسم قواعد النظام الدولي. الصين ترفض ما تصفه بـ«الهيمنة الغربية» على المؤسسات الدولية، وتجد في روسيا شريكاً يشاطرها هذا الموقف.</p>
<p>هذا لا يعني تحالفاً أيديولوجياً حميماً. التاريخ بين البلدين معقد ومثقل بالمنافسة على آسيا الوسطى وعلى الزعامة الشيوعية في القرن الماضي. لكنه يعني أن كلا البلدين يرى في الآخر درعاً مناسباً في مواجهة الضغط الغربي.</p>
<h2 id="s4">حدود الدعم: ما الذي لن تفعله الصين؟</h2>
<p>الدعم الصيني لروسيا ليس مطلقاً. بكين لم تُرسل أسلحة فتاكة لموسكو رغم الضغط الروسي، ولم تعترف بضم المناطق الأوكرانية، ولم تُساعد روسيا على تجاوز العقوبات المالية بشكل مباشر. الخطوط الحمراء الصينية تحكمها مصلحة واحدة: <strong>عدم تعريض العلاقات الاقتصادية مع الغرب للخطر</strong>. أوروبا وأمريكا ما زالتا أكبر أسواق صادرات الصين وأهم مصادر التكنولوجيا والاستثمار.</p>
<p>الصين تحسب: دعم روسيا بشكل منفتح سيعني عقوبات غربية على شركاتها، وهذا ثمن تجاري أعلى بكثير مما تكسبه من روسيا. لذا تبقى في المنطقة الرمادية: لا دعم عسكري صريح، لكن تجارة واسعة وغطاء دبلوماسي دائم.</p>""",
    ],
    verdict="الدعم الصيني لروسيا هو تحالف براغماتي تحكمه المصلحة لا الصداقة. بكين تريد روسيا ضعيفة ومُعتمدة عليها، لا قوية ومستقلة. وهي تريد أن تستمر الحرب الأوكرانية في استنزاف الغرب دون أن تدفع هي ثمن الانحياز المباشر.",
    also_links=[
        ("/articles/axe-chine-russie-alliance-opportunisme.html", "المحور الصيني-الروسي: تحالف أم انتهازية؟"),
        ("/articles/chine-croissance-tensions-commerciales-2026.html", "النمو الصيني والتوتر التجاري"),
        ("/articles/axe-sino-russo-iranien.html", "المحور الصيني-الروسي-الإيراني"),
        ("/articles/ukraine-guerre-sans-fin-2026.html", "أوكرانيا: الحرب التي لا تنتهي"),
    ],
    faq_items=[
        ("هل ترسل الصين أسلحة لروسيا؟", "حتى الآن، لم تُثبت أي دولة غربية أن بكين أرسلت أسلحة فتاكة لموسكو. تُشير التقارير إلى تسليم مكونات ذات استخدام مزدوج (مدني-عسكري)، لكن الصين تنفي ذلك وتُقدّم نفسها كوسيط محتمل للسلام."),
        ("هل يمكن للصين أن تُجبر روسيا على وقف الحرب؟", "من الناحية النظرية نعم، لأن موسكو باتت معتمدة اقتصادياً على بكين. لكن بكين لا تجد مصلحة في إجبار موسكو على إنهاء حرب تستنزف الغرب وتُبقي روسيا في موقع ضعيف أمامها."),
    ]
)

# 3. cinq-conflits-surveiller-2026
ARTICLES["cinq-conflits-surveiller-2026"] = dict(
    cat="default", color="#1a8a6e",
    title="خمسة نزاعات تترقّبها العيون في 2026",
    og_title="خمسة نزاعات تترقّبها العيون في 2026: خريطة التوترات الكبرى",
    desc="تحليل خمسة نزاعات مفصلية في 2026: السودان، اليمن، غزة، أوكرانيا، ومضيق تايوان — الديناميكيات والسيناريوهات والتداعيات الجيوسياسية.",
    keywords="نزاعات 2026, حروب العالم 2026, التوترات الدولية, السودان اليمن غزة أوكرانيا تايوان, تحليل جيوسياسي",
    img_url="https://images.unsplash.com/photo-1451187580459-43490279c0fa",
    badge="🌐 النزاعات الكبرى · 2026",
    h1="خمسة نزاعات", h1_em="تترقّبها العيون في 2026",
    hsub="العالم يشهد في 2026 تصاعداً في التوترات المتزامنة. خمسة نزاعات تُشكّل معاً خريطة الأزمات التي تُعيد رسم موازين القوى.",
    sections=[
        """<p id="s1">لم يشهد العالم منذ نهاية الحرب الباردة هذا الكم من النزاعات المتزامنة التي تتشابك مصالح القوى الكبرى فيها. 2026 يُقدّم خمسة ملفات ساخنة تختلف في طبيعتها لكنها تشترك في قدرتها على زعزعة استقرار مناطق بأكملها.</p>
<h2 id="s2">١. السودان: الحرب المنسية</h2>
<p>منذ أبريل 2023، تشن قوات الدعم السريع وجيش السودان حرباً طاحنة أودت بحياة عشرات الآلاف وهجّرت أكثر من <strong>10 ملايين شخص</strong>. الغرب يتابع من بعيد، والدول الإقليمية منقسمة في دعمها. الصراع لم يجذب الاهتمام الكافي رغم كونه من أسوأ الكوارث الإنسانية في العالم.</p>
<h2 id="s3">٢. اليمن: الحرب التي لا تنتهي</h2>
<p>بعد عشر سنوات من الحرب، لا يزال الحوثيون يسيطرون على صنعاء وكثير من الشمال، ولا تزال غاراتهم على الملاحة في البحر الأحمر تُعطّل التجارة العالمية. المفاوضات السعودية-الإيرانية خففت بعض حدة المواجهات لكنها لم تُوقف الحرب.</p>
<h2 id="s4">٣. غزة: الشرق الأوسط يعيد تموضعه</h2>
<p>النزاع في غزة المستمر منذ أكتوبر 2023 أعاد رسم معادلات إقليمية كاملة. الحدود بين إسرائيل ولبنان، التوترات مع إيران، ومستقبل السلطة الفلسطينية — كل هذه الملفات معلّقة في انتظار تسوية غير مرئية.</p>
<h2 id="s5">٤. أوكرانيا: حرب الاستنزاف</h2>
<p>الحرب الأوكرانية دخلت عامها الرابع دون أفق واضح. خطوط المواجهة شبه ثابتة، والدعم الغربي يواجه ضغوطاً داخلية في واشنطن وأوروبا. روسيا تُراهن على صبر استراتيجي أطول من الغرب.</p>
<h2 id="s6">٥. مضيق تايوان: التوتر الأشد خطورة</h2>
<p>المناورات العسكرية الصينية حول تايوان تصاعدت في وتيرتها وحجمها. بكين لم تتخلَّ عن خيار القوة، وواشنطن تُوسّع مبيعاتها العسكرية لتايبيه. الخطأ في الحسابات — لا القرار المتعمد — هو السيناريو الأكثر احتمالاً لأزمة قد تتجاوز المنطقة بأسرها.</p>""",
    ],
    verdict="النزاعات الخمسة تُشكّل معاً ضغطاً متراكماً على نظام العلاقات الدولية. خطر 2026 لا يكمن في نزاع واحد بعينه بل في تزامن عدة أزمات تستنزف إمكانات الوساطة والتدخل الدولي في الوقت ذاته.",
    also_links=[
        ("/articles/guerre-moyen-orient-2026-analyse.html", "الحرب في الشرق الأوسط 2026"),
        ("/articles/ukraine-guerre-sans-fin-2026.html", "أوكرانيا: الحرب التي لا تنتهي"),
        ("/articles/yemen-houthis-mer-rouge.html", "اليمن والحوثيون والبحر الأحمر"),
        ("/articles/taiwan-2026-1.html", "تايوان 2026"),
    ],
    faq_items=[
        ("أيّ هذه النزاعات الخمسة الأخطر على الاستقرار الدولي؟", "مضيق تايوان يحمل الإمكانية الأعلى للتصعيد المباشر بين قوتين نوويتين كبريين. لكن السودان هو الأعلى كُلفة إنسانية دون أي اهتمام دولي يتناسب مع حجم الكارثة."),
        ("هل هناك إمكانية للتسوية السلمية في أي من هذه النزاعات خلال 2026؟", "اليمن الأقرب نسبياً، بفضل الدور السعودي-الإيراني المشترك. أوكرانيا وتايوان والسودان لا ترى أفق تسوية واضح في الأمد المنظور."),
    ]
)

# 4. ia-militaire-2026
ARTICLES["ia-militaire-2026"] = dict(
    cat="asie", color="#1a8a6e",
    title="من يهيمن على الذكاء الاصطناعي العسكري في 2026؟",
    og_title="الذكاء الاصطناعي العسكري 2026: أمريكا والصين وسباق السيطرة",
    desc="من يقود سباق الذكاء الاصطناعي العسكري في 2026؟ تحليل لقدرات الولايات المتحدة والصين وروسيا في الأسلحة الذاتية والتحليل الاستخباراتي والحرب الإلكترونية.",
    keywords="الذكاء الاصطناعي العسكري 2026, الأسلحة الذاتية, سباق التسلح الرقمي, الصين أمريكا ذكاء اصطناعي, الحرب المستقبلية",
    img_url="https://images.unsplash.com/photo-1677442135703-1787eea5ce01",
    badge="🤖 الذكاء الاصطناعي · الأمن",
    h1="من يهيمن على", h1_em="الذكاء الاصطناعي العسكري في 2026؟",
    hsub="الخوارزميات باتت تُحدد أهدافاً، والمسيّرات المستقلة تُنفّذ ضربات، والقرارات العسكرية الكبرى تستعين بالذكاء الاصطناعي. المنافسة على من يصل أولاً تحكم استراتيجيات القوى الكبرى.",
    sections=[
        """<p id="s1">في 2026، لم يعد الذكاء الاصطناعي العسكري مستقبلاً نظرياً بل حاضراً تشغيلياً. أوكرانيا أصبحت مختبراً حياً لتقنيات المسيّرات المستقلة، وإسرائيل استخدمت أنظمة ذكاء اصطناعي في تحديد الأهداف في غزة، والصين أعلنت عن نشر أنظمة قيادة ذكية في سلاح بحريتها.</p>
<h2 id="s2">الولايات المتحدة: الاستثمار الأكبر</h2>
<p>أمريكا تُنفق أكثر من <strong>3 مليارات دولار سنوياً</strong> على الذكاء الاصطناعي الدفاعي عبر برامج وزارة الدفاع. مشروع Maven — الذي بدأ بتحليل صور المسيّرات فوق سوريا والعراق — تطوّر إلى منظومة تدمج الاستخبارات بالقرار الميداني. وتُعدّ DARPA محرّك الابتكار في مجالات الحرب الإلكترونية والمسيّرات الذاتية والتحليل التنبؤي.</p>
<p>لكن لأمريكا مشكلة: بيروقراطية الأخلاقيات العسكرية تُبطئ النشر الفعلي للأنظمة الذاتية. السياسة الأمريكية الرسمية تشترط «إنساناً في حلقة القرار» للأسلحة الفتاكة. هذا يُبقي التفوق التقني الأمريكي حاضراً لكن تطبيقه الميداني مُقيّداً.</p>
<h2 id="s3">الصين: السرعة لا الضوابط</h2>
<p>الصين تُعلن أن هدفها أن تكون القوة الأولى عالمياً في الذكاء الاصطناعي بحلول 2030. بلا قيود أخلاقية مماثلة، تنشر بكين أسلحة شبه ذاتية في بحر الصين الجنوبي وتختبر أنظمة قيادة ذكية على نطاق واسع. ميزتها الأكبر: البيانات. مراقبة 1.4 مليار مواطن توفّر مخزوناً هائلاً من البيانات لتدريب نماذج الذكاء الاصطناعي.</p>
<h2 id="s4">المعضلة الأخلاقية والقانونية</h2>
<p>حين يُقرر الذكاء الاصطناعي القتل، من المسؤول؟ لا القانون الدولي ولا اتفاقيات جنيف تملك إجابة واضحة. المحادثات في مجلس الأمن والأمم المتحدة تتعثر بسبب الخلافات بين القوى الكبرى. الفراغ القانوني يعني أن كل قوة ستضع قواعدها بنفسها.</p>""",
    ],
    verdict="سباق الذكاء الاصطناعي العسكري لا يكسبه من يطوّر أفضل خوارزمية، بل من يُحسن تكاملها في منظومة القرار البشري. أمريكا تقود التقنية، الصين تقود التطبيق، وروسيا تقود الاستعداد للمجازفة. لا أحد يقود البُعد الأخلاقي والقانوني.",
    also_links=[
        ("/articles/ia-militaire-ethique-droit-guerre.html", "حين يُقرّر الذكاء الاصطناعي القتل"),
        ("/articles/ia-militaire-qui-domine-2026.html", "من يهيمن على الذكاء الاصطناعي العسكري؟"),
        ("/articles/cyber-guerre-mondiale.html", "الحرب السيبرانية العالمية"),
        ("/articles/guerre-technologique-usa-chine.html", "الحرب التكنولوجية الأمريكية-الصينية"),
    ],
    faq_items=[
        ("هل هناك أسلحة ذكاء اصطناعي ذاتية تعمل الآن فعلياً في ميادين القتال؟", "نعم. إسرائيل وأوكرانيا ودول أخرى تستخدم أنظمة مسيّرات تتخذ قرارات هجومية باستقلالية جزئية. الخط بين 'إنسان في الحلقة' و'ذاتية كاملة' بات ضبابياً في الممارسة الميدانية."),
        ("ما الفرق بين ما تستخدمه أمريكا والصين حالياً؟", "أمريكا تتفوق في دقة التحليل الاستخباراتي والحرب الإلكترونية. الصين تتفوق في حجم الإنتاج وسرعة النشر الميداني. روسيا تستخدم أنظمة أبسط لكنها أكثر استعداداً لنشرها في مناطق النزاع."),
    ]
)

# 5. inde-chine-guerre-asie
ARTICLES["inde-chine-guerre-asie"] = dict(
    cat="asie", color="#1a8a6e",
    title="الهند والصين: نحو حرب جديدة في آسيا؟",
    og_title="الهند ضد الصين 2026: الحدود الهيمالايا والتوتر المتصاعد",
    desc="تحليل التوترات العسكرية الهندية-الصينية على الحدود الهيمالايا: خط السيطرة الفعلي، الحوادث الأخيرة، المقارنة العسكرية، وسيناريوهات التصعيد في 2026.",
    keywords="الهند الصين حرب 2026, الحدود الهيمالايا, خط السيطرة الفعلي, التوتر الهندي الصيني, جيوسياسة آسيا",
    img_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
    badge="🏔 الهند · الصين · الهيمالايا",
    h1="الهند والصين:", h1_em="نحو حرب جديدة في آسيا؟",
    hsub="الحدود الهيمالايا بين الهند والصين هي أطول خط تماس بين قوتين نوويتين في العالم وأكثرها التباساً وخطورة.",
    sections=[
        """<p id="s1">في يونيو 2020، اشتبك جنود هنود وصينيون في وادي غالوان بالعصي والحجارة والأيدي في معركة دامية لم تُستخدم فيها الأسلحة النارية لتجنب التصعيد. سقط عشرون جندياً هندياً وعدد غير مُعلَن من الصينيين. كان ذلك التذكير الأقسى بأن الحرب الصينية-الهندية عام 1962 لم تُحسم في الذاكرة الاستراتيجية لأي من البلدين.</p>
<h2 id="s2">خط السيطرة الفعلي: الحدود التي لا أحد يعرف أين تقع</h2>
<p>خط السيطرة الفعلي (LAC) يمتد على طول نحو <strong>3488 كيلومتراً</strong> عبر تضاريس من بين الأكثر قسوة في العالم. لا خريطة متفق عليها بين البلدين تُحدد مساره بدقة. هذا الغموض الجغرافي يجعل كل دورية عسكرية محتملة التصادم مع دوريات الطرف الآخر.</p>
<p>بعد حادثة غالوان 2020، تفاوض البلدان على انسحابات جزئية من عدة نقاط ساخنة. لكن الصين بنت بنية تحتية عسكرية واسعة على الجانب الصيني من الخط، تشمل طرقاً وقواعد جوية وقرى استيطانية في مناطق متنازع عليها. هذا التغيير التدريجي في الوقائع الميدانية هو ما يُقلق نيودلهي أكثر من أي مواجهة عسكرية صريحة.</p>
<h2 id="s3">المقارنة العسكرية: القدرات والحسابات</h2>
<p>الجيش الصيني يتفوق عددياً وتقنياً في معظم المؤشرات. لكن الجيش الهندي يملك ميزة التضاريس: معظم القوات الهندية المتمركزة على الحدود مُدرَّبة خصيصاً للقتال في المرتفعات الشاهقة. الحرب الصينية-الهندية المحتملة ليست حرب طائرات ودبابات على سهل مفتوح، بل مواجهة لوجستية في بيئة من أشد بيئات العالم قسوة على البشر والمعدات.</p>
<h2 id="s4">لماذا الحرب الشاملة غير مرجحة رغم التوتر</h2>
<p>الهند والصين تملكان أسلحة نووية، والحرب بينهما ستُدمّر اقتصاديهما في وقت يحتاجان فيه إلى النمو الداخلي. كلاهما يُفضّل الضغط التدريجي على المواجهة الصريحة. لكن هذا لا يُلغي خطر الخطأ في الحسابات، خاصة في ظل وجود رئيسين يواجهان ضغوطاً قومية داخلية ويُدركان أن التراجع سيُفسَّر ضعفاً.</p>""",
    ],
    verdict="الهند والصين تعيشان توتراً مزمناً سيستمر لعقود. الحرب الشاملة مستبعدة، لكن الاشتباكات المحدودة والضغط التدريجي على الخط الحدودي سيبقيان سمة ثابتة في العلاقة بين أكبر ديمقراطيتين في العالم.",
    also_links=[
        ("/articles/inde-vs-chine-militaire.html", "الهند ضد الصين: المقارنة العسكرية"),
        ("/articles/inde-expansion-technologique-ia-2026.html", "الهند والثورة التكنولوجية"),
        ("/articles/asie-chine-inde-coree-triangles.html", "آسيا: الصين والهند وكوريا"),
        ("/articles/chine-puissance-portrait-strategique.html", "الصين: بورتريه القوة العالمية"),
    ],
    faq_items=[
        ("هل للهند والصين تاريخ من الحروب السابقة؟", "نعم. حرب 1962 انتهت بهزيمة هندية مُذلّة وفقدان أراضٍ لا تزال محلَّ نزاع. هذه الهزيمة تُلقي بظلالها على الاستراتيجية الهندية حتى اليوم وتُفسّر الإنفاق الدفاعي الهندي المتسارع."),
        ("ما الخلاف الحدودي الرئيسي بين الهند والصين؟", "الصين تطالب بمنطقة أروناتشال براديش الهندية (تُسمّيها تبت الجنوبية)، والهند تُطالب بمنطقة أكساي تشين التي تسيطر عليها الصين. كلا النزاعين موروث من رسم حدود الاستعمار البريطاني."),
    ]
)

# 6. inde-puissance-emergente
ARTICLES["inde-puissance-emergente"] = dict(
    cat="asie", color="#1a8a6e",
    title="الهند: القوة الصاعدة بين واشنطن وموسكو",
    og_title="الهند قوة صاعدة: الاستقلالية الاستراتيجية بين القوى الكبرى",
    desc="تحليل موقع الهند في النظام الدولي: الاستقلالية الاستراتيجية، العلاقة مع أمريكا وروسيا والصين، ومستقبل القوة الهندية في عالم متعدد الأقطاب.",
    keywords="الهند قوة صاعدة, الاستقلالية الاستراتيجية الهندية, الهند وأمريكا وروسيا, جيوسياسة الهند 2026, مودي السياسة الخارجية",
    img_url="https://images.unsplash.com/photo-1524492412937-b28074a5d7da",
    badge="🇮🇳 الهند · القوى الكبرى",
    h1="الهند:", h1_em="القوة الصاعدة بين واشنطن وموسكو",
    hsub="شريك أمريكا في الإندو-باسيفيك، أكبر مستورد للأسلحة الروسية، منافس الصين في الهيمالايا، رئيس مجموعة G20 — الهند تُتقن لعبة التوازن متعدد الأقطاب.",
    sections=[
        """<p id="s1">نيودلهي تُجسّد مفهوم «الاستقلالية الاستراتيجية» بمهارة نادرة: تشتري الأسلحة من روسيا والولايات المتحدة وإسرائيل وفرنسا في الوقت ذاته. تنضم إلى تحالف Quad مع أمريكا واليابان وأستراليا لمواجهة الصين في الإندو-باسيفيك، بينما ترفض في الوقت نفسه الانضمام إلى أي عقوبات على روسيا.</p>
<h2 id="s2">الموازنة بين الشركاء المتعارضين</h2>
<p>روسيا كانت حتى وقت قريب مصدر <strong>60٪</strong> من واردات الهند العسكرية. لكن الحرب الأوكرانية كشفت هشاشة هذا الاعتماد: قطع الغيار تأخرت، والروبل المنهك قلّل من موثوقية العقود الدفاعية. نيودلهي تُسرّع تنويع مصادر التسليح، مع حرصها على إبقاء روسيا شريكاً استراتيجياً لموازنة الصين.</p>
<p>أمريكا تُغري الهند بعروض التكنولوجيا الدفاعية المتقدمة وبناء المحركات النفاثة محلياً وشراكات أشباه الموصلات. واشنطن تحتاج الهند في مواجهة الصين أكثر مما تحتاجها الهند واشنطن، وهذا يمنح نيودلهي ورقة تفاوضية ثمينة.</p>
<h2 id="s3">الهند في بريكس: الاستفادة من الكل</h2>
<p>الهند عضو في بريكس، العضوية التي يراها البعض تناقضاً مع توجهها الغربي. لكن نيودلهي ترى في بريكس منبراً لتعزيز صوتها في النظام الدولي دون الانحياز الكامل لأي معسكر. الهند صوّتت في الأمم المتحدة ضد قرارات إدانة روسيا، وفي الوقت ذاته استقبلت وزراء الدفاع والخارجية الأمريكيين.</p>
<h2 id="s4">الاقتصاد: محرك القوة الحقيقي</h2>
<p>الهند باتت خامس أكبر اقتصاد عالمياً وتُتوقع أن تصبح ثالث أكبر اقتصاد بحلول 2030. قطاع التكنولوجيا الهندي يُنتج أكبر عدد من الشركات العالمية في مجال البرمجيات وتكنولوجيا المعلومات. هذا الحضور الاقتصادي هو ما يُحوّل الهند من قوة إقليمية إلى قوة عالمية حقيقية، بمعزل عن خياراتها التحالفية.</p>""",
    ],
    verdict="الهند لن تختار بين أمريكا وروسيا والصين. ستواصل الاستفادة من الجميع وبناء قوتها الذاتية بالتوازي. هذا النهج يُزعج حلفاءها لكنه يُمثّل أكثر السياسات الخارجية استدامة لدولة تتطلع إلى مكانة القوى الكبرى.",
    also_links=[
        ("/articles/inde-expansion-technologique-ia-2026.html", "الهند والاستراتيجية التكنولوجية"),
        ("/articles/tsmc-inde-accord-puces-2026.html", "TSMC والهند: اتفاقية غوجارات"),
        ("/articles/inde-vs-pakistan-nucleaire.html", "الهند وباكستان: التوازن النووي"),
        ("/articles/puissances-moyennes-inde-turquie-saoudie-bresil.html", "القوى المتوسطة الصاعدة"),
    ],
    faq_items=[
        ("لماذا ترفض الهند الانضمام للعقوبات على روسيا رغم قربها من الغرب؟", "لأن الهند تعتمد على روسيا لأكثر من نصف تسليحها العسكري، وأي انضمام للعقوبات سيُعرّض هذه الإمدادات للخطر في وقت تواجه فيه تهديداً مزدوجاً من الصين وباكستان."),
        ("هل الهند عضو في الناتو أو في أي تحالف رسمي؟", "لا. الهند لا تنتمي إلى أي تحالف عسكري رسمي. تشارك في Quad (الحوار الأمني الرباعي) مع أمريكا واليابان وأستراليا، لكن Quad ليس تحالفاً عسكرياً رسمياً بل شراكة أمنية غير مُلزِمة."),
    ]
)

# 7. soft-power-chinois
ARTICLES["soft-power-chinois"] = dict(
    cat="asie", color="#1a8a6e",
    title="القوة الناعمة الصينية: الاستراتيجية والأدوات والحدود",
    og_title="القوة الناعمة الصينية 2026: معارك الرواية والنفوذ الثقافي",
    desc="تحليل استراتيجية القوة الناعمة الصينية في 2026: معاهد كونفوشيوس، الإعلام الحكومي، مبادرة الحزام والطريق، وحدود النفوذ الثقافي الصيني عالمياً.",
    keywords="القوة الناعمة الصينية, معاهد كونفوشيوس, إعلام الصين الخارجي, مبادرة الحزام والطريق الثقافية, الدبلوماسية الصينية الناعمة",
    img_url="https://images.unsplash.com/photo-1513415431021-b6a01a3e75b2",
    badge="🇨🇳 الصين · القوة الناعمة",
    h1="القوة الناعمة الصينية:", h1_em="الاستراتيجية والأدوات والحدود",
    hsub="بكين تُنفق 10 مليارات دولار سنوياً على نشر نفوذها الثقافي والإعلامي. النتائج أقل مما تأملت، والمقاومة أكثر مما توقّعت.",
    sections=[
        """<p id="s1">حين اختار جوزيف ناي مصطلح «القوة الناعمة» عام 1990 ليصف القدرة على الجذب لا الإكراه، لم يكن يتخيل أن الصين ستُحوّله إلى مشروع حكومي ضخم. بكين أنفقت منذ 2009 أكثر من <strong>10 مليارات دولار سنوياً</strong> على شبكة من الأدوات الثقافية والإعلامية والأكاديمية لتشكيل صورتها في العالم.</p>
<h2 id="s2">الأدوات: من كونفوشيوس إلى CGTN</h2>
<p>معاهد كونفوشيوس — المنتشرة في أكثر من 150 دولة — تُقدّم تعليم اللغة الصينية والثقافة كواجهة ناعمة. لكنها في الوقت ذاته موضع انتقاد واسع لكونها أذرع للمراقبة الأيديولوجية وأدوات للضغط على الرأي الأكاديمي. دول عديدة من أمريكا إلى السويد وكندا أغلقت معظمها.</p>
<p>قناة CGTN (تلفزيون الصين الدولي) وكالة شينخوا وصحيفة China Daily تُوزَّع مجاناً في إفريقيا وآسيا وأمريكا اللاتينية، وتُقدّم رواية الحكومة الصينية بأسلوب احترافي. لكن مصداقيتها الإعلامية تبقى محدودة لأن المتلقي يعرف أنها إعلام حكومي مُموَّل.</p>
<h2 id="s3">لماذا يفشل الجاذبية الصينية؟</h2>
<p>القوة الناعمة تعمل حين تُعجب الناس بصدق لا حين تُقنعهم بالأموال. هوليوود جذّابة لأنها تُمثّل قيماً يريدها كثيرون: الحرية الفردية والنجاح الشخصي والمغامرة. القيم التي تُروّجها بكين — الاستقرار الحزبي، والتنمية الاقتصادية تحت قيادة مركزية — جذّابة في بعض السياقات الحكومية لكنها لا تُحرّك المشاعر الشعبية.</p>
<p>الأزمات الكبرى أضرّت بالصورة الصينية: كوفيد وأصول الوباء، تيانانمن المُحتفى بذكراه خارجياً، قضية الإيغور في شينجيانغ التي وثّقتها منظمات حقوق الإنسان الدولية. كل هذه الملفات تحدّ من قدرة بكين على بناء رواية جذّابة عالمياً.</p>
<h2 id="s4">حيث تنجح القوة الصينية الناعمة</h2>
<p>الاستثمار الاقتصادي — رغم أنه ليس قوة ناعمة بالمعنى الكلاسيكي — هو أنجع أدوات الصين. الدول التي تعتمد على الصين تجارياً وبنياً تحمي صورة الصين في تصويتات الأمم المتحدة. هذه هي القوة الناعمة الصينية الحقيقية: ليست الثقافة بل الاعتماد الاقتصادي.</p>""",
    ],
    verdict="الصين لم تفشل في القوة الناعمة لأنها لا تمتلك الأدوات، بل لأن القوة الناعمة الحقيقية تنبع من المجتمع لا من الحكومة. ما طوّرته الصين هو قوة ناعمة حكومية — نافعة في العلاقات بين الحكومات، ومحدودة في استمالة الشعوب.",
    also_links=[
        ("/articles/soft-power-chinois.html", "القوة الناعمة الصينية"),
        ("/articles/chine-puissance-portrait-strategique.html", "الصين: بورتريه القوة العالمية"),
        ("/articles/tiktok-guerre-information.html", "تيك توك وحرب المعلومات"),
        ("/articles/hallyu-coree-soft-power.html", "الموجة الكورية: القوة الناعمة الآسيوية البديلة"),
    ],
    faq_items=[
        ("كم تُنفق الصين على قوتها الناعمة؟", "التقديرات تتراوح بين 7 و10 مليارات دولار سنوياً، لكن الأرقام الدقيقة غير معلنة. يشمل ذلك الإعلام الخارجي والمنح الدراسية ومعاهد كونفوشيوس والمبادرات الثقافية والدبلوماسية الرياضية."),
        ("ما الفرق بين القوة الناعمة الأمريكية والصينية؟", "القوة الناعمة الأمريكية تأتي أساساً من القطاع الخاص: هوليوود والجامعات والموسيقى والتكنولوجيا. الصينية تأتي من الحكومة مباشرة. هذا الفارق يمنح الأمريكية مصداقية أعلى لدى الشعوب."),
    ]
)

# 8. pays-dangereux-monde-2026
ARTICLES["pays-dangereux-monde-2026"] = dict(
    cat="default", color="#b83232",
    title="أخطر دول العالم في 2026: تصنيف وتحليل",
    og_title="أخطر دول العالم في 2026: الصراعات والجريمة وعدم الاستقرار",
    desc="تصنيف وتحليل أخطر دول العالم في 2026 بناءً على مؤشرات الصراع المسلح والإرهاب والجريمة المنظمة. دليل جيوسياسي شامل لخريطة التوترات الكبرى.",
    keywords="أخطر دول العالم 2026, مناطق النزاع المسلح, مؤشر السلام العالمي, البلدان الأكثر خطورة, خريطة التوترات",
    img_url="https://images.unsplash.com/photo-1529107386315-e1a2ed48a620",
    badge="⚠️ الأمن الدولي · 2026",
    h1="أخطر دول العالم في 2026:", h1_em="تصنيف وتحليل جيوسياسي",
    hsub="قياس خطورة دولة ما يجمع النزاعات المسلحة والإرهاب والجريمة المنظمة والهشاشة المؤسسية. تسعة بلدان تتصدر خريطة التوترات في 2026.",
    sections=[
        """<p id="s1">تقييم «خطورة» دولة ما ليس تمريناً أكاديمياً. يعتمد المحللون الجيوسياسيون على مؤشرات معيارية تجمع بيانات من مصادر مستقلة: مؤشر السلام العالمي (GPI)، تقارير وزارات الخارجية الغربية، بيانات الأمم المتحدة حول النزاعات، ومنظمات مراقبة حقوق الإنسان.</p>
<h2 id="s2">الدول الأكثر خطورة في 2026</h2>
<p><strong>١. السودان</strong> — حرب أهلية شاملة بين الجيش وقوات الدعم السريع. أكثر من 10 ملايين نازح، مجاعة تهدد مناطق واسعة، وانهيار شبه كامل للدولة في مناطق النزاع.</p>
<p><strong>٢. اليمن</strong> — عشر سنوات من الحرب متعددة الأطراف. الحوثيون يسيطرون على الشمال وينفّذون هجمات على الملاحة الدولية. البنية التحتية مُدمَّرة والاقتصاد منهار.</p>
<p><strong>٣. ميانمار</strong> — انقلاب 2021 أشعل مقاومة مسلحة واسعة. الجيش يخوض حروباً على جبهات متعددة مع تحالفات من المجموعات العرقية المسلحة. الأوضاع الإنسانية كارثية.</p>
<p><strong>٤. أفغانستان</strong> — حكم طالبان يُفاقم الأزمات الاقتصادية والإنسانية. بؤرة استقطاب للتطرف المسلح وتهريب المخدرات رغم الهدوء الأمني النسبي.</p>
<p><strong>٥. الصومال</strong> — حركة الشباب تسيطر على مناطق واسعة وتُنفّذ هجمات انتحارية متكررة في مقديشو. الحكومة الاتحادية هشّة وتعتمد على دعم خارجي.</p>
<h2 id="s3">المنطقة الأعلى خطورة إجمالاً</h2>
<p>منطقة الساحل الأفريقي (مالي وبوركينا فاسو والنيجر وتشاد) تمثّل في مجموعها الكتلة الجغرافية الأعلى خطورة في العالم: غياب الدولة، انتشار جماعات مسلحة متعددة، جفاف وأزمة غذاء هيكلية، وغياب أفق التسوية.</p>
<h2 id="s4">التمييز بين أنواع الخطر</h2>
<p>دولة خطرة على مواطنيها ليست بالضرورة خطرة على الزوار الأجانب، والعكس صحيح. العراق مثلاً فيه مناطق آمنة نسبياً للسياح (كربلاء وأربيل)، بينما تكون دول ذات مؤشرات سلام جيدة خطرة للناشطين والصحفيين بسبب القمع السياسي.</p>""",
    ],
    verdict="خريطة الخطر العالمي في 2026 تكشف نمطاً ثابتاً: أكثر البلدان خطورة هي التي فشلت دولها في توفير الحدّ الأدنى من الخدمات والأمن لمواطنيها، فنشأ فراغ ملأته الجماعات المسلحة والجريمة المنظمة. الحلول السياسية والاقتصادية لا العسكرية هي المسار الوحيد للاستقرار.",
    also_links=[
        ("/articles/cinq-conflits-surveiller-2026.html", "خمسة نزاعات تترقّبها العيون"),
        ("/articles/guerre-sahel-situation-saggrave.html", "الحرب في الساحل"),
        ("/articles/zones-dangereuses-monde.html", "أخطر مناطق العالم"),
        ("/articles/soudan-or-genocide-eau.html", "السودان: الذهب والإبادة والماء"),
    ],
    faq_items=[
        ("كيف يُقاس مؤشر السلام العالمي؟", "يعتمد مؤشر السلام العالمي (GPI) الصادر عن معهد الاقتصاد والسلام على 23 مؤشراً تشمل: حدة النزاعات الداخلية والخارجية، الإنفاق العسكري، الجريمة المنظمة، الاستقرار السياسي، وانتهاكات حقوق الإنسان."),
        ("هل يعني تصنيف دولة كـ'خطرة' أنه لا يجب زيارتها مطلقاً؟", "لا. معظم الدول الواردة في تصنيفات الخطر تملك مناطق آمنة نسبياً. لكن أي زيارة تستلزم استشارة تحذيرات السفر الرسمية وتأمين مناسب وتحضيراً مسبقاً دقيقاً."),
    ]
)

# 9. pays-eviter-2026
ARTICLES["pays-eviter-2026"] = dict(
    cat="default", color="#b83232",
    title="دول يجب تجنّبها في 2026: دليل المناطق عالية الخطورة",
    og_title="دليل السفر 2026: دول وجب تجنّبها للمسافر الواعي",
    desc="دليل شامل للمسافرين حول الدول الأكثر خطورة في 2026: مناطق النزاع المسلح، الإرهاب، الخطف، وتحذيرات الخارجية الرسمية. معلومات جيوسياسية للسفر الآمن.",
    keywords="دول تجنّبها 2026, مناطق خطرة للسفر, تحذيرات سفر 2026, السفر الآمن جيوسياسة, مناطق النزاع المسلح",
    img_url="https://images.unsplash.com/photo-1436491865332-7a61a109cc05",
    badge="✈️ السفر الآمن · 2026",
    h1="دول يجب تجنّبها في 2026:", h1_em="الدليل العملي للمسافر الواعي",
    hsub="ليس كل الوجهات سواء. بعض الدول تحمل مخاطر حقيقية على حياة الزوار. دليل مبني على بيانات رسمية من وزارات الخارجية والمنظمات الدولية.",
    sections=[
        """<p id="s1">قبل أي رحلة إلى منطقة غير مألوفة، الخطوة الأولى هي الاطلاع على تحذيرات السفر الرسمية. وزارات الخارجية في فرنسا والمملكة المتحدة والولايات المتحدة وكندا وأستراليا تُصدر تقييمات دورية تصنّف الدول من «توخّ الحذر» إلى «لا تسافر إطلاقاً». هذه الدليل يعتمد على هذه التصنيفات ويُضيف إليها التحليل الجيوسياسي.</p>
<h2 id="s2">الفئة الأولى: «لا تسافر» — مناطق النزاع الشامل</h2>
<p><strong>السودان</strong>: الحرب الأهلية تشمل الخرطوم وأجزاء واسعة من دارفور والجزيرة. الرحلات الجوية الدولية شبه متوقفة. لا قنصليات تعمل بشكل طبيعي.</p>
<p><strong>اليمن</strong>: صنعاء ومعظم الشمال تحت سيطرة الحوثيين. عدن والجنوب أكثر استقراراً نسبياً لكنها ليست آمنة. خطر الخطف وألغام الطرق مرتفع.</p>
<p><strong>ميانمار</strong>: الجيش يُقيّد حركة الأجانب والاضطرابات مستمرة. بعض المناطق السياحية التقليدية كانغون وباغان أقل خطورة لكن الوضع غير مضمون.</p>
<h2 id="s3">الفئة الثانية: حذر شديد — مناطق غير مستقرة</h2>
<p><strong>ليبيا</strong>: طرابلس فيها بعض الحضور الدبلوماسي لكن الميليشيات منتشرة. مناطق الجنوب خطرة جداً. خطر الخطف وارد للأجانب.</p>
<p><strong>هايتي</strong>: عصابات تُسيطر على أجزاء كبيرة من بورت أو برنس. الدولة منهارة فعلياً. معدلات الجريمة بين الأعلى في العالم.</p>
<p><strong>إيران</strong> (للجنسيات المزدوجة): خطر الاحتجاز التعسفي مرتفع. عدة دول غربية تُحذّر مواطنيها ذوي الجنسية الإيرانية المزدوجة بصورة خاصة.</p>
<h2 id="s4">القاعدة الذهبية للمسافر</h2>
<p>حتى في الوجهات «الآمنة» نسبياً: ثلاثة مبادئ تُنقذ الأرواح — <strong>التأمين المناسب</strong> (يشمل الإجلاء الطبي)، <strong>تسجيل الرحلة</strong> في قنصلية بلدك، و<strong>معرفة مخرج الطوارئ</strong> قبل الوصول. المسافر الواعي لا يكتفي بقراءة المنتجعات على وسائل التواصل.</p>""",
    ],
    verdict="الخطر الجيوسياسي ليس ثابتاً. دولة آمنة اليوم قد تنزلق إلى عدم الاستقرار خلال أشهر. المراقبة المستمرة للأوضاع وإبقاء خطط الطوارئ محدَّثة هو ما يُميّز المسافر المحترف.",
    also_links=[
        ("/articles/pays-dangereux-monde-2026.html", "أخطر دول العالم في 2026"),
        ("/articles/tourisme-zones-conflit.html", "السياحة المظلمة"),
        ("/articles/voyage-zones-tensions-conseils.html", "السفر إلى مناطق التوتر"),
        ("/articles/zones-dangereuses-monde.html", "أخطر مناطق العالم"),
    ],
    faq_items=[
        ("أين أجد تحذيرات السفر الرسمية المحدّثة؟", "الجهات الرسمية الأفضل: France Diplomatie (فرنسا)، FCDO (بريطانيا)، Travel.State.Gov (أمريكا)، SmartTraveller (أستراليا). كلها تُحدَّث بانتظام وتُقدّم تصنيفات واضحة."),
        ("هل التأمين السياحي العادي يُغطّي مناطق النزاع؟", "لا. التأمين السياحي المعياري يستثني صراحةً مناطق الحرب والنزاعات المسلحة. للسفر إلى مناطق خطرة يُلزَم الحصول على تأمين متخصص يشمل الإجلاء الطبي والأمني."),
    ]
)

# 10. index-serie
ARTICLES["index-serie"] = dict(
    cat="default", color="#1a8a6e",
    title="تحليلات جيوسياسية معمّقة: فهرس المقالات",
    og_title="فهرس التحليلات الجيوسياسية — geopolô",
    desc="فهرس شامل لأبرز التحليلات الجيوسياسية المعمّقة على ar.geopolo.com: القوى الكبرى، النزاعات، التكنولوجيا، الاقتصاد والجيوسياسة.",
    keywords="تحليلات جيوسياسية, مقالات جيوسياسية عربية, geopolô تحليلات, السياسة الدولية بالعربية",
    img_url="https://images.unsplash.com/photo-1451187580459-43490279c0fa",
    badge="📚 فهرس التحليلات",
    h1="تحليلات جيوسياسية معمّقة", h1_em="فهرس المقالات والملفات الاستراتيجية",
    hsub="مجلة geopolô تُقدّم تحليلات معمّقة في الجيوسياسة والاستراتيجية الدولية. هذا الفهرس يجمع أبرز ملفاتنا الاستراتيجية.",
    sections=[
        """<p id="s1">geopolô مجلة جيوسياسية استراتيجية مستقلة تُقدّم تحليلات بالعربية والفرنسية. نؤمن بأن فهم العالم لا يتوقف على اللغة، وأن القارئ العربي يستحق تحليلاً بعمق المصادر الإنجليزية والفرنسية.</p>
<h2 id="s2">الملفات الاستراتيجية الكبرى</h2>
<p>نُغطي خمسة محاور رئيسية: <strong>آسيا والمنافسة الصينية-الأمريكية</strong>، <strong>الشرق الأوسط والنزاعات الإقليمية</strong>، <strong>أفريقيا وسباق الموارد</strong>، <strong>أوروبا وأزمة أوكرانيا</strong>، <strong>التكنولوجيا والذكاء الاصطناعي والجيوسياسة</strong>.</p>
<h2 id="s3">منهجية التحليل</h2>
<p>كل تحليل يعتمد على مصادر متعددة: الصحافة المتخصصة، الأبحاث الأكاديمية، تقارير مراكز الفكر الكبرى (IISS، SIPRI، Brookings، ECFR)، وقراءة التصريحات الرسمية والوثائق الحكومية. نُميّز بين الحقيقة والتحليل والتوقع.</p>
<h2 id="s4">كيف تستخدم هذا الفهرس</h2>
<p>يمكنك تصفّح المقالات حسب المنطقة الجغرافية عبر القائمة العلوية، أو البحث عن موضوع بعينه عبر الكلمات المفتاحية. كل مقال يحتوي على قسم «اقرأ أيضاً» يُرشدك إلى المقالات المتعلقة بالموضوع ذاته لبناء فهم متكامل.</p>""",
    ],
    verdict=None,
    also_links=[
        ("/articles/grandes-puissances-2050.html", "القوى الكبرى في 2050"),
        ("/articles/monde-multipolaire.html", "العالم متعدد الأقطاب"),
        ("/articles/rivalite-usa-chine-guerre-systemique.html", "المنافسة الأمريكية-الصينية"),
        ("/articles/cinq-conflits-surveiller-2026.html", "خمسة نزاعات تترقّبها العيون"),
    ],
    faq_items=[
        ("ما الفرق بين ar.geopolo.com وgeopolo.com؟", "geopolo.com هو الموقع الفرنسي، وar.geopolo.com هو النسخة العربية الكاملة. المحتوى مُكيَّف لا مُترجَم حرفياً، مع مراعاة السياق والاهتمامات الخاصة بالقارئ العربي."),
        ("هل التحليلات متاحة مجاناً؟", "معظم التحليلات متاح مجاناً. بعض الملفات المعمّقة الحصرية متاحة للمشتركين فقط عبر /abonnement.html."),
    ]
)

# 11. destinations-dangereuses-fascinantes
ARTICLES["destinations-dangereuses-fascinantes"] = dict(
    cat="default", color="#c8821a",
    title="الوجهات الخطرة والرائعة: دليل السفر غير التقليدي",
    og_title="أفضل الوجهات الخطرة والرائعة في 2026: للمسافر الجريء",
    desc="دليل الوجهات السياحية الخطرة والرائعة في 2026: إثيوبيا، كولومبيا، جورجيا، العراق وغيرها. الجاذبية وراء القيود وكيف تُدير مخاطر السفر غير التقليدي.",
    keywords="وجهات سياحية خطرة 2026, سياحة المغامرة, السفر إلى مناطق التوتر, إثيوبيا جورجيا كولومبيا سياحة, سياحة غير تقليدية",
    img_url="https://images.unsplash.com/photo-1488085061387-422e29b40080",
    badge="🌍 سياحة المغامرة · 2026",
    h1="الوجهات الخطرة والرائعة:", h1_em="للمسافر الجريء والواعي",
    hsub="بعض أجمل وجهات العالم تخفي خلفها تحذيرات سفر. لكن المسافر المُعدّ جيداً يُدير المخاطر لا يتجاهلها.",
    sections=[
        """<p id="s1">الفضول الإنساني لا يعترف بالتحذيرات الحمراء. الأماكن التي تُثير فضولنا أكثر ما تكون خطرة أو غير مألوفة. لكن ثمة فرق جوهري بين المجازفة العمياء والمغامرة المُحسوبة. دليلنا يعترف بالجاذبية ويأخذ المخاطر بجدية.</p>
<h2 id="s2">إثيوبيا: الجمال في عين الأزمة</h2>
<p>حرب تيغراي (2020-2022) دمّرت مناطق واسعة من شمال إثيوبيا. لكن أديس أبابا ومرتفعات لاليبيلا وبحيرة تانا والجنوب الأفريقي لا تزال تجارب سياحية استثنائية. الحضارات الأكسومية والكنائس المنحوتة في الصخر وتنوع الثقافات الإثيوبية تجعلها وجهة فريدة. الخطوط السياحية تعمل، لكن استشارة الوضع الأمني محلياً ضرورية.</p>
<h2 id="s3">كولومبيا: من عاصمة الكوكايين إلى وجهة السياحة</h2>
<p>كولومبيا التسعينيات — مملكة الكارتيلات — تحوّلت جزئياً. بوغوتا وميدلّين وكارتاخينا وجهات سياحية تستقطب ملايين الزوار سنوياً. لكن الخارج من المدن الكبرى يدخل في مناطق لا تزال تعاني من نشاط جماعات مسلحة. القاعدة: المدن الكبرى مقبولة، الأرياف النائية تحتاج تحقيقاً مسبقاً.</p>
<h2 id="s4">جورجيا: بوابة القوقاز</h2>
<p>جورجيا واحدة من الوجهات غير المكتشفة في أوروبا. تبليسي مدينة رائعة تجمع التراث السوفيتي والكنائس القوقازية والطهي الفريد. أبخازيا وأوسيتيا الجنوبية مناطق انفصالية تحت نفوذ روسي يجب تجنّبها تماماً. بقية جورجيا آمنة نسبياً.</p>
<h2 id="s5">العراق: ما وراء العنوان</h2>
<p>أربيل في كردستان العراق وجهة سياحية متطورة بها فنادق دولية وأمان نسبي. كربلاء والنجف وجهتا حج مليونية لمسلمي العالم. بغداد تتحسن تدريجياً لكنها لا تزال تستلزم احتياطات أمنية مشددة. مناطق الجنوب والغرب متفاوتة الأمان.</p>""",
    ],
    verdict="الوجهات غير التقليدية تُكافئ المسافر الجريء بتجارب أعمق وأصدق من المناطق السياحية المُعلَّبة. لكن المسافر الجريء الحقيقي هو من يُعدّ نفسه جيداً لا من يُهمل المخاطر.",
    also_links=[
        ("/articles/pays-eviter-2026.html", "دول يجب تجنّبها في 2026"),
        ("/articles/tourisme-zones-conflit.html", "السياحة في مناطق النزاع"),
        ("/articles/voyage-zones-tensions-conseils.html", "نصائح السفر إلى مناطق التوتر"),
        ("/articles/pays-dangereux-monde-2026.html", "أخطر دول العالم 2026"),
    ],
    faq_items=[
        ("ما أهم نصيحة للمسافر إلى وجهة خطرة؟", "الإعداد المسبق هو كل شيء: تسجيل الرحلة في قنصلية بلدك، تأمين مناسب يشمل الإجلاء الطبي، معرفة مخرج الطوارئ، وإبلاغ شخص موثوق بخطتك اليومية."),
        ("هل السياحة في مناطق بعد النزاع ممكنة؟", "نعم، وكثيراً ما تكون تجربة إنسانية عميقة. كمبوديا بعد الخمير الحمر، رواندا بعد الإبادة، كولومبيا بعد الكارتيلات — كلها مثالة ناجحة على تحوّل المناطق السابقة من الخطورة إلى الجاذبية السياحية."),
    ]
)

def main():
    for slug, data in ARTICLES.items():
        path = os.path.join(DIR, f"{slug}.html")
        html = make_article(slug=slug, **data)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ {slug}.html")
    print(f"\n✅ {len(ARTICLES)} articles reconstruits.")

if __name__ == "__main__":
    main()
