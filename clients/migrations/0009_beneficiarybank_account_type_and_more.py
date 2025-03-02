# Generated by Django 5.1.4 on 2025-03-01 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_clientlocalbank_client'),
        ('core', '0002_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiarybank',
            name='account_type',
            field=models.CharField(choices=[('CH', 'Checking'), ('SV', 'Savings'), ('MM', 'Money Marke Account'), ('CD', 'Certificate of Deposit')], default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beneficiarybank',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to='core.currency'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='corporateclient',
            name='entity_type',
            field=models.CharField(choices=[('L', 'Limited Liability'), ('P', 'Partnership'), ('T', 'Trust'), ('S', 'Sole Trader'), ('G', 'Government Enterprise')], max_length=1),
        ),
    ]
