from django.db import models



class TennisCourt(models.Model):
    CITY = [
        ("Kraków", "Kraków"),
        ("Poznań", "Poznań"),
        ("Warszawa", "Warszawa"),
        ("Olsztyn", "Olsztyn"),
        ("Wrocław", "Wrocaław"),
    ]

    name = models.CharField(max_length=64)
    open_hour = models.TimeField()
    close_hour = models.TimeField()
    hire_price = models.IntegerField()
    city = models.CharField(choices=CITY, max_length=24)
    adress = models.CharField(max_length=128)
    equipment_rent = models.BooleanField()

    def __str__(self):
        return f'{self.city} / {self.name}'


class Reservations(models.Model):
    RENT_TIME = [
        ('08:00:00', '8:00:00'),
        ('08:30:00', '8:30:00'),
        # ('9.00'),
        # ('4', '9.30'),
        # ('5', '10.00'),
        # ('6', '10.30'),
        # ('7', '11.00'),
        # ('8', '11.30'),
        # ('9', '12.00'),
        # ('10', '12.30'),
        # ('11', '13.00'),
        # ('12', '13.30'),
        # ('13', '14.00'),
        # ('14', '14.30'),
        # ('15', '15.00'),
        # ('16', '15.30'),
        # ('17', '16.00'),
        # ('18', '17.00'),
        # ('19', '17.30'),
        # ('20', '18.00'),
        # ('21', '18.30'),
        # ('22', '19.00'),
        # ('23', '19.30'),
        # ('24', '20.00'),
        # ('25', '20.30'),
        # ('26', '21.00'),
    ]

    object = models.ForeignKey(
        TennisCourt, on_delete=models.CASCADE, related_name="reservations", blank=False, null=False
    )
    reservation_date = models.DateField()
    reservation_start = models.TimeField()
    reservation_end = models.TimeField()
    # reservation_start = models.TimeField(choices=RENT_TIME)
    # reservation_end = models.TimeField(choices=RENT_TIME)

    # reservation_status = models.BooleanField(default=False)
    # reservation_cost = models.IntegerField()

    def __str__(self):
        return f'{self.object}'


if __name__ == '__main__':
    pass
