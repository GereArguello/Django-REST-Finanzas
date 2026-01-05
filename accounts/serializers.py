from rest_framework import serializers

from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'provider',
            'account_type',
            'balance', 
            'currency',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        user = self.context["request"].user
        if Account.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError(
                "Ya existe una cuenta con ese nombre."
            )
        return value

class AccountSetActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()

