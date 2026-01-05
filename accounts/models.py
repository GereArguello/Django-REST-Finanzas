from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from utils.choices import AccountType

# Regla de dominio a nivel colección que impide crear más de 10 cuentas por usuario


class AccountManager(models.Manager):
    def check_can_create_for_user(self, user):
        if self.filter(user=user).count() >= 10:
            raise ValidationError(
                "Llegaste al límite de cuentas. Máximo: 10."
            )

class Account(models.Model):

    class Currency(models.TextChoices):
        ARS = "ARS", "Peso Argentino"
        USD = "USD", "Dólar"
        EUR = "EUR", "Euro"
        USDT = "USDT", "Tether"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    objects = AccountManager() #reemplazo del manager genérico
    name = models.CharField(max_length=50)
    provider = models.CharField(max_length=50, blank=True)
    account_type = models.CharField(max_length=10,choices=AccountType.choices)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=4,choices=Currency.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.balance}"
    
    class Meta:
        unique_together = ["user", "name"]

    
