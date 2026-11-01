# Jaw training gum project (working brand: Cutline)

Hard chewing gum for jaw/masseter training, sold by a Lithuanian operator (see private notes).
Same factory and formulation as Jawliner's hard gums. Reference competitor: https://jawliner.com/

Last updated: 2026-10-31

## Files

| File | What's in it |
|---|---|
| `website/index.html` | MVP storefront draft, version 1 (grey B&W portrait hero) |
| `website/index-v2.html` | Version 2: ivory background, colour hero (`website/hero_01.png`) |
| `docs/01-product-analysis.md` | Jawliner hard gum: line-up, prices, formulation, protocol, claims, funnel |
| `docs/02-market-analysis.md` | Market size, competitors and prices, demand drivers, scientific evidence |
| `docs/03-compliance-checklist.md` | EU/LT launch requirements and claims to avoid |
| `docs/04-factory-questions.md` | Open questions for the manufacturer before launch |
| `docs/05-image-credits.md` | Sources and licence of the draft photos |
| `docs/06-website-spec.md` | Page structure, pricing used in the draft, placeholders to fill |

## Status

- [x] Competitor and market research
- [x] MVP website draft (static HTML, checkout not wired)
- [ ] Factory spec sheet (weights, piece count, hardness test, allergens, polyol %)
- [ ] Trademark check on brand name ("Cutline" is a placeholder)
- [ ] VMVT food business registration
- [ ] Own product photography / packaging
- [ ] Shopify (or similar) build with real checkout

## Supabase

Project ref `vzfwovxlzgrtghxlfkbj`. The Supabase MCP server is configured in `.mcp.json` (project scope).
To connect from Claude Code on your machine, in a regular terminal inside this repo:

```
claude /mcp          # select "supabase" -> Authenticate
npx skills add supabase/agent-skills   # optional
```

Secrets (tokens, DB password) live outside the repo in `Jawliner/Secrets/` and are git-ignored. Never commit them.
