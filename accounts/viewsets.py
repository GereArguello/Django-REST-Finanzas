from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer, AccountSetActiveSerializer
from .models import Account

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(methods=["PATCH"],detail=True,url_path="set-active",serializer_class=AccountSetActiveSerializer)
    def set_active(self, request, pk=None):
        """
        Activa o desactiva una cuenta.
        """
        account = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account.is_active = serializer.validated_data["is_active"]
        account.save()

        return Response(
            self.get_serializer(account).data,
            status=status.HTTP_200_OK
        )
