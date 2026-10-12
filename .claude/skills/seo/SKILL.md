---
name: seo
description: Reusable SEO playbook for local-business and multilingual websites, distilled from the Costa's Meat Market site (elisbrown/costasmeatmarket-site). Use when starting, auditing or extending SEO on any site, including keyword research from Search Console, multilingual pages with hreflang, on-page templates, JSON-LD schema, social share cards, WebP images, sitemap/robots/llms.txt, weekly freshness via GitHub Actions, redirects from an old platform, GA4 + Microsoft Clarity tracking, Google Business Profile, social bios, blog content and instant site search.
---

# SEO playbook

Everything done on costasmeatmarket.com (October 2026), written so it can be repeated on another project.
`reference.md` in this folder has every step in detail, with templates, reasons and gotchas. The
reference implementation is the GitHub repo `elisbrown/costasmeatmarket-site`; file paths below are in that repo.

## How to use this on a new project

1. **Ask for the inputs first** (reference.md §0): Search Console export, Clarity/GA4 data, a Business
   Profile screenshot, real photos and logo, confirmed facts (hours, products, services, staff languages,
   payment), the host (Netlify, Vercel, Cloudflare, GitHub Pages), old-platform URLs, and the GA4 and Clarity IDs.
2. **Work through the phases in order.** Each phase is a checklist in reference.md:

| # | Phase | Done when |
|---|---|---|
| 1 | Keyword research from real query data | Keyword map: cluster × language × target page × priority, plus Search Console regex filters |
| 2 | Architecture: static generator, URL plan, link tokens | `python3 _build/build.py` builds everything; unknown internal links fail the build |
| 3 | Multilingual: every page in every language | Reciprocal hreflang + x-default, localized slugs, no auto-redirects |
| 4 | On-page template | Title, description, canonical, robots, H1, breadcrumb, contents list, FAQ, CTA, related posts, footer with address, phone and hours |
| 5 | Structured data | Business node with hours on every page; WebSite + SearchAction; BlogPosting, BreadcrumbList, FAQPage, Recipe |
| 6 | Share previews | Unique 1200×630 JPEG card per article per language; UTM-tagged share buttons |
| 7 | Images and speed | WebP only on pages, srcset, width/height, preloaded hero, lazy loading, real photos only |
| 8 | Discovery files | sitemap.xml (hreflang + images), robots.txt (AI crawlers allowed), llms.txt, llms-full.txt, RSS per language |
| 9 | Honest weekly freshness | GitHub Action rebuilds, tests, commits; articles keep their real dates |
| 10 | Migration redirects | Old URLs 301 to the closest page in the same language; `_redirects`, `vercel.json`, 404.html fallback |
| 11 | Tracking | GA4 + Clarity on every page; click, share and search events; UTM short links `/go/*` |
| 12 | Off-site local SEO | Owner playbook: Business Profile, Search Console, Apple, Bing, reviews |
| 13 | Social profiles | Keyword bios, `/go/` links, in-app search tips, posting plan |
| 14 | Content | Topics from real queries, every article in every language, subtle CTAs, only verified claims |
| 15 | Site search | Instant, accent- and typo-tolerant, cross-language, grouped results, tracked |
| 16 | QA | Unit tests gate every build; browser check on phone width, dark mode, no console errors |
| 17 | Hand-off | Plain-language owner playbook, ordered by impact, with ready-to-post drafts |

3. **Write the owner hand-off** (reference.md §17). Anything that needs a login (Business Profile, Search
   Console, social apps) goes in that playbook as exact steps and paste-ready text.

## Rules that hold on every project

- **Never invent facts.** Only claim products, services, hours, staff languages or prices the owner confirmed
  or the old site showed. For anything uncertain, write "call to check" or "special order", or leave it out.
- **Never fake freshness.** A page's lastmod and dateModified change only when its content changes. For a
  weekly signal, rotate real content (featured articles) on hub pages instead.
- **Never auto-redirect by language.** Offer a one-tap suggestion so crawlers can reach every language.
- **Schema must match what the page shows.** No self-serving review stars on the business's own site.
- **No AI-generated images.** Use the owner's photos, crops of them, or licensed stock.
- **Pages show WebP only.** Share cards stay JPEG and favicons stay ICO/PNG, because platforms require those.
- **GA4 and Clarity on every HTML page**, including 404, short links and hand-built pages, and a test that
  enforces it.
- **Tests gate the build and the weekly job.** If a test fails, nothing is published.
- **Don't publish or schedule social posts without the owner's go-ahead.** Draft them as ideas.
- **Keep the business name, address and phone identical** everywhere: site, schema, Business Profile,
  Apple, Bing, socials.

## Where the reusable code lives (reference repo)

| Piece | Path | Port by changing |
|---|---|---|
| Build entry point and page writers | `_build/build.py`, `_build/lib/pages.py`, `_build/lib/home.py` | Content and copy |
| Head, hreflang, analytics, footer, business schema | `_build/lib/site.py` | IDs, address, hours, `STORE_NODE` |
| Share cards, photo crops, image cache | `_build/lib/images.py` | Photos, `VARIANTS`, fonts |
| sitemap, robots, llms.txt | `_build/lib/pages.py` (`sitemap`), `_build/lib/discovery.py` | Business facts |
| Click, share and source tracking | `assets/js/track.js` | `GA4_ID`, link rules |
| Language memory and suggestion | `assets/js/lang.js` | Language list |
| Open-now badge | `assets/js/open-now.js` | Time zone |
| Site search | `assets/js/search.js`, `assets/css/search.css`, `_build/lib/search.py`, `_build/content/search_terms.py` | Products, synonyms, UI strings |
| Weekly refresh | `.github/workflows/weekly-refresh.yml` | Time zone, env var name |
| SEO test suite | `test_seo_and_discovery.py` | Site URL, IDs, counts |
| Owner playbook example | `Claude outputs/local-seo-and-social-playbook.md` | Everything |
