from rest_framework import serializers
from django.db import transaction as db_transaction
from wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class CreateWalletSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Wallet
        fields = ('user', 'id')


class FundWalletSerializer(serializers.Serializer):
    wallet_id = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all(), required=True)
    amount = serializers.FloatField(required=True, min_value=0.01)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

    def create(self, validated_data):
        wallet = validated_data.get('wallet_id')
        amount = validated_data.get('amount')

        with db_transaction.atomic():
            # Update wallet balance
            wallet.balance += amount
            wallet.save()

            # Update user wallet_balance
            user = wallet.user
            user.wallet_balance += amount
            user.save()

        return {
            "message": "Wallet funded successfully",
            "success": True,
            "wallet_id": wallet.id,
            "new_balance": wallet.balance,
            "user_wallet_balance": user.wallet_balance,
        }