#!/usr/bin/env python3
"""
Inject Google AdSense script into all article pages.

Two insertion points per article:
  1. After the 2nd <p> tag inside the article body
  2. Before the author card / end of article content

No duplication: skips files that already contain the publisher ID.
"""
import os, re, glob

ARTICLES_DIR = "/workspaces/geopolitics-ar/articles"

ADSENSE = (
    '\n<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    'adsbygoogle.js?client=ca-pub-7897922032846846" crossorigin="anonymous"></script>\n'
)
MARKER = "ca-pub-7897922032846846"

# Anchors that mark the start of the article body
BODY_START_PATTERNS = [
    re.compile(r'<article\s+class="article-body">', re.IGNORECASE),
    re.compile(r'<article\s+class="body">', re.IGNORECASE),
    re.compile(r'<div\s+class="article-body">', re.IGNORECASE),
    re.compile(r'<article(?:\s+[^>]*)?>', re.IGNORECASE),  # fallback
]

# Anchors that mark end of article (try in order, use first match)
END_ANCHORS = [
    '<div class="author-card-v2">',
    '</article>',
    '<div class="nl-cta">',
    '<div class="rel">',
    '</main>',
]


def find_body_start(content):
    """Return index where the article body begins, or None."""
    for pat in BODY_START_PATTERNS:
        m = pat.search(content)
        if m:
            return m.end()
    return None


def inject_after_2nd_paragraph(content, body_start):
    """
    Find the 2nd </p> that appears after body_start and insert AdSense after it.
    Returns modified content, or original if not enough paragraphs.
    """
    segment   = content[body_start:]
    # Find all </p> positions (case-insensitive)
    closes    = [m.end() for m in re.finditer(r'</p>', segment, re.IGNORECASE)]

    if len(closes) < 2:
        # Fewer than 2 paragraphs — insert after the 1st if present
        if closes:
            idx = body_start + closes[0]
            return content[:idx] + ADSENSE + content[idx:]
        return content  # nothing to do

    idx = body_start + closes[1]   # position right after 2nd </p>
    return content[:idx] + ADSENSE + content[idx:]


def inject_at_end(content):
    """
    Insert AdSense before the first matching END_ANCHOR.
    Returns (modified_content, anchor_used) or (original, None).
    """
    for anchor in END_ANCHORS:
        pos = content.find(anchor)
        if pos != -1:
            return content[:pos] + ADSENSE + content[pos:], anchor
    return content, None


def process_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Skip if AdSense already present
    if MARKER in content:
        return "skip"

    original = content

    # ── Injection 1: after 2nd paragraph ──
    body_start = find_body_start(content)
    if body_start is not None:
        content = inject_after_2nd_paragraph(content, body_start)
    else:
        # Fallback: insert after 2nd </p> anywhere in body
        closes = [m.end() for m in re.finditer(r'</p>', content, re.IGNORECASE)]
        if len(closes) >= 2:
            idx = closes[1]
            content = content[:idx] + ADSENSE + content[idx:]

    # ── Injection 2: before end-of-article anchor ──
    content, anchor = inject_at_end(content)

    if content == original:
        return "no-change"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return f"ok ({anchor or 'fallback'})"


def main():
    files   = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.html")))
    total   = len(files)
    done    = skipped = errors = 0

    print(f"📰 Injection AdSense — {total} articles\n")

    for fp in files:
        name = os.path.basename(fp)
        try:
            result = process_file(fp)
            if result == "skip":
                skipped += 1
            elif result == "no-change":
                skipped += 1
                print(f"  — {name} (aucun ancre trouvé)")
            else:
                done += 1
                print(f"  ✅ {name}  [{result}]")
        except Exception as e:
            errors += 1
            print(f"  ❌ {name}: {e}")

    print(f"\n✅ {done} injectés | — {skipped} ignorés | ❌ {errors} erreurs")


if __name__ == "__main__":
    main()
