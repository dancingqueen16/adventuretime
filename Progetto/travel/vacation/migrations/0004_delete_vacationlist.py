# Generated by Django 5.1 on 2024-08-23 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacation', '0003_alter_vacation_duration_alter_vacation_price_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VacationList',
        ),
    ]
