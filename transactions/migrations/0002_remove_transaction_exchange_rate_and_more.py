# Generated by Django 5.0.4 on 2024-11-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='exchange_rate',
        ),
        migrations.AddField(
            model_name='transaction',
            name='origin_currency_rate',
            field=models.DecimalField(decimal_places=10, default=1, max_digits=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='settlement_currency_rate',
            field=models.DecimalField(decimal_places=10, default=1, max_digits=16),
            preserve_default=False,
        ),
    ]
