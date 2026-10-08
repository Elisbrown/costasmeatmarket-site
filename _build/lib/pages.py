"""Article, blog index, short-link, 404, feed and redirect pages."""
import math
import re
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_escape

from lib.site import (SITE, ORDER, MAPS, TEL, WA_GROUP, PUBLISHED, BUILD_DATE, LANGS, HTML_LANG, HOME, BLOG, FEED,
                      LANG_NAME, STORE_NODE, GA4_ID, CLARITY_ID, esc, head, langbar, footer, strip_tags, git_date,
                      human_date, week_index)
from lib.content import fill, add_heading_ids
from lib import images
from content.meta import TOPICS, KINDS

UI = {
    "en": {"home": "Home", "blog": "Blog", "published": "Published", "read": "min read",
           "by": "By the butchers at Costa's Meat Market", "toc": "In this article", "faq": "Quick answers",
           "shop_h": "Shop the counter at Costa's",
           "shop_p": "2169 Davenport Blvd, Davenport, FL, in Webb's Town Center. Open Mon–Sat 8 am–8 pm and Sun "
                     "8 am–5 pm. Order online for pickup, call for custom cuts, or join the WhatsApp group for weekly "
                     "specials.",
           "order": "Order online", "call": "Call the counter", "directions": "Get directions",
           "whatsapp": "WhatsApp deals", "related": "Keep reading", "share": "Share this article",
           "copy": "Copy link", "copied": "Link copied", "updated": "Updated",
           "serves": "Serves", "prep": "Prep", "cook": "Cook", "total": "Total",
           "ingredients": "Ingredients", "steps": "Instructions", "all": "All articles", "featured": "Start here",
           "read_more": "Read the article"},
    "es": {"home": "Inicio", "blog": "Blog", "published": "Publicado el", "read": "min de lectura",
           "by": "Por los carniceros de Costa's Meat Market", "toc": "En este artículo", "faq": "Respuestas rápidas",
           "shop_h": "Visita el mostrador de Costa's",
           "shop_p": "2169 Davenport Blvd, Davenport, FL, en Webb's Town Center. Abierto de lunes a sábado de 8 a. m. "
                     "a 8 p. m. y domingos de 8 a. m. a 5 p. m. Pide en línea y recoge, llama para cortes a la medida "
                     "o únete al grupo de WhatsApp para las ofertas de la semana.",
           "order": "Pedir en línea", "call": "Llamar al mostrador", "directions": "Cómo llegar",
           "whatsapp": "Ofertas por WhatsApp", "related": "Sigue leyendo", "share": "Comparte este artículo",
           "copy": "Copiar enlace", "copied": "Enlace copiado", "updated": "Actualizado el",
           "serves": "Porciones", "prep": "Preparación", "cook": "Cocción", "total": "Total",
           "ingredients": "Ingredientes", "steps": "Preparación paso a paso", "all": "Todos los artículos",
           "featured": "Empieza aquí", "read_more": "Leer el artículo"},
    "pt": {"home": "Início", "blog": "Blog", "published": "Publicado em", "read": "min de leitura",
           "by": "Pelos açougueiros do Costa's Meat Market", "toc": "Neste artigo", "faq": "Respostas rápidas",
           "shop_h": "Venha ao balcão do Costa's",
           "shop_p": "2169 Davenport Blvd, Davenport, FL, no Webb's Town Center. Aberto de segunda a sábado, das 8h "
                     "às 20h, e domingo, das 8h às 17h. Peça online e retire, ligue para cortes sob medida ou entre no "
                     "grupo do WhatsApp para as promoções da semana.",
           "order": "Pedir online", "call": "Ligar para o balcão", "directions": "Como chegar",
           "whatsapp": "Promoções no WhatsApp", "related": "Continue lendo", "share": "Compartilhe este artigo",
           "copy": "Copiar link", "copied": "Link copiado", "updated": "Atualizado em",
           "serves": "Rende", "prep": "Preparo", "cook": "Cozimento", "total": "Total",
           "ingredients": "Ingredientes", "steps": "Modo de preparo", "all": "Todos os artigos",
           "featured": "Comece por aqui", "read_more": "Ler o artigo"},
}

INDEX = {
    "en": {"title": "Butcher's Blog: Cut Guides, Recipes & Deals | Costa's Meat Market",
           "description": "Picanha and Brazilian cut guides, recipes, grilling how-tos, coupons and money-saving tips "
                          "from Costa's Meat Market, the butcher shop in Davenport, FL near Haines City.",
           "h1": "The Butcher's Blog",
           "tagline": "Cut guides, recipes, grilling how-tos and money-saving tips from the counter at Costa's Meat "
                      "Market in Davenport, FL."},
    "es": {"title": "Blog del carnicero: cortes, recetas y ofertas | Costa's Meat Market",
           "description": "Guías de cortes latinos y brasileños, recetas, parrilla paso a paso, cupones y consejos "
                          "para ahorrar de Costa's Meat Market, carnicería en Davenport, FL cerca de Haines City.",
           "h1": "Blog del carnicero",
           "tagline": "Guías de cortes, recetas, parrilla paso a paso y consejos para ahorrar desde el mostrador de "
                      "Costa's Meat Market en Davenport, FL."},
    "pt": {"title": "Blog do açougueiro: cortes, receitas e promoções | Costa's Meat Market",
           "description": "Guias de cortes brasileiros, receitas, churrasco passo a passo, cupons e dicas para "
                          "economizar do Costa's Meat Market, açougue em Davenport, FL perto de Haines City.",
           "h1": "Blog do açougueiro",
           "tagline": "Guias de cortes, receitas, churrasco passo a passo e dicas para economizar direto do balcão "
                      "do Costa's Meat Market em Davenport, FL."},
}

FOOTER_CARD = {"en": "2169 Davenport Blvd · (863) 422-2313", "es": "2169 Davenport Blvd · (863) 422-2313",
               "pt": "2169 Davenport Blvd · (863) 422-2313"}

HEROES = {}


def heroes(root, variant):
    if variant not in HEROES:
        HEROES[variant] = images.save_heroes(root, variant)
    return HEROES[variant]


def hero_image(root, variant):
    files = heroes(root, variant)
    return {"url": files[0][0], "width": files[0][1], "height": files[0][2], "thumb": files[-1][0],
            "thumb_w": files[-1][1], "thumb_h": files[-1][2]}


def picture(root, variant, lang, *, sizes, priority=False, thumb=False):
    files = heroes(root, variant)
    seen, srcset = set(), []
    for url, width, height in sorted(files, key=lambda f: f[1]):
        if width in seen:
            continue
        seen.add(width)
        srcset.append(f"{url} {width}w")
    url, width, height = files[-1] if thumb else files[0]
    loading = 'fetchpriority="high" decoding="async"' if priority else 'loading="lazy" decoding="async"'
    alt = images.VARIANTS[variant]["alt"][lang]
    return (f'<img src="{url}" srcset="{", ".join(srcset)}" sizes="{sizes}" width="{width}" height="{height}" '
            f'alt="{esc(alt)}" {loading}>')


def iso_minutes(value):
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?", value or "")
    if not match:
        return None
    return int(match.group(1) or 0) * 60 + int(match.group(2) or 0)


def human_duration(value, lang):
    minutes = iso_minutes(value)
    if minutes is None:
        return value
    hours, mins = divmod(minutes, 60)
    hour = "hr" if lang == "en" else "h"
    if hours and mins:
        return f"{hours} {hour} {mins} min"
    if hours:
        return f"{hours} {hour}"
    return f"{mins} min"


def recipe_card(recipe, lang):
    ui = UI[lang]
    meta = [(ui["serves"], recipe["yield"])]
    for key in ("prep", "cook", "total"):
        if recipe.get(key):
            meta.append((ui[key], human_duration(recipe[key], lang)))
    meta_html = "".join(f"<li><span>{esc(k)}</span> {esc(v)}</li>" for k, v in meta)
    ingredients = "\n".join(f"<li>{esc(i)}</li>" for i in recipe["ingredients"])
    steps = "\n".join(f"<li>{esc(s)}</li>" for s in recipe["steps"])
    return f'''<section class="recipe-card" data-section="recipe">
<h2>{esc(recipe["name"])}</h2>
<ul class="recipe-meta">{meta_html}</ul>
<h3>{ui["ingredients"]}</h3>
<ul>
{ingredients}
</ul>
<h3>{ui["steps"]}</h3>
<ol>
{steps}
</ol>
</section>'''


def recipe_ld(post, recipe, hero):
    data = {
        "@type": "Recipe",
        "@id": post["url"] + "#recipe",
        "name": recipe["name"],
        "description": post["description"],
        "inLanguage": HTML_LANG[post["lang"]],
        "image": [SITE + post["og_path"], SITE + hero["url"]],
        "author": {"@type": "Organization", "name": "Costa's Meat Market", "url": SITE + "/"},
        "datePublished": post["published"],
        "recipeYield": recipe["yield"],
        "recipeCategory": recipe.get("category", ""),
        "recipeCuisine": recipe.get("cuisine", ""),
        "keywords": recipe.get("keywords", ""),
        "recipeIngredient": recipe["ingredients"],
        "recipeInstructions": [{"@type": "HowToStep", "position": i + 1, "text": s}
                               for i, s in enumerate(recipe["steps"])],
    }
    for key, field in (("prep", "prepTime"), ("cook", "cookTime"), ("total", "totalTime")):
        if recipe.get(key):
            data[field] = recipe[key]
    return {k: v for k, v in data.items() if v != ""}


def card(root, post, *, featured=False):
    ui = UI[post["lang"]]
    sizes = "(max-width: 680px) 100vw, 640px" if featured else "(max-width: 520px) 100vw, 320px"
    return f'''          <li class="card{' card-featured' if featured else ''}">
            <a href="{post["path"]}">
              {picture(root, post["image"], post["lang"], sizes=sizes, thumb=not featured)}
              <span class="card-body">
                <span class="chip">{esc(post["category"])}</span>
                <span class="card-title">{esc(post["h1"])}</span>
                <span class="card-desc">{esc(post["description"])}</span>
              </span>
            </a>
          </li>'''


def share_links(post):
    ui = UI[post["lang"]]

    def tagged(source):
        return (post["url"] + f"?utm_source={source}&utm_medium=social_share&utm_campaign=blog_{post['group']}")

    title = post["h1"]
    wa = "https://wa.me/?text=" + quote(f"{title} {tagged('whatsapp')}")
    fb = "https://www.facebook.com/sharer/sharer.php?u=" + quote(tagged("facebook"), safe="")
    x = ("https://twitter.com/intent/tweet?text=" + quote(title) + "&url=" + quote(tagged("x"), safe=""))
    return f'''        <section class="share" data-section="share">
          <h2>{ui["share"]}</h2>
          <div class="share-row">
            <a href="{esc(wa)}" target="_blank" rel="noopener" data-track="share" data-share="whatsapp">WhatsApp</a>
            <a href="{esc(fb)}" target="_blank" rel="noopener" data-track="share" data-share="facebook">Facebook</a>
            <a href="{esc(x)}" target="_blank" rel="noopener" data-track="share" data-share="x">X</a>
            <button type="button" data-share-copy="{esc(tagged('copy_link'))}" data-copied="{esc(ui['copied'])}">{ui["copy"]}</button>
          </div>
        </section>'''


def related_posts(post, posts):
    same = [p for (g, l), p in posts.items() if l == post["lang"] and g != post["group"]]
    same.sort(key=lambda p: (p["kind"] != post["kind"], (p["order"] - post["order"]) % len(TOPICS)))
    return same[:3]


def post_page(root, post, posts):
    lang, ui = post["lang"], UI[post["lang"]]
    body = post["body"]
    recipe = post.get("recipe")
    if recipe:
        card_html = recipe_card(recipe, lang)
        body = body.replace("%%RECIPE%%", card_html) if "%%RECIPE%%" in body else body.rstrip() + "\n" + card_html
    body = fill(body, lang, posts).strip()
    body, toc = add_heading_ids(body)
    words = len(strip_tags(body + " " + post["lede"]).split())
    minutes = max(3, math.ceil(words / 200))
    hero = hero_image(root, post["image"])
    faq = post.get("faq", [])
    og = {"url": SITE + post["og_path"], "width": 1200, "height": 630, "alt": post["h1"]}

    images.og_card(root, post["og_path"], title=post.get("card", post["h1"]), label=post["category"],
                   variant=post["image"], footer=FOOTER_CARD[lang])

    graph = [
        {
            "@type": "BlogPosting",
            "@id": post["url"] + "#article",
            "headline": post["h1"][:110],
            "description": post["description"],
            "inLanguage": HTML_LANG[lang],
            "datePublished": post["published"],
            "dateModified": post["modified"],
            "wordCount": words,
            "articleSection": post["category"],
            "image": [
                {"@type": "ImageObject", "url": og["url"], "width": 1200, "height": 630},
                {"@type": "ImageObject", "url": SITE + hero["url"], "width": hero["width"], "height": hero["height"],
                 "caption": images.VARIANTS[post["image"]]["alt"][lang]},
            ],
            "author": {"@type": "Organization", "name": "Costa's Meat Market", "url": SITE + "/"},
            "publisher": {"@id": SITE + "/#store"},
            "mainEntityOfPage": post["url"],
            "isPartOf": {"@type": "Blog", "@id": SITE + BLOG[lang] + "#blog"},
            "about": {"@id": SITE + "/#store"},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": ui["home"], "item": SITE + HOME[lang]},
                {"@type": "ListItem", "position": 2, "name": ui["blog"], "item": SITE + BLOG[lang]},
                {"@type": "ListItem", "position": 3, "name": post["h1"], "item": post["url"]},
            ],
        },
    ]
    if faq:
        graph.append({
            "@type": "FAQPage",
            "@id": post["url"] + "#faq",
            "inLanguage": HTML_LANG[lang],
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in faq],
        })
    if recipe:
        graph.append(recipe_ld(post, recipe, hero))
    graph.append(STORE_NODE)
    ld = {"@context": "https://schema.org", "@graph": graph}

    alternates = {code: posts[(post["group"], code)]["path"] for code in LANGS}
    extra = "\n".join([
        f'  <meta property="article:published_time" content="{post["published"]}">',
        f'  <meta property="article:modified_time" content="{post["modified"]}">',
        f'  <meta property="article:section" content="{esc(post["category"])}">',
        '  <meta property="article:publisher" content="https://www.facebook.com/share/1BqfQyWrdy/">',
        f'  <link rel="preload" as="image" href="{hero["url"]}" fetchpriority="high">',
    ])
    out = [head(lang=lang, path=post["path"], title=post["title"], description=post["description"],
                og_type="article", alternates=alternates, ld=ld, extra=extra, og_image=og, feeds=True,
                og_title=post["h1"], content_group=f"blog/{post['kind']}")]
    updated = ""
    if post["modified"] > post["published"]:
        updated = (f' · {ui["updated"]} <time datetime="{post["modified"]}">'
                   f'{human_date(post["modified"], lang)}</time>')
    out.append('<body>\n  <div class="wrap article-wrap">\n')
    out.append(langbar(lang, alternates))
    out.append(f'''
    <nav class="crumbs" aria-label="Breadcrumb">
      <a href="{HOME[lang]}">{ui["home"]}</a><span aria-hidden="true">›</span><a href="{BLOG[lang]}">{ui["blog"]}</a><span aria-hidden="true">›</span><a href="{BLOG[lang]}#{post["kind"]}">{esc(post["category"])}</a>
    </nav>

    <main>
      <article class="post">
        <header>
          <a class="chip" href="{BLOG[lang]}#{post["kind"]}">{esc(post["category"])}</a>
          <h1>{esc(post["h1"])}</h1>
          <p class="lede">{esc(post["lede"])}</p>
          <p class="post-meta">{ui["by"]} · {ui["published"]} <time datetime="{post["published"]}">{human_date(post["published"], lang)}</time>{updated} · {minutes} {ui["read"]}</p>
        </header>

        <figure class="hero">
          {picture(root, post["image"], lang, sizes="(max-width: 740px) 100vw, 700px", priority=True)}
          <figcaption>{esc(images.CAPTION[lang])}</figcaption>
        </figure>
''')
    if len(toc) >= 3:
        items = "\n".join(f'            <li><a href="#{anchor}">{esc(text)}</a></li>' for anchor, text in toc)
        out.append(f'''        <nav class="toc" aria-label="{ui["toc"]}">
          <p>{ui["toc"]}</p>
          <ol>
{items}
          </ol>
        </nav>
''')
    out.append(f'''        <div class="post-body">
{body}
        </div>
''')
    if faq:
        items = "\n".join(f'''          <details>
            <summary>{esc(q)}</summary>
            <p>{esc(a)}</p>
          </details>''' for q, a in faq)
        out.append(f'''        <section class="info-section faq" data-section="faq">
          <h2>{ui["faq"]}</h2>
{items}
        </section>
''')
    out.append(f'''        <section class="shop-box" data-section="article-cta">
          <h2>{ui["shop_h"]}</h2>
          <p>{esc(ui["shop_p"])}</p>
          <div class="shop-actions">
            <a class="primary" href="{ORDER}">{ui["order"]}</a>
            <a href="{TEL}">{ui["call"]}</a>
            <a href="{esc(MAPS)}" target="_blank" rel="noopener">{ui["directions"]}</a>
            <a href="{WA_GROUP}" target="_blank" rel="noopener">{ui["whatsapp"]}</a>
          </div>
        </section>

{share_links(post)}
      </article>
''')
    related = related_posts(post, posts)
    cards = "\n".join(card(root, q) for q in related)
    out.append(f'''
      <section class="related" data-section="related">
        <h2>{ui["related"]}</h2>
        <ul class="cards">
{cards}
        </ul>
        <a class="more-link" href="{BLOG[lang]}">{ui["all"]} →</a>
      </section>
    </main>
''')
    out.append(footer(lang))
    out.append("\n  </div>\n</body>\n</html>\n")
    return "\n".join(out)


def index_page(root, lang, posts):
    c, ui = INDEX[lang], UI[lang]
    mine = [p for (g, l), p in posts.items() if l == lang]
    url = SITE + BLOG[lang]
    og_path = f"/assets/og/{lang}/blog.jpg"
    images.og_card(root, og_path, title=c["h1"], label=ui["blog"], variant="case-full", footer=FOOTER_CARD[lang])
    featured = mine[week_index() % len(mine)]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "@id": url + "#blog",
                "url": url,
                "name": c["h1"] + " · Costa's Meat Market",
                "description": c["description"],
                "inLanguage": HTML_LANG[lang],
                "publisher": {"@id": SITE + "/#store"},
                "dateModified": BUILD_DATE,
                "blogPost": [{"@type": "BlogPosting", "headline": p["h1"][:110], "url": p["url"],
                              "datePublished": p["published"], "dateModified": p["modified"],
                              "image": SITE + p["og_path"]} for p in mine],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": ui["home"], "item": SITE + HOME[lang]},
                    {"@type": "ListItem", "position": 2, "name": ui["blog"], "item": url},
                ],
            },
            STORE_NODE,
        ],
    }
    og = {"url": SITE + og_path, "width": 1200, "height": 630, "alt": c["h1"] + " · Costa's Meat Market"}
    out = [head(lang=lang, path=BLOG[lang], title=c["title"], description=c["description"], alternates=BLOG, ld=ld,
                og_image=og, feeds=True, content_group="blog/index")]
    out.append('<body>\n  <div class="wrap wide-wrap">\n')
    out.append(langbar(lang, BLOG))
    kinds_present = [k for k in KINDS if any(p["kind"] == k for p in mine)]
    chips = "\n".join(f'        <a class="chip" href="#{k}">{esc(KINDS[k][lang])}</a>' for k in kinds_present)
    out.append(f'''
    <nav class="crumbs" aria-label="Breadcrumb">
      <a href="{HOME[lang]}">{ui["home"]}</a><span aria-hidden="true">›</span><span>{ui["blog"]}</span>
    </nav>

    <header class="site">
      <div class="eyebrow">
        <i></i><span>Costa's Meat Market · Davenport, FL</span><i></i>
      </div>
      <h1>{esc(c["h1"])}</h1>
      <p class="tagline">{esc(c["tagline"])}</p>
      <nav class="chips" aria-label="{ui["blog"]}">
{chips}
      </nav>
    </header>

    <main>
      <section data-section="featured">
        <h2 class="section-title">{ui["featured"]}</h2>
        <ul class="cards cards-featured">
{card(root, featured, featured=True)}
        </ul>
      </section>
''')
    for kind in kinds_present:
        group = [p for p in mine if p["kind"] == kind]
        cards = "\n".join(card(root, p) for p in group)
        out.append(f'''      <section id="{kind}" data-section="blog-{kind}">
        <h2 class="section-title">{esc(KINDS[kind][lang])}</h2>
        <ul class="cards">
{cards}
        </ul>
      </section>
''')
    out.append(f'''      <section class="cta-card" data-section="order">
        <h2>{ui["shop_h"]}</h2>
        <p>{esc(ui["shop_p"])}</p>
        <a class="btn-primary" href="{ORDER}">{ui["order"]}</a>
      </section>
    </main>
''')
    out.append(footer(lang))
    out.append("\n  </div>\n</body>\n</html>\n")
    return "\n".join(out)


def tracking_snippet(*, page_view=True, content_group="", lang="en"):
    config = (f"{{ content_group: '{content_group}', page_language: '{lang}' }}" if page_view
              else "{ send_page_view: false }")
    return f'''<!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{GA4_ID}', {config});
  </script>
  <!-- Microsoft Clarity -->
  <script type="text/javascript">
      (function(c,l,a,r,i,t,y){{
          c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
          t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
          y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      }})(window, document, "clarity", "script", "{CLARITY_ID}");
  </script>'''


def go_page(code, target):
    """Tracked short link: records the tap in GA4 with the UTM-tagged destination, then redirects."""
    href = esc(target)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Costa's Meat Market</title>
  <meta name="robots" content="noindex, follow">
  <meta http-equiv="refresh" content="2; url={href}">
  {tracking_snippet(page_view=False)}
  <script>
    (function () {{
      var target = {target!r};
      var done = false;
      function go() {{ if (!done) {{ done = true; window.location.replace(target); }} }}
      if (window.clarity) window.clarity("set", "short_link", {code!r});
      gtag('event', 'short_link_open', {{
        link_code: {code!r},
        page_location: window.location.origin + target,
        transport_type: 'beacon',
        event_callback: go
      }});
      setTimeout(go, 600);
    }})();
  </script>
</head>
<body>
  <p><a href="{href}">Continue to Costa's Meat Market</a></p>
</body>
</html>
'''


NOT_FOUND = {
    "en": ("We couldn't find that page.", "Our old online shop pages have moved. Try one of these:",
           [("/", "Home page"), ("/blog/", "Butcher's Blog"), (ORDER, "Online store"), (TEL, "Call (863) 422-2313")]),
    "es": ("No encontramos esa página.", "Las páginas de nuestra tienda anterior cambiaron. Prueba aquí:",
           [("/es/", "Página principal"), ("/es/blog/", "Blog del carnicero"), (ORDER, "Tienda en línea"),
            (TEL, "Llamar al (863) 422-2313")]),
    "pt": ("Não encontramos essa página.", "As páginas da nossa loja antiga mudaram. Tente aqui:",
           [("/pt/", "Página inicial"), ("/pt/blog/", "Blog do açougueiro"), (ORDER, "Loja online"),
            (TEL, "Ligar para (863) 422-2313")]),
}


def not_found_page(redirect_map):
    """Static 404 with a client-side fallback for old Shopify URLs on hosts that ignore _redirects."""
    blocks = []
    for lang in LANGS:
        title, sub, links = NOT_FOUND[lang]
        items = "".join(f'<li><a href="{esc(h)}">{esc(t)}</a></li>' for h, t in links)
        blocks.append(f'''      <section class="info-section" lang="{HTML_LANG[lang]}">
        <h2>{esc(title)}</h2>
        <p>{esc(sub)}</p>
        <ul>{items}</ul>
      </section>''')
    mapping = ",\n      ".join(f'{src!r}: {dst!r}' for src, dst in redirect_map if "*" not in src)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found | Costa's Meat Market</title>
  <meta name="robots" content="noindex, follow">
  <link rel="stylesheet" href="/assets/css/site.css">
  <link rel="icon" href="/favicon.ico" sizes="any">
  {tracking_snippet(content_group="404")}
  <script>
    (function () {{
      var exact = {{
      {mapping}
      }};
      var path = window.location.pathname.replace(/\\/+$/, "");
      var lang = (/^\\/(es|pt)(\\/|$)/.exec(path) || [])[1] || "";
      var dest = exact[path];
      if (!dest && /^\\/(es\\/|pt\\/)?(products|collections|pages|account|cart|checkout|policies|blogs|search)(\\/|$)/.test(path)) {{
        dest = /\\/search$/.test(path) ? (lang ? "/" + lang + "/blog/" : "/blog/") : (lang ? "/" + lang + "/" : "/");
      }}
      gtag('event', 'page_not_found', {{ page_path: window.location.pathname, page_referrer: document.referrer, redirected_to: dest || '' }});
      if (dest) window.location.replace(dest);
    }})();
  </script>
</head>
<body>
  <div class="wrap">
    <header class="site">
      <div class="eyebrow"><i></i><span>Costa's Meat Market · Davenport, FL</span><i></i></div>
      <h1>404</h1>
    </header>
    <main>
{chr(10).join(blocks)}
    </main>
  </div>
</body>
</html>
'''


def redirect_rules(posts):
    """[(source, destination)] for old Shopify URLs, most specific first."""
    from content.redirects import OLD_PRODUCTS, OLD_SECTIONS
    rules = []
    prefix = {"en": "", "es": "/es", "pt": "/pt"}
    for lang in LANGS:
        for product, group in OLD_PRODUCTS.items():
            rules.append((f"{prefix[lang]}/products/{product}", posts[(group, lang)]["path"]))
    for lang in LANGS:
        rules.append((f"{prefix[lang]}/search", BLOG[lang]))
        for section in OLD_SECTIONS:
            rules.append((f"{prefix[lang]}/{section}", HOME[lang]))
            rules.append((f"{prefix[lang]}/{section}/*", HOME[lang]))
    return rules


def netlify_redirects(rules):
    lines = ["# Old Shopify store URLs -> closest page on the new site (Netlify and Cloudflare Pages read this file).",
             "# Generated by _build/build.py from _build/content/redirects.py."]
    for src, dst in rules:
        lines.append(f"{src:<80} {dst:<70} 301")
    return "\n".join(lines) + "\n"


def vercel_config(rules):
    import json
    redirects = [{
        "source": "/:path*",
        "has": [{"type": "host", "value": "www.costasmeatmarket.com"}],
        "destination": "https://costasmeatmarket.com/:path*",
        "permanent": True,
    }]
    for src, dst in rules:
        redirects.append({"source": src.replace("/*", "/:path*"), "destination": dst, "permanent": True})
    return json.dumps({"redirects": redirects}, indent=2) + "\n"


def rfc822(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%a, %d %b %Y") + " 12:00:00 -0400"


def feed(lang, posts):
    c = INDEX[lang]
    mine = [p for (g, l), p in posts.items() if l == lang]
    items = []
    for p in mine:
        items.append(f'''    <item>
      <title>{xml_escape(p["h1"])}</title>
      <link>{p["url"]}</link>
      <guid isPermaLink="true">{p["url"]}</guid>
      <pubDate>{rfc822(p["published"])}</pubDate>
      <category>{xml_escape(p["category"])}</category>
      <description>{xml_escape(p["description"])}</description>
      <media:content url="{SITE + p["og_path"]}" medium="image" type="image/jpeg" width="1200" height="630"/>
    </item>''')
    language = {"en": "en-us", "es": "es-us", "pt": "pt-br"}[lang]
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>{xml_escape(c["h1"])} · Costa's Meat Market</title>
    <link>{SITE + BLOG[lang]}</link>
    <description>{xml_escape(c["description"])}</description>
    <language>{language}</language>
    <lastBuildDate>{rfc822(BUILD_DATE)}</lastBuildDate>
    <atom:link href="{SITE + FEED[lang]}" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
'''


def sitemap(posts, root):
    """Pages that rotate weekly (home, blog indexes, llms, robots) carry the build date; articles carry
    the date their content last changed, so search engines can keep trusting lastmod."""
    entries = []

    def add(path, freq, priority, lastmod, alts=None, imgs=()):
        entries.append((path, lastmod, freq, priority, alts, imgs))

    home_imgs = [SITE + hero_image(root, "store-front")["url"], SITE + hero_image(root, "case-full")["url"]]
    for lang in LANGS:
        add(HOME[lang], "weekly", "1.0" if lang == "en" else "0.9", BUILD_DATE, HOME, home_imgs)
    add("/socials/", "monthly", "0.9", git_date("socials/index.html"))
    for lang in LANGS:
        add(BLOG[lang], "weekly", "0.8", BUILD_DATE, BLOG, [SITE + hero_image(root, "case-full")["url"]])
    for (group, lang), p in posts.items():
        alts = {code: posts[(group, code)]["path"] for code in LANGS}
        add(p["path"], "monthly", "0.7", p["modified"], alts, [SITE + hero_image(root, p["image"])["url"]])
    add("/llms.txt", "weekly", "0.8", BUILD_DATE)
    add("/llms-full.txt", "weekly", "0.6", BUILD_DATE)
    add("/robots.txt", "weekly", "0.8", BUILD_DATE)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:xhtml="http://www.w3.org/1999/xhtml"',
             '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for path, lastmod, freq, priority, alts, imgs in entries:
        lines += ["  <url>", f"    <loc>{xml_escape(SITE + path)}</loc>", f"    <lastmod>{lastmod}</lastmod>",
                  f"    <changefreq>{freq}</changefreq>", f"    <priority>{priority}</priority>"]
        if alts:
            for code in LANGS:
                if code in alts:
                    lines.append(f'    <xhtml:link rel="alternate" hreflang="{code}" href="{xml_escape(SITE + alts[code])}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{xml_escape(SITE + alts["en"])}"/>')
        for url in imgs:
            lines += ["    <image:image>", f"      <image:loc>{xml_escape(url)}</image:loc>", "    </image:image>"]
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"
