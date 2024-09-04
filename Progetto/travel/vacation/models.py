from django.contrib.auth.models import User
from django.db import models


# Modello per le vacanze
class Vacation(models.Model):
    SEASON_CHOICES = [
        ('Inverno', 'Inverno'),
        ('Primavera', 'Primavera'),
        ('Estate', 'Estate'),
        ('Autunno', 'Autunno'),
    ]

    TYPE_CHOICES = [
        ('Culturale', 'Culturale'),
        ('Relax', 'Relax'),
        ('Enogastronomico', 'Enogastronomico'),
        ('On The Road', 'On The Road'),
        ('Avventura', 'Avventura'),
    ]

    DURATION_CHOICES = [
        ('Weekend Lungo (2-4 Giorni)', 'Weekend Lungo (2-4 Giorni)'),
        ('1 Settimana', '1 Settimana'),
        ('2 Settimane', '2 Settimane'),
        ('3 settimane o più', '3 settimane o più')
    ]

    PRICE_CHOICES = [
        ('Viaggio Low Cost', 'Viaggio Low Cost'),
        ('Budget Medio', 'Budget Medio'),
        ('Viaggio di Lusso', 'Viaggio di Lusso'),
    ]

    CONTINENT_CHOICES = [
        ('Europa', 'Europa'),
        ('America del Nord', 'America del Nord'),
        ('America del Sud', 'America del Sud'),
        ('Africa', 'Africa'),
        ('Asia', 'Asia'),
        ('Oceania', 'Oceania'),
        ('Antartide', 'Antartide')
    ]

    titolo = models.CharField(max_length=200)
    luogo = models.CharField(max_length=200)
    continente = models.CharField(max_length=50, choices=CONTINENT_CHOICES)
    durata = models.CharField(max_length=50, choices=DURATION_CHOICES)
    prezzo = models.CharField(max_length=20, choices=PRICE_CHOICES)
    tipologia = models.CharField(max_length=50, choices=TYPE_CHOICES)
    periodo = models.CharField(max_length=20, choices=SEASON_CHOICES)
    descrizione = models.TextField()
    like = models.ManyToManyField(User, blank=True, related_name='like')

    def like_count(self):
        return self.like.count()

    def __str__(self):
        return self.titolo


# Modello per le liste
class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list')
    name = models.CharField(max_length=100)
    vacations = models.ManyToManyField("Vacation", related_name='in_list')

    def __str__(self):
        return f"{self.name}"


# Modello per il profilo utente
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')

    def __str__(self):
        return self.user.username
