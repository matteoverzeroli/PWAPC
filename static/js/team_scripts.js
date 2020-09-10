document.getElementById("a-team-details").addEventListener("click",get_team_data);

function get_team_data() {
     $.ajax({
        method: 'POST',
        url: '/get_team_list',
        error: function () {
            alert("Errore richiesta dati squadra");
        }
    }).done(set_team_data);
}
function set_team_data(data) {
    console.log(data)
}
