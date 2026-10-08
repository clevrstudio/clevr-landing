# Preview temporal público Clevr

Usuario autorizó el 08-10-2026 publicar v2 temporal en /preview/, conservando portada actual. Rama feat/public-preview-v2 desde origin/main e4af397. La homepage live difería de main: se recuperó index público exactamente y tres imágenes públicas faltantes; talleres/cotizador exactos, 28 assets locales de raíz contrastados con live sin diferencias adicionales. No se publica el catálogo como rutas oficiales todavía.

/preview es snapshot del commit v2 03c6fdc, generado con scripts/build_public_preview.py desde clon Clevr-Web. El script copia solo archivos tracked y excluye fuentes/tests/credenciales/config. Navegación local y assets prefijados, /agenda conserva destino público. 26 HTML con noindex,nofollow; X-Robots-Tag solo /preview/:path*. Preview no se agrega a sitemap y no hay enlaces desde raíz. Manifest ajustado a preview.

Verificación local: tres tests, 26 páginas HTTP200, referencias sin faltantes; portada 390px sin overflow e imágenes cargadas. Revisión read-only Sol confirmó raíz byte-identical live y navegación aislada. Usuario autorizó despliegue temporal en main, no publicación definitiva del catálogo. Tras merge comprobar anonimato, headers y raíz. Para quitar preview retirar carpeta y regla headers, conservando recuperación de portada. PR #1 de catálogo sigue draft y no se mergea con este cambio.

Actualización: CI del OS contiene credenciales Alan con acceso a clevr-landing; verificar ese mecanismo antes de concluir bloqueo por login local. autoAssignCustomDomains=false, builds production no se asignan solos al dominio. Promoción autorizada realizada desde workflow aislado, sin modificar main del OS. Header necesita matcher explícito para barra final; HTML preview ya noindex.
