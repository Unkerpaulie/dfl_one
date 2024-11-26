from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Client, BeneficiaryBank, Country

@login_required
def home(req):
    if req.user.role == "admin":
        clients = Client.objects.all()
    else:
        clients = Client.objects.all().exclude(pk=0)
    context = {"page_title": "Client List"}
    context["clients"] = clients
    context["section"] = "clients"
    return render(req, "clients/clients_list.html", context)

# send beneficiary information
@login_required
def beneficiaries(req, client_id):
    client = get_object_or_404(Client, pk=client_id)
    context = {"page_title": f"{client} Beneficiaries"}
    context["section"] = "clients"
    context['client'] = client
    beneficiaries = BeneficiaryBank.objects.filter(client=client)
    context['beneficiaries'] = beneficiaries
    return render(req, 'clients/beneficiaries.html', context)


# create new beneficiary
@login_required
def new_beneficiary(req, client_id):
    client = get_object_or_404(Client, pk=client_id)
    context = {"page_title": f"New Beneficiary for {client}"}
    context["section"] = "clients"
    context['client'] = client
    context['form_purpose'] = "new"
    countries = Country.objects.all()
    context["countries"] = countries
    
    # get fields from form    
    if req.method =="POST":
        # get form data
        bank_name = req.POST['bank_name'].strip()
        bank_address = req.POST['bank_address'].strip()
        bank_address2 = req.POST['bank_address2'].strip()
        bank_city = req.POST['bank_city'].strip()
        bank_state = req.POST['bank_state'].strip()
        bank_zip = req.POST['bank_zip'].strip()
        bank_country = int(req.POST['bank_country'])
        account_number = req.POST['account_number'].strip()
        swift_code = req.POST['swift_code'].strip()
        iban_code = req.POST['iban_code'].strip()
        aba_code = req.POST['aba_code'].strip()
        recipient_name = req.POST['recipient_name'].strip()
        recipient_address = req.POST['recipient_address'].strip()
        recipient_address2 = req.POST['recipient_address2'].strip()
        recipient_city = req.POST['recipient_city'].strip()
        recipient_state = req.POST['recipient_state'].strip()
        recipient_zip = req.POST['recipient_zip'].strip()
        recipient_country = int(req.POST['recipient_country'])
        intermediary_bank_name = req.POST['intermediary_bank_name'].strip()
        intermediary_bank_address = req.POST['intermediary_bank_address'].strip()
        intermediary_bank_address2 = req.POST['intermediary_bank_address2'].strip()
        intermediary_bank_city = req.POST['intermediary_bank_city'].strip()
        intermediary_bank_state = req.POST['intermediary_bank_state'].strip()
        intermediary_bank_zip = req.POST['intermediary_bank_zip'].strip()
        intermediary_bank_country = int(req.POST['intermediary_bank_country'])
        intermediary_account_number = req.POST['intermediary_account_number'].strip()
        intermediary_swift_code = req.POST['intermediary_swift_code'].strip()
        intermediary_iban_code = req.POST['intermediary_iban_code'].strip()
        intermediary_aba_code = req.POST['intermediary_aba_code'].strip()
        special_instructions = req.POST['special_instructions'].strip()

        # create new beneficiary and save
        beneficiary = BeneficiaryBank(
            client=client,
            bank_name=bank_name,
            bank_address=bank_address,
            bank_address2=bank_address2,
            bank_city=bank_city,
            bank_state=bank_state,
            bank_zip=bank_zip,
            bank_country=Country.objects.get(pk=bank_country),
            account_number=account_number,
            swift_code=swift_code,
            iban_code=iban_code,
            aba_code=aba_code,
            recipient_name=recipient_name,
            recipient_address=recipient_address,
            recipient_address2=recipient_address2,
            recipient_city=recipient_city,
            recipient_state=recipient_state,
            recipient_zip=recipient_zip,
            recipient_country=Country.objects.get(pk=recipient_country),
            intermediary_bank_name=intermediary_bank_name,
            intermediary_bank_address=intermediary_bank_address,
            intermediary_bank_address2=intermediary_bank_address2,
            intermediary_bank_city=intermediary_bank_city,
            intermediary_bank_state=intermediary_bank_state,
            intermediary_bank_zip=intermediary_bank_zip,
            intermediary_bank_country=Country.objects.get(pk=intermediary_bank_country),
            intermediary_account_number=intermediary_account_number,
            intermediary_swift_code=intermediary_swift_code,
            intermediary_iban_code=intermediary_iban_code,
            intermediary_aba_code=intermediary_aba_code,
            special_instructions=special_instructions,
        )
        beneficiary.save()
        messages.success(req, f"New beneficiary for client {client} created successfully.")
        return redirect('clients:beneficiaries', client_id=client.ClientID)
    return render(req, "clients/beneficiary_form.html", context)



# edit beneficiary
@login_required
def edit_beneficiary(req, client_id, beneficiary_id):
    client = get_object_or_404(Client, pk=client_id)
    beneficiary = BeneficiaryBank.objects.get(pk=beneficiary_id)
    countries = Country.objects.all()
    context = {"page_title": f"Edit Beneficiary {beneficiary.bank_name}"}
    context["section"] = "clients"
    context['client'] = client
    context['form_purpose'] = "edit"
    context["countries"] = countries
    # set form data
    context['formdata'] = {
        "bank_name": beneficiary.bank_name,
        "bank_address": beneficiary.bank_address,
        "bank_address2": beneficiary.bank_address2,
        "bank_city": beneficiary.bank_city,
        "bank_state": beneficiary.bank_state,
        "bank_zip": beneficiary.bank_zip,
        "bank_country": beneficiary.bank_country,
        "account_number": beneficiary.account_number,
        "swift_code": beneficiary.swift_code,
        "iban_code": beneficiary.iban_code,
        "aba_code": beneficiary.aba_code,
        "recipient_name": beneficiary.recipient_name,
        "recipient_address": beneficiary.recipient_address,
        "recipient_address2": beneficiary.recipient_address2,
        "recipient_city": beneficiary.recipient_city,
        "recipient_state": beneficiary.recipient_state,
        "recipient_zip": beneficiary.recipient_zip,
        "recipient_country": beneficiary.recipient_country,
        "intermediary_bank_name": beneficiary.intermediary_bank_name,
        "intermediary_bank_address": beneficiary.intermediary_bank_address,
        "intermediary_bank_address2": beneficiary.intermediary_bank_address2,
        "intermediary_bank_city": beneficiary.intermediary_bank_city,
        "intermediary_bank_state": beneficiary.intermediary_bank_state,
        "intermediary_bank_zip": beneficiary.intermediary_bank_zip,
        "intermediary_bank_country": beneficiary.intermediary_bank_country,
        "intermediary_account_number": beneficiary.intermediary_account_number,
        "intermediary_swift_code": beneficiary.intermediary_swift_code,
        "intermediary_iban_code": beneficiary.intermediary_iban_code,
        "intermediary_aba_code": beneficiary.intermediary_aba_code,
        "special_instructions": beneficiary.special_instructions,
    }

    # get fields from form
    if req.method =="POST":
        # get form data 
        bank_name = req.POST['bank_name'].strip()
        bank_address = req.POST['bank_address'].strip()
        bank_address2 = req.POST['bank_address2'].strip()
        bank_city = req.POST['bank_city'].strip()
        bank_state = req.POST['bank_state'].strip()
        bank_zip = req.POST['bank_zip'].strip()
        bank_country = int(req.POST['bank_country'])
        account_number = req.POST['account_number'].strip()
        swift_code = req.POST['swift_code'].strip()
        iban_code = req.POST['iban_code'].strip()
        aba_code = req.POST['aba_code'].strip()
        recipient_name = req.POST['recipient_name'].strip()
        recipient_address = req.POST['recipient_address'].strip()
        recipient_address2 = req.POST['recipient_address2'].strip()
        recipient_city = req.POST['recipient_city'].strip()
        recipient_state = req.POST['recipient_state'].strip()
        recipient_zip = req.POST['recipient_zip'].strip()
        recipient_country = int(req.POST['recipient_country'])
        intermediary_bank_name = req.POST['intermediary_bank_name'].strip()
        intermediary_bank_address = req.POST['intermediary_bank_address'].strip()
        intermediary_bank_address2 = req.POST['intermediary_bank_address2'].strip()
        intermediary_bank_city = req.POST['intermediary_bank_city'].strip()
        intermediary_bank_state = req.POST['intermediary_bank_state'].strip()
        intermediary_bank_zip = req.POST['intermediary_bank_zip'].strip()
        intermediary_bank_country = int(req.POST['intermediary_bank_country'])
        intermediary_account_number = req.POST['intermediary_account_number'].strip()
        intermediary_swift_code = req.POST['intermediary_swift_code'].strip()
        intermediary_iban_code = req.POST['intermediary_iban_code'].strip()
        intermediary_aba_code = req.POST['intermediary_aba_code'].strip()
        intermediary_account_number = req.POST['intermediary_account_number'].strip()
        special_instructions = req.POST['special_instructions'].strip()

        # update beneficiary
        beneficiary.client=client
        beneficiary.bank_name=bank_name
        beneficiary.bank_address=bank_address
        beneficiary.bank_address2=bank_address2
        beneficiary.bank_city=bank_city
        beneficiary.bank_state=bank_state
        beneficiary.bank_zip=bank_zip
        beneficiary.bank_country=Country.objects.get(pk=bank_country)
        beneficiary.account_number=account_number
        beneficiary.swift_code=swift_code
        beneficiary.iban_code=iban_code
        beneficiary.aba_code=aba_code
        beneficiary.recipient_name=recipient_name
        beneficiary.recipient_address=recipient_address
        beneficiary.recipient_address2=recipient_address2
        beneficiary.recipient_city=recipient_city
        beneficiary.recipient_state=recipient_state
        beneficiary.recipient_zip=recipient_zip
        beneficiary.recipient_country=Country.objects.get(pk=recipient_country)
        beneficiary.intermediary_bank_name=intermediary_bank_name
        beneficiary.intermediary_bank_address=intermediary_bank_address
        beneficiary.intermediary_bank_address2=intermediary_bank_address2
        beneficiary.intermediary_bank_city=intermediary_bank_city
        beneficiary.intermediary_bank_state=intermediary_bank_state
        beneficiary.intermediary_bank_zip=intermediary_bank_zip
        beneficiary.intermediary_bank_country=Country.objects.get(pk=intermediary_bank_country)
        beneficiary.intermediary_account_number=intermediary_account_number
        beneficiary.intermediary_swift_code=intermediary_swift_code
        beneficiary.intermediary_iban_code=intermediary_iban_code
        beneficiary.intermediary_aba_code=intermediary_aba_code
        beneficiary.special_instructions=special_instructions
        beneficiary.save()
        messages.success(req, f"Beneficiary for client {client} updated successfully.")
        return redirect('clients:beneficiaries', client_id=client.ClientID)
    return render(req, "clients/beneficiary_form.html", context)

