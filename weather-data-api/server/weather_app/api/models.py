from django.db import models


# datetime.date(1997, 10, 19
class Weather(models.Model):
    station = models.CharField(max_length=15)
    date = models.DateField(null=False)
    tmin = models.IntegerField()
    tmax = models.IntegerField()
    rain = models.IntegerField()

    class Meta:
        ["station", "date"]


class Summary(models.Model):
    avg_tmin = models.FloatField(max_length=10)
    avg_tmax = models.FloatField(max_length=10)
    total_rain = models.IntegerField()
