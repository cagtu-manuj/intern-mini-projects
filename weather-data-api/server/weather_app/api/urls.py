from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("/weather", views.WeatherList.as_view()),
    path("/weather/stats", views.SummaryList.as_view()),
]
