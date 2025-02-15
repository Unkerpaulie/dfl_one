$(document).ready(function() {
    $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    checkForTT('settlement_currency'); 
    check_for_fd(document.getElementById("out_payment"), "fixed_deposit_cert");
});

// not currently in use
function invertRate(id) {
    var rate = document.getElementById(id).value;
    document.getElementById(id).value = 1/rate;
    calcSettlemetAmount();
}

function checkForTT(elem) {
    const select_thing = document.getElementById(elem);
    if (select_thing.options.selectedIndex == 0) {
        document.getElementById(`${elem}_rate`).value = 1;
        hide_div(elem);
    } else {
        document.getElementById(`${elem}_rate`).value = "";
        show_div(elem);
    }
    calcSettlemetAmount();
}

function show_div(elem) {
    document.getElementById(`${elem}_div`).style.visibility = "visible";
}

function hide_div(elem) {
    document.getElementById(`${elem}_div`).style.visibility = "hidden";
}

function check_for_fd(selector, elem) {
    if (selector.value == "fixed") {
        show_div(elem);
    } else {
        hide_div(elem);
    }
}

function calcSettlemetAmount() {
    var foreign_amount = document.getElementById("foreign_amount").value;
    // var exchange_rate = document.getElementById("exchange_rate").value;
    var settlement_currency_rate = document.getElementById("settlement_currency_rate").value;
    var foreign_currency_rate = document.getElementById("foreign_currency_rate").value;
    if (!foreign_currency_rate || !settlement_currency_rate) {
        document.getElementById("settlement_amount").value = 0;
    } else {
        var settlement_amount = foreign_amount * (foreign_currency_rate / settlement_currency_rate);
        document.getElementById("settlement_amount").value = settlement_amount.toFixed(2);
    }
}

function printDiv(divId, title) {
    let mywindow = window.open('', 'PRINT', 'height=650,width=900,top=100,left=150');

    mywindow.document.write(`<html><head><title>${title}</title>`);
    mywindow.document.write('<link rel="stylesheet" href="/static/css/app.css" media="screen,print" />');
    mywindow.document.write('<link rel="stylesheet" href="/static/css/vendor.css" media="screen,print" />');
    mywindow.document.write('<link rel="stylesheet" href="/static/css/custom.css" media="screen,print" />');
    mywindow.document.write('</head><body >');
    mywindow.document.write(document.getElementById(divId).innerHTML);
    mywindow.document.write('</body></html>');

    mywindow.document.close(); // necessary for IE >= 10
    mywindow.focus(); // necessary for IE >= 10* /

    setTimeout(function(){
        mywindow.print();
        mywindow.close();
    },4000);
    return true;
}

