# Image credits

Every blog topic has its own photo, and no source photo is used by two topics. A topic's English, Spanish and
Portuguese articles share their photo. The build turns each source into WebP heroes (1200 and 640 px wide),
a 1200x630 JPEG share card per article and a 120 px search thumbnail. The data lives in `_build/lib/images.py`
(`VARIANTS`) and `_build/content/meta.py` (`TOPICS`), and `test_seo_and_discovery.py` (`TestBlogPhotos`)
enforces the rules below.

- **12 topics use Costa's own photos** (owner uploads on the Google Business Profile, or photos the owner sent).
  Their caption says "Photo taken at Costa's Meat Market…".
- **16 topics use licensed stock**, 15 from Pexels and 1 from Unsplash. Their caption credits the photographer
  and site ("Photo: Snappr / Pexels"), linked to the photo's page, and the article's schema carries `creator`,
  `creditText`, `license` and `acquireLicensePage`. Alt text describes only what's in the photo and never says it
  was taken at the store.
- **AI-generated images: none.**
- Source photos in `_build/photos/` are saved at most 2400 px wide, with camera metadata (including GPS) removed.

## The store's own photos (12 topics)

| Topic | Source file | What it shows | Where it came from |
|---|---|---|---|
| picanha | `costas-picanha-steaks-fat-cap.jpg` | Three raw picanha steaks with their thick fat cap, coarse salt and seasoning, at Costa's Meat Market | Business Profile, Jun 2025 |
| haines-city | `costas-storefront-webbs-town-center.webp` | Costa's Meat Market storefront in Webb's Town Center, 2169 Davenport Blvd, Davenport, FL | Sent by the owner (also on the Business Profile, Mar 2025) |
| coupons | `costas-storefront-sign-davenport-fl.jpg` | The Costa's Meat Market sign and front windows listing Brazilian products, the butcher counter, fresh bread and seasoned meats, in Davenport, FL | Business Profile, Mar 2025 |
| seasoned-meats | `costas-linguica-sandwich-at-the-counter.jpg` | A grilled linguiça sandwich with cheese and a green herb sauce on a cutting board at the Costa's Meat Market counter | Business Profile, Mar 2025 |
| cuts | `costas-meat-case.webp` | The butcher case at Costa's Meat Market in Davenport, FL, with ground beef, maminha, alcatra, ribs, steaks, house-made linguiça and seasoned cuts | Sent by the owner (also on the Business Profile, Mar 2025) |
| short-ribs | `costas-beef-rib-rack-costela.jpg` | A whole rack of beef ribs (costela), vacuum-sealed, on the counter at Costa's Meat Market | Business Profile, Mar 2025 |
| pao-de-queijo | `costas-pao-de-queijo-and-brazilian-coffee.jpg` | Pão de queijo (Brazilian cheese bread) next to bags of Brazilian coffee at Costa's Meat Market | Business Profile, Jun 2025 |
| brazilian-groceries | `costas-brazilian-coffee-and-sugar-shelves.jpg` | Shelves of Brazilian groceries at Costa's Meat Market, with Pilão coffee and União sugar | Business Profile, Mar 2025 |
| doneness | `costas-sliced-picanha-medium-rare.jpg` | Grilled picanha sliced on a cutting board, showing a pink center under the browned fat cap, at Costa's Meat Market | Business Profile, Mar 2025 |
| butcher-vs-grocery | `costas-butcher-slicing-stuffed-beef-roll.jpg` | A butcher in black gloves slicing a stuffed, rolled beef roast into pinwheels at Costa's Meat Market | Business Profile, Jun 2025 |
| bundles | `costas-beef-roast-with-stuffing-ingredients.jpg` | A seasoned raw beef roast with red onion, green onion, cheese, ham and spices on a cutting board at Costa's Meat Market | Business Profile, Mar 2025 |
| save | `costas-store-aisle-and-counter.jpg` | Inside Costa's Meat Market: the checkout counter, an aisle of Brazilian and Latin groceries, and the meat case at the back | Business Profile, Mar 2025 |

## Licensed stock photos (16 topics)

| Topic | Source file | What it shows | Photographer | Source | Licence |
|---|---|---|---|---|---|
| vacation | `burgers-on-backyard-gas-grill-pexels-8522789.jpg` | Burgers and buns on a gas grill in a backyard | RDNE Stock project | [Pexels](https://www.pexels.com/photo/cooking-burgers-on-the-grill-8522789/) | [Pexels License](https://www.pexels.com/license/) |
| per-person | `steaks-filling-a-grill-pexels-39452688.jpg` | An outdoor grill covered with thick ribeye steaks, enough for a crowd | Deane Bayas | [Pexels](https://www.pexels.com/photo/juicy-ribeye-steaks-grilling-outdoors-39452688/) | [Pexels License](https://www.pexels.com/license/) |
| churrasco-menu | `churrasco-skewers-with-farofa-pexels-9500281.jpg` | Grilled churrasco skewers of beef, chicken, sausage and cheese on a platter, with farofa, vinaigrette and dipping sauces | Gustavo Peres | [Pexels](https://www.pexels.com/photo/variety-of-grilled-meat-9500281/) | [Pexels License](https://www.pexels.com/license/) |
| oxtail | `braised-oxtail-pexels-27556975.jpg` | Braised oxtail in a dark, glossy sauce with fresh thyme, in a white bowl | Snappr | [Pexels](https://www.pexels.com/photo/traditional-caribbean-cuisine-27556975/) | [Pexels License](https://www.pexels.com/license/) |
| pot-roast | `pot-roast-with-carrots-and-potatoes-pexels-6545671.jpg` | Fork-tender pot roast with carrots and potatoes on a platter | Thiago Rebouças | [Pexels](https://www.pexels.com/photo/meat-and-fruit-on-plate-6545671/) | [Pexels License](https://www.pexels.com/license/) |
| filet-mignon | `grilled-filet-mignon-pexels-34433608.jpg` | A thick grilled filet mignon steak on a white plate with a side of sauce | Nadin Sh | [Pexels](https://www.pexels.com/photo/juicy-grilled-filet-mignon-on-white-plate-34433608/) | [Pexels License](https://www.pexels.com/license/) |
| prime-rib | `raw-bone-in-rib-roast-pexels-11898916.jpg` | A raw, well-marbled bone-in beef rib roast on a wooden board | Pits Riccardo | [Pexels](https://www.pexels.com/photo/raw-beef-on-table-11898916/) | [Pexels License](https://www.pexels.com/license/) |
| linguica | `sliced-linguica-unsplash-4pkdacqpzec.jpg` | Sliced linguiça (Brazilian pork sausage) browned on a cast-iron plate | Marlom Veloso | [Unsplash](https://unsplash.com/photos/4pkdacQPZec) | [Unsplash License](https://unsplash.com/license) |
| picadinho | `picadinho-with-rice-farofa-and-egg-pexels-32655177.jpg` | Picadinho, a diced beef stew with peas, served with white rice, farofa, beans and a fried egg | Daigoro Folz | [Pexels](https://www.pexels.com/photo/delicious-brazilian-feijoada-with-sides-32655177/) | [Pexels License](https://www.pexels.com/license/) |
| wings | `chicken-wings-on-skewers-over-charcoal-pexels-36798124.jpg` | Chicken wings grilling on skewers over hot charcoal | Mohamed Olwy | [Pexels](https://www.pexels.com/photo/delicious-grilled-chicken-skewers-over-charcoal-36798124/) | [Pexels License](https://www.pexels.com/license/) |
| feijoada | `feijoada-with-rice-and-collards-pexels-34195320.jpg` | Feijoada with sausage in a clay pot, served with white rice, collard greens, orange slices and farofa | José Roberto Oliveira | [Pexels](https://www.pexels.com/photo/traditional-brazilian-feijoada-with-sides-34195320/) | [Pexels License](https://www.pexels.com/license/) |
| pernil | `roast-pork-with-crackling-pexels-26733080.jpg` | A slow-roasted pork roast with crisp, crackling skin resting on a wire rack | Jonathan Borba | [Pexels](https://www.pexels.com/photo/roasting-meat-on-barbecue-26733080/) | [Pexels License](https://www.pexels.com/license/) |
| carne-asada | `carne-asada-and-tortillas-on-grill-pexels-8364557.jpg` | Thin steaks for carne asada grilling next to corn tortillas | ELIZABETH MIRANDA | [Pexels](https://www.pexels.com/photo/grilled-meat-and-flat-bread-on-black-grill-8364557/) | [Pexels License](https://www.pexels.com/license/) |
| steaks | `raw-strip-steaks-pexels-20187072.jpg` | Raw boneless strip steaks on a red cutting board | Boys in Bristol Photography | [Pexels](https://www.pexels.com/photo/meat-on-red-background-20187072/) | [Pexels License](https://www.pexels.com/license/) |
| pork-belly | `crispy-pork-belly-pexels-8408377.jpg` | Slices of crispy roasted pork belly with crackling skin | AMANDA LIM | [Pexels](https://www.pexels.com/photo/close-up-photo-of-a-dish-with-crispy-pork-skin-8408377/) | [Pexels License](https://www.pexels.com/license/) |
| cheap-cuts | `raw-ground-beef-pexels-128401.jpg` | Fresh raw ground beef in a glass bowl | Angele J | [Pexels](https://www.pexels.com/photo/grind-meat-in-glass-bowl-128401/) | [Pexels License](https://www.pexels.com/license/) |

**What the licences allow.** The [Pexels License](https://www.pexels.com/license/) and the
[Unsplash License](https://unsplash.com/license) both allow free commercial use, including cropping and editing,
with no attribution required (the site credits each photographer anyway). Neither allows selling unaltered copies,
implying the photographer endorses the business, or redistributing the photos as a stock collection. None of the
photos above shows another store's logo or an identifiable person's face. The Pexels titles of two photos don't
match what's in them: `delicious-brazilian-feijoada-with-sides-32655177` shows picadinho (diced beef stew with
rice, farofa, beans and an egg), and `meat-and-fruit-on-plate-6545671` shows pot roast. The alt text describes
the photo, not the title.

## Every owner photo on the Google Business Profile (reviewed October 12, 2026)

The "By owner" tab has 16 photos and 4 videos. Customer photos weren't used.

| # | Uploaded | Size | What it shows | Used for |
|---|---|---|---|---|
| 1 | Mar 2025 | 5712x3213 | Storefront from the parking lot, Costa's flag and Webb's Town Center sign | haines-city (same shot as the repo's `costas-storefront-webbs-town-center.webp`) |
| 3 | Mar 2025 | 6549x4912 | Raw beef roast with red onion, green onion, cheese, ham, crumbs and chili flakes | bundles |
| 4 | Mar 2025 | 5712x3213 | Inside: checkout counter, grocery aisle, meat case at the back | save |
| 5 | Mar 2025 | 1574x2048 | Grilled picanha, sliced, pink center | doneness |
| 6 | Mar 2025 | 5712x3213 | Storefront sign and windows (Brazilian products, butcher, fresh bread, seasoned meats) | coupons |
| 7 | Jun 2025 | 3478x2313 | Three raw picanha steaks with fat cap, coarse salt and a seasoning jar | picanha |
| 9 | Mar 2025 | 3840x2160 | Vacuum-sealed rack of beef ribs on the counter | short-ribs |
| 10 | Mar 2025 | 720x960 | Ground meat spread with cheese and parsley, being rolled | Not used: under 1000 px wide |
| 11 | Mar 2025 | 2048x1536 | The butcher case with labeled cuts and seasoned meats | cuts (same shot as the repo's `costas-meat-case.webp`) |
| 12 | Apr 2026 | 3024x4032 | Bags of white garri on a shelf | Not used: no matching topic |
| 13 | Apr 2026 | 4284x5712 | Bags of peanuts on a shelf | Not used: no matching topic |
| 15 | Mar 2025 | 2048x1536 | Grilled linguiça sandwich with cheese and green sauce at the counter | seasoned-meats |
| 16 | Mar 2025 | 3840x2160 | Shelves of Pilão coffee and União sugar | brazilian-groceries |
| 17 | Mar 2025 | 4032x2268 | A staff member at the counter with a Costa's mug | Not used: a portrait of an identifiable person. Good for an "About us" section with their OK |
| 18 | Jun 2025 | 2314x3477 | A butcher in black gloves slicing a stuffed beef roll | butcher-vs-grocery |
| 19 | Jun 2025 | 3480x2321 | Pão de queijo with bags of Brazilian coffee | pao-de-queijo |
| 2, 8, 14, 20 | Dec 2024 to Mar 2025 | | Videos | Not used: videos |

Instagram (@costasmeat) was checked too. Recent posts are designed graphics with text on top (several built on
stock imagery), plus reels, and Instagram serves at most 1080 px wide, so none were used.

## Weaker fits worth replacing with the store's own photos

These topics have a truthful photo, but a store photo would fit better. Take them at the counter (landscape, at
least 1600 px wide) and add them to the Business Profile; then swap the variant in `meta.py`.

- **bundles:** a family meat bundle laid out on the counter (the current photo shows a roast being prepped).
- **seasoned-meats:** the seasoned trays in the case, close up (the case photo is already used for the cuts guide).
- **linguica, wings, picadinho:** Costa's own linguiça, coxinha da asa and picadinho, raw in the case or cooked.
- **steaks, filet-mignon, prime-rib:** ribeye, NY strip, a whole tenderloin and a bone-in rib roast from the counter.
