from  rest_framework import  viewsets

from wallet.models import Wallet
from wallet.serialziers import WalletSerializer


class WalletViewSets(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    http_method_names = ['get']
