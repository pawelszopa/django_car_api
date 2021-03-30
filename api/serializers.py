from django.db.models import Avg
from rest_framework import serializers

from cars.models import Car, Rate


class CarSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.make', required=True, max_length=255)
    model = serializers.CharField(required=True, max_length=255)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'avg_rating')
        depth = 1

    @staticmethod
    def get_avg_rating(instance):
        try:
            avg_rating = round(Rate.objects.filter(car=instance.id).aggregate(Avg('rating')).get('rating__avg'), 2)
        except TypeError:
            avg_rating = 0

        return avg_rating


class CarPopularSerializer(serializers.ModelSerializer):
    make = serializers.ReadOnlyField(source='make.make')
    rates_number = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'rates_number')
        depth = 1

    @staticmethod
    def get_rates_number(instance):
        return Rate.objects.filter(car=instance.id).count()


class CarRatingSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='car.id')

    class Meta:
        model = Rate
        fields = ('car_id', 'rating')
        depth = 1
