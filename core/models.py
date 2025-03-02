from django.db import models


class IdentificationType(models.Model):
    id_type = models.CharField(max_length=40)

    def __str__(self):
        return self.id_type
    
    
class Currency(models.Model):
    currency_name = models.CharField(max_length=140)
    currency_code = models.CharField(max_length=5)
    symbol = models.CharField(max_length=1, default="$", blank=True)

    class Meta:
        verbose_name_plural = "currencies"

    def __str__(self):
        return f"{self.currency_code}"


class DealStatus(models.Model):
    status_name = models.CharField(max_length=140)

    class Meta:
        verbose_name_plural = "deal statuses"

    def __str__(self):
        return self.status_name
    

class Country(models.Model):
    country = models.CharField(max_length=200)
    country_code = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = "Countries"
        
    def __str__(self):
        return self.country

class LocalBankAccount(models.Model):
    ACCOUNT_TYPES = [
        ("CH", "Checking"),
        ("SV", "Savings"),
        ("MM", "Money Marke Account"),
        ("CD", "Certificate of Deposit"),
    ]
    account_owner = models.CharField(max_length=150)
    bank_name = models.CharField(max_length=150)
    branch_city = models.CharField(max_length=100, blank=True, null=True)
    branch_number = models.CharField(max_length=10)
    account_number = models.CharField(max_length=16)
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES)

    class Meta: 
        abstract = True

    def __str__(self):
        return f"{self.bank_name} {self.account_type} account"

class InternationalBankAccount(models.Model):
    bank_name = models.CharField(max_length=100)
    bank_address = models.CharField(max_length=200)
    bank_address2 = models.CharField(max_length=200, null=True, blank=True)
    bank_city = models.CharField(max_length=150)
    bank_state = models.CharField(max_length=20, null=True, blank=True)
    bank_zip = models.CharField(max_length=10, null=True, blank=True)
    bank_country = models.ForeignKey(Country, 
        related_name="%(app_label)s_%(class)s_banks", 
        on_delete=models.CASCADE)
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
    recipient_country = models.ForeignKey(Country, 
        related_name="%(app_label)s_%(class)s_recipients", 
        on_delete=models.CASCADE)
    
    intermediary_bank_name = models.CharField(max_length=100, null=True, blank=True)
    intermediary_bank_address = models.CharField(max_length=200, null=True, blank=True)
    intermediary_bank_address2 = models.CharField(max_length=200, null=True, blank=True)
    intermediary_bank_city = models.CharField(max_length=150, null=True, blank=True)
    intermediary_bank_state = models.CharField(max_length=20, null=True, blank=True)
    intermediary_bank_zip = models.CharField(max_length=10, null=True, blank=True)
    intermediary_bank_country = models.ForeignKey(Country, 
        related_name="%(app_label)s_%(class)s_intermediary_banks", 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True)
    intermediary_account_number = models.CharField(max_length=30, null=True, blank=True)
    intermediary_swift_code = models.CharField(max_length=30, null=True, blank=True)
    intermediary_iban_code = models.CharField(max_length=30, null=True, blank=True)
    intermediary_aba_code = models.CharField(max_length=30, null=True, blank=True)

    account_type = models.CharField(max_length=2, choices=LocalBankAccount.ACCOUNT_TYPES)
    currency = models.ForeignKey(Currency, related_name="%(app_label)s_%(class)s_bank_accounts", on_delete=models.CASCADE)

    class Meta: 
        abstract = True

    def __str__(self):
        return f"{self.bank_name} {self.account_type} account"
