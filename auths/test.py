from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from auths.helpers import register_user, login_user


class AuthsUserTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("token_obtain_pair")

        self.user_data = {
            "username": "Pepe",
            "email": "ejemplo123@gmail.com",
            "password": "Ejemplo1234",
            "password2": "Ejemplo1234"
        }


    def test_register_should_fail_if_passwords_do_not_match(self):
        data = self.user_data.copy()
        data["password2"] = "WrongPassword"

        response = register_user(self.client, self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Las contraseñas no coinciden"
        )

    def test_register_should_fail_if_email_exists(self):
        register_user(self.client, self.register_url, self.user_data)

        data = self.user_data.copy()
        data["username"] = "OtroUsuario"

        response = register_user(self.client, self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["email"][0],
            "El email ya está registrado"
        )


    def test_register_should_return_201(self):
        response = register_user(self.client, self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_login_should_return_tokens(self):
        register_user(self.client, self.register_url, self.user_data)

        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"]
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


    def test_login_should_fail_with_wrong_password(self):
        register_user(self.client, self.register_url, self.user_data)

        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": "wrongpassword"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_access_protected_endpoint(self):
        register_user(self.client, self.register_url, self.user_data)
        login_user(self.client, self.login_url, self.user_data["username"], self.user_data["password"])

        response = self.client.get(reverse("account-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_should_fail_if_not_have_access_token(self):

        response = self.client.get(reverse("account-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_logout_should_blacklist_token(self):
        register_user(self.client, self.register_url, self.user_data)
        
        login_response = login_user(self.client, self.login_url, self.user_data["username"], self.user_data["password"])

        refresh = login_response.data["refresh"]

        response = self.client.post(
            reverse("logout"),
            {"refresh": refresh},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # intentar usar refresh token nuevamente
        refresh_response = self.client.post(
            reverse("token_refresh"),
            {"refresh": refresh},
            format="json"
        )

        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_should_fail_without_refresh_token(self):
        register_user(self.client, self.register_url, self.user_data)
        login_user(self.client, self.login_url, self.user_data["username"], self.user_data["password"])

        response = self.client.post(reverse("logout"), {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
