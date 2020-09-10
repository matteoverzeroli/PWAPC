/*
    AUTHOR: Matteo Verzeroli
 */

//handles Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker
        .register('./service-worker.js')
        .then(function (registration) {
            console.log('Service Worker Registered!');
            return registration;
        })
        .catch(function (err) {
            console.error('Unable to register service worker.', err);
        });
}


/* for synch menager

 document.getElementById('requestButton').addEventListener('click', () => {
       navigator.serviceWorker.ready.then(function (swRegistration) {
    return swRegistration.sync.register('myFirstSync');
});})
*/