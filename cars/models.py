from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Company(models.Model):
    make = models.CharField(max_length=255, unique=True, default=None)

    def __str__(self):
        return f'{self.make}'


class Car(models.Model):
    model = models.CharField(max_length=255, unique=True, default=None)
    make = models.ForeignKey('Company', on_delete=models.CASCADE)
    avg_rating = models.DecimalField(default='0.0', max_digits=3, decimal_places=1)
    rates_number = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return f'Company: {self.make} model: {self.model}'


class Rate(models.Model):
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    car_id = models.ForeignKey('Car', on_delete=models.CASCADE)

    def __str__(self):
        return f'Car_id: {self.car_id}, rating: {self.rating}'
