from django.db import DataError, IntegrityError
from django.test import TestCase

# Create your tests here.
from cars.models import Company, Car, Rate


class CompanyTest(TestCase):

    def setUp(self):
        self.company = Company.objects.create(
            make="test name"
        )

    def test_company_creation(self):
        self.assertTrue(isinstance(self.company, Company))
        self.assertEqual(f'{self.company.make}', 'test name')
        self.assertEqual(self.company.__str__(), self.company.make)

    def test_company_fields(self):
        self.assertEqual(
            [*self.company.__dict__],
            ['_state', 'id', 'make']
        )

    def test_company_make_max_length(self):
        with self.assertRaises(DataError):
            test_company = Company.objects.create(
                make='x' * 256
            )

    def test_company_creation_empty_make(self):
        with self.assertRaises(IntegrityError):
            test_company = Company.objects.create()


class CarTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Test Company'
        )
        self.car = Car.objects.create(
            model='Test Car',
            make=self.company
        )

    def test_car_creation(self):
        self.assertTrue(isinstance(self.car, Car))
        self.assertEqual(f'{self.car.model}', 'Test Car')
        self.assertEqual(self.company, self.car.make)
        self.assertEqual(self.car.__str__(), f'Company: {self.car.make} model: {self.car.model}')

    def test_car_fields(self):
        self.assertEqual(
            [*self.car.__dict__],
            ['_state', 'id', 'model', 'make_id', 'avg_rating', 'rates_number']
        )

    def test_car_model_max_length(self):
        with self.assertRaises(DataError):
            test_car = Car.objects.create(
                model='x' * 256
            )

    def test_car_model_without_data(self):
        with self.assertRaises(IntegrityError):
            test_car = Car.objects.create()

    def test_avg_rating_default(self):
        self.assertEqual(self.car.avg_rating, 0.00)

    def test_rates_number_default(self):
        self.assertEqual(self.car.rates_number, 0)


class RateTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Test Company'
        )
        self.car = Car.objects.create(
            model='Test Car',
            make=self.company
        )
        self.rate = Rate.objects.create(
            car_id=self.car
        )

    def test_rate_create(self):
        self.assertTrue(isinstance(self.rate, Rate))
        self.assertEqual(self.rate.rating, 1)
        self.assertEqual(self.rate.car_id, self.car)
        self.assertEqual(self.rate.__str__(), f'Car_id: {self.rate.car_id}, rating: {self.rate.rating}')
