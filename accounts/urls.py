from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import AccountViewSet


router = DefaultRouter()
router.register('accounts', AccountViewSet, basename='account')

urlpatterns = [
    path('', include(router.urls)),
]