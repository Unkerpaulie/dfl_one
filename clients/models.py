from django.db import models
from django.dispatch import Signal
from core.models import Country, IdentificationType, LocalBankAccount, InternationalBankAccount


class ClientList(models.Model):
    client_name = models.CharField(max_length=200)
    client_type = models.CharField(max_length=1, choices=[("I", "Individual"), ("C", "Corporate")])
    legacy_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.client_name} ({self.get_client_type_display()})"


class IndividualClient(models.Model):
    client_list_entry = models.OneToOneField(ClientList, related_name="source_individual", on_delete=models.CASCADE, null=True, blank=True)
    # choice lists
    MARITAL_STATUSES = [("S", "Single"), ("M", "Married"), ("D", "Divorced"), ("W", "Widowed"), ("O", "Other")]
    EMPLOYMENT_STATUSES = [("E", "Employed"), ("S", "Self-Employed"), ("O", "Other")]
    TRANSACTION_FREQUENCIES = [("M", "Monthly"), ("Q", "Quarterly"), ("Y", "Annually")]
    legacy_id = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    surname = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUSES)
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
    employment_status = models.CharField(max_length=1, choices=EMPLOYMENT_STATUSES)
    position_held = models.CharField(max_length=200, null=True, blank=True)
    employer = models.CharField(max_length=200, null=True, blank=True)
    employer_address = models.CharField(max_length=200, null=True, blank=True)
    business_type = models.CharField(max_length=200, null=True, blank=True)
    transaction_frequency = models.CharField(max_length=1, choices=TRANSACTION_FREQUENCIES)
    politically_exposed = models.BooleanField(default=False)
    political_details = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.surname}"


class CorporateClient(models.Model):
    # choice lists
    client_list_entry = models.OneToOneField(ClientList, related_name="source_corporation", on_delete=models.CASCADE, null=True, blank=True)
    ENTITY_TYPES = [("L", "Limited Liability"), ("P", "Partnership"), ("T", "Trust"), ("S", "Sole Trader"), ("G", "Government Enterprise")]
    TRANSACTION_FREQUENCIES = [("M", "Monthly"), ("Q", "Quarterly"), ("Y", "Annually")]

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
    entity_type = models.CharField(max_length=1, choices=ENTITY_TYPES)
    business_type = models.CharField(max_length=200, null=True, blank=True)
    transaction_frequency = models.CharField(max_length=1, choices=TRANSACTION_FREQUENCIES)
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

    
class BeneficiaryBank(InternationalBankAccount):
    client = models.ForeignKey(ClientList, related_name="beneficiaries", on_delete=models.CASCADE)
    special_instructions = models.TextField(null=True, blank=True)

    
class ClientLocalBank(LocalBankAccount):
    client = models.ForeignKey(ClientList, related_name="local_banks", on_delete=models.CASCADE)
