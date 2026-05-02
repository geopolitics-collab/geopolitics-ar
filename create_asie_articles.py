#!/usr/bin/env python3
"""Create 13 missing Asia/military articles and inject them into asie.html."""
import os
from bs4 import BeautifulSoup

DIR      = "/workspaces/geopolitics-ar"
ARTICLES = os.path.join(DIR, "articles")

COLOR   = "#1a8a6e"
TAG     = "آسيا"

PHOTO   = "https://pub-a7b1a75f72ab40548a0709f708ca2678.r2.dev/Nasser.jpg"

SUBSCRIBE_JS = """function subscribeGeo(form, lang) {
  lang = lang || 'ar';
  var input = form.querySelector('input[type="email"]');
  var btn   = form.querySelector('button[type="submit"]');
  var msg   = form.parentElement.querySelector('.nl-msg') ||
              form.nextElementSibling ||
              (function(){ var p=document.createElement('p'); p.className='nl-msg'; form.parentNode.insertBefore(p,form.nextSibling); return p; })();
  var email = input ? input.value.trim() : '';
  if (!email || !/^[^@]+@[^@]+\\.[^@]+$/.test(email)) {
    msg.innerHTML = '<span style="color:#e05a2b">⚠️ يرجى إدخال بريد إلكتروني صحيح</span>';
    if(input) input.focus();
    return false;
  }
  var origText = btn ? btn.textContent : '';
  if (btn) { btn.textContent = '⏳...'; btn.disabled = true; }
  msg.innerHTML = '';
  fetch('https://floral-math-8fc3.nasseralsabri.workers.dev/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email, lang: lang })
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    if (data.message || data.success) {
      msg.innerHTML = '<span style="color:#1a8a6e;font-family:var(--sans,sans-serif);font-size:.85rem">✅ تم الاشتراك بنجاح — شكراً!</span>';
      if(input) input.value = '';
      if(btn)   { btn.textContent = '✓ تم'; btn.style.background='#1a8a6e'; }
    } else {
      var errMsg = data.error || data.message || 'حدث خطأ';
      if(errMsg.toLowerCase().includes('already') || errMsg.includes('موجود')) {
        msg.innerHTML = '<span style="color:#c8920a;font-family:var(--sans,sans-serif);font-size:.85rem">ℹ️ هذا البريد مشترك بالفعل</span>';
      } else {
        msg.innerHTML = '<span style="color:#e05a2b;font-family:var(--sans,sans-serif);font-size:.85rem">⚠️ ' + errMsg + '</span>';
      }
      if(btn) { btn.textContent = origText; btn.disabled = false; }
    }
  })
  .catch(function() {
    msg.innerHTML = '<span style="color:#e05a2b;font-family:var(--sans,sans-serif);font-size:.85rem">❌ خطأ في الاتصال — حاول مجدداً</span>';
    if(btn) { btn.textContent = origText; btn.disabled = false; }
  });
  return false;
}"""

ARTICLES_DATA = [
    {
        "slug": "armes-hypersoniques-revolution-guerre",
        "title": "الأسلحة ال極音速: ثورة تُعيد رسم قواعد الحرب الحديثة",
        "title_full": "الأسلحة الفائقة السرعة — ثورة تُعيد رسم قواعد الحرب الحديثة",
        "desc": "الصواريخ الفائقة السرعة تتجاوز 5 أضعاف سرعة الصوت وتجعل منظومات الدفاع الجوي التقليدية عاجزة — كيف تُعيد روسيا والصين والولايات المتحدة رسم قواعد الصراع المسلح؟",
        "img": "https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?w=1200&q=80",
        "body": """
<h2>ما هي الأسلحة الفائقة السرعة؟</h2>
<p>الأسلحة الفائقة السرعة (Hypersonic) هي أي مركبة تتحرك بسرعة تتجاوز 5 أضعاف سرعة الصوت (ماخ 5)، أي أكثر من 6100 كيلومتر في الساعة. غير أن ما يُميزها ليس السرعة وحدها، بل القدرة على المناورة والتحرك بمسارات غير متوقعة، مما يجعل اعتراضها شبه مستحيل بالمنظومات الحالية.</p>
<p>تنقسم هذه الأسلحة إلى صنفين رئيسيين: المركبات الانزلاقية (HGV) التي تُطلق من الفضاء وتنزلق نحو هدفها، والصواريخ الجوالة الفائقة السرعة (HCM) التي تحلق داخل الغلاف الجوي طوال مسارها.</p>

<h2>السباق الثلاثي: روسيا والصين وأمريكا</h2>
<p>روسيا أعلنت تشغيل صاروخ "أفانغارد" عام 2019، وهو مركبة انزلاقية تحمل رأساً نووياً بسرعة ماخ 27. وفي عام 2021 كشفت الصين عن تجربة صاروخ فائق السرعة يحلق حول الكرة الأرضية قبل أن يضرب هدفه، مما أثار قلقاً بالغاً في واشنطن. أما الولايات المتحدة فقد ضخّت مليارات الدولارات في برامج مثل ARRW وHAWC لاستعادة التفوق.</p>

<h2>لماذا تُفكك هذه الأسلحة توازن الردع؟</h2>
<p>منظومات الدفاع الصاروخي الحالية — كـ THAAD وPatriot — صُممت لاعتراض الصواريخ الباليستية التقليدية التي تسلك مسارات منحنية يمكن حسابها. أما الصواريخ الفائقة السرعة فتتحرك بمرونة كاملة، مما يُلغي قيمة هذه المنظومات.</p>
<p>هذا يعني أن أي قاعدة عسكرية أو حاملة طائرات أو مركز قيادة باتت معرّضة للضرب في غضون دقائق دون سابق إنذار فعلي، مما يُقلّص زمن صنع القرار إلى الحد الأدنى ويرفع خطر الاستجابة الآلية الخاطئة.</p>

<h2>الأثر الاستراتيجي في آسيا</h2>
<p>في منطقة المحيط الهادئ، تُغير هذه الأسلحة معادلة التايوان والبحر الجنوبي لجنوب الصين. فالصين قادرة نظرياً على شلّ حاملات الطائرات الأمريكية بضربة واحدة قبل وصولها إلى النطاق القتالي. هذا يُكبّل قدرة واشنطن على التدخل ويمنح بكين هامشاً أوسع للمناورة العسكرية.</p>

<h2>هل من دفاع ممكن؟</h2>
<p>تستثمر الولايات المتحدة في أنظمة ليزر عالي الطاقة وشبكات استشعار فضائي متكاملة للكشف المبكر. لكن الفجوة التقنية لا تزال واسعة؛ إذ يقول الخبراء إن التفوق الهجومي سيبقى في صالح المهاجم لعقد على الأقل. ما يعني أن الردع النووي يعود إلى الواجهة كضمانة أخيرة لمنع التصعيد.</p>
"""
    },
    {
        "slug": "chine-invasion-taiwan-probabilite",
        "title": "احتمال غزو الصين لتايوان: تقييم استراتيجي 2026",
        "title_full": "احتمال غزو الصين لتايوان — تقييم استراتيجي معمّق 2026",
        "desc": "هل ستجرؤ الصين على غزو تايوان؟ تحليل معمّق لعوامل الردع والتصعيد والنوافذ الزمنية التي تُحدد مصير أخطر أزمة جيوسياسية في القرن الحادي والعشرين.",
        "img": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=1200&q=80",
        "body": """
<h2>تايوان: تقاطع الهوية والمصالح الاستراتيجية</h2>
<p>تايوان ليست مجرد جزيرة مساحتها 36 ألف كيلومتر مربع — إنها المصنع الأول للرقائق الإلكترونية المتطورة عالمياً عبر شركة TSMC، وبوابة الاستراتيجية الصينية نحو المحيط الهادئ، وفي الوقت ذاته رمز السيادة الصينية في الخطاب الرسمي لبكين.</p>
<p>الرئيس شي جين بينغ أعلن صراحة أن "إعادة التوحيد" هدف لا تنازل عنه، غير أن الغزو العسكري يظل خياراً محفوفاً بمخاطر وجودية للحزب الشيوعي ذاته.</p>

<h2>عوامل تُحفّز التدخل</h2>
<p>يرى المحللون الاستراتيجيون أن النافذة العسكرية الصينية المثلى تمتد بين 2027 و2035، حين تكتمل تحديثات جيش التحرير الشعبي. كذلك تُشكّل أي خطوات نحو استقلال رسمي تايواني "خطاً أحمر" قد يُجبر بكين على التصرف. أضف إلى ذلك الضغوط الداخلية لتحويل الانتباه عن الأزمات الاقتصادية.</p>

<h2>عوامل الردع الفاعلة</h2>
<p>أبرز عوامل الردع هي التكلفة الاقتصادية الكارثية: عقوبات غربية ستُجمّد نصف الاحتياطي الصيني البالغ 3.2 تريليون دولار، وقطع وصول بكين للتقنيات الغربية الحيوية. علاوة على ذلك، تُشير التقديرات إلى أن عملية إنزال برمائية ضد جزيرة محصّنة ستُكبّد الصين خسائر بشرية ضخمة، مما قد يُزعزع الاستقرار الداخلي.</p>

<h2>السيناريو الأرجح</h2>
<p>معظم المحللين يُرجّحون أن بكين ستُصعّد الضغط العسكري والاقتصادي والسيبراني دون غزو مباشر، مراهنةً على استنزاف التايوانيين معنوياً وتقليص الدعم الأمريكي بمرور الوقت. السيناريو الأخطر ليس قرار الغزو المتعمد، بل الانزلاق غير المقصود نحو مواجهة عسكرية جراء خطأ في الحسابات.</p>
"""
    },
    {
        "slug": "cinq-conflits-guerre-mondiale",
        "title": "خمسة بؤر توتر قادرة على إشعال حرب عالمية ثالثة",
        "title_full": "خمسة بؤر توتر قادرة على إشعال حرب عالمية ثالثة — تحليل 2026",
        "desc": "من تايوان إلى كشمير مروراً بشبه الجزيرة الكورية وبحر الصين الجنوبي — خمسة ملفات يمكن لأي منها أن يُشعل مواجهة كبرى بين القوى النووية.",
        "img": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1200&q=80",
        "body": """
<h2>البؤرة الأولى: مضيق تايوان</h2>
<p>تايوان هي البؤرة الأكثر احتمالاً لتحوّل الأزمة إلى حرب مفتوحة. تواجه الولايات المتحدة معضلة الغموض الاستراتيجي: هل ستتدخل عسكرياً؟ أي تحرك صيني خاطئ وأي إجابة أمريكية متسرعة قد يُطلقان سلسلة تصعيد لا عودة منها.</p>

<h2>البؤرة الثانية: شبه الجزيرة الكورية</h2>
<p>كوريا الشمالية تمتلك الآن ترسانة نووية مقدّرة بـ50 رأساً ووسائل إيصال متنوعة. أي استفزاز يتجاوز العتبة الخاطئة قد يدفع سيئول أو طوكيو — أو واشنطن — إلى خيارات وقائية ذات عواقب وخيمة.</p>

<h2>البؤرة الثالثة: بحر الصين الجنوبي</h2>
<p>الصين تُحكم قبضتها على جزر متنازع عليها وتستفز الفلبين والفيتنام وماليزيا. أي حادثة بحرية كتصادم سفن أو إسقاط طائرة استطلاع قد تُجبر واشنطن — المرتبطة بمعاهدة دفاع مع مانيلا — على الانخراط.</p>

<h2>البؤرة الرابعة: كشمير النووية</h2>
<p>الهند وباكستان، القوتان النوويتان المتجاورتان، تتبادلان التوترات بصورة شبه دورية. أي تصعيد على خط السيطرة قد يُفضي إلى استخدام نووي تكتيكي في منطقة مكتظة بالسكان.</p>

<h2>البؤرة الخامسة: القطب الشمالي</h2>
<p>الذوبان المتسارع يفتح طرقاً بحرية جديدة وثروات طبيعية هائلة، مما يشعل تنافساً بين روسيا وكندا والولايات المتحدة والنرويج. التداخل بين المطالب الإقليمية غير المحسومة والوجود العسكري المتزايد يجعل حوادث القطب الشمالي خطراً متصاعداً.</p>
"""
    },
    {
        "slug": "cyber-guerre-arme-invisible",
        "title": "الحرب السيبرانية: السلاح الخفي الذي يُشلّ الدول دون قنبلة",
        "title_full": "الحرب السيبرانية — السلاح الخفي الذي يُشلّ الدول دون إطلاق رصاصة",
        "desc": "من ستاكسنت إلى هجمات البنية التحتية الحيوية — كيف باتت الهجمات السيبرانية سلاحاً استراتيجياً تستخدمه القوى الكبرى لشلّ خصومها دون إعلان الحرب.",
        "img": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&q=80",
        "body": """
<h2>ستاكسنت: فجر الحرب السيبرانية</h2>
<p>عام 2010 شكّل منعطفاً تاريخياً حين دمّر فيروس ستاكسنت أجهزة طرد مركزي إيرانية دون أن تُطلق قنبلة واحدة. كان هذا أول هجوم سيبراني يتسبب في ضرر مادي موثّق لمنشأة حيوية. منذ ذلك الحين دخل العالم عصراً جديداً من الصراع.</p>

<h2>أدوات الحرب السيبرانية الحديثة</h2>
<p>تتنوع الأدوات بين برامج الفدية التي تشلّ المستشفيات والبنوك، وهجمات سلسلة التوريد التي تُخترق من خلال برمجيات موثوقة كما حدث مع SolarWinds، وبرامج التجسس كـ Pegasus لاختراق الهواتف، وهجمات البنية التحتية استهدفت شبكات الكهرباء الأوكرانية مرتين.</p>

<h2>القوى السيبرانية الكبرى</h2>
<p>تتصدر الولايات المتحدة والصين وروسيا وإيران وكوريا الشمالية قائمة أقوى الفاعلين السيبرانيين. كوريا الشمالية تحوّلت قرصنتها إلى مصدر إيرادات: سرقت أكثر من 3 مليارات دولار بالعملات الرقمية لتمويل برنامجها النووي.</p>

<h2>المنطقة الرمادية: بين الحرب والسلام</h2>
<p>تعمل الهجمات السيبرانية في منطقة رمادية تجعل الردّ القانوني والعسكري معقداً. من المسؤول؟ ومتى يُعدّ الهجوم السيبراني عملاً حربياً يستوجب ردّاً تقليدياً؟ هذه أسئلة لا يوجد لها إجابات دولية واضحة حتى الآن، مما يجعل الفضاء السيبراني أرض الصراع الأكثر خطورة في العقد القادم.</p>
"""
    },
    {
        "slug": "domination-militaire-mondiale-2026",
        "title": "من يسيطر على العالم عسكرياً في 2026؟ خريطة القوة الشاملة",
        "title_full": "من يسيطر على العالم عسكرياً في 2026؟ — خريطة القوة الشاملة",
        "desc": "مقارنة شاملة لأقوى الجيوش في العالم عام 2026 من حيث الإنفاق والقدرة النووية والتكنولوجيا — ومن يملك فعلاً مفاتيح الهيمنة العسكرية.",
        "img": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1200&q=80",
        "body": """
<h2>الولايات المتحدة: التفوق المُكلف</h2>
<p>الميزانية الدفاعية الأمريكية تتجاوز 900 مليار دولار — أكثر من مجموع ميزانيات الدول العشر التالية. تمتلك واشنطن 11 حاملة طائرات نووية (الصين 3)، وأكثر من 800 قاعدة عسكرية حول العالم، وشبكة تحالفات لا مثيل لها. لكن هذا التفوق يكلّف مالياً وسياسياً.</p>

<h2>الصين: الصعود الاستراتيجي</h2>
<p>جيش التحرير الشعبي الأكبر بالعديد (2 مليون جندي)، وثاني أكبر ميزانية دفاعية (230 مليار دولار)، وتوسع بحري غير مسبوق في المحيط الهادئ. الصين تُركّز على قدرات A2/AD لمنع التدخل الأمريكي في محيطها الإقليمي بدلاً من منافسة واشنطن عالمياً.</p>

<h2>روسيا: القوة النووية المُثقلة بالأعباء</h2>
<p>روسيا تمتلك أكبر ترسانة نووية عالمياً (6000 رأس)، لكن الحرب في أوكرانيا كشفت عن محدودية قدراتها التقليدية وأوجه خلل في قيادتها وتسليحها. الإنفاق الدفاعي يرتفع لكنه يضغط على الاقتصاد.</p>

<h2>الهند ودول الخليج: القوى الصاعدة</h2>
<p>الهند تستثمر بكثافة في تطوير صناعة دفاعية محلية وتعزيز قدراتها الفضائية والسيبرانية. المملكة العربية السعودية والإمارات يستوردان أحدث الأسلحة وينشئان بُنى تحالفية جديدة. العالم يتجه نحو تعددية قطبية عسكرية لم يشهدها منذ نهاية الحرب الباردة.</p>
"""
    },
    {
        "slug": "drones-remplacer-soldats",
        "title": "الطائرات المسيّرة تحلّ محل الجنود: ثورة ميادين القتال 2026",
        "title_full": "الطائرات المسيّرة تحلّ محل الجنود — ثورة ميادين القتال في 2026",
        "desc": "من أوكرانيا إلى غزة إلى بحر الصين الجنوبي — كيف تُعيد الطائرات المسيّرة تشكيل الحرب الحديثة وتُغيّر معادلة التوازن العسكري بين الدول الكبيرة والصغيرة.",
        "img": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=1200&q=80",
        "body": """
<h2>درس أوكرانيا: الدرون يُغير قواعد اللعبة</h2>
<p>الحرب في أوكرانيا أثبتت أن طائرة مسيّرة بتكلفة ألف دولار قادرة على تدمير دبابة بقيمة 3 ملايين دولار. أوكرانيا استخدمت درونات Bayraktar التركية وآلاف الدرونات التجارية المعدّلة لضرب أرتال المدرعات الروسية وكسر توازن القوى التقليدي.</p>

<h2>أنواع الدرونات العسكرية</h2>
<p>تتراوح بين الدرونات الانتحارية (الذخائر الجوالة) التي تحوم وتنتظر الهدف، والدرونات الاستطلاعية للرصد والتوجيه، ودرونات السرب التي تُطلق بالمئات لإرباك منظومات الدفاع الجوي، والدرونات البحرية لمراقبة المضائق والموانئ.</p>

<h2>السباق التكنولوجي: الاستقلالية والذكاء الاصطناعي</h2>
<p>الجيل التالي من الدرونات لن يحتاج إلى مشغّل بشري — الذكاء الاصطناعي سيُمكّنه من التعرف على الأهداف والهجوم بصورة مستقلة. هذا يُثير تساؤلات أخلاقية حادة: من يتحمل مسؤولية القتل الذي يرتكبه نظام آلي؟</p>

<h2>ماذا يعني هذا للتوازن الاستراتيجي؟</h2>
<p>الدرونات تُمكّن الدول الصغيرة والجماعات غير الحكومية من شن ضربات استراتيجية كانت حِكراً على القوى الكبرى. إيران زوّدت وكلاءها بدرونات أثّرت على حقول النفط السعودية وإسرائيل. هذا الانتشار يعني أن خطر المواجهة المفاجئة بات أعلى من أي وقت مضى.</p>
"""
    },
    {
        "slug": "ia-militaire-revolution-illusion",
        "title": "الذكاء الاصطناعي في الجيوش: ثورة حقيقية أم وهم استراتيجي؟",
        "title_full": "الذكاء الاصطناعي في الجيوش — ثورة حقيقية أم وهم استراتيجي؟",
        "desc": "تضخّ الجيوش الكبرى مليارات الدولارات في الذكاء الاصطناعي العسكري — لكن هل يُغير الذكاء الاصطناعي فعلاً معادلة الحرب؟ تحليل نقدي للوعود والحدود.",
        "img": "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=1200&q=80",
        "body": """
<h2>التطبيقات الفعلية للذكاء الاصطناعي في الميدان</h2>
<p>الذكاء الاصطناعي العسكري ليس خيالاً علمياً — هو موجود اليوم في تحليل صور الاستطلاع بسرعة تفوق قدرة الإنسان آلاف المرات، وفي منظومة القبة الحديدية الإسرائيلية التي تُقرر اعتراض الصواريخ أم لا خلال ثوانٍ، وفي أنظمة التحكم السيبراني التي تكتشف الاختراقات فور حدوثها.</p>

<h2>الوعود الكبيرة: ما تقوله وزارات الدفاع</h2>
<p>البنتاغون يُنفق أكثر من مليار دولار سنوياً على برامج الذكاء الاصطناعي، وتدّعي إمكانية خفض خسائر الجنود، وتسريع دورة صنع القرار، وتحسين دقة الضربات. الصين بدورها تُعلن أن هدفها الريادة في الذكاء الاصطناعي العسكري بحلول 2030.</p>

<h2>الحدود الحقيقية والمخاطر</h2>
<p>لكن الذكاء الاصطناعي يفشل في بيئات الحرب الفوضوية: الدخان والضباب والاتصالات المقطوعة تُخلّ بأداء الخوارزميات. كما أن "التسمم بالبيانات" — تغذية الخصم بمعلومات مضللة — يُمكن أن يُضلّل منظومات الذكاء الاصطناعي بالكامل. والأخطر: تفويض قرار الحياة والموت لنظام آلي.</p>

<h2>خلاصة: الإنسان لا يزال ضرورياً</h2>
<p>الذكاء الاصطناعي يُضخّم قدرات الجيوش لكنه لا يُعوّض الحكم البشري في التعقيدات الأخلاقية والسياسية. القرارات الاستراتيجية الكبرى — متى تُعلن الحرب، متى تتفاوض — ستبقى بشرية. الخطر الحقيقي ليس في الذكاء الاصطناعي بل في الإفراط في الثقة به.</p>
"""
    },
    {
        "slug": "japon-role-conflit-asie",
        "title": "دور اليابان في النزاعات الآسيوية: من السلمية إلى إعادة التسليح",
        "title_full": "دور اليابان في النزاعات الآسيوية — من الدستور السلمي إلى إعادة التسليح",
        "desc": "اليابان تتخلى تدريجياً عن قيود المادة التاسعة السلمية وتستثمر بغير مسبوق في التسليح — كيف يُعيد هذا التحول رسم المشهد الأمني في آسيا؟",
        "img": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1200&q=80",
        "body": """
<h2>المادة التاسعة: الإرث السلمي في مواجهة الواقع</h2>
<p>أعاقت المادة التاسعة من الدستور الياباني طوكيو عن امتلاك قدرات هجومية منذ 1947. لكن في مواجهة الصواريخ الكورية الشمالية المتكررة والتوسع العسكري الصيني، باتت هذه القيود تُعدّ استحالة استراتيجية من قِبل صانعي القرار اليابانيين.</p>

<h2>مضاعفة الإنفاق الدفاعي</h2>
<p>أعلنت طوكيو رفع إنفاقها الدفاعي إلى 2% من الناتج المحلي بحلول 2027، أي مضاعفته. هذا يعني ميزانية سنوية تتجاوز 80 مليار دولار، مما سيجعل اليابان ثالث أو رابع أكبر مُنفق عسكري عالمياً. وتتضمن الخطط شراء صواريخ توماهوك أمريكية وتطوير منظومات ضرب أراضي الخصم.</p>

<h2>التعاون الأمني الإقليمي</h2>
<p>اليابان تعزز شراكاتها مع أستراليا والفلبين وكوريا الجنوبية، وتشارك في تمارين عسكرية مشتركة متعددة. التحالف الأمريكي-الياباني يتعمق عبر تكامل أنظمة القيادة والسيطرة. هذه المنظومة تهدف ضمنياً إلى إحاطة الصين بشبكة ردع متكاملة.</p>

<h2>ردود الفعل الإقليمية</h2>
<p>الصين وكوريا الشمالية تتهمان طوكيو بالعودة إلى النزعة العسكرية التاريخية. حتى كوريا الجنوبية — رغم شراكتها الأمنية مع اليابان — تحتفظ بحساسية تاريخية حادة. هذه التوترات تُعقّد بناء جبهة موحدة في مواجهة بكين وبيونغ يانغ.</p>
"""
    },
    {
        "slug": "marine-chinoise-vs-us-navy",
        "title": "البحرية الصينية في مواجهة الأسطول الأمريكي: من يسيطر على البحار؟",
        "title_full": "البحرية الصينية في مواجهة الأسطول الأمريكي — من يسيطر على بحار آسيا؟",
        "desc": "مقارنة معمّقة بين البحريتين الصينية والأمريكية في 2026 — الأعداد والتكنولوجيا والاستراتيجية — ومن يمتلك التفوق الفعلي في المحيط الهادئ؟",
        "img": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=1200&q=80",
        "body": """
<h2>الأعداد: الصين تتفوق بالحجم</h2>
<p>البحرية الصينية (PLAN) باتت الأكبر عالمياً بعدد السفن (370+ وحدة مقابل 290 أمريكية)، وتُنتج حاملات طائرات وغواصات بوتيرة لم يشهدها العالم منذ الحرب العالمية الثانية. الصين بنت في السنوات الخمس الأخيرة ما يعادل البحرية الفرنسية بأكملها.</p>

<h2>الكيف: أمريكا لا تزال متفوقة</h2>
<p>لكن الكيف لصالح واشنطن: حاملاتها النووية الـ11 تُتيح نشر قوة جوية في أي نقطة بالعالم. غواصاتها النووية الهاجمة (SSN) لا مثيل لها تكنولوجياً. ومعرفة قتالية مكتسبة من عقود النشر الفعلي لا يمكن نقلها بمجرد بناء سفن.</p>

<h2>استراتيجية الصين: A2/AD بدلاً من المواجهة المباشرة</h2>
<p>الصين لا تسعى للمعركة البحرية الكلاسيكية — بل تبني شبكة صواريخ مضادة للسفن وغواصات وأنظمة دفاع جوي تجعل الاقتراب من سواحلها انتحاراً لأي أسطول. هدفها: منع التدخل الأمريكي في نطاقها الإقليمي، لا السيطرة على المحيطات بأسرها.</p>

<h2>النقطة الحرجة: مضيق تايوان</h2>
<p>في سيناريو التايوان، سيكون الأسطول الأمريكي بحاجة لاختراق نطاق A2/AD الصيني لمدة أسابيع — وهو ما سيكبّده خسائر فادحة. هذا التعادل الفعلي في المنطقة هو ما يجعل أي مواجهة بحرية خطيرة للطرفين.</p>
"""
    },
    {
        "slug": "previsions-geopolitiques-2030",
        "title": "توقعات جيوسياسية 2030: كيف سيبدو العالم بعد أربع سنوات؟",
        "title_full": "توقعات جيوسياسية 2030 — كيف سيبدو النظام الدولي بعد أربع سنوات؟",
        "desc": "تحليل استراتيجي لأبرز التحولات الجيوسياسية المتوقعة بحلول 2030 — من صعود القوى الناشئة إلى تراجع الهيمنة الأمريكية ومآلات الصراعات الحالية.",
        "img": "https://images.unsplash.com/photo-1488998427799-e3362cec87c3?w=1200&q=80",
        "body": """
<h2>عالم 2030: ملامح النظام الدولي الجديد</h2>
<p>المحللون الاستراتيجيون يتفقون على أن 2030 ستشهد نظاماً دولياً مختلفاً جوهرياً عمّا نعرفه اليوم. ثلاثة ملفات رئيسية ستُحدد ملامح هذا النظام: مسار الصراع الأمريكي-الصيني، والتحول في موازين القوى الإقليمية، وأثر الثورة التكنولوجية.</p>

<h2>التوقع الأول: تعددية قطبية رسمية</h2>
<p>بحلول 2030 ستكون الصين قد حسمت وضعها كقوة اقتصادية تُضاهي الولايات المتحدة، مع تقدم متواصل في التكنولوجيا والقدرة العسكرية. الهند ستصبح ثالث أكبر اقتصاد عالمي. هذا يعني فعلياً نهاية عصر القطب الأوحد وولادة نظام ثلاثي القطب على الأقل.</p>

<h2>التوقع الثاني: آسيا تتصدر الجغرافيا الاقتصادية</h2>
<p>منطقة آسيا-المحيط الهادئ ستُنتج 60% من الناتج الإجمالي العالمي بحلول 2030. هذا يعني أن الصراعات والتحالفات الآسيوية ستُقرر مصير الاقتصاد العالمي. الممرات البحرية الآسيوية ستكتسب أهمية استراتيجية غير مسبوقة.</p>

<h2>التوقع الثالث: الذكاء الاصطناعي يُعيد تشكيل القوة</h2>
<p>الدول التي تقود السباق التكنولوجي في الذكاء الاصطناعي والحوسبة الكمية ستحظى بتفوق اقتصادي وعسكري هائل. هذا يجعل السيطرة على سلاسل إنتاج الرقائق الإلكترونية — وفي القلب منها تايوان — أهم نقطة جيوسياسية في العقد القادم.</p>

<h2>السيناريو المظلم: الانزلاق نحو الفوضى</h2>
<p>الخطر الأكبر ليس الحرب المتعمدة بل التصعيد غير المقصود: خطأ في الحسابات، حادثة تشرارة، فهم مغلوط للنوايا. نظام دولي بلا حاكم واضح وبلا قواعد مُتّفق عليها هو نظام أكثر عرضة للكوارث المفاجئة.</p>
"""
    },
    {
        "slug": "scenario-declenchement-guerre-mondiale",
        "title": "سيناريو اندلاع الحرب العالمية الثالثة: كيف يمكن أن تبدأ؟",
        "title_full": "سيناريو اندلاع الحرب العالمية الثالثة — كيف يمكن أن تبدأ في 2026؟",
        "desc": "تحليل دقيق لأكثر السيناريوهات احتمالاً لاندلاع مواجهة عسكرية كبرى — من حادثة بحرية في مضيق تايوان إلى خطأ نووي في شبه الجزيرة الكورية.",
        "img": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1200&q=80",
        "body": """
<h2>درس التاريخ: الحروب الكبرى تبدأ بأخطاء صغيرة</h2>
<p>الحرب العالمية الأولى بدأت باغتيال فرد واحد. الحرب الكورية اندلعت من عبور خط عرضي. معظم الحروب الكبرى في التاريخ لم تكن نتيجة قرار متعمد بل سلسلة من الأخطاء والتصعيدات غير المقصودة. هذا الدرس يُلقي بظلاله على مخاوف المحللين اليوم.</p>

<h2>السيناريو الأول: حادثة بحرية في مضيق تايوان</h2>
<p>سفينة حربية صينية تصطدم بمدمرة أمريكية في المضيق. كل جانب يتهم الآخر. الرأي العام يشتعل. بكين تُعلن تدريبات عسكرية مكثفة. واشنطن ترسل حاملة طائرات. طائرة صينية تُطلق النار تحذيراً — الطيار الأمريكي يُجيب بصاروخ. خلال 48 ساعة يمكن أن يتحول هذا إلى مواجهة لا أحد يعرف كيف يوقفها.</p>

<h2>السيناريو الثاني: كوريا الشمالية تُخطئ الحساب</h2>
<p>زعيم يرى تهديداً وجودياً لنظامه يُطلق صاروخاً نووياً تكتيكياً ظاناً أن كوريا الجنوبية لن تجرؤ على الرد. لكن سيئول ترد. الولايات المتحدة واليابان تنخرطان. الصين أمام خيار مستحيل: تترك حليفها أم تواجه أمريكا؟</p>

<h2>السيناريو الثالث: تصعيد سيبراني لا يمكن التحكم به</h2>
<p>هجوم سيبراني روسي يشلّ شبكة كهرباء في دول بالتيق المنتمية لحلف الناتو. المادة الخامسة من ميثاق الناتو تُلزم بالرد. لكن هل يستحق هجوم سيبراني ردّاً عسكرياً تقليدياً؟ هذا السؤال غير المحسوم قد يكون المشعل.</p>
"""
    },
    {
        "slug": "strategie-a2ad-chine-expliquee",
        "title": "استراتيجية A2/AD الصينية: كيف تُغلق الصين المحيط الهادئ أمام أمريكا؟",
        "title_full": "استراتيجية A2/AD الصينية — كيف تُغلق بكين باب تدخل واشنطن في آسيا؟",
        "desc": "شرح معمّق لاستراتيجية الحرمان من الوصول (A2/AD) التي تعتمدها الصين لإبعاد الأساطيل الأمريكية عن محيطها الإقليمي — وكيف تُعيد تشكيل التوازن الاستراتيجي.",
        "img": "https://images.unsplash.com/photo-1569163139599-0f4517e36f51?w=1200&q=80",
        "body": """
<h2>ما هي استراتيجية A2/AD؟</h2>
<p>A2/AD اختصار لـ Anti-Access/Area Denial — "منع الوصول ورفض التواجد في المنطقة". ببساطة: بدلاً من بناء أسطول يُنافس البحرية الأمريكية وجهاً لوجه — وهو سباق لن تربحه الصين على المدى القصير — تبني بكين شبكة متكاملة من الأسلحة التي تجعل اقتراب أي أسطول معادٍ من سواحلها مهمة انتحارية.</p>

<h2>مكوّنات المنظومة الصينية</h2>
<p>المنظومة تشمل: صواريخ مضادة للسفن (DF-21D وDF-26) يصل مداها 4000 كيلومتر وتستطيع استهداف حاملات الطائرات المتحركة. غواصات هجومية هادئة تنتشر في أعماق البحار. شبكة رادار ومراقبة فضائية تُغطي المحيط الهادئ بالكامل. قواعد بحرية اصطناعية في بحر الصين الجنوبي كنقاط عمليات متقدمة.</p>

<h2>حسابات البنتاغون</h2>
<p>قادة الجيش الأمريكي يُقرّون بأن اختراق النطاق A2/AD الصيني في سيناريو تايوان سيُكبّد الأسطول الأمريكي خسائر باهظة. هذا يعني أن التفوق الأمريكي في المحيط الهادئ — الذي كان مسلّماً به منذ الحرب العالمية الثانية — لم يعد كذلك.</p>

<h2>الرد الأمريكي: JADC2 وسلاسل القتل</h2>
<p>واشنطن تعتمد على JADC2 (قيادة وسيطرة مشتركة بالذكاء الاصطناعي) وشبكة "قاتل السلاسل" لاختراق منظومة A2/AD. الفكرة: ضرب منظومات الاستشعار والقيادة الصينية قبل إطلاق الصواريخ. لكن هذا يتطلب ضربات داخل الأراضي الصينية — وهنا يبدأ سيناريو التصعيد النووي.</p>
"""
    },
    {
        "slug": "taiwan-ile-strategique-monde",
        "title": "تايوان: لماذا هذه الجزيرة الصغيرة تُهدد استقرار العالم كله؟",
        "title_full": "تايوان — لماذا هذه الجزيرة الصغيرة مفتاح استقرار العالم في 2026؟",
        "desc": "تايوان ليست مجرد نزاع إقليمي — إنها قلب الاقتصاد الرقمي العالمي ومفترق طرق الجيوسياسة الكبرى. كيف باتت جزيرة بـ23 مليون نسمة تحكم مصير القرن الحادي والعشرين؟",
        "img": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=1200&q=80",
        "body": """
<h2>تايوان والرقائق الإلكترونية: قلب الاقتصاد الرقمي</h2>
<p>شركة TSMC التايوانية تُنتج أكثر من 90% من الرقائق الإلكترونية المتطورة في العالم — تلك التي تُشغّل الهواتف الذكية وسيارات الطيف والطائرات الحربية والمنظومات العسكرية. أي تعطّل في الإنتاج التايواني سيُشلّ الاقتصاد العالمي وسلاسل التوريد العسكرية الأمريكية في وقت واحد.</p>

<h2>الموقع الاستراتيجي: بوابة المحيط الهادئ</h2>
<p>تايوان تقع في قلب سلسلة الجزر الأولى — الخط الذي يفصل المحيط الهادئ الغربي عن الشرقي. سيطرة الصين على تايوان ستعني انفتاحها الكامل على المحيط الهادئ لأول مرة في التاريخ الحديث، مما يُغيّر الجغرافيا الاستراتيجية لشرق آسيا بأسرها.</p>

<h2>معادلة الردع الثلاثية</h2>
<p>ثلاثة عوامل تمنع الصين من التصرف حتى الآن: الخسائر العسكرية الهائلة المتوقعة لأي عملية إنزال، والتدمير الاقتصادي الذاتي الناجم عن تدمير TSMC أو تعطيلها، والغموض الأمريكي حول التدخل العسكري. هذه المعادلة الثلاثية هي ما يُبقي السلام هشاً.</p>

<h2>لماذا الأمر أكبر من تايوان ذاتها؟</h2>
<p>إذا سقطت تايوان بيد الصين فلن يتوقف الأمر عندها: اليابان وكوريا الجنوبية والفلبين وفيتنام ستُعيد حساباتها الاستراتيجية كاملاً. ثقة آسيا بالضمانات الأمنية الأمريكية ستنهار. مسار النظام الدولي سيتغير بصورة جذرية — لهذا تجعل واشنطن من تايوان خطاً أحمر وجودياً، لا مجرد التزام تحالفي.</p>
"""
    },
]

def make_article_html(data):
    slug = data["slug"]
    title = data["title"]
    title_full = data["title_full"]
    desc = data["desc"]
    img = data["img"]
    body = data["body"]

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{title_full}</title>
<link rel="alternate" hreflang="ar" href="https://ar.geopolo.com/articles/{slug}.html"/>
<link rel="alternate" hreflang="x-default" href="https://geopolo.com/"/>
<meta name="description" content="{desc}"/>
<meta property="og:title" content="{title_full}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:image" content="{img}"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="geopolô"/>
<meta property="og:url" content="https://ar.geopolo.com/articles/{slug}.html"/>
<meta property="og:locale" content="ar_AR"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:image" content="{img}"/>
<meta name="twitter:title" content="{title_full[:70]}"/>
<meta name="twitter:description" content="{desc[:200]}"/>
<meta name="twitter:site" content="@geopolo_ar"/>
<link rel="canonical" href="https://ar.geopolo.com/articles/{slug}.html"/>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{title_full}",
  "description": "{desc}",
  "image": "{img}",
  "url": "https://ar.geopolo.com/articles/{slug}.html",
  "datePublished": "2026-05-02",
  "dateModified": "2026-05-02",
  "author": {{"@type": "Person", "name": "ناصر الصبري"}},
  "publisher": {{"@type": "Organization", "name": "geopolô", "logo": {{"@type": "ImageObject", "url": "https://ar.geopolo.com/favicon.ico"}}}},
  "inLanguage": "ar",
  "isAccessibleForFree": true
}}
</script>
<script>
{SUBSCRIBE_JS}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Arabic:wght@400;700;900&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap" rel="stylesheet"/>
<style>
:root{{--navy:#0E1A2B;--gold:#C4952A;--accent:{COLOR};--serif:'Noto Serif Arabic',Georgia,serif;--sans:'Noto Naskh Arabic',sans-serif;--surface:#fff;--ink:#12131a;--rule:#ddd9d0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--sans);background:#f8f6f0;color:var(--ink);direction:rtl}}
a{{color:inherit;text-decoration:none}}
nav{{background:var(--navy);padding:.8rem 1.5rem;display:flex;justify-content:space-between;align-items:center}}
nav a{{color:#fff;font-family:var(--serif);font-size:.9rem;font-weight:700}}
nav .nav-links{{display:flex;gap:1.5rem}}
nav .nav-links a{{font-family:var(--sans);font-size:.78rem;font-weight:600;color:rgba(255,255,255,.85);transition:color .2s}}
nav .nav-links a:hover{{color:var(--gold)}}
.hero{{position:relative;height:420px;overflow:hidden;background:#111}}
.hero img{{width:100%;height:100%;object-fit:cover;opacity:.72;filter:saturate(.9)}}
.hero-body{{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:2.5rem 2rem;background:linear-gradient(to top,rgba(14,26,43,.85) 0%,transparent 60%)}}
.hero-tag{{display:inline-block;background:{COLOR};color:#fff;font-size:.65rem;font-weight:700;letter-spacing:.08em;padding:.22rem .7rem;border-radius:2px;margin-bottom:.8rem;text-transform:uppercase}}
.hero-title{{font-family:var(--serif);font-size:clamp(1.4rem,3.5vw,2.2rem);font-weight:900;color:#fff;line-height:1.3;max-width:800px}}
.container{{max-width:820px;margin:0 auto;padding:2rem 1.5rem}}
.article-body{{font-size:1rem;line-height:1.9;color:#2a2d3a}}
.article-body h2{{font-family:var(--serif);font-size:1.25rem;font-weight:900;color:var(--navy);margin:2rem 0 .8rem;padding-right:.8rem;border-right:4px solid {COLOR}}}
.article-body p{{margin-bottom:1.2rem}}
.author-card-v2{{margin:2.5rem 0;display:flex;gap:1.5rem;align-items:flex-start;background:var(--surface);border:1px solid var(--rule);border-right:4px solid {COLOR};padding:1.5rem}}
.author-photo{{width:88px;height:88px;border-radius:50%;object-fit:cover;object-position:top center;flex-shrink:0;border:3px solid {COLOR}}}
.author-info{{flex:1}}
.author-name-v2{{font-family:var(--serif);font-size:1.05rem;font-weight:900;color:var(--ink);margin-bottom:.15rem}}
.author-title-v2{{font-family:var(--sans);font-size:.68rem;font-weight:600;color:{COLOR};letter-spacing:.04em;text-transform:uppercase;margin-bottom:.55rem}}
.author-bio-v2{{font-family:var(--sans);font-size:.85rem;color:#5a5c72;line-height:1.7;margin-bottom:.8rem}}
.author-links{{display:flex;gap:.5rem;flex-wrap:wrap}}
.author-link{{display:inline-flex;align-items:center;gap:.3rem;font-family:var(--sans);font-size:.65rem;font-weight:600;padding:.28rem .7rem;border:1px solid currentColor;border-radius:2px;transition:background .2s,color .2s;text-decoration:none}}
.author-link.x-link{{color:#000}}.author-link.x-link:hover{{background:#000;color:#fff}}
.author-link.site-link{{color:{COLOR}}}.author-link.site-link:hover{{background:{COLOR};color:#fff}}
.nl-cta{{margin:3rem 0;background:var(--navy);padding:2rem;text-align:center}}
.nl-cta h3{{font-family:var(--serif);color:#fff;font-size:1.1rem;margin-bottom:.5rem}}
.nl-cta p{{font-family:var(--sans);color:rgba(255,255,255,.75);font-size:.85rem;margin-bottom:1rem}}
.nl-form{{display:flex;gap:.5rem;max-width:400px;margin:0 auto}}
.nl-form input{{flex:1;padding:.6rem .9rem;border:none;border-radius:2px;font-family:var(--sans);font-size:.85rem}}
.nl-form button{{background:var(--gold);color:#fff;border:none;padding:.6rem 1.2rem;border-radius:2px;cursor:pointer;font-family:var(--sans);font-weight:700;font-size:.85rem;white-space:nowrap}}
footer{{background:var(--navy);color:rgba(255,255,255,.7);text-align:center;padding:2rem;font-family:var(--sans);font-size:.75rem;margin-top:3rem}}
footer a{{color:var(--gold);margin:0 .5rem}}
</style>
</head>
<body>
<nav>
  <a href="/">geopolô</a>
  <div class="nav-links">
    <a href="/asie.html">آسيا</a>
    <a href="/proche-or.html">الشرق الأوسط</a>
    <a href="/eu.html">أوروبا</a>
    <a href="/voyage.html">سفر</a>
    <a href="/sante.html">صحة</a>
    <a href="/abonnement.html">اشترك</a>
  </div>
</nav>
<div class="hero">
  <img src="{img}" alt="{title_full}" loading="eager"/>
  <div class="hero-body">
    <span class="hero-tag">{TAG}</span>
    <h1 class="hero-title">{title_full}</h1>
  </div>
</div>
<div class="container">
  <article class="article-body">
    {body}
  </article>
  <div class="author-card-v2">
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
  </div>
  <div class="nl-cta">
    <h3>تحليلات استراتيجية أسبوعية</h3>
    <p>اشترك واحصل على أعمق التحليلات الجيوسياسية مباشرة في بريدك</p>
    <form class="nl-form" onsubmit="return subscribeGeo(this,'ar')">
      <input type="email" placeholder="بريدك الإلكتروني" required/>
      <button type="submit">اشترك مجاناً</button>
    </form>
    <p class="nl-msg" style="margin-top:.5rem;min-height:1.2em"></p>
  </div>
</div>
<footer>
  <p>© 2026 geopolô — تحليلات جيوسياسية مستقلة</p>
  <p style="margin-top:.5rem">
    <a href="/">الرئيسية</a>
    <a href="/asie.html">آسيا</a>
    <a href="/eu.html">أوروبا</a>
    <a href="/proche-or.html">الشرق الأوسط</a>
    <a href="/abonnement.html">الاشتراك</a>
  </p>
</footer>
</body>
</html>"""


# ── Step 1: Create missing articles ──────────────────────────────────────────
print("📝 Création des articles manquants...\n")
created = 0
for data in ARTICLES_DATA:
    fp = os.path.join(ARTICLES, f"{data['slug']}.html")
    if os.path.exists(fp):
        print(f"  — {data['slug']} (existe déjà)")
        continue
    html = make_article_html(data)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ {data['slug']}")
    created += 1

print(f"\n✅ {created} articles créés\n")

# ── Step 2: Update asie.html grid ────────────────────────────────────────────
print("🔧 Mise à jour de asie.html...\n")

ASIE_PAGE = os.path.join(DIR, "asie.html")
with open(ASIE_PAGE, encoding="utf-8") as f:
    content = f.read()

NEW_SLUGS = [d["slug"] for d in ARTICLES_DATA]

# Check which slugs are already in the page
missing_slugs = [s for s in NEW_SLUGS if f"/articles/{s}.html" not in content]
print(f"  Slugs manquants dans la grille: {len(missing_slugs)}")

if missing_slugs:
    # Build card HTML for each missing slug
    def make_card(slug, img, title, desc):
        desc_short = desc[:120]
        return f'''<a href="/articles/{slug}.html" class="article-card">
  <div class="article-card__img-wrap">
    <img class="article-card__img" src="{img}" alt="{title}" loading="lazy"/>
  </div>
  <div class="article-card__body">
    <span class="article-card__tag" style="background:{COLOR}">{TAG}</span>
    <h3 class="article-card__title">{title}</h3>
    <p class="article-card__desc">{desc_short}</p>
    <div class="article-card__footer">
      <span class="article-card__read" style="color:{COLOR}">اقرأ التحليل ←</span>
      <span class="article-card__time">⏱ 8 دقائق</span>
    </div>
  </div>
</a>'''

    cards_html = "\n".join([
        make_card(d["slug"], d["img"], d["title"], d["desc"])
        for d in ARTICLES_DATA
        if d["slug"] in missing_slugs
    ])

    # Check if existing grid-asie_ame section exists
    if 'id="grid-asie_ame"' in content:
        # Append cards to existing .article-grid div
        # Find the last </div></section> closing the grid and insert before it
        import re
        # Find the article-grid div inside grid-asie_ame
        pattern = re.compile(r'(<section id="grid-asie_ame".*?<div class="article-grid">)(.*?)(</div>\s*</section>)', re.DOTALL)
        m = pattern.search(content)
        if m:
            new_content = content[:m.start()] + m.group(1) + m.group(2) + "\n" + cards_html + "\n" + m.group(3) + content[m.end():]
            with open(ASIE_PAGE, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ {len(missing_slugs)} cartes ajoutées à la grille existante")
        else:
            print("  ⚠️  Pattern grille non trouvé — injection avant </main>")
            # Fallback: inject a new section
            CARD_GRID_CSS = """
/* ── ARTICLE CARDS GRID v2 ── */
.article-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.2rem;margin:2rem 0}
.article-card{display:flex;flex-direction:column;background:#fff;border:1px solid #e8e4dc;overflow:hidden;transition:transform .22s cubic-bezier(.4,0,.2,1),box-shadow .22s cubic-bezier(.4,0,.2,1);text-decoration:none;color:inherit}
.article-card:hover{transform:translateY(-4px);box-shadow:0 8px 28px rgba(14,26,43,.1)}
"""
            section_html = f'''
<section id="grid-asie_new" style="margin:3rem 0 2rem;max-width:1200px;margin-left:auto;margin-right:auto;padding:0 1.5rem">
  <div class="article-grid-header" style="border-color:{COLOR};color:{COLOR}">
    <h2 style="color:{COLOR}">آسيا والمحيط الهادئ</h2>
    <div class="article-grid-header-line"></div>
    <a href="/asie.html" style="color:{COLOR}">جميع المقالات ←</a>
  </div>
  <div class="article-grid">{cards_html}</div>
</section>'''
            for anchor in ["</main>", "<footer", "</body>"]:
                if anchor in content:
                    content = content.replace(anchor, section_html + "\n" + anchor, 1)
                    break
            with open(ASIE_PAGE, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ Nouvelle section injectée avec {len(missing_slugs)} cartes")
    else:
        print("  ⚠️  Section grid-asie_ame absente — création d'une nouvelle section")
        section_html = f'''
<section id="grid-asie_ame" style="margin:3rem 0 2rem;max-width:1200px;margin-left:auto;margin-right:auto;padding:0 1.5rem">
  <div class="article-grid-header" style="border-color:{COLOR};color:{COLOR}">
    <h2 style="color:{COLOR}">آسيا والمحيط الهادئ</h2>
    <div class="article-grid-header-line"></div>
    <a href="/asie.html" style="color:{COLOR}">جميع المقالات ←</a>
  </div>
  <div class="article-grid">{cards_html}</div>
</section>'''
        for anchor in ["</main>", "<footer", "</body>"]:
            if anchor in content:
                content = content.replace(anchor, section_html + "\n" + anchor, 1)
                break
        with open(ASIE_PAGE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ Section créée avec {len(missing_slugs)} cartes")
else:
    print("  — Tous les slugs sont déjà présents dans asie.html")

print("\nDone.")
