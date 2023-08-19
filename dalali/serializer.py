from rest_framework import serializers
from dalali.models import *
from django.contrib.auth.models import User


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'owner',
            'title', 
            'property_number',
            'description', 
            'property_type', 
            'price', 'status', 
            'location'
        ]

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['title', 'description', 'icon']


class TennantRequestOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tennant
        fields = ['phone_number']


class TennantVerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tennant
        fields = [ 'otp','phone_number']
