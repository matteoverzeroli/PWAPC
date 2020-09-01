/*
  AUTHOR: Matteo Verzeroli FROM BOOK Building Progressive Web Apps: Bringing the Power of Native to the Browser
 */

$(document).ready(function () {
    if ("Notification" in window &&
        "PushManager" in window &&
        "serviceWorker" in navigator) {
        subscribeUserToNotifications();
    }
});
var urlBase64ToUint8Array = function (base64String) {
    var padding = "=".repeat((4 - base64String.length % 4) % 4);
    var base64 = (base64String + padding).replace(/\-/g, "+").replace(/_/g, "/");
    var rawData = window.atob(base64);
    var outputArray = new Uint8Array(rawData.length);
    for (var i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
};

var subscribeUserToNotifications = function () {
    Notification.requestPermission().then(function (permission) {
        if (permission === "granted") {
            var subscribeOptions = {
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(
                    "BI7rQbu-DoXBJ_3vM9JtwKzGqWkQUYTAlw-WbHrTqMLKIBgCCYRrM2He8I9tEeyyaYdNFelxqsunVVAFVsuAiWM" // VAPID PUBLIC KEY
                )
            };
            navigator.serviceWorker.ready.then(function (registration) {
                return registration.pushManager.subscribe(subscribeOptions);
            }).then(function (subscription) {
                $.ajax({
                    url: '/add_user_subscription',
                    type: 'POST',
                    data: JSON.stringify(subscription),
                    contentType: 'application/json',
                    dataType: 'json',
                    async: true
                })
            });
        }
    });
};