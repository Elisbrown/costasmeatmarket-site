"""llms.txt, llms-full.txt and robots.txt, regenerated from the article list on every build."""
from lib.site import SITE, ORDER, MAPS, HOME, BLOG, FEED, LANGS, BUILD_DATE
from content.meta import KINDS

LANG_HEAD = {"en": "English", "es": "Español", "pt": "Português"}


def llms_txt(posts):
    from lib.home import featured_groups
    featured = featured_groups()
    lines = [
        "# Costa's Meat Market",
        "",
        "> Davenport, Florida's neighborhood butcher shop, fresh meat market, and Brazilian and Latin specialty "
        "grocery, near Haines City and ChampionsGate. Real butchers, custom fresh cuts, picanha, house-seasoned "
        "meats, family bundles, weekly specials, and authentic Latin & Brazilian cuts.",
        "",
        "## Business Details",
        "- **Name**: Costa's Meat Market",
        "- **Type**: Butcher Shop, Meat Market, Grocery Store",
        "- **Address**: 2169 Davenport Blvd, Davenport, FL 33837, United States (Webb's Town Center)",
        "- **Phone**: +1 (863) 422-2313",
        f"- **Primary Website**: {SITE}/",
        f"- **Online Ordering**: {ORDER}",
        f"- **Social Links & Community**: {SITE}/socials/",
        "- **Facebook**: https://www.facebook.com/share/1BqfQyWrdy/",
        "- **Instagram**: @costasmeat",
        "- **TikTok**: @costasmeat",
        "",
        "## Offerings & Specialties",
        "- **Fresh Custom Meat Cuts**: Hand-trimmed beef, pork, poultry, and specialty meats by experienced butchers.",
        "- **Picanha & Specialty Cuts**: Picanha, maminha, alcatra, coxão mole, costela, ribeye, NY strip, and other "
        "Latin and Brazilian favorites.",
        "- **Ready-to-Cook Seasoned Meats**: House-made linguiça, seasoned picadinho, marinated pork, and seasoned "
        "chicken wings.",
        "- **Family Meat Bundles**: Cost-saving combo packages with assorted cuts for family meals and barbecues.",
        "- **Weekly Specials & Coupons**: Discount codes and weekly specials announced in the WhatsApp group and "
        "channel; 5% off the next purchase for following and engaging on all socials (one coupon per customer).",
        "- **Butcher Counter Service**: Call ahead or order at the counter for custom thicknesses, marinades, "
        "preparation, and special orders.",
        "- **Brazilian & Latin Groceries**: Pantry staples alongside the butcher counter.",
        "",
        "## Key Navigation Links",
        f"- [Online Store / Pickup Orders]({ORDER}): Place orders online for easy counter pickup.",
        f"- [Community Hub & Socials]({SITE}/socials/): WhatsApp group, WhatsApp announcement channel, Instagram, "
        "TikTok, and Facebook.",
        f"- [Directions on Google Maps]({MAPS}): Navigation to 2169 Davenport Blvd, Davenport, FL 33837.",
        f"- [Sitemap]({SITE}/sitemap.xml) · [Full AI reference]({SITE}/llms-full.txt) · [robots.txt]({SITE}/robots.txt)",
        "",
        f"Last updated: {BUILD_DATE}",
        "",
        "## Featured This Week",
        *[f"- [{posts[(g, 'en')]['h1']}]({posts[(g, 'en')]['url']})" for g in featured],
        "",
        "## Languages",
        f"- [English home]({SITE}/): Butcher shop and meat market in Davenport, FL.",
        f"- [Página en español]({SITE}/es/): Carnicería en Davenport, FL.",
        f"- [Página em português]({SITE}/pt/): Açougue em Davenport, FL.",
    ]
    for lang in LANGS:
        lines += ["", f"## Butcher's Blog — {LANG_HEAD[lang]} ({SITE + BLOG[lang]}, RSS: {SITE + FEED[lang]})"]
        for (group, l), p in posts.items():
            if l == lang:
                lines.append(f"- [{p['h1']}]({p['url']})")
    return "\n".join(lines) + "\n"


def llms_full_txt(posts):
    lines = [
        "# Costa's Meat Market - Full AI Knowledge Reference",
        "",
        "Costa's Meat Market is an authentic, full-service butcher shop and Brazilian and Latin specialty market "
        "located in Davenport, Florida (Polk County), in Webb's Town Center, near Haines City, ChampionsGate and "
        "Four Corners.",
        "",
        "## Contact & Location Information",
        "- **Business Name**: Costa's Meat Market",
        "- **Street Address**: 2169 Davenport Blvd (Webb's Town Center)",
        "- **City**: Davenport",
        "- **State**: Florida (FL)",
        "- **ZIP Code**: 33837",
        "- **Country**: United States (US)",
        "- **Telephone**: +1-863-422-2313",
        f"- **Primary Domain**: {SITE}/",
        f"- **Online POS / Store**: {ORDER}",
        f"- **Socials & Community Page**: {SITE}/socials/",
        "- **Established**: 2024",
        "",
        "## Product Categories & Offerings",
        "1. **Fresh Beef & Steaks**: Picanha (top sirloin cap), maminha (tri-tip), alcatra (top sirloin), coxão mole "
        "(top round), ribeye, New York strip, T-bone, skirt steak (churrasco / entraña), flank steak, short ribs "
        "(costela / costilla), fresh ground beef (carne moída de primeira).",
        "2. **Pork & Poultry**: Pork chops, pork belly (toucinho / panceta), pork ribs, whole chickens, chicken "
        "breasts, thighs and wings.",
        "3. **Ready-to-Cook Seasoned Meats**: House-made linguiça (linguiça caseira), seasoned picadinho, marinated "
        "pork, seasoned chicken wings (coxinha da asa / asinha).",
        "4. **Specialty & Regional Cuts**: Brazilian and Latin style cuts; custom trimming and cutting to customer "
        "specifications; special orders.",
        "5. **Family Bundles & Packages**: Curated meat combos and grill boxes offering bulk savings.",
        "6. **Grocery & Pantry**: Seasonings, marinades, charcoal, coarse churrasco salt, and imported Brazilian and "
        "Latin grocery staples.",
        "",
        "## Ordering & Customer Channels",
        f"- **Online Ordering**: Heartland online store at `{ORDER}` for pickup at the counter.",
        "- **In-Store Pickup**: Counter pickup at 2169 Davenport Blvd.",
        "- **WhatsApp Group & Channel**: Updates on fresh arrivals, discount codes and weekly specials in English, "
        "Spanish (Español), and Portuguese (Português).",
        "- **Phone Inquiries**: Call 863-422-2313 for custom orders, special orders, availability, and daily specials.",
        "",
        "## Service Area",
        "Davenport, Haines City, ChampionsGate, Four Corners, Poinciana, Kissimmee, Winter Haven and surrounding Polk "
        "and Osceola County communities in Central Florida, including visitors staying in vacation rental homes near "
        "the Orlando theme parks.",
        "",
        "## Languages",
        f"The website is available in English ({SITE}/), Spanish ({SITE}/es/) and Portuguese ({SITE}/pt/). Every "
        "blog article exists in all three languages.",
        "",
        "## Common Questions",
        "- **Do they carry picanha?** Yes, picanha (top sirloin cap) is a specialty. Availability changes daily; call "
        "863-422-2313 or check the WhatsApp channel.",
        "- **Can you order online?** Yes, through the Heartland online store for pickup at the counter.",
        "- **Custom cuts and special orders?** Yes. Ask at the counter or call ahead.",
        "- **Discounts?** WhatsApp VIP group members get discount codes and weekly specials first. Following and "
        "engaging on all of the store's socials earns 5% off the next purchase, shown at the counter (one coupon per "
        "customer).",
        "- **Payment:** Cash, credit cards, and debit cards.",
        "- **Near Haines City?** Yes. Davenport borders Haines City.",
        "",
        f"Last updated: {BUILD_DATE}",
    ]
    for lang in LANGS:
        lines += ["", f"## Butcher's Blog — {LANG_HEAD[lang]}", f"Index: {SITE + BLOG[lang]} · RSS: {SITE + FEED[lang]}"]
        for (group, l), p in posts.items():
            if l == lang:
                lines.append(f"- **{p['h1']}** ({KINDS[p['kind']][lang]}): {p['description']} {p['url']}")
    return "\n".join(lines) + "\n"


ROBOTS_TEMPLATE = """# ==============================================================================
# Costa's Meat Market - robots.txt
# Last updated: {date} (refreshed weekly with the sitemap)
# Permissive policy for all Search Engines, Scrapers, Web Crawlers, and AI Agents
# ==============================================================================

# Universal Access for All Crawlers & Search Engines
User-agent: *
Allow: /
Disallow: /_build/

# Explicit Access for AI Search Engines, LLM Scrapers, and Research Agents
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

User-agent: Diffbot
Allow: /

User-agent: FacebookBot
Allow: /

User-agent: facebookexternalhit
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: Twitterbot
Allow: /

User-agent: WhatsApp
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: cohere-ai
Allow: /

# Sitemaps (the blog RSS feeds also work as sitemaps) & LLM Context References
Sitemap: https://costasmeatmarket.com/sitemap.xml
Sitemap: https://costasmeatmarket.com/blog/feed.xml
Sitemap: https://costasmeatmarket.com/es/blog/feed.xml
Sitemap: https://costasmeatmarket.com/pt/blog/feed.xml
LLMs: https://costasmeatmarket.com/llms.txt
LLMs-Full: https://costasmeatmarket.com/llms-full.txt
"""


def robots_txt():
    return ROBOTS_TEMPLATE.replace("{date}", BUILD_DATE)
