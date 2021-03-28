import json
import urllib

import requests
from django.db.models import Avg
from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView, UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response

from api.serializers import CarSerializer, CarPopularSerializer, CarRatingSerializer
from cars.models import Car, Company, Rate


class CarList(ListCreateAPIView):
    serializer_class = CarSerializer
    model = Car

    def get_queryset(self):
        query = self.model.objects.all().prefetch_related('make')
        return query

    def post(self, request, *args, **kwargs):
        serialization = CarSerializer(data=request.data)

        if serialization.is_valid():
            company_name_capitalize = request.data['make'].capitalize()
            company = Company.objects.filter(make=company_name_capitalize).first()

            if company:
                car = Car.objects.filter(make=company.id).filter(model=request.data['model']).first()

            if company and car:
                return Response('Already exist', status=status.HTTP_400_BAD_REQUEST)

            else:
                json_data = self.request_to_external_car_api(request.data['make'])

                if json_data['Count'] > 0:
                    for model in json_data['Results']:
                        if model['Model_Name'] == request.data['model']:
                            make = Company.objects.get_or_create(make=request.data['make'].capitalize())
                            Car.objects.create(make=make[0], model=request.data['model'])
                            return Response(status=status.HTTP_201_CREATED)
                    return Response('Model not found in API', status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response('Model not found in API', status=status.HTTP_400_BAD_REQUEST)

        return Response(serialization.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def request_to_external_car_api(company):
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{company.upper()}?format=json'
        json_data = requests.get(url).json()
        return json_data


class CarDetail(RetrieveDestroyAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Car.objects.filter(pk=pk).prefetch_related('make')
        return queryset


class CarRating(CreateAPIView):
    serializer_class = CarRatingSerializer

    def post(self, request, *args, **kwargs):
        serialization = CarRatingSerializer(data=request.data)
        if serialization.is_valid():
            if request.data['rating'] in range(1, 5):
                car = Car.objects.filter(id=request.data['car_id']).first()
                if car:
                    rating = Rate.objects.create(car_id=car, rating=request.data['rating'])
                    car.rates_number = car.rates_number + 1
                    car.avg_rating = Rate.objects.filter(car_id=car.id).aggregate(Avg('rating'))['rating__avg']
                    car.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response('Car does not exist', status=status.HTTP_400_BAD_REQUEST)
        return Response(serialization.errors, status=status.HTTP_400_BAD_REQUEST)


class CarPopular(ListAPIView):
    serializer_class = CarPopularSerializer
    model = Car

    def get_queryset(self):
        query = self.model.objects.all().order_by("-rates_number").prefetch_related('make')
        return query
