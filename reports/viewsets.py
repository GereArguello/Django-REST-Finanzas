from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import MonthlyBalanceSerializer
from .services.monthly_balance import get_monthly_balance


class ReportViewSet(viewsets.ViewSet):
    """
    Reportes financieros del usuario autenticado.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Balance mensual",
        description=(
            "Devuelve el balance mensual del usuario autenticado.\n\n"
            "Para cada mes se informa:\n"
            "- Total de ingresos\n"
            "- Total de gastos\n"
            "- Detalle de gastos por categoría\n"
            "- Detalle de ingresos por categoría\n\n"
            "Los resultados se devuelven ordenados por mes (descendente)."
        ),
        responses={
            200: MonthlyBalanceSerializer(many=True),
            401: OpenApiResponse(description="No autenticado"),
        },
    )
    @action(detail=False, methods=["get"], url_path="monthly-balance")
    def monthly_balance(self, request):
        data = get_monthly_balance(request.user)
        serializer = MonthlyBalanceSerializer(data, many=True)
        return Response(serializer.data)
