# Website spec (MVP draft)

File: `website/index.html` (static, single page, no build step).

## Page structure
1. Draft banner (remove before launch) + announcement bar
2. Sticky nav: Shop, How to train, Results, Ingredients, FAQ, Cart
3. Hero: "Train the masseter. Every other day." + portrait + pack
4. Why regular gum does nothing: resistance gauge (multipliers pending factory data)
5. Shop: Hard / Ultra Hard tabs, flavours, 1/3/6 packs with €/kg, add to cart (demo)
6. Lifestyle strip: commute, between sets, desk, rest day
7. Band: Load. Rest. Repeat.
8. Session: 6-step protocol + working 3/2/3-minute timer (3 rounds)
9. Results, honestly: bite strength / body fat / bone shape + study summaries
10. Ingredients and nutrition + polyol warning
11. Safety: who shouldn't chew it
12. Reviews: empty state (real, order-linked reviews only)
13. FAQ (8 questions)
14. Footer: brand only, legal links, photo note

## Draft pricing
| Pack | Price | Hard €/kg (116 g) | Ultra €/kg (100 g) |
|---|---|---|---|
| 1 pack (~2 months) | €19.95 | €171.98 | €199.50 |
| 3 packs (~6 months) | €34.95 | €100.43 | €116.50 |
| 6 packs (~12 months) | €59.95 | €86.14 | €99.92 |

Jawliner reference: 1 pack €24.95, 3 packs €39.95.

## Flavours in draft
- Hard: Mint, Mango, Watermelon, Blueberry
- Ultra Hard: Blueberry Ice, Cherry Ice, Mint, Ginger Lime

## Placeholders to fill (amber tags)
- Free shipping threshold, hardness multipliers, polyols/fat/protein/salt, allergens
- Pieces per pack, reuse count, return shipping policy
- Company code, VAT, address, VMVT registration, minimum age, trademark check

## Next build steps
- Port to Shopify theme (or Next.js + Stripe), wire checkout
- Real packshots and UGC
- Lithuanian + other language versions
- Legal pages, cookie banner, analytics with consent

## Update 2026-10-31: above the fold (Jawliner-style)
- Full-width photo hero: portrait on the right blending into a light-grey studio background, headline left.
- Headline A (default): "Hard gum for a stronger jaw" + "Chewing gum built to resist your bite. Train your jaw muscles in 10–15 minutes, every other day."
- Headline B: "Train the masseter. Every other day." Switch with the A/B link in the draft banner, or open index.html#b.
- Star row with placeholder: show a real rating only once verified reviews exist (no invented numbers).
- CTAs: "Shop hard gum" + "How it works".
- Scrolling trust ticker under the hero (sugar-free & vegan, ships from LT, free EU shipping threshold, 2 levels, reusable, 14-day returns).
- Two product tiles (Hard / Ultra Hard, from €19,95) directly below; clicking preselects that level in the shop.
- New image: images/hero-square.jpg (Unsplash photo-1768742466927-42153b867e8b, square crop).

## Version 2 (2026-10-31): website/index-v2.html
- Same page as version 1, but page background ivory (#FBF8F1), cards white, lines warm beige; fonts and colours unchanged.
- Hero uses the user's own image website/hero_01.png (man putting gum in mouth), full colour, on the right half, fading softly into the ivory panel; headline left.
- Mobile: photo on top (4:3), headline below.
- Version 1 (website/index.html) keeps the grey B&W portrait hero for comparison. The draft banner on v2 links back to v1.
