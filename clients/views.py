from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import (
    IndividualClient, 
    CorporateClient, 
    ClientList, 
    IdentificationInfo, 
    BeneficiaryBank,
    ClientLocalBank
)
from core.models import Country, IdentificationType, Currency
from setup.models import DFLLocalBank

@login_required
def home(req):
    if req.user.role == "admin":
        clients = ClientList.objects.all()
    else:
        clients = ClientList.objects.all().exclude(pk=0)
    context = {"page_title": "Client List"}
    context["clients"] = clients
    context["section"] = "clients"
    return render(req, "clients/clients_list.html", context)

# create client list entry for new clients
def create_client_list_entry(client_name, client_type, legacy_id):
    client_list = ClientList(
        client_name=client_name,
        client_type=client_type,
        legacy_id=legacy_id
    )
    client_list.save()
    return client_list

# update client list entry 
def update_client_list_entry(id, client_name, legacy_id):
    client_list = ClientList.objects.get(pk=id)
    client_list.client_name=client_name,
    client_list.legacy_id=legacy_id
    client_list.save()


@login_required
def new_individual(req):
    context = {"page_title": "New Individual Client"}
    context["section"] = "clients"
    context['form_purpose'] = "new"
    countries = Country.objects.all()
    id_types = IdentificationType.objects.all()
    mar_statuses = IndividualClient.MARITAL_STATUSES
    emp_statuses = IndividualClient.EMPLOYMENT_STATUSES
    trans_freq = IndividualClient.TRANSACTION_FREQUENCIES
    context["countries"] = countries
    context["id_types"] = id_types
    context |= {"mar_statuses": mar_statuses, "emp_statuses": emp_statuses, "trans_freq": trans_freq}
    
    # get fields from form
    if req.method =="POST":
        # get form data
        legacy_id = req.POST['legacy_id'].strip()
        first_name = req.POST['first_name'].strip()
        middle_name = req.POST['middle_name'].strip()
        surname = req.POST['surname'].strip()
        date_of_birth = req.POST['date_of_birth']
        gender = req.POST['gender']
        marital_status = req.POST['marital_status']
        residential_address = req.POST['residential_address'].strip()
        residential_address2 = req.POST['residential_address2'].strip()
        residential_city = req.POST['residential_city'].strip()
        residential_country = int(req.POST['residential_country'])
        mailing_address = req.POST['mailing_address'].strip()
        mailing_address2 = req.POST['mailing_address2'].strip()
        mailing_city = req.POST['mailing_city'].strip()
        mailing_country = int(req.POST['mailing_country'])
        country_of_birth = int(req.POST['country_of_birth'])
        nationality = int(req.POST['nationality'])
        dual_citizen = req.POST['dual_citizen'] == 'on'
        dual_nationality = int(req.POST['dual_nationality'])
        primary_phone = req.POST['primary_phone'].strip()
        secondary_phone = req.POST['secondary_phone'].strip()
        email = req.POST['email'].strip()
        telephone_preferred = req.POST['telephone_preferred'] == 'on'
        email_preferred = req.POST['email_preferred'] == 'on'
        primary_income_source = req.POST['primary_income_source'].strip()
        employment_status = req.POST['employment_status'].strip()
        position_held = req.POST['position_held'].strip()
        employer = req.POST['employer'].strip()
        employer_address = req.POST['employer_address'].strip()
        business_type = req.POST['business_type']
        transaction_frequency = req.POST['transaction_frequency']
        politically_exposed = req.POST['politically_exposed'] == 'on'
        political_details = req.POST['political_details'].strip()

        # check for client identification info
        id_type = req.POST.getlist('id_type')
        id_number = req.POST.getlist('id_number')
        id_country = req.POST.getlist('id_country')
        issue_date = req.POST.getlist('issue_date')
        expiry_date = req.POST.getlist('expiry_date')

        # check if client already exists
        client_name = f"{first_name} {surname}"
        if ClientList.objects.filter(client_name=client_name).exists():
            messages.info(req, f"A client with the name {client_name} already exists. Please ensure that this is not a duplicate entry.")
               
        # create new client
        client = IndividualClient(
            legacy_id=legacy_id,
            first_name=first_name,
            middle_name=middle_name,
            surname=surname,
            date_of_birth=date_of_birth,
            gender=gender,
            marital_status=marital_status,
            residential_address=residential_address,
            residential_address2=residential_address2,
            residential_city=residential_city,
            residential_country=Country.objects.get(pk=residential_country),
            mailing_address=mailing_address,
            mailing_address2=mailing_address2,
            mailing_city=mailing_city,
            mailing_country=Country.objects.get(pk=mailing_country),
            country_of_birth=Country.objects.get(pk=country_of_birth),
            nationality=Country.objects.get(pk=nationality),
            dual_citizen=dual_citizen,
            dual_nationality=Country.objects.get(pk=dual_nationality),
            primary_phone=primary_phone,
            secondary_phone=secondary_phone,
            email=email,
            telephone_preferred=telephone_preferred,
            email_preferred=email_preferred,
            primary_income_source=primary_income_source,
            employment_status=employment_status,
            position_held=position_held,
            employer=employer,
            employer_address=employer_address,
            business_type=business_type,
            transaction_frequency=transaction_frequency,
            politically_exposed=politically_exposed,
            political_details=political_details,
        )

        # create client list entry
        client.client_list_entry = create_client_list_entry(client_name, "I", legacy_id)
        client.save()

        # save client identification info
        if id_type:
            for i in range(len(id_type)):
                id_info = IdentificationInfo(
                    client=client,
                    id_type=IdentificationType.objects.get(pk=int(id_type[i])),
                    id_number=id_number[i],
                    id_country=Country.objects.get(pk=int(id_country[i])),
                    issue_date=issue_date[i] or None,
                    expiry_date=expiry_date[i],
                )
                id_info.save()

        messages.success(req, f"New individual client {client_name} created successfully.")
        return redirect('clients:home')
    return render(req, 'clients/ind_client_form.html', context)


@login_required
def edit_individual(req, client_id):
    client = IndividualClient.objects.get(client_list_entry=client_id)
    context = {"page_title": f"Edit Individual Client {client.first_name} {client.surname}"}
    context["section"] = "clients"
    context['form_purpose'] = "edit"
    countries = Country.objects.all()
    id_types = IdentificationType.objects.all()
    mar_statuses = IndividualClient.MARITAL_STATUSES
    emp_statuses = IndividualClient.EMPLOYMENT_STATUSES
    trans_freq = IndividualClient.TRANSACTION_FREQUENCIES
    context["countries"] = countries
    context["id_types"] = id_types
    context |= {"mar_statuses": mar_statuses, "emp_statuses": emp_statuses, "trans_freq": trans_freq}
    # set form data
    context['formdata'] = client
    id_infos = IdentificationInfo.objects.filter(client=client)
    context['id_infos'] = id_infos

    # get fields from form
    if req.method =="POST":
        # get form data
        legacy_id = req.POST['legacy_id'].strip()
        first_name = req.POST['first_name'].strip()
        middle_name = req.POST['middle_name'].strip()
        surname = req.POST['surname'].strip()
        date_of_birth = req.POST['date_of_birth']
        gender = req.POST['gender']
        marital_status = req.POST['marital_status']
        residential_address = req.POST['residential_address'].strip()
        residential_address2 = req.POST['residential_address2'].strip()
        residential_city = req.POST['residential_city'].strip()
        residential_country = int(req.POST['residential_country'])
        mailing_address = req.POST['mailing_address'].strip()
        mailing_address2 = req.POST['mailing_address2'].strip()
        mailing_city = req.POST['mailing_city'].strip()
        mailing_country = int(req.POST['mailing_country'])
        country_of_birth = int(req.POST['country_of_birth'])
        nationality = int(req.POST['nationality'])
        dual_citizen = req.POST['dual_citizen'] == 'on'
        dual_nationality = int(req.POST['dual_nationality'])
        primary_phone = req.POST['primary_phone'].strip()
        secondary_phone = req.POST['secondary_phone'].strip()
        email = req.POST['email'].strip()
        telephone_preferred = req.POST['telephone_preferred'] == 'on'
        email_preferred = req.POST['email_preferred'] == 'on'
        primary_income_source = req.POST['primary_income_source'].strip()
        employment_status = req.POST['employment_status'].strip()
        position_held = req.POST['position_held'].strip()
        employer = req.POST['employer'].strip()
        employer_address = req.POST['employer_address'].strip()
        business_type = req.POST['business_type']
        transaction_frequency = req.POST['transaction_frequency']
        politically_exposed = req.POST['politically_exposed'] == 'on'
        political_details = req.POST['political_details'].strip()

        # update client
        client.legacy_id = legacy_id
        client.first_name = first_name
        client.middle_name = middle_name
        client.surname = surname
        client.date_of_birth = date_of_birth
        client.gender = gender
        client.marital_status = marital_status
        client.residential_address = residential_address
        client.residential_address2 = residential_address2
        client.residential_city = residential_city
        client.residential_country = Country.objects.get(pk=residential_country)
        client.mailing_address = mailing_address
        client.mailing_address2 = mailing_address2
        client.mailing_city = mailing_city
        client.mailing_country = Country.objects.get(pk=mailing_country)
        client.country_of_birth = Country.objects.get(pk=country_of_birth)
        client.nationality = Country.objects.get(pk=nationality)
        client.dual_citizen = dual_citizen
        client.dual_nationality = Country.objects.get(pk=dual_nationality)
        client.primary_phone = primary_phone
        client.secondary_phone = secondary_phone
        client.email = email
        client.telephone_preferred = telephone_preferred
        client.email_preferred = email_preferred
        client.primary_income_source = primary_income_source
        client.employment_status = employment_status
        client.position_held = position_held
        client.employer = employer
        client.employer_address = employer_address
        client.business_type = business_type
        client.transaction_frequency = transaction_frequency
        client.politically_exposed = politically_exposed
        client.political_details = political_details
        # update client list entry
        client.client_list_entry.client_name = f"{first_name} {surname}"
        client.client_list_entry.legacy_id = legacy_id
        client.save()

        # check for client identification info
        id_info_id = req.POST.getlist('id_info_id')
        id_type = req.POST.getlist('id_type')
        id_number = req.POST.getlist('id_number')
        id_country = req.POST.getlist('id_country')
        issue_date = req.POST.getlist('issue_date')
        expiry_date = req.POST.getlist('expiry_date')
              
        # update client identification info
        if id_type:
            for i in range(len(id_type)):
                # create new id info if id_info_id is empty
                if not id_info_id[i]:
                    new_id_info = IdentificationInfo(
                        client=client,
                        id_type=IdentificationType.objects.get(pk=int(id_type[i])),
                        id_number=id_number[i],
                        id_country=Country.objects.get(pk=int(id_country[i])),
                        issue_date=issue_date[i] or None,
                        expiry_date=expiry_date[i],
                    )
                    new_id_info.save()
                else:
                # update existing id info
                    id_info = IdentificationInfo.objects.get(pk=int(id_info_id[i]))
                    id_info.id_type = IdentificationType.objects.get(pk=int(id_type[i]))
                    id_info.id_number = id_number[i]
                    id_country=Country.objects.get(pk=int(id_country[i])),
                    id_info.issue_date = issue_date[i] or None
                    id_info.expiry_date = expiry_date[i]
                    id_info.save()
                    
        # delete removed id info    
        for id_info in id_infos:
            if str(id_info.id) not in id_info_id:
                id_info.delete()

        messages.success(req, f"Individual client {first_name} {surname} updated successfully.")
        return redirect('clients:home')

    return render(req, 'clients/ind_client_form.html', context)


@login_required
def new_corporate(req):
    context = {"page_title": "New Corporate Client"}
    context["section"] = "clients"
    context['form_purpose'] = "new"
    countries = Country.objects.all()
    entity_types = CorporateClient.ENTITY_TYPES
    trans_freq = IndividualClient.TRANSACTION_FREQUENCIES
    context |= {"countries": countries, "entity_types": entity_types, "trans_freq": trans_freq}

    # get fields from form
    if req.method =="POST":
        # get form data
        legacy_id = req.POST['legacy_id'].strip()
        registered_name = req.POST['registered_name'].strip()
        date_of_incorporation = req.POST['date_of_incorporation']
        country_of_incorporation = int(req.POST['country_of_incorporation'])
        registration_number = req.POST['registration_number'].strip()
        bir_number = req.POST['bir_number'].strip()
        vat_registration = req.POST['vat_registration'].strip()
        parent_company = req.POST['parent_company'].strip()
        registered_address = req.POST['registered_address'].strip()
        registered_address2 = req.POST['registered_address2'].strip()
        registered_city = req.POST['registered_city'].strip()
        registered_country = int(req.POST['registered_country'])
        mailing_address = req.POST['mailing_address'].strip()
        mailing_address2 = req.POST['mailing_address2'].strip()
        mailing_city = req.POST['mailing_city'].strip()
        mailing_country = int(req.POST['mailing_country'])
        contact_person = req.POST['contact_person'].strip()
        primary_phone = req.POST['primary_phone'].strip()
        secondary_phone = req.POST['secondary_phone'].strip()
        email = req.POST['email'].strip()
        website = req.POST['website'].strip()
        telephone_preferred = req.POST['telephone_preferred'] == 'on'
        email_preferred = req.POST['email_preferred'] == 'on'
        entity_type = req.POST['entity_type']
        business_type = req.POST['business_type'].strip()
        transaction_frequency = req.POST['transaction_frequency']
        politically_exposed = req.POST['politically_exposed'] == 'on'
        political_details = req.POST['political_details'].strip()

        # check if client already exists
        client_name = registered_name
        if ClientList.objects.filter(client_name=client_name).exists():
            messages.info(req, f"A client with the name {client_name} already exists. Please ensure that this is not a duplicate entry.")
               
        # create new client and save
        client = CorporateClient(
            legacy_id=legacy_id,
            registered_name=registered_name,
            date_of_incorporation=date_of_incorporation,
            country_of_incorporation=Country.objects.get(pk=country_of_incorporation),
            registration_number=registration_number,
            bir_number=bir_number,
            vat_registration=vat_registration,
            parent_company=parent_company,
            registered_address=registered_address,
            registered_address2=registered_address2,
            registered_city=registered_city,
            registered_country=Country.objects.get(pk=registered_country),
            mailing_address=mailing_address,
            mailing_address2=mailing_address2,
            mailing_city=mailing_city,
            mailing_country=Country.objects.get(pk=mailing_country),
            contact_person=contact_person,
            primary_phone=primary_phone,
            secondary_phone=secondary_phone,
            email=email,
            website=website,
            telephone_preferred=telephone_preferred,
            email_preferred=email_preferred,
            entity_type=entity_type,
            business_type=business_type,
            transaction_frequency=transaction_frequency,
            politically_exposed=politically_exposed,
            political_details=political_details,
        )
        # create client list entry
        client.client_list_entry = create_client_list_entry(client_name, "C", legacy_id)
        client.save()
        messages.success(req, f"New corporate client {client_name} created successfully.")
        return redirect('clients:home')
    return render(req, 'clients/corp_client_form.html', context)


@login_required
def edit_corporate(req, client_id):
    client = CorporateClient.objects.get(client_list_entry=client_id)
    context = {"page_title": f"Edit Corporate Client {client.registered_name}"}
    context["section"] = "clients"
    context['form_purpose'] = "edit"
    countries = Country.objects.all()
    entity_types = CorporateClient.ENTITY_TYPES
    trans_freq = IndividualClient.TRANSACTION_FREQUENCIES
    context |= {"countries": countries, "entity_types": entity_types, "trans_freq": trans_freq}
    # set form data
    context['formdata'] = client

    # get fields from form
    if req.method =="POST":
        # get form data
        legacy_id = req.POST['legacy_id'].strip()
        registered_name = req.POST['registered_name'].strip()
        date_of_incorporation = req.POST['date_of_incorporation']
        registration_number = req.POST['registration_number'].strip()
        bir_number = req.POST['bir_number'].strip()
        vat_registration = req.POST['vat_registration'].strip()
        parent_company = req.POST['parent_company'].strip()
        registered_address = req.POST['registered_address'].strip()
        registered_address2 = req.POST['registered_address2'].strip()
        registered_city = req.POST['registered_city'].strip()
        mailing_address = req.POST['mailing_address'].strip()
        mailing_address2 = req.POST['mailing_address2'].strip()
        mailing_city = req.POST['mailing_city'].strip()
        contact_person = req.POST['contact_person'].strip()
        primary_phone = req.POST['primary_phone'].strip()
        secondary_phone = req.POST['secondary_phone'].strip()
        email = req.POST['email'].strip()
        website = req.POST['website'].strip()
        telephone_preferred = req.POST['telephone_preferred'] == 'on'
        email_preferred = req.POST['email_preferred'] == 'on'
        entity_type = req.POST['entity_type']
        business_type = req.POST['business_type'].strip()
        transaction_frequency = req.POST['transaction_frequency']

        # update client
        client.legacy_id = legacy_id
        client.registered_name = registered_name
        client.date_of_incorporation = date_of_incorporation
        client.registration_number = registration_number
        client.bir_number = bir_number
        client.vat_registration = vat_registration
        client.parent_company = parent_company
        client.registered_address = registered_address
        client.registered_address2 = registered_address2
        client.registered_city = registered_city
        client.mailing_address = mailing_address
        client.mailing_address2 = mailing_address2
        client.mailing_city = mailing_city
        client.contact_person = contact_person
        client.primary_phone = primary_phone
        client.secondary_phone = secondary_phone
        client.email = email
        client.website = website
        client.telephone_preferred = telephone_preferred
        client.email_preferred = email_preferred
        client.entity_type = entity_type
        client.business_type = business_type
        client.transaction_frequency = transaction_frequency
        # update client list entry
        client.client_list_entry.client_name = registered_name
        client.client_list_entry.legacy_id = legacy_id
        client.save()
        messages.success(req, f"Corporate client {client.registered_name} updated successfully.")
        return redirect('clients:home')
    return render(req, 'clients/corp_client_form.html', context)


# send beneficiary information
def client_beneficiaries(req, client):
    context = {"page_title": f"{client.client_list_entry} Beneficiaries"}
    context["section"] = "clients"
    context['client'] = client
    beneficiaries = BeneficiaryBank.objects.filter(client=client.client_list_entry)
    context['beneficiaries'] = beneficiaries
    return render(req, 'clients/beneficiaries.html', context)

@login_required
def beneficiaries_i(req, client_id):
    client = IndividualClient.objects.get(pk=client_id)
    return client_beneficiaries(req, client)

@login_required
def beneficiaries_c(req, client_id):
    client = CorporateClient.objects.get(pk=client_id)
    return client_beneficiaries(req, client)


# create new beneficiary
def new_beneficiary(req, client):
    context = {"page_title": f"New Beneficiary for {client.client_list_entry}"}
    context["section"] = "clients"
    context['client'] = client
    context['form_purpose'] = "new"
    context['show_special_instructions'] = True
    countries = Country.objects.all()
    context["countries"] = countries
    context["account_types"] = DFLLocalBank.ACCOUNT_TYPES
    context["currencies"] = Currency.objects.all().exclude(currency_code="TTD")

    
    # get fields from form    
    if req.method =="POST":
        # get form data
        currency = req.POST['currency']
        bank_name = req.POST['bank_name'].strip()
        bank_address = req.POST['bank_address'].strip()
        bank_address2 = req.POST['bank_address2'].strip()
        bank_city = req.POST['bank_city'].strip()
        bank_state = req.POST['bank_state'].strip()
        bank_zip = req.POST['bank_zip'].strip()
        bank_country = int(req.POST['bank_country'])
        account_number = req.POST['account_number'].strip()
        account_type = req.POST['account_type'].strip()
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
        intermediary_swift_code = req.POST['intermediary_swift_code'].strip()
        intermediary_iban_code = req.POST['intermediary_iban_code'].strip()
        intermediary_aba_code = req.POST['intermediary_aba_code'].strip()
        special_instructions = req.POST['special_instructions'].strip()

        # create new beneficiary and save
        beneficiary = BeneficiaryBank(
            client=client.client_list_entry,
            bank_name=bank_name,
            bank_address=bank_address,
            bank_address2=bank_address2,
            bank_city=bank_city,
            bank_state=bank_state,
            bank_zip=bank_zip,
            bank_country=Country.objects.get(pk=bank_country),
            account_number=account_number,
            account_type=account_type,
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
            intermediary_swift_code=intermediary_swift_code,
            intermediary_iban_code=intermediary_iban_code,
            intermediary_aba_code=intermediary_aba_code,
            special_instructions=special_instructions,
            currency=Currency.objects.get(pk=currency)
        )
        beneficiary.save()
        messages.success(req, f"New beneficiary for client {client.client_list_entry} created successfully.")
        if client.client_list_entry.client_type == "I":
            return redirect('clients:beneficiaries_i', client_id=client.id)
        else:
            return redirect('clients:beneficiaries_c', client_id=client.id)
    return render(req, "setup/international_account_form.html", context)

@login_required
def new_i_beneficiary(req, client_id):
    client = IndividualClient.objects.get(pk=client_id)
    return new_beneficiary(req, client)
    
@login_required
def new_c_beneficiary(req, client_id):
    client = CorporateClient.objects.get(pk=client_id)
    return new_beneficiary(req, client)


# edit beneficiary
def edit_beneficiary(req, client, beneficiary_id):
    beneficiary = BeneficiaryBank.objects.get(pk=beneficiary_id)
    countries = Country.objects.all()
    context = {"page_title": f"Edit Beneficiary {beneficiary.bank_name}"}
    context["section"] = "clients"
    context['client'] = client
    context['form_purpose'] = "edit"
    context['show_special_instructions'] = True
    context["countries"] = countries
    context["account_types"] = DFLLocalBank.ACCOUNT_TYPES
    context["currencies"] = Currency.objects.all().exclude(currency_code="TTD")
    # set form data
    context['formdata'] = beneficiary

    # get fields from form
    if req.method =="POST":
        # get form data 
        currency = req.POST['currency']
        bank_name = req.POST['bank_name'].strip()
        bank_address = req.POST['bank_address'].strip()
        bank_address2 = req.POST['bank_address2'].strip()
        bank_city = req.POST['bank_city'].strip()
        bank_state = req.POST['bank_state'].strip()
        bank_zip = req.POST['bank_zip'].strip()
        bank_country = int(req.POST['bank_country'])
        account_number = req.POST['account_number'].strip()
        account_type = req.POST['account_type'].strip()
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
        intermediary_swift_code = req.POST['intermediary_swift_code'].strip()
        intermediary_iban_code = req.POST['intermediary_iban_code'].strip()
        intermediary_aba_code = req.POST['intermediary_aba_code'].strip()
        special_instructions = req.POST['special_instructions'].strip()

        # update beneficiary
        beneficiary.bank_name=bank_name
        beneficiary.bank_address=bank_address
        beneficiary.bank_address2=bank_address2
        beneficiary.bank_city=bank_city
        beneficiary.bank_state=bank_state
        beneficiary.bank_zip=bank_zip
        beneficiary.bank_country=Country.objects.get(pk=bank_country)
        beneficiary.account_number=account_number
        beneficiary.account_type=account_type
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
        beneficiary.intermediary_swift_code=intermediary_swift_code
        beneficiary.intermediary_iban_code=intermediary_iban_code
        beneficiary.intermediary_aba_code=intermediary_aba_code
        beneficiary.special_instructions=special_instructions
        beneficiary.currency=Currency.objects.get(pk=currency)
        beneficiary.save()
        messages.success(req, f"Beneficiary for client {client.client_list_entry} updated successfully.")
        return redirect('clients:home')
    return render(req, "setup/international_account_form.html", context)

@login_required
def edit_i_beneficiary(req, client_id, beneficiary_id):
    client = IndividualClient.objects.get(pk=client_id)
    return edit_beneficiary(req, client, beneficiary_id)

@login_required
def edit_c_beneficiary(req, client_id, beneficiary_id):
    client = CorporateClient.objects.get(pk=client_id)
    return edit_beneficiary(req, client, beneficiary_id)

@login_required
def list_client_bank_accounts_i(req, client_id):
    client = get_object_or_404(IndividualClient, pk=client_id)
    bank_accounts = ClientLocalBank.objects.filter(client=client.client_list_entry)
    context = {
        "page_title": f"Bank Accounts for {client.client_list_entry.client_name}",
        "section": "clients",
        "bank_accounts": bank_accounts,
        "add_url": reverse('clients:add_bank_account_i', args=[client_id]),
        "edit_url_name": 'clients:edit_bank_account_i',
        "default_account_owner": client.client_list_entry.client_name,
        "client": client
    }
    return render(req, 'setup/list_bank_accounts.html', context)

@login_required
def list_client_bank_accounts_c(req, client_id):
    client = get_object_or_404(CorporateClient, pk=client_id)
    bank_accounts = ClientLocalBank.objects.filter(client=client.client_list_entry)
    context = {
        "page_title": f"Bank Accounts for {client.client_list_entry.client_name}",
        "section": "clients",
        "bank_accounts": bank_accounts,
        "add_url": reverse('clients:add_bank_account_c', args=[client_id]),
        "edit_url_name": 'clients:edit_bank_account_c',
        "default_account_owner": client.client_list_entry.client_name,
        "client": client
    }
    return render(req, 'setup/list_bank_accounts.html', context)

@login_required
def add_client_bank_account_i(req, client_id):
    client = get_object_or_404(IndividualClient, pk=client_id)
    return add_client_bank_account(req, client)

@login_required
def add_client_bank_account_c(req, client_id):
    client = get_object_or_404(CorporateClient, pk=client_id)
    return add_client_bank_account(req, client)

def add_client_bank_account(req, client):
    context = {
        "page_title": f"Add Bank Account for {client.client_list_entry.client_name}",
        "section": "clients",
        "account_types": DFLLocalBank.ACCOUNT_TYPES,
        "default_account_owner": client.client_list_entry.client_name,
        "form_action": reverse(f'clients:add_bank_account_{client.client_list_entry.client_type.lower()}', args=[client.id]),
        "cancel_url": reverse(f'clients:list_bank_accounts_{client.client_list_entry.client_type.lower()}', args=[client.id]),
        "client": client
    }
    
    if req.method == 'POST':
        try:
            bank_account = ClientLocalBank(
                client=client.client_list_entry,
                account_owner=req.POST['account_owner'],
                bank_name=req.POST['bank_name'],
                branch_city=req.POST['branch_city'],
                branch_number=req.POST['branch_number'],
                account_number=req.POST['account_number'],
                account_type=req.POST['account_type']
            )
            bank_account.save()
            messages.success(req, 'Bank account added successfully')
            return redirect(f"clients:list_bank_accounts_{client.client_list_entry.client_type.lower()}", client_id=client.id)
        except Exception as e:
            messages.error(req, f'Error adding bank account: {str(e)}')
            return render(req, 'setup/bank_account_form.html', context)
    
    return render(req, 'setup/bank_account_form.html', context)

@login_required
def edit_client_bank_account_i(req, client_id, account_id):
    client = get_object_or_404(IndividualClient, pk=client_id)
    return edit_client_bank_account(req, client, account_id)

@login_required
def edit_client_bank_account_c(req, client_id, account_id):
    client = get_object_or_404(CorporateClient, pk=client_id)
    return edit_client_bank_account(req, client, account_id)

def edit_client_bank_account(req, client, account_id):
    bank_account = get_object_or_404(ClientLocalBank, pk=account_id)
    
    # Verify that the bank account belongs to the client
    if bank_account.client != client.client_list_entry:
        messages.error(req, 'Invalid bank account access attempt')
        return redirect(f'clients:list_bank_accounts_{client.client_list_entry.client_type.lower()}', client_id=client.id)
    
    context = {
        "page_title": f"Edit Bank Account for {client.client_list_entry.client_name}",
        "section": "clients",
        "account_types": DFLLocalBank.ACCOUNT_TYPES,
        "form_action": reverse(f'clients:edit_bank_account_{client.client_list_entry.client_type.lower()}', args=[client.id, account_id]),
        "cancel_url": reverse(f'clients:list_bank_accounts_{client.client_list_entry.client_type.lower()}', args=[client.id]),
        "formdata": bank_account,
        "client": client
    }
    
    if req.method == 'POST':
        try:
            bank_account.account_owner = req.POST['account_owner']
            bank_account.bank_name = req.POST['bank_name']
            bank_account.branch_city = req.POST['branch_city']
            bank_account.branch_number = req.POST['branch_number']
            bank_account.account_number = req.POST['account_number']
            bank_account.account_type = req.POST['account_type']
            bank_account.save()
            messages.success(req, 'Bank account updated successfully')
            return redirect(f'clients:list_bank_accounts_{client.client_list_entry.client_type.lower()}', client_id=client.id)
        except Exception as e:
            messages.error(req, f'Error updating bank account: {str(e)}')
            return render(req, 'setup/bank_account_form.html', context)
    
    return render(req, 'setup/bank_account_form.html', context)
