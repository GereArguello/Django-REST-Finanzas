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
            'opening_balance',
            'currency',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'balance']
    
    def validate(self, data):
        # Si es update (ya existe instancia)
        if self.instance and 'opening_balance' in data:
            raise serializers.ValidationError(
                {"opening_balance": "No se puede modificar el saldo inicial."}
            )
        return data

    def validate_name(self, value):
        user = self.context["request"].user
        if not self.instance:
            if Account.objects.filter(user=user, name=value).exists():
                raise serializers.ValidationError(
                    "Ya existe una cuenta con ese nombre."
                )
        return value

class AccountSetActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()

