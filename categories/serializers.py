from rest_framework import serializers

from .models import Category

class CategorySerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M", read_only=True
    )    

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'category_type',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['id']