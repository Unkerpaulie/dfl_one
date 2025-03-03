# Generated by Django 5.1.4 on 2025-03-03 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0016_remove_dflinternationalbank_intermediary_account_number'),
        ('transactions', '0009_transaction_check_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='beneficiary',
            new_name='client_beneficiary_account',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='local_bank_account',
            new_name='client_local_bank_account',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='dfl_bank_account',
            new_name='dfl_local_bank_account',
        ),
        migrations.AddField(
            model_name='transaction',
            name='dfl_intl_bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setup.dflinternationalbank'),
        ),
    ]
