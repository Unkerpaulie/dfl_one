from django.db import models
from clients.models import Client, BeneficiaryBank
from core.models import Currency, DealStatus
from account.models import User


class Transaction(models.Model):
    transaction_types = [("P", "Purchase"), ("S", "Sale")]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contract_date = models.DateField()
    value_date = models.DateField()
    transaction_type = models.CharField(max_length=1, choices=transaction_types)
    foreign_currency = models.ForeignKey(Currency, related_name="exhanged_from", on_delete=models.CASCADE)
    foreign_amount = models.DecimalField(max_digits=16, decimal_places=2)
    foreign_currency_rate = models.DecimalField(max_digits=10, decimal_places=4)
    settlement_currency = models.ForeignKey(Currency, related_name="exchanged_to", on_delete=models.CASCADE)
    settlement_amount = models.DecimalField(max_digits=16, decimal_places=2)
    settlement_currency_rate = models.DecimalField(max_digits=10, decimal_places=4)
    # exchange_rate = models.DecimalField(max_digits=16, decimal_places=10)
    # exchange_rate = settlement_currency_rate / foreign_currency_rate
    bank_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    deal_status = models.ForeignKey(DealStatus, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(BeneficiaryBank, on_delete=models.CASCADE, null=True, blank=True)
    payment_details = models.CharField(max_length=255, null=True, blank=True)
    trader = models.ForeignKey(User, related_name="trader", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(User, related_name="updater", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{'Purchased' if self.transaction_type == 'P' else 'Sold'} {self.foreign_currency}{self.foreign_amount} from {self.client.ClientName} on {self.value_date}"
