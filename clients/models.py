from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=False)
    wallet = models.IntegerField(default=0)

    def updateUserProfile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    post_save.connect(updateUserProfile, sender=User)

    def __str__(self):
        return f'{self.user.username}'
