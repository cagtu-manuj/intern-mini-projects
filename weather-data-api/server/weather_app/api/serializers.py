from rest_framework import serializers
from .models import Weather, Summary


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = "__all__"
