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


if __name__ == "__main__":
    unittest.main()
