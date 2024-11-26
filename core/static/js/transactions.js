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
    checkForTT('origin_currency');
});

function invertRate(id) {
    var rate = document.getElementById(id).value;
    document.getElementById(id).value = 1/rate;
    calcSettlemetAmount();
}

function checkForTT(elem) {
    var select_thing = document.getElementById(elem);
    if (select_thing.options.selectedIndex == 0) {
        document.getElementById(`${elem}_rate`).value = 1;
        document.getElementById(`${elem}_rate`).readOnly = true;
    } else {
        document.getElementById(`${elem}_rate`).readOnly = false;
    }
    calcSettlemetAmount();
}

function calcSettlemetAmount() {
    var settlement_amount = document.getElementById("settlement_amount").value;
    // var exchange_rate = document.getElementById("exchange_rate").value;
    var settlement_currency_rate = document.getElementById("settlement_currency_rate").value;
    var origin_currency_rate = document.getElementById("origin_currency_rate").value;
    var exchange_rate = settlement_currency_rate / origin_currency_rate;
    var origin_amount = settlement_amount * exchange_rate;
    document.getElementById("origin_amount").value = origin_amount.toFixed(2);
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

function saveDiv(divId, title) {
    var doc = new jsPDF();
    doc.fromHTML(`<html><head><title>${title}</title></head>
        <body>` + document.getElementById(divId).innerHTML + `</body></html>`);
    doc.save('div.pdf');
}

function dealReview() {
    // get values from form
    const form_elements = document.getElementById("transaction_form").elements;
    const bank_charges = "95";
    const value_date = new Date(form_elements["value_date"].value);
    const contract_date = new Date(form_elements["contract_date"].value);
    const value_date_formatted = value_date.toLocaleString('default',{dateStyle:'long'});
    const contract_date_formatted = contract_date.toLocaleString('default',{dateStyle:'long'});
    const transaction_type = form_elements["transaction_type"].options[form_elements["transaction_type"].selectedIndex].text;
    const settlement_currency = form_elements["settlement_currency"].options[form_elements["settlement_currency"].selectedIndex].text;
    const settlement_amount = form_elements["settlement_amount"].value;
    const settlement_currency_rate = Math.round(form_elements["settlement_currency_rate"].value * 10000) / 10000;
    const origin_currency = form_elements["origin_currency"].options[form_elements["origin_currency"].selectedIndex].text;
    const origin_amount = form_elements["origin_amount"].value;
    const origin_currency_rate = Math.round(form_elements["origin_currency_rate"].value * 10000) / 10000;
    const total_amount = Number(settlement_amount) + Number(bank_charges);
    
    const client_id = form_elements["client_id"].value;
    const client_name = form_elements["client_name"].value;
    const trader = form_elements["trader"].value;
    const deal_id = form_elements["deal_id"].value;
    const beneficiary_id = form_elements["beneficiary"].options[form_elements["beneficiary"].selectedIndex].value;
    
    // get beneficiary data via ajax
    $.ajax({
        url: `/transactions/${client_id}/beneficiary/${beneficiary_id}`,
        datatype: 'json',
        type: 'GET',
        success: function(res) {
            const data = JSON.parse(res)[0]["fields"];
            console.log(data);
            // set beneficiary values
            const bank_name = data.bank_name;
            const account_number = data.account_number;
            const aba_code = data.aba_code;
            const bank_address = data.bank_address;
            const bank_address2 = data.bank_address2;
            const bank_city = data.bank_city;
            const bank_state = data.bank_state;
            const bank_zip = data.bank_zip;
            const bank_country = data.bank_country;
            const iban_code = data.iban_code;
            const swift_code = data.swift_code;
            const intermediary_bank_name = data.intermediary_bank_name;
            const intermediary_account_number = data.intermediary_account_number;
            const intermediary_aba_code = data.intermediary_aba_code;
            const intermediary_bank_address = data.intermediary_bank_address;
            const intermediary_bank_address2 = data.intermediary_bank_address2;
            const intermediary_bank_city = data.intermediary_bank_city;
            const intermediary_bank_state = data.intermediary_bank_state;
            const intermediary_bank_zip = data.intermediary_bank_zip;
            const intermediary_bank_country = data.intermediary_bank_country;
            const intermediary_iban_code = data.intermediary_iban_code;
            const intermediary_swift_code = data.intermediary_swift_code;
            const recipient_name = data.recipient_name;
            const recipient_address = data.recipient_address;
            const recipient_address2 = data.recipient_address2;
            const recipient_city = data.recipient_city;
            const recipient_state = data.recipient_state;
            const recipient_zip = data.recipient_zip;
            const recipient_country = data.recipient_country;
            
            document.getElementById("review-account_number").innerText = account_number;
            document.getElementById("review-bank_name").innerText = bank_name;
            document.getElementById("review-bank_address").innerText = bank_address;
            document.getElementById("review-bank_address2").innerText = bank_address2;
            document.getElementById("review-bank_state").innerText = bank_state;
            document.getElementById("review-bank_city").innerText = bank_city;
            document.getElementById("review-bank_zip").innerText = bank_zip;
            // document.getElementById("review-bank_country").innerText = bank_country;
            document.getElementById("review-swift_code").innerText = swift_code;
            document.getElementById("review-intermediary_bank_name").innerText = intermediary_bank_name;
            document.getElementById("review-intermediary_bank_address").innerText = intermediary_bank_address;
            document.getElementById("review-intermediary_bank_address2").innerText = intermediary_bank_address2;
            document.getElementById("review-intermediary_bank_state").innerText = intermediary_bank_state;
            document.getElementById("review-intermediary_bank_city").innerText = intermediary_bank_city;
            document.getElementById("review-intermediary_bank_zip").innerText = intermediary_bank_zip;
            // document.getElementById("review-intermediary_bank_country").innerText = intermediary_bank_country;
            document.getElementById("review-intermediary_swift_code").innerText = intermediary_swift_code;
            document.getElementById("review-recipient_name").innerText = recipient_name;
            document.getElementById("review-recipient_address").innerText = recipient_address;
            document.getElementById("review-recipient_address2").innerText = recipient_address2;
            document.getElementById("review-recipient_state").innerText = recipient_state;
            document.getElementById("review-recipient_city").innerText = recipient_city;
            document.getElementById("review-recipient_zip").innerText = recipient_zip;
            // document.getElementById("review-recipient_country").innerText = recipient_country;
            document.getElementById("review-client_name").innerText = client_name;
            document.getElementById("review-client_name2").innerText = client_name;
            document.getElementById("review-client_name3").innerText = client_name;
            document.getElementById("review-client_name4").innerText = client_name;
            document.getElementById("review-trader").innerText = trader;
            document.getElementById("review-deal_id").innerText = deal_id;

        }
    });


    // set review values
    document.getElementById("review-bank_charges").innerText = bank_charges;
    document.getElementById("review-settlement_currency").innerText = settlement_currency;
    document.getElementById("review-settlement_currency2").innerText = settlement_currency;
    document.getElementById("review-settlement_currency3").innerText = settlement_currency;
    // document.getElementById("review-settlement_currency4").innerText = settlement_currency;
    document.getElementById("review-settlement_amount").innerText = settlement_amount;
    document.getElementById("review-settlement_amount2").innerText = settlement_amount;
    // document.getElementById("review-settlement_amount3").innerText = settlement_amount;
    document.getElementById("review-origin_currency").innerText = origin_currency;
    document.getElementById("review-origin_currency2").innerText = origin_currency;
    document.getElementById("review-origin_currency3").innerText = origin_currency;
    document.getElementById("review-origin_amount").innerText = origin_amount;
    document.getElementById("review-total_amount").innerText = total_amount;
    document.getElementById("review-total_amount2").innerText = total_amount;
    document.getElementById("review-settlement_currency_rate").innerText = settlement_currency_rate;
    document.getElementById("review-transaction_type").innerText = transaction_type;
    document.getElementById("review-value_date").innerText = value_date_formatted;
    document.getElementById("review-value_date2").innerText = value_date_formatted;
    document.getElementById("review-value_date3").innerText = value_date_formatted;
    document.getElementById("review-contract_date").innerText = contract_date_formatted;
    
}

