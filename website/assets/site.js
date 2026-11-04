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

/* ---------- flavour icons + custom flavour picker (replaces native <select>) ---------- */
const FL_ICON={
  Mint:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21c0-6 1-11 7-17-1 7-3 12-7 17z" fill="#3FB984"/><path d="M12 21C11 15 8 10 4 7c0 6 3 11 8 14z" fill="#7CC9EA"/><path d="M12 21c0-5 1.5-9 5-13M12 21c-.6-4-2.4-8-6-11" stroke="#fff" stroke-width="1" fill="none" opacity=".7"/></svg>',
  Mango:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7c4-4 12-2 13 5s-5 10-10 9S3 11 7 7z" fill="#F4B23E"/><path d="M8 9c2-2 6-2 8 0" stroke="#fff" stroke-width="1.3" fill="none" opacity=".55" stroke-linecap="round"/><path d="M12 5c1-2 3-3 5-3-1 2-3 3-5 3z" fill="#3FB984"/></svg>',
  Watermelon:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 9h20a10 10 0 0 1-20 0z" fill="#3FB984"/><path d="M4 9h16a8 8 0 0 1-16 0z" fill="#EE6A7A"/><circle cx="9" cy="12" r=".9" fill="#2b1d1d"/><circle cx="12" cy="14" r=".9" fill="#2b1d1d"/><circle cx="15" cy="12" r=".9" fill="#2b1d1d"/></svg>',
  Blueberry:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="14" r="6" fill="#5B43B8"/><circle cx="16" cy="11" r="5.5" fill="#7D5CD9"/><path d="M14.5 8.5l1.5 1 1.5-1-.5 1.8" stroke="#2f2366" stroke-width="1.1" fill="none" stroke-linecap="round"/><circle cx="7.5" cy="12.5" r="1.3" fill="#fff" opacity=".35"/></svg>'
};
const flIcon=f=>`<span class="fl-ic">${FL_ICON[f]||""}</span>`;
/* kind: "mix" | "duo" · i: slot index · val: current flavour · label: aria label */
function fselHTML(kind,i,val,label){
  const opts=Object.keys(FL_ICON).map(f=>`<li role="option" tabindex="-1" data-v="${f}" aria-selected="${f===val}">${flIcon(f)}<span>${f}</span>${f===val?'<span class="ck" aria-hidden="true">✓</span>':""}</li>`).join("");
  return `<div class="fsel" data-kind="${kind}" data-i="${i}"><button type="button" class="fsel-btn" aria-haspopup="listbox" aria-expanded="false" aria-label="${label}: ${val}">${flIcon(val)}<span class="nm">${val}</span><span class="cv" aria-hidden="true">▾</span></button><ul class="fsel-list" role="listbox" aria-label="${label}" hidden>${opts}</ul></div>`;
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
