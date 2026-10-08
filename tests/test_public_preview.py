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
 def test_preview_pages_remain_inside_preview_and_do_not_index(self):
  pages=list((ROOT/'preview').rglob('*.html'))
  self.assertEqual(len(pages),26)
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
  self.assertEqual(config['headers'],[{'source':'/preview/:path*','headers':[{'key':'X-Robots-Tag','value':'noindex, nofollow'}]}])
  self.assertEqual(config['redirects'][0]['source'],'/agenda')
 def test_root_does_not_link_to_preview(self):
  for f in ['index.html','talleres.html','cotizador.html']:
   self.assertFalse(any('/preview' in x for x in Page((ROOT/f).read_text()).links))
if __name__=='__main__':unittest.main()
