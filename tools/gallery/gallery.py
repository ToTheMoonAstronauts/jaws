"""JAWZR product-gallery slides: layer text/graphics in code on top of untouched raw images.
Usage:  python3 tools/gallery/gallery.py      -> tools/gallery/out/G01..G12.png
One layout function per slide; copy follows docs/09-gallery-brief.md."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW, OUT, FONTS = (os.path.join(HERE, d) for d in ("raw", "out", "fonts"))
os.makedirs(OUT, exist_ok=True)
S = 1080  # 1:1 canvas

# ---- brand constants
INK = (18, 22, 20)
WHITE = (255, 255, 255)
COBALT = (36, 64, 230)
COBALT_LT = (127, 149, 255)   # accent on dark backgrounds
NAVY = (12, 42, 79)
NAVY_DK = (7, 22, 44)
OCEAN = (47, 120, 196)
LT_FLAG = [(253, 185, 19), (0, 106, 68), (193, 39, 45)]
M = 64  # outer margin

def F(kind, size):
    return ImageFont.truetype(os.path.join(FONTS, {
        "head": "BigShoulders-Black.ttf", "head2": "BigShoulders-ExtraBold.ttf",
        "mono": "Mono-Bold.ttf", "mono2": "Mono-SemiBold.ttf",
        "body": "Plex-Regular.ttf", "semi": "Plex-SemiBold.ttf", "bold": "Plex-Bold.ttf"}[kind]), size)

# ---- helpers
def cover(path, focus=(0.5, 0.5)):
    im = Image.open(path).convert("RGB")
    w, h = im.size; sc = max(S / w, S / h)
    im = im.resize((round(w * sc), round(h * sc)), Image.LANCZOS)
    x = int((im.width - S) * focus[0]); y = int((im.height - S) * focus[1])
    return im.crop((x, y, x + S, y + S)).convert("RGBA")

def scrim(img, side, size, color=NAVY_DK, alpha=200, box=None):
    """Soft gradient from one edge ('top','bottom','left','right') covering `size` px, max opacity `alpha`."""
    x0, y0, x1, y1 = box or (0, 0, S, S)
    w, h = x1 - x0, y1 - y0
    g = Image.new("L", (w, h), 0); gd = ImageDraw.Draw(g)
    n = size
    for i in range(n):
        a = int(alpha * (1 - i / n) ** 1.6)
        if side == "top": gd.line([(0, i), (w, i)], fill=a)
        if side == "bottom": gd.line([(0, h - 1 - i), (w, h - 1 - i)], fill=a)
        if side == "left": gd.line([(i, 0), (i, h)], fill=a)
        if side == "right": gd.line([(w - 1 - i, 0), (w - 1 - i, h)], fill=a)
    layer = Image.new("RGBA", (w, h), color + (0,)); layer.putalpha(g)
    img.alpha_composite(layer, (x0, y0))

def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w or not cur: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def headline(d, text, x, y, max_w, color=WHITE, size=96, min_size=54, max_lines=3, lh=0.92, kind="head", align="left"):
    """Auto-fit: largest size where the wrapped text fits max_w in <= max_lines. Returns bottom y."""
    for s in range(size, min_size - 1, -2):
        f = F(kind, s); lines = wrap(d, text, f, max_w)
        if len(lines) <= max_lines and all(d.textlength(l, font=f) <= max_w for l in lines): break
    for i, l in enumerate(lines):
        tx = x if align == "left" else x + max_w - d.textlength(l, font=f)
        d.text((tx, y + i * s * lh), l, font=f, fill=color)
    return y + len(lines) * s * lh

def para(d, text, x, y, max_w, font, color=WHITE, lh=1.32, align="left", shadow=None):
    rows = []
    for l in wrap(d, text, font, max_w):
        tx = x if align == "left" else (x + max_w - d.textlength(l, font=font) if align == "right" else x + (max_w - d.textlength(l, font=font)) / 2)
        rows.append((tx, y, l)); y += font.size * lh
    if shadow is not None: shadow_text(shadow, rows, font); d = ImageDraw.Draw(shadow, "RGBA")
    for tx, ty, l in rows: d.text((tx, ty), l, font=font, fill=color)
    return y

def chip(d, x, y, text, size=26, fill=COBALT, color=WHITE, pad=10):
    """Label on a solid cobalt block (same colour as the callout dots). Returns bottom y."""
    f = F("mono", size); w = d.textlength(text, font=f)
    d.rectangle([x, y, x + w + pad * 2, y + size * 1.45], fill=fill); d.text((x + pad, y + size * 0.16), text, font=f, fill=color)
    return y + size * 1.45

def dot(d, x, y, color=COBALT, r=17):
    d.ellipse([x - r - 9, y - r - 9, x + r + 9, y + r + 9], fill=color + (70,))
    d.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=WHITE, width=3)
    d.line([(x - 8, y), (x + 8, y)], fill=WHITE, width=3); d.line([(x, y - 8), (x, y + 8)], fill=WHITE, width=3)

def shadow_text(img, items, font, blur=4, alpha=230, offset=(0, 2)):
    """Soft dark shadow under text items [(x, y, text)] drawn onto img before the text itself."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    for x, y, t in items:
        ld.text((x + offset[0], y + offset[1]), t, font=font, fill=(0, 0, 0, alpha))
        ld.text((x, y), t, font=font, fill=(0, 0, 0, alpha), stroke_width=2, stroke_fill=(0, 0, 0, alpha))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))

def callout(d, at, label, side, text_x, width=300, color=WHITE, line=COBALT_LT, dotc=COBALT, size=22, shadow=None):
    """Dot on the subject at `at`; label block on `side` ('left'|'right') starting/ending at text_x; line joins them."""
    f = F("mono", size); x, y = at
    lines = wrap(d, label, f, width); h = len(lines) * size * 1.25
    ty = y - h / 2
    if shadow is not None:
        pos = [((text_x - d.textlength(l, font=f)) if side == "left" else text_x, ty + i * size * 1.25, l) for i, l in enumerate(lines)]
        shadow_text(shadow, pos, f)
    if side == "left":
        for i, l in enumerate(lines):
            d.text((text_x - d.textlength(l, font=f), ty + i * size * 1.25), l, font=f, fill=color)
        d.line([(text_x + 14, y), (x - 24, y)], fill=line, width=3)
    else:
        for i, l in enumerate(lines):
            d.text((text_x, ty + i * size * 1.25), l, font=f, fill=color)
        d.line([(x + 24, y), (text_x - 14, y)], fill=line, width=3)
    dot(d, x, y, dotc)

def pill(d, cx, cy, text, fill=COBALT, color=WHITE, size=24, padx=34, h=58):
    f = F("mono", size); w = d.textlength(text, font=f) + padx * 2
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h / 2, fill=fill)
    d.text((cx - w / 2 + padx, cy - size * 0.62), text, font=f, fill=color)

def wordmark(img, x, y, h=34, color=WHITE, anchor="br"):
    """JAWZR wordmark from brand PNG, tinted."""
    wm = Image.open(os.path.join(HERE, "..", "..", "brand", "jawzr-wordmark.png")).convert("RGBA")
    wm = wm.resize((round(wm.width * h / wm.height), h), Image.LANCZOS)
    tint = Image.new("RGBA", wm.size, color + (255,)); tint.putalpha(wm.split()[3])
    px = x - wm.width if "r" in anchor else x; py = y - h if "b" in anchor else y
    img.alpha_composite(tint, (int(px), int(py)))

def cite(d, x, y, items, max_w, label="STUDIES:", color=WHITE, accent=COBALT_LT, size=17):
    fb, fr, fl = F("bold", size), F("body", size), F("mono", size + 1)
    d.text((x, y), label, font=fl, fill=accent); y += size * 1.9
    for who, rest in items:
        # bold author/year, then regular remainder, wrapped together
        words = [(w, fb) for w in (who + ":").split()] + [(w, fr) for w in rest.split()]
        cx, line_h = x, size * 1.35
        for w, f in words:
            ww = d.textlength(w + " ", font=f)
            if cx + ww - x > max_w: cx = x; y += line_h
            d.text((cx, y), w, font=f, fill=color); cx += ww
        y += line_h + size * 0.7
    return y

def rating(d, x, y, n, of=5, color=COBALT, r=11, gap=30, half=False):
    for i in range(of):
        cx = x + i * gap
        if i < n: d.ellipse([cx - r, y - r, cx + r, y + r], fill=color)
        elif half and i == n:
            d.ellipse([cx - r, y - r, cx + r, y + r], outline=color, width=3); d.pieslice([cx - r, y - r, cx + r, y + r], 90, 270, fill=color)
        else: d.ellipse([cx - r, y - r, cx + r, y + r], outline=color, width=3)

def save(img, code):
    p = os.path.join(OUT, code + ".png"); img.convert("RGB").save(p, optimize=True); return p

# ---- slides (one layout function each)
def g01_product():
    im = cover(os.path.join(RAW, "2.png")); scrim(im, "top", 380, alpha=150); scrim(im, "bottom", 360, alpha=200)
    d = ImageDraw.Draw(im, "RGBA")
    headline(d, "HARDNESS YOU CAN TASTE.", M, 56, 820, size=112, max_lines=2)
    callout(d, (430, 370), "BUILT TO RESIST YOUR BITE", "left", 330, width=290, size=29, shadow=im); d = ImageDraw.Draw(im, "RGBA")
    callout(d, (650, 470), "FLAVOUR THAT LASTS THE SESSION", "right", 750, width=290, size=29, shadow=im); d = ImageDraw.Draw(im, "RGBA")
    fb, fr = F("bold", 38), F("body", 31)
    shadow_text(im, [(M, 900, "Sugar-free"), (362, 900, "JAWZR HARD")], fb); shadow_text(im, [(M, 947, "and vegan"), (362, 947, "Dense, low-softener gum base")], fr)
    d = ImageDraw.Draw(im, "RGBA")
    d.text((M, 900), "Sugar-free", font=fb, fill=WHITE); d.text((M, 947), "and vegan", font=fr, fill=WHITE)
    d.line([(330, 902), (330, 990)], fill=COBALT_LT, width=3)
    d.text((362, 900), "JAWZR HARD", font=fb, fill=WHITE); d.text((362, 947), "Dense, low-softener gum base", font=fr, fill=WHITE)
    return save(im, "G01")

def g02_softdiet():
    im = cover(os.path.join(RAW, "3.png")); scrim(im, "top", 330, alpha=170)
    scrim(im, "left", 360, alpha=200); scrim(im, "right", 360, alpha=200)
    d = ImageDraw.Draw(im, "RGBA")
    headline(d, "MODERN SOFT DIET", M, 50, 360, size=92, max_lines=3)
    headline(d, "JAWZR HARD GUM", S - M - 360, 50, 360, size=92, max_lines=3, align="right", color=WHITE)
    d.line([(540, 360), (540, 1080)], fill=WHITE + (90,), width=2)
    L = [((415, 560), "SOFT, PROCESSED FOOD"), ((395, 690), "ALMOST NO RESISTANCE"), ((440, 820), "YOUR JAW MUSCLES BARELY WORK")]
    R = [((665, 560), "REAL RESISTANCE, LIKE TOUGH FOOD"), ((690, 690), "TRAINS YOUR MAIN CHEWING MUSCLE"), ((640, 820), "8–15 MIN A DAY, 30-DAY PLAN")]
    # labels 30% larger than v1 (20 -> 26 px) with a soft dark shadow; one draw per callout so shadows sit under their own text
    for at, t in L:
        callout(d, at, t, "left", 300, width=250, size=26, shadow=im); d = ImageDraw.Draw(im, "RGBA")
    for at, t in R:
        callout(d, at, t, "right", 780, width=250, size=26, shadow=im); d = ImageDraw.Draw(im, "RGBA")
    return save(im, "G02")

def g03_howto():
    im = cover(os.path.join(RAW, "4.png")); d = ImageDraw.Draw(im, "RGBA")
    steps = ["Place a fresh piece on your back teeth.", "Warm it up for about a minute (a cold bite can crack it).",
             "Chew slowly and firmly, mouth closed.", "Bite all the way through, every time."]
    for i, t in enumerate(steps):
        px, py = (i % 2) * 540, (i // 2) * 540
        scrim(im, "bottom", 300, color=NAVY_DK, alpha=225, box=(px, py, px + 540, py + 540))
        d = ImageDraw.Draw(im, "RGBA")
        d.text((px + 36, py + 318), f"0{i+1}.", font=F("head", 104), fill=WHITE)
        para(d, t, px + 38, py + 428, 470, F("semi", 30), shadow=im); d = ImageDraw.Draw(im, "RGBA")
    # pro tip on panel 4 (top of the panel, over a soft scrim)
    scrim(im, "top", 230, color=NAVY_DK, alpha=205, box=(540, 540, 1080, 1080)); d = ImageDraw.Draw(im, "RGBA")
    y = chip(d, 576, 560, "PRO TIP", size=22)
    para(d, "WANT MORE FLAVOUR? CHEW ONE HARD AND ONE ULTRA HARD PIECE TOGETHER. WHEN IT GOES SOFT, ADD A FRESH PIECE.", 576, y + 10, 470, F("mono2", 22), lh=1.35, shadow=im)
    d = ImageDraw.Draw(im, "RGBA")
    d.line([(540, 0), (540, 1080)], fill=WHITE, width=4); d.line([(0, 540), (1080, 540)], fill=WHITE, width=4)
    return save(im, "G03")

def g04_science():
    im = cover(os.path.join(RAW, "5.png")); scrim(im, "top", 360, alpha=170)
    scrim(im, "bottom", 320, color=(244, 244, 241), alpha=240)   # light band so the studies can be black
    d = ImageDraw.Draw(im, "RGBA")
    headline(d, "THE SCIENCE: IT'S MUSCLE, NOT BONE.", M, 52, 600, size=100, max_lines=3)
    callout(d, (360, 690), "MASSETER: TRAINED BY RESISTANCE", "left", 250, width=225, size=27, shadow=im); d = ImageDraw.Draw(im, "RGBA")
    callout(d, (690, 790), "BONE STRUCTURE STAYS THE SAME", "right", 790, width=250, size=27, shadow=im); d = ImageDraw.Draw(im, "RGBA")
    cite(d, M, 892, [("RAADSHEER M.C. ET AL. (1999)", "Contribution of jaw muscle size and craniofacial morphology to human bite force magnitude. Journal of Dental Research, 78(1), 31–42."),
                     ("JUNG H.-J. ET AL. (2024)", "Effects of gum chewing training on occlusal force, masseter muscle thickness and mandibular shape: a randomised controlled clinical trial. Journal of Oral Rehabilitation.")],
         950, color=INK, accent=COBALT, size=20)
    return save(im, "G04")

def g05_feel():
    im = cover(os.path.join(RAW, "6.png"))
    scrim(im, "left", 480, alpha=220, box=(0, 0, S, 540)); scrim(im, "right", 460, alpha=240, box=(0, 540, S, 1080))
    d = ImageDraw.Draw(im, "RGBA")
    headline(d, "FEEL IT WORKING.", M, 48, 380, size=96, max_lines=2)
    # top: relaxed, dot on the left masseter. Labels sit on cobalt chips (same colour as the dot)
    y = chip(d, M, 382, "RELAX", size=28)
    para(d, "Put two fingers on the dot.", M, y + 10, 260, F("semi", 32), shadow=im); d = ImageDraw.Draw(im, "RGBA")
    d.line([(M + 132, 396), (250, 330)], fill=COBALT_LT, width=3); dot(d, 268, 312)
    # bottom: clenched, dot on the right masseter
    x = 846
    y = chip(d, x, 588, "CLENCH", size=28)
    para(d, "That's your masseter: the muscle JAWZR trains.", x, y + 10, 210, F("semi", 29), shadow=im); d = ImageDraw.Draw(im, "RGBA")
    d.line([(x - 10, 790), (826, 828)], fill=COBALT_LT, width=3); dot(d, 810, 846)
    d.line([(0, 540), (1080, 540)], fill=WHITE, width=4)
    return save(im, "G05")

def g06_problem():
    im = cover(os.path.join(RAW, "7.png")); scrim(im, "bottom", 540, color=NAVY_DK, alpha=240)
    d = ImageDraw.Draw(im, "RGBA")
    d.text((M, 56), "The 30-day JAWZR plan.", font=F("semi", 32), fill=INK)
    headline(d, "WHY YOUR JAW NEEDS WORK.", M, 104, 380, color=INK, size=96, max_lines=4)
    y = 600
    for lab, txt in [("THE PROBLEM", "Modern soft food gives your jaw almost no work."),
                     ("THE TRUTH", "For most of history, people chewed tough, raw food every day."),
                     ("THE SOLUTION", "Bring the resistance back: 8–15 minutes a day with JAWZR.")]:
        y = chip(d, M, y, lab, size=26) + 8
        y = para(d, txt, M, y, 700, F("semi", 31), shadow=im) + 18; d = ImageDraw.Draw(im, "RGBA")
    f = F("mono", 26)
    shadow_text(im, [(M, 1010, "FAST SHIPPING")], f); t = "SUGAR-FREE · VEGAN · 40 PIECES"
    shadow_text(im, [(S - M - d.textlength(t, font=f), 1010, t)], f); d = ImageDraw.Draw(im, "RGBA")
    d.text((M, 1010), "FAST SHIPPING", font=f, fill=WHITE)
    d.text((S - M - d.textlength(t, font=f), 1010), t, font=f, fill=WHITE)
    return save(im, "G06")

def g07_skulls():
    im = cover(os.path.join(RAW, "8.png")); d = ImageDraw.Draw(im, "RGBA")
    headline(d, "WHY MODERN JAWS DO LESS WORK.", M, 52, 900, color=INK, size=104, max_lines=2)
    c1, c2, lx = 430, 770, M
    fh = F("mono", 28)
    for cx, t in [(c1, "PRE-INDUSTRIAL"), (c2, "MODERN")]:
        d.text((cx - d.textlength(t, font=fh) / 2, 584), t, font=fh, fill=INK)
    rows = [("Lower jaw", "Broad, robust", "Shorter, narrower"), ("Dental arch", "Broad", "Narrower, more crowding"), ("Diet", "Tough, raw food", "Soft, processed food")]
    y = 635; fl, fv = F("bold", 28), F("body", 26)
    d.line([(lx, y), (S - M, y)], fill=COBALT, width=2)
    for lab, a, b in rows:
        last = lab == "Diet"
        d.text((lx, y + 24), lab, font=fl, fill=COBALT if last else INK)
        for cx, t in [(c1, a), (c2, b)]:
            d.text((cx - d.textlength(t, font=fv) / 2, y + 26), t, font=fv, fill=COBALT if last else INK)
        y += 84; d.line([(lx, y), (S - M, y)], fill=COBALT, width=2)
    yy = para(d, "Differences built up over generations. Gum trains the muscle; it doesn't reshape adult bone.", lx, y + 16, 950, F("body", 26), color=INK)
    cite(d, lx, yy + 10, [("VON CRAMON-TAUBADEL N. (2011)", "Global human mandibular variation reflects differences in agricultural and hunter-gatherer subsistence strategies. PNAS, 108(49), 19546–19551.")],
         950, label="STUDY:", color=INK, accent=COBALT, size=20)
    return save(im, "G07")

def g08_compare():
    im = cover(os.path.join(RAW, "9.png")); d = ImageDraw.Draw(im, "RGBA")
    headline(d, "HARD VS. ULTRA HARD.", M, 52, 620, color=INK, size=112, max_lines=2)
    c1, c2, lx = 520, 865, M
    fh = F("mono", 29)
    for cx, t in [(c1, "HARD"), (c2, "ULTRA HARD")]:
        d.text((cx - d.textlength(t, font=fh) / 2, 605), t, font=fh, fill=INK)
    y = 650; fl, fv = F("bold", 30), F("body", 27)
    d.line([(lx, y), (S - M, y)], fill=COBALT, width=2)
    rows = [("Hardness", ("r", 4, False), ("r", 5, False)), ("Flavour", ("r", 5, False), ("r", 1, False)),
            ("Use in the plan", ("t", "Week 1 + light days"), ("t", "Full days from week 2")),
            ("Sweeteners", ("t", "Polyols + stevia, sucralose"), ("t", "Maltitol only"))]
    for lab, a, b in rows:
        d.text((lx, y + 22), lab, font=fl, fill=COBALT)
        for cx, v in [(c1, a), (c2, b)]:
            if v[0] == "r": rating(d, cx - 60, y + 42, v[1], half=v[2])
            else: d.text((cx - d.textlength(v[1], font=fv) / 2, y + 26), v[1], font=fv, fill=INK)
        y += 82; d.line([(lx, y), (S - M, y)], fill=COBALT, width=2)
    t = "Best together: the 30-day plan uses both."
    d.text((lx, y + 22), t, font=F("semi", 31), fill=INK)
    return save(im, "G08")

def g09_why():
    im = cover(os.path.join(RAW, "10.png"))
    # the raw contains third-party press logos -> fully covered by an overlay panel (pixels underneath untouched)
    panel = Image.new("RGBA", (S, S)); pd = ImageDraw.Draw(panel)
    for y in range(S):
        t = y / S; c = tuple(int(NAVY_DK[i] * (1 - t) + OCEAN[i] * t * 0.55 + NAVY[i] * t * 0.45) for i in range(3))
        pd.line([(0, y), (S, y)], fill=c + (255,))
    im.alpha_composite(panel); d = ImageDraw.Draw(im, "RGBA")
    headline(d, "WHY JAWZR.", M, 60, 700, size=120, max_lines=1)
    items = ["SUGAR-FREE", "100% VEGAN", "2 HARDNESS LEVELS", "40 PIECES PER PACK", "30-DAY PLAN INCLUDED", "FAST SHIPPING", "FREE EU SHIPPING FROM €49", "14-DAY RETURNS ON SEALED PACKS"]
    f = F("head2", 46)
    for i, t in enumerate(items):
        x = M + (i % 2) * 490; y = 300 + (i // 2) * 165
        d.ellipse([x, y + 6, x + 44, y + 50], outline=COBALT_LT, width=4)
        d.line([(x + 12, y + 29), (x + 20, y + 37), (x + 34, y + 20)], fill=COBALT_LT, width=4)
        lines = wrap(d, t, f, 380)
        for k, l in enumerate(lines): d.text((x + 64, y + k * 46), l, font=f, fill=WHITE)
    wordmark(im, S - M, S - 56, h=36)
    return save(im, "G09")

def g10_challenge():
    im = cover(os.path.join(RAW, "11.png")); scrim(im, "bottom", 460, color=NAVY_DK, alpha=240)
    d = ImageDraw.Draw(im, "RGBA")
    d.line([(540, 0), (540, 730)], fill=WHITE, width=4)
    headline(d, "TAKE THE 30-DAY JAWZR CHALLENGE.", M, 790, 950, size=84, max_lines=2)
    pill(d, 270, 1012, "YOUR DAY 1", size=31, h=74, padx=40); pill(d, 810, 1012, "YOUR DAY 30", size=31, h=74, padx=40)
    return save(im, "G10")

def g11_share():
    im = cover(os.path.join(RAW, "12.png")); scrim(im, "bottom", 440, color=NAVY_DK, alpha=240)
    d = ImageDraw.Draw(im, "RGBA")
    d.line([(540, 0), (540, 760)], fill=WHITE, width=4)
    headline(d, "JOIN THE #JAWZRCHALLENGE.", M, 830, 950, size=84, max_lines=2)
    pill(d, 270, 1012, "YOUR DAY 1", size=31, h=74, padx=40); pill(d, 810, 1012, "YOUR DAY 30", size=31, h=74, padx=40)
    return save(im, "G11")

def g12_plan():
    """No raw image for this one: navy/ocean gradient background built in code."""
    im = Image.new("RGBA", (S, S)); d = ImageDraw.Draw(im)
    for y in range(S):
        t = y / S; d.line([(0, y), (S, y)], fill=tuple(int(NAVY_DK[i] * (1 - t) + OCEAN[i] * t * 0.7) for i in range(3)) + (255,))
    d = ImageDraw.Draw(im, "RGBA")
    headline(d, "YOUR 30-DAY PLAN.", M, 56, 900, size=116, max_lines=1)
    fm, fs = F("mono", 22), F("semi", 30)
    d.rectangle([M, 210, M + 30, 240], fill=COBALT); d.text((M + 44, 203), "FULL DAY: 3 rounds, 10–15 min", font=fs, fill=WHITE)
    d.rectangle([M + 530, 210, M + 560, 240], outline=COBALT_LT, width=3); d.text((M + 574, 203), "LIGHT DAY: 1 round, ~8 min", font=fs, fill=WHITE)
    cell, gap, x0, y0 = 118, 14, M, 300
    for i in range(30):
        r, c = divmod(i, 7) if False else divmod(i, 6)
        x, y = x0 + c * (cell + 14 + 20), y0 + r * (cell - 10 + gap)
        full = i % 2 == 0
        box = [x, y, x + cell + 20, y + cell - 10]
        if r == 0 and False: pass
        if full: d.rounded_rectangle(box, 10, fill=COBALT)
        else: d.rounded_rectangle(box, 10, outline=COBALT_LT, width=3)
        d.text((x + 14, y + 10), f"{i+1}", font=F("head", 40), fill=WHITE)
        lvl = "HARD" if i < 7 or not full else "ULTRA"
        d.text((x + 14, y + 62), lvl, font=F("mono", 22), fill=WHITE if full else COBALT_LT)
    d.text((M, 928), "WEEK 1: HARD EVERY DAY", font=F("mono", 24), fill=WHITE)
    d.text((M, 962), "WEEKS 2–4: ULTRA HARD ON FULL DAYS, HARD ON LIGHT DAYS", font=F("mono", 24), fill=WHITE)
    d.text((M, 1010), "Never more than 15 minutes a day. Stop if it hurts.", font=F("semi", 30), fill=WHITE)
    wordmark(im, S - M, S - 46, h=30)
    return save(im, "G12")

SLIDES = [("G01", "Product close-up", g01_product), ("G02", "Soft diet vs JAWZR", g02_softdiet), ("G03", "How to chew", g03_howto),
          ("G04", "Muscle, not bone", g04_science), ("G05", "Feel it working", g05_feel), ("G06", "Problem · truth · solution", g06_problem),
          ("G07", "Skull table", g07_skulls), ("G08", "Hard vs Ultra Hard", g08_compare), ("G09", "Why JAWZR (replaces press logos)", g09_why),
          ("G10", "30-day challenge invite", g10_challenge), ("G11", "Join the challenge", g11_share), ("G12", "30-day plan calendar", g12_plan)]

if __name__ == "__main__":
    for code, name, fn in SLIDES: print(code, fn())
