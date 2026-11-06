"""Insert Open Graph / Twitter / canonical tags into the EN pages (idempotent, between <!--og--> markers).
The LT build translates og:title / og:description and swaps url, image and locale (see build_lt.py)."""
import re, glob, os, html
SITE = "https://jawzr.com"
os.chdir(os.path.join(os.path.dirname(__file__), "../../website"))
HOME_DESC = "Hard chewing gum for jaw training. Two hardness levels, sugar-free and vegan. Ships from Lithuania."
LT_PAGES = {"index.html","gums.html","gum.html","checkout.html","terms.html","returns.html","shipping.html","privacy.html","safety.html","legal.html"}
IMG = {"gums.html": "og-gums", "gum.html": "og-gums"}
TITLE = {"gums.html": "JAWZR Hard & Ultra Hard Gum", "gum.html": "JAWZR Hard & Ultra Hard Gum"}
SKIP = {"v1.html", "product-pick.html", "index-v2.html", "product-sub.html", "product.html"}
for f in sorted(glob.glob("*.html")):
    if f in SKIP: continue
    s = open(f, encoding="utf-8").read()
    s = re.sub(r"<!--og-->.*?<!--/og-->\n?", "", s, flags=re.S)
    title = TITLE.get(f) or html.unescape(re.search(r"<title>([^<]*)", s).group(1))
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = html.unescape(m.group(1)) if m else HOME_DESC
    path = "" if f == "index.html" else f[:-5]
    img = IMG.get(f, "og-home")
    e = lambda t: html.escape(t, quote=True)
    tags = [f'<link rel="canonical" href="{SITE}/{path}">'] if 'rel="canonical"' not in s else []
    if not m: tags.append(f'<meta name="description" content="{e(desc)}">')
    tags += [
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="JAWZR">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{SITE}/{path}">',
        f'<meta property="og:image" content="{SITE}/images/{img}-en.jpg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="JAWZR hard chewing gum">',
        '<meta property="og:locale" content="en_US">',
    ]
    if f in LT_PAGES: tags += ['<meta property="og:locale:alternate" content="de_DE">', '<meta property="og:locale:alternate" content="lt_LT">']
    tags += ['<meta name="twitter:card" content="summary_large_image">',
             f'<meta name="twitter:image" content="{SITE}/images/{img}-en.jpg">']
    s = s.replace("</head>", "<!--og-->\n" + "\n".join(tags) + "\n<!--/og-->\n</head>", 1)
    open(f, "w", encoding="utf-8").write(s)
    print(f, "|", title, "|", img)
