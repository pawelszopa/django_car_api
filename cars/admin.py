from django.contrib import admin


from cars.models import Company, Car, Rate

admin.site.register(Company)
admin.site.register(Car)
admin.site.register(Rate)
