from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (extend_schema,extend_schema_view,OpenApiResponse)
from .serializers import CategorySerializer, CategorySetActiveSerializer
from .models import Category


@extend_schema_view(
    list=extend_schema(
        summary="Listar categorías",
        description="Devuelve todas las categorías del usuario autenticado.",
        responses=CategorySerializer(many=True),
    ),
    retrieve=extend_schema(
        summary="Obtener categoría",
        description="Devuelve el detalle de una categoría del usuario.",
        responses=CategorySerializer,
    ),
    create=extend_schema(
        summary="Crear categoría",
        description=(
            "Crea una nueva categoría.\n\n"
            "La categoría se asocia automáticamente al usuario autenticado."
        ),
        responses=CategorySerializer,
    ),
    update=extend_schema(
        summary="Actualizar categoría",
        description="Actualiza completamente una categoría existente.",
        responses=CategorySerializer,
    ),
    partial_update=extend_schema(
        summary="Actualizar categoría parcialmente",
        description="Actualiza uno o más campos de una categoría.",
        responses=CategorySerializer,
    ),
    destroy=extend_schema(
        summary="Eliminar categoría",
        description="Elimina permanentemente una categoría del usuario.",
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Activar o desactivar categoría",
        description=(
            "Activa o desactiva una categoría sin modificar otros campos.\n\n"
            "Este endpoint solo modifica el estado `is_active`."
        ),
        request=CategorySetActiveSerializer,
        responses={
            200: CategorySerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            404: OpenApiResponse(description="Categoría no encontrada"),
        },
    )
    @action(methods=["PATCH"],detail=True,url_path="set-active",serializer_class=CategorySetActiveSerializer)
    def set_active(self, request, pk=None):
        category = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.is_active = serializer.validated_data["is_active"]
        category.save()

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_200_OK,
        )
