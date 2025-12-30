from django.db import models
from accounts.models import Account
from categories.models import Category
from django.contrib.auth.models import User
from utils.choices import CategoryType

class Transaction(models.Model):

    class Meta:
        ordering = ['-created_at']
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.category} - {self.amount}"
