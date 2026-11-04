"""Builds the JAWZR journal: website/articles.html + website/article-<slug>.html
Usage: python3 tools/articles/build.py"""
import os, re, html, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "website")
legal = open(os.path.join(ROOT, "legal.html"), encoding="utf-8").read()
HEAD_END = legal.index("<style>")
FONTS_HEAD = legal[:HEAD_END]
TAIL = legal[legal.index("</main>") + len("</main>"):]

CSS = """<style>
.jr{max-width:760px;padding-block:36px 40px}
.jr h1{font-size:clamp(2.4rem,6vw,3.8rem);margin-top:10px;line-height:.98}
.jr .meta{color:var(--muted);font-size:.85rem;margin-top:12px;font-family:var(--mono)}
.jr .jhero{margin:24px 0 8px;border-radius:10px;overflow:hidden;aspect-ratio:16/9;background:var(--soft);min-height:0}
.jr .jhero img{width:100%;height:100%;object-fit:cover;display:block}
.jr .lead{font-size:1.15rem;line-height:1.6;color:#2A302D;margin-top:18px}
.jr .body{display:grid;gap:14px;margin-top:18px}
.jr .body h2{font-size:1.7rem;margin-top:22px}
.jr .body p,.jr .body li{line-height:1.7;color:#2A302D}
.jr .body ul,.jr .body ol{margin:0;padding-left:22px;display:grid;gap:6px}
.jr .key{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:16px 18px}
.jr .key b{display:block;font:600 .74rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.jr .src{margin-top:30px;border-top:1px solid var(--line);padding-top:18px;font-size:.88rem}
.jr .src h3{font-size:1.1rem;margin-bottom:8px}
.jr .src ol{padding-left:20px;display:grid;gap:6px;color:var(--muted)}
.jr .cta{margin-top:30px;background:var(--ink);color:var(--bg);border-radius:10px;padding:22px;display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.jr .cta p{margin:0;max-width:44ch}
.jr .note{font-size:.8rem;color:var(--muted);margin-top:18px}
.jgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:26px}
.jcard{display:grid;gap:10px;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden;transition:border-color .15s,transform .15s}
.jcard:hover{border-color:var(--accent);transform:translateY(-2px)}
.jcard{min-width:0}.jcard .im{aspect-ratio:16/10;background:var(--soft);overflow:hidden;min-height:0}.jcard .im img{width:100%;height:100%;object-fit:cover;display:block}
.jcard .tx{padding:4px 16px 18px;display:grid;gap:8px}
.jcard h3{font-size:1.35rem;line-height:1.05}
.jcard p{font-size:.9rem;color:var(--muted);margin:0}
.jcard .t{font:600 .7rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--accent-deep)}
.jlist{max-width:1100px;padding-block:36px 50px}
@media(max-width:900px){.jgrid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.jgrid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="top-bar"><div class="wrap">Free EU shipping from €49 · Ships from Lithuania</div></div>
<nav class="site"><div class="wrap">
  <a class="logo" href="index-v2.html"><i></i><span class="wm" aria-hidden="true"></span><span class="sr">JAWZR</span></a>
  <div class="links"><a href="product-sub.html">Shop</a><a href="index-v2.html#how">How it works</a><a href="articles.html">Articles</a><a href="index-v2.html#faq">FAQ</a></div>
  <button class="cart-btn" type="button" data-open-cart>Cart (<span data-cart-count>0</span>)</button>
</div></nav>
"""

def head(title, desc, extra=""):
    h = FONTS_HEAD.replace("<title>Legal Notice · JAWZR</title>", f"<title>{html.escape(title)}</title>\n<meta name=\"description\" content=\"{html.escape(desc)}\">{extra}")
    return h + CSS

from articles_content import ARTICLES

def card(a):
    return f'''<a class="jcard" href="article-{a["slug"]}.html"><div class="im"><img src="{a["img"]}"{' style="object-fit:contain;background:#fff"' if a.get("fit") else ""} alt="" loading="lazy"></div><div class="tx"><span class="t">{a["tag"]} · {a["mins"]} min read</span><h3>{html.escape(a["title"])}</h3><p>{html.escape(a["desc"])}</p></div></a>'''

for a in ARTICLES:
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": "2026-11-04", "author": {"@type": "Organization", "name": "JAWZR"}, "publisher": {"@type": "Organization", "name": "JAWZR"}}
    others = [o for o in ARTICLES if o["slug"] != a["slug"]][:3]
    srcs = "".join(f"<li>{s}</li>" for s in a["sources"])
    page = head(a["title"] + " · JAWZR", a["desc"], f'\n<script type="application/ld+json">{json.dumps(ld)}</script>') + f'''<main class="wrap jr">
  <p class="eyebrow"><a href="articles.html" style="color:inherit;text-decoration:none">Articles</a> · {a["tag"]}</p>
  <h1>{html.escape(a["title"])}</h1>
  <p class="meta">JAWZR team · 4 November 2026 · {a["mins"]} min read</p>
  <div class="jhero"><img src="{a["img"]}"{' style="object-fit:contain;background:#fff"' if a.get("fit") else ""} alt="{html.escape(a["alt"])}"></div>
  <p class="lead">{a["lead"]}</p>
  <div class="key"><b>In short</b>{a["short"]}</div>
  <div class="body">{a["body"]}</div>
  <div class="cta"><p><b>Want to train your jaw?</b> JAWZR hard gum comes with a 30-day plan: 8–15 minutes a day, alternating full and light days.</p><a class="btn" href="product-sub.html">Shop hard gum</a></div>
  <div class="src"><h3>Sources</h3><ol>{srcs}</ol></div>
  <p class="note">This article is general information, not medical or dental advice. If you have jaw, joint or dental problems, ask a dentist before training your jaw.</p>
</main>
<section style="padding-top:0"><div class="wrap jlist" style="padding-top:0"><div class="sec-head"><p class="eyebrow">Keep reading</p><h2>More articles</h2></div><div class="jgrid">{"".join(card(o) for o in others)}</div></div></section>
''' + TAIL
    open(os.path.join(ROOT, f'article-{a["slug"]}.html'), "w", encoding="utf-8").write(page)

idx = head("Articles on jaw training and hard gum · JAWZR", "Plain-language articles on jaw muscles, hard gum training and what the research says.") + f'''<main class="wrap jlist">
  <p class="eyebrow">JAWZR journal</p>
  <h1 style="font-size:clamp(2.6rem,6vw,4rem);margin-top:10px">Jaw training, explained</h1>
  <p class="lede" style="margin-top:14px;max-width:60ch">What your chewing muscles do, what hard-gum training can and can't change, and what the studies actually found.</p>
  <div class="jgrid">{"".join(card(a) for a in ARTICLES)}</div>
</main>
''' + TAIL
open(os.path.join(ROOT, "articles.html"), "w", encoding="utf-8").write(idx)
# homepage teaser snippet
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_teaser.html"), "w").write("".join(card(a) for a in ARTICLES[:3]))
print("built", len(ARTICLES), "articles")
