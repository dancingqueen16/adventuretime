from django.contrib.auth.models import User
from django.db import models


class Vacation(models.Model):
    SEASON_CHOICES = [
        ('INV', 'Inverno'),
        ('PRI', 'Primavera'),
        ('EST', 'Estate'),
        ('AUT', 'Autunno'),
    ]

    TYPE_CHOICES = [
        ('BEACH', 'Beach'),
        ('MOUNTAIN', 'Mountain'),
        ('CITY', 'City'),
        ('CRUISE', 'Cruise'),
        ('ADVENTURE', 'Adventure'),
    ]

    DURATION_CHOICES = [
        ('<SETT', 'Meno di una settimana'),
        ('12SETT', '1/2 Settimane'),
        ('3SETT', '3 Settimane'),
        ('>3SETT', 'Più di 3 settimane')
    ]

    PRICE_CHOICES = [
        ('€', 'Economica'),
        ('€€', 'Costosa'),
        ('€€€', 'Lusso'),
    ]

    title = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    duration = models.CharField(max_length=10,choices=DURATION_CHOICES)
    price = models.CharField(max_length=3, choices=PRICE_CHOICES)
    type = models.CharField(max_length=20,choices=TYPE_CHOICES)
    likes = models.IntegerField(default=0)
    season = models.CharField(max_length=10,choices=SEASON_CHOICES)

    def __str__(self):
        return self.title


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list')
    name = models.CharField(max_length=100)
    vacations = models.ManyToManyField("Vacation", related_name='in_list')

    def __str__(self):
        return f"{self.name}"


class VacationList(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('DONE', 'Done'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacation = models.ManyToManyField("Vacation", related_name='list')
    status = models.CharField(max_length=4, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.status} - {self.user.username}" "list"
