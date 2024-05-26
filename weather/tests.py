from django.test import TestCase
from django.urls import reverse
from .views import GetWeather

class GetWeatherTest(TestCase):
    
    def test_get_weather(self):

        city = 'London'
        url = reverse('get_weather')
        response = self.client.get(url, {'city': city})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['city'], city)
        self.assertIn('tempreature', data)
        self.assertIn('description', data)

    def test_get_weather_for_invalid_city(self):

        city = 'aaaaa'
        url = reverse('get_weather')
        response = self.client.get(url, {'city': city})

        self.assertEqual(response.status_code, 404)

# assert
        


        


