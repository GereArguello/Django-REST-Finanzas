from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer
from .models import Transaction
from utils.choices import CategoryType

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)

        account = transaction.account

        if transaction.category.category_type == CategoryType.INCOME:
            account.balance += transaction.amount
        else:
            account.balance -= transaction.amount

        account.save()

