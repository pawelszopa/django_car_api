import json

from django.test import TestCase

# Create your tests here.
from api.serializers import CarSerializer, CarPopularSerializer, CarRatingSerializer
from cars.models import Car, Company, Rate


class TestCarSerializer(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Honda'
        )
        self.car = Car.objects.create(
            model='Accord',
            make=self.company
        )

        self.serialized_model = CarSerializer(instance=self.car)

    def test_module_fields(self):
        data = self.serialized_model.data
        self.assertEqual(data.keys(), {'id', 'make', 'model', 'avg_rating'})


class CarPopularSerializerTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Honda'
        )
        self.car = Car.objects.create(
            model='Accord',
            make=self.company
        )

        self.serialized_model = CarPopularSerializer(instance=self.car)

    def test_module_fields(self):
        data = self.serialized_model.data
        self.assertEqual(data.keys(), {'id', 'make', 'model', 'rates_number'})


class CarRatingSerializerTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Honda'
        )
        self.car = Car.objects.create(
            model='Accord',
            make=self.company
        )
        self.rate = Rate.objects.create(
            car_id=self.car
        )
        self.serialized_model = CarRatingSerializer(instance=self.rate)

    def test_module_fields(self):
        data = self.serialized_model.data
        self.assertEqual(data.keys(), {'car_id', 'rating'})


