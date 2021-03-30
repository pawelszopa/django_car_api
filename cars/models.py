from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Company(models.Model):
    make = models.CharField(max_length=255, unique=True, default=None)

    def __str__(self):
        return f'{self.make}'


class Car(models.Model):
    model = models.CharField(max_length=255, unique=True, default=None)
    make = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        return f'Company: {self.make} model: {self.model}'


class Rate(models.Model):
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    car = models.ForeignKey('Car', on_delete=models.CASCADE)

    def __str__(self):
        return f'Car_id: {self.car}, rating: {self.rating}'
