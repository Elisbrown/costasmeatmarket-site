"""Old Shopify store URLs that still get Google impressions, mapped to the closest new article.

Product slugs come from the Search Console Pages report (October 2026). Each one is redirected for
/products/<slug>, /es/products/<slug> and /pt/products/<slug> to the article in that language.
"""

OLD_PRODUCTS = {
    "pao-frances-panebras-french-bread": "brazilian-groceries",
    "tenderloin-special-order": "filet-mignon",
    "polvilho-pq": "pao-de-queijo",
    "yoki-pol-azedo": "pao-de-queijo",
    "yoki-yellow": "pao-de-queijo",
    "cheese-bread-mix": "pao-de-queijo",
    "fini-jelly-kiss": "brazilian-groceries",
    "mel-de-portugal-honey-500gr": "brazilian-groceries",
    "polpa-acerola": "brazilian-groceries",
    "geleia-framboesa": "brazilian-groceries",
    "baton-ovo": "brazilian-groceries",
    "ouro-branco": "brazilian-groceries",
    "camil-black-beans": "feijoada",
    "rice-med-too-joao": "brazilian-groceries",
    "grao-de-campo": "brazilian-groceries",
    "oregano": "brazilian-groceries",
    "thick-barbecue-salt-sal-grosso-para-churrasco-lebre-32-27oz-1kg": "picanha",
    "chicken-skewers-5-skewers-vac-sealed": "wings",
    "chicken-flats-pack": "wings",
    "lombo-gd": "seasoned-meats",
    "veal-chop": "steaks",
}

# Old store sections without a specific match go to the home page (or blog, for search) of the same language.
OLD_SECTIONS = ["products", "collections", "pages", "account", "cart", "checkout", "policies", "blogs"]
