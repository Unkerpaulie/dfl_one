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
    check_for_fd(document.getElementById("out_payment"), "fd_certificate_number");
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
    if (selector[selector.selectedIndex].value == "fixed") {
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


function dealReview() {
    // get values from form
    const form_elements = document.getElementById("transaction_form").elements;
    const value_date = new Date(form_elements["value_date"].value);
    value_date.setDate(value_date.getUTCDate());
    value_date.setMonth(value_date.getUTCMonth());
    value_date.setFullYear(value_date.getUTCFullYear());
    const contract_date = new Date(form_elements["contract_date"].value);
    contract_date.setDate(contract_date.getUTCDate());
    contract_date.setMonth(contract_date.getUTCMonth());
    contract_date.setFullYear(contract_date.getUTCFullYear());
    const value_date_formatted = value_date.toLocaleString('default',{dateStyle:'long'});
    const contract_date_formatted = contract_date.toLocaleString('default',{dateStyle:'long'});
    const transaction_type = form_elements["transaction_type"].options[form_elements["transaction_type"].selectedIndex].text;
    const settlement_currency = form_elements["settlement_currency"].options[form_elements["settlement_currency"].selectedIndex].text;
    const settlement_amount = form_elements["settlement_amount"].value;
    const settlement_currency_rate = Math.round(form_elements["settlement_currency_rate"].value * 10000) / 10000;
    const foreign_currency = form_elements["foreign_currency"].options[form_elements["foreign_currency"].selectedIndex].text;
    const foreign_amount = form_elements["foreign_amount"].value;
    const foreign_currency_rate = Math.round(form_elements["foreign_currency_rate"].value * 10000) / 10000;
    // const bank_fee = "95";
    const bank_fee = form_elements["bank_fee"].value;
    console.log(bank_fee);
    const total_amount = Number(settlement_amount) + Number(bank_fee);
    const payment_details = form_elements["payment_details"].value;
    
    const client_id = form_elements["client_id"].value;
    const client_name = form_elements["client_name"].value;
    const trader = form_elements["trader"].value;
    const deal_id = form_elements["deal_id"].value;
    const out_payment_choice = form_elements["out_payment"].options[form_elements["out_payment"].selectedIndex].value;
    
    // get beneficiary data via ajax if a beneficiary is selected
    if (out_payment_choice.substring(0,3) == "bb-") {
        const bb_id = out_payment_choice.substring(3);
        $.ajax({
            url: `/transactions/${client_id}/beneficiary/${bb_id}`,
            datatype: 'json',
            type: 'GET',
            success: function(res) {
                const data = JSON.parse(res)[0]["fields"];
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
                document.getElementById("review-payment_details").innerText = payment_details;
                document.getElementById("review-deal_id").innerText = deal_id;

            }
        });
    }


    // review summary box
    var summary_box = `
            <div class="row border border-dark">
                <div class="col">`;
    summary_box += transaction_type == "S" ? `We sell:<br>` : `We purchase:<br>`;
    summary_box += `Rate:<br>
                    ${foreign_currency} Equivalent:<br>`;
    summary_box += bank_fee > 0 ? `Bank Charges:<br>` : `<br>`;
    summary_box += `                   
                    Total Amount Due:<br>
                    Value Date:<br>
                </div>
                <div class="col text-center">
                    ${settlement_currency}<br>
                    <br>
                    ${foreign_currency}<br>
                    TTD<br>
                    TTD<br>
                </div>
                <div class="col text-right">
                    ${settlement_amount}<br>
                    ${foreign_currency_rate}<br>
                    ${foreign_amount}<br>`;
    summary_box += bank_fee > 0 ? `${bank_fee}<br>` : `<br>`;
    summary_box += `${total_amount}<br>
                    ${value_date}<br>
                </div>
            </div>
    `;
    document.getElementById("review-summary_box").innerHTML = summary_box;
    /*
    document.getElementById("review-bank_fee").innerText = bank_fee;
    document.getElementById("review-settlement_currency").innerText = settlement_currency;
    document.getElementById("review-settlement_currency2").innerText = settlement_currency;
    // document.getElementById("review-settlement_currency3").innerText = settlement_currency;
    // document.getElementById("review-settlement_currency4").innerText = settlement_currency;
    document.getElementById("review-settlement_amount").innerText = settlement_amount;
    document.getElementById("review-settlement_amount2").innerText = settlement_amount;
    // document.getElementById("review-settlement_amount3").innerText = settlement_amount;
    document.getElementById("review-foreign_currency").innerText = foreign_currency;
    document.getElementById("review-foreign_currency2").innerText = foreign_currency;
    document.getElementById("review-foreign_currency3").innerText = foreign_currency;
    document.getElementById("review-foreign_amount").innerText = foreign_amount;
    document.getElementById("review-total_amount").innerText = total_amount;
    document.getElementById("review-total_amount2").innerText = total_amount;
    document.getElementById("review-settlement_currency_rate").innerText = settlement_currency_rate;
    // document.getElementById("review-transaction_type").innerText = transaction_type;
    document.getElementById("review-value_date").innerText = value_date_formatted;
    document.getElementById("review-value_date2").innerText = value_date_formatted;
    document.getElementById("review-value_date3").innerText = value_date_formatted;
    document.getElementById("review-contract_date").innerText = contract_date_formatted;
    */
}

