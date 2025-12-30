from rest_framework import serializers

from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M", read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'account',
            'category',
            'amount',
            'description',
            'created_at'
        ]
        read_only_fields = ['id']

    def validate_account(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError(
                "La cuenta no pertenece al usuario."
            )
        return value

    
    def validate_category(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError(
                "La categoría no pertenece al usuario."
            )
        return value
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El monto debe ser mayor a cero."
            )
        return value
