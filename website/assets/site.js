/* Shared catalogue + cart drawer for the Cutline draft store. Checkout is not connected yet. */
const CATALOG={
  hard:{name:"Cutline Hard Gum",short:"Hard",grams:116,cls:"",
    flavours:{"Mint":"#3FB8A0","Mango":"#F2A33A","Watermelon":"#E9546B","Blueberry":"#5B6BE0"}},
  ultra:{name:"Cutline Ultra Hard Gum",short:"Ultra Hard",grams:100,cls:"ultra",
    flavours:{"Blueberry Ice":"#6E8BF0","Cherry Ice":"#D13B55","Mint":"#3FB8A0","Ginger Lime":"#A6C93E"}}
};
const PACKS=[
  {id:1,label:"2 Months Supply",sub:"1 pack",price:19.95},
  {id:3,label:"6 Months Supply",sub:"3 packs, mix flavours",price:34.95,tag:"Bestseller"},
  {id:6,label:"12 Months Supply",sub:"6 packs, mix flavours",price:59.95}
];
const FREE_SHIP=49;
const eur=n=>"€"+n.toFixed(2).replace(".",",");
const $=id=>document.getElementById(id);
function pouchHTML(level,flavour,extra=""){
  const L=CATALOG[level];const c=L.flavours[flavour]||Object.values(L.flavours)[0];
  return `<div class="pouch ${L.cls} ${extra}" style="--fl:${c}"><div class="p-top"><small>Jaw training gum</small><b>Cutline</b></div><span class="p-lvl">${L.short}</span><span class="p-fl">${flavour}</span></div>`;
}

/* cart (kept in this browser only) */
let cart=[];
try{cart=JSON.parse(localStorage.getItem("cutline-cart")||"[]")}catch(e){cart=[]}
function saveCart(){try{localStorage.setItem("cutline-cart",JSON.stringify(cart))}catch(e){}}
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
  if(!cart.length){lines.innerHTML='<p class="empty">Your cart is empty.</p>'}
  else lines.innerHTML=cart.map((l,i)=>`<div class="line">${pouchHTML(l.level,l.flavour)}<div><b>${CATALOG[l.level].short} · ${l.flavour}</b><small>${l.label} · qty ${l.qty}</small><br><button class="rm" data-rm="${i}" type="button">Remove</button></div><b>${eur(l.price*l.qty)}</b></div>`).join("");
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
  if(e.target.closest("#checkoutBtn"))toast("Checkout will be connected before launch.");
});
document.addEventListener("keydown",e=>{if(e.key==="Escape")closeCart()});
document.addEventListener("DOMContentLoaded",renderCart);

/* newsletter (demo) */
document.addEventListener("submit",e=>{
  const f=e.target.closest("[data-news]");if(!f)return;e.preventDefault();
  f.hidden=true;const ok=f.nextElementSibling;if(ok)ok.hidden=false;
});

/* Review cards. SAMPLE_REVIEWS are layout placeholders only: replace with real,
   order-linked reviews (e.g. from Judge.me / Loox) before launch. Never publish samples as real. */
const SAMPLE_REVIEWS=[
  {i:"A",name:"Customer name",lvl:"hard",fl:"Mint",pack:"6 Months Supply",text:"Sample review text. A real buyer's words about hardness, flavour and how the sessions feel will appear here."},
  {i:"B",name:"Customer name",lvl:"ultra",fl:"Blueberry Ice",pack:"2 Months Supply",text:"Sample review text. Short, honest feedback from a verified order."},
  {i:"C",name:"Customer name",lvl:"hard",fl:"Mango",pack:"12 Months Supply",text:"Sample review text. Longer reviews wrap naturally and the cards stack in columns, like on the reference store."},
  {i:"D",name:"Customer name",lvl:"hard",fl:"Watermelon",pack:"6 Months Supply",text:"Sample review text."},
  {i:"E",name:"Customer name",lvl:"ultra",fl:"Cherry Ice",pack:"6 Months Supply",text:"Sample review text. Customers can attach a photo of the pack or of themselves."},
  {i:"F",name:"Customer name",lvl:"ultra",fl:"Ginger Lime",pack:"2 Months Supply",text:"Sample review text from a verified buyer."}
];
function renderReviews(el,list,n){
  el.innerHTML=list.slice(0,n).map((r,k)=>`<article class="rv"><span class="rv-sample">Sample</span>
    <div class="rv-photo"><div class="rv-tilt" style="--r:${k%2?4:-4}deg">${pouchHTML(r.lvl,r.fl)}</div></div>
    <div class="rv-body"><span class="rv-stars" aria-label="Rating">★★★★★</span><p>${r.text}</p>
    <div class="rv-meta"><span class="rv-av">${r.i}</span><span><b>${r.name}</b><small>${CATALOG[r.lvl].short} · ${r.fl} · ${r.pack}</small></span><span class="rv-ver">✓ Verified</span></div></div></article>`).join("");
}
