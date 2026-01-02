from django.urls import path
from .views import MonthlyBalanceView

urlpatterns=[
    path('reports/',MonthlyBalanceView.as_view(), name='report')
]