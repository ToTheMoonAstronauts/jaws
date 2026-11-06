"""Build a translated copy of the site from the English source.
usage: python3 tools/i18n/build_lang.py <lang> <src website dir> <out dir (e.g. _site/de)> [--report] [--en-hreflang]
Pages are translated segment by segment with the language's dict; anything without a translation
stays English and is listed with --report. <lang>_overrides/ (e.g. localized gallery images) is
copied over the result last."""
import os, re, sys, shutil, html, importlib
sys.path.insert(0, os.path.dirname(__file__))
from segments import html_segments, js_segments
from pages import PAGES, JS

SITE = "https://jawzr.com"
LANGS = {  # code: (dict modules, og:locale, joining word for "A and B" links)
    "lt": (["lt_strings", "lt_legal"], "lt_LT", "ir"),
    "de": (["de_strings"], "de_DE", "und"),
}
ALL = ["en"] + list(LANGS)
LOCALE = {"en": "en_US", **{k: v[1] for k, v in LANGS.items()}}
missing = {}

def load(lang):
    T = {}
    for m in LANGS[lang][0]: T.update(importlib.import_module(m).T)
    return {k: v for k, v in T.items() if v}

def make_fn(T, where):
    def fn(s):
        k = s.strip()
        if k in T: return T[k]
        k2 = re.sub(r"\s+", " ", k)  # tolerate collapsed whitespace in long paragraphs
        if k2 in T: return T[k2]
        k3 = html.unescape(k2)
        if k3 in T: return html.escape(T[k3], quote=False)
        missing.setdefault(k2, where)
        return s
    return fn

def clean(p): return "" if p == "index.html" else p[:-5]

def fix_og(doc, lang):
    """Language copy of the OG block: own url, own image, own locale + the others as alternates."""
    def blk(m):
        b = m.group(0)
        b = re.sub(r'(rel="canonical" href=|property="og:url" content=)"https://jawzr\.com/', rf'\1"https://jawzr.com/{lang}/', b)
        b = re.sub(r'(images/og-[a-z]+)-en\.jpg', rf'\1-{lang}.jpg', b)
        b = re.sub(r'<meta property="og:locale(:alternate)?" content="[^"]*">\n?', "", b)
        loc = [f'<meta property="og:locale" content="{LOCALE[lang]}">'] + [f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in ALL if l != lang]
        return b.replace('<meta name="twitter:card"', "\n".join(loc) + '\n<meta name="twitter:card"', 1)
    return re.sub(r"<!--og-->.*?<!--/og-->", blk, doc, flags=re.S)

def fix_links(doc, lang):
    # pages that exist only in English live one level up
    doc = re.sub(r'(href|src)="(articles\.html|article-[^"]+|dash/[^"]*|v1\.html|product-pick\.html)', r'\1="../\2', doc)
    doc = re.sub(r'<html lang="en"', f'<html lang="{lang}"', doc)
    w = LANGS[lang][2]  # single lowercase words are skipped as code, so join words are fixed here
    return doc.replace("</b> at <b>", "</b> <b>").replace("</a> and <a", f"</a> {w} <a").replace("</a>, and <a", f"</a> {w} <a")

def hreflang(en_file):
    tags = [f'<link rel="alternate" hreflang="{l}" href="{SITE}/{"" if l == "en" else l + "/"}{clean(en_file)}">' for l in ALL]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{clean(en_file)}">')
    return "\n".join(tags) + "\n"

def add_hreflang(doc, en_file):
    doc = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?', "", doc)
    return doc.replace("</head>", hreflang(en_file) + "</head>", 1)

def build(lang, src, out, report):
    T = load(lang)
    os.makedirs(out, exist_ok=True)
    for p in PAGES:
        doc = open(os.path.join(src, p), encoding="utf-8").read()
        if 'name="robots" content="noindex' not in doc: doc = add_hreflang(doc, p)
        doc = html_segments(doc, make_fn(T, p))
        doc = fix_og(fix_links(doc, lang), lang)
        open(os.path.join(out, p), "w", encoding="utf-8").write(doc)
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    for j in JS:
        code = open(os.path.join(src, j), encoding="utf-8").read()
        open(os.path.join(out, j), "w", encoding="utf-8").write(js_segments(code, make_fn(T, j)))
    shutil.copy(os.path.join(src, "assets/site.css"), os.path.join(out, "assets/site.css"))
    for d in os.listdir(src):
        full = os.path.join(src, d)
        if os.path.isdir(full) and d not in ("assets", "dash"):
            shutil.copytree(full, os.path.join(out, d), dirs_exist_ok=True)
        elif d.endswith((".ico", ".png", ".svg", ".webmanifest")):
            shutil.copy(full, os.path.join(out, d))
    for f in os.listdir(os.path.join(src, "assets")):
        if f not in ("site.js", "site.css"):
            s = os.path.join(src, "assets", f)
            (shutil.copytree(s, os.path.join(out, "assets", f), dirs_exist_ok=True) if os.path.isdir(s) else shutil.copy(s, os.path.join(out, "assets", f)))
    # old URLs keep working
    for old in ("index-v2.html", "product-sub.html", "product.html"):
        open(os.path.join(out, old), "w", encoding="utf-8").write(open(os.path.join(src, old), encoding="utf-8").read().replace("https://jawzr.com/", f"https://jawzr.com/{lang}/"))
    # language-only assets (e.g. gallery images with translated text) replace the EN copies
    ov = os.path.join(os.path.dirname(__file__), f"{lang}_overrides")
    if os.path.isdir(ov): shutil.copytree(ov, out, dirs_exist_ok=True)
    if report:
        for k, w in sorted(missing.items(), key=lambda x: x[1]): print(f"[{lang}][{w}] {k[:140]}")
        print(lang, len(missing), "untranslated segments")

def add_en_hreflang(site):
    """EN pages in the built site get the same alternates."""
    for p in PAGES:
        target = os.path.join(site, p)
        if not os.path.exists(target): continue
        doc = open(target, encoding="utf-8").read()
        if 'name="robots" content="noindex' in doc: continue
        open(target, "w", encoding="utf-8").write(add_hreflang(doc, p))

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    build(args[0], args[1], args[2], "--report" in sys.argv)
    if "--en-hreflang" in sys.argv: add_en_hreflang(os.path.dirname(os.path.normpath(args[2])))
