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
    rates_number = models.IntegerField(default=0)

    def __str__(self):
        return f'Company: {self.make} model: {self.model}'
