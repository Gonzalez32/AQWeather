import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.
def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_API_KEY'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        getData = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : getData['main']['temp'],
            'description' : getData['weather'][0]['description'],
            'icon' : getData['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'home.html', context)


# def about(request):
#     return render(request, 'about.html', {})