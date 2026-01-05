from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from accounts.models import Account

class AccountsViewSetsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        for i in range(10):
            Account.objects.create(
                user=self.user,
                name=f"{i}",
                provider="Santander rio",
                account_type="BANK",
                balance=50000,
                currency="ARS",
                is_active=True,
            )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_cannot_create_more_than_10_accounts(self):
        url = reverse("account-list")

        data = {
            "name": "ejemplo",
            "provider": "ejemplo",
            "account_type" :"BANK",
            "balance" : 50000,
            "currency" : "ARS",
            "is_active" : True
        }
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
