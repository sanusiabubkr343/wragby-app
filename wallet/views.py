from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from wallet.models import Wallet
from wallet.serialziers import WalletSerializer, CreateWalletSerializer, FundWalletSerializer


class WalletViewSets(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateWalletSerializer
        elif self.action == 'fund':
            return FundWalletSerializer
        return WalletSerializer

    @action(detail=False, methods=['post'], url_path='fund')
    def fund(self, request):
        """
        Fund a wallet with a specified amount.
        """
        serializer = FundWalletSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
