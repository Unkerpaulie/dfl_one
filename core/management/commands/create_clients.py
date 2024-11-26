from django.core.management.base import BaseCommand, CommandError
import random
from datetime import date, timedelta
from clients.models import *
from faker import Faker


class Command(BaseCommand):
    help = 'Create fake transactions'

    def create_new_client(self, id):
        fake = Faker()

        # create individual clients 75% of the time
        if random.random() < 0.75:
            # individual client
            client_name = fake.name()
            client_tyoe = ClientType.objects.get(pk=1)
            client_subtype = ClientSubType.objects.get(pk=random.randint(1, 3))
        else:
            # corporate client
            client_name = fake.company()
            client_tyoe = ClientType.objects.get(pk=2)
            client_subtype = ClientSubType.objects.get(pk=random.randint(4, 7))

        Client.objects.create(
            ClientID=id+1,
            DateOpened=fake.date_between(start_date='-15y', end_date='-5y'),
            ClientType=client_tyoe,
            ClientSubType=client_subtype,
            ClientName=client_name,
            ClientStatusID=ClientStatus.objects.get(pk=random.randint(1, 8)),
            ClientAMLRiskRatingID=ClientAMLRiskRating.objects.get(pk=random.randint(1, 4)),
            PEP=0,
            USPerson=0,
            ClientAccountStatus=ClientAccountStatus.objects.get(pk=random.randint(1, 8)),
            ClientAddress1=fake.street_address(),
            ClientAddress2=fake.secondary_address() if random.random() > 0.8 else "",
            ClientAddressCity=fake.city(),
            ClientAddressState=fake.state_abbr() if random.random() > 0.8 else "",
            ClientAddressZipCode=fake.postalcode() if random.random() > 0.8 else "",
            CountryID=Country.objects.get(pk=216) if random.random() > 0.1 else Country.objects.get(pk=random.randint(1, 239)),
            ClientPhone="",
            ClientFax="",
            ClientEmail="",
            ClientWebsite="",
            ClientApprovalStatus="Final Approval"
        )
        self.stdout.write(self.style.SUCCESS(f"New Client: {client_name} (id: {id+1}) created"))


    def handle(self, *args, **kwargs):
        for i in range(60):
            self.create_new_client(i)