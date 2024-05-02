from django.urls import path
from .views import GetWeather

urlpatterns = [
     # path('weather/', get_weather),
     path('weatherclass/', GetWeather.as_view()),
    
]