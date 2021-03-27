from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.
class Company(models.Model):
    make = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.make}'


class Car(models.Model):
    model = models.CharField(max_length=255, unique=True)
    make = models.ForeignKey('Company', on_delete=models.CASCADE)
    avg_rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    rates_number = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return f'Company: {self.make} model: {self.model}'


class Rate(models.Model):
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5)])
    car_id = models.ForeignKey('Car', on_delete=models.CASCADE)

    def __str__(self):
        return f'Car_id: {self.car_id}, rating: {self.rating}'
