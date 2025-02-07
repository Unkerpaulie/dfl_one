## Setup

No 3rd party libraries needed in Django. However, the system itself uses faker for generating random data, and openpyxl for generating excel downloads, andofcourse, Django:

`pip install django, faker`

Create the database structure and superuser account:

`python manage.py migrate`

`python manage.py createsuperuser`

* the superuser, and all users, sign in with email and password instead of username. 
* standard superuser email is 'admin@dflbusiness.com'
* When creating a superuser, type 'admin' as the role. The other roles are 'trader' and 'reviewer'

## Load initial data (custom commands)

`python manage.py load_system`

Sets up the initial reference datasets like countries and client types. These populate pulldown menus in forms

`python manage.py create_fake_clients`

This script creates 25 random clients to populate the client base

Generate fake beneficiaries for each client. This script creates between 1 and 4 random beneficiaries for each client created:

`python manage.py create_beneficiaries`

Alternatively, real clients can be added to the system by entering real clients and their beneficiaries using the data entry forms on the application


## Create initial currency stock

`python manage.py create_start_stock`

This script does the following:
* create DFL as client 0
* create the initial TT pool total
* create initial starting amounts for each currency
* set the starting deal number
* create 3 fake traders

The following instructions need to occur only once when the system is launched. This will be modified once real data is going to be used

## Run the server

`python manage.py runserver`

## Create fake transactions daily

`python manage.py create_transactions`

## Other utilities

`move_data_to_csv.py`

This script pulls data not randomly generated (reference data for pull down menus) and loads this into appropriate csv files in the start_data folder

`tryfake.py`

This script generates fake data for testing purposes. It gives an example of each of the functions andwhat they generate.