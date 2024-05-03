from django.urls import path
from .views import GetWeather

urlpatterns = [
     # path('weather/', get_weather),
     path('weather/', GetWeather.as_view()),
    
]