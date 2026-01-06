from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category

class CategoriesViewSetsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="1234"
        )

        for i in range(10):
            Category.objects.create(
                user = self.user,
                name = f"income_{i}",
                category_type = "INCOME",
                is_active = True
            )
        for i in range(20):
            Category.objects.create(
                user = self.user,
                name = f"expense_{i}",
                category_type = "EXPENSE",
                is_active = True
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_cannot_create_more_than_10_categories_income(self):
        url = reverse("category-list")

        data = {
            "name" : "ejemplo",
            "category_type" : "INCOME",
            "is_active" : True
        }
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cannot_create_more_than_10_categories_expense(self):
        url = reverse("category-list")

        data = {
            "name" : "ejemplo",
            "category_type" : "EXPENSE",
            "is_active" : True
        }
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_income_category_below_limit(self):
        Category.objects.filter(
            user=self.user,
            category_type="INCOME"
        ).delete()

        url = reverse("category-list")

        data = {
            "name": "income_ok",
            "category_type": "INCOME",
            "is_active": True
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_other_user_can_create_categories(self):
        other_user = User.objects.create_user(
            username="other",
            password="1234"
        )
        self.client.force_authenticate(user=other_user)

        url = reverse("category-list")

        data = {
            "name": "otra",
            "category_type": "INCOME",
            "is_active": True
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
