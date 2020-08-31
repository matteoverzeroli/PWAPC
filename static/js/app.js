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

//Geolocalization API
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
        geo_success,
        geo_error
    );
} else {
    alert("No geo")
}

function geo_success(position) {
    console.log("Lat: ", position.coords.latitude);
    console.log("Long: ", position.coords.longitude);
}

function geo_error(error) {
    alert("Errore")
}