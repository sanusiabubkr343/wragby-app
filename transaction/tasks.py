from celery import shared_task
from django.db import transaction as db_transaction
from wallet.models import Wallet
from transaction.models import Transaction


@shared_task
def perform_transaction_task(transaction_id, sender_wallet_id, recipient_wallet_id, amount):
    """
    Background task to perform wallet transaction
    """
    transaction_obj = None
    try:
        transaction_obj = Transaction.objects.get(id=transaction_id)
        sender_wallet = Wallet.objects.get(id=sender_wallet_id)
        recipient_wallet = Wallet.objects.get(id=recipient_wallet_id)

        with db_transaction.atomic():
            # Update wallet balances
            sender_wallet.balance -= amount
            sender_wallet.save()
            recipient_wallet.balance += amount
            recipient_wallet.save()

            # Update user wallet_balances
            sender_user = sender_wallet.user
            sender_user.wallet_balance -= amount
            sender_user.save()

            recipient_user = recipient_wallet.user
            recipient_user.wallet_balance += amount
            recipient_user.save()

            # Update transaction status to completed
            transaction_obj.status = 'successful'
            transaction_obj.save()

        return True
    except Exception as e:
        # Update transaction status to failed
        if transaction_obj:
            transaction_obj.status = 'failed'
            transaction_obj.save()
        raise e
