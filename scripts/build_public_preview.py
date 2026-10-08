"""Freeze a reviewed static site under /preview/ without changing production URLs."""
from pathlib import Path
from urllib.parse import urlsplit, urljoin
import json, re, shutil, subprocess, sys
source = Path(sys.argv[1]).resolve()
root = Path(__file__).resolve().parents[1]
dest = root / 'preview'
exclude = {'.git', '.vercel', '.DS_Store', 'CLAUDE.md', 'contenido', 'scripts', 'tests', 'docs', 'robots.txt', 'sitemap.xml', 'vercel.json', '.vercelignore', '.gitignore', 'cotizador.html'}

def relocate(url, page):
    if not url or url.startswith('#') or urlsplit(url).scheme or url.startswith('//'):
        return url
    absolute = urljoin('/' + page, url)
    if absolute.split('?')[0].split('#')[0] == '/agenda':
        return url
    return '/preview' + absolute

tracked = subprocess.check_output(['git', '-C', str(source), 'ls-files', '-z']).decode().split('\0')
for filename in filter(None, tracked):
    path = source / filename
    relative = path.relative_to(source)
    if any(part in exclude or part == '__pycache__' for part in relative.parts) or not path.is_file():
        continue
    target = dest / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == '.html':
        html = path.read_text()
        html = re.sub(r'\b(href|src|action)=("|\')(.*?)\2', lambda m: m[1] + '=' + m[2] + relocate(m[3], str(relative)) + m[2], html)
        html = re.sub(r'<meta\s+name=["\']robots["\'][^>]*>', '', html, flags=re.I)
        html = html.replace('</head>', '<meta name="robots" content="noindex, nofollow">\n</head>', 1)
        target.write_text(html)
    elif path.suffix == '.css':
        css = re.sub(r'url\(["\']?(/[^)"\']+)["\']?\)', lambda m: 'url("/preview' + m[1] + '")', path.read_text())
        target.write_text(css)
    elif path.name == 'site.webmanifest':
        manifest = json.loads(path.read_text())
        for icon in manifest.get('icons', []):
            icon['src'] = relocate(icon['src'], str(relative))
        target.write_text(json.dumps(manifest, ensure_ascii=False))
    else:
        shutil.copyfile(path, target)
print(f'Preview frozen from {source}: {len(list(dest.rglob("*.html")))} HTML pages')
