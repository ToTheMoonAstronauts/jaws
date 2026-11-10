/* Shared catalogue + cart drawer for the JAWZR draft store. Checkout is not connected yet. */
const CATALOG={
  hard:{name:"JAWZR Hard Gum",short:"Hard",grams:116,cls:"",
    flavours:{"Mint":"#7CC9EA","Mango":"#F4B23E","Watermelon":"#EE6A7A","Blueberry":"#7D5CD9"}},
  ultra:{name:"JAWZR Ultra Hard Gum",short:"Ultra Hard",grams:100,cls:"ultra",
    flavours:{"Mint":"#7CC9EA","Mango":"#F4B23E","Watermelon":"#EE6A7A","Blueberry":"#7D5CD9"}},
  /* separate product line, own page (energy.html): Hard hardness, mint only, 40 mg caffeine per piece */
  caffeine:{name:"JAWZR Hard + Caffeine",short:"Hard + Caffeine",grams:116,cls:"caffeine",caffeineMg:40,
    flavours:{"Mint":"#7CC9EA"}}
};
/* ---------- language: <html lang="lt|de"> on the translated pages (built by tools/i18n/build_lang.py) ---------- */
const LANG=(document.documentElement.lang||"en").slice(0,2);
/* display names for values that are also data keys (flavours, frequencies): data stays English */
const TR_LT={Mint:"Mėtų",Mango:"Mangų",Watermelon:"Arbūzų",Blueberry:"Mėlynių",Mixed:"Mišrūs",Pack:"Pakuotė","bought singly":"perkant atskirai","/ piece":"/ gab.",Save:"Sutaupyk","/ pack":"/ pak.",
  "4 weeks":"4 savaites","6 weeks":"6 savaites","2 months":"2 mėnesius","3 months":"3 mėnesius","4 months":"4 mėnesius",
  "5 months":"5 mėnesius","6 months":"6 mėnesius","8 months":"8 mėnesius","10 months":"10 mėnesių",
  Austria:"Austrija",Belgium:"Belgija",Bulgaria:"Bulgarija",Croatia:"Kroatija",Cyprus:"Kipras",Czechia:"Čekija",Denmark:"Danija",
  Estonia:"Estija",Finland:"Suomija",France:"Prancūzija",Germany:"Vokietija",Greece:"Graikija",Hungary:"Vengrija",Ireland:"Airija",
  Italy:"Italija",Latvia:"Latvija",Lithuania:"Lietuva",Luxembourg:"Liuksemburgas",Malta:"Malta",Netherlands:"Nyderlandai",
  Poland:"Lenkija",Portugal:"Portugalija",Romania:"Rumunija",Slovakia:"Slovakija",Slovenia:"Slovėnija",Spain:"Ispanija",Sweden:"Švedija"};
const TR_DE={Mint:"Minze",Mango:"Mango",Watermelon:"Wassermelone",Blueberry:"Blaubeere",Mixed:"Gemischt",Pack:"Packung","bought singly":"einzeln","/ piece":"/ Stück",Save:"Spare","/ pack":"/ Packung",
  "4 weeks":"4 Wochen","6 weeks":"6 Wochen","2 months":"2 Monate","3 months":"3 Monate","4 months":"4 Monate",
  "5 months":"5 Monate","6 months":"6 Monate","8 months":"8 Monate","10 months":"10 Monate",
  Austria:"Österreich",Belgium:"Belgien",Bulgaria:"Bulgarien",Croatia:"Kroatien",Cyprus:"Zypern",Czechia:"Tschechien",Denmark:"Dänemark",
  Estonia:"Estland",Finland:"Finnland",France:"Frankreich",Germany:"Deutschland",Greece:"Griechenland",Hungary:"Ungarn",Ireland:"Irland",
  Italy:"Italien",Latvia:"Lettland",Lithuania:"Litauen",Luxembourg:"Luxemburg",Malta:"Malta",Netherlands:"Niederlande",
  Poland:"Polen",Portugal:"Portugal",Romania:"Rumänien",Slovakia:"Slowakei",Slovenia:"Slowenien",Spain:"Spanien",Sweden:"Schweden"};
const TR={lt:TR_LT,de:TR_DE};
const tr=s=>(TR[LANG]&&TR[LANG][s])||s;
/* ---------- market & currency: ?market=us | ?market=eu (remembered in this browser) ---------- */
const MARKETS={
  eu:{cur:"EUR",sym:"€",free:49,ship:4.95,express:14.95,klarna:true,region:"EU",
      price:{1:{hard:17.95,ultra:23.95,caffeine:19.95},2:{hard:37.95,ultra:37.95},3:{hard:31.95,ultra:41.95,caffeine:35.95},6:{hard:53.95,ultra:71.95,caffeine:59.95}}},
  us:{cur:"USD",sym:"$",free:59,ship:9.95,express:24.95,klarna:false,region:"US",
      price:{1:{hard:19.95,ultra:26.95,caffeine:22.95},2:{hard:41.95,ultra:41.95},3:{hard:35.95,ultra:46.95,caffeine:39.95},6:{hard:59.95,ultra:79.95,caffeine:65.95}}}
};
/* ?market=useur: the US market (prices, shipping, rules) shown in euros */
MARKETS.useur={...MARKETS.us,cur:"EUR",sym:"€"};
const MARKET=(()=>{let m=new URLSearchParams(location.search).get("market");
  try{if(m&&MARKETS[m.toLowerCase()]){m=m.toLowerCase();localStorage.setItem("jawzr-market",m)}else m=localStorage.getItem("jawzr-market")}catch(e){}
  return LANG!=="en"?"eu":(MARKETS[m]?m:"eu")})();
const MK=MARKETS[MARKET];
const US=MK.region==="US";
const PACKS=[
  {id:1,label:"1 Pack · 40 pieces",sub:"1-month supply",price:MK.price[1]},
  {id:2,label:"Starter Duo · 80 pieces",sub:"1 Hard + 1 Ultra Hard · 2-month supply",price:MK.price[2],duo:true},
  {id:3,label:"3 Packs · 120 pieces",sub:"3-month supply, mix flavours",price:MK.price[3],tag:"Bestseller"},
  {id:6,label:"6 Packs · 240 pieces",sub:"6-month supply, free shipping",price:MK.price[6],tag:"Best results",tagCls:"green"}
];
const packPrice=(level,id)=>PACKS.find(p=>p.id===id).price[level];
/* what the same pieces cost as single packs (for "Save x%") */
const singlesPrice=(level,id)=>id===2?PACKS[0].price.hard+PACKS[0].price.ultra:PACKS[0].price[level]*id;
const SUB_OFF=0.15;
const subPrice=p=>Math.round(p*(1-SUB_OFF)*100)/100;
const FREE_SHIP=MK.free;
/* money in the current market's format: €17,95 or $19.95 */
const eur=n=>MK.cur==="USD"?"$"+n.toFixed(2):LANG!=="en"?n.toFixed(2).replace(".",",")+" €":"€"+n.toFixed(2).replace(".",",");
const eur0=n=>eur(n).replace(/[.,]00( €)?$/,"$1");
const $=id=>document.getElementById(id);
function inkOn(h){const n=parseInt(h.slice(1),16),r=n>>16,g=n>>8&255,b=n&255;return (0.299*r+0.587*g+0.114*b)>150?"#121614":"#fff"}
const slug=f=>f.toLowerCase().replace(/[^a-z]+/g,"-");
const MIXED="Mixed",MIXED_C="conic-gradient(#7CC9EA 0 33%,#F4B23E 0 66%,#EE6A7A 0)";
function packSrc(level,flavour){return flavour===MIXED?`images/products/bundle-${level}.webp`:`images/products/${level}-${slug(flavour)}.webp`}
function trioSrc(level,flavour){return flavour===MIXED?`images/products/bundle-${level}.webp`:`images/products/trio-${level}-${slug(flavour)}.webp`}
function pouchHTML(level,flavour,extra=""){
  const L=CATALOG[level];const c=L.flavours[flavour]||Object.values(L.flavours)[0];
  return `<div class="pouch ${L.cls} ${extra} ${flavour===MIXED?"mixed":""}"><img src="${packSrc(level,flavour)}" alt="JAWZR ${L.short} gum, ${flavour===MIXED?"mixed flavours (mint, mango, watermelon)":tr(flavour)+" flavour"}" loading="lazy"></div>`;
}

/* cart (kept in this browser only) */
let cart=[];
try{cart=JSON.parse(localStorage.getItem("jawzr-cart-v2-"+MARKET)||"[]")}catch(e){cart=[]}
function saveCart(){try{localStorage.setItem("jawzr-cart-v2-"+MARKET,JSON.stringify(cart))}catch(e){}}
function cartTotal(){return cart.reduce((s,l)=>s+l.price*l.qty,0)}
function cartCount(){return cart.reduce((s,l)=>s+l.qty,0)}
/* mix (optional): array of flavours, one per pack, e.g. ["Mint","Mint","Mango"] */
function mixLabel(mix,display){const o=Object.keys(CATALOG.hard.flavours),c={},d=f=>display?tr(f):f;mix.forEach(f=>c[f]=(c[f]||0)+1);return Object.entries(c).sort((x,y)=>o.indexOf(x[0])-o.indexOf(y[0])).map(([f,n])=>n>1?`${d(f)} ×${n}`:d(f)).join(", ")}
/* opts.duo: [hardFlavour, ultraFlavour] for the Starter Duo · opts.sub: {every:"4 months"} for a subscription */
function addToCart(level,flavour,packId,mix,opts={}){
  const P=PACKS.find(p=>p.id===packId);
  let name=flavour,duo=opts.duo||null,sub=opts.sub||null;
  if(duo){level="hard";flavour=duo[0];name=`Hard ${duo[0]} + Ultra Hard ${duo[1]}`;}
  else if(mix&&mix.length){const u=[...new Set(mix)];flavour=u.length===1?u[0]:MIXED;name=u.length===1?u[0]:mixLabel(mix);}
  const key=level+"|"+name+"|"+packId+"|"+(sub?sub.every:"once");
  const price=sub?subPrice(P.price[level]):P.price[level];
  const ex=cart.find(l=>l.key===key);
  if(ex)ex.qty++;else cart.push({key,level,flavour,name,mix:mix||null,duo,sub,pack:packId,label:P.label+(sub?` · Subscription, every ${tr(sub.every)} (−${SUB_OFF*100}%)`:""),price,qty:1});
  saveCart();renderCart();openCart();
}
function lineTitle(l){return l.duo?`Starter Duo · Hard ${tr(l.duo[0])} + Ultra Hard ${tr(l.duo[1])}`:`${CATALOG[l.level].short} · ${l.flavour===MIXED?"Mixed flavours":tr(l.name||l.flavour)}`}
function renderCart(){
  document.querySelectorAll("[data-cart-count]").forEach(e=>e.textContent=cartCount());
  const lines=$("cartLines");if(!lines)return;
  if(!cart.length){lines.innerHTML='<p class="empty">Your cart is empty.</p>'}
  else lines.innerHTML=cart.map((l,i)=>`<div class="line">${pouchHTML(l.level,l.flavour)}<div><b>${lineTitle(l)}</b><small>${l.label} · qty ${l.qty}</small><br><button class="rm" data-rm="${i}" type="button">Remove</button></div><b>${eur(l.price*l.qty)}</b></div>`).join("");
  const t=cartTotal();$("cartTotal").textContent=eur(t);
  const left=FREE_SHIP-t;
  $("shipMsg").textContent=LANG==="lt"?(t===0?`Nemokamas pristatymas ES nuo ${eur0(FREE_SHIP)}`:left>0?`Iki nemokamo pristatymo trūksta ${eur(left)}`:"Tau taikomas nemokamas pristatymas"):
    LANG==="de"?(t===0?`Kostenloser EU-Versand ab ${eur0(FREE_SHIP)}`:left>0?`Noch ${eur(left)} bis zum kostenlosen Versand`:"Dein Versand ist kostenlos"):
    t===0?`Free ${MK.region} shipping from ${eur0(FREE_SHIP)}`:left>0?`${eur(left)} away from free ${MK.region} shipping`:`You get free ${MK.region} shipping`;
  $("shipBar").style.width=Math.min(100,t/FREE_SHIP*100)+"%";
}
function openCart(){$("drawerBg").hidden=false;$("drawer").hidden=false}
function closeCart(){$("drawerBg").hidden=true;$("drawer").hidden=true}
let tt;function toast(m){const t=$("toast");if(!t)return;t.textContent=m;t.hidden=false;clearTimeout(tt);tt=setTimeout(()=>t.hidden=true,2800)}
document.addEventListener("click",e=>{
  if(e.target.closest("[data-open-cart]"))openCart();
  if(e.target.closest("[data-close-cart]"))closeCart();
  const rm=e.target.closest("[data-rm]");if(rm){cart.splice(+rm.dataset.rm,1);saveCart();renderCart();}
  if(e.target.closest("#checkoutBtn")){if(!cart.length){toast("Your cart is empty.");return}location.href="checkout.html"}
});
document.addEventListener("keydown",e=>{if(e.key==="Escape")closeCart()});
document.addEventListener("DOMContentLoaded",renderCart);

/* newsletter (demo) */
document.addEventListener("submit",e=>{
  const f=e.target.closest("[data-news]");if(!f)return;e.preventDefault();
  const email=(f.querySelector("input[type=email]")||{}).value||"";
  sbInsert("leads",{session_id:getSID(),source:"newsletter",email:email.trim().slice(0,254),marketing_consent:true,utm:UTM,lang:LANG,market:MARKET,geo:GEO||undefined});track("newsletter_signup");
  f.hidden=true;const ok=f.nextElementSibling;if(ok)ok.hidden=false;
});

/* Review cards. SAMPLE_REVIEWS are layout placeholders only: replace with real,
   order-linked reviews (e.g. from Judge.me / Loox) before launch. Never publish samples as real. */
const SAMPLE_REVIEWS=[
  {i:"A",name:"Customer name",lvl:"hard",fl:"Mint",pack:"3 Packs",text:"Sample review text. A real buyer's words about hardness, flavour and how the sessions feel will appear here."},
  {i:"B",name:"Customer name",lvl:"ultra",fl:"Blueberry",pack:"1 Pack",text:"Sample review text. Short, honest feedback from a verified order."},
  {i:"C",name:"Customer name",lvl:"hard",fl:"Mango",pack:"6 Packs",text:"Sample review text. Longer reviews wrap naturally and the cards stack in columns, like on the reference store."},
  {i:"D",name:"Customer name",lvl:"hard",fl:"Watermelon",pack:"3 Packs",text:"Sample review text."},
  {i:"E",name:"Customer name",lvl:"ultra",fl:"Watermelon",pack:"3 Packs",text:"Sample review text. Customers can attach a photo of the pack or of themselves."},
  {i:"F",name:"Customer name",lvl:"ultra",fl:"Mango",pack:"1 Pack",text:"Sample review text from a verified buyer."}
];
function renderReviews(el,list,n){
  el.innerHTML=list.slice(0,n).map((r,k)=>`<article class="rv"><span class="rv-sample">Sample</span>
    <div class="rv-photo"><div class="rv-tilt" style="--r:${k%2?4:-4}deg">${pouchHTML(r.lvl,r.fl)}</div></div>
    <div class="rv-body"><span class="rv-stars" aria-label="Rating">★★★★★</span><p>${r.text}</p>
    <div class="rv-meta"><span class="rv-av">${r.i}</span><span><b>${r.name}</b><small>${CATALOG[r.lvl].short} · ${r.fl} · ${r.pack}</small></span><span class="rv-ver">✓ Verified</span></div></div></article>`).join("");
}

/* ---------- Fake door tracking (Supabase, insert-only) ---------- */
const SB_URL="https://vzfwovxlzgrtghxlfkbj.supabase.co/rest/v1/";
const SB_KEY="sb_publishable_JP7_gwTXfMBITq2e2gHe8A_snjOsWTT";
/* Consent: analytics only after the visitor accepts (ePrivacy/GDPR). Cart storage is strictly necessary. */
/* EU: opt-in (banner). US: tracking on by default (no banner), off if the visitor opts out
   via "Your privacy choices" or their browser sends Global Privacy Control. */
const GPC=navigator.globalPrivacyControl===true;
function getConsent(){let v=null;try{v=localStorage.getItem("cutline-consent")}catch(e){}
  if(v)return v;return US?(GPC?"denied":"granted"):null}
function setConsent(v){try{localStorage.setItem("cutline-consent",v)}catch(e){}}
const TMP_SID="tmp-"+Math.random().toString(36).slice(2,12);
function getSID(){
  if(getConsent()!=="granted")return TMP_SID;
  try{let s=localStorage.getItem("cutline-sid");if(!s){s=(crypto.randomUUID?crypto.randomUUID():String(Date.now())+Math.random()).slice(0,36);localStorage.setItem("cutline-sid",s)}return s}catch(e){return TMP_SID}
}
const UTM=(()=>{const q=new URLSearchParams(location.search),u={};["utm_source","utm_medium","utm_campaign","utm_content","utm_term","fbclid"].forEach(k=>{if(q.get(k))u[k]=q.get(k).slice(0,200)});
  try{if(Object.keys(u).length&&getConsent()==="granted")sessionStorage.setItem("cutline-utm",JSON.stringify(u));return Object.keys(u).length?u:JSON.parse(sessionStorage.getItem("cutline-utm")||"{}")}catch(e){return u}})();
const LOCAL_PREVIEW=location.protocol==="file:";
/* Coarse visitor country (ISO-2) read same-origin from Cloudflare's trace endpoint, cached once per
   visitor. Used only for analytics (which market converts); never for pricing or access. */
let GEO=null;try{GEO=localStorage.getItem("jawzr-geo")||null}catch(e){}
function loadGeo(){
  if(GEO)return Promise.resolve(GEO);
  if(LOCAL_PREVIEW)return Promise.resolve(null);
  return fetch("/cdn-cgi/trace").then(r=>r.text()).then(t=>{const m=t.match(/\bloc=([A-Z]{2})\b/);if(m){GEO=m[1];try{localStorage.setItem("jawzr-geo",GEO)}catch(e){}}return GEO}).catch(()=>null);
}
function sbInsert(table,row){
  if(LOCAL_PREVIEW)return Promise.resolve(false);
  return fetch(SB_URL+table,{method:"POST",keepalive:true,headers:{"apikey":SB_KEY,"Authorization":"Bearer "+SB_KEY,"Content-Type":"application/json","Prefer":"return=minimal"},body:JSON.stringify(row)})
    .then(r=>r.ok).catch(()=>false);
}
function track(event,props={}){
  if(getConsent()!=="granted")return Promise.resolve(false);
  return sbInsert("events",{session_id:getSID(),event,page:location.pathname.slice(-200),props,referrer:(document.referrer||"").slice(0,500),utm:UTM,geo:GEO||undefined});
}
document.addEventListener("DOMContentLoaded",()=>loadGeo().then(()=>track("page_view")));
/* wrap addToCart so every add is tracked */
const _addToCart=addToCart;
addToCart=function(level,flavour,packId,mix,opts={}){
  try{const lv=opts.duo?"hard":level,base=packPrice(lv,packId),pr=opts.sub?subPrice(base):base,id=skuOf({level:lv,duo:opts.duo,pack:packId,sub:opts.sub});
    metaEvent("AddToCart",{value:pr,currency:MK.cur,content_type:"product",content_ids:[id],contents:[{id,quantity:1,item_price:pr}],num_items:1})}catch(e){}
  track("add_to_cart",{level,flavour,pack:packId,mix:mix?mix.join("|"):undefined,duo:opts.duo?opts.duo.join("|"):undefined,sub:opts.sub?opts.sub.every:undefined});return _addToCart(level,flavour,packId,mix,opts)};

/* cookie banner */
function cookieBanner(){
  let b=document.getElementById("cookieBar");
  if(!b){b=document.createElement("div");b.id="cookieBar";b.className="cookie-bar";b.setAttribute("role","dialog");b.setAttribute("aria-label","Cookie choice");
    b.innerHTML='<p>We use your browser\'s storage to keep your cart. With your OK, we also measure visits and shop steps, and use the Meta Pixel to measure our Facebook and Instagram ads. <a href="privacy.html">Privacy &amp; Cookies</a></p><div class="cookie-btns"><button type="button" class="btn ghost" data-consent="denied">Decline</button><button type="button" class="btn" data-consent="granted">Accept</button></div>';
    document.body.appendChild(b);}
  b.hidden=false;
}
document.addEventListener("click",e=>{
  const c=e.target.closest("[data-consent]");
  if(c){const v=c.dataset.consent,was=getConsent();setConsent(v);document.getElementById("cookieBar").hidden=true;
    if(v==="granted"&&was!=="granted"){track("consent",{value:v});track("page_view");metaBoot()}
    if(v==="denied"&&window.fbq)fbq("consent","revoke");}
  if(e.target.closest("[data-cookie-settings]")){e.preventDefault();cookieBanner()}
});
document.addEventListener("DOMContentLoaded",()=>{if(!getConsent())cookieBanner();
  if(US)document.querySelectorAll("[data-cookie-settings]").forEach(a=>a.textContent="Your privacy choices");});

/* ---------- 10% welcome popup (exit intent on desktop, timed/scroll on mobile; once per 14 days) ---------- */
(function(){
  const KEY="jawzr-pop",DAYS=14,CODE="WELCOME10";
  function seen(){try{const t=+localStorage.getItem(KEY)||0;return Date.now()-t<DAYS*864e5}catch(e){return true}}
  function mark(){try{localStorage.setItem(KEY,String(Date.now()))}catch(e){}}
  function blocked(){const c=document.getElementById("cookieBar");const d=document.getElementById("drawer");return (c&&!c.hidden)||(d&&!d.hidden)}
  let shown=false;
  function show(trigger){
    if(shown||seen()||blocked())return;shown=true;mark();
    const bg=document.createElement("div");bg.className="pop-bg";bg.setAttribute("role","dialog");bg.setAttribute("aria-modal","true");bg.setAttribute("aria-labelledby","popT");
    bg.innerHTML=`<div class="pop"><button class="x" type="button" aria-label="Close" data-pop-x>×</button>
      <div data-step="1"><p class="eyebrow">Before you go</p><h2 id="popT">Get 10% off</h2><p>Your first order of JAWZR hard gum. Enter your email and we'll show your code.</p>
      <form novalidate><input type="email" required placeholder="Your email" autocomplete="email" aria-label="Email"><button class="btn block big" type="submit">Get my 10%</button></form>
      <p class="fine">By signing up you agree to receive emails from JAWZR. Unsubscribe anytime. <a href="privacy.html">Privacy</a></p>
      <button class="no" type="button" data-pop-x>No thanks</button></div>
      <div data-step="2" hidden><p class="eyebrow">You're in</p><h2>Your code</h2><div class="code">${CODE}</div><p>Use it for 10% off your first order. We'll remind you by email too.</p><button class="btn block big" type="button" data-pop-x>Keep shopping</button></div></div>`;
    document.body.appendChild(bg);
    const close=()=>{bg.remove();document.removeEventListener("keydown",esc)};
    const esc=e=>{if(e.key==="Escape")close()};document.addEventListener("keydown",esc);
    bg.addEventListener("click",e=>{if(e.target===bg||e.target.closest("[data-pop-x]")){track("popup_close",{trigger});close()}});
    const f=bg.querySelector("form"),inp=f.querySelector("input");
    f.addEventListener("submit",e=>{e.preventDefault();const v=inp.value.trim();
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)){inp.setCustomValidity("Enter a valid email address.");inp.reportValidity();return}
      sbInsert("leads",{session_id:getSID(),source:"popup_10",email:v.slice(0,254),marketing_consent:true,utm:UTM,lang:LANG,market:MARKET,geo:GEO||undefined});track("popup_signup",{trigger});
      bg.querySelector('[data-step="1"]').hidden=true;bg.querySelector('[data-step="2"]').hidden=false;});
    inp.addEventListener("input",()=>inp.setCustomValidity(""));
    setTimeout(()=>inp.focus(),50);track("popup_show",{trigger});
  }
  document.addEventListener("DOMContentLoaded",()=>{
    if(!document.body.hasAttribute("data-popup")||seen())return;
    const start=Date.now(),fine=matchMedia("(pointer:fine)").matches;
    if(fine)document.addEventListener("mouseout",e=>{if(!e.relatedTarget&&e.clientY<=0&&Date.now()-start>8000)show("exit")});
    else{setTimeout(()=>show("timer"),35000);
      addEventListener("scroll",()=>{const h=document.documentElement;if(Date.now()-start>12000&&h.scrollTop/(h.scrollHeight-h.clientHeight)>0.6)show("scroll")},{passive:true});}
  });
})();

/* ---------- flavour icons + custom flavour picker (replaces native <select>) ---------- */
const FL_ICON={
  Mint:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19C4 11 9 4 20 3c1 10-5 16-15 16z" fill="#3FB984"/><path d="M5 19C9 14 12 10 17 6" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round" opacity=".8"/><path d="M9 14.5l-1.5-3M11.5 11.5 10.5 8M12 12.5l3 .5M9.5 15.5l3 .3" stroke="#fff" stroke-width=".9" stroke-linecap="round" opacity=".6"/></svg>',
  Mango:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7c4-4 12-2 13 5s-5 10-10 9S3 11 7 7z" fill="#F4B23E"/><path d="M8 9c2-2 6-2 8 0" stroke="#fff" stroke-width="1.3" fill="none" opacity=".55" stroke-linecap="round"/><path d="M12 5c1-2 3-3 5-3-1 2-3 3-5 3z" fill="#3FB984"/></svg>',
  Watermelon:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 9h20a10 10 0 0 1-20 0z" fill="#3FB984"/><path d="M4 9h16a8 8 0 0 1-16 0z" fill="#EE6A7A"/><circle cx="9" cy="12" r=".9" fill="#2b1d1d"/><circle cx="12" cy="14" r=".9" fill="#2b1d1d"/><circle cx="15" cy="12" r=".9" fill="#2b1d1d"/></svg>',
  Blueberry:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="14" r="6" fill="#5B43B8"/><circle cx="16" cy="11" r="5.5" fill="#7D5CD9"/><path d="M14.5 8.5l1.5 1 1.5-1-.5 1.8" stroke="#2f2366" stroke-width="1.1" fill="none" stroke-linecap="round"/><circle cx="7.5" cy="12.5" r="1.3" fill="#fff" opacity=".35"/></svg>'
};
const flIcon=f=>`<span class="fl-ic">${FL_ICON[f]||""}</span>`;
/* kind: "mix" | "duo" · i: slot index · val: current flavour · label: aria label */
/* list: option values (defaults to the flavours, with icons) · icons:false for plain text options */
function fselHTML(kind,i,val,label,list,icons=true){
  list=list||Object.keys(FL_ICON);const ic=v=>icons?flIcon(v):"";
  const opts=list.map(f=>`<li role="option" tabindex="-1" data-v="${f}" aria-selected="${f===val}">${ic(f)}<span>${tr(f)}</span>${f===val?'<span class="ck" aria-hidden="true">✓</span>':""}</li>`).join("");
  return `<div class="fsel" data-kind="${kind}" data-i="${i}"><button type="button" class="fsel-btn" aria-haspopup="listbox" aria-expanded="false" aria-label="${label}: ${tr(val)}">${ic(val)}<span class="nm">${tr(val)}</span><span class="cv" aria-hidden="true"><svg viewBox="0 0 12 12" width="12" height="12"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span></button><ul class="fsel-list" role="listbox" aria-label="${label}" hidden>${opts}</ul></div>`;
}
function fselClose(except){document.querySelectorAll(".fsel-list:not([hidden])").forEach(l=>{if(l.parentNode!==except){l.hidden=true;l.previousElementSibling.setAttribute("aria-expanded","false")}})}
function fselOpen(f,focusSel){fselClose(f);const l=f.querySelector(".fsel-list");l.hidden=false;f.querySelector(".fsel-btn").setAttribute("aria-expanded","true");
  const r=f.getBoundingClientRect();l.classList.toggle("up",innerHeight-r.bottom<220&&r.top>220);
  if(focusSel)(l.querySelector('[aria-selected="true"]')||l.firstElementChild).focus();}
function fselPick(f,v){fselClose();f.dispatchEvent(new CustomEvent("fsel-change",{bubbles:true,detail:{kind:f.dataset.kind,i:+f.dataset.i,value:v}}))}
document.addEventListener("click",e=>{
  const b=e.target.closest(".fsel-btn"),o=e.target.closest(".fsel-list [data-v]");
  if(o){fselPick(o.closest(".fsel"),o.dataset.v);return}
  if(b){const f=b.parentNode;f.querySelector(".fsel-list").hidden?fselOpen(f,false):fselClose();return}
  fselClose();
});
document.addEventListener("keydown",e=>{
  const f=e.target.closest&&e.target.closest(".fsel");if(!f)return;
  const l=f.querySelector(".fsel-list"),items=[...l.children],k=items.indexOf(document.activeElement);
  if(e.target.classList.contains("fsel-btn")&&["ArrowDown","ArrowUp"].includes(e.key)){e.preventDefault();fselOpen(f,true);return}
  if(l.hidden)return;
  if(e.key==="ArrowDown"){e.preventDefault();items[Math.min(items.length-1,k+1)].focus()}
  else if(e.key==="ArrowUp"){e.preventDefault();items[Math.max(0,k-1)].focus()}
  else if((e.key==="Enter"||e.key===" ")&&k>-1){e.preventDefault();fselPick(f,items[k].dataset.v)}
  else if(e.key==="Escape"||e.key==="Tab"){fselClose();f.querySelector(".fsel-btn").focus()}
});

/* ---------- desktop: random lifestyle photo on product-card hover ---------- */
(function(){
  if(!matchMedia("(hover:hover) and (pointer:fine)").matches)return;
  const IMGS=[1,2,3,4,5,6,7,8].map(n=>`images/mouseover/mo-${n}.webp`);let last=-1,warm=false;
  function pick(){let k;do{k=Math.floor(Math.random()*IMGS.length)}while(k===last&&IMGS.length>1);last=k;return IMGS[k]}
  document.addEventListener("mouseover",e=>{
    const host=e.target.closest(".card-visual, .range .pv");if(!host||host.contains(e.relatedTarget))return;
    if(!warm){warm=true;IMGS.forEach(s=>{const i=new Image();i.src=s})}
    let im=host.querySelector(":scope > .mo");
    if(!im){im=document.createElement("img");im.className="mo";im.alt="";im.setAttribute("aria-hidden","true");host.appendChild(im)}
    im.src=pick();requestAnimationFrame(()=>host.classList.add("mo-on"));
  });
  document.addEventListener("mouseout",e=>{const host=e.target.closest(".card-visual, .range .pv");if(host&&!host.contains(e.relatedTarget))host.classList.remove("mo-on")});
})();

/* ---------- mobile: size the hero photo so the CTA stays in the first screen ---------- */
(function(){
  function fit(){
    const hero=document.querySelector(".hero"),img=hero&&hero.querySelector(".hero-img"),cta=hero&&hero.querySelector(".cta-row");
    if(!img||!cta)return;
    if(innerWidth>760){img.style.height="";img.style.aspectRatio="";return}
    img.style.height="";const vh=(window.visualViewport?visualViewport.height:innerHeight);
    img.style.aspectRatio="auto";const full=img.offsetWidth;img.style.height=full+"px";
    const over=cta.getBoundingClientRect().bottom+window.scrollY+16-vh;
    if(over>0)img.style.height=Math.max(200,full-over)+"px";
  }
  addEventListener("load",fit);addEventListener("resize",fit);document.addEventListener("DOMContentLoaded",fit);
})();

/* ---------- US market: swap EU shipping/price wording in static page text ---------- */
const US_TEXT=[
 ["Standard shipping is €4,95 and free on orders from €49. DHL Express is €14,95 (1–3 business days).","Standard shipping (duties included) is $9.95 and free on orders from $59. DHL Express is $24.95 (3–5 business days)."],
 ["EU delivery usually takes 2–6 business days.","US delivery usually takes 7–12 business days."],
 ["We ship across the EU from Lithuania.","We ship to the US from the EU, with import duties included."],
 ["Free EU shipping on orders from €49.","Free US shipping on orders from $59."],
 ["Shipping is free on orders from €49.","Shipping is free on orders from $59."],
 ["Free EU shipping from €49","Free US shipping from $59"],
 ["free EU shipping from €49","free US shipping from $59"],
 ["Incl. VAT, plus shipping","Import duties included, plus shipping"],
 ["Incl. VAT.","Import duties included."],
 ["€0,22–0,60","$0.25–0.67"],
 ["from €17,95","from $19.95"],["from €23,95","from $26.95"],
 ["vs €53,85 bought singly","vs $59.85 bought singly"],["€31,95","$35.95"],["save 41%","save 40%"]
];
function applyMarketText(root){
  if(!US)return;
  const toLocal=t=>MK.cur==="USD"?t:t.replace(/\$(\d+)(?:\.(\d\d))?/g,(m,x,c)=>"€"+x+(c?","+c:""));
  const w=document.createTreeWalker(root||document.body,NodeFilter.SHOW_TEXT);let n;
  while((n=w.nextNode())){let t=n.nodeValue,o=t;if(!/[€]|EU/.test(t))continue;US_TEXT.forEach(([a,b])=>{if(t.includes(a))t=t.split(a).join(toLocal(b))});if(t!==o)n.nodeValue=t}
}
document.addEventListener("DOMContentLoaded",()=>{applyMarketText();document.documentElement.dataset.market=MARKET;
  /* footer market switch */
  const f=document.querySelector("footer .legal");if(f&&!document.getElementById("mkSwitch")){const d=document.createElement("p");d.id="mkSwitch";d.className="mk-switch";
    d.innerHTML=`Shipping to: <a href="?market=eu" ${MARKET==="eu"?'aria-current="true"':""}>EU · €</a> <a href="?market=us" ${MARKET==="us"?'aria-current="true"':""}>United States · $</a>`;f.parentNode.insertBefore(d,f)}});

/* ---------- payment brand icons (CC0: gilbarbara/logos, simple-icons) ---------- */
const PAY_ICON={"visa": "<svg viewBox=\"0 0 256 83\" aria-hidden=\"true\"><defs><linearGradient id=\"SVGSdd43daQ\" x1=\"45.974%\" x2=\"54.877%\" y1=\"-2.006%\" y2=\"100%\"><stop offset=\"0%\" stop-color=\"#222357\"/><stop offset=\"100%\" stop-color=\"#254aa5\"/></linearGradient></defs><path fill=\"url(#SVGSdd43daQ)\" d=\"M132.397 56.24c-.146-11.516 10.263-17.942 18.104-21.763c8.056-3.92 10.762-6.434 10.73-9.94c-.06-5.365-6.426-7.733-12.383-7.825c-10.393-.161-16.436 2.806-21.24 5.05l-3.744-17.519c4.82-2.221 13.745-4.158 23-4.243c21.725 0 35.938 10.724 36.015 27.351c.085 21.102-29.188 22.27-28.988 31.702c.069 2.86 2.798 5.912 8.778 6.688c2.96.392 11.131.692 20.395-3.574l3.636 16.95c-4.982 1.814-11.385 3.551-19.357 3.551c-20.448 0-34.83-10.87-34.946-26.428m89.241 24.968c-3.967 0-7.31-2.314-8.802-5.865L181.803 1.245h21.709l4.32 11.939h26.528l2.506-11.939H256l-16.697 79.963zm3.037-21.601l6.265-30.027h-17.158zm-118.599 21.6L88.964 1.246h20.687l17.104 79.963zm-30.603 0L53.941 26.782l-8.71 46.277c-1.022 5.166-5.058 8.149-9.54 8.149H.493L0 78.886c7.226-1.568 15.436-4.097 20.41-6.803c3.044-1.653 3.912-3.098 4.912-7.026L41.819 1.245H63.68l33.516 79.963z\" transform=\"matrix(1 0 0 -1 0 82.668)\"/></svg>", "mastercard": "<svg viewBox=\"0 0 256 199\" aria-hidden=\"true\"><path d=\"M46.54 198.011V184.84c0-5.05-3.074-8.342-8.343-8.342c-2.634 0-5.488.878-7.464 3.732c-1.536-2.415-3.731-3.732-7.024-3.732c-2.196 0-4.39.658-6.147 3.073v-2.634h-4.61v21.074h4.61v-11.635c0-3.731 1.976-5.488 5.05-5.488c3.072 0 4.61 1.976 4.61 5.488v11.635h4.61v-11.635c0-3.731 2.194-5.488 5.048-5.488c3.074 0 4.61 1.976 4.61 5.488v11.635zm68.271-21.074h-7.463v-6.366h-4.61v6.366h-4.171v4.17h4.17v9.66c0 4.83 1.976 7.683 7.245 7.683c1.976 0 4.17-.658 5.708-1.536l-1.318-3.952c-1.317.878-2.853 1.098-3.951 1.098c-2.195 0-3.073-1.317-3.073-3.513v-9.44h7.463zm39.076-.44c-2.634 0-4.39 1.318-5.488 3.074v-2.634h-4.61v21.074h4.61v-11.854c0-3.512 1.536-5.488 4.39-5.488c.878 0 1.976.22 2.854.439l1.317-4.39c-.878-.22-2.195-.22-3.073-.22m-59.052 2.196c-2.196-1.537-5.269-2.195-8.562-2.195c-5.268 0-8.78 2.634-8.78 6.805c0 3.513 2.634 5.488 7.244 6.147l2.195.22c2.415.438 3.732 1.097 3.732 2.195c0 1.536-1.756 2.634-4.83 2.634s-5.488-1.098-7.025-2.195l-2.195 3.512c2.415 1.756 5.708 2.634 9 2.634c6.147 0 9.66-2.853 9.66-6.805c0-3.732-2.854-5.708-7.245-6.366l-2.195-.22c-1.976-.22-3.512-.658-3.512-1.975c0-1.537 1.536-2.415 3.951-2.415c2.635 0 5.269 1.097 6.586 1.756zm122.495-2.195c-2.635 0-4.391 1.317-5.489 3.073v-2.634h-4.61v21.074h4.61v-11.854c0-3.512 1.537-5.488 4.39-5.488c.879 0 1.977.22 2.855.439l1.317-4.39c-.878-.22-2.195-.22-3.073-.22m-58.833 10.976c0 6.366 4.39 10.976 11.196 10.976c3.073 0 5.268-.658 7.463-2.414l-2.195-3.732c-1.756 1.317-3.512 1.975-5.488 1.975c-3.732 0-6.366-2.634-6.366-6.805c0-3.951 2.634-6.586 6.366-6.805c1.976 0 3.732.658 5.488 1.976l2.195-3.732c-2.195-1.757-4.39-2.415-7.463-2.415c-6.806 0-11.196 4.61-11.196 10.976m42.588 0v-10.537h-4.61v2.634c-1.537-1.975-3.732-3.073-6.586-3.073c-5.927 0-10.537 4.61-10.537 10.976s4.61 10.976 10.537 10.976c3.073 0 5.269-1.097 6.586-3.073v2.634h4.61zm-16.904 0c0-3.732 2.415-6.805 6.366-6.805c3.732 0 6.367 2.854 6.367 6.805c0 3.732-2.635 6.805-6.367 6.805c-3.951-.22-6.366-3.073-6.366-6.805m-55.1-10.976c-6.147 0-10.538 4.39-10.538 10.976s4.39 10.976 10.757 10.976c3.073 0 6.147-.878 8.562-2.853l-2.196-3.293c-1.756 1.317-3.951 2.195-6.146 2.195c-2.854 0-5.708-1.317-6.367-5.05h15.587v-1.755c.22-6.806-3.732-11.196-9.66-11.196m0 3.951c2.853 0 4.83 1.757 5.268 5.05h-10.976c.439-2.854 2.415-5.05 5.708-5.05m114.372 7.025v-18.879h-4.61v10.976c-1.537-1.975-3.732-3.073-6.586-3.073c-5.927 0-10.537 4.61-10.537 10.976s4.61 10.976 10.537 10.976c3.074 0 5.269-1.097 6.586-3.073v2.634h4.61zm-16.903 0c0-3.732 2.414-6.805 6.366-6.805c3.732 0 6.366 2.854 6.366 6.805c0 3.732-2.634 6.805-6.366 6.805c-3.952-.22-6.366-3.073-6.366-6.805m-154.107 0v-10.537h-4.61v2.634c-1.537-1.975-3.732-3.073-6.586-3.073c-5.927 0-10.537 4.61-10.537 10.976s4.61 10.976 10.537 10.976c3.074 0 5.269-1.097 6.586-3.073v2.634h4.61zm-17.123 0c0-3.732 2.415-6.805 6.366-6.805c3.732 0 6.367 2.854 6.367 6.805c0 3.732-2.635 6.805-6.367 6.805c-3.951-.22-6.366-3.073-6.366-6.805\"/><path fill=\"#ff5f00\" d=\"M93.298 16.903h69.15v124.251h-69.15z\"/><path fill=\"#eb001b\" d=\"M97.689 79.029c0-25.245 11.854-47.637 30.074-62.126C114.373 6.366 97.47 0 79.03 0C35.343 0 0 35.343 0 79.029s35.343 79.029 79.029 79.029c18.44 0 35.343-6.366 48.734-16.904c-18.22-14.269-30.074-36.88-30.074-62.125\"/><path fill=\"#f79e1b\" d=\"M255.746 79.029c0 43.685-35.343 79.029-79.029 79.029c-18.44 0-35.343-6.366-48.734-16.904c18.44-14.488 30.075-36.88 30.075-62.125s-11.855-47.637-30.075-62.126C141.373 6.366 158.277 0 176.717 0c43.686 0 79.03 35.563 79.03 79.029\"/></svg>", "amex": "<svg viewBox=\"0 0 256 256\" aria-hidden=\"true\"><path fill=\"#006fcf\" d=\"M256 138.548V0H0v256h256v-74.69c-.57 0 0-42.762 0-42.762\"/><path fill=\"#fff\" d=\"M224.641 124.294h19.386V79.252H222.93v6.271l-3.991-6.271h-18.245v7.982l-3.421-7.982h-33.64c-1.14 0-2.28.57-3.42.57s-1.71.57-2.851 1.14c-1.14.57-1.71.57-2.85 1.14v-2.85H58.155l-2.85 7.412l-2.852-7.412H29.648v7.982l-3.42-7.982H7.981L0 98.637v25.657h13.114l2.28-6.272h4.561l2.281 6.272h100.348v-5.702l3.99 5.702h27.938v-3.42c.57.57 1.71.57 2.28 1.14c.571.57 1.711.57 2.281 1.14c1.14.57 2.281.57 3.421.57h20.526l2.28-6.272h4.562l2.28 6.272h27.938v-5.702zM256 181.31v-42.192H99.207l-3.991 5.702l-3.991-5.702H45.612v45.042h45.613l3.991-5.701l3.991 5.701h28.508v-9.692h-1.14q5.986 0 10.262-1.71v11.973h20.526v-5.702l3.991 5.702h84.953c3.421-1.14 6.842-1.711 9.693-3.421\"/><path fill=\"#006fcf\" d=\"M246.307 170.477h-15.394v6.271h14.824c6.272 0 10.263-3.99 10.263-9.692s-3.42-8.553-9.122-8.553h-6.842c-1.71 0-2.851-1.14-2.851-2.85s1.14-2.851 2.85-2.851h13.114L256 146.53h-15.394c-6.272 0-10.263 3.991-10.263 9.123c0 5.701 3.42 8.552 9.122 8.552h6.842c1.71 0 2.851 1.14 2.851 2.85c.57 2.281-.57 3.422-2.85 3.422m-27.937 0h-15.394v6.271H217.8c6.271 0 10.262-3.99 10.262-9.692s-3.42-8.553-9.122-8.553h-6.842c-1.71 0-2.85-1.14-2.85-2.85s1.14-2.851 2.85-2.851h13.114l2.85-6.272h-15.394c-6.272 0-10.263 3.991-10.263 9.123c0 5.701 3.421 8.552 9.123 8.552h6.842c1.71 0 2.85 1.14 2.85 2.85c.57 2.281-1.14 3.422-2.85 3.422m-19.956-18.245v-6.272h-23.946v30.218h23.946v-6.272H181.31v-6.271h16.534v-6.272H181.31v-5.702h17.104zm-38.77 0c2.85 0 3.99 1.71 3.99 3.42c0 1.711-1.14 3.421-3.99 3.421h-8.553v-7.412zm-8.553 13.113h3.421l9.123 10.833h8.552l-10.263-11.403c5.132-1.14 7.982-4.561 7.982-9.122c0-5.702-3.99-9.693-10.262-9.693h-15.965v30.218h6.842zm-18.245-9.122c0 2.28-1.14 3.99-3.99 3.99h-9.123v-7.981h8.552c2.85 0 4.561 1.71 4.561 3.99m-19.955-10.263v30.218h6.842v-10.263h9.122c6.272 0 10.833-3.99 10.833-10.262c0-5.702-3.99-10.263-10.263-10.263zm-10.263 30.218h8.552l-11.973-15.394l11.973-14.824h-8.552l-7.412 9.693l-7.412-9.693h-8.552l11.973 14.824l-11.973 14.824h8.552l7.412-9.693zm-25.657-23.946v-6.272H53.024v30.218h23.947v-6.272H59.866v-6.271h16.535v-6.272H59.866v-5.702h17.105zm138.548-53.595l11.973 18.245h8.553V86.664h-6.842v19.955l-1.71-2.85l-10.834-17.105h-9.122v30.218h6.842V96.356zm-29.648-.57l2.28-6.272l2.281 6.272l2.85 6.842H183.02zm11.973 18.815h7.412l-13.113-30.218h-9.123l-13.114 30.218h7.412l2.851-6.272h14.824zm-31.929 0l2.851-6.272h-1.71c-5.132 0-7.983-3.42-7.983-8.552v-.57c0-5.132 2.851-8.553 7.983-8.553h7.412v-6.271h-7.982c-9.123 0-14.254 6.271-14.254 14.824v.57c0 9.122 5.131 14.824 13.683 14.824m-25.657 0h6.842V87.234h-6.842zm-14.824-23.947c2.851 0 3.991 1.71 3.991 3.421s-1.14 3.421-3.99 3.421h-8.553v-7.412zm-8.552 13.114h3.42l9.123 10.833h8.553l-10.263-11.403c5.131-1.14 7.982-4.561 7.982-9.123c0-5.701-3.991-9.692-10.263-9.692H109.47v30.218h6.842zm-12.543-13.114v-6.271H80.392v30.218h23.947v-6.272H87.234v-6.271h16.534v-6.272H87.234v-5.702h17.105zm-51.885 23.947h6.272l8.552-24.517v24.517h6.842V86.664H62.717l-6.842 20.525l-6.842-20.525H37.63v30.218h6.842V92.365zm-37.06-18.815l2.28-6.272l2.281 6.272l2.851 6.842H12.543zm11.973 18.815h7.413L21.666 86.664h-8.552L0 116.882h7.412l2.85-6.272h14.825z\"/></svg>", "paypal": "<svg viewBox=\"0 0 256 302\" aria-hidden=\"true\"><path fill=\"#27346a\" d=\"M217.168 23.507C203.234 7.625 178.046.816 145.823.816h-93.52A13.39 13.39 0 0 0 39.076 12.11L.136 259.077c-.774 4.87 2.997 9.28 7.933 9.28h57.736l14.5-91.971l-.45 2.88c1.033-6.501 6.593-11.296 13.177-11.296h27.436c53.898 0 96.101-21.892 108.429-85.221c.366-1.873.683-3.696.957-5.477q-2.334-1.236 0 0c3.671-23.407-.025-39.34-12.686-53.765\"/><path fill=\"#27346a\" d=\"M102.397 68.84a11.7 11.7 0 0 1 5.053-1.14h73.318c8.682 0 16.78.565 24.18 1.756a102 102 0 0 1 6.177 1.182a90 90 0 0 1 8.59 2.347c3.638 1.215 7.026 2.63 10.14 4.287c3.67-23.416-.026-39.34-12.687-53.765C203.226 7.625 178.046.816 145.823.816H52.295C45.71.816 40.108 5.61 39.076 12.11L.136 259.068c-.774 4.878 2.997 9.282 7.925 9.282h57.744L95.888 77.58a11.72 11.72 0 0 1 6.509-8.74\"/><path fill=\"#2790c3\" d=\"M228.897 82.749c-12.328 63.32-54.53 85.221-108.429 85.221H93.024c-6.584 0-12.145 4.795-13.168 11.296L61.817 293.621c-.674 4.262 2.622 8.124 6.934 8.124h48.67a11.71 11.71 0 0 0 11.563-9.88l.474-2.48l9.173-58.136l.591-3.213a11.71 11.71 0 0 1 11.562-9.88h7.284c47.147 0 84.064-19.154 94.852-74.55c4.503-23.15 2.173-42.478-9.739-56.054c-3.613-4.112-8.1-7.508-13.327-10.28c-.283 1.79-.59 3.604-.957 5.477\"/><path fill=\"#1f264f\" d=\"M216.952 72.128a90 90 0 0 0-5.818-1.49a110 110 0 0 0-6.177-1.174c-7.408-1.199-15.5-1.765-24.19-1.765h-73.309a11.6 11.6 0 0 0-5.053 1.149a11.68 11.68 0 0 0-6.51 8.74l-15.582 98.798l-.45 2.88c1.025-6.501 6.585-11.296 13.17-11.296h27.444c53.898 0 96.1-21.892 108.428-85.221c.367-1.873.675-3.688.958-5.477q-4.682-2.47-10.14-4.279a83 83 0 0 0-2.77-.865\"/></svg>", "apple-pay": "<svg viewBox=\"0 0 512 211\" aria-hidden=\"true\"><path d=\"M93.552 27.103c-6 7.1-15.602 12.702-25.203 11.901c-1.2-9.6 3.5-19.802 9.001-26.103C83.35 5.601 93.852.4 102.353 0c1 10.001-2.9 19.802-8.8 27.103m8.701 13.802c-13.902-.8-25.803 7.9-32.404 7.9c-6.7 0-16.802-7.5-27.803-7.3c-14.301.2-27.603 8.3-34.904 21.202c-15.002 25.803-3.9 64.008 10.601 85.01c7.101 10.401 15.602 21.802 26.803 21.402c10.602-.4 14.802-6.9 27.604-6.9c12.901 0 16.602 6.9 27.803 6.7c11.601-.2 18.902-10.4 26.003-20.802c8.1-11.801 11.401-23.303 11.601-23.903c-.2-.2-22.402-8.7-22.602-34.304c-.2-21.402 17.502-31.603 18.302-32.203c-10.002-14.802-25.603-16.402-31.004-16.802m80.31-29.004V167.82h24.202v-53.306h33.504c30.603 0 52.106-21.002 52.106-51.406c0-30.403-21.103-51.206-51.306-51.206zm24.202 20.403h27.903c21.003 0 33.004 11.201 33.004 30.903s-12.001 31.004-33.104 31.004h-27.803zM336.58 169.019c15.202 0 29.303-7.7 35.704-19.902h.5v18.702h22.403V90.21c0-22.502-18.002-37.004-45.706-37.004c-25.703 0-44.705 14.702-45.405 34.904h21.803c1.8-9.601 10.7-15.902 22.902-15.902c14.802 0 23.103 6.901 23.103 19.603v8.6l-30.204 1.8c-28.103 1.7-43.304 13.202-43.304 33.205c0 20.202 15.701 33.603 38.204 33.603m6.5-18.502c-12.9 0-21.102-6.2-21.102-15.702c0-9.8 7.901-15.501 23.003-16.401l26.903-1.7v8.8c0 14.602-12.401 25.003-28.803 25.003m82.01 59.707c23.603 0 34.704-9 44.405-36.304L512 54.706h-24.603l-28.503 92.11h-.5l-28.503-92.11h-25.303l41.004 113.513l-2.2 6.901c-3.7 11.701-9.701 16.202-20.402 16.202c-1.9 0-5.6-.2-7.101-.4v18.702c1.4.4 7.4.6 9.201.6\"/></svg>", "google-pay": "<svg viewBox=\"0 0 512 204\" aria-hidden=\"true\"><path fill=\"#5f6368\" d=\"M362.927 55.057c14.075 0 24.952 3.839 33.27 11.517c8.317 7.677 12.155 17.914 12.155 30.71v61.42h-17.914V144.63h-.64c-7.677 11.517-18.554 17.275-31.35 17.275c-10.877 0-20.474-3.2-28.151-9.597c-7.038-6.398-11.517-15.355-11.517-24.952q0-15.356 11.517-24.953c7.677-6.398 18.554-8.957 31.35-8.957c11.516 0 20.474 1.92 27.511 6.398v-4.478c0-5.972-2.229-11.943-6.688-15.834l-.99-.801c-5.118-4.479-11.516-7.038-18.553-7.038q-16.315 0-24.953 13.436L321.34 74.89c10.236-13.436 23.672-19.834 41.587-19.834M272.715 11.55c11.48 0 22.39 3.995 31.113 11.445l1.517 1.35c8.957 7.678 13.435 19.195 13.435 31.351s-4.478 23.033-13.435 31.35s-19.834 12.796-32.63 12.796l-30.71-.64v59.502H222.81V11.55zm92.77 97.25q-11.516 0-19.193 5.758q-7.678 4.798-7.678 13.435c0 5.119 2.56 9.597 6.398 12.157c4.479 3.199 9.597 5.118 14.716 5.118c7.165 0 14.331-2.787 19.936-7.84l1.177-1.117c6.398-5.758 9.597-12.796 9.597-20.474c-5.758-4.478-14.076-7.038-24.952-7.038m-91.49-79.336h-31.99V80.65h31.99c7.037 0 14.075-2.559 18.554-7.677c10.236-9.597 10.236-25.592.64-35.19l-.64-.64c-5.119-5.118-11.517-8.317-18.555-7.677M512 58.256l-63.34 145.235h-19.194l23.672-50.544l-41.587-94.051h20.474l30.07 72.297h.64l29.431-72.297H512z\"/><path fill=\"#4285f4\" d=\"M165.868 86.407c0-5.758-.64-11.516-1.28-17.274H84.615v32.63h45.425c-1.919 10.236-7.677 19.833-16.634 25.592v21.113h27.511c15.995-14.715 24.952-36.469 24.952-62.06\"/><path fill=\"#34a853\" d=\"M84.614 168.942c23.032 0 42.226-7.678 56.302-20.474l-27.511-21.113c-7.678 5.118-17.275 8.317-28.791 8.317c-21.754 0-40.948-14.715-47.346-35.189H9.118v21.753c14.715 28.791 43.506 46.706 75.496 46.706\"/><path fill=\"#fbbc04\" d=\"M37.268 100.483c-3.838-10.237-3.838-21.753 0-32.63V46.1H9.118c-12.157 23.673-12.157 51.824 0 76.136z\"/><path fill=\"#ea4335\" d=\"M84.614 33.304c12.156 0 23.672 4.479 32.63 12.796l24.312-24.312C126.2 7.712 105.727-.605 85.253.034c-31.99 0-61.42 17.915-75.496 46.706l28.151 21.753c5.758-20.474 24.952-35.189 46.706-35.189\"/></svg>", "maestro": "<svg viewBox=\"0 0 256 199\" aria-hidden=\"true\"><path fill=\"#6c6bbd\" d=\"M162.611 141.315H93.389V16.913h69.222z\"/><path fill=\"#d32011\" d=\"M97.783 79.117c0-25.236 11.815-47.715 30.215-62.201C114.543 6.323 97.56 0 79.106 0C35.416 0 0 35.421 0 79.117c0 43.695 35.416 79.116 79.106 79.116c18.455 0 35.437-6.323 48.892-16.916c-18.4-14.486-30.215-36.965-30.215-62.2\"/><path fill=\"#0099df\" d=\"M256 79.117c0 43.695-35.416 79.116-79.106 79.116c-18.455 0-35.437-6.323-48.897-16.916c18.405-14.486 30.22-36.965 30.22-62.2c0-25.236-11.815-47.715-30.22-62.201C141.457 6.323 158.44 0 176.894 0C220.584 0 256 35.421 256 79.117\"/><path fill=\"#110f0d\" d=\"M186.033 176.466c.92 0 2.243.176 3.254.573l-1.408 4.306c-.966-.397-1.932-.528-2.857-.528c-2.988 0-4.482 1.931-4.482 5.402v11.78h-4.572v-21.005h4.527v2.55c1.187-1.846 2.902-3.078 5.538-3.078m-16.891 4.703h-7.47v9.491c0 2.108.745 3.516 3.034 3.516c1.187 0 2.68-.397 4.039-1.187l1.317 3.909c-1.448 1.01-3.732 1.63-5.709 1.63c-5.407 0-7.293-2.903-7.293-7.782v-9.577h-4.265v-4.175h4.265v-6.373h4.612v6.373h7.47zm-58.494 4.482c.488-3.033 2.33-5.1 5.584-5.1c2.942 0 4.833 1.845 5.316 5.1zm15.649 1.846c-.046-6.55-4.09-11.031-9.98-11.031c-6.151 0-10.457 4.482-10.457 11.03c0 6.675 4.482 11.026 10.769 11.026c3.164 0 6.061-.79 8.611-2.942l-2.243-3.385c-1.755 1.408-3.999 2.198-6.106 2.198c-2.943 0-5.624-1.363-6.283-5.14h15.598c.045-.574.09-1.143.09-1.756m20.08-5.141c-1.273-.795-3.864-1.806-6.545-1.806c-2.505 0-3.999.926-3.999 2.465c0 1.403 1.58 1.8 3.557 2.062l2.153.307c4.572.664 7.338 2.596 7.338 6.288c0 3.998-3.516 6.855-9.577 6.855c-3.43 0-6.594-.88-9.1-2.726l2.154-3.561c1.539 1.187 3.828 2.198 6.991 2.198c3.119 0 4.789-.92 4.789-2.55c0-1.182-1.187-1.846-3.692-2.193l-2.153-.307c-4.703-.664-7.253-2.772-7.253-6.197c0-4.175 3.43-6.725 8.747-6.725c3.34 0 6.373.75 8.566 2.198zm56.36-1.55c-.94 0-1.81.167-2.62.494a6.3 6.3 0 0 0-2.093 1.388a6.4 6.4 0 0 0-1.388 2.138q-.504 1.246-.503 2.741c0 1.001.166 1.911.503 2.741q.506 1.247 1.388 2.138a6.3 6.3 0 0 0 2.093 1.388c.81.332 1.68.493 2.62.493s1.816-.16 2.62-.493a6.3 6.3 0 0 0 2.103-1.388c.599-.593 1.062-1.308 1.404-2.138c.337-.83.503-1.74.503-2.741q.001-1.495-.503-2.741c-.342-.83-.805-1.544-1.404-2.138a6.3 6.3 0 0 0-2.102-1.388a6.9 6.9 0 0 0-2.62-.493m0-4.34q2.445-.001 4.527.85q2.083.846 3.602 2.334a10.7 10.7 0 0 1 2.379 3.51q.86 2.031.86 4.407t-.86 4.406a10.7 10.7 0 0 1-2.38 3.516c-1.01.991-2.213 1.766-3.6 2.334q-2.084.845-4.528.845q-2.445 0-4.527-.845c-1.388-.568-2.58-1.343-3.586-2.334a10.8 10.8 0 0 1-2.37-3.516q-.86-2.03-.86-4.406t.86-4.406a10.8 10.8 0 0 1 2.37-3.511a10.9 10.9 0 0 1 3.586-2.334q2.082-.851 4.527-.85M83.95 187.496c0-3.691 2.42-6.724 6.373-6.724c3.778 0 6.328 2.902 6.328 6.725s-2.55 6.72-6.328 6.72c-3.953 0-6.373-3.028-6.373-6.72m17.007 0v-10.502h-4.568v2.55c-1.453-1.891-3.646-3.078-6.634-3.078c-5.89 0-10.503 4.612-10.503 11.03c0 6.414 4.613 11.031 10.503 11.031c2.988 0 5.18-1.187 6.634-3.078V198h4.568zM75.207 198v-13.183c0-4.965-3.164-8.305-8.259-8.35c-2.681-.045-5.453.79-7.384 3.737c-1.449-2.329-3.737-3.737-6.946-3.737c-2.239 0-4.437.659-6.152 3.118v-2.59h-4.567V198h4.612v-11.644c0-3.647 2.022-5.583 5.14-5.583c3.034 0 4.573 1.976 4.573 5.538V198h4.613v-11.645c0-3.647 2.112-5.583 5.14-5.583c3.124 0 4.618 1.976 4.618 5.538V198z\"/></svg>", "klarna": "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path fill=\"#0b051d\" d=\"M4.592 2v20H0V2zm11.46 0c0 4.194-1.583 8.105-4.415 11.068l-.278.283L17.702 22h-5.668l-6.893-9.4l1.779-1.332c2.858-2.14 4.535-5.378 4.637-8.924L11.562 2zM21.5 17a2.5 2.5 0 1 1 0 5a2.5 2.5 0 0 1 0-5\"/></svg>"};
const pic=k=>`<i class="${k==="klarna"?"kl":""}" title="${k}">${PAY_ICON[k]}</i>`;
/* product pages: icon row under the buy button, Klarna only where it's offered */
document.addEventListener("DOMContentLoaded",()=>{document.querySelectorAll(".pay").forEach(el=>{
  el.classList.add("pic");el.innerHTML=["visa","mastercard","amex","paypal","apple-pay","google-pay",...(MK.klarna?["klarna"]:[])].map(pic).join("");})});

/* ---------- Meta Pixel + Conversions API (only after the visitor clicks Accept) ----------
   Browser: PageView, AddToCart, InitiateCheckout, Lead, Purchase.
   Server (capi edge function): Lead + Purchase with the same event_id, so Meta keeps one of each pair. */
const META_PIXEL="28889931507316454";
const CAPI_URL="https://vzfwovxlzgrtghxlfkbj.supabase.co/functions/v1/capi";
const uuid=()=>(crypto.randomUUID?crypto.randomUUID():Date.now().toString(36)+Math.random().toString(36).slice(2));
/* ad click id: fbclid in the landing URL, kept with the time we first saw it (milliseconds) */
const FBCLID=(()=>{const q=new URLSearchParams(location.search).get("fbclid");
  if(q){const v={id:q.slice(0,250),ts:Date.now(),landing:(location.origin+location.pathname).slice(0,500)};try{sessionStorage.setItem("jawzr-fbclid",JSON.stringify(v))}catch(e){}return v}
  try{return JSON.parse(sessionStorage.getItem("jawzr-fbclid")||"null")}catch(e){return null}})();
function persistClick(){if(FBCLID&&getConsent()==="granted"){try{localStorage.setItem("jawzr-fbclid",JSON.stringify(FBCLID))}catch(e){}}}
function clickInfo(){let c=FBCLID;if(!c){try{c=JSON.parse(localStorage.getItem("jawzr-fbclid")||"null")}catch(e){}}return c}
const cookie=n=>{const m=document.cookie.match(new RegExp("(?:^|; )"+n+"=([^;]*)"));return m?decodeURIComponent(m[1]):undefined};
function fbc(){const c=cookie("_fbc");if(c)return c;const k=clickInfo();return k?`fb.1.${k.ts}.${k.id}`:undefined}
const fbp=()=>cookie("_fbp");
function metaAttribution(){const k=clickInfo();return {fbc:(fbc()||"").slice(0,300)||null,fbp:(fbp()||"").slice(0,120)||null,fbclid:k?k.id:null,landing_page:k?k.landing:null,user_agent:navigator.userAgent.slice(0,500)}}
let metaReady=false;
function metaBoot(){if(LOCAL_PREVIEW)return;
  if(metaReady||getConsent()!=="granted")return;metaReady=true;persistClick();
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version="2.0";n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,"script","https://connect.facebook.net/en_US/fbevents.js");
  try{fbq("consent","grant");fbq("init",META_PIXEL);fbq("track","PageView")}catch(e){}
  const q=window.__metaQ||[];window.__metaQ=[];q.forEach(a=>metaEvent.apply(null,a));
}
/* name: Meta standard event · params: custom_data · opt.server: also send via CAPI with opt.user · opt.eventID to reuse */
function metaEvent(name,params={},opt={}){if(LOCAL_PREVIEW)return;
  if(getConsent()!=="granted")return null;
  const eventID=opt.eventID||uuid();
  if(!metaReady){(window.__metaQ=window.__metaQ||[]).push([name,params,{...opt,eventID}]);metaBoot();return eventID}
  try{fbq("track",name,params,{eventID})}catch(e){}
  if(opt.server){try{fetch(CAPI_URL,{method:"POST",keepalive:true,headers:{"Content-Type":"application/json"},
    body:JSON.stringify({event_name:name,event_id:eventID,event_time_ms:Date.now(),consent:true,event_source_url:location.href.split("#")[0].slice(0,500),
      session_id:getSID(),fbc:fbc(),fbp:fbp(),user:opt.user||{},custom_data:params})}).catch(()=>{})}catch(e){}}
  track("meta_"+name.toLowerCase(),{event_id:eventID,server:!!opt.server,value:params.value});
  return eventID;
}
/* product ids for Meta: hard-3, ultra-1, duo-2; "-sub" for subscriptions */
function skuOf(l){return `${l.duo?"duo":l.level}-${l.pack}${l.sub?"-sub":""}`}
function cartContents(){return cart.map(l=>({id:skuOf(l),quantity:l.qty,item_price:l.price}))}
document.addEventListener("DOMContentLoaded",metaBoot);

/* ---------- top bar currency switch (English pages) + footer language link ---------- */
const LANGS={en:"English",de:"Deutsch",lt:"Lietuviškai"};
const LT_PAGES=["index.html","gums.html","gum.html","energy.html","checkout.html","terms.html","returns.html","shipping.html","privacy.html","safety.html","legal.html"];
document.addEventListener("DOMContentLoaded",()=>{
  let file=(location.pathname.split("/").pop()||"index.html");if(!file.includes("."))file+=".html";
  const clean=file==="index.html"?"":file.replace(/\.html$/,"");
  if(LANG==="en"){
    const w=document.querySelector(".top-bar .wrap");
    if(w&&!w.querySelector(".cur-sw")){
      const link=m=>{const u=new URL(location.href);u.searchParams.set("market",m);return u.pathname.split("/").pop()+u.search+u.hash};
      const sp=document.createElement("span");sp.className="cur-sw";sp.setAttribute("aria-label","Currency");
      sp.innerHTML=`<a href="${link("eu")}" ${MARKET==="eu"?'aria-current="true"':""}>€ EUR</a><a href="${link("us")}" ${MARKET==="us"?'aria-current="true"':""}>$ USD</a>`;
      const t=document.createElement("span");t.className="tb-txt";while(w.firstChild)t.appendChild(w.firstChild);w.appendChild(t);
      w.classList.add("has-sw");w.appendChild(sp);
      sp.addEventListener("click",e=>{const a=e.target.closest("a");if(a)track("currency_switch",{to:a.textContent.trim()})});
    }
  }
  const f=document.querySelector("footer .legal");
  if(f&&!document.getElementById("langLink")){
    const base=LANG==="en"?"":"../",page=LT_PAGES.includes(file)?clean:"";
    const a=document.createElement("p");a.id="langLink";a.className="mk-switch";
    a.innerHTML=Object.keys(LANGS).filter(l=>l!==LANG).map(l=>`<a href="${base}${l==="en"?"":l+"/"}${page}" hreflang="${l}" lang="${l}">${LANGS[l]}</a>`).join(" · ");
    f.parentNode.insertBefore(a,f);
  }
  if(LANG!=="en"){const m=document.getElementById("mkSwitch");if(m)m.remove()}
});
