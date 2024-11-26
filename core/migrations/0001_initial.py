# Generated by Django 5.0.4 on 2024-11-16 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=140)),
                ('currency_code', models.CharField(max_length=5)),
                ('symbol', models.CharField(blank=True, default='$', max_length=1)),
            ],
            options={
                'verbose_name_plural': 'currencies',
            },
        ),
        migrations.CreateModel(
            name='DealStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=140)),
            ],
            options={
                'verbose_name_plural': 'deal statuses',
            },
        ),
        migrations.CreateModel(
            name='IdentificationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_type', models.CharField(max_length=40)),
            ],
        ),
    ]
