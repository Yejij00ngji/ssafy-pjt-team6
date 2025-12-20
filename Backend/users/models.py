from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from products.models import DepositOptions, DepositProducts

# Create your models here.
class User(AbstractUser):
  # email = models.EmailField(null=True)
  # nickname = models.CharField(null=True)
  birth_date = models.DateField(null=True, blank=True)
  salary = models.IntegerField(null=True)
  possessions = models.IntegerField(null=True)
  is_mydata_agreed = models.BooleanField(default=False)

class Subscription(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='subscriptions'
  )

  deposit_option = models.ForeignKey(
    'products.DepositOptions',
    on_delete=models.CASCADE,
    related_name='subscribers'
  )

  amounts = models.BigIntegerField(default=0)

  subscribed_at = models.DateField(auto_now_add=True)
  expired_at = models.DateField(null=True, blank=True)

  class Meta:
    unique_together = ('user', 'deposit_option')