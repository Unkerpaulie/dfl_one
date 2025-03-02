from django.db import models
from core.models import LocalBankAccount, InternationalBankAccount, Currency


class BankFee(models.Model):
    bank_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.bank_fee)
    
class DFLLocalBank(LocalBankAccount):
    class Meta:
        verbose_name_plural = "DFL Bank Accounts"

class DFLInternationalBank(InternationalBankAccount):
    account_type = models.CharField(max_length=2, choices=LocalBankAccount.ACCOUNT_TYPES)
    
    def __str__(self):
        return f"{self.bank_name} ({self.currency.currency_code})"