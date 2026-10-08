"""Loads the article files and resolves the tokens used inside article bodies."""
import importlib.util
import os
import re

from lib.site import (SITE, ORDER, MAPS, TEL, REVIEW, WA_GROUP, WA_CHANNEL, HOME, BLOG, SOCIALS, LANGS, PUBLISHED,
                      slugify, git_date)
from content.meta import TOPICS, KINDS

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(path):
    spec = importlib.util.spec_from_file_location("post_" + slugify(path), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.POST


def load_posts():
    """Returns {(group, lang): post} with computed fields, in TOPICS order."""
    posts = {}
    for order, (group, kind, image) in enumerate(TOPICS):
        for lang in LANGS:
            path = os.path.join(HERE, "content", "posts", lang, group + ".py")
            if not os.path.exists(path):
                raise SystemExit(f"Missing article: content/posts/{lang}/{group}.py")
            post = dict(_load(path))
            post.update(group=group, lang=lang, kind=kind, image=post.get("image", image), order=order,
                        category=KINDS[kind][lang], path=BLOG[lang] + post["slug"] + "/")
            post["url"] = SITE + post["path"]
            post["og_path"] = f"/assets/og/{lang}/{post['slug']}.jpg"
            post["published"] = post.get("published", PUBLISHED)
            post["modified"] = max(git_date(f"_build/content/posts/{lang}/{group}.py"), post["published"])
            posts[(group, lang)] = post
    slugs = {}
    for (group, lang), post in posts.items():
        key = (lang, post["slug"])
        if key in slugs:
            raise SystemExit(f"Duplicate slug {post['slug']} in {lang}")
        slugs[key] = group
    return posts


def fill(text, lang, posts):
    def link(match):
        group, other = match.group(1), match.group(2)
        target = posts.get((group, other or lang))
        if not target:
            raise SystemExit(f"Unknown link target: {match.group(0)}")
        return target["path"]

    text = re.sub(r"%%LINK:([a-z0-9-]+)(?::(en|es|pt))?%%", link, text)
    tokens = {
        "%%ORDER%%": ORDER, "%%MAPS%%": MAPS.replace("&", "&amp;"), "%%TEL%%": TEL, "%%REVIEW%%": REVIEW,
        "%%WA%%": WA_GROUP, "%%WA_CHANNEL%%": WA_CHANNEL, "%%SOCIALS%%": SOCIALS[lang].replace("&", "&amp;"),
        "%%BLOG%%": BLOG[lang], "%%HOME%%": HOME[lang],
    }
    for key, value in tokens.items():
        text = text.replace(key, value)
    leftover = re.findall(r"%%[A-Z_:a-z0-9-]+%%", text)
    if leftover:
        raise SystemExit(f"Unresolved tokens: {leftover}")
    return text


def add_heading_ids(body):
    """Gives every <h2> an id (for the contents list) and returns (body, [(id, text)])."""
    toc, used = [], set()

    def rep(match):
        text = match.group(1)
        anchor = slugify(text) or "section"
        while anchor in used:
            anchor += "-2"
        used.add(anchor)
        toc.append((anchor, re.sub(r"<[^>]+>", "", text)))
        return f'<h2 id="{anchor}">{text}</h2>'

    return re.sub(r"<h2>(.*?)</h2>", rep, body), toc
