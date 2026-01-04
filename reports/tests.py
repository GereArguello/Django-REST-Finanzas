from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction

class ReportsViewSetsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        self.account = Account.objects.create(
            user=self.user,
            name="Santander",
            provider="Santander rio",
            account_type="BANK",
            balance=50000,
            currency="ARS",
            is_active=True,
        )

        self.income_category = Category.objects.create(
            user=self.user,
            name="Pedidosya",
            category_type="INCOME",
            is_active=True
        )

        self.expense_category = Category.objects.create(
            user=self.user,
            name="Supermercado",
            category_type="EXPENSE",
            is_active=True
        )

        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.income_category,
            amount=15000
        )

        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.expense_category,
            amount=5000
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_monthly_balance_report(self):
        url = reverse("reports-monthly-balance")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # El endpoint devuelve una lista de reportes mensuales
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

        data = response.data[0]  # primer mes del reporte

        # Totales mensuales
        self.assertEqual(data["income"], "15000.00")
        self.assertEqual(data["expense"], "5000.00")
        self.assertEqual(data["balance"], "10000.00")

        # Detalle por categoría
        self.assertEqual(data["incomes_by_category"][0]["category"], "Pedidosya")
        self.assertEqual(data["expenses_by_category"][0]["category"], "Supermercado")
