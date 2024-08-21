from django.contrib.auth.models import User
from django.db import models


class Vacation(models.Model):
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    season = models.CharField(max_length=200)


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.name} - {self.user.username}"


class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    item = models.ForeignKey(Vacation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.title} in {self.list.name} - {self.list.user.username}"