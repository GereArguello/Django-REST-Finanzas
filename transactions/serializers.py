from rest_framework import serializers

from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    ) #Nos aseguramos que el user siempre venga de request

    created_at = serializers.DateTimeField(
        format="%d/%m/%Y %H:%M", read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'account',
            'category',
            'amount',
            'description',
            'created_at'
        ]
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Con esto nos aseguramos que los choices correspondan a la cuenta del usuario que hace el request
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['account'].queryset = (
                self.fields['account'].queryset.filter(user=request.user)
            )
            self.fields['category'].queryset = (
                self.fields['category'].queryset.filter(user=request.user)
            )

    def validate(self, data):
        account = data.get("account")
        category = data.get("category")

        if account and category and account.user != category.user:
            raise serializers.ValidationError(
                "La cuenta y la categoría no pertenecen al mismo usuario."
            )

        return data
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El monto debe ser mayor a cero."
            )
        return value
