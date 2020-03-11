import requests
from django.shortcuts import render


from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/dformata/2.5/weather?q={}&units=imperial&appid=91f8d63600a67a6100acbb2b27bf632d'
    msg = ''
    msg_class = 'is-danger'

    form = CityForm(request.POST)
    if request.method ==  'POST':

        #print(request.POST)
        
        
        if form.is_valid() and City.objects.filter(name= form.cleaned_data['name']).count() == 0:
            new_city = form.cleaned_data['name'] # .cleaned_data['name']


            print(requests.get(url.format(new_city)))

            re = requests.get(url.format(new_city)).json()
            if re['cod' =='404']:      
                msg = 'City not found!'
            form.save()
            msg = 'City is added'
            msg_class = 'is-success'
        else:
            msg = 'City alredy exists in database'

    form = CityForm()


    cities = City.objects.all()

    #print(cities)
    wearther_list = []
    for city in cities:
        print(city)
        
        #print(re)
        # if re['cod'] == '404':
        #     continue
        try:
            re = requests.get(url.format(city)).json()
            city_weather = {
                'city': city.name,
                'temperature' :re['main']['temp'],
                'description' : re['weather'][0]['description'],
                'icon' : re['weather'][0]['icon']
            }
            wearther_list.append(city_weather)

        except :
            pass
       
    
    print(wearther_list)
    context = {'weather_list' : wearther_list, 
                'form' : form,
                'msg' : msg,
                'msg_class' : msg_class
                }
                
                
                


    return render(request, 'weather.html',  context)


# Create your views here.
