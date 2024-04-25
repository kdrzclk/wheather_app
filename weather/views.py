from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decouple import config
import requests
from pprint import pprint


@api_view(['GET'])
def get_weather(request):

    API_key = config('API_KEY')
    city = request.GET.get('city')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
    response = requests.get(url)
    informations = response.json()

    pprint(informations)

    if response.status_code == 200:
        return Response({
            'City' : informations['name'],
            'Tempreature' : int(informations['main']['temp']),
            'Description' : informations['weather'][0]['description']
        }, status = status.HTTP_200_OK)
    
    else:
        return Response({
            'Something is Wrong'
        })