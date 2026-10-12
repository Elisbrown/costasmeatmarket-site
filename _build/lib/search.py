"""Site search: one JSON index per language (products, recipes, blog, general), the /search/ pages and the
search box markup. Matching and ranking run in the browser (assets/js/search.js), so results update on every
keystroke without a server.
"""
import hashlib
import json
import os
import re
import unicodedata
from urllib.parse import quote_plus

from lib import images, site
from lib.site import (ORDER, MAPS, TEL, REVIEW, WA_GROUP, HOME, BLOG, SOCIALS, LANGS, esc, head, langbar, footer,
                      strip_tags)
from content.home_copy import COPY
from content.meta import KINDS
from content.search_terms import PRODUCTS, GENERAL, SYNONYMS

SEARCH = site.SEARCH_PATH

UI = {
    "en": {
        "title": "Search Costa's Meat Market: cuts, recipes, deals and store info",
        "description": "Search Costa's Meat Market in Davenport, FL: meat cuts, Brazilian groceries, recipes, "
                       "cut guides, coupons, opening hours and directions.",
        "h1": "Search Costa's",
        "intro": "Cuts, groceries, recipes, deals and store info. Results update as you type, in English, "
                 "Spanish or Portuguese.",
        "label": "Search", "placeholder": "Search cuts, recipes, deals…", "blog_placeholder": "Search the blog: picanha, oxtail, coupons…",
        "button": "Search", "close": "Close",
        "cats": {"p": "Products", "r": "Recipes", "b": "Blog", "g": "General"},
        "popular": "Popular searches", "browse": "Browse",
        "empty": "No matches for “{q}” yet.",
        "empty_help": "Try another spelling or a cut name in any language, or ask the butchers: call (863) 422-2313 "
                      "or message the WhatsApp group.",
        "count": "{n} results", "count1": "1 result", "all": "See all results for “{q}”",
        "order": "Order", "section": "Section", "question": "FAQ", "guide": "Guide",
        "keys": "↑ ↓ to move · Enter to open · Esc to close",
        "other": "Results in {lang}",
        "noscript": "Search needs JavaScript. Browse the blog or call the counter instead.",
        "popular_terms": ["picanha", "oxtail", "coupons", "hours", "pão de queijo", "ribeye", "chicken wings",
                          "skirt steak", "pernil"],
    },
    "es": {
        "title": "Buscar en Costa's Meat Market: cortes, recetas, ofertas e información",
        "description": "Busca en Costa's Meat Market, Davenport, FL: cortes de carne, productos brasileños, recetas, "
                       "guías de cortes, cupones, horario y cómo llegar.",
        "h1": "Buscar en Costa's",
        "intro": "Cortes, productos, recetas, ofertas e información de la tienda. Los resultados cambian mientras "
                 "escribes, en español, inglés o portugués.",
        "label": "Buscar", "placeholder": "Busca cortes, recetas, ofertas…", "blog_placeholder": "Busca en el blog: picaña, rabo de res, cupones…",
        "button": "Buscar", "close": "Cerrar",
        "cats": {"p": "Productos", "r": "Recetas", "b": "Blog", "g": "General"},
        "popular": "Búsquedas populares", "browse": "Explorar",
        "empty": "Todavía no hay resultados para «{q}».",
        "empty_help": "Prueba otra forma de escribirlo o el nombre del corte en otro idioma, o pregunta a los "
                      "carniceros: llama al (863) 422-2313 o escribe en el grupo de WhatsApp.",
        "count": "{n} resultados", "count1": "1 resultado", "all": "Ver todos los resultados de «{q}»",
        "order": "Pedir", "section": "Sección", "question": "Pregunta", "guide": "Guía",
        "keys": "↑ ↓ para moverte · Enter para abrir · Esc para cerrar",
        "other": "Resultados en {lang}",
        "noscript": "La búsqueda necesita JavaScript. Mira el blog o llama al mostrador.",
        "popular_terms": ["picaña", "rabo de res", "cupones", "horario", "carne asada", "arrachera", "pernil",
                          "costillas", "pan de queso"],
    },
    "pt": {
        "title": "Buscar no Costa's Meat Market: cortes, receitas, promoções e informações",
        "description": "Busque no Costa's Meat Market, Davenport, FL: cortes de carne, produtos brasileiros, receitas, "
                       "guias de cortes, cupons, horário e como chegar.",
        "h1": "Buscar no Costa's",
        "intro": "Cortes, produtos, receitas, promoções e informações da loja. Os resultados mudam enquanto você "
                 "digita, em português, inglês ou espanhol.",
        "label": "Buscar", "placeholder": "Busque cortes, receitas, promoções…", "blog_placeholder": "Busque no blog: picanha, rabada, cupom…",
        "button": "Buscar", "close": "Fechar",
        "cats": {"p": "Produtos", "r": "Receitas", "b": "Blog", "g": "Geral"},
        "popular": "Buscas populares", "browse": "Explorar",
        "empty": "Ainda não temos resultados para “{q}”.",
        "empty_help": "Tente outra grafia ou o nome do corte em outro idioma, ou pergunte aos açougueiros: ligue "
                      "para (863) 422-2313 ou mande mensagem no grupo do WhatsApp.",
        "count": "{n} resultados", "count1": "1 resultado", "all": "Ver todos os resultados de “{q}”",
        "order": "Pedir", "section": "Seção", "question": "Pergunta", "guide": "Guia",
        "keys": "↑ ↓ para navegar · Enter para abrir · Esc para fechar",
        "other": "Resultados em {lang}",
        "noscript": "A busca precisa de JavaScript. Veja o blog ou ligue para o balcão.",
        "popular_terms": ["picanha", "rabada", "cupom", "horário", "pão de queijo", "linguiça", "feijoada",
                          "costela", "maminha"],
    },
}

STOP = set("""a an and are as at be by do does for from how i in is it my of on or the to what with you your
el la los las de del y o en con para por un una que como al es se mi lo le su
o os as do da dos das e em no na nos nas com um uma ao aos pra""".split())

ICONS = {"hours": "clock", "directions": "pin", "call": "phone", "order": "cart", "coupons": "tag",
         "whatsapp": "chat", "socials": "share", "review": "star", "custom": "knife", "home": "home", "blog": "book"}


def norm(text):
    """Same normalization as norm() in search.js: lowercase, no accents, no apostrophes, words only."""
    text = unicodedata.normalize("NFD", str(text).lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"['’]", "", text)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def tokens(*texts):
    out = []
    for text in texts:
        out += norm(text).split()
    return out


SYN_GROUPS = [norm(g).split() for g in SYNONYMS]


def synonyms(*texts):
    have = set(tokens(*texts))
    extra = []
    for group in SYN_GROUPS:
        if have.intersection(group):
            extra += [word for word in group if word not in have and word not in extra]
    return " ".join(extra)


def body_words(html, known):
    """Unique searchable words of an article body, excluding words already in its title, keywords or headings."""
    seen, words = set(known), []
    for word in norm(strip_tags(html.replace("&nbsp;", " ").replace("&amp;", "&"))).split():
        if len(word) < 3 or word in STOP or word in seen or word.isdigit():
            continue
        seen.add(word)
        words.append(word)
    return " ".join(words)


def resolve(target, lang, posts):
    if isinstance(target, tuple):
        return target[LANGS.index(lang)], False
    if target.startswith("LINK:"):
        return posts[(target[5:], lang)]["path"], False
    fixed = {"MAPS": (MAPS, True), "TEL": (TEL, False), "ORDER": (ORDER, True), "WA": (WA_GROUP, True),
             "REVIEW": (REVIEW, True), "SOCIALS": (SOCIALS[lang], False), "HOME": (HOME[lang], False),
             "BLOG": (BLOG[lang], False)}
    return fixed[target]


def blog_doc(root, post, posts):
    from lib.pages import article_body
    lang = post["lang"]
    body, toc = article_body(post, posts)
    h3 = [strip_tags(m) for m in re.findall(r"<h3>(.*?)</h3>", body)]
    strong = [strip_tags(m) for m in re.findall(r"<strong>(.*?)</strong>", body)]
    questions = [q for q, _a in post.get("faq", [])]
    others = {code: posts[(post["group"], code)] for code in LANGS if code != lang}
    keywords = " ".join(dict.fromkeys(strong + h3))[:600]
    recipe = post.get("recipe")
    if recipe:
        keywords += " " + recipe["name"] + " " + " ".join(recipe.get("ingredients", []))[:400]
    known = tokens(post["h1"], post.get("card", ""), keywords, *[t for _a, t in toc], *questions)
    doc = {
        "c": "r" if post["kind"] == "recipe" else "b",
        "t": post["h1"],
        "u": post["path"],
        "s": post["description"],
        "l": post["category"],
        "i": images.save_thumb(root, post["image"]),
        "k": " ".join(dict.fromkeys([post.get("card", ""), KINDS[post["kind"]][lang], keywords])).strip(),
        "h": [[text, anchor] for anchor, text in toc],
        "q": questions,
        "x": {code: other["h1"] for code, other in others.items()},
        "a": {code: other["path"] for code, other in others.items()},
        "w": body_words(post["lede"] + " " + body, known),
    }
    doc["y"] = synonyms(doc["t"], doc["k"], *[t for t, _a in doc["h"]], *questions, *doc["x"].values())
    return doc


def product_docs(root, lang, posts):
    i = LANGS.index(lang)
    docs = []
    for group, names, terms, descs in PRODUCTS:
        post = posts[(group, lang)]
        docs.append({
            "c": "p",
            "t": names[i],
            "u": post["path"],
            "s": descs[i],
            "l": post["category"],
            "g": post.get("card", post["h1"]),
            "i": images.save_thumb(root, post["image"]),
            "k": " ".join(dict.fromkeys([*names, terms])),
            "y": synonyms(*names, terms),
            "o": 1,
        })
    return docs


def general_docs(lang, posts):
    i = LANGS.index(lang)
    docs = []
    for key, titles, descs, target, terms in GENERAL:
        url, external = resolve(target, lang, posts)
        doc = {"c": "g", "t": titles[i], "u": url, "s": descs[i], "k": " ".join([*titles, terms]),
               "ic": ICONS.get(key, "info"), "n": 1}
        doc["y"] = synonyms(doc["t"], doc["k"])
        if external:
            doc["e"] = 1
        docs.append(doc)
    c = COPY[lang]
    for q, a in c["faq"]:
        docs.append({"c": "g", "t": q, "u": HOME[lang] + "#faq", "s": a if len(a) < 170 else a[:167].rsplit(" ", 1)[0] + "…",
                     "k": c["faq_h"], "ic": "faq", "y": synonyms(q)})
    return docs


def build_indexes(root, posts):
    """Writes /assets/search/<lang>.json and returns a short version string for cache busting."""
    payloads = {}
    for lang in LANGS:
        ui = UI[lang]
        docs = product_docs(root, lang, posts)
        docs += [blog_doc(root, p, posts) for (g, l), p in posts.items() if l == lang]
        docs += general_docs(lang, posts)
        payload = {
            "lang": lang,
            "ui": {k: ui[k] for k in ("cats", "empty", "empty_help", "count", "count1", "all", "order", "section",
                                      "question", "guide", "keys", "other", "placeholder", "label", "close",
                                      "popular", "popular_terms")},
            "order": ORDER,
            "docs": docs,
        }
        payloads[lang] = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    digest = hashlib.sha256()
    for lang in LANGS:
        digest.update(payloads[lang].encode())
    for rel in ("assets/js/search.js", "assets/css/search.css"):
        with open(os.path.join(root, rel), "rb") as fh:
            digest.update(fh.read())
    version = digest.hexdigest()[:10]
    os.makedirs(os.path.join(root, "assets", "search"), exist_ok=True)
    for lang, text in payloads.items():
        with open(os.path.join(root, "assets", "search", lang + ".json"), "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    site.SEARCH_VERSION = version
    return version


ICON_SVG = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/>'
            '<path d="m20 20-3.6-3.6"/></svg>')


def search_box(lang, *, box_id, placeholder=None, mode="inline", autofocus=False):
    """A search form that works without JavaScript (GET /search/?q=) and gets live results with it."""
    ui = UI[lang]
    focus = " autofocus" if autofocus else ""
    return f'''<form class="search-box search-{mode}" role="search" action="{SEARCH[lang]}" method="get" data-search="{mode}">
        <label class="sr-only" for="{box_id}">{esc(ui["label"])}</label>
        {ICON_SVG}
        <input id="{box_id}" type="search" name="q" placeholder="{esc(placeholder or ui["placeholder"])}" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search"{focus}>
        <button type="submit">{esc(ui["button"])}</button>
      </form>'''


def search_page(lang, posts):
    ui = UI[lang]
    from lib.pages import UI as PAGE_UI
    popular = "\n".join(
        f'          <a class="chip" href="{SEARCH[lang]}?q={quote_plus(term)}">{esc(term)}</a>' for term in ui["popular_terms"])
    kinds = [k for k in KINDS if any(p["kind"] == k and p["lang"] == lang for p in posts.values())]
    browse = "\n".join(f'          <a class="chip" href="{BLOG[lang]}#{k}">{esc(KINDS[k][lang])}</a>' for k in kinds)
    quick = [(HOME[lang] + "#hours-h", GENERAL[0][1][LANGS.index(lang)]),
             (ORDER, PAGE_UI[lang]["order"]), (TEL, PAGE_UI[lang]["call"]), (MAPS, PAGE_UI[lang]["directions"])]
    quick_html = "\n".join(f'          <a class="chip" href="{esc(h)}">{esc(t)}</a>' for h, t in quick)
    out = [head(lang=lang, path=SEARCH[lang], title=ui["title"], description=ui["description"], alternates=SEARCH,
                robots="noindex, follow", content_group="search")]
    out.append('<body>\n  <div class="wrap wide-wrap">\n')
    out.append(langbar(lang, SEARCH))
    out.append(f'''
    <nav class="crumbs" aria-label="Breadcrumb">
      <a href="{HOME[lang]}">{PAGE_UI[lang]["home"]}</a><span aria-hidden="true">›</span><span>{esc(ui["label"])}</span>
    </nav>

    <main class="search-page" data-section="search">
      <header class="site">
        <h1>{esc(ui["h1"])}</h1>
        <p class="tagline">{esc(ui["intro"])}</p>
      </header>
      {search_box(lang, box_id="search-q", mode="page", autofocus=True)}
      <p class="search-status" id="search-status" aria-live="polite"></p>
      <div class="search-results" id="search-results"></div>
      <noscript><p class="search-status">{esc(ui["noscript"])}</p></noscript>

      <section class="search-explore" id="search-explore" data-section="search-explore">
        <h2 class="section-title">{esc(ui["popular"])}</h2>
        <nav class="chips" aria-label="{esc(ui["popular"])}">
{popular}
        </nav>
        <h2 class="section-title">{esc(ui["browse"])}</h2>
        <nav class="chips" aria-label="{esc(ui["browse"])}">
{browse}
{quick_html}
        </nav>
      </section>
    </main>
''')
    out.append(footer(lang))
    out.append("\n  </div>\n</body>\n</html>\n")
    return "\n".join(out)
