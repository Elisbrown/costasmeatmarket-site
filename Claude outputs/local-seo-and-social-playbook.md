# Costa's Meat Market: Local Search, Google Business & Social Playbook

*Prepared October 8, 2026. Covers the website changes on branch `claude/youthful-maxwell-nn6lg9` and the steps that have to happen inside Google, Apple, Bing and the social apps.*

---

## 0. Checklist, in order of impact

**Already done on the website** (goes live once the branch is merged and deployed):

- [x] Home page in **English (/), Spanish (/es/) and Portuguese (/pt/)**, with proper `hreflang` tags so Google shows each language to the right searchers. The old tags pointed Spanish and Portuguese at `/socials/`, which Google would have ignored.
- [x] Language switcher on every page. Visitors whose phone is set to Spanish or Portuguese get a one-tap "see this page in your language" link. Nothing redirects, so Google can crawl all three versions.
- [x] **Butcher's Blog**: 14 articles (8 English, 3 Spanish, 3 Portuguese), each written for a specific search (see section 1).
- [x] FAQ sections with FAQ schema on the home pages and every article. Google's AI answers on Maps (see 2.7) and ChatGPT/Perplexity both pull from content like this.
- [x] Tracking: every tap on call, directions, order online, WhatsApp, Instagram, TikTok, Facebook and "leave a review" is now logged in Microsoft Clarity, along with where the visitor came from. It also goes to Google Analytics 4 once you add an ID (section 4).
- [x] Tracked short links for bios and printed QR codes: `costasmeatmarket.com/go/ig`, `/go/tt`, `/go/fb`, `/go/wa`, `/go/qr`.
- [x] Sitemap, `llms.txt` and `llms-full.txt` updated; the social links in the business schema now include Instagram and TikTok.

**Your to-do list:**

1. [ ] Merge and deploy the branch.
2. [ ] Google Search Console: verify the site, submit the sitemap, request indexing (section 3).
3. [ ] Google Business Profile: categories, description, **hours**, products, tracked website link, photos (section 2).
4. [ ] Start asking every happy customer for a Google review (section 2.6). This is the single biggest local ranking factor you control.
5. [ ] Claim **Apple Business Connect** and **Bing Places** (section 2.8). The socials page already sends iPhone users to Apple Maps.
6. [ ] Update Instagram, TikTok and Facebook bios and links (section 5).
7. [ ] In Buffer, change the timezone from **Africa/Douala** to **America/New_York**. Otherwise scheduled posts go out at the wrong time for Florida.
8. [ ] Optional: create a Google Analytics 4 property and paste the ID into `assets/js/track.js` (section 4.2).
9. [ ] **Send me your opening hours.** I'll add them to the site's business schema. Hours are one of the facts Google checks between your website and your Business Profile.

---

## 1. Keyword map

I couldn't log into Search Console from this session, so this map comes from researching what Davenport-area customers search for. Search Console will show the real queries 4 to 6 weeks after the new pages are indexed. Use the regex filters in section 3.4 to check this map against them.

**Why these keywords:** in web search results, independent butcher shops barely appear for Davenport, so local competition is thin. The area also has three large groups of potential customers:

- **Vacation renters.** Davenport is about 10 miles from Walt Disney World, and the rental homes around ChampionsGate and Four Corners have grills.
- **Brazilians.** The Brazilian Consulate in Orlando estimated about 200,000 Brazilians in Central Florida in 2023.
- **Hispanic families.** About 56% of Osceola County residents are Hispanic or Latino (2020 Census).

| # | Cluster | English searches | Spanish | Portuguese | Page that targets it | Priority |
|---|---|---|---|---|---|---|
| 1 | Local "near me" | butcher shop Davenport FL, butcher near me, meat market Davenport FL, butcher near ChampionsGate / Four Corners / Haines City / Poinciana | carnicería en Davenport FL, carnicería cerca de mí, carnicería latina Kissimmee | açougue em Davenport, açougue perto de mim, açougue brasileiro na Flórida | `/`, `/es/`, `/pt/` + Google Business Profile | **High** (people ready to buy) |
| 2 | Picanha | picanha near me, where to buy picanha Davenport / Kissimmee / Orlando, what is picanha, picanha in English, top sirloin cap | qué es la picanha, picaña, tapa de cuadril | picanha nos EUA, picanha em inglês, onde comprar picanha na Flórida | `/blog/what-is-picanha/` + ES + PT versions | **High** |
| 3 | Vacation rentals | butcher near Disney vacation rentals, where to buy steaks near Disney, grilling at vacation rental, BBQ ChampionsGate rental | — | — | `/blog/vacation-rental-bbq-guide-davenport/` | **High** |
| 4 | Cut names | Brazilian meat cuts in English, skirt steak in Spanish, fraldinha in English | cortes de carne en inglés, arrachera en inglés, entraña en inglés | nomes dos cortes de carne em inglês, fraldinha em inglês, contrafilé em inglês | cut guides (EN/ES/PT) | Medium (draws newcomers to the area) |
| 5 | Party planning | how much meat per person BBQ, how much picanha for 10 people | cuánta carne por persona asado / parrillada | quanto de carne por pessoa churrasco | per-person guides (EN/ES/PT) | Medium |
| 6 | Steak choice | ribeye vs NY strip, picanha vs ribeye | — | — | `/blog/ribeye-vs-ny-strip-vs-picanha/` | Medium |
| 7 | Pork belly | torresmo recipe, pork belly in Portuguese, where to buy pork belly Davenport | chicharrón de panceta | torresmo, barriga de porco | `/blog/pork-belly-recipes-torresmo-panceta/` | Medium |
| 8 | Deals | meat specials Davenport, family meat bundles, meat packages Polk County | ofertas de carne | promoção de carne | `/blog/save-money-on-meat-davenport/` + Business Profile offers | Medium |
| 9 | Butcher vs grocery | butcher shop vs grocery store meat, is butcher meat better | — | — | `/blog/butcher-shop-vs-grocery-store-meat/` | Low (supports cluster 1) |

**Next articles to write**, timed for the season:

| Publish by | Topic | Language | Target search |
|---|---|---|---|
| Nov 1 | Holiday roasts: prime rib, tenderloin, how big to order | EN | prime rib Davenport FL, holiday roast order |
| Nov 15 | Pernil for Nochebuena: which shoulder and how much | ES | pernil para Nochebuena, cuánto pernil por persona |
| Nov 15 | Ceia de Natal: pernil, tender, costela | PT | pernil de Natal, ceia de Natal nos EUA |
| Dec 1 | Feijoada: which pork cuts to buy in the U.S. | PT + EN | cortes para feijoada nos EUA |
| Jan 15 | Game day: wings, ribs and sliders for a crowd | EN | wings for Super Bowl party, how many wings per person |
| Feb 1 | Carne asada: skirt vs. flank, and the marinade | ES + EN | mejor carne para carne asada |
| Mar 1 | Costela no bafo / beef ribs low and slow | PT | costela no bafo na churrasqueira a gás |
| Apr 1 | Bistec de palomilla at home | ES | bistec de palomilla receta |

---

## 2. Google Business Profile

### 2.1 Basics

- **Business name:** exactly `Costa's Meat Market`. Don't add keywords like "Butcher Davenport" to the name; Google suspends profiles for it.
- **Address and phone** must match the website character for character: `2169 Davenport Blvd, Davenport, FL 33837` · `(863) 422-2313`.
- **Primary category:** `Butcher shop`.
- **Secondary categories:** type "meat", "grocery", "Brazilian" and "Latin" into the category box and add only the ones that are true and that Google offers. You may see options such as *Grocery store* or a Brazilian or Latin American grocery category. Don't add a category for something you don't sell.
- **Hours + holiday hours:** fill them in, and update holiday hours before Thanksgiving, Christmas Eve (Nochebuena) and New Year's.
- **Service area:** Davenport, Haines City, ChampionsGate, Four Corners, Poinciana, Kissimmee.

### 2.2 Links (these make Google traffic trackable)

| Field | Paste this |
|---|---|
| Website | `https://costasmeatmarket.com/?utm_source=google&utm_medium=organic&utm_campaign=gbp` |
| Online ordering / Order ahead | `https://costasmeatmarket.hrpos.heartland.us/` |
| Social profiles | Instagram `instagram.com/costasmeat`, TikTok `tiktok.com/@costasmeat`, Facebook page, WhatsApp channel (if offered) |

### 2.3 Business description (747 of 750 characters)

> Costa's Meat Market is a full-service butcher shop and meat market at 2169 Davenport Blvd in Davenport, Florida. Our butchers cut fresh beef, pork and chicken to order, from picanha (top sirloin cap), ribeye and NY strip to skirt steak, short ribs, fresh ground chuck and pork belly. We specialize in Latin and Brazilian cuts: ask for your cut by the name you know from home and we'll help you find the closest match. Order online for pickup, pick up a family BBQ bundle, or join our WhatsApp VIP group for weekly specials and discount codes. We serve Davenport, Haines City, ChampionsGate, Four Corners, Poinciana and Kissimmee, plus visitors grilling at vacation homes near the parks. Our website is available in English, Spanish and Portuguese.

If your counter staff speak Spanish or Portuguese, say so here and turn on the matching attribute. It's a strong reason for people to choose you. I left it out because I couldn't confirm it.

### 2.4 Products (add each with a photo)

Put the Spanish and Portuguese names in each description so the profile matches searches in all three languages:

| Product | Description |
|---|---|
| Picanha | Whole top sirloin cap with the fat cap on (picaña · tapa de cuadril). Whole or cut into steaks for the skewer. |
| Ribeye | Hand-cut ribeye (ojo de bife · bife ancho), any thickness. |
| NY Strip | New York strip (bife de chorizo · contrafilé). |
| Churrasco / Skirt steak | Skirt steak (entraña · arrachera · churrasco) for the grill and carne asada. |
| Short ribs | Beef short ribs (costilla · costela), including cross-cut for asado de tira. |
| Fresh ground chuck | Ground fresh daily (carne molida · carne moída). |
| Pork belly | Pork belly (panceta · barriga de porco · toucinho), cut into strips or cubes on request. |
| Family BBQ bundle | Weekly combo of assorted cuts for families and weekend grillers. |
| Chicken | Whole chickens, wings and house-seasoned cuts. |

For each product's button, use "Order online" (Heartland link) or "Learn more" linked to the matching blog article with `?utm_source=google&utm_medium=organic&utm_campaign=gbp_product`.

### 2.5 Photos and weekly posts

- **Photos:** add 3 to 5 new photos every week: the storefront from the street (helps people find you), the counter, labeled cuts, the team, and finished dishes. Profiles with fresh photos get more direction requests.
- **Posts:** one or two a week. Rotate a weekly special (an "Offer" post), a fresh arrival, and a link to one of the articles. Ready-to-use drafts are in the appendix. Link posts with `?utm_source=google&utm_medium=organic&utm_campaign=gbp_post`.

### 2.6 Reviews

- Put a QR code at the counter and on receipts that points straight to your review link: `https://g.page/r/CVkkR-S3RMu7EBE/review`.
- Ask in person right after a good interaction: "Would you mind telling people what you bought today in a Google review?" Reviews that mention picanha, ribeye or "Brazilian cuts" help you rank for those words.
- Reply to every review within two days, in the reviewer's language.
- **Never offer a discount or gift in exchange for a review.** Google's policy prohibits incentivized reviews, removes them, and can penalize the profile. The FTC's 2024 consumer-review rule also bans incentives that depend on a review being positive. The 5% off for following your socials is fine; keep reviews out of it.

### 2.7 Q&A no longer exists, so do this instead

Google removed the Questions & Answers section from Business Profiles (announced December 2025). Its replacement, **Ask Maps**, is a Gemini-powered assistant that answers questions from your reviews, description, photos and website. That's why the new pages include FAQs about picanha, custom cuts, online ordering, deals and payment. Keep the description and hours accurate, and keep the reviews coming.

### 2.8 Other maps and listings (keep the name, address and phone identical everywhere)

- **Apple Business Connect** (businessconnect.apple.com): Apple Maps is the default on iPhones, and the socials page already opens Apple Maps for iPhone users. Website: `https://costasmeatmarket.com/?utm_source=apple&utm_medium=organic&utm_campaign=apple_maps`.
- **Bing Places** (bingplaces.com): can import directly from Google Business Profile. Bing powers Microsoft Copilot's local answers and is one of the sources other AI assistants draw on. Website: `?utm_source=bing&utm_medium=organic&utm_campaign=bing_places`.
- **Facebook page:** check that the address, phone, hours and "Butcher Shop" category are filled in.
- **Yelp** and **Nextdoor Business:** claim both free listings.
- A directory (iExit) already lists Costa's at the right address with 0 reviews. Nothing to do there, but it shows Google already knows the address.

---

## 3. Google Search Console

### 3.1 Set up

1. Go to search.google.com/search-console → **Add property**.
2. Choose **Domain** and enter `costasmeatmarket.com`. Google gives you a TXT record to add at your domain registrar. If that's a hassle, choose **URL prefix** instead and send me the HTML meta tag; I'll add it to the site.
3. **Sitemaps** → submit `https://costasmeatmarket.com/sitemap.xml`.
4. **URL Inspection** → paste each of these and click **Request indexing**: `/`, `/es/`, `/pt/`, `/blog/`, `/es/blog/`, `/pt/blog/`, `/blog/what-is-picanha/`, `/blog/vacation-rental-bbq-guide-davenport/`.
5. **Settings → Associations** → link to Google Analytics once you have a GA4 property.

### 3.2 Reports to watch

- **Performance → Search results:** queries, clicks, impressions and position.
- **Pages → Indexing:** confirm the new pages are indexed (usually takes 1 to 3 weeks).
- **Enhancements:** breadcrumbs and FAQ markup parse correctly. Since 2023 Google only shows FAQ rich results for government and health sites, but the markup still helps AI answers.

### 3.3 Monthly routine (about 15 minutes)

1. Performance → last 28 days → **Queries** tab → export.
2. For each cluster in section 1, log clicks, impressions and average position in a sheet.
3. Look for queries with impressions where your average position is **8 to 20**. Those are the quickest wins: tell me the query and the page, and I'll strengthen that page.
4. Compare **Countries** and **Search appearance** to see whether the Spanish and Portuguese pages are getting traffic.

### 3.4 Query filters (Performance → + New → Query → Custom (regex))

| Filter | Regex |
|---|---|
| Brand | `costa` |
| Picanha | `picanha\|picaña\|top sirloin cap` |
| Local intent | `davenport\|championsgate\|four corners\|haines\|poinciana\|kissimmee\|near me\|cerca\|perto` |
| Spanish | `carnicer\|carne\|cortes\|asado\|parrillada\|cu[aá]nta` |
| Portuguese | `a[cç]ougue\|churrasco\|cortes de carne\|quanto de carne\|fraldinha` |
| Vacation | `disney\|vacation\|rental\|villa\|resort` |

---

## 4. Tracking: how you'll know what's working

### 4.1 What's tracked now (Microsoft Clarity, already installed)

**Events** (Clarity → Dashboard → Smart events / Filters → Custom events):

| Event | Fires when someone taps… |
|---|---|
| `click_call` | any phone number |
| `click_directions` | Get directions (Google or Apple Maps) |
| `click_order_online` | the Heartland online store |
| `click_whatsapp_group` / `click_whatsapp_channel` | the WhatsApp group or channel |
| `click_instagram` / `click_tiktok` / `click_facebook` | a social profile |
| `click_google_review` | Leave a review |
| `click_blog` / `click_socials_hub` | an article or the socials page |
| `select_language` | the EN / ES / PT switch |

Sessions with a call, directions, order or WhatsApp-group tap are flagged for recording, so you can watch exactly how those customers used the site.

**Tags** (Clarity → Filters → Custom tags): `traffic_source` (for example `instagram / social`, `google / organic`, `qr_code / print`, `chatgpt / ai_assistant`), `utm_campaign`, `referrer`, `ai_assistant`, and `page_lang`. Combine them: "how many people from Instagram tapped Call?" or "do Spanish-page visitors ask for directions more?"

### 4.2 Google Analytics 4 (optional, recommended)

1. analytics.google.com → Admin → **Create property** → Web data stream for `costasmeatmarket.com`.
2. Copy the Measurement ID (`G-XXXXXXXXXX`) and paste it into `assets/js/track.js` on the line `var GA4_ID = "";`, or send it to me and I'll do it.
3. In GA4 → Admin → **Key events**, mark `click_call`, `click_directions`, `click_order_online` and `click_whatsapp_group` as key events.
4. Link GA4 with Search Console (3.1 step 5).

### 4.3 Links to use everywhere

| Where | Use this link | Shows up as |
|---|---|---|
| Instagram bio | `costasmeatmarket.com/go/ig` | instagram / social / bio_link |
| TikTok bio | `costasmeatmarket.com/go/tt` | tiktok / social / bio_link |
| Facebook page "Website" field | `costasmeatmarket.com/go/fb` | facebook / social / page_link |
| WhatsApp group description and shares | `costasmeatmarket.com/go/wa` | whatsapp / social / group_share |
| QR codes on counter signs, flyers, bags, receipts | `costasmeatmarket.com/go/qr` | qr_code / print / in_store |
| Google Business Profile | see 2.2 | google / organic / gbp |
| Apple / Bing | see 2.8 | apple or bing / organic |
| A specific post | add `?utm_source=facebook&utm_medium=social&utm_campaign=picanha_guide` to any page URL | facebook / social / picanha_guide |

Want a separate link for a partner, such as a vacation-rental manager's welcome book or a church bulletin? Ask me for a new `/go/` link so each partner's traffic shows up separately.

### 4.4 Monthly scorecard

| Source | Numbers to log |
|---|---|
| Google Business Profile → Performance | searches, profile views, calls, direction requests, website clicks |
| Search Console | clicks and impressions per keyword cluster (3.4) |
| Clarity | sessions by `traffic_source`; count of each `click_*` event |
| Google reviews | total count and average rating |
| WhatsApp | group members and channel followers |
| Heartland | online orders (compare with `click_order_online`) |

---

## 5. Social profiles

### 5.1 Bios (Instagram's Name field is searchable, so put the keyword there)

| Platform | Field | Text |
|---|---|---|
| Instagram | Name (42/64) | `Costa's Meat Market \| Butcher Davenport FL` |
| Instagram | Bio (135/150) | `🥩 Butcher shop · Davenport, FL` ↵ `Picanha · Latin & Brazilian cuts · BBQ bundles` ↵ `EN · ES · PT 🇺🇸🇲🇽🇧🇷` ↵ `📍2169 Davenport Blvd · Order online ↓` |
| Instagram | Link | `costasmeatmarket.com/go/ig` |
| TikTok | Bio (74/80) | `Butcher shop in Davenport, FL 🥩 Picanha, Latin & Brazilian cuts · EN/ES/PT` |
| TikTok | Link | `costasmeatmarket.com/go/tt` |
| Facebook | Intro (100/101) | `Butcher shop in Davenport, FL: picanha, Latin & Brazilian cuts, family BBQ bundles and weekly deals.` |
| Facebook | Website | `costasmeatmarket.com/go/fb` |
| Facebook | Category | Butcher Shop |

### 5.2 Getting found inside Instagram and TikTok

Both apps index what's **said** in the video, the **on-screen text** and the caption, not just hashtags. In each video:

- Say the place and the cut out loud: "Picanha, fresh at our butcher shop in Davenport, Florida."
- Put on-screen text like `Picanha in Davenport FL` or `Açougue em Davenport`.
- Use 3 to 5 hashtags, mixing location and product.

**Hashtag sets:**

- Local: `#DavenportFL #ChampionsGate #FourCornersFL #HainesCity #PolkCounty #KissimmeeFL #CentralFlorida`
- Product: `#picanha #butchershop #steak #churrasco #ribeye #bbq`
- Spanish: `#carniceria #asado #carneasada #parrillada`
- Portuguese: `#acougue #churrasco #brasileirosnaflorida #brasileirosemorlando`
- Visitors: `#vacationrental #disneyvacation #orlandovacation`

### 5.3 What to post (3 to 5 times a week)

1. **Cut of the week:** show the cut and say its name in English, Spanish and Portuguese (straight from the cut guide).
2. **"How much for your party?":** a 15-second clip from the per-person table.
3. **Vacation renters** (Friday to Sunday, when new guests check in): "Staying near Disney? Grill tonight."
4. **Fresh arrivals and WhatsApp drops:** "Picanha just came in. VIP group got the code first."
5. **Recipes:** picanha on the skewer, torresmo, five-minute chimichurri.
6. **Behind the counter:** the butchers, the regulars (with their permission).

End captions with "Order online, link in bio." On Facebook, paste the article URL with a UTM tag.

### 5.4 Partnerships that bring traffic you can track

- **Vacation rental managers and hosts** around ChampionsGate, Four Corners and Solterra: offer a "grill night" flyer for their welcome books with a QR code. Give each manager their own `/go/` link.
- **Brazilian and Latin community groups, churches and Facebook groups** (for example "Brasileiros em Orlando"): share the Portuguese and Spanish guides where the group rules allow.
- **Local sports leagues and schools:** bundle deals for team cookouts.

### 5.5 Buffer

Buffer is connected to Instagram (@costasmeat), TikTok (@costasmeat) and the Facebook page. Two things to know:

- The account timezone is **Africa/Douala**. Change it to **America/New_York** before scheduling anything.
- The free plan allows 3 channels (all used) and 10 scheduled posts, so Google Business Profile posts have to be done in the Google app or website unless you upgrade.

---

## 6. What I couldn't do from this session, and why

- **Log into Search Console, Business Profile or the social apps:** this cloud session has no browser. To let me click through those dashboards next time, start a session from the Claude desktop app with Claude in Chrome enabled.
- **Search volumes:** Search Console has no data until the pages are indexed, and I had no keyword tool connected. The map in section 1 is based on research into local demand and competition.
- **Opening hours:** they aren't on the current site. Send them and I'll add them to the schema.
- **Facts to double-check:** the articles only state things the existing site already says: picanha, ribeye, NY strip, skirt, short ribs, ground chuck, pork belly, whole chickens, wings, house-seasoned cuts, family bundles, custom cuts, online ordering, WhatsApp deals, 5% off for following, and cash/credit/debit. If any of these has changed, tell me and I'll update the pages.

---

## Appendix: ready-to-post drafts

**Google Business Profile post (EN, "Update", link: picanha guide + `?utm_source=google&utm_medium=organic&utm_campaign=gbp_post`)**
> Picanha, the top sirloin cap Brazilian steakhouses are famous for, is hard to find whole at the supermarket. We cut it the Brazilian way, fat cap on, whole or ready for the skewer. Read our guide to choosing and grilling it, or order online for pickup.

**Google Business Profile post (EN, "Offer")**
> Follow and engage with us on Instagram, TikTok and Facebook and get 5% off your next purchase. Just show us at the counter. One coupon per customer.

**Google Business Profile post (ES, link: `/es/blog/guia-de-cortes-latinos/`)**
> ¿Entraña, arrachera o vacío? Pide tu corte con el nombre que conoces y te ayudamos a encontrar el equivalente. Mira nuestra guía de cortes latinos en inglés.

**Google Business Profile post (PT, link: `/pt/blog/quanto-de-carne-por-pessoa-churrasco/`)**
> Quanto de carne por pessoa no churrasco? A conta do açougueiro, já em libras: de ¾ a 1 libra por adulto. Veja a tabela completa para 10, 20 e 30 pessoas e encomende com antecedência.

Social captions for Instagram, TikTok and Facebook are saved as **Ideas in Buffer**, ready to schedule once the pages are live.
