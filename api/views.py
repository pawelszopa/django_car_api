from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from api.serializers import CarSerializer
from cars.models import Car


class CarList(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
