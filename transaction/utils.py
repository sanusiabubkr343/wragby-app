from  django.db import transaction as db_transaction

from wallet.models import Wallet


def perform_transaction(sender_wallet_id, recipient_wallet_id, amount):
    sender_wallet= Wallet.objects.get(id=sender_wallet_id)
    recipient_wallet= Wallet.objects.get(id=recipient_wallet_id)
    with db_transaction.atomic():
        sender_wallet.balance -= amount
        sender_wallet.save()
        recipient_wallet.balance += amount
        recipient_wallet.save()

    return True
