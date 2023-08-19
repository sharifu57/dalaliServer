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
        fields = '__all__'

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'


class TennantRequestOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tennant
        fields = ['phone_number']


class TennantVerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tennant
        fields = [ 'otp','phone_number']
