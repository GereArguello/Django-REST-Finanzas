
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Sum, Case, When, DecimalField
from django.db.models.functions import TruncMonth

from collections import defaultdict 

from transactions.models import Transaction
from .serializers import MonthlyBalanceSerializer


class ReportViewSet(viewsets.ViewSet):

    """
    Devuelve el balance mensual del usuario autenticado.
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="monthly-balance")
    def monthly_balance(self, request):

        # Primero se crea el campo "month" truncando created_at al mes.
        # Luego, al usar values("month"), se agrupan las transacciones exclusivamente por mes.
        # A partir de ese agrupamiento, se usan annotate + Sum para crear las columnas
        # "income" y "expense", que se calculan a partir de los amount de todas las
        # transacciones que pertenecen a cada mes.

        monthly_qs = (
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

        #Filtramos las categorías por TIPO para tener el monto total de cada categoría

        expenses_by_category = (
            Transaction.objects
            .filter(
                user=request.user,
                category__category_type="EXPENSE"
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month", "category__name")
            .annotate(total=Sum("amount"))
        )

        incomes_by_category = (
            Transaction.objects
            .filter(
                user=request.user,
                category__category_type="INCOME"
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month", "category__name")
            .annotate(total=Sum("amount"))
        )


        #Mapa para guardar todos los datos de incomes y expenses
        categories_map = defaultdict(lambda: {
            "expenses": [],
            "incomes": []
        })  #En caso de que un mes esté vació devolvemos []

        for row in expenses_by_category:
            categories_map[row["month"]]["expenses"].append({ #Agregamos por mes y tipo la categoría y monto
                "category": row["category__name"],
                "amount": row["total"]
            })

        for row in incomes_by_category:
            categories_map[row["month"]]["incomes"].append({
                "category": row["category__name"],
                "amount": row["total"]
            })

        #Ordenamos los valores de mayor a menor
        for month_data in categories_map.values():
            month_data["expenses"].sort(
                key=lambda x: x["amount"],
                reverse=True
            )
            month_data["incomes"].sort(
                key=lambda x: x["amount"],
                reverse=True
            )

        #Lista con todos los datos a serializar
        result = []

        # Combinamos los totales mensuales con el detalle por categoría
        for row in monthly_qs:
            result.append({
                "month": row["month"],
                "income": row["income"],
                "expense": row["expense"],
                "expenses_by_category": categories_map[row["month"]]["expenses"],
                "incomes_by_category": categories_map[row["month"]]["incomes"],
            })


        serializer = MonthlyBalanceSerializer(result, many=True)
        return Response(serializer.data)
