from rest_framework import serializers

from cars.models import Car, Rate


class CarSerializer(serializers.ModelSerializer):
    make = serializers.CharField(source='make.make', required=True)
    model = serializers.CharField(required=True)

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'avg_rating')
        depth = 1
        read_only_fields = ('id', 'avg_rating', 'rates_number')


class CarPopularSerializer(serializers.ModelSerializer):
    make = serializers.ReadOnlyField(source='make.make')

    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'rates_number')
        depth = 1


class CarRatingSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='car_id.id')

    class Meta:
        model = Rate
        fields = ('car_id', 'rating')
        depth = 1
