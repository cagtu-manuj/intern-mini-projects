from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def getWeatherData(request):
    person = {"name": "Dennis", "age": 28}
    return Response(person)


@api_view(["GET"])
def getWeatherStats(request):
    person = {"name": "Dennis", "age": 28}
    return Response(person)
