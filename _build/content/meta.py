"""Blog topics in display order. Each topic has one article per language in content/posts/<lang>/<group>.py.

kind  -> category label (KINDS)
image -> photo variant in lib/images.py
"""

KINDS = {
    "local":    {"en": "Local guide",      "es": "Guía local",        "pt": "Guia local"},
    "cuts":     {"en": "Cut guide",        "es": "Guía de cortes",    "pt": "Guia de cortes"},
    "recipe":   {"en": "Recipe",           "es": "Receta",            "pt": "Receita"},
    "tutorial": {"en": "How-to",           "es": "Paso a paso",       "pt": "Passo a passo"},
    "basics":   {"en": "Butcher basics",   "es": "Lo básico",         "pt": "Básico do açougue"},
    "planning": {"en": "Party planning",   "es": "Para fiestas",      "pt": "Para festas"},
    "savings":  {"en": "Deals & savings",  "es": "Ofertas y ahorro",  "pt": "Promoções e economia"},
}

TOPICS = [
    # group,                kind,       image
    ("picanha",             "cuts",     "case-raw-cuts"),
    ("haines-city",         "local",    "store-front"),
    ("coupons",             "savings",  "store-banner"),
    ("seasoned-meats",      "tutorial", "case-seasoned"),
    ("vacation",            "local",    "store-building"),
    ("cuts",                "cuts",     "case-full"),
    ("per-person",          "planning", "case-raw-cuts"),
    ("churrasco-menu",      "planning", "case-seasoned"),
    ("oxtail",              "recipe",   "case-steaks-ribs"),
    ("pot-roast",           "recipe",   "case-raw-cuts"),
    ("filet-mignon",        "cuts",     "case-raw-cuts"),
    ("prime-rib",           "cuts",     "case-steaks-ribs"),
    ("short-ribs",          "recipe",   "case-steaks-ribs"),
    ("linguica",            "tutorial", "case-linguica-picadinho"),
    ("picadinho",           "recipe",   "case-linguica-picadinho"),
    ("wings",               "recipe",   "case-wings"),
    ("pao-de-queijo",       "recipe",   "store-front"),
    ("brazilian-groceries", "local",    "store-front"),
    ("feijoada",            "recipe",   "case-lombo"),
    ("pernil",              "recipe",   "case-lombo"),
    ("carne-asada",         "recipe",   "case-raw-cuts"),
    ("doneness",            "basics",   "case-steaks-ribs"),
    ("steaks",              "cuts",     "case-steaks-ribs"),
    ("butcher-vs-grocery",  "basics",   "case-ground-beef"),
    ("pork-belly",          "recipe",   "case-lombo"),
    ("cheap-cuts",          "savings",  "case-ground-beef"),
    ("bundles",             "savings",  "case-full"),
    ("save",                "savings",  "store-building"),
]

# Home pages show HOME_PINNED first, then HOME_ROTATING articles that change every week
# (the weekly GitHub Action rebuilds the site, so the home pages and blog indexes stay fresh).
HOME_PINNED = ["haines-city"]
HOME_ROTATING = 3
