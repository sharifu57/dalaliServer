from django.urls import path, include
from . import views
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', OwnerViewSet, basename="users")
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'property_types', PropertyTypeViewSet, basename='propertyTypes')
router.register(r'tennant', TannantViewSet, basename='tennant')

urlpatterns = router.urls
