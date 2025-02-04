from django.core.management.base import BaseCommand, CommandError
import random
from datetime import date, timedelta
from clients.models import *
from core.models import Country
from faker import Faker


class Command(BaseCommand):
    help = 'Create fake clients'

    def create_client_list_entry(self, client_name, client_type, legacy_id):
        client_list = ClientList(
            client_name=client_name,
            client_type=client_type,
            legacy_id=legacy_id
        )
        client_list.save()
        return client_list

    def create_new_client(self, id):
        # create variables
        fake = Faker()
        genders = ["M", "F"]
        mar_statuses = [s[0] for s in IndividualClient.mar_statuses]
        emp_statuses = [s[0] for s in IndividualClient.emp_statuses]
        trans_freq = [s[0] for s in IndividualClient.trans_freq]
        countries = Country.objects.all()
        tt = Country.objects.get(country_code="TT")
        id_types = IdentificationType.objects.all()

        # create individual clients 75% of the time
        if random.random() < 0.75:
            # individual client
            iclient = IndividualClient(
                first_name=fake.first_name(),
                middle_name=fake.first_name() if random.random() < 0.25 else '',
                surname=fake.last_name(),
                date_of_birth=fake.date_of_birth(),
                gender=random.choice(genders),
                marital_status=random.choice(mar_statuses),
                residential_address=fake.street_address(),
                residential_address2=fake.secondary_address() if random.random() > 0.8 else "",
                residential_city=fake.city(),
                residential_country=tt if random.random() > 0.1 else random.choice(countries),
                mailing_address=fake.street_address(),
                mailing_address2=fake.secondary_address() if random.random() > 0.8 else "",
                mailing_city=fake.city(),
                mailing_country=tt if random.random() > 0.1 else random.choice(countries),
                country_of_birth=tt if random.random() > 0.1 else random.choice(countries),
                nationality=tt if random.random() > 0.1 else random.choice(countries),
                dual_citizen=False,
                dual_nationality=None,
                primary_phone=fake.basic_phone_number(),
                secondary_phone=fake.basic_phone_number() if random.random() < 0.1 else None,
                email=fake.email(),
                telephone_preferred=random.choice([True, False]),
                email_preferred=random.choice([True, False]),
                primary_income_source=fake.catch_phrase(),
                employment_status=random.choice(emp_statuses),
                position_held=fake.job(),
                employer=fake.company(),
                employer_address=fake.address(),
                business_type=fake.word(),
                transaction_frequency=random.choice(trans_freq),
                politically_exposed=random.choice([True, False]),
                political_details=fake.sentence()if random.random() < 0.5 else None
            )
            # create client list entry
            client_name = f"{iclient.first_name} {iclient.surname}"
            iclient.client_list_entry = self.create_client_list_entry(client_name, "I", None)
            iclient.save()

            # create some identification
            for i in range(random.randint(1, 2)):
                id_info = IdentificationInfo(
                    client=iclient,
                    id_type=random.choice(id_types),
                    id_number=fake.ean8(),
                    id_country=tt if random.random() > 0.1 else random.choice(countries),
                    issue_date=fake.date(),
                    expiry_date=fake.date(),
                )
                id_info.save()
        else:
            # corporate client
            cclient = CorporateClient(
                registered_name=fake.company(),
                date_of_incorporation=fake.date(),
                country_of_incorporation=tt if random.random() > 0.1 else random.choice(countries),
                registration_number=fake.ean8(),
                bir_number=fake.ean13(),
                vat_registration=fake.ean8(),
                parent_company=fake.company(),
                registered_address=fake.street_address(),
                registered_address2=fake.secondary_address() if random.random() > 0.8 else "",
                registered_city=fake.city(),
                registered_country=tt if random.random() > 0.1 else random.choice(countries),
                mailing_address=fake.street_address(),
                mailing_address2=fake.secondary_address() if random.random() > 0.8 else "",
                mailing_city=fake.city(),
                mailing_country=tt if random.random() > 0.1 else random.choice(countries),
                contact_person=fake.name(),
                primary_phone=fake.basic_phone_number(),
                secondary_phone=fake.basic_phone_number() if random.random() < 0.1 else None,
                email=fake.email(),
                website=fake.url(),
                telephone_preferred=random.choice([True, False]),
                email_preferred=random.choice([True, False]),
                entity_type=fake.word(),
                business_type=fake.word(),
                transaction_frequency=random.choice(trans_freq),
                politically_exposed=random.choice([True, False]),
                political_details=fake.sentence()if random.random() < 0.5 else None
            )
            # create client list entry
            client_name = cclient.registered_name
            cclient.client_list_entry = self.create_client_list_entry(client_name, "C", None)
            cclient.save()
        
        self.stdout.write(self.style.SUCCESS(f"New Client: {client_name} (id: {id+1}) created"))


    def handle(self, *args, **kwargs):
        for i in range(25):
            self.create_new_client(i)