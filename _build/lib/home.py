import json

from lib.site import (SITE, ORDER, MAPS, REVIEW, HOME, BLOG, SOCIALS, STORE_NODE, ARROW, LANGS, HTML_LANG, BUILD_DATE,
                      HOURS, esc, head, langbar, footer, week_index)
from lib.pages import card, picture, hero_image
from lib import images
from content.home_copy import COPY
from content.meta import TOPICS, HOME_PINNED, HOME_ROTATING


def featured_groups():
    """Pinned articles plus a set that rotates every week."""
    pool = [group for group, _kind, _image in TOPICS if group not in HOME_PINNED]
    start = (week_index() * HOME_ROTATING) % len(pool)
    return HOME_PINNED + [pool[(start + i) % len(pool)] for i in range(HOME_ROTATING)]

GEO_EXTRA = '''  <meta name="publisher" content="Costa's Meat Market">
  <meta name="slurp" content="index, follow">
  <meta name="duckduckbot" content="index, follow">
  <meta name="baiduspider" content="index, follow">
  <meta name="yandexbot" content="index, follow">
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="Davenport, Florida">
  <meta name="geo.position" content="28.1614;-81.6017">
  <meta name="ICBM" content="28.1614, -81.6017">
  <meta name="format-detection" content="telephone=yes, address=yes">'''

TILE_IDS = ["link-socials", "link-directions", "link-call", "link-blog", "link-review", "link-llms"]


def home_ld(lang, c, root):
    url = SITE + HOME[lang]
    return {
        "@context": "https://schema.org",
        "@graph": [
            STORE_NODE,
            {
                "@type": "WebSite",
                "@id": SITE + "/#website",
                "url": SITE + "/",
                "name": "Costa's Meat Market",
                "description": "Official website for Costa's Meat Market in Davenport, Florida.",
                "inLanguage": ["en", "es", "pt-BR"],
                "publisher": {"@id": SITE + "/#store"},
            },
            {
                "@type": "WebPage",
                "@id": url + "#webpage",
                "url": url,
                "name": c["title"],
                "description": c["description"],
                "inLanguage": HTML_LANG[lang],
                "isPartOf": {"@id": SITE + "/#website"},
                "about": {"@id": SITE + "/#store"},
                "dateModified": BUILD_DATE,
                "primaryImageOfPage": SITE + hero_image(root, "store-front")["url"],
            },
            {
                "@type": "ImageGallery",
                "@id": url + "#photos",
                "name": c["photos_h"],
                "inLanguage": HTML_LANG[lang],
                "about": {"@id": SITE + "/#store"},
                "image": [{"@type": "ImageObject", "contentUrl": SITE + hero_image(root, v)["url"],
                           "caption": cap, "width": hero_image(root, v)["width"],
                           "height": hero_image(root, v)["height"]} for v, cap in c["photos"]],
            },
            {
                "@type": "FAQPage",
                "@id": url + "#faq",
                "inLanguage": HTML_LANG[lang],
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in c["faq"]
                ],
            },
        ],
    }


def build_home(root, lang, posts):
    c = COPY[lang]
    out = [head(lang=lang, path=HOME[lang], title=c["title"], description=c["description"],
                og_description=c["og_description"], keywords=c["keywords"], alternates=HOME,
                ld=home_ld(lang, c, root), extra=GEO_EXTRA, feeds=True, content_group="home")]
    out.append("<body>\n  <div class=\"wrap\">\n")
    out.append(langbar(lang, HOME))
    out.append(f'''
    <header class="site">
      <img class="brand-mark" src="/assets/img/costas-meat-market-logo.webp" width="160" height="160" alt="{esc(c["logo_alt"])}">
      <div class="eyebrow">
        <i></i><span>Davenport, Florida</span><i></i>
      </div>
      <h1>Costa's Meat Market</h1>
      <p class="tagline">{esc(c["tagline"])}</p>
    </header>

    <main>
      <section class="cta-card" data-section="order">
        <h2>{esc(c["order_h"])}</h2>
        <p>{esc(c["order_p"])}</p>
        <a class="btn-primary" href="{ORDER}" id="link-order-online">
          {esc(c["order_btn"])}
          {ARROW}
        </a>
      </section>

      <nav class="grid-links" aria-label="{esc(c["nav_label"])}" data-section="quick-links">''')
    hrefs = [SOCIALS[lang], MAPS, "tel:+18634222313", BLOG[lang], REVIEW, "/llms.txt"]
    for tile_id, href, (title, desc) in zip(TILE_IDS, hrefs, c["tiles"]):
        target = ' target="_blank" rel="noopener"' if href in (MAPS, REVIEW) else ""
        out.append(f'''        <a class="link-tile" id="{tile_id}" href="{esc(href)}"{target}>
          <div>
            <span class="title">{esc(title)}</span>
            <span class="desc">{esc(desc)}</span>
          </div>
        </a>''')
    out.append("      </nav>\n")
    labels = c["hour_labels"]
    rows = []
    for i, name in enumerate(c["days"]):
        js_day = (i + 1) % 7  # Monday-first table, Sunday-first schedule
        opens, closes = HOURS[js_day]
        rows.append(f'''          <tr data-day="{js_day}"><th scope="row">{esc(name)}</th><td>{labels[opens]} – {labels[closes]}</td></tr>''')
    badge = json.dumps({"hours": HOURS, "t": {str(k): v for k, v in labels.items()}, **c["open_now"]},
                       ensure_ascii=False)
    out.append(f'''      <section class="info-section hours" data-section="hours" aria-labelledby="hours-h">
        <h2 id="hours-h">{esc(c["hours_h"])}</h2>
        <p class="open-now" data-open-now="{esc(badge)}" hidden></p>
        <table class="hours-table">
{chr(10).join(rows)}
        </table>
        <p class="hours-note">{esc(c["hours_note"])}</p>
        <p><strong>Costa's Meat Market</strong><br>2169 Davenport Blvd, Davenport, FL 33837 (Webb's Town Center)<br>
        <a href="{esc(MAPS)}" target="_blank" rel="noopener" id="link-hours-directions">{esc(c["tiles"][1][0])}</a> · <a href="tel:+18634222313" id="link-hours-call">(863) 422-2313</a></p>
      </section>
''')
    figures = "\n".join(f'''        <figure>
          {picture(root, variant, lang, sizes="(max-width: 660px) 100vw, 620px")}
          <figcaption>{esc(caption)}</figcaption>
        </figure>''' for variant, caption in c["photos"])
    out.append(f'''      <section class="gallery" data-section="photos" aria-labelledby="photos-h">
        <h2 class="section-title" id="photos-h">{esc(c["photos_h"])}</h2>
{figures}
      </section>
''')
    items = "\n".join(f"          <li><strong>{esc(k)}</strong> {esc(v)}</li>" for k, v in c["about_list"])
    vac = posts[(c["vac_link"][0], lang)]["path"]
    out.append(f'''      <article class="info-section" data-section="about">
        <h2>{esc(c["about_h"])}</h2>
        <p>{esc(c["about_p"])}</p>
        <ul>
{items}
        </ul>
      </article>

      <section class="info-section" data-section="vacation">
        <h2>{esc(c["vac_h"])}</h2>
        <p>{esc(c["vac_p"])}</p>
        <a class="more-link" href="{vac}">{esc(c["vac_link"][1])}</a>
      </section>
''')
    cards = "\n".join(card(root, posts[(g, lang)]) for g in featured_groups())
    out.append(f'''      <section class="related" data-section="blog">
        <h2 class="section-title">{esc(c["blog_h"])}</h2>
        <ul class="cards">
{cards}
        </ul>
        <a class="more-link" href="{BLOG[lang]}">{esc(c["blog_all"])}</a>
      </section>
''')
    faq = "\n".join(
        f'''        <details>
          <summary>{esc(q)}</summary>
          <p>{esc(a)}</p>
        </details>''' for q, a in c["faq"])
    out.append(f'''      <section class="info-section faq" data-section="faq">
        <h2>{esc(c["faq_h"])}</h2>
{faq}
      </section>
    </main>
''')
    out.append(footer(lang))
    out.append("\n  </div>\n</body>\n</html>\n")
    return "\n".join(out)
