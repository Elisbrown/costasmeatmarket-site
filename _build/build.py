"""Builds the static site for costasmeatmarket.com.

Usage (from the repository root):  python3 _build/build.py

Source of truth:
  _build/content/home_copy.py        home page copy (EN/ES/PT)
  _build/content/meta.py             blog topics, categories and photos, in display order
  _build/content/posts/<lang>/*.py   one file per article per language
  _build/content/redirects.py        old Shopify URLs to redirect
  _build/lib/images.py               photo crops and social share cards

Generated (do not edit by hand): index.html, es/, pt/, blog/, es/blog/, pt/blog/, go/, 404.html,
assets/img/blog/, assets/og/, sitemap.xml, llms.txt, llms-full.txt, robots.txt, _redirects, vercel.json.
"""
import os
import shutil
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
sys.path.insert(0, BUILD)

from PIL import Image  # noqa: E402

from lib.site import HOME, BLOG, FEED, LANGS  # noqa: E402
from lib.content import load_posts  # noqa: E402
from lib import pages, discovery, images  # noqa: E402
from lib.home import build_home  # noqa: E402

GO = {
    "ig": "/socials/?utm_source=instagram&utm_medium=social&utm_campaign=bio_link",
    "tt": "/socials/?utm_source=tiktok&utm_medium=social&utm_campaign=bio_link",
    "fb": "/?utm_source=facebook&utm_medium=social&utm_campaign=page_link",
    "wa": "/?utm_source=whatsapp&utm_medium=social&utm_campaign=group_share",
    "qr": "/?utm_source=qr_code&utm_medium=print&utm_campaign=in_store",
}

# Generated HTML is rebuilt from scratch; images are only re-rendered when their inputs change,
# and images that are no longer used are removed.
GENERATED_DIRS = ["blog", "es/blog", "pt/blog", "go"]
IMAGE_DIRS = ["assets/og", "assets/img/blog"]


def write(rel, content):
    path = os.path.join(ROOT, rel.lstrip("/"))
    if rel.endswith("/"):
        path = os.path.join(path, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def export_logo():
    """WebP versions of the logo: small for the home page header, full size for the socials page."""
    for name, size in (("costas-meat-market-logo.webp", 320), ("costas-meat-market-logo-555.webp", 555)):
        url = "/assets/img/" + name
        if images.fresh(ROOT, url, ["logo", size, images._source_hash("costas-logo.png")]):
            continue
        mark = Image.open(os.path.join(BUILD, "photos", "costas-logo.png")).convert("RGBA")
        out = os.path.join(ROOT, url.lstrip("/"))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        mark.resize((size, size), Image.LANCZOS).save(out, "WEBP", quality=90, method=6)


def remove_stale_images():
    for rel in IMAGE_DIRS:
        base = os.path.join(ROOT, rel)
        for folder, _dirs, files in os.walk(base):
            for name in files:
                key = os.path.relpath(os.path.join(folder, name), ROOT).replace(os.sep, "/")
                if key not in images.PRODUCED:
                    os.remove(os.path.join(folder, name))


def main():
    for rel in GENERATED_DIRS:
        shutil.rmtree(os.path.join(ROOT, rel), ignore_errors=True)
    export_logo()
    posts = load_posts()
    for lang in LANGS:
        write(BLOG[lang], pages.index_page(ROOT, lang, posts))
        write(FEED[lang], pages.feed(lang, posts))
    for post in posts.values():
        write(post["path"], pages.post_page(ROOT, post, posts))
    for lang in LANGS:
        write(HOME[lang], build_home(ROOT, lang, posts))
    for code, target in GO.items():
        write(f"/go/{code}/", pages.go_page(code, target))
    rules = pages.redirect_rules(posts)
    write("/404.html", pages.not_found_page(rules))
    write("/_redirects", pages.netlify_redirects(rules))
    write("/vercel.json", pages.vercel_config(rules))
    write("/sitemap.xml", pages.sitemap(posts, ROOT))
    write("/llms.txt", discovery.llms_txt(posts))
    write("/llms-full.txt", discovery.llms_full_txt(posts))
    write("/robots.txt", discovery.robots_txt())
    remove_stale_images()
    images.save_manifest()
    print(f"Built {len(posts)} articles, {len(LANGS)} home pages, {len(LANGS)} blog indexes, {len(GO)} short links, "
          f"{len(rules)} redirects. Build date {pages.BUILD_DATE}.")


if __name__ == "__main__":
    main()
