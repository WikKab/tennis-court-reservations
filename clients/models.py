from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=False)
    wallet = models.IntegerField(default=0)
    unit_payment = models.IntegerField(default=0)