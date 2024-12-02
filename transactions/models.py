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
    settlement_currency = models.ForeignKey(Currency, related_name="exchanged_to", on_delete=models.CASCADE)
    settlement_currency_rate = models.DecimalField(max_digits=16, decimal_places=10)
    settlement_amount = models.DecimalField(max_digits=16, decimal_places=2)
    origin_currency = models.ForeignKey(Currency, related_name="exhanged_from", on_delete=models.CASCADE)
    origin_currency_rate = models.DecimalField(max_digits=16, decimal_places=10)
    origin_amount = models.DecimalField(max_digits=16, decimal_places=2)
    # exchange_rate = models.DecimalField(max_digits=16, decimal_places=10)
    # exchange_rate = settlement_currency_rate / origin_currency_rate
    deal_status = models.ForeignKey(DealStatus, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(BeneficiaryBank, on_delete=models.CASCADE, null=True, blank=True)
    payment_details = models.CharField(max_length=255, null=True, blank=True)
    trader = models.ForeignKey(User, related_name="trader", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(User, related_name="updater", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.transaction_type == "P":
            return f"Purchased {self.origin_currency}{self.origin_amount} from {self.client.ClientName} on {self.value_date}"
        else:
            return f"Sold {self.settlement_currency}{self.settlement_amount} to {self.client.ClientName} on {self.value_date}"