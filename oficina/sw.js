const CACHE = 'clevr-hq-c9e45f1fad9b';
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const scope = self.registration.scope;
    const response = await fetch(scope);
    const html = await response.text();
    const manifest = await (await fetch(new URL('offline-assets.json', scope))).json();
    const assets = [...new Set([...manifest.map(path => new URL(path, scope).href), ...[...html.matchAll(/(?:src|href)="([^"#]+\.(?:js|css))"/g)].map(match => new URL(match[1], scope).href)])];
    const cache = await caches.open(CACHE);
    await cache.put(scope, new Response(html, { headers: { 'Content-Type': 'text/html' } }));
    await cache.addAll(assets);
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', event => event.waitUntil((async () => {
  for (const key of await caches.keys()) if (key.startsWith('clevr-hq-') && key !== CACHE) await caches.delete(key);
  await self.clients.claim();
})()));
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET' || new URL(event.request.url).origin !== self.location.origin) return;
  event.respondWith((async () => {
    const cached = await caches.match(event.request);
    if (cached) return cached;
    try { return await fetch(event.request); }
    catch (error) {
      if (event.request.mode === 'navigate') return (await caches.match(self.registration.scope)) || Response.error();
      throw error;
    }
  })());
});
