from django.contrib.messages.api import success
from  rest_framework import serializers

from transaction.models import Transaction
from transaction.utils import perform_transaction
from wallet.models import Wallet
from  django.db import transaction as db_transaction



class PerformTransferSerializer(serializers.Serializer):
    recipient_wallet_id = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all(),required=True)
    sender_wallet_id = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all(),required=True)
    amount = serializers.FloatField(required=True,min_value=0)


    def validate(self, data):
        sender_wallet :Wallet= data.get('sender_wallet_id')
        recipient_wallet :Wallet= data.get('recipient_wallet_id')
        if sender_wallet.balance < data.get('amount'):
            raise serializers.ValidationError({"balance": "Insufficient balance"})

        if recipient_wallet == sender_wallet:
            raise serializers.ValidationError({"recipient": "Sender and recipient cannot be the same"})

        data["sender_wallet"]=sender_wallet
        data["recipient_wallet"]=recipient_wallet
        data["sender"]=sender_wallet.user
        data["receiver"]=recipient_wallet.user

        return data

    def create(self, validated_data):
        amount=validated_data.get('amount')
        sender_wallet=validated_data.get('sender_wallet')
        recipient_wallet=validated_data.get('recipient_wallet')
        with db_transaction.atomic():
            Transaction.objects.create(
                sender=validated_data.get('sender'),
                receiver=validated_data.get('receiver'),
                amount=validated_data.get('amount'),
                status='pending'
            )

            sender_wallet_id=sender_wallet.id
            recipient_wallet=recipient_wallet.id
        initiated_tx =perform_transaction(sender_wallet_id,recipient_wallet,amount)

        if not initiated_tx:
            return{
                "message": "Transaction failed",
                "success": False,
            }
        return {
            "message": "Transaction initiated successfully",
            "success": True,
        }



