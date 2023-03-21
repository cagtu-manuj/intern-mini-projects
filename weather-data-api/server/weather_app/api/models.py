from django.db import models
from django.db.models.constraints import UniqueConstraint


# datetime.date(1997, 10, 19
class Weather(models.Model):
    station = models.CharField(max_length=15)
    date = models.DateField(null=False)
    tmin = models.IntegerField()
    tmax = models.IntegerField()
    rain = models.IntegerField()

    class Meta:
        unique_together = ("date", "station")


class Summary(models.Model):
    station = models.CharField(max_length=15)
    year = models.DateField(null=False)
    avg_tmin = models.FloatField(max_length=10)
    avg_tmax = models.FloatField(max_length=10)
    total_rain = models.IntegerField()

    class Meta:
        unique_together = ("year", "station")
