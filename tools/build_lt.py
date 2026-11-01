"""Rebuild website-lt/ from website/: copy, then translate with tools/lt_dict.py. Run: python3 tools/build_lt.py"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from lt_dict import PAIRS
R=os.path.join(os.path.dirname(__file__),"..")
SRC,DST=os.path.join(R,"website"),os.path.join(R,"website-lt")
shutil.rmtree(DST,ignore_errors=True)
shutil.copytree(SRC,DST,ignore=shutil.ignore_patterns("index.html","terms.html","returns.html","withdraw.html","shipping.html","privacy.html","safety.html","legal.html"))
os.rename(os.path.join(DST,"index-v2.html"),os.path.join(DST,"index.html"))
files=["index.html","product.html","checkout.html","assets/site.js"]
used=set()
for f in files:
    p=os.path.join(DST,f);s=open(p,encoding="utf-8").read().replace("index-v2.html","index.html")
    for i,(en,lt) in enumerate(sorted(PAIRS,key=lambda x:-len(x[0]))):
        if en in s: s=s.replace(en,lt);used.add(en)
    open(p,"w",encoding="utf-8").write(s)
miss=[en for en,lt in PAIRS if en not in used]
print("translated",len(used),"/",len(PAIRS));[print("  MISSING:",m[:90].replace("\n"," ")) for m in miss]
