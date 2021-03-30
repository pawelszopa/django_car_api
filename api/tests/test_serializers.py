import json

from django.test import TestCase

# Create your tests here.
from api.serializers import CarSerializer, CarPopularSerializer, CarRatingSerializer
from cars.models import Car, Company, Rate


class CarSerializerTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Honda'
        )
        self.car = Car.objects.create(
            model='Accord',
            make=self.company
        )

        self.serializer_data = {
            "make": "Volkswagen",
            "model": "Golf"
        }

        Rate.objects.create(car=self.car, rating=5)
        Rate.objects.create(car=self.car, rating=1)

        self.serialized_model = CarSerializer(instance=self.car)

    def test_get_module_fields(self):
        data = self.serialized_model.data
        self.assertTrue('make' in data.keys())
        self.assertTrue('id' in data.keys())
        self.assertTrue('model' in data.keys())

    def test_get_serializer_expected_values(self):
        data = self.serialized_model.data
        self.assertEqual(data["id"], self.car.id)
        self.assertEqual(data["make"], self.company.make)
        self.assertEqual(data["model"], self.car.model)

    def test_contain_expected_values(self):
        data = self.serialized_model.data
        self.assertEqual(data["make"], self.company.make)
        self.assertEqual(data["model"], self.car.model)

    def test_too_long_make(self):
        self.serializer_data["make"] = "x" * 256
        serializer = CarSerializer(data=self.serializer_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["make"])

    def test_too_long_model(self):
        self.serializer_data["model"] = "x" * 256
        serializer = CarSerializer(data=self.serializer_data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["model"])

    def test_valid_data(self):
        serializer = CarSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)


class CarPopularSerializerTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Honda'
        )
        self.car = Car.objects.create(
            model='Accord',
            make=self.company
        )

        Rate.objects.create(car=self.car, rating=5)
        Rate.objects.create(car=self.car, rating=1)

        self.serialized_model = CarPopularSerializer(instance=self.car)

    def test_module_fields(self):
        data = self.serialized_model.data
        self.assertEqual(data.keys(), {'id', 'make', 'model'})

    def test_get_serializer_expected_values(self):
        data = self.serialized_model.data
        self.assertEqual(data["id"], self.car.id)
        self.assertEqual(data["make"], self.company.make)
        self.assertEqual(data["model"], self.car.model)


class CarRatingSerializerTest(TestCase):
    def setUp(self):
        self.serializer_data = {
            "car_id": 1,
            "rating": 1
        }

        self.company = Company.objects.create(
            make='Honda'
        )
        self.car = Car.objects.create(
            model='Accord',
            make=self.company
        )
        self.rate = Rate.objects.create(
            car=self.car
        )
        self.serialized_model = CarRatingSerializer(instance=self.rate)

    def test_module_fields(self):
        data = self.serialized_model.data
        self.assertEqual(data.keys(), {'car_id', 'rating'})

    def test_contain_expected_values(self):
        data = self.serialized_model.data
        self.assertEqual(data["car_id"], self.rate.car.id)
        self.assertEqual(data["rating"], self.rate.rating)

    def test_too_small_rating_data(self):
        self.serializer_data["rating"] = 0
        serializer = CarRatingSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["rating"])

    def test_too_big_rating_data(self):
        self.serializer_data["rating"] = 6
        serializer = CarRatingSerializer(data=self.serializer_data)

        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ["rating"])
