from rest_framework import serializers
from dalali.models import *
from django.contrib.auth.models import User


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class PropertyPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = '__all__'

class PropertyViewSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    # photos = PropertyPhotosSerializer()
    class Meta:
        model = Property
        fields = '__all__'

        
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id',
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
