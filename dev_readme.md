## Setup

No 3rd party libraries needed in Django. However, the system itself uses faker for generating random data, and openpyxl for generating excel downloads, andofcourse, Django:

`pip install django, faker, openpyxl`

Create the database structure and superuser account:

`python manage.py migrate`

`python manage.py createsuperuser`

* the superuser, and all users, sign in with email and password instead of username. 
* When creating a superuser, type 'admin' as the role. The other roles are 'trader' and 'reviewer'

## Load initial data (custom commands)

`python manage.py load_from_csv`

Sets up the initial reference datasets like countries and client types. These populate pulldown menus in forms

`python manage.py create_clients`

This script creates 60 random clients to populate the client base

`python manage.py create_beneficiaries`

This script creates between 1 and 3 random beneficiaries for each client created

## Start the server and create initial currency stock

The following instructions need to occur only once when the system is launched

### 1. Log in and go to admin panel

`python manage.py runserver`

Note: When you first log in to thesystem, you will be prompted to change your password. 

You can go to <http://127.0.0.1:8000/admin/> or click your name in the top right corner of the app and click "Admin Panel" from the menu.

### 2. Create a starting currency stock entry

In the **Currency stocks** table under **SETUP**, create the following entry:
- Source transaction: -
- Adjustment soure: Manual
- Adjustment type: Increase
- Currency: TTD
- Currency rate: 1
- Amount: 1000000000 (one billion)
- Effective date: (current date)
- Comment: "initial deposit" (although this is optional)
- Entered by: (select your user email)
- Last updated by: (same as above)

### 3. Create client 0

The **Clients** table will be populated with random client information starting at ClientID 1. Click "Add Client" and create a client with ClientID 0. This is a special client entry only visible to the admin in the system, and allows the other currency stocks to be initialized. You can give it a client name like "Foreign Exchange Account" or something. Enter something for all the required fields, those don't matter what you put but you have to put something The fields PEP and USPerson should be set to 0.

### 4. Create a beneficiary for client 0

Return to the main website. The TTD on hand should be the amount you initially entered in **Currency stock**. Click the **Clients** link on the sidebar. As admin, you'll find client 0 that you created. To the right, click the icon to add beneficiary. Here you'll create a foreign currency beneficiary. Fill all the necessary fields and save.

### 5. Create foriegn currency deposits

From the **Clients** menu, select Client 0 and click the "New Transaction" icon. A Purchase transactin needs to be made for each foreign currency deposit. Set the Contract Date and Value Date before the current date. This way these deposits will represent the opening balances for today. The Settlment Currency for each transaction is TTD. The exchange rates for the origin currencies on the list relative to TTD are as follows:
- USD: 6.78
- GBP: 8.54
- JPY: 0.044
- EUR: 7.15
- XCD: 2.51

Select the foreign currency as Origin Currency and enter the rate as Origin Currency Rate. The Settlement Amount is then the desrieed amount multiplied by the Origin Currency rate. For example, if you need to deposit 1000000 USD and the exchange rate is 6.78, enter 6780000 as the Settlement amount. The Origin Amount of 1000000 will automatically be entered. Select the Beneficiary that was created. Before saving the transaction, click review. A transaction sheet is generated which can be printed or exported. Click Confirm to save the transaction. The Payment details field is optional, but a comment may be entered. Save and repeat for each foreign currency deposit.

### 6. Confirm that all opening balances

Select **Blotter** from the side menu and ensure that all the initial values are entered and are correct. The TTD on hand value will also decrease accordingly because of the initial purchases

### 7. Create at least 1 trader

As admin, you have access to the Settings menu on the sidebar. Click User Management to add a new User. Give the user a name and email address and set their role to Trader. 

## Daily transactions

The system is designed for data entry of actual fireign exchange transactions. However, for testing purposes we can generate random transactions

`python manage.py create_transactions`

Run this script each day to generate between 50 and 100 random transactions for each client. The transactions are randomly generated using a combination of reference data and random number generation.


## Other utilities

`move_data_to_csv.py`

This script pulls data not randomly generated (reference data for pull down menus) and loads this into appropriate csv files in the start_data folder

`tryfake.py`

This script generates fake data for testing purposes. It gives an example of each of the functions andwhat they generate.