from rest_framework import serializers
from dalali.models import *
from django.contrib.auth.models import User


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = OwnerSerializer()
    class Meta:
        model = UserProfile
        fields = "__all__"

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
    photos = PropertyPhotosSerializer()
    class Meta:
        model = Property
        fields = '__all__'

        
class PropertySerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    owner = OwnerSerializer()
    class Meta:
        model = Property
        fields = '__all__'

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

###############################################################################33

class PropertiesSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()
    location = LocationSerializer()
    photos = PropertyPhotosSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = "__all__"