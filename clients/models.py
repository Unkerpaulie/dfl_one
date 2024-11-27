from django.db import models


class ClientType(models.Model):
    ClientTypeID = models.IntegerField(primary_key=True)
    ClientType1 = models.CharField(max_length=50)

    def __str__(self):
        return self.ClientType1

class ClientSubType(models.Model):
    ClientTypeSubID = models.ForeignKey(ClientType, on_delete=models.CASCADE)
    ClientTypeSub1 = models.CharField(max_length=50)

    def __str__(self):
        return self.ClientTypeSub1

class ClientStatus(models.Model):
    ClientStatusID = models.IntegerField(primary_key=True)
    Status = models.CharField(max_length=50)

    def __str__(self):
        return self.Status

class ClientAMLRiskRating(models.Model):
    ClientAMLRiskRatingID = models.IntegerField(primary_key=True)
    ClientAMLRiskRating1 = models.CharField(max_length=50)
    Min = models.IntegerField()
    Max = models.IntegerField()

    def __str__(self):
        return self.ClientAMLRiskRating1

class ClientAccountStatus(models.Model):
    ClientAccountStatusID = models.IntegerField(primary_key=True)
    ClientAccountStatus1 = models.CharField(max_length=50)

    def __str__(self):
        return self.ClientAccountStatus1

class Country(models.Model):
    CountryID = models.IntegerField(primary_key=True)
    CountryName = models.CharField(max_length=200)
    CountryCode = models.CharField(max_length=5)

    def __str__(self):
        return self.CountryName

class Client(models.Model):
    ClientID = models.IntegerField(primary_key=True)
    DateOpened = models.DateField()
    ClientType = models.ForeignKey(ClientType, on_delete=models.CASCADE)
    ClientSubType = models.ForeignKey(ClientSubType, on_delete=models.CASCADE)
    ClientName = models.CharField(max_length=200)
    ClientStatusID = models.ForeignKey(ClientStatus, on_delete=models.CASCADE)
    ClientAMLRiskRatingID = models.ForeignKey(ClientAMLRiskRating, on_delete=models.CASCADE)
    PEP = models.IntegerField()
    USPerson = models.IntegerField()
    ClientAccountStatus = models.ForeignKey(ClientAccountStatus, on_delete=models.CASCADE)
    ClientAddress1 = models.CharField(max_length=200)
    ClientAddress2 = models.CharField(max_length=200, blank=True, null=True)
    ClientAddressCity = models.CharField(max_length=200)
    ClientAddressState = models.CharField(max_length=50, blank=True, null=True)
    ClientAddressZipCode = models.CharField(max_length=15, blank=True, null=True)
    CountryID = models.ForeignKey(Country, on_delete=models.CASCADE)
    ClientPhone = models.CharField(max_length=50, blank=True, null=True)
    ClientFax = models.CharField(max_length=15, blank=True, null=True)
    ClientEmail = models.CharField(max_length=200, blank=True, null=True)
    ClientWebsite = models.CharField(max_length=200, blank=True, null=True)
    ClientApprovalStatus = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Countries"
        
    def __str__(self):
        return self.ClientName

class BeneficiaryBank(models.Model):
    client = models.ForeignKey(Client, related_name="beneficiaries", on_delete=models.CASCADE)
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