from django.db import models
from django.contrib.auth.models import User
from utils.choices import CategoryType


class Category(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category_type = models.CharField(
        max_length=10,
        choices=CategoryType.choices
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name