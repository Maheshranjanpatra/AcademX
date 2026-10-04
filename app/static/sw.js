// AcademX Service Worker v4
const CACHE_NAME = 'academx-v4';
const PRECACHE = [
  '/static/css/tailwind.build.css',
  '/static/css/style.css',
  '/static/css/mobile_style.css',
  '/static/css/errors.css',
  '/static/css/spinner.css',
  '/static/js/spinner.js',
  '/static/js/mobile_nav.js',
  '/static/images/academx-mark.svg',
  '/static/manifest.json'
];

const OFFLINE_HTML = `<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AcademX</title>
<style>
  body{font-family:sans-serif;text-align:center;margin-top:20vh;color:#333;padding:1rem}
  button{padding:12px 24px;font-size:16px;border-radius:8px;
         border:1px solid #ccc;background:#f9f9f9;cursor:pointer;margin-top:1rem}
</style>
</head><body>
<h2 id="t">Waking AcademX up…</h2>
<p id="m">Couldn't reach the server. Retrying automatically.</p>
<button onclick="location.reload()">Retry now</button>
<script>
  var first = parseInt(sessionStorage.getItem('academx-wake-start') || '0', 10);
  var now = Date.now();
  if (!first) {
    first = now;
    sessionStorage.setItem('academx-wake-start', String(first));
  }
  var elapsed = now - first;
  if (elapsed < 30000) {
    setTimeout(function(){ location.reload(); }, 5000);
  } else {
    sessionStorage.removeItem('academx-wake-start');
    document.getElementById('t').textContent = "You're offline";
    document.getElementById('m').textContent =
      "Check your internet connection and tap Retry.";
  }
</script>
</body></html>`;

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => Promise.allSettled(PRECACHE.map(u => cache.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Message handler — MUST be at the top level, not inside fetch
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Pages: always network, friendly fallback if it fails or Render is cold
  if (req.mode === 'navigate') {
    const fallback = () => new Response(OFFLINE_HTML, {
      status: 200,
      headers: { 'Content-Type': 'text/html; charset=utf-8' }
    });
    event.respondWith(
      fetch(req)
        .then(res => [502, 503, 504].includes(res.status) ? fallback() : res)
        .catch(fallback)
    );
    return;
  }

  // Static files only: cache + background refresh
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(req).then(cached => {
        const net = fetch(req).then(res => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE_NAME).then(c => c.put(req, copy));
          }
          return res;
        }).catch(() => cached || new Response('', { status: 503 }));
        return cached || net;
      })
    );
  }
});
