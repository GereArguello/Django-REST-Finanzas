from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (extend_schema, extend_schema_view, OpenApiResponse)
from .serializers import AccountSerializer, AccountSetActiveSerializer
from .models import Account

@extend_schema_view(
    list=extend_schema(
        summary="Listar cuentas",
        description="Devuelve todas las cuentas del usuario autenticado.",
        responses=AccountSerializer(many=True),
    ),
    retrieve=extend_schema(
        summary="Obtener cuenta",
        description="Devuelve el detalle de una cuenta del usuario.",
        responses=AccountSerializer,
    ),
    create=extend_schema(
        summary="Crear cuenta",
        description=(
            "Crea una nueva cuenta.\n\n"
            "La cuenta se asocia automáticamente al usuario autenticado."
        ),
        responses=AccountSerializer,
    ),
    update=extend_schema(
        summary="Actualizar cuenta",
        description="Actualiza completamente una cuenta existente.",
        responses=AccountSerializer,
    ),
    partial_update=extend_schema(
        summary="Actualizar cuenta parcialmente",
        description="Actualiza uno o más campos de una cuenta.",
        responses=AccountSerializer,
    ),
    destroy=extend_schema(
        summary="Eliminar cuenta",
        description="Elimina permanentemente una cuenta del usuario.",
    ),
)
class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            Account.objects.check_can_create_for_user(self.request.user)
        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)
        
        serializer.save(user=self.request.user)



    @extend_schema(
        summary="Activar o desactivar cuenta",
        description=(
            "Activa o desactiva una cuenta sin modificar otros campos.\n\n"
            "Este endpoint solo modifica el estado `is_active`."
        ),
        request=AccountSetActiveSerializer,
        responses={
            200: AccountSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            404: OpenApiResponse(description="Cuenta no encontrada"),
        },
    )
    @action(methods=["PATCH"],detail=True,url_path="set-active",serializer_class=AccountSetActiveSerializer)
    def set_active(self, request, pk=None):
        account = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account.is_active = serializer.validated_data["is_active"]
        account.save()

        return Response(
            AccountSerializer(account).data,
            status=status.HTTP_200_OK,
        )
