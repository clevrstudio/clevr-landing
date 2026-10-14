# Preview temporal público Clevr

Usuario autorizó el 08-10-2026 publicar v2 temporal en /preview/, conservando portada actual. Rama feat/public-preview-v2 desde origin/main e4af397. La homepage live difería de main: se recuperó index público exactamente y tres imágenes públicas faltantes; talleres/cotizador exactos, 28 assets locales de raíz contrastados con live sin diferencias adicionales. No se publica el catálogo como rutas oficiales todavía.

/preview es snapshot del commit v2 03c6fdc, generado con scripts/build_public_preview.py desde clon Clevr-Web. El script copia solo archivos tracked y excluye fuentes/tests/credenciales/config. Navegación local y assets prefijados, /agenda conserva destino público. 26 HTML con noindex,nofollow; X-Robots-Tag solo /preview/:path*. Preview no se agrega a sitemap y no hay enlaces desde raíz. Manifest ajustado a preview.

Verificación local: tres tests, 26 páginas HTTP200, referencias sin faltantes; portada 390px sin overflow e imágenes cargadas. Revisión read-only Sol confirmó raíz byte-identical live y navegación aislada. Usuario autorizó despliegue temporal en main, no publicación definitiva del catálogo. Tras merge comprobar anonimato, headers y raíz. Para quitar preview retirar carpeta y regla headers, conservando recuperación de portada. PR #1 de catálogo sigue draft y no se mergea con este cambio.

Actualización: CI del OS contiene credenciales Alan con acceso a clevr-landing; verificar ese mecanismo antes de concluir bloqueo por login local. autoAssignCustomDomains=false, builds production no se asignan solos al dominio. Promoción autorizada realizada desde workflow aislado, sin modificar main del OS. Header necesita matcher explícito para barra final; HTML preview ya noindex.

## Preview corregida tras revisión Alan, 08-10-2026

Basada en feat/public-preview-v2 6884301. Restaurado noindex meta en26 páginas y headerscon/sintrailingslash. Agendaapunta/agenda. Seeliminaronfuentesinternasdelartifact, previewmantiene26páginas15soluciones7industrias. ConservaexploradorAlanMed&Health/Finance/RealEstate/B2B; índicealineado4pilares+otrasaplicaciones,schema8ItemList. RetailB2B,catálogovisiblemobile/sinJS,desarrollosenpráctica,mockupilustrativo. Cinco pruebasmásvalidaciónJSON/metadata/fragmentosPASSlocally; HTTP público debeverificarsedespuéspromoción. Portadaoficial/talleres/cotizadoridénticosorigin/main.

## Oficina virtual de Clevr, 14-10-2026

Benjamín autorizó alojar la demo ETM en clevr.cl para compartir con el equipo. Se añade únicamente `oficina/` (build estático de `clevr-comercial/clevr-agent-hq`) y headers scoped noindex/nofollow, con service worker limitado a `/oficina/`. Incluye oficina ampliada, 16 subagentes por módulo/cliente, ocho logos originales, nueve clientes/proyectos y respuestas locales. Buenaventura conserva identificación textual al no haber logo original disponible y se identifica como Propuesta.

La portada pública al iniciar sigue el commit f484b64 (SHA256 d37f80464ecbd196ba3515396e72887cd64077ced11eef56ac9696ed13bd53fc), aunque main contiene después el rename de marketing en3a512e6. El despliegue de oficina debe tomar el baseline público f484b64 y superponer solo `oficina/` y `vercel.json` para preservar el contenido actual de producción. No promover directamente el Git deploy de main si cambia la portada. Usar workflow aislado OS con credenciales del proyecto web y restaurar autoAssignCustomDomains=false después de promover. Estado y enlace público quedan registrados en handoff Clevr tras verificación.

Primera publicación pública verificada: workflow OS38619703772 SUCCESS, deployment clevr-landing-goctjyodo-alans-projects-ab124748.vercel.app. `/oficina/`200 sin login,19assets byte-identical, portada/talleres/cotizador preservados, autoAssignCustomDomains restauradofalse. Auditorías posteriores Gemini/Terra corrigieron foco por cliente/módulo, QR en reposo, ajuste de tarjetas móvil e instrucción touch; se actualiza artifact de oficina, con el mismo aislamiento de la portada.

Publicación final de oficina completada: https://www.clevr.cl/oficina/200 anónimo. Workflow38620480664SUCCESS, deployment clevr-landing-r6zte5sik-alans-projects-ab124748.vercel.app, artifact1495bc4 sobre baselinef484b64.19assets y worker byte-identical; portada/talleres/cotizador preservados, agendaintacta, autoAssignCustomDomains=false restaurado. Browser público confirma nueveclientes, sus módulos, QRreposo y recargaoffline conlogos; sinerroresJS ni desborde390px. Auditado conSol,Luna,Gemini3.8Flash yTerra5.6; corregidos focoporclienteymodulo ytarjetas. No se promueven otroscambiosprevios dehomepage. Siguiente: equipo revisa enlace y prueba enmonitor delstand.

## Explorador de oficinas por cliente, 14-10-2026

Actualizado artifact de oficina: nueve oficinas independientes, 22 subagentes, cámara con arrastre, rueda/pinch, minimapa y vista general. Logos y módulos por cliente; interfaz inicial enfocada para legibilidad. Build OFFICE_BASE=/oficina/. Browser local verifica nueve selecciones sin remontar canvas, zoom/minimapa/terminal y móvil390px sin overflow ni errores JS. Publicar con baselinef484b64 y workflow aislado, preservando portada.

Publicación del explorador verificada: workflow 38643372335 SUCCESS, artifact f839661, deployment clevr-landing-p28lvqaxn-alans-projects-ab124748.vercel.app. Nueve oficinas y 22 subagentes públicos en /oficina/. Los 19 assets y el worker coinciden byte a byte; portada, talleres y cotizador preservados. autoAssignCustomDomains=false restaurado. Auditoría visual Gemini 3.8 Flash supervisada por Luna; motor y offline verificados por Sol. El primer preflight 38643238336 detectó rutas relativas antes de desplegar; recompilar con base explícita corrigió el artifact. Siguiente: probar en monitor físico.
