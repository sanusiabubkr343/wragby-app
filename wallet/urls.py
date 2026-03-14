from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wallet.views import WalletViewSets

router = DefaultRouter()
router.register(r'wallets', WalletViewSets, basename='wallet')

urlpatterns = [
    path('', include(router.urls)),
]
