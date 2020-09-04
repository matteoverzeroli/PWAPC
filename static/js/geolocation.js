//AUTHOR: Matteo Verzeroli

var geolocationApi = false;
//Geolocalization API
if ("geolocation" in navigator) {
    geolocationApi = true;
    console.log("Geolocation API found");
} else {
    geolocationApi = false;
    alert("No geolocation API found");
}

document.getElementById("btn-position").addEventListener("click", send_my_position);

function send_my_position() {
    if (geolocationApi) {
        navigator.geolocation.getCurrentPosition(
            geo_success,
            geo_error
        );

        function geo_success(position) {
            console.log("Lat: ", position.coords.latitude);
            console.log("Long: ", position.coords.longitude);
            $.ajax({
                method: 'POST',
                url: '/set_user_position',
                data: JSON.stringify({"lat": position.coords.latitude, "long": position.coords.longitude}),
                contentType: 'application/json',
                dataType: 'json',
                async: true,
            }).done(function () {
                alert("Posizione inviata !")
            });

        }

        function geo_error(error) {
            alert("Errore nella localizzazione")
        }
    }
}

