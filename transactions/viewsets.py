from rest_framework import viewsets 
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from drf_spectacular.utils import (extend_schema,extend_schema_view,OpenApiResponse)

from .serializers import TransactionSerializer
from .models import Transaction


@extend_schema_view(
    list=extend_schema(
        summary="Listar transacciones",
        description="Devuelve todas las transacciones del usuario autenticado.",
        responses=TransactionSerializer(many=True),
    ),
    retrieve=extend_schema(
        summary="Obtener transacción",
        description="Devuelve el detalle de una transacción del usuario.",
        responses=TransactionSerializer,
    ),
    create=extend_schema(
        summary="Crear transacción",
        description=(
            "Crea una nueva transacción y actualiza automáticamente el balance "
            "de la cuenta asociada.\n\n"
            "- Si la categoría es de tipo INCOME, el balance se incrementa.\n"
            "- Si la categoría es de tipo EXPENSE, el balance se decrementa.\n\n"
            "La operación se ejecuta dentro de una transacción atómica."
        ),
        responses={
            201: TransactionSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
        },
    ),
    update=extend_schema(
        summary="Actualizar transacción",
        description="Actualiza completamente una transacción existente.",
        responses=TransactionSerializer,
    ),
    partial_update=extend_schema(
        summary="Actualizar transacción parcialmente",
        description="Actualiza uno o más campos de una transacción.",
        responses=TransactionSerializer,
    ),
    destroy=extend_schema(
        summary="Eliminar transacción",
        description="Elimina una transacción del usuario.",
    ),
)
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        transaction.account.recalculate_balance()

    @transaction.atomic
    def perform_update(self, serializer):
        old_account = serializer.instance.account
        transaction = serializer.save(user=self.request.user)
        new_account = transaction.account

        old_account.recalculate_balance()
        if old_account != new_account:
            new_account.recalculate_balance()

    @transaction.atomic
    def perform_destroy(self, instance):
        account = instance.account
        instance.delete()
        account.recalculate_balance()
