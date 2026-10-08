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

# Every hero image is a real photo of Costa's Meat Market. Swap or add entries here
# (e.g. licensed stock photos) and point topics at them in content/meta.py.
VARIANTS = {
    "case-full": {
        "src": CASE, "box": (0, 110, 1360, 875),
        "file": "costas-meat-market-butcher-case-davenport-fl",
        "alt": {"en": "The butcher case at Costa's Meat Market in Davenport, FL, with ground beef, maminha, alcatra, ribs, steaks, house-made linguiça and seasoned cuts",
                "es": "La vitrina de Costa's Meat Market en Davenport, FL, con carne molida, maminha, alcatra, costillas, steaks, linguiça casera y cortes sazonados",
                "pt": "O balcão do Costa's Meat Market em Davenport, FL, com carne moída, maminha, alcatra, costela, bifes, linguiça caseira e carnes temperadas"},
    },
    "case-raw-cuts": {
        "src": CASE, "box": (330, 150, 1360, 730),
        "file": "fresh-beef-cuts-maminha-alcatra-costas-meat-market",
        "alt": {"en": "Fresh beef cuts, including maminha, alcatra and ribs, in the case at Costa's Meat Market",
                "es": "Cortes frescos de res, como maminha, alcatra y costillas, en la vitrina de Costa's Meat Market",
                "pt": "Cortes bovinos frescos, como maminha, alcatra e costela, no balcão do Costa's Meat Market"},
    },
    "case-ground-beef": {
        "src": CASE, "box": (0, 160, 900, 666),
        "file": "fresh-ground-beef-carne-moida-costas-meat-market",
        "alt": {"en": "Freshly ground beef (carne moída de primeira) and whole beef cuts at Costa's Meat Market",
                "es": "Carne molida fresca y cortes enteros de res en Costa's Meat Market",
                "pt": "Carne moída de primeira e peças inteiras no balcão do Costa's Meat Market"},
    },
    "case-steaks-ribs": {
        "src": CASE, "box": (760, 150, 1360, 488),
        "file": "beef-steaks-and-ribs-costas-meat-market",
        "alt": {"en": "Bone-in steaks and beef ribs in the butcher case at Costa's Meat Market",
                "es": "Steaks con hueso y costillas de res en la vitrina de Costa's Meat Market",
                "pt": "Bifes com osso e costela bovina no balcão do Costa's Meat Market"},
    },
    "case-seasoned": {
        "src": CASE, "box": (160, 420, 1200, 1005),
        "file": "seasoned-meats-linguica-picadinho-costas-meat-market",
        "alt": {"en": "House-seasoned meats ready to cook: pork loin, picadinho, linguiça and chicken at Costa's Meat Market",
                "es": "Carnes sazonadas listas para cocinar: lomo de cerdo, picadinho, linguiça y pollo en Costa's Meat Market",
                "pt": "Carnes temperadas prontas para preparar: lombo, picadinho, linguiça e frango no Costa's Meat Market"},
    },
    "case-linguica-picadinho": {
        "src": CASE, "box": (390, 470, 1100, 870),
        "file": "house-made-linguica-and-picadinho-costas-meat-market",
        "alt": {"en": "House-made linguiça sausage and seasoned picadinho at Costa's Meat Market",
                "es": "Linguiça casera y picadinho sazonado en Costa's Meat Market",
                "pt": "Linguiça caseira e picadinho temperado no Costa's Meat Market"},
    },
    "case-wings": {
        "src": CASE, "box": (900, 320, 1360, 579),
        "file": "seasoned-chicken-wings-coxinha-da-asa-costas-meat-market",
        "alt": {"en": "Seasoned chicken wings (coxinha da asa) ready for the grill at Costa's Meat Market",
                "es": "Alitas de pollo sazonadas listas para la parrilla en Costa's Meat Market",
                "pt": "Coxinha da asa temperada pronta para a churrasqueira no Costa's Meat Market"},
    },
    "case-lombo": {
        "src": CASE, "box": (100, 540, 760, 911),
        "file": "seasoned-pork-loin-lombo-costas-meat-market",
        "alt": {"en": "Seasoned pork in the case at Costa's Meat Market",
                "es": "Cerdo sazonado en la vitrina de Costa's Meat Market",
                "pt": "Carne de porco temperada no balcão do Costa's Meat Market"},
    },
    "store-front": {
        "src": STORE, "box": (0, 0, 1360, 765),
        "file": "costas-meat-market-storefront-webbs-town-center-davenport",
        "alt": {"en": "Costa's Meat Market storefront in Webb's Town Center, 2169 Davenport Blvd, Davenport, FL",
                "es": "La tienda de Costa's Meat Market en Webb's Town Center, 2169 Davenport Blvd, Davenport, FL",
                "pt": "A loja do Costa's Meat Market no Webb's Town Center, 2169 Davenport Blvd, Davenport, FL"},
    },
    "store-banner": {
        "src": STORE, "box": (90, 0, 790, 394),
        "file": "costas-meat-market-banner-davenport-fl",
        "alt": {"en": "Costa's Meat Market flag outside the store in Davenport, FL",
                "es": "La bandera de Costa's Meat Market frente a la tienda en Davenport, FL",
                "pt": "A bandeira do Costa's Meat Market em frente à loja em Davenport, FL"},
    },
    "store-building": {
        "src": STORE, "box": (400, 150, 1360, 690),
        "file": "webbs-town-center-davenport-fl-costas-meat-market",
        "alt": {"en": "Webb's Town Center in Davenport, FL, home of Costa's Meat Market",
                "es": "Webb's Town Center en Davenport, FL, donde está Costa's Meat Market",
                "pt": "Webb's Town Center em Davenport, FL, onde fica o Costa's Meat Market"},
    },
}

CAPTION = {
    "en": "Photo taken at Costa's Meat Market, 2169 Davenport Blvd, Davenport, FL.",
    "es": "Foto tomada en Costa's Meat Market, 2169 Davenport Blvd, Davenport, FL.",
    "pt": "Foto feita no Costa's Meat Market, 2169 Davenport Blvd, Davenport, FL.",
}

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
