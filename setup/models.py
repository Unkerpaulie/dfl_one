from django.db import models
from core.models import Currency, LocalBankAccount
from account.models import User
from transactions.models import Transaction

class CurrencyStock(models.Model):
    ADJUSTMENTS = [(1, 'Increase'), (-1, 'Decrease')]
    ADJUSTMENT_SOURCES = [("M", 'Manual'), ("X", 'Exchange'), ("F", "Fake")]
    source_transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    adjustment_source = models.CharField(max_length=1, choices=ADJUSTMENT_SOURCES)
    adjustment_type = models.IntegerField(choices=ADJUSTMENTS)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=4)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    effective_date = models.DateField()
    comment = models.CharField(max_length=200, null=True, blank=True)
    entered_by = models.ForeignKey(User, related_name='entered_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(User, related_name='last_updated_by', on_delete=models.CASCADE)
    last_updated_at = models.DateTimeField(auto_now=True)

    @property
    def adjustment_amount(self):
        return self.adjustment_type * self.amount

    def __str__(self):
        return f"{self.created_at.date()}: {self.currency} {self.adjustment_type} x {self.amount} ({self.adjustment_source})"


class BankFee(models.Model):
    bank_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.bank_fee)
    
class DFLLocalBank(LocalBankAccount):
    class Meta:
        verbose_name_plural = "DFL Bank Accounts"