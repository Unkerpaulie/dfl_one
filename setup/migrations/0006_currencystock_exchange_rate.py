# Generated by Django 5.0.4 on 2024-11-20 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0005_currencystock_last_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencystock',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=16),
            preserve_default=False,
        ),
    ]
