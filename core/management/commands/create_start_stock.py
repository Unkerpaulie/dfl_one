from django.core.management.base import BaseCommand, CommandError
from datetime import date, timedelta
from pathlib import Path
from faker import Faker
import json, random
from clients.models import *
from core.models import Currency, DealStatus
from setup.models import CurrencyStock
from transactions.models import Transaction
from account.models import User


class Command(BaseCommand):
    help = "Creates Client 0 and adds start stock data"

    fake = Faker()
    # get currency data from json file
    directory = "core/start_data"
    currency_file = Path(directory) / "currencies.json"
    with open(currency_file, "r") as f:
        currencies = json.load(f)

    tt_start_amount = 1000000000

    def create_client_0(self):
        Client.objects.create(
            ClientID=0,
            DateOpened=date(2020, 5, 17),
            ClientType=ClientType.objects.get(pk=2),
            ClientSubType=ClientSubType.objects.get(pk=4),
            ClientName="Development Finance Limited",
            ClientStatusID=ClientStatus.objects.get(pk=7),
            ClientAMLRiskRatingID=ClientAMLRiskRating.objects.get(pk=1),
            PEP=0,
            USPerson=0,
            ClientAccountStatus=ClientAccountStatus.objects.get(pk=2),
            ClientAddress1="10 Cipriani Blvd",
            ClientAddressCity="Port of Spain",
            CountryID=Country.objects.get(pk=216),
            ClientPhone="(868) 625-0007",
            ClientEmail="info@dflbusiness.com",
            ClientApprovalStatus="Final Approval"
        )
        self.stdout.write(self.style.SUCCESS("DFL FX Client Account created"))

        # create client beneficiary bank
        BeneficiaryBank.objects.create(
            client=Client.objects.get(pk=0),
            bank_name="DFL FX Account",
            bank_address="10 Cipriani Blvd",
            bank_city="Port of Spain",
            bank_country=Country.objects.get(pk=216),
            account_number="1234567890",
            recipient_name="DFL FX Account",
            recipient_address="10 Cipriani Blvd",
            recipient_city="Port of Spain",
            recipient_country=Country.objects.get(pk=216),
            special_instructions="Trade into FX account"
        )
        self.stdout.write(self.style.SUCCESS("DFL FX Beneficiary Bank created"))

    def set_tt_start(self):
        CurrencyStock.objects.create(
            adjustment_source="M",
            adjustment_type=1,
            currency=Currency.objects.get(pk=1),
            currency_rate=1,
            amount=self.tt_start_amount,
            effective_date=date.today() - timedelta(days=7),
            comment="Initial TT Stock",
            entered_by=User.objects.get(pk=1),
            last_updated_by=User.objects.get(pk=1),
        )
        self.stdout.write(self.style.SUCCESS("Initial TT Stock created"))

    def add_start_stock_transaction(self, currency):
        # create transaction object
        t = Transaction(
            client=Client.objects.get(ClientID=0),
            contract_date=date.today(),
            value_date=date.today() + timedelta(days=random.randint(1, 3)) if random.random() > 0.7 else date.today(),
            transaction_type="P",
            foreign_currency=Currency.objects.filter(currency_code=currency["code"]).first(),
            foreign_currency_rate=currency["rate"],
            foreign_amount=currency["start"],
            settlement_currency=Currency.objects.filter(currency_code="TTD").first(),
            settlement_currency_rate=1,
            settlement_amount=currency["start"] * currency["rate"],
            bank_fee=0,
            deal_status=DealStatus.objects.get(pk=2),
            trader=User.objects.get(pk=1),
            last_updated_by=User.objects.get(pk=1),
            beneficiary=Client.objects.get(ClientID=0).beneficiaries.first(),
            payment_details=f"Initial {currency['code']} Stock of {currency['start']}"
        )
        t.save()
        self.stdout.write(self.style.SUCCESS(f"Initial {currency['code']} Stock of {currency['start']} creates"))
        # update currecncy stock
        # adjust foreign currency stock
        foreign_stock = CurrencyStock(
            source_transaction=t,
            currency=t.foreign_currency,
            currency_rate=t.foreign_currency_rate,
            amount=t.foreign_amount,
            effective_date=t.value_date,
            adjustment_source = "X",
            adjustment_type = 1,
            entered_by=t.trader,
            last_updated_by=t.trader
        )
        foreign_stock.save()
        self.stdout.write(self.style.SUCCESS(f"Purchased: {foreign_stock}"))
        # adjust settlement currency stock
        settle_stock = CurrencyStock(
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
        settle_stock.save()
        self.stdout.write(self.style.SUCCESS(f"Settled for: {settle_stock}"))

    def create_fake_traders(self, n):
        for i in range(n):
            first_name=self.fake.first_name()
            last_name=self.fake.last_name()
            email=f"{first_name[0].lower()}{last_name.lower()}@dflbusiness.com"
            User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                role="trader",
                is_staff=False,
                is_superuser=False,
                is_active=True,
            )

    def handle(self, *args, **kwargs):
        # self.create_client_0()
        # self.set_tt_start()
        # for currency in self.currencies:
        #     self.add_start_stock_transaction(currency)
        # optional create fake traders
        self.create_fake_traders(3)

