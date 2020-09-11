function get_operation_info() {
    $.ajax({
        method: 'POST',
        url: '/get_operation_info',
        error: function () {
            alert("Errore richiesta dati intervento");
        },
        success: set_operation_info
    })
}

function set_operation_info(data) {

    if (data.operation_info == null) {
        document.getElementsByClassName("operation-elements").style = "hidden";
    } else {
        document.getElementsByClassName("operation-elements").style = "visible";

        if (data.operation_info.typology == 'E') {
            document.getElementsByClassName("operation-elements").style = "hidden";

            document.getElementById("operation-typology").innerText = "Tipologia intervento: Emergenza";
        } else if (data.operation_info.typology == 'P') {
            document.getElementById("operation-typology").innerText = "Tipologia intervento: Programmato";
        }
        if (data.operation_info.color == 3) {
            document.getElementById("operation-color").innerText = "Codice Colore: Rosso";
            document.getElementById("operation-color").classList.remove("text-green")
            document.getElementById("operation-color").classList.remove("text-warning")
            document.getElementById("operation-color").classList.add("text-danger");
        } else if (data.operation_info.color == 2) {
            document.getElementById("operation-color").innerText = "Codice Colore: Giallo";
            document.getElementById("operation-color").classList.remove("text-green")
            document.getElementById("operation-color").classList.add("text-warning")
            document.getElementById("operation-color").classList.remove("text-danger");
        } else if (data.operation_info.color == 1) {
            document.getElementById("operation-color").innerText = "Codice Colore: Verde";
            document.getElementById("operation-color").classList.add("text-green")
            document.getElementById("operation-color").classList.remove("text-warning")
            document.getElementById("operation-color").classList.remove("text-danger");
        }
    }

}