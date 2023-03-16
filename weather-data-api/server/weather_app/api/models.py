from django.db import models


class Weather(models.Model):
    data = models.DateField(unique=True, null=False)
    tmin = models.IntegerField()
    tmax = models.IntegerField()
    rain = models.IntegerField()


class Summary(models.Model):
    avg_tmin = models.FloatField(max_length=10)
    avg_tmax = models.FloatField(max_length=10)
    total_rain = models.IntegerField()
