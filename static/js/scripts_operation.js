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

        if (data.operation_info.operation_typology == 'E') {
            document.getElementById("operation_typology").innerText = "Tipologia intervento: Emergenza";
        } else if (data.operation_info.operation_typology == 'P') {
            document.getElementById("operation_typology").innerText = "Tipologia intervento: Programmato";
        }
        if (data.operation_info.operation_color == 3) {
            document.getElementById("operation_color").innerText = "Codice Colore: Rosso";
            document.getElementById("operation_color").classList.remove("text-green")
            document.getElementById("operation_color").classList.remove("text-warning")
            document.getElementById("operation_color").classList.add("text-danger");
        } else if (data.operation_info.operation_color == 2) {
            document.getElementById("operation_color").innerText = "Codice Colore: Giallo";
            document.getElementById("operation_color").classList.remove("text-green")
            document.getElementById("operation_color").classList.add("text-warning")
            document.getElementById("operation_color").classList.remove("text-danger");
        } else if (data.operation_info.operation_color == 1) {
            document.getElementById("operation_color").innerText = "Codice Colore: Verde";
            document.getElementById("operation_color").classList.add("text-green")
            document.getElementById("operation_color").classList.remove("text-warning")
            document.getElementById("operation_color").classList.remove("text-danger");
        }

        document.getElementById("operation_contact_name").innerText = "Nome Referente: " + data.operation_info.operation_contact_name;

        if (data.operation_info.operation_contact_surname != null) {
            document.getElementById("operation_contact_surname").style.visibility = "visible";
            document.getElementById("operation_contact_surname").innerText = "Cognome Referente: " + data.operation_info.operation_contact_surname;
        } else {
            document.getElementById("operation_contact_surname").style.visibility = "hidden";
        }
        if (data.operation_info.operation_contact_telephone != null) {
            document.getElementById("operation_contact_telephone").style.visibility = "visible";
            document.getElementById("operation_contact_telephone").value = data.operation_info.operation_contact_telephone;
        } else {
            document.getElementById("operation_contact_telephone").style.visibility = "hidden";
        }

        document.getElementById("operation_contact_type").innerText = "Segnalato tramite: " + data.operation_info.operation_contact_type;

        if (data.operation_info.operation_note != null) {
            document.getElementById("operation_note").style.visibility = "visible";
            document.getElementById("operation_note").value = data.operation_info.operation_note;
        } else {
            document.getElementById("operation_note").style.visibility = "hidden";
        }

        document.getElementById("operation_contact_type").innerText = "Segnalato tramite: " + data.operation_info.operation_contact_type;

        if (data.operation_info.operation_materials != null) {
            document.getElementById("operation_materials").style.visibility = "visible";
            document.getElementById("operation_materials").value = data.operation_info.operation_materials;
        } else {
            document.getElementById("operation_materials").style.visibility = "hidden";
        }
        document.getElementById("operation_manager").innerText = "Intervento inserito da: " + data.operation_info.operation_manager;

        document.getElementById("operation_date_start").value = new Date(data.operation_info.operation_date_start).toISOString().slice(0, 19);

        document.getElementById("operation_date_stop").value = new Date(data.operation_info.operation_date_stop).toISOString().slice(0, 19);

    }

}