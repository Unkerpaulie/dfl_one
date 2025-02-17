from django.db import models
from django.dispatch import Signal
from core.models import Country, IdentificationType, LocalBankAccount


class ClientList(models.Model):
    client_name = models.CharField(max_length=200)
    client_type = models.CharField(max_length=1, choices=[("I", "Individual"), ("C", "Corporate")])
    legacy_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.client_name} ({self.get_client_type_display()})"


class IndividualClient(models.Model):
    client_list_entry = models.OneToOneField(ClientList, related_name="source_individual", on_delete=models.CASCADE, null=True, blank=True)
    # choice lists
    mar_statuses = [
        ("S", "Single"),
        ("M", "Married"),
        ("D", "Divorced"),
        ("W", "Widowed"),
        ("O", "Other"),
    ]
    emp_statuses = [("E", "Employed"), ("S", "Self-Employed"), ("O", "Other")]
    trans_freq = [("M", "Monthly"), ("Q", "Quarterly"), ("Y", "Annually")]
    legacy_id = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    surname = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    marital_status = models.CharField(max_length=1, choices=mar_statuses)
    residential_address = models.CharField(max_length=200)
    residential_address2 = models.CharField(max_length=200, null=True, blank=True)
    residential_city = models.CharField(max_length=150)
    residential_country = models.ForeignKey(Country, related_name="clients_residing_here", on_delete=models.CASCADE)
    mailing_address = models.CharField(max_length=200, null=True, blank=True)
    mailing_address2 = models.CharField(max_length=200, null=True, blank=True)
    mailing_city = models.CharField(max_length=150, null=True, blank=True)
    mailing_country = models.ForeignKey(Country, related_name="clients_mailed_here", on_delete=models.CASCADE, null=True, blank=True)
    country_of_birth = models.ForeignKey(Country, related_name="clients_born_here", on_delete=models.CASCADE)
    nationality = models.ForeignKey(Country, related_name="clients_nationality", on_delete=models.CASCADE)
    dual_citizen = models.BooleanField(default=False)
    dual_nationality = models.ForeignKey(Country, related_name="clients_dual_nationality", on_delete=models.CASCADE, null=True, blank=True)
    primary_phone = models.CharField(max_length=15)
    secondary_phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=200)
    telephone_preferred = models.BooleanField(default=False)
    email_preferred = models.BooleanField(default=False)
    primary_income_source = models.CharField(max_length=200)
    employment_status = models.CharField(max_length=1, choices=emp_statuses)
    position_held = models.CharField(max_length=200, null=True, blank=True)
    employer = models.CharField(max_length=200, null=True, blank=True)
    employer_address = models.CharField(max_length=200, null=True, blank=True)
    business_type = models.CharField(max_length=200, null=True, blank=True)
    transaction_frequency = models.CharField(max_length=1, choices=trans_freq)
    politically_exposed = models.BooleanField(default=False)
    political_details = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.surname}"


class CorporateClient(models.Model):
    # choice lists
    client_list_entry = models.OneToOneField(ClientList, related_name="source_corporation", on_delete=models.CASCADE, null=True, blank=True)
    entity_types = [
        ("L", "Limited Liability"),
        ("P", "Partnership"),
        ("T", "Trust"),
        ("S", "Sole Trader"),
        ("G", "Government Enterprise"),
        ("O", "Other"),
    ]
    trans_freq = [("M", "Monthly"), ("Q", "Quarterly"), ("Y", "Annually")]

    legacy_id = models.CharField(max_length=20, null=True, blank=True)
    registered_name = models.CharField(max_length=250)
    registration_number = models.CharField(max_length=15)
    date_of_incorporation = models.DateField()
    country_of_incorporation = models.ForeignKey(Country, related_name="clients_incorporated_here", on_delete=models.CASCADE)
    bir_number = models.CharField(max_length=15)
    vat_registration = models.CharField(max_length=15)
    parent_company = models.CharField(max_length=250, null=True, blank=True)
    registered_address = models.CharField(max_length=200)
    registered_address2 = models.CharField(max_length=200, null=True, blank=True)
    registered_city = models.CharField(max_length=150)
    registered_country = models.ForeignKey(Country, related_name="clients_registered_here", on_delete=models.CASCADE)
    mailing_address = models.CharField(max_length=200, null=True, blank=True)
    mailing_address2 = models.CharField(max_length=200, null=True, blank=True)
    mailing_city = models.CharField(max_length=150, null=True, blank=True)
    mailing_country = models.ForeignKey(Country, related_name="corp_clients_mailed_here", on_delete=models.CASCADE, null=True, blank=True)
    contact_person = models.CharField(max_length=150)
    primary_phone = models.CharField(max_length=15)
    secondary_phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=200)
    website = models.EmailField(max_length=200, null=True, blank=True)
    telephone_preferred = models.BooleanField(default=False)
    email_preferred = models.BooleanField(default=False)
    website = models.CharField(max_length=250)
    entity_type = models.CharField(max_length=1, choices=entity_types)
    business_type = models.CharField(max_length=200, null=True, blank=True)
    transaction_frequency = models.CharField(max_length=1, choices=trans_freq)
    politically_exposed = models.BooleanField(default=False)
    political_details = models.CharField(max_length=200, null=True, blank=True)
   
    def __str__(self):
        return self.registered_name


class IdentificationInfo(models.Model):
    client = models.ForeignKey(IndividualClient, on_delete=models.CASCADE)
    id_type = models.ForeignKey(IdentificationType, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20)
    id_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.client} {self.id_type}"

    
class BeneficiaryBank(models.Model):
    client = models.ForeignKey(ClientList, related_name="beneficiaries", on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    bank_address = models.CharField(max_length=200)
    bank_address2 = models.CharField(max_length=200, null=True, blank=True)
    bank_city = models.CharField(max_length=150)
    bank_state = models.CharField(max_length=20, null=True, blank=True)
    bank_zip = models.CharField(max_length=10, null=True, blank=True)
    bank_country = models.ForeignKey(Country, related_name="banks_from_here", on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30)
    swift_code = models.CharField(max_length=30, null=True, blank=True)
    iban_code = models.CharField(max_length=30, null=True, blank=True)
    aba_code = models.CharField(max_length=30, null=True, blank=True)

    recipient_name = models.CharField(max_length=100)
    recipient_address = models.CharField(max_length=200)
    recipient_address2 = models.CharField(max_length=200, null=True, blank=True)
    recipient_city = models.CharField(max_length=150)
    recipient_state = models.CharField(max_length=20, null=True, blank=True)
    recipient_zip = models.CharField(max_length=10, null=True, blank=True)
    recipient_country = models.ForeignKey(Country, related_name="recipients_from_here", on_delete=models.CASCADE)
    
    intermediary_bank_name = models.CharField(max_length=100, null=True, blank=True)
    intermediary_bank_address = models.CharField(max_length=200, null=True, blank=True)
    intermediary_bank_address2 = models.CharField(max_length=200, null=True, blank=True)
    intermediary_bank_city = models.CharField(max_length=150, null=True, blank=True)
    intermediary_bank_state = models.CharField(max_length=20, null=True, blank=True)
    intermediary_bank_zip = models.CharField(max_length=10, null=True, blank=True)
    intermediary_bank_country = models.ForeignKey(Country, related_name="intermediary_banks_from_here", on_delete=models.CASCADE, null=True, blank=True)
    intermediary_account_number = models.CharField(max_length=30, null=True, blank=True)
    intermediary_swift_code = models.CharField(max_length=30, null=True, blank=True)
    intermediary_iban_code = models.CharField(max_length=30, null=True, blank=True)
    intermediary_aba_code = models.CharField(max_length=30, null=True, blank=True)
    special_instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.client}: {self.bank_name} - {self.account_number}"
    
class ClientLocalBank(LocalBankAccount):
    client = models.ForeignKey(ClientList, related_name="local_banks", on_delete=models.CASCADE)
