from  rest_framework import viewsets

from transaction.models import Transaction
from transaction.serializers import PerformTransferSerializer
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = PerformTransferSerializer
    http_method_names = ['post']
