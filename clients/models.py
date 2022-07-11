from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=False)
    wallet = models.IntegerField(default=0)
    unit_payment = models.IntegerField(default=0)

    def updateUserProfile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    post_save.connect(updateUserProfile, sender=User)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super(Reservations, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
    #     r_end = self.reservation_end.time()
    #     r_start = self.reservation_start.time()
    #     t = strptime(str(self.reservation_end), "%H:%M")
    #     start_hour = int(str(self.reservation_start)[:1])
    #     start_minute = int(str(self.reservation_start)[3:4])
    #     end_hour = int(str(self.reservation_end)[:1])
    #     end_minute = int(str(self.reservation_end)[3:4])
    #
    #     self.reservation_cost = self.court.hire_price * ((end_hour * 60 + end_minute - start_hour * 60
    #                                                       - start_minute) / 30) + self.court.equipment_cost
