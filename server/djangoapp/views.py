from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import requests


#Render

def static_page(request):
    return render(request, 'static_page.html')


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Autenticación exitosa, iniciar sesión
            login(request, user)
            # Redirigir al usuario a una página de éxito o a la página deseada
            return redirect('/djangoapp')
        else:
            # Autenticación fallida, mostrar mensaje de error
            messages.error(request, 'Invalid username or password.')
            return redirect('/djangoapp')
    else:
        # Renderizar la página de inicio de sesión
        return render(request, 'djangoapp/index.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    # Redirigir al usuario a una página de éxito o a la página deseada después del cierre de sesión
    return redirect('/djangoapp')

# Create a `` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        last_name= request.POST.get('last_name')
        first_name= request.POST.get('first_name')
        
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return redirect('/djangoapp')
    else:
        return render(request, 'djangoapp/registration.html')



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/be79a8fa-64da-4b4c-8d3d-1983448e2c90/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships if dealer.short_name is not None])
        context['dealerships'] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/be79a8fa-64da-4b4c-8d3d-1983448e2c90/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/be79a8fa-64da-4b4c-8d3d-1983448e2c90/default/Get%20all%20reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, id):
    context = {}
    dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/be79a8fa-64da-4b4c-8d3d-1983448e2c90/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer

    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            car_id = request.POST.get("car")
            car = CarModel.objects.get(pk=car_id)

            payload = {
                "time": datetime.utcnow().isoformat(),
                "name": username,
                "dealership": id,
                "id": id,
                "review": request.POST.get("content"),
                "purchase": "purchasecheck" in request.POST,
                "purchase_date": request.POST.get("purchasedate"),
                "car_model": car.name,
                "car_make": str(car.car_make),
                "car_year": car.year.year
            }

            review_post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/be79a8fa-64da-4b4c-8d3d-1983448e2c90/default/POST"

            response = requests.post(review_post_url, json={"review": payload})

            if response.status_code == 200:
                # La solicitud se envió correctamente
                return redirect("djangoapp:dealer_details", id=id)
            else:
                # La solicitud no se pudo enviar correctamente, manejar el error apropiadamente
                # ...
                pass
        else:
            # El usuario no está autenticado, manejar el escenario de error apropiadamente
            # ...
            pass

    return redirect("djangoapp:dealer_details", id=id)

