from django.core.management.base import BaseCommand, CommandError
import random
from pathlib import Path
from clients.models import *
from faker import Faker


class Command(BaseCommand):
    help = "Creates Random beneficiaries for existing clients"

    def handle(self, *args, **kwargs):
        fake = Faker()
        # get list client ids
        all_ids = list(Client.objects.all().values_list("ClientID", flat=True))
        country_ids = list(Country.objects.all().values_list("CountryID", flat=True))
        for i in all_ids:
            client = Client.objects.get(pk=i)
            b_num = random.randint(1, 4)
            for j in range(b_num):
                add_intermediary = random.random() > 0.75
                b = BeneficiaryBank(
                    client=client,
                    bank_name=f"Bank of {fake.company()}" if random.random() > 0.5 else f"{fake.company()} Bank",
                    bank_address=fake.street_address(),
                    bank_address2=fake.secondary_address() if random.random() > 0.7 else "",
                    bank_city=fake.city(),
                    bank_state=fake.state_abbr() if random.random() > 0.7 else "",
                    bank_zip=fake.postalcode() if random.random() > 0.7 else "",
                    bank_country=Country.objects.get(pk=random.choice(country_ids)),
                    account_number=fake.ean(),
                    swift_code=fake.swift() if random.random() > 0.6 else "",
                    iban_code=fake.bban() if random.random() > 0.95 else "",
                    aba_code=fake.aba() if random.random() > 0.9 else "",
                    recipient_name=fake.name(),

                    recipient_address=fake.street_address(),
                    recipient_address2=fake.secondary_address() if random.random() > 0.7 else "",
                    recipient_city=fake.city(),
                    recipient_state=fake.state_abbr() if random.random() > 0.7 else "",
                    recipient_zip=fake.postalcode() if random.random() > 0.7 else "",
                    recipient_country=Country.objects.get(pk=random.choice(country_ids)),

                    intermediary_bank_name=f"Bank of {fake.company()}" if random.random() > 0.5 else f"{fake.company()} Bank" if add_intermediary else "",
                    intermediary_bank_address=fake.street_address() if add_intermediary else "",
                    intermediary_bank_address2=fake.secondary_address() if random.random() > 0.7 else "" if add_intermediary else "",
                    intermediary_bank_city=fake.city() if add_intermediary else "",
                    intermediary_bank_state=fake.state_abbr() if random.random() > 0.7 else "" if add_intermediary else "",
                    intermediary_bank_zip=fake.postalcode() if random.random() > 0.7 else "" if add_intermediary else "",
                    intermediary_bank_country=Country.objects.get(pk=random.choice(country_ids)) if add_intermediary else None,
                    intermediary_account_number=fake.ean() if add_intermediary else "",
                    intermediary_swift_code=fake.swift() if random.random() > 0.6 else "" if add_intermediary else "",
                    intermediary_iban_code=fake.bban() if random.random() > 0.95 else "" if add_intermediary else "",
                    intermediary_aba_code=fake.aba() if random.random() > 0.9 else "" if add_intermediary else "",
                    special_instructions=fake.sentence() if random.random() > 0.5 else ""
                )
                b.save()
            print(f"Created {b_num} beneficiaries for {client}")
