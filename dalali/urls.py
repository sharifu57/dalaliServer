from django.urls import path, include
from . import views
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'create_user', RegisterUserViewSet, basename='create_user')
# router.register(r'categories', CategorViewSet)
# router.register(r'products', ProductViewSet)
# router.register(r'create_product', ProductCreateViewSet, basename='create_food_item')
# router.register(r'create_category', CategoryCreateViewSet, basename='create_category')

urlpatterns = router.urls
