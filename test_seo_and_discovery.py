"""Unit test suite for SEO, crawler permissions, Schema.org metadata, and AI discovery files.

This module validates the correctness of the HTML SEO tags, JSON-LD Schema data,
robots.txt directives, XML sitemap syntax, and LLMs.txt AI discovery files for
Costa's Meat Market.
"""

import json
import os
import re
import unittest
import xml.etree.ElementTree as ET


class TestSeoAndDiscovery(unittest.TestCase):
    """Test cases for verifying SEO, bots/crawler permissions, and AI discovery."""

    @classmethod
    def setUpClass(cls):
        """Set up file paths and read core contents for testing."""
        cls.base_dir = os.path.dirname(os.path.abspath(__file__))
        cls.index_path = os.path.join(cls.base_dir, "index.html")
        cls.robots_path = os.path.join(cls.base_dir, "robots.txt")
        cls.sitemap_path = os.path.join(cls.base_dir, "sitemap.xml")
        cls.llms_path = os.path.join(cls.base_dir, "llms.txt")
        cls.llms_full_path = os.path.join(cls.base_dir, "llms-full.txt")

        with open(cls.index_path, "r", encoding="utf-8") as f:
            cls.index_html = f.read()

        with open(cls.robots_path, "r", encoding="utf-8") as f:
            cls.robots_txt = f.read()

        with open(cls.sitemap_path, "r", encoding="utf-8") as f:
            cls.sitemap_xml = f.read()

        with open(cls.llms_path, "r", encoding="utf-8") as f:
            cls.llms_txt = f.read()

    def test_robots_meta_tag_allows_indexing(self):
        """Ensure meta robots allows indexing and does not have noindex."""
        self.assertNotIn('content="noindex"', self.index_html)
        self.assertIn('name="robots" content="index, follow', self.index_html)
        self.assertIn('name="googlebot" content="index, follow', self.index_html)
        self.assertIn('name="bingbot" content="index, follow', self.index_html)

    def test_title_and_description(self):
        """Ensure title and description tags are present and descriptive."""
        title_match = re.search(r"<title>(.*?)</title>", self.index_html, re.IGNORECASE)
        self.assertIsNotNone(title_match, "Title tag must exist.")
        title = title_match.group(1).strip()
        self.assertIn("Costa's Meat Market", title)
        self.assertGreater(len(title), 15)

        desc_match = re.search(r'<meta name="description" content="(.*?)"', self.index_html)
        self.assertIsNotNone(desc_match, "Meta description tag must exist.")
        desc = desc_match.group(1).strip()
        self.assertIn("Davenport", desc)
        self.assertGreater(len(desc), 30)

    def test_geo_meta_tags(self):
        """Ensure local SEO geo tags exist for Davenport, FL."""
        self.assertIn('name="geo.region" content="US-FL"', self.index_html)
        self.assertIn('name="geo.placename" content="Davenport, Florida"', self.index_html)
        self.assertIn('name="geo.position"', self.index_html)

    def test_opengraph_and_twitter_tags(self):
        """Ensure OpenGraph and Twitter card metadata are properly configured."""
        self.assertIn('property="og:title"', self.index_html)
        self.assertIn('property="og:description"', self.index_html)
        self.assertIn('property="og:type" content="website"', self.index_html)
        self.assertIn('property="og:url"', self.index_html)
        self.assertIn('name="twitter:card"', self.index_html)

    def test_json_ld_schema(self):
        """Ensure JSON-LD LocalBusiness schema parses cleanly and contains key data."""
        schema_match = re.search(
            r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
            self.index_html,
            re.DOTALL,
        )
        self.assertIsNotNone(schema_match, "JSON-LD script block must exist.")
        data = json.loads(schema_match.group(1))

        self.assertIn("@graph", data)
        graph = data["@graph"]

        store = next((item for item in graph if "ButcherShop" in item.get("@type", [])), None)
        self.assertIsNotNone(store, "ButcherShop entity must exist in Schema graph.")
        self.assertEqual(store["name"], "Costa's Meat Market")
        self.assertEqual(store["telephone"], "+1-863-422-2313")
        self.assertEqual(store["address"]["addressLocality"], "Davenport")
        self.assertEqual(store["address"]["addressRegion"], "FL")
        self.assertEqual(store["address"]["postalCode"], "33837")

    def test_robots_txt_rules(self):
        """Ensure robots.txt allows all crawlers and lists AI agents and sitemap."""
        self.assertIn("User-agent: *", self.robots_txt)
        self.assertIn("Allow: /", self.robots_txt)
        self.assertIn("User-agent: GPTBot", self.robots_txt)
        self.assertIn("User-agent: ClaudeBot", self.robots_txt)
        self.assertIn("User-agent: PerplexityBot", self.robots_txt)
        self.assertIn("Sitemap: https://costasmeatmarket.com/sitemap.xml", self.robots_txt)
        self.assertIn("LLMs: https://costasmeatmarket.com/llms.txt", self.robots_txt)

    def test_sitemap_xml_validity(self):
        """Ensure sitemap.xml is well-formed XML and contains homepage and socials."""
        root = ET.fromstring(self.sitemap_xml)
        namespaces = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [elem.text for elem in root.findall("sm:url/sm:loc", namespaces)]

        self.assertIn("https://costasmeatmarket.com/", locs)
        self.assertIn("https://costasmeatmarket.com/socials/", locs)
        self.assertIn("https://costasmeatmarket.com/llms.txt", locs)

    def test_llms_txt_content(self):
        """Ensure llms.txt exists, is non-empty, and contains necessary AI context."""
        self.assertIn("Costa's Meat Market", self.llms_txt)
        self.assertIn("2169 Davenport Blvd", self.llms_txt)
        self.assertIn("863", self.llms_txt)
        self.assertIn("Picanha", self.llms_txt)


SITE = "https://costasmeatmarket.com"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read(rel_path):
    with open(os.path.join(BASE_DIR, rel_path), "r", encoding="utf-8") as f:
        return f.read()


def url_to_file(url):
    """Map a site URL or root-relative path to the file that serves it."""
    path = url.replace(SITE, "", 1).split("?")[0].split("#")[0] or "/"
    rel = path.lstrip("/")
    if path.endswith("/"):
        rel = os.path.join(rel, "index.html")
    return rel


def all_html_files():
    found = []
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "Claude outputs"]
        for name in files:
            if name.endswith(".html"):
                found.append(os.path.relpath(os.path.join(root, name), BASE_DIR))
    return sorted(found)


def alternates(page_html):
    return dict(re.findall(r'<link rel="alternate" hreflang="([a-zA-Z-]+)" href="([^"]+)">', page_html))


def json_ld_blocks(page_html):
    blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page_html, re.DOTALL)
    return [json.loads(block) for block in blocks]


class TestMultilingualSiteAndBlog(unittest.TestCase):
    """Language versions, blog posts, internal links, sitemap coverage, and tracking."""

    @classmethod
    def setUpClass(cls):
        cls.sitemap_xml = read("sitemap.xml")
        root = ET.fromstring(cls.sitemap_xml)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        cls.sitemap_locs = [elem.text for elem in root.findall("sm:url/sm:loc", ns)]
        cls.html_files = all_html_files()
        cls.indexable = [f for f in cls.html_files if not f.startswith("go" + os.sep)]

    def test_home_page_exists_in_every_language(self):
        """English, Spanish and Portuguese home pages exist, declare their language and point at each other."""
        expected = {"en": SITE + "/", "es": SITE + "/es/", "pt": SITE + "/pt/"}
        for lang, url in expected.items():
            page = read(url_to_file(url))
            self.assertRegex(page, r'<html lang="%s' % lang)
            self.assertIn('<link rel="canonical" href="%s">' % url, page)
            alts = alternates(page)
            for other, other_url in expected.items():
                self.assertEqual(alts.get(other), other_url, "%s home must link to %s" % (lang, other))
            self.assertEqual(alts.get("x-default"), SITE + "/")

    def test_hreflang_links_are_reciprocal(self):
        """Every hreflang alternate exists and links back to the page that references it."""
        for rel in self.indexable:
            page = read(rel)
            canonical = re.search(r'<link rel="canonical" href="([^"]+)">', page)
            alts = alternates(page)
            if not alts:
                continue
            self.assertIsNotNone(canonical, rel)
            self.assertIn(canonical.group(1), alts.values(), "%s must list itself in hreflang" % rel)
            for lang, url in alts.items():
                target = url_to_file(url)
                self.assertTrue(os.path.exists(os.path.join(BASE_DIR, target)), "%s -> missing %s" % (rel, url))
                self.assertIn(canonical.group(1), alternates(read(target)).values(),
                              "%s (%s) does not link back to %s" % (url, lang, rel))

    def test_every_indexable_page_has_core_seo_tags(self):
        """Each public page has a title, description, canonical and valid JSON-LD."""
        for rel in self.indexable:
            page = read(rel)
            self.assertRegex(page, r"<title>.{15,}</title>", rel)
            self.assertRegex(page, r'<meta name="description" content=".{50,}">', rel)
            self.assertRegex(page, r'<link rel="canonical" href="https://costasmeatmarket\.com/', rel)
            for block in json_ld_blocks(page):
                self.assertEqual(block.get("@context"), "https://schema.org", rel)

    def test_blog_posts_have_article_schema_in_the_page_language(self):
        """Blog posts carry BlogPosting schema whose language matches the page."""
        posts = [f for f in self.indexable if re.match(r"^((es|pt)/)?blog/[^/]+/index\.html$", f.replace(os.sep, "/"))]
        self.assertGreaterEqual(len(posts), 10)
        for rel in posts:
            page = read(rel)
            html_lang = re.search(r'<html lang="([^"]+)"', page).group(1)
            graph = json_ld_blocks(page)[0]["@graph"]
            article = next(item for item in graph if item.get("@type") == "BlogPosting")
            self.assertEqual(article["inLanguage"], html_lang, rel)
            self.assertTrue(article["headline"], rel)
            self.assertIn('property="og:type" content="article"', page, rel)

    def test_internal_links_resolve(self):
        """Every root-relative link and asset points at a file that exists."""
        for rel in self.html_files:
            page = read(rel)
            for ref in re.findall(r'(?:href|src)="(/[^"]*)"', page):
                if ref.startswith("//"):
                    continue
                target = url_to_file(ref)
                self.assertTrue(os.path.exists(os.path.join(BASE_DIR, target)), "%s links to missing %s" % (rel, ref))

    def test_sitemap_matches_pages(self):
        """The sitemap lists every public page and nothing that doesn't exist."""
        for loc in self.sitemap_locs:
            self.assertTrue(os.path.exists(os.path.join(BASE_DIR, url_to_file(loc))), "sitemap lists missing " + loc)
        listed = {url_to_file(loc) for loc in self.sitemap_locs}
        for rel in self.indexable:
            self.assertIn(rel.replace(os.sep, "/"), listed, rel + " is missing from sitemap.xml")
        self.assertFalse([loc for loc in self.sitemap_locs if "/go/" in loc], "short links must stay out of the sitemap")

    def test_short_links_are_noindex_and_tagged(self):
        """The /go/ short links used in bios and QR codes carry UTM tags and stay out of the index."""
        short_links = [f for f in self.html_files if f.startswith("go" + os.sep)]
        self.assertGreaterEqual(len(short_links), 5)
        for rel in short_links:
            page = read(rel)
            self.assertIn('content="noindex, follow"', page, rel)
            self.assertRegex(page, r"utm_source=[a-z_]+&amp;utm_medium=[a-z]+&amp;utm_campaign=[a-z_]+", rel)

    def test_tracking_is_on_every_public_page(self):
        """Clarity and the click/source tracker load on every public page, including the socials hub."""
        for rel in self.indexable:
            page = read(rel)
            self.assertIn('"clarity", "script", "yjadt0p2o2"', page, rel)
            self.assertIn('<script src="/assets/js/track.js" defer></script>', page, rel)


if __name__ == "__main__":
    unittest.main()
