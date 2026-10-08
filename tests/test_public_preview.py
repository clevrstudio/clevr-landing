from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, unittest
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self, text):
  super().__init__();self.links=[];self.noindex=False;self.feed(text)
 def handle_starttag(self, tag, attrs):
  a=dict(attrs)
  if tag=='meta' and a.get('name')=='robots':self.noindex='noindex' in a.get('content','')
  if tag in ['a','link','img','script','form']:
   for k in ['href','src','action']:
    if k in a:self.links.append(a[k])
class Preview(unittest.TestCase):
 def test_preview_contains_exactly_reviewed_pages(self):
  preview=ROOT/'preview'
  pages=list(preview.rglob('*.html'))
  self.assertEqual(len(pages),26)
  self.assertEqual(len(list((preview/'soluciones').glob('*/index.html'))),15)
  self.assertEqual(len(list((preview/'industrias').glob('*/index.html'))),7)
  for name in ['index.html','talleres.html','soluciones/index.html','industrias/index.html']:
   self.assertTrue((preview/name).is_file(),name)
 def test_preview_has_no_editorial_sources_or_internal_tools(self):
  excluded={'contenido','scripts','tests','docs','CLAUDE.md','.gitignore','.vercelignore','vercel.json','robots.txt','sitemap.xml','cotizador.html','__pycache__'}
  for path in (ROOT/'preview').rglob('*'):
   self.assertFalse(set(path.relative_to(ROOT/'preview').parts) & excluded,str(path))
 def test_preview_pages_remain_inside_preview_and_do_not_index(self):
  pages=list((ROOT/'preview').rglob('*.html'))
  for path in pages:
   with self.subTest(page=str(path)):
    page=Page(path.read_text());self.assertTrue(page.noindex)
    for url in page.links:
     parsed=urlsplit(url)
     if parsed.scheme or url.startswith('//') or not parsed.path:continue
     if parsed.path=='/agenda':continue
     self.assertTrue(parsed.path.startswith('/preview/'),url)
     target=ROOT/unquote(parsed.path.lstrip('/'))
     if target.is_dir():target/='index.html'
     self.assertTrue(target.is_file(),url)
 def test_noindex_header_is_scoped_to_preview(self):
  config=json.loads((ROOT/'vercel.json').read_text())
  self.assertEqual(config['headers'],[{'source':source,'headers':[{'key':'X-Robots-Tag','value':'noindex, nofollow'}]} for source in ['/preview/:path*','/preview/:path*/']])
  self.assertEqual(config['redirects'][0]['source'],'/agenda')
 def test_root_does_not_link_to_preview(self):
  for f in ['index.html','talleres.html','cotizador.html']:
   self.assertFalse(any('/preview' in x for x in Page((ROOT/f).read_text()).links))
if __name__=='__main__':unittest.main()
