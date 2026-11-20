# Mr Build — Phase 1 research brief

Date: 20 Nov 2026 · Scope: company-profile landing page that links to the online store.

## The company (what we could verify)

- **Name / line:** Mr Build — "Your Building Buddy". Sister brand: **The Builder** ("He's Your Guy").
- **Branches (mrbuild.co.za):**
  | Branch | Address | Phone |
  |---|---|---|
  | Tzaneen | Cnr Danie Joubert & Claude Wheatley St | 015 004 0560 |
  | Louis Trichardt | Cnr Rissik & Grobler Straat | 015 004 0168 |
  | Musina | 6 Pat Harrison Rd | 015 004 1031 |
  | Giyani | Giyani-BA | 015 812 3786 |
  | Sibasa | 204 Makhado Rd | 015 963 3856 |
  | Thohoyandou | 90/91 B.A, next to Thulamela Municipality | 015 962 0444 |
  | The Builder Thohoyandou | Thohoyandou | 015 962 5545 |
  | The Builder Giyani | 6 First Rd, Giyani-BA | 015 004 0561 |
- **Hours:** Mon–Fri 07:30–13:30, 14:00–16:30 · Sat 07:30–12:30 · Sun closed.
- **Departments:** Building materials, Electrical, Plumbing, Tools, Paint, Wrapped doors, Cutting & edging, DIY.
- **Online store:** mrbuild-online.co.za (WooCommerce). **Collect-in-store only, no delivery.** Plumbing 1,235 products, Wood/Board 621 products.
- **Brands stocked (Oct 2026 promo):** Dulux, AfriSam, PG Bison, Sonae Arauco, JoJo, Bosch, Ingco, Tork Craft, Alcolin, Afrimat, Nutec, Yale, Ariston, Harvey Roofing, Lasher, Eureka, Safedor and others.
- **Socials:** Instagram @mrbuild_sa, Facebook (profile id 61551736583171).
- **Other facts (Cartrack case study, 2021):** about 200 staff, a fleet of 30–40 vehicles, board cutting and design packages, exclusive BILHAM décor range, retail and wholesale.

### Decisions (20 Nov 2026)
- **Age:** use **38 years** (from their Oct 2026 flyer). Ignore Cartrack's "2007".
- **Delivery:** **off.** Page says collection only, matching store policy.
- **Vector logo:** user will ask client. Raster 400px used until then.

## Brand (kept as-is, per brief)
| Token | Value | Source |
|---|---|---|
| Red | `#D9232A` (logo) / `#ED1C24` (web) | logo pixels, site CSS |
| Yellow | `#F3DD27` | mascot helmet, site `--primary` |
| Amber | `#EBAF2B` | mascot overalls |
| Ink | `#1A1919` | logo tagline, site CSS |
| Display | Aleo (slab) | site Google Fonts |
| UI / body | Barlow (+ Barlow Condensed for display) | site Google Fonts |

Logo: the only copies available are 400px raster. **We need a vector logo from the client** before final export.

## Competitors
| Who | What they lead with | Gap Mr Build can own |
|---|---|---|
| **Build it** (franchise, several Limpopo stores) | "Say yes" home-building simplicity, credit, rewards, store picker | Generic national voice, no local story |
| **Cashbuild** (Polokwane, Seshego, Baobab) | Huge catalogue, price-led, store locator | Catalogue-first, impersonal |
| **BUCO** | Trade accounts, departments, B2B dashboards | Contractor-heavy, cold for DIY |
| **New Builders Hardware** (4 Limpopo stores) | WhatsApp a store, quote list, popular searches (cement, IBR, lintel) | Closest local rival, but plain WooCommerce look |

**Takeaways for the page**
1. National chains look like catalogues. Mr Build's edge is **being local**: Vhembe and Mopani towns, named branches, real phone numbers, and a mascot people already know.
2. Every competitor's first job is "find my store". Branches and hours must sit high on the page.
3. In-store services (board cutting, edging, door wrapping) are rare in competitors' messaging. They're a strong reason to visit.
4. The online store should be clearly labelled **"order online, collect at your branch"** so nobody expects delivery.

## Page goal
A company profile that sends visitors to **mrbuild-online.co.za**. Main CTA: *Shop online*. Secondary: *Find your branch* / call.

## Imagery
Pexels (free licence), saved in `assets/`: SA construction crews (10202856, 5298215, 33656091), worker portrait (10682438), lumber yard (12278566, 12278574), bricklaying (19688828, 37422760), DIY maker (6790943), paint (3616759), warehouse aisle (4170172), timber stack (30285503). Instagram scraping needs a logged-in browser session, which isn't set up, so we used Pexels instead.
