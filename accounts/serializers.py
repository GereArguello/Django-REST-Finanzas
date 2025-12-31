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

class AccountSetActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()