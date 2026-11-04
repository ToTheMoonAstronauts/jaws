/* Shared catalogue + cart drawer for the JAWZR draft store. Checkout is not connected yet. */
const CATALOG={
  hard:{name:"JAWZR Hard Gum",short:"Hard",grams:116,cls:"",
    flavours:{"Mint":"#7CC9EA","Mango":"#F4B23E","Watermelon":"#EE6A7A","Blueberry":"#7D5CD9"}},
  ultra:{name:"JAWZR Ultra Hard Gum",short:"Ultra Hard",grams:100,cls:"ultra",
    flavours:{"Mint":"#7CC9EA","Mango":"#F4B23E","Watermelon":"#EE6A7A","Blueberry":"#7D5CD9"}}
};
const PACKS=[
  {id:1,label:"1 Pack · 40 pieces",sub:"Covers the full 30-day plan",price:{hard:17.95,ultra:23.95}},
  {id:2,label:"Starter Duo · 80 pieces",sub:"1 Hard + 1 Ultra Hard, made for the 30-day plan",price:{hard:37.95,ultra:37.95},tag:"New",duo:true},
  {id:3,label:"3 Packs · 120 pieces",sub:"4 months of daily training, mix flavours",price:{hard:31.95,ultra:41.95},tag:"Bestseller"},
  {id:6,label:"6 Packs · 240 pieces",sub:"8 months of daily training, free shipping",price:{hard:53.95,ultra:71.95}}
];
const packPrice=(level,id)=>PACKS.find(p=>p.id===id).price[level];
/* what the same pieces cost as single packs (for "Save x%") */
const singlesPrice=(level,id)=>id===2?PACKS[0].price.hard+PACKS[0].price.ultra:PACKS[0].price[level]*id;
const SUB_OFF=0.15;
const subPrice=p=>Math.round(p*(1-SUB_OFF)*100)/100;
const FREE_SHIP=49;
const eur=n=>"€"+n.toFixed(2).replace(".",",");
const $=id=>document.getElementById(id);
function inkOn(h){const n=parseInt(h.slice(1),16),r=n>>16,g=n>>8&255,b=n&255;return (0.299*r+0.587*g+0.114*b)>150?"#121614":"#fff"}
const slug=f=>f.toLowerCase().replace(/[^a-z]+/g,"-");
const MIXED="Mixed",MIXED_C="conic-gradient(#7CC9EA 0 33%,#F4B23E 0 66%,#EE6A7A 0)";
function packSrc(level,flavour){return flavour===MIXED?`images/products/bundle-${level}.webp`:`images/products/${level}-${slug(flavour)}.webp`}
function trioSrc(level,flavour){return flavour===MIXED?`images/products/bundle-${level}.webp`:`images/products/trio-${level}-${slug(flavour)}.webp`}
function pouchHTML(level,flavour,extra=""){
  const L=CATALOG[level];const c=L.flavours[flavour]||Object.values(L.flavours)[0];
  return `<div class="pouch ${L.cls} ${extra} ${flavour===MIXED?"mixed":""}"><img src="${packSrc(level,flavour)}" alt="JAWZR ${L.short} gum, ${flavour===MIXED?"mixed flavours (mint, mango, watermelon)":flavour+" flavour"}" loading="lazy"></div>`;
}

/* cart (kept in this browser only) */
let cart=[];
try{cart=JSON.parse(localStorage.getItem("jawzr-cart-v2")||"[]")}catch(e){cart=[]}
function saveCart(){try{localStorage.setItem("jawzr-cart-v2",JSON.stringify(cart))}catch(e){}}
function cartTotal(){return cart.reduce((s,l)=>s+l.price*l.qty,0)}
function cartCount(){return cart.reduce((s,l)=>s+l.qty,0)}
/* mix (optional): array of flavours, one per pack, e.g. ["Mint","Mint","Mango"] */
function mixLabel(mix){const o=Object.keys(CATALOG.hard.flavours),c={};mix.forEach(f=>c[f]=(c[f]||0)+1);return Object.entries(c).sort((x,y)=>o.indexOf(x[0])-o.indexOf(y[0])).map(([f,n])=>n>1?`${f} ×${n}`:f).join(", ")}
/* opts.duo: [hardFlavour, ultraFlavour] for the Starter Duo · opts.sub: {every:"4 months"} for a subscription */
function addToCart(level,flavour,packId,mix,opts={}){
  const P=PACKS.find(p=>p.id===packId);
  let name=flavour,duo=opts.duo||null,sub=opts.sub||null;
  if(duo){level="hard";flavour=duo[0];name=`Hard ${duo[0]} + Ultra Hard ${duo[1]}`;}
  else if(mix&&mix.length){const u=[...new Set(mix)];flavour=u.length===1?u[0]:MIXED;name=u.length===1?u[0]:mixLabel(mix);}
  const key=level+"|"+name+"|"+packId+"|"+(sub?sub.every:"once");
  const price=sub?subPrice(P.price[level]):P.price[level];
  const ex=cart.find(l=>l.key===key);
  if(ex)ex.qty++;else cart.push({key,level,flavour,name,mix:mix||null,duo,sub,pack:packId,label:P.label+(sub?` · Subscription, every ${sub.every} (−${SUB_OFF*100}%)`:""),price,qty:1});
  saveCart();renderCart();openCart();
}
function lineTitle(l){return l.duo?`Starter Duo · Hard ${l.duo[0]} + Ultra Hard ${l.duo[1]}`:`${CATALOG[l.level].short} · ${l.flavour===MIXED?"Mixed flavours":(l.name||l.flavour)}`}
function renderCart(){
  document.querySelectorAll("[data-cart-count]").forEach(e=>e.textContent=cartCount());
  const lines=$("cartLines");if(!lines)return;
  if(!cart.length){lines.innerHTML='<p class="empty">Your cart is empty.</p>'}
  else lines.innerHTML=cart.map((l,i)=>`<div class="line">${pouchHTML(l.level,l.flavour)}<div><b>${lineTitle(l)}</b><small>${l.label} · qty ${l.qty}</small><br><button class="rm" data-rm="${i}" type="button">Remove</button></div><b>${eur(l.price*l.qty)}</b></div>`).join("");
  const t=cartTotal();$("cartTotal").textContent=eur(t);
  const left=FREE_SHIP-t;
  $("shipMsg").textContent=t===0?`Free EU shipping from ${eur(FREE_SHIP)}`:left>0?`${eur(left)} away from free EU shipping`:"You get free EU shipping";
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
  sbInsert("leads",{session_id:getSID(),source:"newsletter",email:email.trim().slice(0,254),marketing_consent:true,utm:UTM});track("newsletter_signup");
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
function getConsent(){try{return localStorage.getItem("cutline-consent")}catch(e){return null}}
function setConsent(v){try{localStorage.setItem("cutline-consent",v)}catch(e){}}
const TMP_SID="tmp-"+Math.random().toString(36).slice(2,12);
function getSID(){
  if(getConsent()!=="granted")return TMP_SID;
  try{let s=localStorage.getItem("cutline-sid");if(!s){s=(crypto.randomUUID?crypto.randomUUID():String(Date.now())+Math.random()).slice(0,36);localStorage.setItem("cutline-sid",s)}return s}catch(e){return TMP_SID}
}
const UTM=(()=>{const q=new URLSearchParams(location.search),u={};["utm_source","utm_medium","utm_campaign","utm_content","utm_term","fbclid"].forEach(k=>{if(q.get(k))u[k]=q.get(k).slice(0,200)});
  try{if(Object.keys(u).length&&getConsent()==="granted")sessionStorage.setItem("cutline-utm",JSON.stringify(u));return Object.keys(u).length?u:JSON.parse(sessionStorage.getItem("cutline-utm")||"{}")}catch(e){return u}})();
function sbInsert(table,row){
  return fetch(SB_URL+table,{method:"POST",keepalive:true,headers:{"apikey":SB_KEY,"Authorization":"Bearer "+SB_KEY,"Content-Type":"application/json","Prefer":"return=minimal"},body:JSON.stringify(row)})
    .then(r=>r.ok).catch(()=>false);
}
function track(event,props={}){
  if(getConsent()!=="granted")return Promise.resolve(false);
  return sbInsert("events",{session_id:getSID(),event,page:location.pathname.slice(-200),props,referrer:(document.referrer||"").slice(0,500),utm:UTM});
}
document.addEventListener("DOMContentLoaded",()=>track("page_view"));
/* wrap addToCart so every add is tracked */
const _addToCart=addToCart;
addToCart=function(level,flavour,packId,mix,opts={}){track("add_to_cart",{level,flavour,pack:packId,mix:mix?mix.join("|"):undefined,duo:opts.duo?opts.duo.join("|"):undefined,sub:opts.sub?opts.sub.every:undefined});return _addToCart(level,flavour,packId,mix,opts)};

/* cookie banner */
function cookieBanner(){
  let b=document.getElementById("cookieBar");
  if(!b){b=document.createElement("div");b.id="cookieBar";b.className="cookie-bar";b.setAttribute("role","dialog");b.setAttribute("aria-label","Cookie choice");
    b.innerHTML='<p>We use your browser\'s storage to keep your cart. With your OK, we also measure visits and shop steps to see how many people are interested in JAWZR. No advertising cookies. <a href="privacy.html">Privacy &amp; Cookies</a></p><div class="cookie-btns"><button type="button" class="btn ghost" data-consent="denied">Decline</button><button type="button" class="btn" data-consent="granted">Accept analytics</button></div>';
    document.body.appendChild(b);}
  b.hidden=false;
}
document.addEventListener("click",e=>{
  const c=e.target.closest("[data-consent]");
  if(c){const v=c.dataset.consent,was=getConsent();setConsent(v);document.getElementById("cookieBar").hidden=true;
    if(v==="granted"&&was!=="granted"){track("consent",{value:v});track("page_view")}}
  if(e.target.closest("[data-cookie-settings]")){e.preventDefault();cookieBanner()}
});
document.addEventListener("DOMContentLoaded",()=>{if(!getConsent())cookieBanner()});

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
      sbInsert("leads",{session_id:getSID(),source:"popup_10",email:v.slice(0,254),marketing_consent:true,utm:UTM});track("popup_signup",{trigger});
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
