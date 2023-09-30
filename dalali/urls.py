from django.urls import path, include
from dalali.views import *
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', OwnerViewSet, basename="users")
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'property_types', PropertyTypeViewSet, basename='propertyTypes')
router.register(r'tennant', TannantViewSet, basename='tennant')
router.register(r'owner_properties', PropertiesViewSet, basename='property')
router.register(r'locations', LocationsViewSet, basename="location")
router.register(r'location_properties', LocationPropertiesViewSet, basename='location_properties')
router.register(r'properties_list', PropertyListViewSet, basename='properties_list')
router.register(r'', CreateNewPropertyViewSet, basename="new_property")

urlpatterns = router.urls
