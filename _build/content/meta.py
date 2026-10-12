"""Blog topics in display order. Each topic has one article per language in content/posts/<lang>/<group>.py.

kind  -> category label (KINDS)
image -> photo variant in lib/images.py (each topic has its own photo)
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
    ("picanha",              "cuts",     "picanha-steaks"),
    ("haines-city",          "local",    "store-front"),
    ("coupons",              "savings",  "store-sign"),
    ("seasoned-meats",       "tutorial", "linguica-sandwich"),
    ("vacation",             "local",    "grill-burgers"),
    ("cuts",                 "cuts",     "case-full"),
    ("per-person",           "planning", "grill-steaks"),
    ("churrasco-menu",       "planning", "churrasco-skewers"),
    ("oxtail",               "recipe",   "oxtail-braised"),
    ("pot-roast",            "recipe",   "pot-roast"),
    ("filet-mignon",         "cuts",     "filet-grilled"),
    ("prime-rib",            "cuts",     "rib-roast"),
    ("short-ribs",           "recipe",   "rib-rack"),
    ("linguica",             "tutorial", "linguica-sliced"),
    ("picadinho",            "recipe",   "picadinho"),
    ("wings",                "recipe",   "wings-skewers"),
    ("pao-de-queijo",        "recipe",   "pao-de-queijo"),
    ("brazilian-groceries",  "local",    "coffee-shelves"),
    ("feijoada",             "recipe",   "feijoada"),
    ("pernil",               "recipe",   "pork-roast"),
    ("carne-asada",          "recipe",   "carne-asada"),
    ("doneness",             "basics",   "sliced-picanha"),
    ("steaks",               "cuts",     "strip-steaks"),
    ("butcher-vs-grocery",   "basics",   "butcher-slicing"),
    ("pork-belly",           "recipe",   "pork-belly"),
    ("cheap-cuts",           "savings",  "ground-beef"),
    ("bundles",              "savings",  "roast-prep"),
    ("save",                 "savings",  "store-aisle"),
]

# Home pages show HOME_PINNED first, then HOME_ROTATING articles that change every week
# (the weekly GitHub Action rebuilds the site, so the home pages and blog indexes stay fresh).
HOME_PINNED = ["haines-city"]
HOME_ROTATING = 3
