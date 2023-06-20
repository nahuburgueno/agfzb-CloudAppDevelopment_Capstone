from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    CAR_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('wagon', 'WAGON'),   
    ]
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    year = models.DateField()
    
    def __str__(self):
        return self.name



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, 
                 dealership, 
                 name, 
                 purchase, 
                 review):
        # Dealership
        self.dealership = dealership
        # Name
        self.name = name
        # Purchase
        self.purchase = purchase
        # Review
        self.review = review
        # Purchase Date
        self.purchase_date = '99/99/9999'
        # Car Make
        self.car_make = 'N/A'
        # Car Model
        self.car_model = 'N/A'
        # Car Year
        self.car_year = 9999
        # Sentiment
        self.sentiment = ''
        # ID
        self.id = 0      
    def __str__(self):
        return "Review: " + self.review 