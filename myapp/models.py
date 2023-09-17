from django.db import models

# Create your models here.


class userdate(models.Model):
    names = models.CharField(max_length=24)
    date = models.CharField(max_length=24)