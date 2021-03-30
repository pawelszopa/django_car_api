from django.db.models import Avg
from rest_framework import serializers

from cars.models import Car, Rate


class CarSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.make', required=True, max_length=255)
    model = serializers.CharField(required=True, max_length=255)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'avg_rating')
        depth = 1


class CarPopularSerializer(serializers.ModelSerializer):
    make = serializers.ReadOnlyField(source='make.make')
    rates_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'rates_number')
        depth = 1


class CarRatingSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='car.id')

    class Meta:
        model = Rate
        fields = ('car_id', 'rating')
        depth = 1
