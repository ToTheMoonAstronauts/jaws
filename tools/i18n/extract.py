"""List every English segment of the pages we translate, merged into lt.json (keeps existing translations).
Run: python3 tools/i18n/extract.py   -> prints how many are missing."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from segments import html_segments, js_segments
R = os.path.join(os.path.dirname(__file__), "..", "..", "website")
from pages import PAGES, JS
path = os.path.join(os.path.dirname(__file__), "lt.json")
lt = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
seen = {}
def keep(t, src):
    seen.setdefault(t, src); return t
for p in PAGES: html_segments(open(os.path.join(R, p), encoding="utf-8").read(), lambda t, p=p: keep(t, p))
for j in JS: js_segments(open(os.path.join(R, j), encoding="utf-8").read(), lambda t, j=j: keep(t, j))
out = {k: lt.get(k, "") for k in seen}
json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
miss = [k for k, v in out.items() if not v]
print(len(out), "segments,", len(miss), "untranslated")
if "-v" in sys.argv:
    for k in miss: print("  ", seen[k], "|", k[:110])
