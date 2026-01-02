from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from accounts.models import Account
from categories.models import Category


class TransactionsViewSetTests(TestCase):

    def setUp(self):
        self.user_account = User.objects.create_user(
            username="user_account",
            password="1234"
        )

        self.user_category = User.objects.create_user(
            username="user_category",
            password="1234"
        )
        self.account = Account.objects.create(
            user = self.user_account,
            name = "Santander",
            provider = "Santander rio",
            account_type = "BANK",
            balance = 50000,
            currency = "ARS",
            is_active = True,
        )
        self.category = Category.objects.create(
            user = self.user_category,
            name = "Verduras",
            category_type = "EXPENSE",
            is_active = True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_account)

    def test_transaction_fails_if_account_and_category_have_different_users(self):
        url = reverse("transaction-list")

        data = {
            "account": self.account.id,
            "category": self.category.id,
            "amount": 1000,
            "description": "Test",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)