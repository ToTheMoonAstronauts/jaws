"""Builds the legal pages in website/ from one shared shell. Edit COMPANY and the texts below, then run:
   python3 tools/build_legal.py"""
import os, html
OUT = os.path.join(os.path.dirname(__file__), "..", "website")
UPDATED = "1 November 2026"
# The brand is used everywhere. The legal operator appears only once, on the Legal Notice,
# as OPERATOR (EU law requires the seller's legal name, address and registration number).
COMPANY = {
  "name": "Cutline",
  "address": "[return address], Lithuania",
  "email": "[contact email]",
}
OPERATOR = "[operator legal name]<br>[registered address]<br>Registration number: [registration number]<br>VAT: [VAT number, or: not VAT-registered]"
C = COMPANY

def shell(title, eyebrow, body, extra_head="", extra_js=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)} · Cutline</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800;900&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600;700&display=swap">
<link rel="stylesheet" href="assets/site.css">{extra_head}
</head>
<body>
<div class="top-bar"><div class="wrap">Free EU shipping from €49 · Ships from Lithuania</div></div>
<nav class="site"><div class="wrap">
  <a class="logo" href="index-v2.html"><i></i>Cutline</a>
  <div class="links"><a href="product.html">Shop</a><a href="index-v2.html#how">How it works</a><a href="index-v2.html#faq">FAQ</a></div>
  <button class="cart-btn" type="button" data-open-cart>Cart (<span data-cart-count>0</span>)</button>
</div></nav>
<main class="wrap legal">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{html.escape(title)}</h1>
  <p class="updated">Last updated {UPDATED}</p>
  <nav class="legal-toc" aria-label="Legal pages">{TOC}</nav>
  <article class="legal-body">
{body}
  </article>
</main>
{FOOTER}
{DRAWER}
<script src="assets/site.js"></script>{extra_js}
</body>
</html>
'''

PAGES = [("terms.html","Terms of Service"),("returns.html","Returns & Refunds"),("withdraw.html","Withdraw from contract"),
         ("shipping.html","Shipping & Payment"),("privacy.html","Privacy & Cookies"),("safety.html","Safety Instructions"),("legal.html","Legal Notice")]
TOC = "".join(f'<a href="{f}">{t}</a>' for f,t in PAGES)
FOOTER = '''<footer><div class="wrap">
  <div><a class="logo" href="index-v2.html" style="color:var(--bg)"><i></i>Cutline</a><p style="margin-top:12px;opacity:.75;max-width:40ch">Hard chewing gum for jaw training. Ships from Lithuania.</p></div>
  <div><h4>Shop</h4><ul><li><a href="product.html#hard">Hard Gum</a></li><li><a href="product.html#ultra">Ultra Hard Gum</a></li><li><a href="product.html#hard-6">6-Month Bundle</a></li></ul></div>
  <div><h4>Info</h4><ul><li><a href="terms.html">Terms of Service</a></li><li><a href="returns.html">Returns &amp; Refunds</a></li><li><a href="shipping.html">Shipping &amp; Payment</a></li><li><a href="privacy.html">Privacy &amp; Cookies</a></li><li><a href="safety.html">Safety Instructions</a></li><li><a href="legal.html">Legal Notice</a></li><li><a href="withdraw.html"><b>Withdraw from contract here</b></a></li><li><a href="#" data-cookie-settings>Cookie settings</a></li></ul></div>
  <p class="legal">© 2026 Cutline</p>
</div></footer>'''
DRAWER = '''<div class="drawer-bg" id="drawerBg" hidden data-close-cart></div>
<aside class="drawer" id="drawer" hidden aria-label="Cart">
  <header><h3>Your cart</h3><button class="x" type="button" data-close-cart aria-label="Close cart">×</button></header>
  <div class="ship-meter"><span id="shipMsg"></span><div class="bar"><i id="shipBar"></i></div></div>
  <div class="lines" id="cartLines"></div>
  <div class="tot"><span>Total</span><span id="cartTotal">€0,00</span></div>
  <button class="btn block big" type="button" id="checkoutBtn">Checkout</button>
</aside>
<div class="toast" id="toast" hidden></div>'''

PRELAUNCH = '''<div class="callout"><b>Pre-launch notice.</b> Cutline is not on sale yet. If you complete checkout now, we register a <b>pre-order request</b> only: no contract of sale is formed, no payment is taken and no payment details are collected. We'll email you when products are available, and you are free not to buy.</div>'''

TERMS = f'''{PRELAUNCH}
<h2>1. Who we are</h2>
<p>Cutline is an online shop for hard chewing gum, based in Lithuania. The business that operates Cutline is identified in our <a href="legal.html">Legal Notice</a>. Email: {C["email"]}. These terms apply to all orders placed on this website.</p>
<h2>2. Pre-launch period</h2>
<p>While the pre-launch notice above is shown, the shop is used to measure interest before we start selling. Completing checkout creates a pre-order request, not a purchase. We store the details you enter (see our <a href="privacy.html">Privacy Policy</a>) to contact you about availability. No money is charged at any point during this period. Sections 3 to 11 apply once sales open and the notice is removed.</p>
<h2>3. Who can buy</h2>
<p>You must be at least 18, or have a parent or guardian's consent, to place an order. Our products are not for children under 14. We sell to consumers in the European Union. We currently don't ship outside the EU.</p>
<h2>4. Product information</h2>
<p>We describe our products, ingredients, nutrition values and use instructions as accurately as we can. Product pictures may differ slightly from the packaging you receive. Our gum is a food product used for chewing exercise. It is not a medical device and does not treat or prevent any condition.</p>
<h2>5. How a contract is made</h2>
<p>Product pages are an invitation to order. When you click the order button, you make an offer to buy. We confirm receipt by email. The contract is formed when we send you an order confirmation or dispatch the goods, whichever comes first. You can review and correct your order on the checkout page before submitting it. We send you these terms and your order details by email, and you can save or print this page.</p>
<h2>6. Prices and payment</h2>
<p>Prices are in euros and include VAT where applicable. Delivery costs are shown before you order. Payment is processed by licensed payment providers; we never see or store your full card number. Your payment is taken when you place the order. When we show a reduced price, the reference price is the lowest price we charged in the 30 days before the reduction.</p>
<h2>7. Delivery</h2>
<p>We deliver within the time stated in our <a href="shipping.html">Shipping &amp; Payment</a> policy and in any case within 30 days of the contract unless agreed otherwise. If we can't deliver because a product is unavailable, we tell you without delay and refund any payment within 14 days. The risk of loss passes to you when you or a person you name receives the goods.</p>
<h2>8. Your right to withdraw</h2>
<p>You can withdraw from the contract within 14 days without giving a reason. Details, exceptions and how to send goods back are in <a href="returns.html">Returns &amp; Refunds</a>. You can withdraw online at any time using <a href="withdraw.html">Withdraw from contract here</a>. Sealed gum packs that you have opened after delivery can't be returned for health and hygiene reasons.</p>
<h2>9. Legal guarantee</h2>
<p>You have the statutory rights for goods that don't conform to the contract, for 2 years from delivery. If a product is faulty, damaged in transit, or you received the wrong item, contact us at {C["email"]} with your order number and a photo. We'll replace it or refund you at no cost. Please use products before the best-before date printed on the pack.</p>
<h2>10. Liability</h2>
<p>We are liable under applicable law for damage caused intentionally or through gross negligence, for death or personal injury, and under product liability law. For other damage caused by slight negligence, our liability is limited to the foreseeable damage typical for this type of contract. Nothing in these terms limits your statutory rights as a consumer. Please follow the <a href="safety.html">Safety Instructions</a>: harm caused by use against those instructions is not caused by a defect in the product.</p>
<h2>11. Reviews and content you send us</h2>
<p>Reviews on our site come from customers with a confirmed order. We don't publish reviews we have paid for or written ourselves, and we don't remove negative reviews because they are negative. If you send us a review or photo, you allow us to show it on our website and social media with your first name. You can ask us to remove it at any time.</p>
<h2>12. Complaints and disputes</h2>
<p>Please contact us first at {C["email"]}. We reply within 14 days. If we can't resolve it, you can file a complaint free of charge with the Lithuanian State Consumer Rights Protection Authority (Valstybinė vartotojų teisių apsaugos tarnyba), Vilniaus g. 25, 01402 Vilnius, <a href="https://www.vvtat.lt" rel="noopener">www.vvtat.lt</a>, or with the consumer authority or courts of your own country.</p>
<h2>13. Applicable law</h2>
<p>These terms are governed by the law of the Republic of Lithuania. If you are a consumer living in another EU country, you keep the protection of the mandatory consumer laws of that country.</p>
<h2>14. Changes</h2>
<p>We may update these terms for future orders. The version in force when you place your order applies to that order.</p>'''

RETURNS = f'''{PRELAUNCH}
<h2>Your 14-day right of withdrawal</h2>
<p>You may withdraw from your contract within 14 days without giving any reason. The period ends 14 days after the day you, or a person you name other than the carrier, receive the goods. If you ordered several items delivered separately, it runs from receipt of the last one.</p>
<h2>How to withdraw</h2>
<p>Tell us clearly that you want to withdraw before the period ends. The quickest way is our online form, <a href="withdraw.html">Withdraw from contract here</a>. You can also email {C["email"]} or write to {C["name"]}, {C["address"]}. You may use the model form below, but you don't have to.</p>
<h2>Sending items back</h2>
<p>Send the goods back without undue delay and no later than 14 days after telling us you are withdrawing, to: {C["name"]}, {C["address"]}. Please include your order number. You pay the direct cost of returning the goods. You are only responsible for a loss in value caused by handling beyond what was needed to check the goods.</p>
<h2>Hygiene exception for gum</h2>
<p>Our gum comes in sealed packs. For health and hygiene reasons, a pack that you open after delivery can't be returned, and the right of withdrawal ends for that pack once it is unsealed. Unopened, sealed packs can always be returned within the 14 days.</p>
<h2>Your refund</h2>
<p>We refund all payments received from you, including standard delivery costs, without undue delay and at the latest within 14 days of receiving your withdrawal. If you chose a more expensive delivery than our standard option, we don't refund the extra. We use the same payment method you used, unless you agree otherwise, and you won't pay any fees for the refund. We may hold the refund until we've received the goods back or you've shown proof of sending them, whichever is earlier.</p>
<h2>Faulty, damaged or wrong items</h2>
<p>This is separate from withdrawal and covered by your legal guarantee. Email {C["email"]} with your order number and a photo within a reasonable time of noticing the problem. We'll send a replacement or refund you, and you don't need to return the item or pay any postage.</p>
<h2>Model withdrawal form</h2>
<div class="formbox">
<p>To {C["name"]}, {C["address"]}, {C["email"]}:</p>
<p>I/We (*) hereby give notice that I/We (*) withdraw from my/our (*) contract of sale of the following goods (*):</p>
<p>Ordered on (*) / received on (*):<br>Name of consumer(s):<br>Address of consumer(s):<br>Signature of consumer(s) (only if this form is notified on paper):<br>Date:</p>
<p><small>(*) Delete as appropriate.</small></p>
</div>'''

WITHDRAW = f'''<p>Use this form to withdraw from a contract within your 14-day withdrawal period. You don't need to log in or give a reason. After you confirm, you'll see a receipt with the date and time we received your withdrawal. Save or screenshot it; we'll also confirm by email within 2 business days.</p>
<div class="callout"><b>Pre-launch:</b> no sales contracts exist yet, so nothing can be charged. If you placed a pre-order request and want us to delete it, you can use this form too, or email {C["email"]}.</div>
<form id="wForm" class="wform" novalidate>
  <div class="step" id="wStep1">
    <h2>Step 1: your details</h2>
    <div class="f-grid2">
      <div class="field"><label for="wName">Full name</label><input id="wName" autocomplete="name" required><span class="err" id="wNameErr"></span></div>
      <div class="field"><label for="wEmail">Email used for the order</label><input id="wEmail" type="email" autocomplete="email" required><span class="err" id="wEmailErr"></span></div>
      <div class="field"><label for="wOrder">Order number (if you have it)</label><input id="wOrder" placeholder="e.g. #1042"></div>
      <div class="field"><label for="wDate">Order date (if you know it)</label><input id="wDate" type="date"></div>
      <div class="field full"><label for="wItems">Which items? (leave empty for the whole order)</label><input id="wItems" placeholder="e.g. Hard Gum, Mint, 6 Months Supply"></div>
    </div>
    <button class="btn big" type="button" id="wNext">Continue</button>
  </div>
  <div class="step" id="wStep2" hidden>
    <h2>Step 2: confirm</h2>
    <div class="formbox" id="wSummary"></div>
    <div class="cta-row"><button class="btn big" type="submit" id="wSubmit">Confirm withdrawal</button><button class="btn ghost" type="button" id="wBack">Edit details</button></div>
  </div>
  <div class="step" id="wDone" hidden>
    <h2>Withdrawal received</h2>
    <div class="callout ok" id="wReceipt"></div>
    <p>Keep this receipt. If you've received goods, please send unopened packs back within 14 days, as explained in <a href="returns.html">Returns &amp; Refunds</a>.</p>
  </div>
  <p class="err" id="wErr"></p>
</form>'''

WITHDRAW_JS = '''
<script>
const v=id=>document.getElementById(id).value.trim();
const okEmail=e=>/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(e);
$("wNext").addEventListener("click",()=>{
  let ok=true;
  $("wNameErr").textContent=v("wName")?"":(ok=false,"Enter your full name.");
  $("wEmailErr").textContent=okEmail(v("wEmail"))?"":(ok=false,"Enter a valid email address.");
  if(!ok)return;
  $("wSummary").innerHTML=`<p>I withdraw from my contract for: <b>${v("wItems")||"the whole order"}</b>.</p><p>Name: <b>${v("wName").replace(/</g,"&lt;")}</b><br>Email: <b>${v("wEmail").replace(/</g,"&lt;")}</b><br>Order: <b>${(v("wOrder")||"not given").replace(/</g,"&lt;")}</b>, ordered <b>${v("wDate")||"date not given"}</b></p>`;
  $("wStep1").hidden=true;$("wStep2").hidden=false;$("wSubmit").focus();
});
$("wBack").addEventListener("click",()=>{$("wStep2").hidden=true;$("wStep1").hidden=false});
$("wForm").addEventListener("submit",async e=>{
  e.preventDefault();$("wSubmit").disabled=true;$("wErr").textContent="";
  const ok=await sbInsert("withdrawals",{full_name:v("wName").slice(0,200),email:v("wEmail").slice(0,254),order_ref:v("wOrder").slice(0,100)||null,order_date:v("wDate")||null,items:v("wItems").slice(0,1000)||null});
  if(!ok){$("wSubmit").disabled=false;$("wErr").textContent="We couldn't send your withdrawal. Please try again, or email us — your withdrawal by email is just as valid.";return}
  const t=new Date();
  $("wReceipt").innerHTML=`We received your withdrawal on <b>${t.toLocaleDateString("en-GB",{day:"numeric",month:"long",year:"numeric"})}</b> at <b>${t.toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit"})}</b> (${Intl.DateTimeFormat().resolvedOptions().timeZone}). We'll confirm by email to ${v("wEmail").replace(/</g,"&lt;")} within 2 business days.`;
  $("wStep2").hidden=true;$("wDone").hidden=false;
});
</script>'''

SHIPPING = f'''{PRELAUNCH}
<h2>Where we ship</h2>
<p>We ship to all EU countries from Lithuania. We don't ship outside the EU yet. Because there are no customs borders inside the EU, you won't pay any import duties or extra taxes on delivery.</p>
<h2>Costs and delivery times</h2>
<div class="table-scroll"><table class="compare">
<thead><tr><th>Destination</th><th>Standard shipping</th><th>Typical delivery</th></tr></thead>
<tbody>
<tr><td>Lithuania, Latvia, Estonia</td><td>€4,95 · free from €49</td><td>1–3 business days</td></tr>
<tr><td>Poland, Finland, Germany, Nordics</td><td>€4,95 · free from €49</td><td>2–5 business days</td></tr>
<tr><td>Rest of the EU</td><td>€4,95 · free from €49</td><td>3–7 business days</td></tr>
</tbody></table></div>
<p>We dispatch orders within 1–2 business days. Delivery times are estimates from dispatch. You'll get a tracking link by email when your parcel leaves us.</p>
<h2>Address problems and returned parcels</h2>
<p>Please check your address and phone number at checkout. If a parcel comes back to us because the address was incomplete or it wasn't collected, we'll contact you and either reship it once you pay the new shipping cost, or refund the order minus the shipping costs we incurred.</p>
<h2>Lost or delayed parcels</h2>
<p>If tracking hasn't changed for 7 business days, or it shows "delivered" but you don't have it, email {C["email"]}. We'll open an investigation with the carrier and, if the parcel is lost, send a replacement or a full refund. Until goods reach you, the risk is ours.</p>
<h2>Payment</h2>
<p>When sales open, we'll accept cards (Visa, Mastercard, American Express), PayPal, Apple Pay, Google Pay and Klarna, all processed by licensed payment providers. Your payment is taken when you place the order. All prices are in euros and include VAT where applicable.</p>
<h2>Shipping outside the EU</h2>
<p>We plan to add the UK and the USA later. For the USA, all parcels are now subject to US import duties, so we will only ship there with duties and fees collected at checkout (DDP), so you don't get a bill on delivery.</p>'''

PRIVACY = f'''<h2>1. Who is responsible for your data</h2>
<p>The controller is the operator of Cutline identified in our <a href="legal.html">Legal Notice</a>. For any privacy question, email {C["email"]}. We have not appointed a data protection officer.</p>
<h2>2. What we collect and why</h2>
<div class="table-scroll"><table class="compare">
<thead><tr><th>Data</th><th>Purpose</th><th>Legal basis (GDPR)</th><th>Kept for</th></tr></thead>
<tbody>
<tr><td>Checkout: email, first and last name, country, chosen payment method, cart contents and total</td><td>Handle your pre-order request or order and contact you about it</td><td>Art. 6(1)(b), steps at your request before a contract</td><td>Pre-orders: until launch + 6 months, or until you ask us to delete. Orders: as long as tax and accounting law requires (up to 10 years)</td></tr>
<tr><td>Marketing email (only if you tick the box or sign up for the newsletter)</td><td>Send training tips and offers</td><td>Art. 6(1)(a), your consent, which you can withdraw any time</td><td>Until you unsubscribe</td></tr>
<tr><td>Usage analytics (only if you accept analytics cookies): a random browser ID, pages viewed, add-to-cart and checkout steps, referring site and campaign tags</td><td>Understand how many visitors are interested in our product and improve the shop</td><td>Art. 6(1)(a), consent</td><td>24 months</td></tr>
<tr><td>Withdrawal requests: name, email, order details</td><td>Process your withdrawal and keep proof</td><td>Art. 6(1)(c), legal obligation</td><td>3 years</td></tr>
<tr><td>Server logs (IP address, browser, time) kept by our host</td><td>Deliver the website securely</td><td>Art. 6(1)(f), legitimate interest in a secure website</td><td>Set by the host, typically a few days</td></tr>
</tbody></table></div>
<p>We never collect card numbers. Payments will be processed directly by payment providers under their own privacy terms. We don't sell your data and don't use it for automated decisions with legal effects.</p>
<h2>3. Cookies and browser storage</h2>
<p>We don't use advertising cookies. We store in your browser: your cart (needed for the shop to work, no consent required), your cookie choice, and, only if you accept analytics, a random ID that links your visits. You can change your choice any time under <a href="#" data-cookie-settings>Cookie settings</a>. If we later add advertising pixels (for example Meta or Google), we will ask for separate consent first and update this policy.</p>
<h2>4. Who processes data for us</h2>
<ul>
<li><b>Supabase</b> (Supabase Inc., USA): database for orders, pre-orders and analytics. Data is stored in the EU (Ireland).</li>
<li><b>GitHub Pages</b> (GitHub Inc., USA): website hosting.</li>
<li><b>Google Fonts</b> (Google Ireland Ltd.): delivers the fonts on our site; your browser connects to Google's servers.</li>
</ul>
<p>Where a provider is based outside the EU, transfers rely on the EU–US Data Privacy Framework or the European Commission's standard contractual clauses (GDPR Art. 45–46).</p>
<h2>5. Your rights</h2>
<p>You can ask us to access, correct or delete your data, restrict or object to its use, receive it in a portable format, and withdraw consent at any time without affecting earlier processing. Email {C["email"]}; we reply within one month. You can also complain to the Lithuanian State Data Protection Inspectorate (Valstybinė duomenų apsaugos inspekcija), L. Sapiegos g. 17, 10312 Vilnius, <a href="https://vdai.lrv.lt" rel="noopener">vdai.lrv.lt</a>, or to the authority in your own country.</p>
<h2>6. Children</h2>
<p>Our shop is not aimed at children. We don't knowingly collect data from anyone under 16.</p>
<h2>7. Changes</h2>
<p>We'll update this page when our processing changes and show the date at the top.</p>'''

SAFETY = f'''<p>Cutline gum is much harder than regular chewing gum. It is a training product: used correctly, it is safe for healthy adults. Please read these instructions before your first session.</p>
<h2>Who should not use it</h2>
<ul>
<li>Children under 14. Keep away from small children: risk of choking.</li>
<li>People with jaw-joint (TMJ) pain, clicking, locking or limited mouth opening.</li>
<li>People with loose teeth, loose fillings, crowns, veneers, bridges or implants, or recent dental work. Ultra Hard must not be used with any dental work.</li>
<li>People wearing braces or aligners.</li>
</ul>
<p>If you are unsure, ask your dentist or doctor before starting.</p>
<h2>How to use it safely</h2>
<ul>
<li>Limit training to 10–15 minutes, every other day. More chewing doesn't mean faster progress.</li>
<li>Warm the piece in your mouth first and bite down gradually. A cold, hard bite can crack the gum or strain your teeth.</li>
<li>Chew on your back molars, not your front teeth. Switch sides evenly.</li>
<li>Never swallow the gum.</li>
<li>Use a fresh piece for every session and throw it away afterwards. Don’t keep chewed gum for later.</li>
</ul>
<h2>Stop and seek advice if</h2>
<ul>
<li>You feel sharp pain in a tooth or the jaw joint.</li>
<li>Your jaw clicks, locks or aches the next day beyond normal muscle soreness.</li>
<li>You get headaches or ear pain after training.</li>
</ul>
<p>A muscle burn that fades within a day is normal. Pain is not.</p>
<h2>Ingredients and diet</h2>
<p>Hard and Ultra Hard contain polyol sweeteners. Excessive consumption may produce laxative effects. Full ingredients and nutrition values are on each product page and on the pack. Contact us if you have a specific allergy question before ordering.</p>
<h2>What to expect</h2>
<p>Hard gum trains your chewing muscles. How your jawline looks also depends on your body fat, genetics and bone structure. We don't promise any specific visual result, and the product is not intended to diagnose, treat or prevent any medical condition.</p>'''

LEGAL = f'''<h2>Operator</h2>
<p>Cutline is operated by:<br>{OPERATOR}<br>Email: {C["email"]}</p>
<p>Food business operator registration with the State Food and Veterinary Service (VMVT): [registration number, before sales start].</p>
<h2>Consumer disputes</h2>
<p>The EU Online Dispute Resolution platform closed on 20 July 2025. For disputes, contact us first; you can then turn to the Lithuanian State Consumer Rights Protection Authority (Valstybinė vartotojų teisių apsaugos tarnyba), Vilniaus g. 25, 01402 Vilnius, <a href="https://www.vvtat.lt" rel="noopener">www.vvtat.lt</a>. Its out-of-court procedure is free for consumers, and we take part in it.</p>
<h2>Website content</h2>
<p>We prepare the information on this website carefully, including the training guidance, but it is general information and not medical or dental advice. We are not responsible for the content of external websites we link to; when we learn that a linked page breaks the law, we remove the link.</p>
<h2>Copyright and trademarks</h2>
<p>Texts, graphics and the Cutline name and logo belong to the operator of Cutline unless marked otherwise. Some photos are used under the Unsplash licence. Please don't copy our content for commercial use without written permission.</p>'''

CSS_EXTRA = '''
<style>
.legal{max-width:820px;padding-block:40px 24px}
.legal h1{font-size:clamp(2.6rem,6vw,4rem);margin-top:10px}
.legal .updated{color:var(--muted);font-size:.85rem;margin-top:10px}
.legal-toc{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 8px}
.legal-toc a{font-size:.82rem;text-decoration:none;color:var(--ink);border:1px solid var(--line);background:var(--surface);padding:6px 10px;border-radius:999px}
.legal-toc a[aria-current="page"]{border-color:var(--accent);color:var(--accent-deep);font-weight:600}
.legal-body{display:grid;gap:14px;margin-top:20px}
.legal-body h2{font-size:1.6rem;margin-top:22px}
.legal-body p,.legal-body li{color:#2A302D;line-height:1.65;max-width:72ch}
.legal-body ul{margin:0;padding-left:20px;display:grid;gap:6px}
.legal-body .compare th,.legal-body .compare td{font-size:.88rem;vertical-align:top}
.legal-body .compare thead th{font-size:1rem}
.callout{background:#EEF1FF;border:1px solid #C9D1FB;border-radius:8px;padding:14px 16px;line-height:1.55}
.callout.ok{background:#E3F3EA;border-color:#BFE3CD;color:#14532D}
.formbox{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:18px;display:grid;gap:10px}
.wform{display:grid;gap:16px;margin-top:8px}
.wform .step{display:grid;gap:16px}
.f-grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.f-grid2 .full{grid-column:1/-1}
@media (max-width:560px){.f-grid2{grid-template-columns:1fr}}
.field{display:grid;gap:6px;min-width:0}
.field label{font-size:.85rem;font-weight:500}
.field input{font:inherit;padding:13px 14px;border:1.5px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink);width:100%}
.field input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(36,64,230,.15)}
.err{color:var(--bad);font-size:.82rem;min-height:1em}
</style>'''

BODIES = {"terms.html":("Policies",TERMS,""),"returns.html":("Policies",RETURNS,""),"withdraw.html":("Your 14-day right",WITHDRAW,WITHDRAW_JS),
          "shipping.html":("Policies",SHIPPING,""),"privacy.html":("Policies",PRIVACY,""),"safety.html":("Before you start",SAFETY,""),"legal.html":("Imprint",LEGAL,"")}
for f,title in PAGES:
    eyebrow,body,js = BODIES[f]
    page = shell(title,eyebrow,body,CSS_EXTRA,js).replace(f'<a href="{f}">',f'<a href="{f}" aria-current="page">',1)
    open(os.path.join(OUT,f),"w",encoding="utf-8").write(page)
    print("wrote",f)
