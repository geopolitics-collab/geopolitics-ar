#!/usr/bin/env python3
"""
Connect all newsletter forms to the real Cloudflare Worker API.

API endpoint: https://floral-math-8fc3.nasseralsabri.workers.dev/subscribe
Method: POST / Content-Type: application/json
Body: { email, lang: "ar" }
Response: { message } on success | { error } on failure

Fixes:
1. Replace onsubmit="return false" with real subscribeGeo(this)
2. Add name="email" to all inputs
3. Add msg <p> for feedback display
4. Inject shared JS function into all articles + index.html
5. Fix sidebar newsletter (add inline mini-form)
6. Fix index.html newsletter form
"""
import os, glob, re

DIR      = "/workspaces/geopolitics-ar"
ARTICLES = os.path.join(DIR, "articles")

API_URL = "https://floral-math-8fc3.nasseralsabri.workers.dev/subscribe"

# ── Shared subscribe function (injected into every page) ───────────────────
SUBSCRIBE_JS = f"""
function subscribeGeo(form, lang) {{
  lang = lang || 'ar';
  var input = form.querySelector('input[type="email"]');
  var btn   = form.querySelector('button[type="submit"]');
  var msg   = form.parentElement.querySelector('.nl-msg') ||
              form.nextElementSibling ||
              (function(){{ var p=document.createElement('p'); p.className='nl-msg'; form.parentNode.insertBefore(p,form.nextSibling); return p; }})();

  var email = input ? input.value.trim() : '';
  if (!email || !/^[^@]+@[^@]+\\.[^@]+$/.test(email)) {{
    msg.innerHTML = '<span style="color:#e05a2b">⚠️ يرجى إدخال بريد إلكتروني صحيح</span>';
    if(input) input.focus();
    return false;
  }}

  var origText = btn ? btn.textContent : '';
  if (btn) {{ btn.textContent = '⏳...'; btn.disabled = true; }}
  msg.innerHTML = '';

  fetch('{API_URL}', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{ email: email, lang: lang }})
  }})
  .then(function(r) {{ return r.json(); }})
  .then(function(data) {{
    if (data.message || data.success) {{
      msg.innerHTML = '<span style="color:#1a8a6e;font-family:var(--sans,sans-serif);font-size:.85rem">✅ تم الاشتراك بنجاح — شكراً!</span>';
      if(input) input.value = '';
      if(btn)   {{ btn.textContent = '✓ تم'; btn.style.background='#1a8a6e'; }}
    }} else {{
      var errMsg = data.error || data.message || 'حدث خطأ';
      if(errMsg.toLowerCase().includes('already') || errMsg.includes('موجود')) {{
        msg.innerHTML = '<span style="color:#c8920a;font-family:var(--sans,sans-serif);font-size:.85rem">ℹ️ هذا البريد مشترك بالفعل</span>';
      }} else {{
        msg.innerHTML = '<span style="color:#e05a2b;font-family:var(--sans,sans-serif);font-size:.85rem">⚠️ ' + errMsg + '</span>';
      }}
      if(btn)   {{ btn.textContent = origText; btn.disabled = false; }}
    }}
  }})
  .catch(function() {{
    msg.innerHTML = '<span style="color:#e05a2b;font-family:var(--sans,sans-serif);font-size:.85rem">❌ خطأ في الاتصال — حاول مجدداً</span>';
    if(btn) {{ btn.textContent = origText; btn.disabled = false; }}
  }});
  return false;
}}
"""

# ── CSS for feedback message ────────────────────────────────────────────────
NL_MSG_CSS = """
.nl-msg{margin-top:.6rem;min-height:1.2rem;text-align:center;font-family:var(--sans,'Noto Naskh Arabic',sans-serif);font-size:.82rem;line-height:1.5;position:relative;z-index:11}
"""

# ── New form HTML (replaces broken form in articles) ───────────────────────
OLD_FORM  = '<form class="nl-form" onsubmit="return false">'
NEW_FORM  = '<form class="nl-form" onsubmit="return subscribeGeo(this,\'ar\')" novalidate>'

OLD_INPUT = '<input class="nl-input" type="email" placeholder="بريدك الإلكتروني"/>'
NEW_INPUT = '<input class="nl-input" type="email" name="email" placeholder="بريدك الإلكتروني" autocomplete="email" required/>'

OLD_NOTE  = '<p class="nl-note">بدون إزعاج · إلغاء في أي وقت</p>'
NEW_NOTE  = '<p class="nl-msg" aria-live="polite"></p>\n      <p class="nl-note">بدون إزعاج · إلغاء في أي وقت</p>'

# ── Index.html form fix ─────────────────────────────────────────────────────
INDEX_FORM_OLD = 'onsubmit="return false;"'
INDEX_FORM_NEW = 'onsubmit="return subscribeGeo(this,\'ar\')" novalidate'


def fix_file(filepath, is_index=False):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if 'lang="ar"' not in content and not is_index:
        return False, "skip"

    changed = []

    # 1. Add CSS for .nl-msg if not present
    if ".nl-msg" not in content and "</style>" in content:
        content = content.replace("</style>", NL_MSG_CSS + "</style>", 1)
        changed.append("css")

    # 2. Fix article inline nl-cta forms
    if OLD_FORM in content:
        content = content.replace(OLD_FORM, NEW_FORM)
        changed.append("form-action")

    if OLD_INPUT in content:
        content = content.replace(OLD_INPUT, NEW_INPUT)
        changed.append("input-name")

    if OLD_NOTE in content and '<p class="nl-msg"' not in content:
        content = content.replace(OLD_NOTE, NEW_NOTE)
        changed.append("msg-added")

    # 3. Fix index.html newsletter form
    if is_index and INDEX_FORM_OLD in content:
        content = content.replace(INDEX_FORM_OLD, INDEX_FORM_NEW)
        # Add name to email input in index
        content = re.sub(
            r'(<input[^>]+type="email"[^>]*)(placeholder="بريدك الإلكتروني")',
            r'\1name="email" \2 autocomplete="email" required',
            content
        )
        # Add .nl-msg after form if not present
        if '.newsletter__form' in content and 'nl-msg' not in content:
            content = content.replace(
                '</form>',
                '</form>\n<p class="nl-msg newsletter__msg" aria-live="polite" style="text-align:center;margin-top:.6rem;font-size:.85rem;min-height:1.4rem"></p>',
                1
            )
        changed.append("index-form")

    # 4. Fix newsletter.html sendEmail → subscribeGeo
    if 'sendEmail' in content and 'subscribeGeo' not in content:
        content = content.replace(
            'onsubmit="return sendEmail(this)"',
            'onsubmit="return subscribeGeo(this,\'ar\')" novalidate'
        )
        # Remove old sendEmail function
        content = re.sub(
            r'function sendEmail\(form\)\s*\{.*?\}\s*</script>',
            '</script>',
            content, flags=re.DOTALL
        )
        changed.append("newsletter-page")

    # 5. Inject subscribeGeo function body (not just reference in onsubmit)
    if 'function subscribeGeo' not in content:
        if '</script>' in content:
            content = content.replace('</script>', SUBSCRIBE_JS + '\n</script>', 1)
            changed.append("js-injected")
        elif '</body>' in content:
            content = content.replace(
                '</body>',
                f'<script>{SUBSCRIBE_JS}</script>\n</body>'
            )
            changed.append("js-injected-body")

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return bool(changed), ", ".join(changed)


def main():
    print("═" * 60)
    print("  NEWSLETTER FIX — Connexion API réelle")
    print("═" * 60)
    print(f"  API: {API_URL}\n")

    # Fix all articles
    article_files = sorted(glob.glob(os.path.join(ARTICLES, "*.html")))
    fixed = skipped = 0
    for fp in article_files:
        ok, msg = fix_file(fp)
        if ok:
            fixed += 1
        else:
            skipped += 1

    print(f"  Articles: ✅ {fixed} fixés | — {skipped} ignorés")

    # Fix index.html
    ok, msg = fix_file(os.path.join(DIR, "index.html"), is_index=True)
    print(f"  index.html: {'✅ ' + msg if ok else '— déjà ok'}")

    # Fix newsletter.html
    ok, msg = fix_file(os.path.join(DIR, "newsletter.html"))
    print(f"  newsletter.html: {'✅ ' + msg if ok else '— déjà ok'}")

    # Fix abonnement.html if exists
    for page in ["abonnement.html"]:
        fp = os.path.join(DIR, page)
        if os.path.exists(fp):
            ok, msg = fix_file(fp)
            print(f"  {page}: {'✅ ' + msg if ok else '— déjà ok'}")

    # Verify
    print("\n🔍 Vérification:")
    sample = article_files[:3] + [os.path.join(DIR, "index.html"), os.path.join(DIR, "newsletter.html")]
    for fp in sample:
        with open(fp, encoding="utf-8") as f: c = f.read()
        has_api   = API_URL in c
        has_fn    = 'subscribeGeo' in c
        has_name  = 'name="email"' in c
        has_msg   = 'nl-msg' in c
        print(f"  {os.path.basename(fp):45s} api={has_api} fn={has_fn} name={has_name} msg={has_msg}")


if __name__ == "__main__":
    main()
