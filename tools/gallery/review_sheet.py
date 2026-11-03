"""Builds a single self-contained HTML review sheet (dark theme, base64 images, tagged comment boxes).
Usage: python3 tools/gallery/review_sheet.py  -> tools/gallery/out/JAWZR-gallery-review.html"""
import base64, html, io, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gallery import SLIDES, OUT

def b64(path, q=82):
    buf = io.BytesIO(); Image.open(path).convert("RGB").save(buf, "JPEG", quality=q, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()

GROUPS = [("All slides · numbered like the raw images", [str(n) for n in range(2, 13)] + ["2-ultra", "3-ultra"])]
names = {c: n for c, n, _ in SLIDES}

cards = []
for title, codes in GROUPS:
    tiles = []
    for c in codes:
        tag = f"#{c} 1:1 | {names[c]}"
        tiles.append(f'''<figure class="card"><figcaption><span class="chip">#{c}</span><span class="nm">{html.escape(names[c])}</span><span class="ratio">1:1 · 1080×1080</span></figcaption>
<img src="data:image/jpeg;base64,{b64(os.path.join(OUT, c + ".png"))}" alt="{c} {html.escape(names[c])}" width="1080" height="1080">
<textarea class="cell" data-ttl="{html.escape(tag)}" placeholder="Notes for #{c}…"></textarea></figure>''')
    cards.append(f'<section><h2>{html.escape(title)}</h2><div class="grid">{"".join(tiles)}</div></section>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JAWZR gallery review</title>
<style>
:root{{--bg:#0d0f10;--card:#171a1c;--line:#2a2f33;--ink:#e9ecef;--muted:#9aa3ab;--acc:#5c78ff}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
.bar{{position:sticky;top:0;z-index:5;background:#0d0f10ee;backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:12px 20px;display:grid;grid-template-columns:1fr auto;gap:12px;align-items:start}}
.bar h1{{margin:0 0 6px;font-size:16px;letter-spacing:.04em}} .bar p{{margin:0;color:var(--muted);font-size:13px}}
#master{{width:100%;height:96px;resize:vertical;background:#0a0c0d;color:var(--ink);border:1px solid var(--line);padding:8px 10px;font:13px/1.45 ui-monospace,Menlo,monospace}}
button{{background:var(--acc);color:#fff;border:0;padding:12px 18px;font-weight:600;cursor:pointer;border-radius:6px;white-space:nowrap}}
#hint{{color:var(--muted);font-size:12px;margin-top:6px;min-height:1em}}
main{{padding:8px 20px 60px}} h2{{font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:28px 0 12px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:18px}}
.card{{margin:0;background:var(--card);border:1px solid var(--line);padding:12px;display:grid;gap:10px}}
.card figcaption{{display:flex;align-items:center;gap:10px}}
.chip{{background:var(--acc);color:#fff;font:700 12px ui-monospace,Menlo,monospace;padding:3px 7px}}
.nm{{font-weight:600}} .ratio{{margin-left:auto;color:var(--muted);font-size:12px}}
.card img{{width:100%;height:auto;display:block;border-radius:0}}
.cell{{width:100%;min-height:70px;resize:vertical;background:#0a0c0d;color:var(--ink);border:1px solid var(--line);padding:8px 10px;font:14px/1.45 system-ui,sans-serif}}
.cell:focus,#master:focus{{outline:2px solid var(--acc);outline-offset:-1px}}
</style></head><body>
<div class="bar"><div><h1>JAWZR product gallery · review</h1><p>Type notes under any tile. They collect below with their tags; press Copy all and paste the block back.</p>
<textarea id="master" readonly placeholder="Your tagged notes appear here…"></textarea><div id="hint"></div></div>
<button id="copy" type="button">Copy all</button></div>
<main>{"".join(cards)}</main>
<script>
const cells=[...document.querySelectorAll("textarea.cell")],master=document.getElementById("master"),hint=document.getElementById("hint");
function collect(){{master.value=cells.filter(c=>c.value.trim()).map(c=>c.dataset.ttl+"\\n"+c.value.trim()).join("\\n\\n");}}
cells.forEach(c=>c.addEventListener("input",collect));
document.getElementById("copy").addEventListener("click",async()=>{{
  collect(); master.focus(); master.select();
  let ok=false; try{{await navigator.clipboard.writeText(master.value);ok=true}}catch(e){{try{{ok=document.execCommand("copy")}}catch(e2){{}}}}
  hint.textContent=ok?"Copied "+(master.value?master.value.split("\\n\\n").length:0)+" note(s).":"Copy blocked: click the box, then Ctrl/Cmd+A and Ctrl/Cmd+C.";
}});
</script></body></html>'''
path = os.path.join(OUT, "JAWZR-gallery-review.html")
open(path, "w", encoding="utf-8").write(page)
print(path, round(os.path.getsize(path) / 1e6, 2), "MB")
