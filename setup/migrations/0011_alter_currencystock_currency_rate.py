# Generated by Django 5.0.4 on 2024-12-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0010_bankfee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencystock',
            name='currency_rate',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]
