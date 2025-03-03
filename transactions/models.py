from django.db import models
from clients.models import ClientList, BeneficiaryBank, ClientLocalBank
from core.models import Currency, DealStatus
from account.models import User
from setup.models import DFLLocalBank, DFLInternationalBank


class Transaction(models.Model):
    TRANSACTION_TYPES = [("P", "Purchase"), ("S", "Sale")]
    INPAYMENT_TYPES = [("cash", "Cash"), ("check", "Check"), ("local", "Local Bank Transfer"), ("foreign", "Foreign Bank Account")]

    client = models.ForeignKey(ClientList, on_delete=models.CASCADE)
    contract_date = models.DateField()
    value_date = models.DateField()
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    foreign_currency = models.ForeignKey(Currency, related_name="exhanged_from", on_delete=models.CASCADE)
    foreign_amount = models.DecimalField(max_digits=16, decimal_places=2)
    foreign_currency_rate = models.DecimalField(max_digits=10, decimal_places=4)
    settlement_currency = models.ForeignKey(Currency, related_name="exchanged_to", on_delete=models.CASCADE)
    settlement_amount = models.DecimalField(max_digits=16, decimal_places=2)
    settlement_currency_rate = models.DecimalField(max_digits=10, decimal_places=4)
    bank_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    deal_status = models.ForeignKey(DealStatus, on_delete=models.CASCADE)
    # inbound payment options to DFL
    in_payment_type = models.CharField(max_length=10, choices=INPAYMENT_TYPES)
    check_number = models.CharField(max_length=20, null=True, blank=True)
    dfl_local_bank_account = models.ForeignKey(DFLLocalBank, on_delete=models.CASCADE, null=True, blank=True)
    dfl_intl_bank_account = models.ForeignKey(DFLInternationalBank, on_delete=models.CASCADE, null=True, blank=True)
    # outbound payment options to client
    cash_settlement = models.BooleanField(default=False)
    fixed_deposit = models.BooleanField(default=False)
    fixed_deposit_cert = models.CharField(max_length=255, null=True, blank=True)
    client_local_bank_account = models.ForeignKey(ClientLocalBank, on_delete=models.CASCADE, null=True, blank=True)
    client_beneficiary_account = models.ForeignKey(BeneficiaryBank, on_delete=models.CASCADE, null=True, blank=True)
    payment_details = models.CharField(max_length=255, null=True, blank=True)

    trader = models.ForeignKey(User, related_name="trader", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(User, related_name="updater", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{'Purchased' if self.transaction_type == 'P' else 'Sold'} {self.foreign_currency}{self.foreign_amount} from {self.client.client_name} on {self.value_date}"

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
