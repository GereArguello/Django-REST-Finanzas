from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.db.models import Sum, Case, When, DecimalField, F
from utils.choices import AccountType


class AccountManager(models.Manager):
    def check_can_create_for_user(self, user):
        if self.filter(user=user).count() >= 10:
            raise ValidationError(
                "Llegaste al límite de cuentas. Máximo: 10."
            )


class Account(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_account_per_user"
            )
        ]

    class Currency(models.TextChoices):
        ARS = "ARS", "Peso Argentino"
        USD = "USD", "Dólar"
        EUR = "EUR", "Euro"
        USDT = "USDT", "Tether"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts"
    )
    objects = AccountManager()

    name = models.CharField(max_length=50)
    provider = models.CharField(max_length=50, blank=True)
    account_type = models.CharField(
        max_length=10,
        choices=AccountType.choices
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    currency = models.CharField(
        max_length=4,
        choices=Currency.choices
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Al crear la cuenta, el balance inicial es el opening_balance
        if self._state.adding:
            self.balance = self.opening_balance
        super().save(*args, **kwargs)

    def recalculate_balance(self):
        movements_total = (
            self.transactions.aggregate(
                total=Sum(
                    Case(
                        When(
                            category__category_type="INCOME",
                            then=F("amount")
                        ),
                        When(
                            category__category_type="EXPENSE",
                            then=-F("amount")
                        ),
                        output_field=DecimalField(),
                    )
                )
            )["total"]
            or 0
        )

        self.balance = self.opening_balance + movements_total
        self.save(update_fields=["balance"])

    def __str__(self):
        return f"{self.name} - {self.balance}"
