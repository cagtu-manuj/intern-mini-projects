from rest_framework import generics
from .models import Weather, Summary
from .serializers import WeatherSerializer, SummarySerializer


class WeatherList(generics.ListCreateAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer


class SummaryList(generics.ListCreateAPIView):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
