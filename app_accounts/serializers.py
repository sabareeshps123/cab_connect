from rest_framework import serializers
from .models import User, Driver
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password', 'user_type')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class DriverProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Driver
        fields = ['user', 'gender', 'latitude', 'longitude', 'license', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise ValueError("User must be provided when creating a Driver profile.")
        return Driver.objects.create(user=user, **validated_data)




