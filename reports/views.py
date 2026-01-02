
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Sum, Case, When, DecimalField
from django.db.models.functions import TruncMonth

from transactions.models import Transaction
from .serializers import MonthlyBalanceSerializer


class MonthlyBalanceView(APIView):

    """
    Devuelve el balance mensual agregado del usuario autenticado.
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Primero se crea el campo "month" truncando created_at al mes.
        # Luego, al usar values("month"), se agrupan las transacciones exclusivamente por mes.
        # A partir de ese agrupamiento, se usan annotate + Sum para crear las columnas
        # "income" y "expense", que se calculan a partir de los amount de todas las
        # transacciones que pertenecen a cada mes.

        qs = (
            Transaction.objects
            .filter(user=request.user)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(
                income=Sum(
                    Case(
                        When(category__category_type="INCOME", then="amount"),
                        default=0,
                        output_field=DecimalField(),
                    )
                ),
                expense=Sum(
                    Case(
                        When(category__category_type="EXPENSE", then="amount"),
                        default=0,
                        output_field=DecimalField(),
                    )
                ),
            )
            .order_by("-month")
        )

        serializer = MonthlyBalanceSerializer(qs, many=True)
        return Response(serializer.data)
