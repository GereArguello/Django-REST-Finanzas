from django.db import models


class AccountType(models.TextChoices):
    BANK = "BANK", "Banco"
    CASH = "CASH", "Efectivo"
    WALLET = "WALLET", "Billetera virtual"
    CRYPTO = "CRYPTO", "Cripto"


class CategoryType(models.TextChoices):
    INCOME = "INCOME", "Ingreso"
    EXPENSE = "EXPENSE", "Gasto"