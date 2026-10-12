"""Photo crops for article heroes and 1200x630 social share cards (Open Graph / Twitter)."""
import hashlib
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS = os.path.join(HERE, "photos")
FONTS = os.path.join(HERE, "fonts")

CASE = "costas-meat-case.webp"
STORE = "costas-storefront-webbs-town-center.webp"

def pexels(author, page):
    return {"author": author, "source_url": f"https://www.pexels.com/photo/{page}/",
            "license": "Pexels License", "license_url": "https://www.pexels.com/license/"}


def unsplash(author, photo_id):
    return {"author": author, "source_url": f"https://unsplash.com/photos/{photo_id}",
            "license": "Unsplash License", "license_url": "https://unsplash.com/license"}


# Every variant is either the store's own photo ("owner": True, from the Google Business Profile) or licensed
# stock with a "credit" (author, source_url, license, license_url). "ai": True marks an AI-generated image (at most
# 5% of topics, only when no real photo fits). Each blog topic in content/meta.py has its own variant and source
# photo; image-credits.md in "Claude outputs" lists them all.
VARIANTS = {
    # The store's own photos
    "case-full": {
        "src": CASE, "owner": True, "box": (0, 110, 1360, 875),
        "file": "costas-meat-market-butcher-case-davenport-fl",
        "alt": {"en": "The butcher case at Costa's Meat Market in Davenport, FL, with ground beef, maminha, alcatra, ribs, steaks, house-made linguiça and seasoned cuts",
                "es": "La vitrina de Costa's Meat Market en Davenport, FL, con carne molida, maminha, alcatra, costillas, steaks, linguiça casera y cortes sazonados",
                "pt": "O balcão do Costa's Meat Market em Davenport, FL, com carne moída, maminha, alcatra, costela, bifes, linguiça caseira e carnes temperadas"},
    },
    "store-front": {
        "src": STORE, "owner": True, "box": (0, 0, 1360, 765),
        "file": "costas-meat-market-storefront-webbs-town-center-davenport",
        "alt": {"en": "Costa's Meat Market storefront in Webb's Town Center, 2169 Davenport Blvd, Davenport, FL",
                "es": "La tienda de Costa's Meat Market en Webb's Town Center, 2169 Davenport Blvd, Davenport, FL",
                "pt": "A loja do Costa's Meat Market no Webb's Town Center, 2169 Davenport Blvd, Davenport, FL"},
    },
    "store-sign": {
        "src": "costas-storefront-sign-davenport-fl.jpg", "owner": True, "box": (280, 230, 1600, 972),
        "file": "costas-meat-market-store-sign-davenport-fl",
        "alt": {"en": "The Costa's Meat Market sign and front windows listing Brazilian products, the butcher counter, fresh bread and seasoned meats, in Davenport, FL",
                "es": "El letrero de Costa's Meat Market y sus vitrinas con productos brasileños, carnicería, pan fresco y carnes sazonadas, en Davenport, FL",
                "pt": "O letreiro do Costa's Meat Market e as vitrines com produtos brasileiros, açougue, pão fresco e carnes temperadas, em Davenport, FL"},
    },
    "store-aisle": {
        "src": "costas-store-aisle-and-counter.jpg", "owner": True, "box": (0, 0, 2400, 1350),
        "file": "inside-costas-meat-market-aisle-and-counter",
        "alt": {"en": "Inside Costa's Meat Market: the checkout counter, an aisle of Brazilian and Latin groceries, and the meat case at the back",
                "es": "Dentro de Costa's Meat Market: la caja, un pasillo de productos brasileños y latinos, y la vitrina de carnes al fondo",
                "pt": "Dentro do Costa's Meat Market: o caixa, um corredor de produtos brasileiros e latinos e o balcão de carnes ao fundo"},
    },
    "picanha-steaks": {
        "src": "costas-picanha-steaks-fat-cap.jpg", "owner": True, "box": (0, 120, 2400, 1470),
        "file": "raw-picanha-steaks-with-fat-cap-costas-meat-market",
        "alt": {"en": "Three raw picanha steaks with their thick fat cap, coarse salt and seasoning, at Costa's Meat Market",
                "es": "Tres steaks de picanha crudos con su gruesa capa de grasa, sal gruesa y sazón, en Costa's Meat Market",
                "pt": "Três bifes de picanha crus com a capa de gordura, sal grosso e tempero, no Costa's Meat Market"},
    },
    "sliced-picanha": {
        "src": "costas-sliced-picanha-medium-rare.jpg", "owner": True, "box": (0, 560, 1574, 1445),
        "file": "sliced-grilled-picanha-pink-center-costas-meat-market",
        "alt": {"en": "Grilled picanha sliced on a cutting board, showing a pink center under the browned fat cap, at Costa's Meat Market",
                "es": "Picanha a la parrilla rebanada en una tabla, con el centro rosado bajo la capa de grasa dorada, en Costa's Meat Market",
                "pt": "Picanha grelhada fatiada na tábua, com o centro rosado sob a capa de gordura dourada, no Costa's Meat Market"},
    },
    "linguica-sandwich": {
        "src": "costas-linguica-sandwich-at-the-counter.jpg", "owner": True, "box": (180, 170, 2048, 1220),
        "file": "linguica-sandwich-at-the-counter-costas-meat-market",
        "alt": {"en": "A grilled linguiça sandwich with cheese and a green herb sauce on a cutting board at the Costa's Meat Market counter",
                "es": "Un sándwich de linguiça a la parrilla con queso y salsa verde de hierbas, sobre una tabla en el mostrador de Costa's Meat Market",
                "pt": "Um sanduíche de linguiça grelhada com queijo e molho verde de ervas, na tábua do balcão do Costa's Meat Market"},
    },
    "rib-rack": {
        "src": "costas-beef-rib-rack-costela.jpg", "owner": True, "box": (0, 0, 2400, 1350),
        "file": "whole-beef-rib-rack-costela-costas-meat-market",
        "alt": {"en": "A whole rack of beef ribs (costela), vacuum-sealed, on the counter at Costa's Meat Market",
                "es": "Un costillar entero de res (costela), empacado al vacío, en el mostrador de Costa's Meat Market",
                "pt": "Uma costela bovina inteira, embalada a vácuo, no balcão do Costa's Meat Market"},
    },
    "pao-de-queijo": {
        "src": "costas-pao-de-queijo-and-brazilian-coffee.jpg", "owner": True, "box": (0, 125, 2400, 1475),
        "file": "pao-de-queijo-and-brazilian-coffee-costas-meat-market",
        "alt": {"en": "Pão de queijo (Brazilian cheese bread) next to bags of Brazilian coffee at Costa's Meat Market",
                "es": "Pão de queijo (pan de queso brasileño) junto a paquetes de café brasileño en Costa's Meat Market",
                "pt": "Pão de queijo ao lado de pacotes de café brasileiro no Costa's Meat Market"},
    },
    "coffee-shelves": {
        "src": "costas-brazilian-coffee-and-sugar-shelves.jpg", "owner": True, "box": (0, 0, 2400, 1350),
        "file": "brazilian-groceries-pilao-coffee-uniao-sugar-costas-meat-market",
        "alt": {"en": "Shelves of Brazilian groceries at Costa's Meat Market, with Pilão coffee and União sugar",
                "es": "Estantes de productos brasileños en Costa's Meat Market, con café Pilão y azúcar União",
                "pt": "Prateleiras de produtos brasileiros no Costa's Meat Market, com café Pilão e açúcar União"},
    },
    "butcher-slicing": {
        "src": "costas-butcher-slicing-stuffed-beef-roll.jpg", "owner": True, "box": (0, 700, 2314, 2002),
        "file": "butcher-slicing-stuffed-beef-roll-costas-meat-market",
        "alt": {"en": "A butcher in black gloves slicing a stuffed, rolled beef roast into pinwheels at Costa's Meat Market",
                "es": "Un carnicero con guantes negros rebana un rollo de carne relleno en Costa's Meat Market",
                "pt": "Um açougueiro de luvas pretas fatiando um rocambole de carne recheado no Costa's Meat Market"},
    },
    "roast-prep": {
        "src": "costas-beef-roast-with-stuffing-ingredients.jpg", "owner": True, "box": (0, 300, 2400, 1650),
        "file": "beef-roast-with-cheese-ham-and-onion-costas-meat-market",
        "alt": {"en": "A seasoned raw beef roast with red onion, green onion, cheese, ham and spices on a cutting board at Costa's Meat Market",
                "es": "Una pieza de res cruda y sazonada con cebolla morada, cebollín, queso, jamón y especias sobre una tabla en Costa's Meat Market",
                "pt": "Uma peça de carne crua e temperada com cebola roxa, cebolinha, queijo, presunto e temperos na tábua, no Costa's Meat Market"},
    },
    # Licensed stock photos (none of these were taken at the store)
    "oxtail-braised": {
        "src": "braised-oxtail-pexels-27556975.jpg", "box": (0, 126, 2400, 1476),
        "credit": pexels("Snappr", "traditional-caribbean-cuisine-27556975"),
        "file": "braised-oxtail-with-thyme",
        "alt": {"en": "Braised oxtail in a dark, glossy sauce with fresh thyme, in a white bowl",
                "es": "Rabo de res guisado en una salsa oscura y brillante con tomillo fresco, en un plato blanco",
                "pt": "Rabada cozida em molho escuro e brilhante com tomilho fresco, em um prato branco"},
    },
    "grill-burgers": {
        "src": "burgers-on-backyard-gas-grill-pexels-8522789.jpg", "box": (0, 125, 2400, 1475),
        "credit": pexels("RDNE Stock project", "cooking-burgers-on-the-grill-8522789"),
        "file": "burgers-on-a-backyard-gas-grill",
        "alt": {"en": "Burgers and buns on a gas grill in a backyard",
                "es": "Hamburguesas y panes en una parrilla de gas en el patio",
                "pt": "Hambúrgueres e pães em uma churrasqueira a gás no quintal"},
    },
    "grill-steaks": {
        "src": "steaks-filling-a-grill-pexels-39452688.jpg", "box": (0, 125, 2400, 1475),
        "credit": pexels("Deane Bayas", "juicy-ribeye-steaks-grilling-outdoors-39452688"),
        "file": "ribeye-steaks-filling-an-outdoor-grill",
        "alt": {"en": "An outdoor grill covered with thick ribeye steaks, enough for a crowd",
                "es": "Una parrilla al aire libre llena de ribeyes gruesos, suficiente para un grupo grande",
                "pt": "Uma churrasqueira ao ar livre cheia de bifes de ancho (ribeye) grossos, para muita gente"},
    },
    "churrasco-skewers": {
        "src": "churrasco-skewers-with-farofa-pexels-9500281.jpg", "box": (0, 125, 2400, 1475),
        "credit": pexels("Gustavo Peres", "variety-of-grilled-meat-9500281"),
        "file": "churrasco-skewers-with-farofa-and-sauces",
        "alt": {"en": "Grilled churrasco skewers of beef, chicken, sausage and cheese on a platter, with farofa, vinaigrette and dipping sauces",
                "es": "Brochetas de churrasco de res, pollo, salchicha y queso en una bandeja, con farofa, vinagreta y salsas",
                "pt": "Espetinhos de churrasco de carne, frango, linguiça e queijo na travessa, com farofa, vinagrete e molhos"},
    },
    "pot-roast": {
        "src": "pot-roast-with-carrots-and-potatoes-pexels-6545671.jpg", "box": (0, 125, 2400, 1475),
        "credit": pexels("Thiago Rebouças", "meat-and-fruit-on-plate-6545671"),
        "file": "pot-roast-with-carrots-and-potatoes",
        "alt": {"en": "Fork-tender pot roast with carrots and potatoes on a platter",
                "es": "Carne asada a la olla, muy tierna, con zanahorias y papas en una bandeja",
                "pt": "Carne de panela macia com cenoura e batata na travessa"},
    },
    "filet-grilled": {
        "src": "grilled-filet-mignon-pexels-34433608.jpg", "box": (0, 1100, 2400, 2450),
        "credit": pexels("Nadin Sh", "juicy-grilled-filet-mignon-on-white-plate-34433608"),
        "file": "grilled-filet-mignon-steak",
        "alt": {"en": "A thick grilled filet mignon steak on a white plate with a side of sauce",
                "es": "Un filet mignon grueso a la parrilla en un plato blanco con salsa aparte",
                "pt": "Um filé mignon alto e grelhado em prato branco, com molho à parte"},
    },
    "rib-roast": {
        "src": "raw-bone-in-rib-roast-pexels-11898916.jpg", "box": (0, 263, 2400, 1613),
        "credit": pexels("Pits Riccardo", "raw-beef-on-table-11898916"),
        "file": "raw-bone-in-beef-rib-roast",
        "alt": {"en": "A raw, well-marbled bone-in beef rib roast on a wooden board",
                "es": "Un asado de costilla de res con hueso, crudo y bien marmoleado, sobre una tabla",
                "pt": "Uma peça de costela de boi com osso (prime rib), crua e bem marmorizada, sobre a tábua"},
    },
    "linguica-sliced": {
        "src": "sliced-linguica-unsplash-4pkdacqpzec.jpg", "box": (0, 125, 2400, 1475),
        "credit": unsplash("Marlom Veloso", "4pkdacQPZec"),
        "file": "sliced-browned-linguica-sausage",
        "alt": {"en": "Sliced linguiça (Brazilian pork sausage) browned on a cast-iron plate",
                "es": "Linguiça (salchicha brasileña de cerdo) en rodajas, dorada en una plancha de hierro",
                "pt": "Linguiça suína fatiada e dourada em uma chapa de ferro"},
    },
    "picadinho": {
        "src": "picadinho-with-rice-farofa-and-egg-pexels-32655177.jpg", "box": (0, 225, 2400, 1575),
        "credit": pexels("Daigoro Folz", "delicious-brazilian-feijoada-with-sides-32655177"),
        "file": "picadinho-diced-beef-stew-with-rice-and-egg",
        "alt": {"en": "Picadinho, a diced beef stew with peas, served with white rice, farofa, beans and a fried egg",
                "es": "Picadinho, un guiso de res en cubos con arvejas, servido con arroz blanco, farofa, frijoles y un huevo frito",
                "pt": "Picadinho de carne com ervilha, servido com arroz branco, farofa, feijão e ovo frito"},
    },
    "wings-skewers": {
        "src": "chicken-wings-on-skewers-over-charcoal-pexels-36798124.jpg", "box": (0, 0, 2400, 1350),
        "credit": pexels("Mohamed Olwy", "delicious-grilled-chicken-skewers-over-charcoal-36798124"),
        "file": "chicken-wings-grilling-on-skewers-over-charcoal",
        "alt": {"en": "Chicken wings grilling on skewers over hot charcoal",
                "es": "Alitas de pollo asándose en brochetas sobre carbón encendido",
                "pt": "Asinhas de frango assando no espeto sobre o carvão em brasa"},
    },
    "feijoada": {
        "src": "feijoada-with-rice-and-collards-pexels-34195320.jpg", "box": (0, 125, 2400, 1475),
        "credit": pexels("José Roberto Oliveira", "traditional-brazilian-feijoada-with-sides-34195320"),
        "file": "feijoada-with-rice-collard-greens-and-orange",
        "alt": {"en": "Feijoada with sausage in a clay pot, served with white rice, collard greens, orange slices and farofa",
                "es": "Feijoada con salchicha en una olla de barro, servida con arroz blanco, col rizada, naranja y farofa",
                "pt": "Feijoada com linguiça na panela de barro, servida com arroz branco, couve, laranja e farofa"},
    },
    "pork-roast": {
        "src": "roast-pork-with-crackling-pexels-26733080.jpg", "box": (0, 125, 2400, 1475),
        "credit": pexels("Jonathan Borba", "roasting-meat-on-barbecue-26733080"),
        "file": "slow-roasted-pork-with-crackling-skin",
        "alt": {"en": "A slow-roasted pork roast with crisp, crackling skin resting on a wire rack",
                "es": "Un asado de cerdo lento con la piel crujiente, reposando sobre una rejilla",
                "pt": "Um assado de porco lento com a pele pururucada, descansando na grelha"},
    },
    "carne-asada": {
        "src": "carne-asada-and-tortillas-on-grill-pexels-8364557.jpg", "box": (0, 146, 2400, 1496),
        "credit": pexels("ELIZABETH MIRANDA", "grilled-meat-and-flat-bread-on-black-grill-8364557"),
        "file": "carne-asada-and-tortillas-on-the-grill",
        "alt": {"en": "Thin steaks for carne asada grilling next to corn tortillas",
                "es": "Carne asada en cortes delgados a la parrilla junto a tortillas de maíz",
                "pt": "Bifes finos de carne asada na grelha ao lado de tortillas de milho"},
    },
    "strip-steaks": {
        "src": "raw-strip-steaks-pexels-20187072.jpg", "box": (0, 125, 2400, 1475),
        "credit": pexels("Boys in Bristol Photography", "meat-on-red-background-20187072"),
        "file": "raw-boneless-strip-steaks",
        "alt": {"en": "Raw boneless strip steaks on a red cutting board",
                "es": "Steaks de lomo (strip) crudos y sin hueso sobre una tabla roja",
                "pt": "Bifes de contrafilé crus e sem osso sobre uma tábua vermelha"},
    },
    "pork-belly": {
        "src": "crispy-pork-belly-pexels-8408377.jpg", "box": (0, 1700, 2400, 3050),
        "credit": pexels("AMANDA LIM", "close-up-photo-of-a-dish-with-crispy-pork-skin-8408377"),
        "file": "crispy-roasted-pork-belly-slices",
        "alt": {"en": "Slices of crispy roasted pork belly with crackling skin",
                "es": "Rebanadas de panceta de cerdo asada con la piel crujiente",
                "pt": "Fatias de barriga de porco assada com a pele pururucada"},
    },
    "ground-beef": {
        "src": "raw-ground-beef-pexels-128401.jpg", "box": (0, 125, 2400, 1475),
        "credit": pexels("Angele J", "grind-meat-in-glass-bowl-128401"),
        "file": "fresh-raw-ground-beef-in-a-bowl",
        "alt": {"en": "Fresh raw ground beef in a glass bowl",
                "es": "Carne molida de res fresca y cruda en un tazón de vidrio",
                "pt": "Carne moída fresca e crua em uma tigela de vidro"},
    },
}

CAPTION = {
    "en": "Photo taken at Costa's Meat Market, 2169 Davenport Blvd, Davenport, FL.",
    "es": "Foto tomada en Costa's Meat Market, 2169 Davenport Blvd, Davenport, FL.",
    "pt": "Foto feita no Costa's Meat Market, 2169 Davenport Blvd, Davenport, FL.",
}
CREDIT = {"en": "Photo", "es": "Foto", "pt": "Foto"}
CROPPED = {"en": "cropped", "es": "recortada", "pt": "recortada"}
AI_CAPTION = {"en": "Illustration generated with AI.", "es": "Ilustración generada con IA.",
              "pt": "Ilustração gerada com IA."}
SITES = {"pexels.com": "Pexels", "unsplash.com": "Unsplash", "pixabay.com": "Pixabay",
         "wikimedia.org": "Wikimedia Commons", "flickr.com": "Flickr"}


def source_site(url):
    host = url.split("/")[2]
    return next(name for domain, name in SITES.items() if host == domain or host.endswith("." + domain))


def needs_attribution(credit):
    """Creative Commons BY licences require a credit and licence link; Pexels, Unsplash, Pixabay and CC0 don't."""
    return credit["license"].startswith("CC BY")

HERO_WIDTHS = (1200, 640)
IMAGES_VERSION = "2"  # bump to force every image to be regenerated

MANIFEST_PATH = os.path.join(HERE, "image-manifest.json")
try:
    MANIFEST = json.load(open(MANIFEST_PATH))
except (OSError, ValueError):
    MANIFEST = {}
PRODUCED = set()


def _source_hash(name):
    with open(os.path.join(PHOTOS, name), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def fresh(root, url, inputs):
    """True when the output exists and was made from these exact inputs (so it can be skipped)."""
    key = url.lstrip("/")
    fingerprint = hashlib.sha256(json.dumps([IMAGES_VERSION, inputs], sort_keys=True).encode()).hexdigest()
    PRODUCED.add(key)
    if MANIFEST.get(key) == fingerprint and os.path.exists(os.path.join(root, key)):
        return True
    MANIFEST[key] = fingerprint
    return False


def save_manifest():
    for key in list(MANIFEST):
        if key not in PRODUCED:
            del MANIFEST[key]
    with open(MANIFEST_PATH, "w") as fh:
        json.dump(MANIFEST, fh, indent=1, sort_keys=True)
        fh.write("\n")
INK = (21, 18, 14)
RED = (176, 20, 27)
PAPER = (242, 236, 222)
TAG = (231, 221, 199)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


_cache = {}


def crop(variant):
    if variant not in _cache:
        v = VARIANTS[variant]
        _cache[variant] = Image.open(os.path.join(PHOTOS, v["src"])).convert("RGB").crop(v["box"])
    return _cache[variant]


def hero_files(variant):
    """Write the WebP hero sizes for a variant; returns [(url, width, height)], widest first."""
    v = VARIANTS[variant]
    img = crop(variant)
    out = []
    for target in HERO_WIDTHS:
        width = min(target, img.width)
        height = round(img.height * width / img.width)
        url = f"/assets/img/blog/{v['file']}-{target}.webp"
        out.append((url, width, height, img.resize((width, height), Image.LANCZOS)))
    return out


def save_heroes(root, variant):
    v = VARIANTS[variant]
    results = []
    for url, width, height, im in hero_files(variant):
        inputs = ["hero", v["src"], _source_hash(v["src"]), list(v["box"]), width]
        if not fresh(root, url, inputs):
            path = os.path.join(root, url.lstrip("/"))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            im.save(path, "WEBP", quality=80, method=6)
        results.append((url, width, height))
    return results


def save_thumb(root, variant, size=120):
    """Small square WebP for search results (a few KB instead of the 640px card image)."""
    v = VARIANTS[variant]
    url = f"/assets/img/blog/{v['file']}-sq{size}.webp"
    if not fresh(root, url, ["thumb", v["src"], _source_hash(v["src"]), list(v["box"]), size]):
        path = os.path.join(root, url.lstrip("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cover(crop(variant), (size, size)).save(path, "WEBP", quality=72, method=6)
    return url


def logo(color, size):
    mark = Image.open(os.path.join(PHOTOS, "costas-logo.png")).convert("LA")
    alpha = mark.split()[1]
    alpha = alpha.resize((size, size), Image.LANCZOS)
    solid = Image.new("RGBA", (size, size), color + (255,))
    solid.putalpha(alpha)
    return solid


def spaced(draw, xy, text, fnt, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + spacing
    return x


def wrap(text, fnt, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if fnt.getlength(trial) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def cover(img, size):
    return ImageOps.fit(img, size, Image.LANCZOS, centering=(0.5, 0.5))


def og_card(root, url, *, title, label, variant, footer):
    v = VARIANTS[variant]
    if fresh(root, url, ["og", title, label, variant, footer, v["src"], _source_hash(v["src"]), list(v["box"])]):
        return
    path = os.path.join(root, url.lstrip("/"))
    W, H = 1200, 630
    base = cover(crop(variant), (W, H)).convert("RGBA")
    # Left-to-right ink gradient so the headline always reads, photo stays visible on the right.
    grad = Image.new("L", (W, 1))
    for x in range(W):
        t = x / W
        a = 238 if t < 0.42 else int(238 - (t - 0.42) / 0.58 * 200)
        grad.putpixel((x, 0), max(a, 38))
    shade = Image.new("RGBA", (W, H), INK + (255,))
    shade.putalpha(grad.resize((W, H)))
    card = Image.alpha_composite(base, shade)
    draw = ImageDraw.Draw(card)

    card.alpha_composite(logo((242, 236, 222), 92), (52, 40))
    spaced(draw, (162, 52), "COSTA'S MEAT MARKET", font("Oswald-600.ttf", 30), PAPER, 3)
    spaced(draw, (163, 94), "DAVENPORT, FLORIDA", font("Oswald-500.ttf", 19), TAG, 5)

    chip_font = font("Oswald-600.ttf", 22)
    chip_w = int(sum(chip_font.getlength(c) + 3 for c in label.upper())) + 36
    draw.rectangle((56, 176, 56 + chip_w, 216), fill=RED)
    spaced(draw, (74, 180), label.upper(), chip_font, (255, 255, 255), 3)

    size = 68
    while True:
        fnt = font("Oswald-700.ttf", size)
        lines = wrap(title, fnt, 760)
        if len(lines) <= 4 or size <= 40:
            break
        size -= 4
    y = 238
    for line in lines[:4]:
        draw.text((56, y), line, font=fnt, fill=(255, 255, 255))
        y += int(size * 1.12)

    draw.rectangle((0, H - 12, W, H), fill=RED)
    fx = 56
    bold, regular = font("Karla-700.ttf", 25), font("Karla-400.ttf", 25)
    draw.text((fx, H - 62), "costasmeatmarket.com", font=bold, fill=(255, 255, 255))
    fx += bold.getlength("costasmeatmarket.com")
    draw.text((fx, H - 62), "  ·  " + footer, font=regular, fill=TAG)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    card.convert("RGB").save(path, "JPEG", quality=84, optimize=True, progressive=True)
