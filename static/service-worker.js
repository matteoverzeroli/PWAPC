const CACHE_NAME = 'static-cache-v0'; //use version to upgrade offline caches

const FILES_TO_CACHE = [
    "/static/offline.html",
    "/static/css/styles_homepage.css",
    "/static/js/app.js"
];

//install service worker and caching
self.addEventListener('install', (evt) => {
    console.log('[ServiceWorker] Install');
    evt.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[ServiceWorker] Pre-caching offline page');
            return cache.addAll(FILES_TO_CACHE);
        })
    );
});

// activate service worker and clear old service worker

self.addEventListener('activate', (evt) => {
    console.log('[ServiceWorker] Activate');
    evt.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME) {
                    console.log('[ServiceWorker] Removing old cache', key);
                    return caches.delete(key);
                }
            }));
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', function (event) {
    event.respondWith(
        fetch(event.request).catch(function () { //added ignoresearch to avoid URL problem -> see page 67 book
            return caches.match(event.request, {ignoreSearch: true}).then(function (response) {
                if (response) {
                    return response;
                } else if (event.request.headers.get("accept").includes("text/html")) {
                    return caches.match("/static/offline.html", {ignoreSearch: true})
                }
            })
        })
    );
});


self.addEventListener("push", function (event) {
    self.registration.showNotification(event.data.text());
})

/*
self.addEventListener('sync', function(event) {
    console.log("Ok")
  if (event.tag == 'myFirstSync') {
    event.waitUntil(doSomeStuff());
  }
});


function doSomeStuff() {
    fetch('192/set_user_position')
      .then(function (response) {
        return response;
      })
      .then(function (text) {
        console.log('Request successful', text);
      })
      .catch(function (error) {
        console.log('Request failed', error);
      });
}
*/