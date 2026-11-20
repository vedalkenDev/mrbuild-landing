# Mr Build landing page: project brief for coding agents

Read this file before you change anything. `docs/04-handoff.md` and `docs/01-research-brief.md` have more background.

## What this is
This is a concept company-profile landing page for **Mr Build**, a building supplies and hardware chain in Limpopo, South Africa. The page tells people who the company is and sends shoppers to the online store, **https://mrbuild-online.co.za**. It does not sell anything itself.

- It is a static site: `public/index.html` holds the HTML, the inline CSS and the inline JS, with no build step. Photos are in `public/img/`.
- The approved design is direction "A1 · Yard Bold". Full-page reference renders are in `docs/reference/A1-desktop-final.jpg` and `docs/reference/A1-mobile.jpg`.
- The source design lives in the Figcraft file `mrbuild.figcraft`, which stays with the designer and is not in this repo.

## Hard rules
1. **Keep the client's logo and colours.** Do not restyle the brand.
2. **No AI-generated images.** Use Pexels or other free-licence photos, or the client's own photos. All photos are placeholders until the client sends real ones.
3. **Collection only, no delivery.** Never write copy that offers delivery.
4. Use "**38 years**" for the company's age.
5. Keep the yellow "Design concept" strip at the top until the client approves the page.
6. Watch for AI-looking copy and design after every change:
   - no filler words ("seamless", "elevate", "one-stop shop")
   - no em-dash asides
   - no emoji section markers
   - no "01 / 02 / 03" numbering on content that isn't a real sequence
   - no generic gradient heroes
   Write plainly, the way staff at a Limpopo hardware store would talk.

## Brand tokens (already in `:root`)
| Token | Hex | Use |
|---|---|---|
| `--red` | #D9232A | Brand red: fact strip, story band, nav button, phone numbers |
| `--yellow` | #F3DD27 | Brand yellow: main CTAs, highlights, the Electrical card |
| `--ink` | #1A1919 | Text, dark bands |
| `--ink-2` | #111010 | Footer |
| `--cream` | #F6F3EC | Page background |
| `--paper` | #FFFDF6 | Cutting-list slip |
| greys | #4A4744 #6B6762 #A8A39C #D9D6D0 #E8E5DF | Secondary text, rules |

**Type** (Google Fonts):
- Barlow Condensed 700/800/900 for headings, always uppercase.
- Barlow 400–700 for body text.
- Aleo 700 for the story heading only.

The page commits to one light look on purpose. Do not add dark mode.

## Page order
Each section's `id` is in brackets.

1. Concept strip
2. Sticky nav (`#top`): logo, links and the red "Shop online" button. On mobile, a hamburger opens a drawer.
3. Hero: kicker listing the towns, "BUILDING LIMPOPO FOR 38 YEARS.", sub-line, a yellow shop CTA and a ghost "Find your branch" button.
4. Red fact strip with 4 facts.
5. Shop by department (`#departments`), a mosaic:
   - Hardware, the big card, 5,643 products
   - Plumbing, 1,235
   - Paint, 962
   - Electrical, 819 (the yellow card)
   - Wood & board, 621
   - Building materials, 292, as a full-width strip with "See all 9,572 products"
   - The counts were read from the store on 20 Nov 2026.
6. Cut to size while you wait (`#cutting`): ink band with a tilted paper cutting-list slip.
7. Eight branches (`#branches`), with the opening hours:
   - Vhembe (5 branches) and Mopani (3 branches)
   - Phone numbers right-aligned
   - Yellow "Ordered online?" collect box
8. Story (`#story`, red band): a big "38", "From Musina to Tzaneen.", and the brands list (`#brands`).
9. Footer: "Order online. Collect in Limpopo." CTA, then the logo and the Shop / Company / Follow columns.

## Breakpoints
- **980px and below:** the nav links collapse into the hamburger; the department mosaic becomes 2 columns with Hardware full width; the cutting, branches and story sections stack.
- **640px and below:** buttons go full width; the fact strip becomes a 2×2 grid; type gets smaller.
- Every band uses `.band` with the gutter `max(16px, env(safe-area-inset-*))`. Keep it.

## Motion rules (Emil Kowalski's design-engineering principles)
- **Easing:** use the custom curves only: `--ease-out` `cubic-bezier(0.23,1,0.32,1)`, `--ease-in-out`, `--ease-drawer`. Never use `ease-in` on UI.
- **Properties:** animate only `transform` and `opacity` (plus colour on hover). Never use `transition: all`.
- **Pressable things:** add `:active { transform: scale(.97) }` at 160ms ease-out (cards use .985).
- **Hover:** wrap hover effects in `@media (hover:hover) and (pointer:fine)`.
- **Durations:** UI animation stays under 300ms. Exits are faster than entrances (the drawer opens in 280ms and closes in 180ms).
- **Hero load sequence:** this is the one orchestrated moment. Headline lines rise out of `overflow:hidden` masks, staggered 70ms, then the sub-line and CTAs fade up, staggered 60ms. The photo settles from scale 1.07.
- **Scroll reveal:** only elements *below the first screen at load* get `.pending`, so the page is complete without scrolling. Department cards stagger 60ms.
- **Cutting slip:** drops in with a slight overshoot, then its lines stagger in 70ms apart.
- **"38" count-up:** runs once, from 1, over about 1.1s.
- **Never animate from `scale(0)`.** Do not add animation to anything used often or triggered from the keyboard.
- **Reduced motion:** `prefers-reduced-motion` removes movement but keeps short fades. Keep that block up to date.

## Open items / TODO
- [ ] Department cards all link to the store home page. Swap in the real category URLs from mrbuild-online.co.za.
- [ ] The Facebook link is a placeholder. Get the real page URL from the client.
- [ ] Swap `img/logo.png` (raster, 400×133) for the vector logo when the client sends it.
- [ ] Replace the Pexels photos (`hero`, `hardware`, `plumbing`, `paint`, `wood`, `building`) with the client's own photos.
- [ ] Confirm the branch phone numbers, addresses and hours with the client.
- [ ] Re-check the product counts before launch, since they drift.
- [ ] Optional: add SEO meta tags, Open Graph tags and LocalBusiness JSON-LD for each branch.
- [ ] Optional: deploy `public/` to Netlify, Vercel or Cloudflare Pages.

## Run locally
```
npx serve public
```
Opening `public/index.html` directly in a browser also works.

## Hosting: GitHub Pages
The site deploys from `public/` through GitHub Actions (`.github/workflows/pages.yml`) on every push to `main`.

First-time setup, done with the GitHub CLI (`gh`):
1. `gh auth status`. If you are not logged in, run `gh auth login` (GitHub.com, HTTPS, log in with a browser). The user completes this step in the browser. Never ask the user to paste a token into chat.
2. `git init -b main && git add -A && git commit -m "Initial commit: Mr Build landing page concept"`
3. `gh repo create mrbuild-landing --public --source=. --remote=origin --push`
   Pages on a private repo needs a paid GitHub plan, so the repo is public.
4. Turn on Pages with Actions as the source:
   `gh api -X POST repos/{owner}/mrbuild-landing/pages -f build_type=workflow`
   If Pages is already on, use `-X PUT` instead.
5. Watch the deploy with `gh run watch`, then print the URL:
   `gh api repos/{owner}/mrbuild-landing/pages --jq .html_url`
   The URL looks like `https://<username>.github.io/mrbuild-landing/`.

All asset paths are relative (`img/...`), so the site works under the `/mrbuild-landing/` sub-path. Keep them relative.
The site is public, so the yellow "Design concept" strip must stay until the client signs off.
