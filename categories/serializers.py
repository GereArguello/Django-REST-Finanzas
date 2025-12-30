from rest_framework import serializers

from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'category_type',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['created_at']