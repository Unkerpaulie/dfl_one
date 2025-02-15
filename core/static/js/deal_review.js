// declare vars
var form_elements;
var deal_id;
var client_name;
var client_address1;
var client_address2;
var client_city;
var contact_person;
var value_date;
var contract_date;
var value_date_formatted;
var contract_date_formatted;
var transaction_type;
var settlement_currency;
var settlement_amount;
var settlement_currency_rate;
var foreign_currency;
var foreign_amount;
var foreign_currency_rate;
var bank_fee;
var total_amount;
var payment_details;
var client_id;
var trader;
var out_payment_choice;


function set_vars() {
    form_elements = document.getElementById("transaction_form").elements;
    deal_id = form_elements["deal_id"].value;
    client_name = form_elements["client_name"].value;
    client_address1 = form_elements["client_address1"].value;
    client_address2 = form_elements["client_address2"].value;
    client_city = form_elements["client_city"].value;
    contact_person = form_elements["contact_person"].value;
    value_date = new Date(form_elements["value_date"].value);
    value_date.setDate(value_date.getUTCDate());
    value_date.setMonth(value_date.getUTCMonth());
    value_date.setFullYear(value_date.getUTCFullYear());
    contract_date = new Date(form_elements["contract_date"].value);
    contract_date.setDate(contract_date.getUTCDate());
    contract_date.setMonth(contract_date.getUTCMonth());
    contract_date.setFullYear(contract_date.getUTCFullYear());
    value_date_formatted = value_date.toLocaleString('default',{dateStyle:'long'});
    contract_date_formatted = contract_date.toLocaleString('default',{dateStyle:'long'});
    transaction_type = form_elements["transaction_type"].options[form_elements["transaction_type"].selectedIndex].text;
    settlement_currency = form_elements["settlement_currency"].options[form_elements["settlement_currency"].selectedIndex].text;
    settlement_amount = form_elements["settlement_amount"].value;
    settlement_currency_rate = Math.round(form_elements["settlement_currency_rate"].value * 10000) / 10000;
    foreign_currency = form_elements["foreign_currency"].options[form_elements["foreign_currency"].selectedIndex].text;
    foreign_amount = form_elements["foreign_amount"].value;
    foreign_currency_rate = Math.round(form_elements["foreign_currency_rate"].value * 10000) / 10000;
    bank_fee = form_elements["bank_fee"].checked ? form_elements["bank_fee"].value : 0;
    total_amount = Number(settlement_amount) + Number(bank_fee);
    payment_details = form_elements["payment_details"].value;
    client_id = form_elements["client_id"].value;
    trader = form_elements["trader"].value;
    out_payment_choice = form_elements["out_payment"].options[form_elements["out_payment"].selectedIndex].value;
}


function build_contract_heading() {
    var html_div = `
            <div class="row">
                <div class="col">
                    <p>Contract Date: ${contract_date_formatted}</p>
                    <p>${client_name}<br>
                        ${client_address1}, ${client_address2}<br>
                        ${client_city}
                    </p>
                    <p>Attn: ${contact_person}</p>
                </div>
                <div class="col"></div>
                <div class="col">
                    <p>Deal No: ${deal_id}</p>
                </div>
            </div>
    `;
    document.getElementById("review-contract_heading").innerHTML = html_div;
}

function build_summary_box() {
    var html_div = `
            <div>We now confirm details of the above transaction as follows:</div>
            <div class="row border border-dark">
                <div class="col">
                    We ${transaction_type == "S" ? "sell" : "purchase"}:<br>
                    Rate:<br>
                    ${settlement_currency} Equivalent:<br>
                    ${bank_fee > 0 ? "Bank Charges:<br>" : "<br>"}
                    Total Amount Due:<br>
                    Value Date:<br>
                </div>
                <div class="col text-center">
                    ${foreign_currency}<br>
                    <br>
                    ${settlement_currency}<br>
                    TTD<br>
                    TTD<br>
                </div>
                <div class="col text-right">
                    ${foreign_amount}<br>
                    ${foreign_currency_rate}<br>
                    ${settlement_amount}<br>
                    ${bank_fee > 0 ? bank_fee + "<br>" : "<br>"}
                    ${total_amount}<br>
                    ${value_date_formatted}<br>
                </div>
            </div>
            <p><strong>Our settlement of the stated value date is subject to receipt of the TTD funds on <u>${value_date_formatted} </u>.</strong></p>
    `;
    document.getElementById("review-summary_box").innerHTML = html_div;
}

function build_inbound_payment() {
    var html_div = `
            <div>
                <p>${client_name} will send ${settlement_currency} ${settlement_amount} to Development Finance Limited on ${value_date_formatted} as follows:</p>
            </div>
            <div class="row mb-3">
                <div class="col-3"></div>
                <div class="col-9">
                    RBC Royal Bank<br>
                    Independence Sq.<br>
                    Account # 1000-040-134874-3-2
                </div>
            </div>
    `;
    document.getElementById("review-inbound_payment").innerHTML = html_div;
}

function build_outbound_payment() {
    var html_div = `
                <p>Upon receipt of <span id="review-origin_currency3"></span> funds, Development Finance Limited will transfer <span id="review-y"></span> <span id="review-settlement_amount2"></span> to:</p>
                <div class="row mb-3">
                    <div class="col-3">
                        Intermediary Bank:<br>
                        <br>
                        <strong>SWIFT:</strong><br>
                    </div>
                    <div class="col-9">
                        <strong>${12345}</strong><br>
                        ${12345} ${12345}, 
                        ${12345}, ${12345} ${12345}<br>
                        <strong>${12345}</strong><br>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-3">
                        Beneficiary Bank:<br>
                        <br>
                        <strong>SWIFT:</strong><br>
                    </div>
                    <div class="col-9">
                        <strong>${12345}</strong><br>
                        ${12345} ${12345}, 
                        ${12345}, ${12345} ${12345}<br>
                        <strong>${12345}
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-3">
                        Beneficiary Customer:<br>
                        <br>
                        <br>
                        <strong>ACC #:</strong><br>
                    </div>
                    <div class="col-9">
                        <strong>${12345}</strong><br>
                        ${12345} ${12345}, <br>
                        ${12345}, ${12345} ${12345}<br>
                        <strong>${12345}</strong><br>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-3">
                        Payment Details::<br>
                    </div>
                    <div class="col-9">
                        ${12345}<br>
                    </div>
                </div>
    `;
    document.getElementById("review-outbound_payment").innerHTML = html_div;
}

function build_signatures() {
    var html_div = `
            <div>
                <p>
                    Dealers: ${trader}<br>
                    Kindly confirm your agreement by signing, stamping, and returning a copy of this confirmation to us.
                </p>
            </div>
            <div class="row mb-3">
                <div class="col-4 mt-5 border-top border-dark">
                    <p>Authorized Signature (DFL)</p>
                </div>
                <div class="col-2"></div>
                <div class="col-4 mt-5 border-top border-dark">
                    <p >Accepted (${contact_person})</p>
                </div>
                <div class="col"></div>
            </div>
            <div class="row mb-3">
                <div class="col-4 mt-5 border-top border-dark">
                    <p>Authorized Signature (DFL)</p>
                </div>
                <div class="col"></div>
            </div>
    `;
    document.getElementById("review-signatures").innerHTML = html_div;
}



function get_beneficiary_info() {
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
            
            var html_div = `
                        <p>Upon receipt of <span id="review-origin_currency3"></span> funds, Development Finance Limited will transfer <span id="review-y"></span> <span id="review-settlement_amount2"></span> to:</p>
                        <div class="row mb-3">
                            <div class="col-3">
                                Intermediary Bank:<br>
                                <br>
                                <strong>SWIFT:</strong><br>
                            </div>
                            <div class="col-9">
                                <strong>${intermediary_bank_name}</strong><br>
                                ${intermediary_bank_address} ${intermediary_bank_address2 ? ", " + intermediary_bank_address2 : ""}, 
                                ${intermediary_bank_city}, ${intermediary_bank_state} ${intermediary_bank_state}, ${intermediary_bank_country}<br>
                                <strong>${intermediary_swift_code}</strong><br>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-3">
                                Beneficiary Bank:<br>
                                <br>
                                <strong>SWIFT:</strong><br>
                            </div>
                            <div class="col-9">
                                <strong>${bank_name}</strong><br>
                                ${bank_address} ${bank_address2 ? ", " + bank_address2 : ""}, 
                                ${bank_city}, ${bank_state} ${bank_state}, ${bank_country}<br>
                                <strong>${swift_code}</strong><br>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-3">
                                Beneficiary Customer:<br>
                                <br>
                                <br>
                                <strong>ACC #:</strong><br>
                            </div>
                            <div class="col-9">
                                <strong>${recipient_name}</strong><br>
                                ${recipient_address} ${recipient_address2 ? ", " + recipient_address2 : ""}, 
                                ${recipient_city}, ${recipient_state} ${recipient_state}, ${recipient_country}<br>
                                <strong>${account_number}</strong><br>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-3">
                                Payment Details::<br>
                            </div>
                            <div class="col-9">
                                ${payment_details}<br>
                            </div>
                        </div>
            `;
            document.getElementById("review-outbound_payment").innerHTML = html_div;
        }
    });
}

function dealReview() {
    set_vars();
    console.log(bank_fee);
    console.log(form_elements["bank_fee"].checked);
    build_contract_heading();
    build_summary_box();
    if (out_payment_choice.substring(0,3) == "bb-") {
        get_beneficiary_info();
    } else if (out_payment_choice == "cash"){
        cash_details();
    } else {
        fixed_deposit_details();
    }
    build_inbound_payment();
    build_signatures();
}




