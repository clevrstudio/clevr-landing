"""Contract checks for publicly crawlable solution and industry pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://www.clevr.cl'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.h1s = 0
        self.canonical = []
        self.links = []
        self.meta = {}
        self.title = ''
        self.in_title = False
        self.schemas = []
        self.in_schema = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1': self.h1s += 1
        if tag == 'title': self.in_title = True
        if tag == 'meta': self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical.append(attrs.get('href'))
        if tag in ('a', 'link', 'img'): self.links.append(attrs.get('href', attrs.get('src', '')))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_schema = True
            self.schemas.append('')

    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'script': self.in_schema = False

    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_schema: self.schemas[-1] += data

class CrawlablePages(unittest.TestCase):
    def test_catalog_has_all_modules_and_distinct_industries(self):
        self.assertEqual(len(list((ROOT / 'soluciones').glob('*/index.html'))), 15)
        self.assertEqual(len(list((ROOT / 'industrias').glob('*/index.html'))), 7)
        self.assertTrue((ROOT / 'soluciones/index.html').exists())
        self.assertTrue((ROOT / 'industrias/index.html').exists())

    def test_search_engines_can_follow_pages_without_javascript(self):
        files = list((ROOT / 'soluciones').rglob('index.html')) + list((ROOT / 'industrias').rglob('index.html'))
        self.assertEqual(len(files), 24)
        sitemap = ET.parse(ROOT / 'sitemap.xml')
        urls = {node.text for node in sitemap.findall('.//{*}loc')}
        titles, descriptions = set(), set()
        for path in files:
            with self.subTest(page=str(path.relative_to(ROOT))):
                page = Page(path.read_text())
                url = ORIGIN + '/' + str(path.parent.relative_to(ROOT)) + '/'
                self.assertEqual(page.h1s, 1)
                self.assertEqual(page.canonical, [url])
                self.assertIn(url, urls)
                self.assertNotIn('noindex', page.meta.get('robots', ''))
                self.assertTrue(page.title)
                self.assertNotIn(page.title, titles)
                titles.add(page.title)
                description = page.meta.get('description', '')
                self.assertTrue(description)
                self.assertNotIn(description, descriptions)
                descriptions.add(description)
                self.assertTrue(page.schemas)
                for schema in page.schemas: json.loads(schema)
                self.assertIn('/agenda', page.links)
                for link in page.links:
                    parsed = urlsplit(link)
                    if parsed.scheme or not parsed.path or parsed.path == '/agenda': continue
                    target = ROOT / unquote(parsed.path.lstrip('/'))
                    if target.is_dir(): target /= 'index.html'
                    self.assertTrue(target.is_file(), f'Broken local link: {link}')

    def test_entities_describe_solutions_and_industries_correctly(self):
        for path in list((ROOT / 'soluciones').rglob('index.html')) + list((ROOT / 'industrias').rglob('index.html')):
            with self.subTest(page=str(path.relative_to(ROOT))):
                graph = json.loads(Page(path.read_text()).schemas[0])['@graph']
                ids = [node['@id'] for node in graph]
                self.assertEqual(len(ids), len(set(ids)))
                webpage = next(node for node in graph if node['@type'] in ('WebPage', 'CollectionPage'))
                entities = [node for node in graph if node['@type'] in ('Service', 'CreativeWork')]
                if path.parent.name == 'soluciones' or path.parent.name == 'industrias':
                    catalog = next(node for node in graph if node['@type'] == 'ItemList')
                    self.assertEqual(webpage['mainEntity']['@id'], catalog['@id'])
                    expected = 15 if path.parent.name == 'soluciones' else 7
                    self.assertEqual(len(catalog['itemListElement']), expected)
                elif 'soluciones' in path.parts:
                    self.assertEqual(len(entities), 1)
                    entity = entities[0]
                    self.assertEqual(webpage['mainEntity']['@id'], entity['@id'])
                    self.assertIn('creator' if entity['@type'] == 'CreativeWork' else 'provider', entity)
                else:
                    self.assertFalse(entities, 'An industry page must not pretend to be a service')
                    self.assertTrue(webpage['mentions'])
                breadcrumb = next(node for node in graph if node['@type'] == 'BreadcrumbList')
                items = breadcrumb['itemListElement']
                self.assertEqual([item['position'] for item in items], list(range(1, len(items) + 1)))
                self.assertEqual(items[-1]['item'], webpage['url'])

    def test_sitemap_matches_public_pages_and_root_canonicals(self):
        expected = {ORIGIN + '/', ORIGIN + '/talleres.html'}
        for directory in ('soluciones', 'industrias'):
            expected.update(ORIGIN + '/' + str(p.parent.relative_to(ROOT)) + '/' for p in (ROOT / directory).rglob('index.html'))
        urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')]
        self.assertEqual(set(urls), expected)
        self.assertEqual(len(urls), len(set(urls)))
        for filename, url in [('index.html', ORIGIN + '/'), ('talleres.html', ORIGIN + '/talleres.html')]:
            page = Page((ROOT / filename).read_text())
            self.assertEqual(page.canonical, [url])
            self.assertNotIn('noindex', page.meta.get('robots', ''))

    def test_internal_quote_tool_is_not_indexable(self):
        page = Page((ROOT / 'cotizador.html').read_text())
        self.assertIn('noindex', page.meta.get('robots', ''))
        urls = {node.text for node in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')}
        self.assertNotIn(ORIGIN + '/cotizador.html', urls)

if __name__ == '__main__': unittest.main()
