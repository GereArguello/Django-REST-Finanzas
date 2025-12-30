from rest_framework import serializers

from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'account',
            'category',
            'transaction_type',
            'amount',
            'description',
            'created_at'
        ]
        read_only_fields = ['id','created_at']

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

    def validate(self, data):
        category = data['category']
        transaction_type = data['transaction_type']

        if category.category_type != transaction_type:
            raise serializers.ValidationError(
                "El tipo de transacción no coincide con el tipo de la categoría."
            )

        return data