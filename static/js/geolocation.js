//AUTHOR: Matteo Verzeroli

document.getElementById("btn-position").addEventListener("click", send_my_position);
document.getElementById("btn-position-continuos").addEventListener("click", send_my_position_continuos);

var geo_options = {
    enableHighAccuracy: true,
    maximumAge: 100,
    timeout: 30000
}

function set_pos_object(position, node) {
    var pos = {};
    pos['lat'] = position.coords.latitude;
    pos['long'] = position.coords.longitude;

    position.coords.accuracy = pos['acc'] = position.coords.accuracy;
    position.coords.altitude = pos['alt'] = position.coords.altitude;
    position.coords.altitude = pos['accalt'] = position.coords.altitudeAccuracy;
    position.coords.heading = pos['heading'] = position.coords.heading;
    position.coords.speed = pos['speed'] = position.coords.speed;

    pos['node'] = node;
    pos['date'] = new Date().toLocaleString('it-IT', {
        hour12: false,
    });
    return pos;
}

//Geolocalization API
if ("geolocation" in navigator) {
    console.log("Geolocation API found");
} else {
    alert("No geolocation API found");
}


//single position sender
function send_my_position() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            geo_success,
            geo_error,
            geo_options
        );

        function geo_success(position) {
            $.ajax({
                method: 'POST',
                url: '/set_user_position',
                data: JSON.stringify(set_pos_object(position, null)),
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
var node = 'I';

function send_my_position_continuos() {
    if (document.getElementById("label-btn-position-continuos").classList.contains("text-green")) {
        if ("geolocation" in navigator) {
            watchId = navigator.geolocation.watchPosition(
                geo_success,
                geo_error,
                geo_options
            );

            function geo_success(position) {

                $.ajax({
                    method: 'POST',
                    url: '/set_user_position',
                    data: JSON.stringify(set_pos_object(position, node)),
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
                        node = 'C'
                    }
                })
            }

            function geo_error(error) {
                alert("Errore nella localizzazione")
            }
        }


    } else {
        navigator.geolocation.clearWatch(watchId);

        navigator.geolocation.getCurrentPosition(
            geo_success,
            geo_error,
            geo_options
        )

        function geo_success(position) {
            $.ajax({
                method: 'POST',
                url: '/set_user_position',
                data: JSON.stringify(set_pos_object(position, 'F')),
                contentType: 'application/json',
                dataType: 'json',
                async: true,
                error: function () {
                    alert("Ultima posizione non inviata !")
                },
                success: function () {
                    document.getElementById("label-btn-position-continuos").classList.add("text-green");
                    document.getElementById("label-btn-position-continuos").classList.remove("text-danger");
                    document.getElementById("label-btn-position-continuos").innerText = "Avvia condivisione percorso !";
                    node = 'S';
                }
            })
        }

        function geo_error(error) {
            alert("Errore nella localizzazione")
        }
    }
}

//todo da sistemare con local storage per lo stato della condivisione dopo che ho chiuso l'app