from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  birth_date = models.DateField(null=True, blank=True)
  salary = models.IntegerField(null=True)
  possessions = models.IntegerField(null=True)
  is_mydata_agreed = models.BooleanField(default=False)
