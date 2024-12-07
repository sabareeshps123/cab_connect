
from rest_framework import serializers
from .models import Ride
from app_accounts.models import User, Driver

class RideSerializer(serializers.ModelSerializer):
    rider_name = serializers.CharField(source='rider.username', read_only=True)

    class Meta:
        model = Ride
        fields = [
            'id',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'status',
            'created_at',
            'updated_at',
            'rider_name'
        ]

    def create(self, validated_data):
        validated_data['rider'] = self.context['user']
        return super().create(validated_data)

    def validate(self, data):
        user = self.context.get('user')
        if user.user_type != 'rider':
            raise serializers.ValidationError("Only riders can create ride requests.")
        return data


class DriverLocationSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Driver
        fields = [
            'id',
            'latitude',
            'longitude',
            'driver_name'
        ]
