import datetime
from django.db import models
from users.models import User
from developer.models import Developer

class Game(models.Model):
    creator = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(default="", max_length=200, null=True, blank=True)
    publication_date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
