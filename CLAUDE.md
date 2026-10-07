# Web pública de Clevr

Repositorio: `clevrstudio/clevr-landing`. HTML/CSS/JS estáticos, Vercel. No necesita npm ni build de aplicación.

Contexto personal: `~/benjamin-os/IDENTITY.md`, `FRENTES.md` y memoria Clevr. Registro comercial y auditoría: `~/Documents/Clevr/interno/web-seo-2026-10/`. Nunca copiar a este repo público dossiers, contratos, credenciales o atribuciones privadas de clientes.

## Páginas y contenido

`contenido/modulos.json`: 15 soluciones. `contenido/industrias.json`: siete industrias. `contenido/industria-modulos.json`: enlaces entre sectores y módulos. `scripts/generar_paginas.py` genera HTML estático, directorios, sitemap y robots. Las fuentes editoriales y scripts se excluyen de Vercel mediante `.vercelignore`, pero viven versionados.

Benjamín confirmó el 07-10-2026 que los 15 módulos se presentan como desarrollados. No inventar resultados, ahorros, precisión, marcas de ERP ni clientes específicos. Los logos van separados del catálogo. Maestro AI es proyecto propio, no afirmar despliegues escolares ni resultados académicos.

```
python3 scripts/generar_paginas.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8766 --bind 127.0.0.1
```

La salida tiene 15 páginas de soluciones, siete de industrias y dos índices. Sitemap incluye esas 24 más home y talleres. Canonical: `https://www.clevr.cl`, siguiendo el dominio servido actualmente. Cotizador interno tiene noindex; esto no es autenticación.

## Estado 07-10-2026

Rama `feat/seo-soluciones-industrias-2026-10-07`. Se recuperó primero la homepage pública porque difería de main: diseño de canvas, bloque de adopción de IA y assets públicos adicionales. El commit de recuperación preserva ese baseline antes de los cambios SEO. No se probó el origen del desfase; no sustituir esta portada por una copia antigua de main.

Se agregaron nuevas páginas, navegación, canonical/Open Graph/JSON-LD, robots y sitemap, noindex del cotizador, imágenes WebP y dimensiones/loading en home/talleres. No se cambiaron formularios ni destino de agenda.

Validación inicial: tres pruebas pasan; 26 URLs del sitemap responden 200 en servidor local. Render revisado en Chrome a 1440 y 390 px, sin desbordamiento en muestras de catálogo, industria y módulo; FAQ abre y no presenta errores de consola en módulo revisado. No hay datos GSC ni puntaje PageSpeed (API 429).

La cuenta Vercel disponible es de Benjamín y no tiene acceso al proyecto de Alan. No se ha publicado esta rama. Antes de producción: revisión final del cambio, visto bueno de Benjamín para publicación y deploy por la cuenta autorizada. Verificar home, páginas, sitemap y agenda en dominio público después. No crear otro proyecto ni cambiar DNS para eludir acceso.
