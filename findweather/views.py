import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

# Create your views here.
def home(request):
    # url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_API_KEY'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f7559e8dce1a0f28232101edcca98a0a'


    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        # form.save()

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                getData = requests.get(url.format(new_city)).json()

                if getData['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Sorry city does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'
    
    if err_msg:
        message = err_msg
        message_class = 'is-danger'
    else:
        message = 'City added successfully!'
        message_class = 'is-success'

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

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }

    return render(request, 'home.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')


# def about(request):
#     return render(request, 'about.html', {})