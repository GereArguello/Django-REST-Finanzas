from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from utils.choices import CategoryType

class CategoryManager(models.Manager):
    def check_can_create(self, user, category_type):
        limits = {
            "INCOME": 10,
            "EXPENSE": 20,
        }

        if category_type not in limits:
            return

        count = self.filter(
            user=user,
            category_type=category_type
        ).count()

        if count >= limits[category_type]:
            raise ValidationError(
                f"Llegaste al límite de categorías {category_type}."
            )

class Category(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    objects = CategoryManager()
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