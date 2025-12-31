from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, CategorySetActiveSerializer
from .models import Category

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["PATCH"],detail=True,url_path="set-active",serializer_class=CategorySetActiveSerializer)
    def set_active(self, request, pk=None):
        """
        Activa o desactiva una categoría.
        """
        category = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.is_active = serializer.validated_data["is_active"]
        category.save()

        return Response(
            self.get_serializer(category).data,
            status=status.HTTP_200_OK
        )