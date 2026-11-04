"""Hard/jaw-gum price dataset, collected 2026-11-04. EUR conversion: ECB 2 Nov 2026 (1 EUR = 1.1216 USD = 0.8358 GBP).
Amazon.com rows: price shown by Amazon to a Lithuanian buyer in EUR (Amazon FX ~0.895 EUR/USD); USD is the listed US price."""
import csv, statistics as st
USD, GBP = 1/1.1216, 1/0.8358
# brand, country, channel, product, level, pieces, grams, price, cur, price_eur_override, rating, reviews, note, url
R = [
 # --- own websites
 ("Jawliner","DE","Own site","Hard, 1 pack (2-month)","Hard",40,116,24.95,"EUR",None,4.5,"2.1K","pieces derived (40 mg caffeine/piece, 1380 mg/100 g)","https://jawliner.com/products/hard-chewing-gum"),
 ("Jawliner","DE","Own site","Hard, 3 packs (6-month)","Hard",120,348,39.95,"EUR",None,None,None,"shown 'was €74.85'","https://jawliner.com/products/hard-chewing-gum"),
 ("Jawliner","DE","Own site","Hard, 6 packs (12-month)","Hard",240,696,69.95,"EUR",None,None,None,"shown 'was €149.70'","https://jawliner.com/products/hard-chewing-gum"),
 ("Jawliner","DE","Own site","Ultra Hard, 1 pack","Ultra",None,100,24.95,"EUR",None,4.5,"2.1K","sub −15%","https://jawliner.com/products/ultra-hard-fitness-chewing-gum"),
 ("Jawliner","DE","Own site","Ultra Hard, 3 packs","Ultra",None,300,39.95,"EUR",None,None,None,"","https://jawliner.com/products/ultra-hard-fitness-chewing-gum"),
 ("Jawliner","DE","Own site","Ultra Hard, 6 packs","Ultra",None,600,69.95,"EUR",None,None,None,"","https://jawliner.com/products/ultra-hard-fitness-chewing-gum"),
 ("Jawliner","DE","Own site","Starter Pack (2 packs)","Mixed",80,232,34.95,"EUR",None,None,None,"landing-page offer; free try pack €0 also exists","https://jawliner.com/products/jawliner-chewing-gum-discount"),
 ("Rockjaw","UK","Own site","Tuff Gum + B vitamins, 3-month","Hard",60,None,24.95,"EUR",None,4.6,"186","GBP 21.98; sub 15% then 35–40%","https://rockjaw.co.uk/products/rockjaw%C2%AE-jawline-gum-tuff-gum-2-0-stim-free"),
 ("Rockjaw","UK","Own site","Tuff Gum, 9-month (3 packs)","Hard",180,None,42.95,"EUR",None,None,None,"pieces inferred 3×60","https://rockjaw.co.uk/products/rockjaw%C2%AE-jawline-gum-tuff-gum-2-0-stim-free"),
 ("Rockjaw","UK","Own site","Tuff Gum, 18-month (6 packs)","Hard",360,None,66.95,"EUR",None,None,None,"pieces inferred 6×60","https://rockjaw.co.uk/products/rockjaw%C2%AE-jawline-gum-tuff-gum-2-0-stim-free"),
 ("Rockjaw","UK","Own site","Tuff Gum Performance (caffeine+taurine), 3-month","Functional",60,None,26.95,"EUR",None,None,None,"pieces assumed same as Tuff Gum","https://rockjaw.co.uk/products/rockjaw%C2%AE-tuff-gum"),
 ("Rockjaw","UK","Own site","Mastic Stackables 20 g","Mastic",None,20,23.95,"EUR",None,None,None,"","https://rockjaw.co.uk/products/rockjaw-mastic-jawline-gum-stackables"),
 ("Stronger Gum","FI","Own site","Regular, 1 pack","Medium",120,320,21.90,"EUR",None,4.4,"105","","https://strongergum.com/products/regular-strawberry-330g"),
 ("Stronger Gum","FI","Own site","Regular, 5 packs (pay 3)","Medium",600,1600,65.70,"EUR",None,None,None,"","https://strongergum.com/products/regular-set-5-packs-for-price-of-3"),
 ("Stronger Gum","FI","Own site","Extra Tough, 1 pack","Hard",60,162,23.95,"EUR",None,None,None,"","https://strongergum.com/products/extra-tough-watermelon-sugar-free-60-pieces-162g"),
 ("Stronger Gum","FI","Own site","Extra Tough, 3 packs","Hard",180,486,47.90,"EUR",None,None,None,"","https://strongergum.com/products/extra-tough-watermelon-sugar-free-60-pieces-162g"),
 ("Stronger Gum","FI","Own site","Extra Tough lightly flavoured","Hard",90,315,23.95,"EUR",None,None,None,"","https://strongergum.com/products/extra-tough-spearmint-90-pieces"),
 ("JAWCO","US","Own site","Classic, 1 pack","Hard",35,None,18.99,"USD",None,None,"138","free shipping; '2nd pack 50% off'","https://jawcogum.com/products/mighty-mint-jawline-gum"),
 ("JAWCO","US","Own site","Classic, 3 packs","Hard",105,None,49.99,"USD",None,None,None,"","https://jawcogum.com/products/mighty-mint-jawline-gum"),
 ("JAWCO","US","Own site","Classic, 6 packs","Hard",210,None,89.99,"USD",None,None,None,"","https://jawcogum.com/products/mighty-mint-jawline-gum"),
 ("JAWCO","US","Own site","Energy, 1 pack","Functional",35,None,20.99,"USD",None,None,None,"","https://jawcogum.com/products/energy-mint-jawline-gum"),
 ("Jawzrgum (Jawzrsize)","US","Own site","Mastic-style gum, 1 pack","Hard",40,None,13.99,"USD",None,None,"1,287","shown 'was $17.99'; sub −10%","https://jawzrsize.com/products/jawzrgum"),
 ("Jawzrgum (Jawzrsize)","US","Own site","6 packs","Hard",240,None,74.99,"USD",None,None,None,"","https://jawzrsize.com/products/jawzrgum"),
 ("Gymgum","US","Own site","Jawline Gum, 1 pack","Hard",40,None,19.99,"USD",None,None,"1,288","one-time; autoship $15.99, 2-pack $23.99, 4-pack $39.99","https://gymgum.co/products/jawline-chewing-gum"),
 ("Gumforce","FR","Own site","Creatine jaw gum, 1 sachet","Functional",35,94.5,29.99,"EUR",None,4.8,"849","500 mg creatine/piece; 'was €35'","https://gumforce.co/products/gumforce"),
 ("Gumforce","FR","Own site","Buy 2 get 2 (4 sachets)","Functional",140,378,49.99,"EUR",None,None,None,"'was €140'","https://gumforce.co/products/gumforce"),
 ("FitGum","FR","Own site","1 pack","Hard",40,None,29.90,"EUR",None,4.7,None,"EU store, verified 4 Nov","https://fitgum.co/products/fitgum-jawline"),
 ("FitGum","FR","Own site","2 packs","Hard",80,None,49.80,"EUR",None,None,None,"free shipping","https://fitgum.co/en-eu/products/fitgum-jawline"),
 ("FitGum","FR","Own site","3 packs","Hard",120,None,69.70,"EUR",None,None,None,"free shipping","https://fitgum.co/products/fitgum-jawline"),
 ("GrindLabs","FR","Own site","1-month","Hard",None,None,29.90,"EUR",None,None,"5K+ (claimed)","pieces not stated","https://grindlabs.fr/products/chewing-gum-grindlabs"),
 # --- Amazon.de (EUR, ships to LT)
 ("Jawliner","DE","Amazon.de","Hard, 1 pack, mint","Hard",40,116,29.34,"EUR",None,4.2,"86","+18% vs own site","https://www.amazon.de/dp/B0FKZ723HC"),
 ("Jawliner","DE","Amazon.de","Caffeine extra hard, 40 pack","Functional",40,113,28.27,"EUR",None,3.8,"20","","https://www.amazon.de/dp/B0HD7LR1B7"),
 ("Rockjaw","UK","Amazon.de","Tuff Gum caffeine+taurine","Functional",60,None,33.90,"EUR",None,3.9,"58","€0.57/count shown","https://www.amazon.de/dp/B0BRYJ46PD"),
 ("Falim","TR","Amazon.de","Sugarless mastic gum, 100 pcs","Commodity",100,None,13.70,"EUR",None,4.2,"17","ordinary-hard Turkish gum","https://www.amazon.de/dp/B0CZWHGHQR"),
 ("Falim","TR","Amazon.de","Damla mastic, box of 100","Commodity",100,140,6.99,"EUR",None,3.8,"16","","https://www.amazon.de/dp/B0F6VLWKQ6"),
 ("Falim","TR","Amazon.de","3-flavour bundle, 300 pcs","Commodity",300,None,15.26,"EUR",None,None,None,"","https://www.amazon.de/dp/B0HJGX9QZQ"),
 ("Apollo","GR","Amazon.de","Mastic gum 25 g ('looksmaxxing')","Mastic",None,25,27.88,"EUR",None,4.7,"41","","https://www.amazon.de/dp/B0FMPD2TDW"),
 ("YouHerbIt","GR","Amazon.de","Chios mastic resin 25 g","Mastic",None,25,17.70,"EUR",None,4.3,"832","","https://www.amazon.de/dp/B01MZ1UZVP"),
 # --- Amazon.com (EUR shown to LT buyer; USD list in note)
 ("JAWCO","US","Amazon.com","Classic 1 pack","Hard",35,None,14.99,"USD",13.41,4.2,"497","Amazon US jawline-gum top 10, ~3K units/mo","https://www.amazon.com/dp/B0D1WZB87B"),
 ("GigaJaw","US","Amazon.com","15X hardness gum","Hard",30,None,18.99,"USD",16.99,4.2,"93","","https://www.amazon.com/dp/B0DC7CZWDF"),
 ("Mayena","US","Amazon.com","Jawline Max ultra-hard gum","Hard",40,None,16.99,"USD",15.20,4.0,"30","","https://www.amazon.com/dp/B0FDBMDDCP"),
 ("Gymgum","US","Amazon.com","Jawline Gum 40 ct","Hard",40,None,None,"USD",18.16,4.0,"694","","https://www.amazon.com/dp/B0GWFFPFV7"),
 ("Gymgum","US","Amazon.com","10x Hard Jawline Gum 10 ct (trial)","Hard",10,None,3.99,"USD",3.57,3.7,"157","trial size","https://www.amazon.com/dp/B0FH1SDH13"),
 ("Jawcraft","US","Amazon.com","Extra Strong Jaw Gum 45 pcs","Hard",45,None,18.99,"USD",16.99,None,None,"new listing","https://www.amazon.com/dp/B0H3C3PD6N"),
 ("Jawliner","DE","Amazon.com","Hard 40 pcs (US)","Hard",40,116,None,"USD",35.77,4.0,"85","priced above its EU site","https://www.amazon.com/dp/B0FKZ723HC"),
 ("Jawliner","DE","Amazon.com","Medium-hard strips 48 (130 g)","Medium",48,130,None,"USD",12.16,3.8,"188","'2x harder'","https://www.amazon.com/dp/B0D9BGMT6C"),
 # --- other US retail
 ("MASS GUM","US","Walmart","Tough gum 5×12 pcs","Medium",60,None,14.95,"USD",None,3.0,"1","out of stock","https://www.walmart.com/ip/14361318165"),
 ("Jawliner","DE","Urban Outfitters","Ultra Hard 100 g","Ultra",None,100,14.99,"USD",None,None,None,"sale from $28.00","https://www.urbanoutfitters.com/shop/jawliner-ultra-hard-chewing-gum"),
]
rows=[]
for b,c,ch,p,lv,pc,g,pr,cur,eur_o,rt,rv,note,url in R:
    eur = eur_o if eur_o is not None else (pr if cur=="EUR" else pr*(USD if cur=="USD" else GBP))
    rows.append(dict(brand=b,country=c,channel=ch,product=p,level=lv,pieces=pc,grams=g,price=pr,currency=cur,price_eur=round(eur,2),
        eur_per_piece=round(eur/pc,3) if pc else None,eur_per_100g=round(eur/g*100,2) if g else None,rating=rt,reviews=rv,note=note,url=url))
with open("hard_gum_prices_2026-11.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# ---- analysis
def tier(x):
    p=x["eur_per_piece"]
    if x["level"] in ("Mastic",) or p is None: return None
    return "Budget (<€0.20)" if p<0.20 else "Value (€0.20–0.40)" if p<0.40 else "Core (€0.40–0.60)" if p<0.60 else "Premium (≥€0.60)"
for x in rows: x["tier"]=tier(x)
jaw=[x for x in rows if x["level"] in ("Hard","Ultra","Functional") and x["eur_per_piece"]]
single=[x for x in jaw if x["pieces"] and x["pieces"]<=60 and x["pieces"]>=30]
print("Single packs (30–60 pcs, jaw gums):",len(single))
ps=sorted(x["eur_per_piece"] for x in single); pp=sorted(x["price_eur"] for x in single)
print(" per-piece min/median/max: %.2f / %.2f / %.2f" % (ps[0],st.median(ps),ps[-1]))
print(" pack price min/median/max: %.2f / %.2f / %.2f" % (pp[0],st.median(pp),pp[-1]))
for x in sorted(single,key=lambda x:x["eur_per_piece"]): print("  %-22s %-13s %-38s %5.2f €  %3d pcs  €%.2f/pc  %s"%(x["brand"],x["channel"],x["product"][:38],x["price_eur"],x["pieces"],x["eur_per_piece"],x["tier"]))
print("\nMulti-pack per-piece:")
for x in sorted([x for x in jaw if x["pieces"] and x["pieces"]>60],key=lambda x:x["eur_per_piece"]): print("  %-22s %-34s %6.2f € %4d pcs €%.3f/pc"%(x["brand"],x["product"][:34],x["price_eur"],x["pieces"],x["eur_per_piece"]))
print("\nBudget/commodity:")
for x in rows:
    if x["level"] in ("Commodity","Medium"): print("  %-14s %-34s €%.2f  %s pcs  €%s/pc"%(x["brand"],x["product"][:34],x["price_eur"],x["pieces"],x["eur_per_piece"]))
print("\nMastic per gram:")
for x in rows:
    if x["level"]=="Mastic": print("  %-10s %-30s €%.2f  %sg  €%.2f/g"%(x["brand"],x["product"][:30],x["price_eur"],x["grams"],x["price_eur"]/x["grams"]))
print("\nPer 100 g (where grams known):")
for x in sorted([x for x in rows if x["eur_per_100g"] and x["level"]!="Mastic"],key=lambda x:x["eur_per_100g"]): print("  %-14s %-34s €%.2f/100g"%(x["brand"],x["product"][:34],x["eur_per_100g"]))
