import pandas as pd
import datetime
from api.models import Weather, Summary
from django.db.models.functions import TruncYear
from django.db.models import Avg, Sum
import os
import time


def run():
    total_records = 0
    total_tables = 0
    start_time = time.time()
    for filename in os.listdir(os.path.join(os.getcwd(), "wx_data")):
        total_tables += 1
        with open(os.path.join(os.getcwd(), "wx_data", filename), "r") as file:
            station = str(file.name.split("/")[-1].split(".")[0])
            df = pd.read_csv("USC00110072.txt", sep="\t", header=1, parse_dates=True)
            df.columns = ["date", "tmin", "tmax", "rain"]
            df["date"] = pd.to_datetime(df.date, format="%Y%m%d")
            df_records = df.to_dict("records")
            model_instances = [
                Weather(
                    station=station,
                    date=record["date"],
                    tmin=record["tmin"],
                    tmax=record["tmax"],
                    rain=record["rain"],
                )
                for record in df_records
            ]
            objs = Weather.objects.bulk_create(model_instances, ignore_conflicts=True)
            total_records += len(objs)

    queryset = (
        Weather.objects.exclude(tmin=-9999, tmax=-9999, rain=-9999)
        .annotate(year=TruncYear("date"))
        .values("station", "year")
        .annotate(avgMin=Avg("tmin"), avgMax=Avg("tmax"), totalRain=Sum("rain"))
    ).values()
    model_instances = [
        Summary(
            station=record["station"],
            year=record["year"],
            avg_tmin=record["avgMin"],
            avg_tmax=record["avgMax"],
            total_rain=record["totalRain"],
        )
        for record in queryset
    ]
    objs = Summary.objects.bulk_create(model_instances, ignore_conflicts=True)

    end_time = time.time()
    print(f"Total tables added: {total_tables}")
    print(f"Total rows added: {total_records}")
    print(f"Total time: {end_time - start_time}")
