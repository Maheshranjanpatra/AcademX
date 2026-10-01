// Nymora Service Worker
const CACHE_NAME = 'nymora-v2';
const ASSETS = [
  '/',
  '/static/css/tailwind.build.css',
  '/static/css/style.css',
  '/static/css/mobile_style.css',
  '/static/css/errors.css',
  '/static/css/spinner.css',
  '/static/js/spinner.js',
  '/static/js/mobile_nav.js',
  '/static/images/nymora.svg',
  '/static/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS).catch(() => {}))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    )
  );
  return self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      const networkFetch = fetch(event.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => {
        if (cached) return cached;
        if (event.request.headers.get('accept')?.includes('text/html')) {
          return caches.match('/offline');
        }
        return new Response('', { status: 503 });
      });

      return cached || networkFetch;
    })
  );
});
