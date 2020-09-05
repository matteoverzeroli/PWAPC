//AUTHOR: Matteo Verzeroli

document.getElementById("btn-position").addEventListener("click", send_my_position);
document.getElementById("btn-position-continuos").addEventListener("click", send_my_position_continuos);


var geolocationApi = false;
var geo_options = {
    enableHighAccuracy: true,
    maximumAge: 100,
    timeout: 30000
}

function set_pos_object(position) {
    var pos = {};
    pos['lat'] = position.coords.latitude;
    pos['long'] = position.coords.latitude;

    position.coords.accuracy = pos['acc'] = position.coords.accuracy;
    position.coords.altitude = pos['alt'] = position.coords.altitude;
    position.coords.altitude = pos['accalt'] = position.coords.altitudeAccuracy;
    position.coords.heading = pos['heading'] = position.coords.heading;
    position.coords.speed = pos['speed'] = position.coords.speed;

    return pos;
}

//Geolocalization API
if ("geolocation" in navigator) {
    geolocationApi = true;
    console.log("Geolocation API found");
} else {
    geolocationApi = false;
    alert("No geolocation API found");
}


//single position sender
function send_my_position() {
    if (geolocationApi) {
        navigator.geolocation.getCurrentPosition(
            geo_success,
            geo_error,
            geo_options
        );

        function geo_success(position) {
            console.log("Lat: ", position.coords.latitude);
            console.log("Long: ", position.coords.longitude);
            console.log("Altitude: ", position.coords.altitude);
            console.log("Accuracy: ", position.coords.accuracy);
            console.log("Altaccuracy: ", position.coords.altitudeAccuracy);
            console.log("Heading: ", position.coords.heading);
            console.log("Speed: ", position.coords.speed);

            $.ajax({
                method: 'POST',
                url: '/set_user_position',
                data: JSON.stringify(set_pos_object(position)),
                contentType: 'application/json',
                dataType: 'json',
                async: true,
                error: function () {
                    alert("Posizione non inviata !")
                }
            })
        }

        function geo_error(error) {
            alert("Errore nella localizzazione")
        }
    }
}

//continuos position sender
var watchId;

function send_my_position_continuos() {
    if (document.getElementById("label-btn-position-continuos").classList.contains("text-green")) {
        if (geolocationApi) {
            watchId = navigator.geolocation.watchPosition(
                geo_success,
                geo_error,
                geo_options
            );

            function geo_success(position) {
                console.log("Lat: ", position.coords.latitude);
                console.log("Long: ", position.coords.longitude);
                console.log("Altitude: ", position.coords.altitude);
                console.log("Accuracy: ", position.coords.accuracy);
                console.log("Altaccuracy: ", position.coords.altitudeAccuracy);
                console.log("Heading: ", position.coords.heading);
                console.log("Speed: ", position.coords.speed);

                $.ajax({
                    method: 'POST',
                    url: '/set_user_position',
                    data: JSON.stringify(set_pos_object(position)),
                    contentType: 'application/json',
                    dataType: 'json',
                    async: true,
                    error: function () {
                        document.getElementById("label-btn-position-continuos").classList.remove("text-green");
                        document.getElementById("label-btn-position-continuos").classList.remove("text-danger");
                        document.getElementById("label-btn-position-continuos").classList.add("text-warning");
                        document.getElementById("label-btn-position-continuos").innerText = "Stop condivisione percorso !"
                    },
                    success: function () {
                        document.getElementById("label-btn-position-continuos").classList.remove("text-green");
                        document.getElementById("label-btn-position-continuos").classList.add("text-danger");
                        document.getElementById("label-btn-position-continuos").innerText = "Stop condivisione percorso !"
                    }
                })
            }

            function geo_error(error) {
                alert("Errore nella localizzazione")
            }
        }


    } else {
        navigator.geolocation.clearWatch(watchId);
        document.getElementById("label-btn-position-continuos").classList.add("text-green");
        document.getElementById("label-btn-position-continuos").classList.remove("text-danger");
        document.getElementById("label-btn-position-continuos").innerText = "Avvia condivisione percorso !";
    }
}

