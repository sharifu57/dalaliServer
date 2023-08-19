from django.shortcuts import render
from dalali.serializer import *
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
import random
import string
import pendulum

# Create your views here.
def generate_otp():
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(6))

class OwnerViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    queryset = User.objects.filter(is_active=True)
class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.filter(is_active=True, is_deleted=False).order_by('-created')


class PropertyTypeViewSet(viewsets.ModelViewSet):
    serializer_class = PropertyTypeSerializer
    queryset = PropertyType.objects.filter(is_active=True, is_deleted=False).order_by('-created')


class TannantViewSet(viewsets.GenericViewSet):
    queryset = Tennant.objects.filter(is_active=True, is_deleted=False)
    serializer_class = TennantRequestOTPSerializer

    @action(detail=False, methods=['post'])
    def request_otp(self, request):
        phone_number = request.data.get('phone_number')

        if phone_number:
            otp = generate_otp()
            tennant, created = Tennant.objects.get_or_create(phone_number=phone_number)
            tennant.otp = otp
            tennant.is_verified = False
            tennant.save()

            return Response({'message': 'OTP generated successfully.', 'otp': otp})
        else:
            return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        serializer = TennantVerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']

            try:
                tennant = Tennant.objects.filter(
                    phone_number__iexact=phone_number,
                    otp=otp
                ).first()

            except Tennant.DoesNotExist:
                return Response({'message': 'Invalid Number or OTP'}, status=status.HTTP_400_BAD_REQUEST)
    
            if tennant:
                tennant.is_active=True
                tennant.is_deleted=False
                tennant.updated=pendulum.now()
                tennant.is_verified=True
                tennant.save()
                return Response({'message': "Phone Number verified Successfully", 'data': serializer.data}, status=200)

            else:
                return Response({'message': "Incorect OTP"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)