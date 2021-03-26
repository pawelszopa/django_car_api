from django.contrib import admin

# Register your models here.
from cars.models import Company, Car

admin.site.register(Company)
admin.site.register(Car)