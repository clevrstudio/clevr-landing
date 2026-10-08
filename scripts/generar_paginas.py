#!/usr/bin/env python3
"""Build crawlable HTML from the reviewed Clevr content, without a JS runtime."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://www.clevr.cl'
MODULES = json.loads((ROOT / 'contenido/modulos.json').read_text())
INDUSTRIES = json.loads((ROOT / 'contenido/industrias.json').read_text())
MAPPING = json.loads((ROOT / 'contenido/industria-modulos.json').read_text())
MODULE_BY_SLUG = {item['slug']: item for item in MODULES}
INDUSTRY_NAMES = {item['slug']: item['name'] for item in INDUSTRIES}

groups = [
    ('Finanzas y gestión de activos', [0, 1, 2, 3, 4, 5]),
    ('Ventas, atención y marketing', [7, 8, 9, 13]),
    ('Operación, documentos y calidad', [6, 10, 11]),
    ('Evaluación y educación', [12, 14])]

def e(value):
    return escape(str(value), quote=True)

def link(path, text, css=''):
    return f'<a class="{css}" href="{e(path)}">{e(text)}</a>'

def layout(path, title, description, h1, intro, body, section):
    url = ORIGIN + path
    schema = {
        '@context': 'https://schema.org', '@graph': [
            {'@type': 'Organization', '@id': ORIGIN + '/#organization', 'name': 'Clevr',
             'url': ORIGIN + '/', 'logo': ORIGIN + '/android-chrome-512x512.png',
             'email': 'contacto@clevr.cl', 'telephone': '+56 9 6898 7762',
             'sameAs': ['https://www.linkedin.com/company/softwarefactoryclevr/']},
            {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': title,
             'description': description, 'inLanguage': 'es-CL',
             'isPartOf': {'@id': ORIGIN + '/#website'},
             'publisher': {'@id': ORIGIN + '/#organization'},
             'breadcrumb': {'@id': url + '#breadcrumb'}},
            {'@type': 'WebSite', '@id': ORIGIN + '/#website', 'url': ORIGIN + '/', 'name': 'Clevr'},
            {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': ORIGIN + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': section,
                 'item': ORIGIN + ('/soluciones/' if section == 'Soluciones' else '/industrias/')},
            ]}
        ]}
    if path.count('/') > 2:
        schema['@graph'][-1]['itemListElement'].append(
            {'@type': 'ListItem', 'position': 3, 'name': h1, 'item': url})
    if path.startswith('/soluciones/') and path != '/soluciones/':
        entity_id = url + '#solution'
        schema['@graph'][1]['mainEntity'] = {'@id': entity_id}
        entity_type = 'CreativeWork' if path == '/soluciones/copiloto-docente/' else 'Service'
        entity = {'@type': entity_type, '@id': entity_id, 'name': h1, 'url': url,
                  'description': description,
                  'creator' if entity_type == 'CreativeWork' else 'provider': {'@id': ORIGIN + '/#organization'}}
        schema['@graph'].append(entity)
    if path in ('/soluciones/', '/industrias/'):
        schema['@graph'][1]['@type'] = 'CollectionPage'
        items = [MODULES[i] for _, indexes in groups for i in indexes] if path == '/soluciones/' else INDUSTRIES
        schema['@graph'][1]['mainEntity'] = {'@id': url + '#catalog'}
        schema['@graph'].append({'@type': 'ItemList', '@id': url + '#catalog',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': item['name'],
                                 'url': ORIGIN + path + item['slug'] + '/'} for i, item in enumerate(items)]})
    elif path.startswith('/industrias/'):
        slug = path.strip('/').split('/')[-1]
        schema['@graph'][1]['about'] = {'@id': ORIGIN + '/#organization'}
        schema['@graph'][1]['mentions'] = [{'@id': ORIGIN + '/soluciones/' + MODULES[i]['slug'] + '/#solution'} for i in MAPPING[slug]]
    structured = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    active = '/soluciones/' if section == 'Soluciones' else '/industrias/'
    breadcrumb = f'{link("/", "Inicio")}<span>/</span>{link(active, section)}'
    if path != active: breadcrumb += f'<span>/</span><span aria-current="page">{e(h1)}</span>'
    return f'''<!DOCTYPE html>
<html lang="es-CL"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
<link rel="canonical" href="{url}"><meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{ORIGIN}/android-chrome-512x512.png">
<meta property="og:locale" content="es_CL"><meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.ico"><link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/seo-pages.css"><script type="application/ld+json">{structured}</script></head>
<body><a class="skip-link" href="#contenido">Ir al contenido</a>
<header class="site-header"><a class="brand" href="/" aria-label="Clevr, inicio">clev<span class="brand-dot">r</span></a>
<nav aria-label="Navegación principal">{link('/soluciones/', 'Soluciones', 'active' if section == 'Soluciones' else '')}{link('/industrias/', 'Industrias', 'active' if section == 'Industrias' else '')}{link('/talleres.html', 'Capacitaciones')}{link('/agenda', 'Agendemos', 'nav-cta')}</nav></header>
<main id="contenido"><section class="page-hero"><div class="wrap"><nav class="breadcrumb" aria-label="Ruta de navegación">{breadcrumb}</nav>
<h1>{e(h1)}</h1><p class="intro">{e(intro)}</p><div class="hero-actions">{link('/agenda', 'Conversemos sobre tu proceso', 'button')}{link('/soluciones/' if section == 'Industrias' else '/industrias/', 'Explorar soluciones' if section == 'Industrias' else 'Ver aplicaciones por industria', 'text-link')}</div></div></section>
<div class="wrap content">{body}</div>
<section class="contact-band"><div class="wrap contact-inner"><div><h2>Partamos por tu operación</h2><p>Cuéntanos qué proceso quieres automatizar y qué herramientas usa hoy tu equipo.</p></div>{link('/agenda', 'Agendar una conversación', 'button')}</div></section></main>
<footer class="site-footer"><div class="wrap"><a class="brand" href="/">clev<span class="brand-dot">r</span></a><p>Transformación y automatización con IA en tu empresa.</p><nav aria-label="Enlaces del pie">{link('/soluciones/', 'Soluciones')}{link('/industrias/', 'Industrias')}{link('/talleres.html', 'Capacitaciones')}{link('mailto:contacto@clevr.cl', 'contacto@clevr.cl')}{link('https://wa.me/56968987762', 'WhatsApp')}</nav></div></footer></body></html>'''

def cards(items, prefix):
    return '<div class="catalog-grid">' + ''.join(
        f'<article class="catalog-item"><h3>{link(prefix + item["slug"] + "/", item["name"])}</h3><p>{e(item.get("summary", item["intro"]))}</p>{link(prefix + item["slug"] + "/", "Conocer la solución" if prefix == "/soluciones/" else "Ver aplicaciones", "text-link")}</article>'
        for item in items) + '</div>'

def write(path, html):
    dest = ROOT / path.lstrip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html + '\n')

for module in MODULES:
    flow = '<ol class="flow">' + ''.join(
        f'<li><span class="flow-label">{label}</span><p>{e(text)}</p></li>'
        for label, text in zip(('Datos de entrada', 'Proceso', 'Resultado'), module['flow'])) + '</ol>'
    sectors = ''.join(link('/industrias/' + slug + '/', INDUSTRY_NAMES[slug], 'sector-link') for slug in module['industries'])
    body = f'<section class="overview" id="alcance"><h2>Qué hace el módulo</h2><p>{e(module["body"])}</p></section><section id="como-funciona"><h2>Cómo funciona</h2>{flow}</section>'
    if sectors: body += f'<section class="sector-block"><h2>Aplicaciones por industria</h2><div class="sector-links">{sectors}</div></section>'
    body += '<section class="questions" id="preguntas"><h2>Preguntas sobre esta solución</h2>' + ''.join(
        f'<details><summary>{e(q["question"])}</summary><p>{e(q["answer"])}</p></details>' for q in module['faq']) + '</section>'
    if module.get('related'):
        body += '<section id="soluciones-relacionadas"><h2>Soluciones relacionadas</h2>' + cards([MODULE_BY_SLUG[slug] for slug in module['related']], '/soluciones/') + '</section>'
    if module.get('sources'):
        body += '<section id="referencias"><h2>Referencias del proyecto</h2><p>' + ' · '.join(link(source['url'], source['name'], 'text-link') for source in module['sources']) + '</p></section>'
    body += f'<section class="next-step"><h2>{e(module["cta"])}</h2>{link("/agenda", "Agendar una conversación", "text-link")}</section>'
    write('/soluciones/' + module['slug'] + '/', layout('/soluciones/' + module['slug'] + '/', module['title'], module['description'], module['h1'], module['intro'], body, 'Soluciones'))

for industry in INDUSTRIES:
    related = [MODULES[i] for i in MAPPING[industry['slug']]]
    body = f'<section class="overview"><h2>El proceso en tu industria</h2><p>{e(industry["problem"])}</p></section><section><h2>De la información al trabajo del equipo</h2><ol class="industry-flow">' + ''.join(f'<li><h3>{e(step["title"])}</h3><p>{e(step["text"])}</p></li>' for step in industry['process']) + '</ol></section>'
    body += '<section><h2>Soluciones que conectan este proceso</h2>' + cards(related, '/soluciones/') + '</section>'
    body += '<section class="questions" id="preguntas"><h2>Preguntas de tu equipo</h2>' + ''.join(f'<details><summary>{e(q["question"])}</summary><p>{e(q["answer"])}</p></details>' for q in industry['faq']) + '</section>'
    write('/industrias/' + industry['slug'] + '/', layout('/industrias/' + industry['slug'] + '/', industry['title'], industry['description'], industry['h1'], industry['intro'], body, 'Industrias'))

body = ''.join('<section class="catalog-section"><h2>' + e(name) + '</h2>' + cards([MODULES[i] for i in indexes], '/soluciones/') + '</section>' for name, indexes in groups)
write('/soluciones/', layout('/soluciones/', 'Soluciones de IA y automatización para empresas | Clevr', 'Conoce 15 módulos desarrollados por Clevr: cobranza, conciliación, portales B2B, órdenes de compra, calidad e IA aplicada a tu operación.', 'Soluciones que parten de un proceso real', 'Hemos desarrollado módulos para automatizar procesos, conectar sistemas y trabajar con información. Explora qué hace cada solución y cómo se adapta a la operación de tu empresa.', body, 'Soluciones'))
write('/industrias/', layout('/industrias/', 'Automatización e IA por industria | Clevr', 'Aplicaciones de IA y automatización para inmobiliarias, laboratorios, distribución, manufactura, evaluación, gimnasios y educación.', 'La misma tecnología. Una operación distinta.', 'Cada industria trabaja con sus propios datos, herramientas y decisiones. Conoce las aplicaciones que hemos desarrollado y encuentra un punto de partida para tu equipo.', '<section><h2>Explora tu industria</h2>' + cards(INDUSTRIES, '/industrias/') + '</section>', 'Industrias'))

urls = ['/', '/talleres.html', '/soluciones/', '/industrias/'] + ['/soluciones/' + m['slug'] + '/' for m in MODULES] + ['/industrias/' + i['slug'] + '/' for i in INDUSTRIES]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{ORIGIN}{url}</loc></url>\n' for url in urls) + '</urlset>\n')
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + ORIGIN + '/sitemap.xml\n')
print(f'Generated {len(MODULES)} solutions, {len(INDUSTRIES)} industries and 2 directories; {len(urls)} sitemap URLs.')
