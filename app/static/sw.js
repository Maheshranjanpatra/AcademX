// Nymora Service Worker
const CACHE_NAME = 'nymora-v1';
const ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/landing.js',
  '/static/images/nymora.jpg',
  '/static/css/auth_login.css',
  '/static/css/admin_dashboard.css',
  '/static/js/auth_login.js',
  '/static/js/admin_dashboard.js'
];

// Install event - cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching Nymora assets...');
        return cache.addAll(ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      );
    })
  );
  return self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(cached => {
        if (cached) {
          // Return cached version, then update in background
          fetch(event.request).then(response => {
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, response);
            });
          }).catch(() => {});
          return cached;
        }
        return fetch(event.request)
          .then(response => {
            // Cache dynamic responses (HTML pages, etc.)
            if (event.request.url.includes('/qa/') || 
                event.request.url.includes('/quiz/') ||
                event.request.url.includes('/video/')) {
              const clone = response.clone();
              caches.open(CACHE_NAME).then(cache => {
                cache.put(event.request, clone);
              });
            }
            return response;
          })
          .catch(() => {
            // Offline fallback
            return caches.match('/offline');
          });
      })
  );
});
