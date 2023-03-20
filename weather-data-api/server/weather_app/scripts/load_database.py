import pandas as pd
import datetime
from api.models import Weather
import os


def run():
    df = pd.read_csv("USC00110072.txt", sep="\t", header=1, parse_dates=True)
    df.columns = ["date", "tmin", "tmax", "rain"]
    df["date"] = pd.to_datetime(df.date, format="%Y%m%d")
    df_records = df.to_dict("records")
    model_instances = [
        Weather(
            date=record["date"],
            tmin=record["tmin"],
            tmax=record["tmax"],
            rain=record["rain"],
        )
        for record in df_records
    ]
    Weather.objects.bulk_create(model_instances)
