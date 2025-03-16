# api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserBalance, CurrencyExchange
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm')
        extra_kwargs = {'email': {'required': True}}

    def validate_email(self, value):
        # Ensure email is provided
        if not value:
            raise serializers.ValidationError("Email is required")
        # Check if email is already in use
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use")
        return value

    def validate_password(self, value):
        # Use Django's built-in password validators
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords don't match"})
        return data

    def create(self, validated_data):
        # Remove password_confirm field
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        # Create the user
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserBalanceSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserBalance
        fields = ('username', 'balance')


class CurrencyExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchange
        fields = ('id', 'currency_code', 'rate', 'created_at')
        read_only_fields = ('id', 'created_at')
