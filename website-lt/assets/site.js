/* Shared catalogue + cart drawer for the Cutline draft store. Checkout is not connected yet. */
const CATALOG={
  hard:{name:"Cutline kieta guma",short:"Kieta",grams:116,cls:"",
    flavours:{"Mėtų":"#3FB8A0","Mangų":"#F2A33A","Arbūzų":"#E9546B","Mėlynių":"#5B6BE0"}},
  ultra:{name:"Cutline ypač kieta guma",short:"Ypač kieta",grams:100,cls:"ultra",
    flavours:{"Ledinių mėlynių":"#6E8BF0","Ledinių vyšnių":"#D13B55","Mėtų":"#3FB8A0","Imbiero ir laimo":"#A6C93E"}}
};
const PACKS=[
  {id:1,label:"2 mėnesių atsargos",sub:"1 pakuotė",price:19.95},
  {id:3,label:"6 mėnesių atsargos",sub:"3 pakuotės, derink skonius",price:34.95,tag:"Perkamiausias"},
  {id:6,label:"12 mėnesių atsargos",sub:"6 pakuotės, derink skonius",price:59.95}
];
const FREE_SHIP=49;
const eur=n=>n.toFixed(2).replace(".",",")+" €";
const $=id=>document.getElementById(id);
function pouchHTML(level,flavour,extra=""){
  const L=CATALOG[level];const c=L.flavours[flavour]||Object.values(L.flavours)[0];
  return `<div class="pouch ${L.cls} ${extra}" style="--fl:${c}"><div class="p-top"><small>Žandikaulio treniruotėms</small><b>Cutline</b></div><span class="p-lvl">${L.short}</span><span class="p-fl">${flavour}</span></div>`;
}

/* cart (kept in this browser only) */
let cart=[];
try{cart=JSON.parse(localStorage.getItem("cutline-lt-cart")||"[]")}catch(e){cart=[]}
function saveCart(){try{localStorage.setItem("cutline-lt-cart",JSON.stringify(cart))}catch(e){}}
function cartTotal(){return cart.reduce((s,l)=>s+l.price*l.qty,0)}
function cartCount(){return cart.reduce((s,l)=>s+l.qty,0)}
function addToCart(level,flavour,packId){
  const P=PACKS.find(p=>p.id===packId);
  const key=level+"|"+flavour+"|"+packId;
  const ex=cart.find(l=>l.key===key);
  if(ex)ex.qty++;else cart.push({key,level,flavour,pack:packId,label:P.label,price:P.price,qty:1});
  saveCart();renderCart();openCart();
}
function renderCart(){
  document.querySelectorAll("[data-cart-count]").forEach(e=>e.textContent=cartCount());
  const lines=$("cartLines");if(!lines)return;
  if(!cart.length){lines.innerHTML='<p class="empty">Tavo krepšelis tuščias.</p>'}
  else lines.innerHTML=cart.map((l,i)=>`<div class="line">${pouchHTML(l.level,l.flavour)}<div><b>${CATALOG[l.level].short} · ${l.flavour}</b><small>${l.label} · ${l.qty} vnt.</small><br><button class="rm" data-rm="${i}" type="button">Pašalinti</button></div><b>${eur(l.price*l.qty)}</b></div>`).join("");
  const t=cartTotal();$("cartTotal").textContent=eur(t);
  const left=FREE_SHIP-t;
  $("shipMsg").textContent=t===0?`Nemokamas pristatymas ES nuo ${eur(FREE_SHIP)}`:left>0?`Iki nemokamo pristatymo trūksta ${eur(left)}`:"Pristatymas nemokamas";
  $("shipBar").style.width=Math.min(100,t/FREE_SHIP*100)+"%";
}
function openCart(){$("drawerBg").hidden=false;$("drawer").hidden=false}
function closeCart(){$("drawerBg").hidden=true;$("drawer").hidden=true}
let tt;function toast(m){const t=$("toast");if(!t)return;t.textContent=m;t.hidden=false;clearTimeout(tt);tt=setTimeout(()=>t.hidden=true,2800)}
document.addEventListener("click",e=>{
  if(e.target.closest("[data-open-cart]"))openCart();
  if(e.target.closest("[data-close-cart]"))closeCart();
  const rm=e.target.closest("[data-rm]");if(rm){cart.splice(+rm.dataset.rm,1);saveCart();renderCart();}
  if(e.target.closest("#checkoutBtn")){if(!cart.length){toast("Tavo krepšelis tuščias.");return}location.href="checkout.html"}
});
document.addEventListener("keydown",e=>{if(e.key==="Escape")closeCart()});
document.addEventListener("DOMContentLoaded",renderCart);

/* newsletter (demo) */
document.addEventListener("submit",e=>{
  const f=e.target.closest("[data-news]");if(!f)return;e.preventDefault();
  const email=(f.querySelector("input[type=email]")||{}).value||"";
  sbInsert("leads",{session_id:getSID(),lang:"lt",source:"newsletter",email:email.trim().slice(0,254),marketing_consent:true,utm:UTM});track("newsletter_signup");
  f.hidden=true;const ok=f.nextElementSibling;if(ok)ok.hidden=false;
});

/* Review cards. SAMPLE_REVIEWS are layout placeholders only: replace with real,
   order-linked reviews (e.g. from Judge.me / Loox) before launch. Never publish samples as real. */
const SAMPLE_REVIEWS=[
  {i:"A",name:"Pirkėjo vardas",lvl:"hard",fl:"Mėtų",pack:"6 mėnesių atsargos",text:"Pavyzdinis atsiliepimas. Čia bus tikro pirkėjo žodžiai apie kietumą, skonį ir treniruotes."},
  {i:"B",name:"Pirkėjo vardas",lvl:"ultra",fl:"Ledinių mėlynių",pack:"2 mėnesių atsargos",text:"Pavyzdinis atsiliepimas. Trumpas, sąžiningas patvirtinto pirkėjo atsiliepimas."},
  {i:"C",name:"Pirkėjo vardas",lvl:"hard",fl:"Mangų",pack:"12 mėnesių atsargos",text:"Pavyzdinis atsiliepimas. Ilgesni atsiliepimai natūraliai perkeliami į kitą eilutę, o kortelės išsidėsto stulpeliais."},
  {i:"D",name:"Pirkėjo vardas",lvl:"hard",fl:"Arbūzų",pack:"6 mėnesių atsargos",text:"Pavyzdinis atsiliepimas."},
  {i:"E",name:"Pirkėjo vardas",lvl:"ultra",fl:"Ledinių vyšnių",pack:"6 mėnesių atsargos",text:"Pavyzdinis atsiliepimas. Pirkėjai gali pridėti pakuotės ar savo nuotrauką."},
  {i:"F",name:"Pirkėjo vardas",lvl:"ultra",fl:"Imbiero ir laimo",pack:"2 mėnesių atsargos",text:"Pavyzdinis patvirtinto pirkėjo atsiliepimas."}
];
function renderReviews(el,list,n){
  el.innerHTML=list.slice(0,n).map((r,k)=>`<article class="rv"><span class="rv-sample">Pavyzdys</span>
    <div class="rv-photo"><div class="rv-tilt" style="--r:${k%2?4:-4}deg">${pouchHTML(r.lvl,r.fl)}</div></div>
    <div class="rv-body"><span class="rv-stars" aria-label="Įvertinimas">★★★★★</span><p>${r.text}</p>
    <div class="rv-meta"><span class="rv-av">${r.i}</span><span><b>${r.name}</b><small>${CATALOG[r.lvl].short} · ${r.fl} · ${r.pack}</small></span><span class="rv-ver">✓ Patvirtintas</span></div></div></article>`).join("");
}

/* ---------- Fake door tracking (Supabase, insert-only) ---------- */
const SB_URL="https://vzfwovxlzgrtghxlfkbj.supabase.co/rest/v1/";
const SB_KEY="sb_publishable_JP7_gwTXfMBITq2e2gHe8A_snjOsWTT";
/* Consent: analytics only after the visitor accepts (ePrivacy/GDPR). Cart storage is strictly necessary. */
function getConsent(){try{return localStorage.getItem("cutline-lt-consent")}catch(e){return null}}
function setConsent(v){try{localStorage.setItem("cutline-lt-consent",v)}catch(e){}}
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
  return sbInsert("events",{session_id:getSID(),event,page:location.pathname.slice(-200),props:Object.assign({lang:"lt"},props),referrer:(document.referrer||"").slice(0,500),utm:UTM});
}
document.addEventListener("DOMContentLoaded",()=>track("page_view"));
/* wrap addToCart so every add is tracked */
const _addToCart=addToCart;
addToCart=function(level,flavour,packId){track("add_to_cart",{level,flavour,pack:packId});return _addToCart(level,flavour,packId)};

/* cookie banner */
function cookieBanner(){
  let b=document.getElementById("cookieBar");
  if(!b){b=document.createElement("div");b.id="cookieBar";b.className="cookie-bar";b.setAttribute("role","dialog");b.setAttribute("aria-label","Slapukų pasirinkimas");
    b.innerHTML='<p>Naršyklės atmintį naudojame tavo krepšeliui išsaugoti. Jei sutiksi, taip pat matuosime apsilankymus ir apsipirkimo žingsnius, kad sužinotume, kiek žmonių domisi Cutline. Reklaminių slapukų nenaudojame. <a href="privacy.html">Privatumas ir slapukai</a></p><div class="cookie-btns"><button type="button" class="btn ghost" data-consent="denied">Atsisakyti</button><button type="button" class="btn" data-consent="granted">Sutinku su analitika</button></div>';
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
