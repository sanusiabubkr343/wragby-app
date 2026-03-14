from django.db import models

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField('user.User',on_delete=models.PROTECT,related_name='user_wallet')
    balance = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Wallet for {self.user.username}"