# Mr Build landing page: project brief for coding agents

Read this file before you change anything. `docs/04-handoff.md` and `docs/01-research-brief.md` have more background.

## What this is
This is a concept company-profile landing page for **Mr Build**, a building supplies and hardware chain in Limpopo, South Africa. The page tells people who the company is and sends shoppers to the online store, **https://mrbuild-online.co.za**. It does not sell anything itself.

- It is a static multi-page site with no build step at runtime:
  - `public/index.html` (home), `services.html`, `branches.html`, `about.html`, `contact.html`
  - `public/css/site.css`: all styles. `public/js/site.js`: all behaviour. Pages must work without JS.
- **The HTML is generated.** Edit `tools/build.py`, then run `python3 tools/build.py public`. Do not hand-edit the pages; the next build overwrites them. Branch data (`BRANCHES`) and departments (`DEPTS`) live at the top of that file.
- Design v2 (Nov 2026) follows the client's feedback: bigger logo, Buddy everywhere, fewer words, brand logos as graphics, cartoon look, a store map, and the store-sign frame.
- The A1 renders in `docs/reference/` show the old v1 look and are kept only for history.

## Hard rules
1. **Keep the client's logo and colours.** Logos are `img/logo-red.svg` and `img/logo-white.svg`, taken from mrbuild.co.za.
2. **No AI-generated images.** Use the client's own photos (`img/store-*.jpg`) or free-licence photos.
3. **Collection only, no delivery.** Never write copy that offers delivery.
4. Use "**38 years**" for the company's age. The source is the client's Oct 2026 flyer.
5. Keep the black "Design concept" strip at the top until the client approves the page.
6. **Few words.** The client asked for more graphics and fewer words. Headlines of 2-4 words, one short line under them. No filler, no em dashes, no emoji.
7. **Do not describe The Builder as a sister brand, subsidiary or partner until the client confirms.** Only call its branches collection points.

## Design system (v2)
- **Colours:** only 4. `--red` #D9232A, `--yellow` #F3DD27, `--black` #111, `--white` #fff. No greys and no cream.
- **Type:** Lilita One (display, cartoon headings) and Barlow 500/600/700 (body).
- **Cartoon look:** 3px black outlines, hard offset shadows (`--sh`), dot halftone backgrounds (`.dots`), starburst stickers (`.burst`), speech bubbles (`.bubble`, `.l`, `.b`).
- **The sign frame ("slanted Flintstone"):** the client meant the steel sign structure on their stores: red posts with slanted crossbeams sticking out past the board. It is drawn in `img/frame.svg` and used by `.post`: a white `.board` on the frame, with Buddy beside it. Heading tags `.beam` are slanted bars (rotate -2.5deg). Section edges `.slant` and `.slant-r` are cut on an angle with `clip-path`.
- **Buddy** (`img/buddy.svg`) appears in every hero, How it works, the footer CTA, and as the map pins.
- **Department icons** are the mrbuild.co.za SVGs in `img/icons/`, drawn with CSS `mask-image` so they take any colour. `doors.svg` was drawn to match. Masks need http, so test with a local server, not file://.
- **Department tiles** (`.pylon`) copy the red pylon sign at the stores.
- **Brands** are logo tiles from `img/brands/`. White backgrounds were removed with a flood fill.
- **Map:** Leaflet 1.9.4 (cdnjs) with OpenStreetMap tiles. Store data comes from the `#store-data` JSON block. The store list next to the map works without JS. Keep the OSM attribution.

## Motion rules (Emil Kowalski's design-engineering principles)
- **Easing:** use the custom curves only: `--ease-out` `cubic-bezier(0.23,1,0.32,1)`, `--ease-in-out`, `--ease-drawer`. Never use `ease-in` on UI.
- **Properties:** animate only `transform` and `opacity` (plus colour on hover). Never use `transition: all`.
- **Pressable things:** add `:active { transform: scale(.97) }` at 160ms ease-out (cards use .985).
- **Hover:** wrap hover effects in `@media (hover:hover) and (pointer:fine)`.
- **Durations:** UI animation stays under 300ms. Exits are faster than entrances (the drawer opens in 280ms and closes in 180ms).
- **Scroll reveal:** `.rv` elements below the first screen fade up. Grid items stagger 60ms, capped at 8.
- **Buddy wave:** one short wave on Buddy in heroes. Off under reduced motion.
- **"38" count-up:** runs once, from 1, over about 1.1s.
- **Never animate from `scale(0)`.** Do not add animation to anything used often or triggered from the keyboard.
- **Reduced motion:** `prefers-reduced-motion` removes movement but keeps short fades. Keep that block up to date.

## Images
- Department tiles use the lifestyle photos from the client's current site (mrbuild.co.za `/assets/*.jpg`), cropped to 480x360 in `img/dept/`.
- Brands show as a ticker of stickers. Logos with a solid badge (see `BADGE` in `tools/build.py`) fill their sticker in the badge colour; the rest sit on white.

## Open items / TODO
- [x] 9th store is Mr Build Mankweng (from the client's flyer), added to `BRANCHES`.
- [ ] Mankweng: get the store email and the exact map pin. The pin is town-level for now.
- [ ] Is "Mr Build Wood" (signage in the client's drone photos) a store or a department?
- [ ] Real store photos: ask the client for their own Google Business Profile photos or new shots of each store. Photos uploaded to Google Maps by the public belong to those users, so don't copy them.
- [ ] Which branches are in `store-yard.jpg`, `store-front.jpg` and `store-pylon.jpg`? Alt text stays generic until we know.
- [ ] Check each branch's map pin with the client. Some are town-level, not the exact site.
- [ ] **Contact form backend.** The form has `data-concept="true"` and a `REPLACE_ME` Formspree URL. Wire it up and remove `data-concept`.
- [ ] Confirm per-branch hours (all branches use the same hours now).
- [ ] Wrapped doors: colours and lead times.
- [ ] Ask the client how Mr Build and The Builder are related.
- [ ] Re-check product counts before launch.
- [ ] When the real domain is known, change `BASE` in `tools/build.py`.

## Run locally
```
python3 -m http.server 8765 -d public
```
Use a server: the icon masks do not load from file://.

## Hosting: GitHub Pages
Live at https://vedalkendev.github.io/mrbuild-landing/

Pages builds from the **`gh-pages` branch** (root), which holds only the contents of `public/`. To deploy after committing to `main`:
```
git subtree split --prefix public -b gh-pages-tmp
git push -f origin gh-pages-tmp:gh-pages
git branch -D gh-pages-tmp
```
Keep `public/.nojekyll`. Never ask the user to paste a token into chat; if `gh auth status` fails, the user runs `gh auth login` in the browser.

All asset paths are relative (`img/...`, `css/...`), so the site works under the `/mrbuild-landing/` sub-path. Keep them relative.
The site is public, so the "Design concept" strip must stay until the client signs off.
