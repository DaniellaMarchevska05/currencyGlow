# api/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.IntegerField(default=1000)

    def __str__(self):
        return f"{self.user.username}'s balance: {self.balance}"


class CurrencyExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_requests')
    currency_code = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.currency_code} - {self.rate} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


# Create UserBalance automatically when a user is created
@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(user=instance)
