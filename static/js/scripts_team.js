document.getElementById("a-team-details").addEventListener("click", get_team_data);

let team_list_table = document.getElementById("team-list");
let table = document.createElement('TABLE');
let tableBody = document.createElement('TBODY');


//create table for member team list
$(document).ready(function () {
    table.classList.add("table");
    table.classList.add("table-striped");

    table.appendChild(tableBody);
    team_list_table.appendChild(table);

    let tr = document.createElement('TR');
    tableBody.appendChild(tr);
    let th = document.createElement('TH');
    th.appendChild(document.createTextNode("Nome"));
    tr.appendChild(th);
    th = document.createElement('TH');
    th.appendChild(document.createTextNode("Cognome"));
    tr.appendChild(th);
})

function get_team_data() {
    $.ajax({
        method: 'POST',
        url: '/get_team_list',
        error: function () {
            alert("Errore richiesta dati squadra");
        },
        success: set_team_data
    })
}

function set_team_data(data) {
///da sistemare !!!
    for (let i = 0; i < data.length; i++) {
        let tr = document.createElement('TR');
        tableBody.appendChild(tr);

        for (let j = 0; j < 2; j++) {
            let td = document.createElement('TD');
            td.appendChild(document.createTextNode(data[i][j]));
            tr.appendChild(td);
        }
    }

}
