from django.db import models


class Vacation(models.Model):
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    season = models.CharField(max_length=200)
