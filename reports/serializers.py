from rest_framework import serializers
from decimal import Decimal


class CategoryAmountSerialiszer(serializers.Serializer):
    category = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class MonthlyBalanceSerializer(serializers.Serializer):

    month = serializers.SerializerMethodField()
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    incomes_by_category = CategoryAmountSerialiszer(many=True)
    expenses_by_category = CategoryAmountSerialiszer(many=True)

    balance = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    def get_month(self, obj):
        return obj["month"].strftime("%Y-%m")

    def to_representation(self, obj):
        data = super().to_representation(obj)
        balance = Decimal(data["income"]) - Decimal(data["expense"])
        data["balance"] = f"{balance:.2f}"
        return data

