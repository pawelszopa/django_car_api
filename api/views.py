import requests
from django.db.models import Count, Avg, Func

from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response

from api.serializers import CarSerializer, CarPopularSerializer, CarRatingSerializer
from cars.models import Car, Company, Rate


class CarList(ListCreateAPIView):
    serializer_class = CarSerializer
    model = Car

    def get_queryset(self):
        queryset = Car.objects.select_related("make").all().annotate(
            avg_rating=Func(Avg("rate__rating"), 2, function="ROUND"))
        return queryset

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
                try:
                    json_data = self.request_to_external_car_api(request.data['make'])
                except:
                    return Response('External API problem', status=status.HTTP_400_BAD_REQUEST)

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
                    rating = Rate.objects.create(car=car, rating=request.data['rating'])
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response('Car does not exist', status=status.HTTP_400_BAD_REQUEST)
        return Response(serialization.errors, status=status.HTTP_400_BAD_REQUEST)


class CarPopular(ListAPIView):
    serializer_class = CarPopularSerializer
    model = Car
    queryset = Car.objects.select_related("make").all().annotate(
        rates_number=Count("rate__rating")).order_by("-rates_number")
