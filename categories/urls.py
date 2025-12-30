from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CategoryViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]