from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json


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
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

