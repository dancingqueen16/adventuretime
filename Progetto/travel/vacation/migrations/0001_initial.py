# Generated by Django 5.1 on 2024-08-25 16:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=200)),
                ('luogo', models.CharField(max_length=200)),
                ('continente', models.CharField(choices=[('EUROPA', 'Europa'), ('NORDAMERICA', 'America del Nord'), ('SUDAMERICA', 'America del Sud'), ('AFRICA', 'Africa'), ('ASIA', 'Asia'), ('OCEANIA', 'Oceania'), ('ANTARTIDE', 'Antartide')], max_length=50)),
                ('durata', models.CharField(choices=[('WEEKEENDLUNGO', 'Weekend Lungo (2-4 Giorni)'), ('1SETTIMANA', '1 Settimana'), ('2SETTIMANE', '2 Settimane'), ('3SETTIMANE+', '3 settimane o più')], max_length=50)),
                ('prezzo', models.CharField(choices=[('LOWCOST', 'Viaggio Low Cost'), ('MEDIO', 'Budget Medio'), ('LUSSO', 'Viaggio di Lusso')], max_length=20)),
                ('tipologia', models.CharField(choices=[('CULTURA', 'Culturale'), ('RELAX', 'Relax'), ('ENOGASTRONOMICO', 'Enogastronomico'), ('ONTHEROAD', 'On The Road'), ('AVVENTURA', 'Avventura')], max_length=50)),
                ('periodo', models.CharField(choices=[('INV', 'Inverno'), ('PRI', 'Primavera'), ('EST', 'Estate'), ('AUT', 'Autunno')], max_length=20)),
                ('descrizione', models.TextField()),
                ('like', models.ManyToManyField(blank=True, null=True, related_name='like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list', to=settings.AUTH_USER_MODEL)),
                ('vacations', models.ManyToManyField(related_name='in_list', to='vacation.vacation')),
            ],
        ),
    ]
