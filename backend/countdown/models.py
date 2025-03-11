from django.db import models

class Countdown(models.Model):
    target_time = models.BigIntegerField()  # Store Unix timestamp as a big integer

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)

class Session(models.Model):
    session_name = models.CharField(max_length=150, unique=True)
    users = models.ManyToManyField(User)
