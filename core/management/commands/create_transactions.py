from django.core.management.base import BaseCommand, CommandError
import random, json
from pathlib import Path
from datetime import date, timedelta
from faker import Faker
from clients.models import *
from transactions.models import Transaction, CurrencyStock 
from setup.models import BankFee, DFLLocalBank, DFLInternationalBank
from core.models import Currency, DealStatus
from account.models import User


class Command(BaseCommand):
    help = 'Create fake transactions'

    # get currency data from json file
    directory = "core/start_data"
    currency_file = Path(directory) / "currencies.json"
    with open(currency_file, "r") as f:
        currencies = json.load(f)

    def handle(self, *args, **kwargs):
        fake = Faker()
        # get list clients with beneficiaries
        all_clients = list(ClientList.objects.exclude(pk=0).exclude(beneficiaries=None).all())

        num_transactions = random.randint(30, 60)
        for i in range(num_transactions):
            # generate random transaction set up
            t_type = random.choice(["P", "S"])
            client = random.choice(all_clients)
            foreign_currency = random.choice(self.currencies)
            trader = random.choice(User.objects.filter(role="trader"))
            amount = random.randint(10, 250) * 100

            # create transaction object
            t = Transaction(
                client=client,
                contract_date=date.today(),
                value_date=date.today() + timedelta(days=random.randint(1, 3)) if random.random() > 0.7 else date.today(),
                transaction_type=t_type,
                foreign_currency=Currency.objects.filter(currency_code=foreign_currency["code"]).first(),
                foreign_currency_rate=foreign_currency["rate"],
                foreign_amount=amount,
                settlement_currency=Currency.objects.filter(currency_code="TTD").first(),
                settlement_currency_rate=1,
                settlement_amount=foreign_currency["rate"] * amount,
                bank_fee=BankFee.objects.get(pk=1).bank_fee,
                deal_status=DealStatus.objects.get(pk=2),
                in_payment_type=(ip := random.choice(["cash", "check", "foreign"])),
                check_number=fake.random_number(digits=10) if ip == "check" else None,
                client_beneficiary_account=random.choice(client.beneficiaries.all()) if ip == "foreign" else None,
                client_local_bank_account=None,                
                payment_details=fake.sentence(),                
                trader=trader,
                last_updated_by=trader
            )
            t.save()
            self.stdout.write(self.style.SUCCESS(f"{i+1}: {t}"))
            # update currecncy stock
            # adjust foreign currency stock
            foreign_stock = CurrencyStock(
                source_transaction=t,
                currency=t.foreign_currency,
                currency_rate=t.foreign_currency_rate,
                amount=t.foreign_amount,
                effective_date=t.value_date,
                adjustment_source = "F",
                adjustment_type = 1 if t_type == "P" else -1,
                entered_by=t.trader,
                last_updated_by=t.trader
            )
            foreign_stock.save()
            self.stdout.write(self.style.SUCCESS(f"{'Purchased' if t_type == 'P' else 'Sold'}: {foreign_stock}"))
            # adjust settlement currency stock
            settle_stock = CurrencyStock(
                source_transaction=t,
                currency=t.settlement_currency,
                currency_rate=t.settlement_currency_rate,
                amount=t.settlement_amount,
                effective_date=t.value_date,
                adjustment_source = "F",
                adjustment_type = -1 if t_type == "P" else 1,
                entered_by=t.trader,
                last_updated_by=t.trader
            )
            settle_stock.save()
            self.stdout.write(self.style.SUCCESS(f"Settled for: {settle_stock}"))
