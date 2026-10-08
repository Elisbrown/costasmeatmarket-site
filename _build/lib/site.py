"""Shared constants and HTML building blocks for every generated page."""
import datetime
import html
import json
import os
import re
import subprocess

SITE = "https://costasmeatmarket.com"
GA4_ID = "G-S4GM8NREGG"
CLARITY_ID = "yjadt0p2o2"
ORDER = "https://costasmeatmarket.hrpos.heartland.us/"
MAPS = ("https://www.google.com/maps/dir/?api=1&destination=Costa%27s%20Meat%20Market%2C"
        "%202169%20Davenport%20Blvd%2C%20Davenport%2C%20FL%2033837")
TEL = "tel:+18634222313"
REVIEW = "https://g.page/r/CVkkR-S3RMu7EBE/review"
WA_GROUP = "https://chat.whatsapp.com/EKn1EKcbsDy9UAvs1jKP7j"
WA_CHANNEL = "https://whatsapp.com/channel/0029Vb9JwUW84Om4QDHTch3h"
PUBLISHED = "2026-10-08"
LANGS = ("en", "es", "pt")

# The weekly GitHub Action sets COSTAS_BUILD_DATE; locally it's today's date.
BUILD_DATE = os.environ.get("COSTAS_BUILD_DATE") or datetime.date.today().isoformat()
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def git_date(rel_path):
    """Date a file last changed: today if it has uncommitted edits, else its last commit date."""
    try:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", rel_path], cwd=REPO,
                               capture_output=True, text=True, check=True).stdout.strip()
        if dirty:
            return BUILD_DATE
        date = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel_path], cwd=REPO,
                              capture_output=True, text=True, check=True).stdout.strip()
        return max(date or PUBLISHED, PUBLISHED)
    except (OSError, subprocess.CalledProcessError):
        return PUBLISHED


MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
           "November", "December"],
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
           "noviembre", "diciembre"],
    "pt": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
           "novembro", "dezembro"],
}


def human_date(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    if lang == "en":
        return f"{MONTHS['en'][m - 1]} {d}, {y}"
    return f"{d} de {MONTHS[lang][m - 1]} de {y}"


def week_index():
    """A number that goes up by one every ISO week, used to rotate featured articles."""
    y, w, _ = datetime.date.fromisoformat(BUILD_DATE).isocalendar()
    return y * 53 + w

HTML_LANG = {"en": "en", "es": "es", "pt": "pt-BR"}
OG_LOCALE = {"en": "en_US", "es": "es_US", "pt": "pt_BR"}
HOME = {"en": "/", "es": "/es/", "pt": "/pt/"}
BLOG = {"en": "/blog/", "es": "/es/blog/", "pt": "/pt/blog/"}
FEED = {"en": "/blog/feed.xml", "es": "/es/blog/feed.xml", "pt": "/pt/blog/feed.xml"}
LANG_LABEL = {"en": "EN", "es": "ES", "pt": "PT"}
LANG_NAME = {"en": "English", "es": "Español", "pt": "Português"}
SOCIALS = {"en": "/socials/", "es": "/socials/?lang=es", "pt": "/socials/?lang=pt"}

STORE_NODE = {
    "@type": ["ButcherShop", "GroceryStore", "LocalBusiness"],
    "@id": SITE + "/#store",
    "name": "Costa's Meat Market",
    "alternateName": ["Costa's Meat", "Costas Meat Market Davenport"],
    "description": ("Costa's Meat Market is a full-service butcher shop and Brazilian and Latin market in Davenport, "
                    "Florida, offering fresh custom meat cuts, picanha, house-seasoned meats, family bundles, weekly "
                    "specials, and grocery items."),
    "url": SITE + "/",
    "logo": SITE + "/android-chrome-512.png",
    "image": [SITE + "/og-image.jpg",
              SITE + "/assets/img/blog/costas-meat-market-storefront-webbs-town-center-davenport-1200.webp",
              SITE + "/assets/img/blog/costas-meat-market-butcher-case-davenport-fl-1200.webp"],
    "telephone": "+1-863-422-2313",
    "priceRange": "$$",
    "currenciesAccepted": "USD",
    "paymentAccepted": "Cash, Credit Card, Debit Card",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "2169 Davenport Blvd",
        "addressLocality": "Davenport",
        "addressRegion": "FL",
        "postalCode": "33837",
        "addressCountry": "US",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 28.1614, "longitude": -81.6017},
    "hasMap": MAPS,
    "areaServed": ["Davenport, FL", "Haines City, FL", "ChampionsGate, FL", "Four Corners, FL", "Poinciana, FL",
                   "Kissimmee, FL", "Winter Haven, FL", "Polk County, FL", "Osceola County, FL"],
    "knowsAbout": ["Picanha", "Brazilian beef cuts", "Latin American beef cuts", "Churrasco", "Custom butchery",
                   "House-made linguiça", "Seasoned meats"],
    "sameAs": [
        "https://www.facebook.com/share/1BqfQyWrdy/",
        "https://www.instagram.com/costasmeat",
        "https://www.tiktok.com/@costasmeat",
        "https://costasmeatmarket.hrpos.heartland.us/",
    ],
    "potentialAction": {
        "@type": "OrderAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": ORDER,
            "actionPlatform": ["http://schema.org/DesktopWebPlatform", "http://schema.org/MobileWebPlatform"],
        },
        "deliveryMethod": "http://purl.org/goodrelations/v1#DeliveryModePickup",
    },
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700'
         '&family=Karla:ital,wght@0,400;0,500;0,700;1,400&display=swap">')

ICONS = ('<link rel="icon" href="/favicon.ico" sizes="any">\n'
         '  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">\n'
         '  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">\n'
         '  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n'
         '  <link rel="manifest" href="/site.webmanifest">')


def analytics(content_group, lang):
    """Google Analytics 4 + Microsoft Clarity, then the shared click/source tracker."""
    return f'''<!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{GA4_ID}', {{ content_group: '{content_group}', page_language: '{lang}' }});
  </script>
  <!-- Microsoft Clarity -->
  <script type="text/javascript">
      (function(c,l,a,r,i,t,y){{
          c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
          t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
          y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      }})(window, document, "clarity", "script", "{CLARITY_ID}");
  </script>
  <script src="/assets/js/track.js" defer></script>
  <script src="/assets/js/lang.js" defer></script>'''


ARROW = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>')


def esc(text):
    # Attributes are always double-quoted, so apostrophes can stay as-is.
    return html.escape(str(text), quote=False).replace('"', "&quot;")


def jsonld(data):
    return json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text)


def slugify(text):
    import unicodedata
    text = unicodedata.normalize("NFKD", strip_tags(text)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def head(*, lang, path, title, description, content_group, og_type="website", alternates=None, ld=None,
         keywords=None, extra="", og_title=None, og_description=None, og_image=None, robots=None, feeds=False):
    url = SITE + path
    og_image = og_image or {"url": SITE + "/og-image.jpg", "width": 1200, "height": 630,
                            "alt": "Costa's Meat Market — fresh cuts on a wooden board, Davenport FL"}
    robots = robots or "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    lines = [
        "<!doctype html>",
        f'<html lang="{HTML_LANG[lang]}">',
        "<head>",
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f"  <title>{esc(title)}</title>",
        f'  <meta name="description" content="{esc(description)}">',
    ]
    if keywords:
        lines.append(f'  <meta name="keywords" content="{esc(keywords)}">')
    lines += [
        '  <meta name="author" content="Costa\'s Meat Market">',
        '  <meta name="theme-color" content="#B0141B">',
        '  <meta name="referrer" content="strict-origin-when-cross-origin">',
        f'  <meta name="robots" content="{robots}">',
    ]
    if "noindex" not in robots:
        lines += [
            '  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">',
            '  <meta name="bingbot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">',
        ]
    if extra:
        lines.append(extra)
    lines.append("")
    lines.append(f'  <link rel="canonical" href="{url}">')
    if alternates:
        for code in LANGS:
            if code in alternates:
                lines.append(f'  <link rel="alternate" hreflang="{code}" href="{SITE + alternates[code]}">')
        lines.append(f'  <link rel="alternate" hreflang="x-default" href="{SITE + alternates.get("en", path)}">')
    if feeds:
        lines.append(f'  <link rel="alternate" type="application/rss+xml" title="Costa\'s Meat Market — {esc(LANG_NAME[lang])}" href="{FEED[lang]}">')
    lines += [
        '  <link rel="help" type="text/plain" href="/llms.txt" title="LLM and AI Agent Summary">',
        '  <link rel="sitemap" type="application/xml" href="/sitemap.xml" title="Sitemap">',
        "",
        '  <meta property="og:site_name" content="Costa\'s Meat Market">',
        f'  <meta property="og:type" content="{og_type}">',
        f'  <meta property="og:url" content="{url}">',
        f'  <meta property="og:title" content="{esc(og_title or title)}">',
        f'  <meta property="og:description" content="{esc(og_description or description)}">',
        f'  <meta property="og:locale" content="{OG_LOCALE[lang]}">',
    ]
    for code in LANGS:
        if code != lang and alternates and code in alternates:
            lines.append(f'  <meta property="og:locale:alternate" content="{OG_LOCALE[code]}">')
    lines += [
        f'  <meta property="og:image" content="{og_image["url"]}">',
        f'  <meta property="og:image:secure_url" content="{og_image["url"]}">',
        '  <meta property="og:image:type" content="image/jpeg">',
        f'  <meta property="og:image:width" content="{og_image["width"]}">',
        f'  <meta property="og:image:height" content="{og_image["height"]}">',
        f'  <meta property="og:image:alt" content="{esc(og_image["alt"])}">',
        '  <meta name="twitter:card" content="summary_large_image">',
        f'  <meta name="twitter:url" content="{url}">',
        f'  <meta name="twitter:title" content="{esc(og_title or title)}">',
        f'  <meta name="twitter:description" content="{esc(og_description or description)}">',
        f'  <meta name="twitter:image" content="{og_image["url"]}">',
        f'  <meta name="twitter:image:alt" content="{esc(og_image["alt"])}">',
        "",
        "  " + FONTS,
        '  <link rel="stylesheet" href="/assets/css/site.css">',
        "  " + ICONS,
    ]
    if ld:
        lines += ["", '  <script type="application/ld+json">', jsonld(ld), "  </script>"]
    lines += ["", "  " + analytics(content_group, lang), "</head>"]
    return "\n".join(lines)


def langbar(lang, targets):
    """targets: lang -> path for the switcher."""
    links = []
    for code in LANGS:
        current = ' aria-current="page"' if code == lang else ""
        links.append(f'<a href="{targets[code]}" hreflang="{code}" lang="{code}"{current}>{LANG_LABEL[code]}</a>')
    return ('    <nav class="langbar" aria-label="Language / Idioma / Idioma">\n      '
            + "\n      ".join(links) + "\n    </nav>\n"
            '    <p class="lang-suggest" id="lang-suggest" hidden></p>')


FOOT = {
    "en": {"est": "Est. 2024", "where": "In Webb's Town Center", "socials": "Social Links Hub", "order": "Order Online",
           "blog": "Butcher's Blog", "sitemap": "Sitemap", "llms": "LLMs Context", "rss": "RSS"},
    "es": {"est": "Desde 2024", "where": "En Webb's Town Center", "socials": "Redes sociales", "order": "Pedir en línea",
           "blog": "Blog del carnicero", "sitemap": "Mapa del sitio", "llms": "Contexto para IA", "rss": "RSS"},
    "pt": {"est": "Desde 2024", "where": "No Webb's Town Center", "socials": "Redes sociais", "order": "Pedir online",
           "blog": "Blog do açougueiro", "sitemap": "Mapa do site", "llms": "Contexto para IA", "rss": "RSS"},
}


def footer(lang):
    f = FOOT[lang]
    langs = " · ".join(
        f'<a href="{HOME[c]}" hreflang="{c}" lang="{c}">{LANG_NAME[c]}</a>' for c in LANGS)
    return f'''    <footer class="site">
      <p><strong>Costa's Meat Market · {f["est"]}</strong><br>
      2169 Davenport Blvd, Davenport, FL 33837 · {f["where"]} | Tel: <a id="foot-call" href="tel:+18634222313">(863) 422-2313</a></p>
      <p><a id="foot-socials" href="{SOCIALS[lang]}">{f["socials"]}</a> · <a id="foot-order-online" href="{ORDER}">{f["order"]}</a> · <a id="foot-blog" href="{BLOG[lang]}">{f["blog"]}</a> · <a id="foot-rss" href="{FEED[lang]}">{f["rss"]}</a> · <a id="foot-sitemap" href="/sitemap.xml">{f["sitemap"]}</a> · <a id="foot-llms" href="/llms.txt">{f["llms"]}</a></p>
      <p>{langs}</p>
    </footer>'''
