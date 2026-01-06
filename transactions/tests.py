from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import Account
from categories.models import Category
from .models import Transaction


class TransactionsViewSetTests(TestCase):

    user = get_user_model()

    def setUp(self):
        self.user_account = self.user.objects.create_user(
            username="user_account",
            password="1234"
        )

        self.user_category = self.user.objects.create_user(
            username="user_category",
            password="1234"
        )
        self.account_user_account = Account.objects.create(
            user = self.user_account,
            name = "Santander",
            provider = "Santander rio",
            account_type = "BANK",
            opening_balance = 50000,
            currency = "ARS",
            is_active = True,
        )

        self.account2_user_account = Account.objects.create(
            user = self.user_account,
            name = "Banco galicia",
            provider = "Santander rio",
            account_type = "BANK",
            opening_balance = 0,
            currency = "ARS",
            is_active = True,
        )

        self.category_user_account = Category.objects.create(
            user = self.user_account,
            name = "Salario",
            category_type = "INCOME",
            is_active = True
        )

        self.category_user_category = Category.objects.create(
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
            "account": self.account_user_account.name,
            "category": self.category_user_category.name,
            "amount": 1000,
            "description": "Test",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_perform_update_should_recalculate_balances_when_account_changes(self):
        
        # Transacción en cuenta 1
        transaction = Transaction.objects.create(
            user=self.user_account,
            account = self.account_user_account,
            category = self.category_user_account,
            amount = 1000,
        )
        self.account_user_account.recalculate_balance()
        self.account_user_account.refresh_from_db()
        self.assertEqual(self.account_user_account.balance, 51000)

        # Mover la transacción a cuenta 2

        url = reverse("transaction-detail", args=[transaction.id])
        data = {
            "account" : self.account2_user_account.name,
            "category" : self.category_user_account.name,
            "amount" : 1000
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refrescar balances
        self.account_user_account.refresh_from_db()
        self.account2_user_account.refresh_from_db()

        self.assertEqual(self.account_user_account.balance, 50000)
        self.assertEqual(self.account2_user_account.balance, 1000)