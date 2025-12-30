from django.db import models
from django.contrib.auth.models import User
from utils.choices import AccountType

class Account(models.Model):

    class Currency(models.TextChoices):
        ARS = "ARS", "Peso Argentino"
        USD = "USD", "Dólar"
        EUR = "EUR", "Euro"
        USDT = "USDT", "Tether"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    provider = models.CharField(max_length=50, blank=True)
    account_type = models.CharField(max_length=10,choices=AccountType.choices)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=4,choices=Currency.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.balance}"

    
