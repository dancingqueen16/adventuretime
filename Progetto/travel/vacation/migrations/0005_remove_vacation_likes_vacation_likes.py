# Generated by Django 5.1 on 2024-08-23 14:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacation', '0004_delete_vacationlist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacation',
            name='likes',
        ),
        migrations.AddField(
            model_name='vacation',
            name='likes',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
