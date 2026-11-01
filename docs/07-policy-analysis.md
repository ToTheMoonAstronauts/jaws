# Policy analysis: Jawliner vs Cutline

Reviewed 2026-11-01. Not legal advice: have a Lithuanian lawyer check the final texts before real sales.

## What Jawliner has (MEG GmbH, Germany)

| Page | What it contains | Weak spots |
|---|---|---|
| Terms of Service | German AGB, 17 sections: contract formed by order confirmation, prices incl. VAT, payment methods, delivery, retention of title, withdrawal by reference, warranty, liability tiers, health disclaimer, ODR link, German law | Withdrawal period not stated in the terms; garbled CISG clause; no subscription terms although they sell auto-renewing supplies; English site, German-only terms |
| Return & Refund | Standard German withdrawal notice: 14 days, customer pays return shipping, refund within 14 days incl. standard delivery | No hygiene exception stated here (but FAQ says opened gum can't be returned); no damaged/wrong item process |
| Safety Instructions | On product pages: not under 14, stop if pain, consult a doctor with jaw problems, "you accept full responsibility" | Blanket liability waiver is unenforceable against EU consumers |
| Privacy | Long generic German template: Dropbox, Zendesk, WhatsApp, Google Ads, social media | Still cites Privacy Shield (invalid since 2020); doesn't name Shopify, Klarna, Meta pixel; no supervisory authority named |
| Shipping & Payment | Price table by country, free shipping from €59/€79, USA via DDP €14.95, €10/€20 fee for undeliverable parcels | Doesn't say when payment is taken; no lost-parcel process |
| Legal notice | Impressum: MEG GmbH, HRB 12113 Kempten, VAT DE310927505, managing directors, content/link/copyright disclaimers | Still links the EU ODR platform (closed 20 July 2025) |
| Revoke Order | Page exists but no form content found | Does not yet meet the 2026 withdrawal-button rules |

## Rules that apply to us (Lithuanian seller)

**EU / Lithuania, B2C online sales**
- Consumer Rights Directive (2011/83/EU) as implemented in the Lithuanian Civil Code: pre-contract information, 14-day withdrawal, model form, refund within 14 days, delivery within 30 days unless agreed.
- **Withdrawal button (Directive 2023/2673), from 19 June 2026**: every online shop must offer an always-available "withdraw from contract here" function, with a two-step confirmation and an automatic receipt on a durable medium (email). Jawliner doesn't have this yet; we built it (`withdraw.html`).
- Hygiene exception: sealed goods "unsuitable for return for health or hygiene reasons" lose the withdrawal right **only once unsealed**. Gum qualifies.
- Legal guarantee (conformity): 2 years in the EU. For gum we can state its best-before date, but we can't shorten the legal guarantee for consumers.
- **ODR platform closed** on 20 July 2025 (Reg. 2024/3228). Don't link it. Instead name the national ADR body: **Valstybinė vartotojų teisių apsaugos tarnyba (VVTAT)**, Vilniaus g. 25, Vilnius, vvtat.lt. Free for consumers.
- Omnibus Directive: "was" prices = lowest price in the last 30 days; say how reviews are verified.
- Food Information Regulation 1169/2011: ingredients, allergens, nutrition, net weight, operator, "with sweeteners" and the polyol laxative warning must be shown **before purchase** on the product page (done).
- Language: product and contract information for Lithuanian consumers must be available in Lithuanian. Translate before marketing in LT.
- GDPR + ePrivacy: analytics IDs in browser storage need **consent** (only the cart is "strictly necessary"). Supervisory authority: **Valstybinė duomenų apsaugos inspekcija (VDAI)**, ada.lt.
- Consumers keep the protection of their own country's mandatory law even if Lithuanian law is chosen (Rome I, Art. 6).
- European Accessibility Act (since June 2025): micro-enterprises (<10 staff and <€2M turnover) are exempt for services; aim for accessible pages anyway.

**Selling to the USA (later)**
- US de minimis is gone: suspended for all countries since 29 Aug 2025, codified in 2026, and ended by statute from 1 July 2027. Every parcel is dutiable and needs customs entry; postal shipments need a qualified party paying duties. Ship **DDP** (duties collected at checkout) or customers get surprise bills.
- Food imports: FDA **Prior Notice** for every food shipment (including mail), FDA food facility registration of the manufacturer, US-style Nutrition Facts label in English. California Prop 65 may apply.
- Advertising: FTC rules on endorsements and reviews (fake reviews banned since 2024), and substantiation for any "builds muscle" claim.
- Privacy: state privacy laws mostly apply above size thresholds we won't hit; still honour opt-outs and don't sell data.
- **Recommendation:** EU-only during the test. Add the US later via a DDP-capable carrier (e.g. DHL Express or a 3PL) after FDA steps.

## Our pages (website/)

| Page | File |
|---|---|
| Terms of Service (incl. pre-launch clause) | terms.html |
| Returns & Refunds | returns.html |
| Withdraw from contract (2026 button, 2-step) | withdraw.html |
| Shipping & Payment | shipping.html |
| Privacy & Cookies | privacy.html |
| Safety Instructions | safety.html |
| Legal Notice | legal.html |

## Open items before real sales
- Fill company code, VAT number, registered address, contact email (placeholders in brackets).
- Automatic withdrawal receipt by email (needs an email service, e.g. Resend or Postmark via a Supabase function).
- Self-host the Google Fonts (German courts have fined sites for sending visitor IPs to Google Fonts).
- Lithuanian translation of all legal pages.
- Lawyer review; product liability insurance; VMVT food business registration.
