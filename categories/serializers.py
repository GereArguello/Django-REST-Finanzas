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

    def validate_name(self, value):
        user = self.context["request"].user
        if Category.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError(
                "Ya existe una categoría con ese nombre."
            )
        return value
    
    def validate(self, data):
        if self.instance is None:
            Category.objects.check_can_create(
                user=self.context["request"].user,
                category_type=data.get("category_type")
            )
        return data



class CategorySetActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()