from django.db import models

# Create your models here.


class Transaction(models.Model):


  status_choices = (
      ('pending', 'pending'),
      ('successful', 'successful'),
      ('failed', 'failed'),
  )

  id = models.AutoField(primary_key=True)
  sender =models.ForeignKey('user.User',on_delete=models.PROTECT,related_name='sender_transactions')
  receiver = models.ForeignKey('user.User',on_delete=models.PROTECT,related_name='receiver_transactions')
  amount = models.FloatField()
  status = models.CharField(max_length=20,choices=status_choices,default='pending')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
      ordering = ['-created_at']

  def __str__(self):
      return self.sender_id

