"""Build the Lithuanian site from the English source.
usage: python3 tools/i18n/build_lt.py <src website dir> <out dir (e.g. _site/lt)> [--report]
EN pages are translated segment by segment with lt_strings.T + lt_legal.T; anything without
a translation stays English and is listed with --report."""
import os, re, sys, shutil, html
sys.path.insert(0, os.path.dirname(__file__))
from segments import html_segments, js_segments
from pages import PAGES, JS
import lt_strings, lt_legal

T = {**lt_strings.T, **lt_legal.T}
T = {k: v for k, v in T.items() if v}
SITE = "https://jawzr.com"
missing = {}

def make_fn(where):
    def fn(s):
        k = s.strip()
        if k in T: return T[k]
        # tolerate collapsed whitespace in long paragraphs
        k2 = re.sub(r"\s+", " ", k)
        if k2 in T: return T[k2]
        k3 = html.unescape(k2)
        if k3 in T: return html.escape(T[k3], quote=False)
        missing.setdefault(k2, where)
        return s
    return fn

def out_name(p): return "index.html" if p == "index-v2.html" else p

def fix_links(doc):
    doc = doc.replace('href="index-v2.html', 'href="index.html')
    # pages that exist only in English live one level up
    doc = re.sub(r'(href|src)="(articles\.html|article-[^"]+|dash/[^"]*|v1\.html|product-pick\.html)', r'\1="../\2', doc)
    doc = re.sub(r'<html lang="en"', '<html lang="lt"', doc)
    doc = doc.replace("</b> at <b>", "</b> <b>").replace("</a> and <a", "</a> ir <a").replace("</a>, and <a", "</a> ir <a")  # single lowercase words are skipped as code
    return doc

def hreflang(en_file):
    en = SITE + "/" + ("" if en_file == "index-v2.html" else en_file)
    lt = SITE + "/lt/" + ("" if en_file == "index-v2.html" else en_file)
    return (f'<link rel="alternate" hreflang="en" href="{en}">\n'
            f'<link rel="alternate" hreflang="lt" href="{lt}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{en}">\n')

def add_hreflang(doc, en_file):
    doc = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?', "", doc)
    return doc.replace("</head>", hreflang(en_file) + "</head>", 1)

def main(src, out, report):
    os.makedirs(out, exist_ok=True)
    for p in PAGES:
        doc = open(os.path.join(src, p), encoding="utf-8").read()
        if 'name="robots" content="noindex' not in doc: doc = add_hreflang(doc, p)
        doc = html_segments(doc, make_fn(p))
        doc = fix_links(doc)
        open(os.path.join(out, out_name(p)), "w", encoding="utf-8").write(doc)
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    for j in JS:
        code = open(os.path.join(src, j), encoding="utf-8").read()
        open(os.path.join(out, j), "w", encoding="utf-8").write(js_segments(code, make_fn(j)))
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
    # Lithuanian-only assets (e.g. gallery images with LT text) replace the EN copies
    ov = os.path.join(os.path.dirname(__file__), "lt_overrides")
    if os.path.isdir(ov): shutil.copytree(ov, out, dirs_exist_ok=True)
    if report:
        for k, w in sorted(missing.items(), key=lambda x: x[1]): print(f"[{w}] {k[:140]}")
        print(len(missing), "untranslated segments")

def add_en_hreflang(site):
    """EN pages in the built site get the same alternates."""
    for p in PAGES:
        f = os.path.join(site, out_name(p) if p == "index-v2.html" else p)
        for target in ([f, os.path.join(site, "index-v2.html")] if p == "index-v2.html" else [f]):
            if not os.path.exists(target): continue
            doc = open(target, encoding="utf-8").read()
            if 'name="robots" content="noindex' in doc: continue
            open(target, "w", encoding="utf-8").write(add_hreflang(doc, p))

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0], args[1], "--report" in sys.argv)
    if "--en-hreflang" in sys.argv: add_en_hreflang(os.path.dirname(os.path.normpath(args[1])))
