from django.core.management.base import BaseCommand, CommandError
import csv
from pathlib import Path
from clients.models import Client


class Command(BaseCommand):
    help = "Loads real client data from core/client_names/Client.csv"
    
    directory = "core/client_names"


    def csv_to_dict_list(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            return [row for row in reader]

    def handle(self, *args, **kwargs):
        f_path = Path(self.directory) / "Client.csv"
        data = self.csv_to_dict_list(f_path)
        # convert any numeric values
        for row in data:
            for k, v in row.items():
                try:
                    row[k] = int(v)
                except ValueError:
                    try:
                        row[k] = float(v)
                    except ValueError:
                        pass

        for record in data:
            Client.create(**record)
        print(f"Added {len(data)} clients")

