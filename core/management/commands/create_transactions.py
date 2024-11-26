from django.core.management.base import BaseCommand, CommandError
import random
from datetime import date, timedelta
from clients.models import *
from transactions.models import Transaction
from setup.models import CurrencyStock, Currency
from core.models import DealStatus
from account.models import User
from faker import Faker


class Command(BaseCommand):
    help = 'Create fake transactions'


    def handle(self, *args, **kwargs):
        fake = Faker()
        # get list client ids with beneficiaries
        all_ids = list(Client.objects.exclude(pk=0).exclude(beneficiaries=None).values_list("ClientID", flat=True))

        currencies = [
            {"code": "USD", "rate": 6.78},
            {"code": "EUR", "rate": 7.14},
            {"code": "GBP", "rate": 8.51},
            {"code": "XCD", "rate": 2.76},
            {"code": "JPY", "rate": 0.4386},
        ]

        num_transactions = random.randint(50, 150)
        for i in range(num_transactions):
            # generate random transaction set up
            t_type = random.choice(["P", "S"])
            client_id = random.choice(all_ids)
            foreign_currency = random.choice(currencies)
            if t_type == "P":
                orig_currency = Currency.objects.filter(currency_code=foreign_currency["code"]).first()
                orig_rate = foreign_currency["rate"]
                orig_amount = random.randint(10, 250) * 100
                set_currency = Currency.objects.filter(currency_code="TTD").first()
                set_rate = 1
                set_amount = round(orig_amount * orig_rate, 2)
            else:
                set_currency = Currency.objects.filter(currency_code=foreign_currency["code"]).first()
                set_rate = foreign_currency["rate"]
                set_amount = random.randint(10, 250) * 100
                orig_currency = Currency.objects.filter(currency_code="TTD").first()
                orig_rate = 1
                orig_amount = round(set_amount * set_rate, 2)
            # create transaction object
            t = Transaction(
                client = Client.objects.get(ClientID=client_id),
                contract_date = date.today(),
                value_date = date.today() + timedelta(days=random.randint(1, 3)) if random.random() > 0.7 else date.today(),
                transaction_type = t_type,
                origin_currency = orig_currency,
                origin_currency_rate = orig_rate,
                origin_amount = orig_amount,
                settlement_currency = set_currency,
                settlement_currency_rate = set_rate,
                settlement_amount = set_amount,
                deal_status = DealStatus.objects.get(pk=2),
                trader = User.objects.get(pk=random.choice([2, 3])),
                beneficiary = random.choice(Client.objects.get(ClientID=client_id).beneficiaries.all()),
                payment_details = fake.sentence()
            )
            t.save()
            self.stdout.write(self.style.SUCCESS(f"{i+1}: {t}"))
            # update currecncy stock
            # deduct settlement currency amount from currency stock
            decrease_stock = CurrencyStock(
                source_transaction=t,
                currency=t.settlement_currency,
                currency_rate=t.settlement_currency_rate,
                amount=t.settlement_amount,
                effective_date=t.value_date,
                adjustment_source = "X",
                adjustment_type = -1,
                entered_by=t.trader,
                last_updated_by=t.trader
            )
            decrease_stock.save()
            self.stdout.write(self.style.SUCCESS(f"Decreased stock: {decrease_stock}"))
            # add origin currency amount to currency stock
            increase_stock = CurrencyStock(
                source_transaction=t,
                currency=t.origin_currency,
                currency_rate=t.origin_currency_rate,
                amount=t.origin_amount,
                effective_date=t.value_date,
                adjustment_source = "X",
                adjustment_type = 1,
                entered_by=t.trader,
                last_updated_by=t.trader
            )
            increase_stock.save()
            self.stdout.write(self.style.SUCCESS(f"Increased stock: {increase_stock}"))
