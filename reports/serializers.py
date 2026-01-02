from rest_framework import serializers


class MonthlyBalanceSerializer(serializers.Serializer):

    month = serializers.SerializerMethodField()
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.SerializerMethodField()

    def get_month(self, obj):
        # obj["month"] es una fecha (ej: 2026-01-01)
        return obj["month"].strftime("%Y-%m")

    def get_balance(self, obj):
        return obj["income"] - obj["expense"]