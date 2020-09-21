/*!
    * Start Bootstrap - Agency v6.0.2 (https://startbootstrap.com/template-overviews/agency)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
    */
(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
            this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 72,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 74,
    });

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict


//author: Matteo Verzeroli

$(document).ready(function () {
    $.ajax({
        method: 'POST',
        url: '/get_user_data',
        error: function () {
            alet("Errore nel caricare dati utente (ajax-post-get_user_data)")
        },
        success: set_data
    })
})

function set_data(data) {
    document.getElementById("navbar_text").innerText = data.user_data.name + " " + data.user_data.surname + "\n" + data.user_data.role;

    document.getElementById("user_zone").innerText = "Zona: " + data.zone_data.name;

    if (data.team_data.name == "Nessuna Squadra!") {
        document.getElementById("a-team-details").style.visibility = "hidden";
    } else {
        document.getElementById("a-team-details").style.visibility = "visible";
    }

    for (let i = 0; i < document.getElementsByClassName("team-name").length; i++) {
        document.getElementsByClassName("team-name")[i].innerText = document.getElementsByClassName("team-name")[i].innerText + data.team_data.name;
    }

    document.getElementById("team_state").innerText = "Stato: " + data.team_data.state;

    for (let i = 0; i < document.getElementsByClassName("team-master").length; i++) {
        document.getElementsByClassName("team-master")[i].innerText = document.getElementsByClassName("team-master")[i].innerText + data.team_data.master;
    }

    document.getElementById("user_username").value = data.user_data.username;
    document.getElementById("user_regional_id").value = data.user_data.regional_id;
    document.getElementById("user_name").value = data.user_data.name;
    document.getElementById("user_surname").value = data.user_data.surname;
    document.getElementById("user_residency").value = data.user_data.residency;
    document.getElementById("user_address").value = data.user_data.address;

    document.getElementById("user_birthday").value = new Date(data.user_data.birthday).toISOString().slice(0, 10);
    document.getElementById("user_CF").value = data.user_data.CF;

    //it handles the select item in modificadatiutente
    if (data.user_data.sex == "M") {
        document.getElementById("user_sex").selectedIndex = 0;
    } else {
        document.getElementById("user_sex").selectedIndex = 1;
    }

    document.getElementById("user_mobile_phone").value = data.user_data.mobile_phone;
    document.getElementById("user_telephone").value = data.user_data.telephone;
    document.getElementById("user_telegram_username").value = data.user_data.telegram_username;
    document.getElementById("user_email").value = data.user_data.email;
    document.getElementById("user_qualification").value = data.user_data.qualification;

    document.getElementById("contact_mobile_phone").href = "tel:" + data.contact_data.mobile_phone;
    document.getElementById("contact_whatsapp").href = "https://wa.me/" + data.contact_data.whatsapp;
    document.getElementById("contact_telegram").href = "https://telegram.me/" + data.contact_data.telegram;
    document.getElementById("contact_email").href = "mailto:" + data.contact_data.email;

    //show botton navbar when the state of team is active
    if (document.getElementById("team_state").innerText.toLowerCase() == "stato: attivo") {
        document.getElementById("bottomNav").style.visibility = "visible";
    } else {
        document.getElementById("bottomNav").style.visibility = "hidden";
    }

    //select the operative button
    set_operative_btn(data.user_data.operative)
}

document.getElementById("btn_submit").addEventListener('click', submit_form_modificautente);

// submit form modificadatiutente
function submit_form_modificautente() {
    $("#form_modificadatiutente").submit();
}

document.getElementById("btn-operative").addEventListener('click', send_operative_status);

//send operative status
function send_operative_status() {
    $.ajax({
        method: 'POST',
        url: '/set_user_operation_status',
        data: JSON.stringify({"operativo": !(document.getElementById("btn-operative").value == '1')}),
        contentType: 'application/json',
        dataType: 'json',
        async: true,
        error: function () {
            alert("Errore invio stato operativo!");
        },
        success: function () {
            set_operative_btn(!(document.getElementById("btn-operative").value == '1'));
        }
    });
}

//set operative status
function set_operative_btn(status) {
    if (status == false) {
        document.getElementById("btn-operative").innerText = "NON OPERATIVO !";
        document.getElementById("btn-operative").value = "0";

        document.getElementById("btn-operative").classList.add('btn-warning')
        document.getElementById("btn-operative").classList.remove('btn-danger')
    } else {
        document.getElementById("btn-operative").innerText = "OPERATIVO !";
        document.getElementById("btn-operative").value = "1";

        document.getElementById("btn-operative").classList.add('btn-danger')
        document.getElementById("btn-operative").classList.remove('btn-warning')
    }
}

