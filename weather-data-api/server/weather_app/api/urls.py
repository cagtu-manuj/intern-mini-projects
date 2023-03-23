from django.urls import path
from . import views

urlpatterns = [
    path("weather", views.WeatherList.as_view()),
    path("weather/stats", views.SummaryList.as_view()),
]
