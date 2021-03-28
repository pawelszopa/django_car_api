from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from api.serializers import CarSerializer
from api.views import CarList
from cars.models import Company, Car, Rate

factory = APIRequestFactory()
client = Client()
api_client = APIClient()


class TestCarList(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Honda'
        )
        self.car = Car.objects.create(
            id=90,
            model='Accord',
            make=self.company
        )

    def test_get_car_list(self):
        request = factory.get(reverse("api:car_list"))
        view = CarList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_serializer_response(self):
        serializer_response = client.get(reverse("api:car_list"))
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(serializer_response.data, serializer.data)

    def test_serializer_response_id(self):
        serializer_response = client.get(reverse("api:car_list"))
        data = dict(serializer_response.data[0])
        self.assertEqual(data['id'], self.car.id)
        self.assertEqual(data['id'], self.car.id)
        self.assertEqual(data['make'], self.car.make.make)
        self.assertEqual(data['model'], self.car.model)
        self.assertEqual(data['avg_rating'], self.car.avg_rating)

    def test_post_car_valid_data(self):
        data = {
            "make": "Volvo",
            "model": "V60"
        }
        request = factory.post(reverse("api:car_list"), data=data)
        view = CarList.as_view()
        response = view(request)
        self.assertTrue(Car.objects.filter(model='V60'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_car_invalid_data_make(self):
        data = {
            "test": "Volvo",
            "model": "S60"
        }
        request = factory.post(reverse("api:car_list"), data=data)
        view = CarList.as_view()
        response = view(request)
        self.assertFalse(Car.objects.filter(model='S60'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_car_invalid_data_make_value(self):
        data = {
            "make": "TEST123",
            "model": "S60"
        }
        request = factory.post(reverse("api:car_list"), data=data)
        view = CarList.as_view()
        response = view(request)
        self.assertFalse(Car.objects.filter(model='S60'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_car_invalid_data_model_value(self):
        data = {
            "make": "Volvo",
            "model": "TESTCAR123"
        }
        request = factory.post(reverse("api:car_list"), data=data)
        view = CarList.as_view()
        response = view(request)
        self.assertFalse(Car.objects.filter(model='TESTCAR123'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_car_invalid_data_model(self):
        data = {
            "make": "Volvo",
            "test": "S60"
        }
        request = factory.post(reverse("api:car_list"), data=data)
        view = CarList.as_view()
        response = view(request)
        self.assertFalse(Car.objects.filter(model='S60'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_already_created_car(self):
        data = {
            "make": "Volvo",
            "model": "V60"
        }
        request = factory.post(reverse("api:car_list"), data=data)
        request_second = factory.post(reverse("api:car_list"), data=data)

        view = CarList.as_view()
        response = view(request)
        response_second = view(request_second)
        self.assertFalse(Car.objects.filter(model='V60').count() > 1)
        self.assertEqual(response_second.status_code, status.HTTP_400_BAD_REQUEST)


class TestCarDetail(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Honda'
        )
        self.car = Car.objects.create(
            id=88,
            model='Delete_test_car',
            make=self.company
        )

    def test_delete_car(self):
        request = api_client.delete(f"/cars/{self.car.id}")
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_existing_car(self):
        request = api_client.delete(f"/cars/{934}")
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)



class TestCarRating(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Test Company'
        )
        self.car = Car.objects.create(
            pk=1,
            model='Test Car',
            make=self.company
        )

    def test_add_rating(self):
        rating = {
            "car_id": 1,
            "rating": 4
        }
        response = api_client.post(reverse("api:car_rate"), rating, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.get(id=rating['car_id']).avg_rating, rating['rating'])

    def test_add_multiple_time(self):
        rating = {
            "car_id": 1,
            "rating": 4
        }
        response_1 = api_client.post(reverse("api:car_rate"), rating, format='json')

        rating_2 = {
            "car_id": 1,
            "rating": 2
        }
        response = api_client.post(reverse("api:car_rate"), rating_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.get(id=rating_2['car_id']).avg_rating, 3)

    def test_add_to_big_rating(self):
        rating = {
            "car_id": 1,
            "rating": 41
        }
        response = api_client.post(reverse("api:car_rate"), rating, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_to_low_rating(self):
        rating = {
            "car_id": 1,
            "rating": 0
        }
        response = api_client.post(reverse("api:car_rate"), rating, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rating_to_not_existing_car(self):
        rating = {
            "car_id": 66,
            "rating": 4
        }
        response = api_client.post(reverse("api:car_rate"), rating, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CarPopularTest(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            make='Test Company'
        )
        self.car1 = Car.objects.create(
            pk=1,
            model='Test Car',
            make=self.company
        )
        self.car2 = Car.objects.create(
            id=2,
            model='Civic',
            make=self.company
        )
        self.car3 = Car.objects.create(
            id=3,
            model='City',
            make=self.company
        )

        rating = {
            "car_id": 1,
            "rating": 4
        }
        response_1 = api_client.post(reverse("api:car_rate"), rating, format='json')

        rating_2 = {
            "car_id": 1,
            "rating": 2
        }
        response = api_client.post(reverse("api:car_rate"), rating_2, format='json')

        rating_3 = {
            "car_id": 3,
            "rating": 2
        }
        response = api_client.post(reverse("api:car_rate"), rating_3, format='json')

    def test_order(self):
        serializer_response = client.get(reverse("api:car_popular"))
        self.assertTrue(serializer_response.data[0]['id'] == 1)
        self.assertTrue(serializer_response.data[1]['id'] == 3)
        self.assertTrue(serializer_response.data[2]['id'] == 2)
