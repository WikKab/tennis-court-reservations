from time import strptime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime


class TennisCourt(models.Model):
    CITY = [
        ("Białystok", "Białystok"),
        ("Gdańsk", "Gdańsk"),
        ("Kraków", "Kraków"),
        ('Lublin', 'Lublin'),
        ("Olsztyn", "Olsztyn"),
        ("Poznań", "Poznań"),
        ("Warszawa", "Warszawa"),
        ("Wrocław", "Wrocław"),
    ]

    city = models.CharField(choices=CITY, max_length=24)
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    open_hour = models.TimeField()
    close_hour = models.TimeField()
    hire_price = models.IntegerField()
    equipment_rent = models.BooleanField()
    equipment_cost = models.IntegerField(default=0)
    short_description = models.CharField(max_length=1024, default='')

    def __str__(self):
        return f'{self.city} - {self.name} - {self.address}'


class Reservations(models.Model):
    court = models.ForeignKey(
        TennisCourt,
        on_delete=models.CASCADE,
        related_name="reservations",
        blank=False,
        null=False
    )

    reservation_date = models.DateField()
    reservation_start = models.TimeField()
    reservation_end = models.TimeField()
    client = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, blank=False, null=False)

    reservation_cost = models.IntegerField(default=0)
# z timefiled na datetime
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Reservations, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        # r_end = self.reservation_end.time()
        # r_start = self.reservation_start.time()
        # t = strptime(str(self.reservation_end), "%H:%M")
        start_hour = int(str(self.reservation_start)[:1])
        start_minute = int(str(self.reservation_start)[3:4])
        end_hour = int(str(self.reservation_end)[:1])
        end_minute = int(str(self.reservation_end)[:1])

        self.reservation_cost = self.court.hire_price * ((end_hour * 60 + end_minute - start_hour * 60 + start_minute) / 30)

    def __str__(self):
        return f'{self.court}'

#osobna apka
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=False)
    wallet = models.IntegerField(default=0)
    unit_payment = models.IntegerField(default=0)


class AdminPanel(models.Model):
    pass


if __name__ == '__main__':
    pass
