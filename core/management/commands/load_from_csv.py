from django.core.management.base import BaseCommand, CommandError
import csv
from pathlib import Path
import importlib
from clients.models import *
from core.models import *


class Command(BaseCommand):
    help = "Loads initial client setup data from csv files in start_data folder"
    
    directory = "core/start_data"
    # data models
    data_models = [
        {
            "app": "clients",
            "models": [
                "ClientType",
                "ClientSubType",
                "ClientStatus",
                "ClientAMLRiskRating",
                "ClientAccountStatus",
                "Country",
            ]
        },
        {
            "app": "core",
            "models": [
                "Currency",
                "DealStatus",
            ]
        }
    ]

    def get_app_model(self, app, model_name):
        # app = filename.split("_")[0]
        # model_name = filename.split("_")[1].split(".")[0]
        # for dm in self.data_models:
        #     if dm['app'] == app:
        #         for mdl in dm["models"]:
        #             if mdl.lower() == model_name:
        try:
            module_path = f"{app}.models"
            models_module = importlib.import_module(module_path)
            # Get the model class
            model_class = getattr(models_module, model_name, None)
            
            if model_class is None:
                raise AttributeError(f"Model '{model_name}' not found in '{module_path}'.")
            
            return model_class
        
        except ImportError as e:
            print(f"Error importing module '{module_path}': {e}")
        except AttributeError as e:
            print(f"Error retrieving model '{model_name}' from '{module_path}': {e}")
        return None

    def csv_to_dict_list(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            return [row for row in reader]

    def handle(self, *args, **kwargs):
        file_list = [file.name for file in Path(self.directory).iterdir() if file.suffix == '.csv']
        for data_model in self.data_models:
            for m in data_model["models"]:
                f = f"{data_model['app']}_{m.lower()}.csv"
        # for f in file_list:
                f_path =  Path(self.directory) / f
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

                app_class = self.get_app_model(data_model['app'], m)

            
                if not app_class:
                    print(f"Skipping {f} as it is not a valid data model")
                else:
                    print(f"Loading {f}....  ", end="")

                    for record in data:
                        app_class.objects.create(**record)
                    print(f"completed {len(data)} records")

