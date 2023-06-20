from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here

class CarModelInline(admin.StackedInline):
    model = CarModel

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'car_type', 'year', 'dealer_id')
    list_filter = ('car_make', 'car_type', 'year')
    search_fields = ('name', 'car_make__name')

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
