/*
  AUTHOR: Matteo Verzeroli
 */

var subsribeOptions = {
    userVisibleOnly: true
}

Notification.requestPermission().then(function (permission) {

    if (permission === "granted") {
        navigator.serviceWorker.ready.then(function (registration) {
            return registration.pushManager.subscribe(subsribeOptions);
        }).then(function (subscription) {
            console.log(subscription)
        });
    }
})
