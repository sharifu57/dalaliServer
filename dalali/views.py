from django.shortcuts import render
from dalali.serializer import *
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
import random
import string
import pendulum


# Create your views here.
def generate_otp():
    digits = string.digits
    return "".join(random.choice(digits) for _ in range(5))


class OwnerViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerSerializer
    queryset = User.objects.filter(is_active=True)


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertyViewSerializer
    queryset = Property.objects.filter(is_active=True, is_deleted=False).order_by(
        "-created"
    )[:5]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("photos")
        return queryset


# class PropertyTypeViewSet(viewsets.ModelViewSet):
#     serializer_class = PropertyTypeSerializer
#     queryset = PropertyType.objects.filter(is_active=True, is_deleted=False).order_by(
#         "-created"
#     )


class PropertyTypeViewSet(viewsets.ModelViewSet):
    serializer_class = PropertyTypeSerializer
    queryset = PropertyType.objects.filter(is_active=True, is_deleted=False).order_by(
        "-created"
    )


class LocationsViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter(is_active=True, is_deleted=False).order_by(
        "-name"
    )


class PropertiesViewSet(viewsets.GenericViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.filter(is_active=True, is_deleted=False).order_by(
        "-created"
    )

    @action(detail=True, methods=["get"])
    def properties_by_owner_id(self, request, pk=None):
        try:
            owner = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"message": "Owner does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        properties = Property.objects.filter(
            owner=owner, is_active=True, is_deleted=False
        ).order_by("-created")
        serializer = PropertySerializer(properties, many=True)

        return Response({"data": serializer.data})


class TannantViewSet(viewsets.GenericViewSet):
    queryset = Tennant.objects.filter(is_active=True, is_deleted=False)
    serializer_class = TennantRequestOTPSerializer

    @action(detail=False, methods=["post"])
    def request_otp(self, request):
        phone_number = request.data.get("phone_number")

        if phone_number:
            otp = generate_otp()
            tennant, created = Tennant.objects.get_or_create(phone_number=phone_number)
            tennant.otp = otp
            tennant.is_verified = False
            tennant.save()

            return Response(
                {"status": 200, "message": "OTP generated successfully.", "otp": otp}
            )
        else:
            return Response(
                {"message": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"])
    def verify_otp(self, request):
        serializer = TennantVerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            otp = serializer.validated_data["otp"]

            try:
                tennant = Tennant.objects.filter(
                    phone_number__iexact=phone_number, otp=otp
                ).first()

            except Tennant.DoesNotExist:
                return Response(
                    {"message": "Invalid Number or OTP"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if tennant:
                tennant.is_active = True
                tennant.is_deleted = False
                tennant.updated = pendulum.now()
                tennant.is_verified = True
                tennant.save()
                return Response(
                    {
                        "status": 200,
                        "message": "Phone Number verified Successfully",
                        "data": serializer.data,
                    },
                    status=200,
                )

            else:
                return Response(
                    {"message": "Incorect OTP"}, status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationPropertiesViewSet(viewsets.GenericViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter(is_active=True, is_deleted=False)

    @action(detail=True, methods=["get"])
    def get_properties(self, request, pk=None):
        try:
            location = Location.objects.get(id=pk)

        except Location.DoesNotExist:
            return Response(
                {"message": "Location does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        properties = Property.objects.filter(
            location=location, is_active=True, is_deleted=False
        )

        serializers = PropertiesSerializer(properties, many=True)
        return Response({"data": serializers.data})


class PropertyListViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertiesSerializer


class CreateNewPropertyViewSet(viewsets.GenericViewSet):
    serializer_class = CreatePropertySerializer
    queryset = Property.objects.filter(is_active=True, is_deleted=False)

    @action(detail=False, methods=["POST"])
    def create_property(self, request):
        try:
            serializer = CreatePropertySerializer(data=request.data)
            print(serializer)

            if serializer.is_valid():
                property = serializer.save()

                photo = request.data.get("photos", [])

                for p in photo:
                    # to be emplemented later on 
                    print("_____here p")
                    print(p)
                PropertyPhoto.objects.create(property=property, url=photo)
                return Response({"message": "Property created successfully"}, status=201)

        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=500)
            

