from django.urls import path
from . import views

urlpatterns = [
    path("api/weather", views.getWeatherData),
    path("api/weather/stats", views.getWeatherStats),
]
