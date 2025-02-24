from django.db import models
from core.models import LocalBankAccount


class BankFee(models.Model):
    bank_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.bank_fee)
    
class DFLLocalBank(LocalBankAccount):
    class Meta:
        verbose_name_plural = "DFL Bank Accounts"