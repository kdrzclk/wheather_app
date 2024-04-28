from django.urls import path
from .views import get_weather, GetWeather

urlpatterns = [
     path('weather/', get_weather),
     path('weatherclass/', GetWeather.as_view()),
    
]