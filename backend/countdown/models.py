from django.db import models

class Countdown(models.Model):
    target_time = models.BigIntegerField()  # Store Unix timestamp as a big integer
