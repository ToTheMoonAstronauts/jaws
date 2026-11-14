"""Build a translated copy of the site from the English source.
usage: python3 tools/i18n/build_lang.py <lang> <src website dir> <out dir (e.g. _site/de)> [--report] [--en-hreflang]
Pages are translated segment by segment with the language's dict; anything without a translation
stays English and is listed with --report. <lang>_overrides/ (e.g. localized gallery images) is
copied over the result last."""
import os, re, sys, shutil, html, importlib
sys.path.insert(0, os.path.dirname(__file__))
from segments import html_segments, js_segments
from pages import PAGES, ARTICLES, JS

SITE = "https://jawzr.com"
LANGS = {  # code: (dict modules, og:locale, joining word for "A and B" links)
    "lt": (["lt_strings", "lt_legal", "lt_articles"], "lt_LT", "ir"),
    "de": (["de_strings"], "de_DE", "und"),
}
ARTICLE_LANGS = {"lt"}  # languages that ship translated article pages (others link up to the English ones)
ALL = ["en"] + list(LANGS)
LOCALE = {"en": "en_US", **{k: v[1] for k, v in LANGS.items()}}
missing = {}

def load(lang):
    T = {}
    for m in LANGS[lang][0]: T.update(importlib.import_module(m).T)
    return {k: v for k, v in T.items() if v}

def make_fn(T, where):
    def v(x): return "" if x == "∅" else x  # "∅" means: render nothing in this language
    def fn(s):
        k = s.strip()
        if k in T: return v(T[k])
        k2 = re.sub(r"\s+", " ", k)  # tolerate collapsed whitespace in long paragraphs
        if k2 in T: return v(T[k2])
        k3 = html.unescape(k2)
        if k3 in T: return html.escape(v(T[k3]), quote=False)
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
    eng_only = r'dash/[^"]*|v1\.html|product-pick\.html'
    if lang not in ARTICLE_LANGS: eng_only = r'articles\.html|article-[^"]+|' + eng_only
    doc = re.sub(r'(href|src)="(' + eng_only + r')', r'\1="../\2', doc)
    doc = re.sub(r'<html lang="en"', f'<html lang="{lang}"', doc)
    doc = re.sub(r"€(\d+(?:,\d\d)?)(?![\d,])", r"\1 €", doc)  # €31,95 -> 31,95 € (prices with no words are skipped by the translator)
    w = LANGS[lang][2]  # single lowercase words are skipped as code, so join words are fixed here
    return doc.replace("</b> at <b>", "</b> <b>").replace("</a> and <a", f"</a> {w} <a").replace("</a>, and <a", f"</a> {w} <a")

def hreflang(en_file):
    tags = [f'<link rel="alternate" hreflang="{l}" href="{SITE}/{"" if l == "en" else l + "/"}{clean(en_file)}">' for l in ALL]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{clean(en_file)}">')
    return "\n".join(tags) + "\n"

def add_hreflang(doc, en_file):
    doc = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?', "", doc)
    return doc.replace("</head>", hreflang(en_file) + "</head>", 1)

def override_paths(lang):
    """Relative paths (e.g. images/gallery/3.webp) the language overrides."""
    ov = os.path.join(os.path.dirname(__file__), f"{lang}_overrides")
    out = set()
    for root, _, files in os.walk(ov) if os.path.isdir(ov) else []:
        for f in files:
            out.add(os.path.relpath(os.path.join(root, f), ov).replace(os.sep, "/"))
    return out

def share_assets(text, lang, overrides):
    """Heavy assets identical across languages (the hero, product shots, article images, the
    video) are served once from the site root, so translated pages point at /images/ and /media/
    instead of carrying a copy. images/gallery/ is the exception: its slides are localised and the
    product page builds their paths at runtime (images/gallery/${n}.webp), so that folder stays
    relative and is duplicated per language. images/products/ and media/ are kept relative too for a
    language that ships its own localised bag shots or video (i.e. has overrides under them)."""
    if not any(p.startswith("media/") for p in overrides):
        text = re.sub(r'(?<![\w/.])media/', '/media/', text)
    excl = "gallery/|products/" if any(p.startswith("images/products/") for p in overrides) else "gallery/"
    text = re.sub(r'(?<![\w/.])images/(?!' + excl + r')', '/images/', text)
    return text

def build(lang, src, out, report, local=False):
    """local=True: a self-contained copy for file:// review — asset paths stay relative and the
    full images/ and media/ trees are copied in (then the language overrides overlaid), so it opens
    straight off disk. Production build (local=False) keeps images/ and media/ shared from the root."""
    T = load(lang)
    ov_paths = override_paths(lang)
    os.makedirs(out, exist_ok=True)
    pages = list(PAGES) + (list(ARTICLES) if lang in ARTICLE_LANGS else [])
    for p in pages:
        doc = open(os.path.join(src, p), encoding="utf-8").read()
        if p in PAGES and 'name="robots" content="noindex' not in doc: doc = add_hreflang(doc, p)
        doc = html_segments(doc, make_fn(T, p))
        doc = fix_og(fix_links(doc, lang), lang)
        if not local: doc = share_assets(doc, lang, ov_paths)
        open(os.path.join(out, p), "w", encoding="utf-8").write(doc)
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    for j in JS:
        code = open(os.path.join(src, j), encoding="utf-8").read()
        code = js_segments(code, make_fn(T, j))
        if not local: code = share_assets(code, lang, ov_paths)
        open(os.path.join(out, j), "w", encoding="utf-8").write(code)
    shutil.copy(os.path.join(src, "assets/site.css"), os.path.join(out, "assets/site.css"))
    if local:
        # self-contained: full images + media, then language overrides win
        shutil.copytree(os.path.join(src, "images"), os.path.join(out, "images"), dirs_exist_ok=True)
        if os.path.isdir(os.path.join(src, "media")):
            shutil.copytree(os.path.join(src, "media"), os.path.join(out, "media"), dirs_exist_ok=True)
    else:
        # images/ and media/ are shared from the site root; only images/gallery/ is per language
        shutil.copytree(os.path.join(src, "images/gallery"), os.path.join(out, "images/gallery"), dirs_exist_ok=True)
        # a language with its own bag shots keeps images/products/ per language too (overrides win below)
        if any(p.startswith("images/products/") for p in ov_paths):
            shutil.copytree(os.path.join(src, "images/products"), os.path.join(out, "images/products"), dirs_exist_ok=True)
        # likewise media/ (e.g. a localised video) is kept per language when overridden
        if any(p.startswith("media/") for p in ov_paths) and os.path.isdir(os.path.join(src, "media")):
            shutil.copytree(os.path.join(src, "media"), os.path.join(out, "media"), dirs_exist_ok=True)
    for d in os.listdir(src):
        full = os.path.join(src, d)
        if os.path.isdir(full) and d not in ("assets", "dash", "images", "media"):
            shutil.copytree(full, os.path.join(out, d), dirs_exist_ok=True)
        elif d.endswith((".ico", ".png", ".svg", ".webmanifest")):
            shutil.copy(full, os.path.join(out, d))
    for f in os.listdir(os.path.join(src, "assets")):
        if f not in ("site.js", "site.css"):
            s = os.path.join(src, "assets", f)
            (shutil.copytree(s, os.path.join(out, "assets", f), dirs_exist_ok=True) if os.path.isdir(s) else shutil.copy(s, os.path.join(out, "assets", f)))
    # old URLs keep working
    for old in ("index-v2.html", "product-sub.html", "product.html"):
        doc = open(os.path.join(src, old), encoding="utf-8").read().replace("https://jawzr.com/", f"https://jawzr.com/{lang}/")
        open(os.path.join(out, old), "w", encoding="utf-8").write(share_assets(doc, lang, ov_paths))
    # language-only assets (e.g. gallery images with translated text): only these are duplicated
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
    build(args[0], args[1], args[2], "--report" in sys.argv, local="--local" in sys.argv)
    if "--en-hreflang" in sys.argv: add_en_hreflang(os.path.dirname(os.path.normpath(args[2])))
