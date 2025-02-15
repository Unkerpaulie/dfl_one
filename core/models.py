from django.db import models

# no longer in use
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
    ACCUOUNT_TYPES = [
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
    account_type = models.CharField(max_length=2, choices=ACCUOUNT_TYPES)

    class Meta: 
        abstract = True

    def __str__(self):
        return f"{self.account_owner} {self.bank_name} {self.account_type} account"
