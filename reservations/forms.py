from datetime import date, datetime


import pandas as pd
from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    SelectDateWidget,
    Select,
    CheckboxSelectMultiple,
)
from django import forms
from django.utils.translation import gettext_lazy as _

from reservations.models import Reservations, TennisCourt

RENT_TIME = [
    ('8.00', '8.00'),
    ('8.30', '8.30'),
    ('9.00', '9.00'),
    ('9.30', '9.30'),
    ('10.00', '10.00'),
    ('10.30', '10.30'),
    ('11.00', '11.00'),
    ('11.30', '11.30'),
    ('12.00', '12.00'),
    ('12.30', '12.30'),
    ('13.00', '13.00'),
    ('13.30', '13.30'),
    ('14.00', '14.00'),
    ('14.30', '14.30'),
    ('15.00', '15.00'),
    ('15.30', '15.30'),
    ('16.30', '16.00'),
    ('17.00', '17.00'),
    ('17.30', '17.30'),
    ('18.00', '18.00'),
    ('18.30', '18.30'),
    ('19.00', '19.00'),
    ('19.30', '19.30'),
    ('20.00', '20.00'),
    ('20.30', '20.30'),
    ('21.00', '21.00'),
    ('21.30', '21.30'),
    ('22.00', '22.00'),
]

def hour_range(open_hour, close_hour):
    datelist = pd.date_range(start=str(open_hour), end=str(close_hour),
                             freq='0.5H').to_pydatetime().tolist()
    renting_time = []
    for hours in datelist:
        hour = str(hours)[11:16]
        renting_time.append((hour, hour))
    # renting_time = []
    # if open_hour[-5] == '3':
    #     renting_time.append((open_hour, open_hour))
    # for hours in range(int(open_hour[:2]), int(close_hour[:2]) + 1):
    #     if hours == int(close_hour[:2]) and close_hour[-5] == '0':
    #         renting_time.append((str(hours) + ':00', str(hours) + ':00'))
    #     else:
    #         renting_time.append((str(hours) + ':00', str(hours) + ':00'))
    #         renting_time.append((str(hours) + ':30', str(hours) + ':30'))
    return renting_time

class CreateReservationModelForm(ModelForm):
    rez_start = Reservations.reservation_start
    rez_end = Reservations.reservation_end

    def clean(self):
        cleaned_data = super().clean()
        rez_start = cleaned_data.get('reservation_start')
        rez_end = cleaned_data.get('reservation_end')

        if rez_end < rez_start:
            raise ValidationError(f'WARNING!!! Reservation end time you have chosen is lower than '
                                  f'start of your reservation. Change reservation finish time.')
        if rez_end == rez_start:
            raise ValidationError(f'WARNING!!! Reservation start and end time are the same. '
                                  f' Change reservation time.')
        return cleaned_data

    class Meta:
        model = Reservations
        fields = [
            'court',
            'reservation_date',
            'reservation_start',
            'reservation_end',
        ]
        widgets = {
            'reservation_date': SelectDateWidget(
                empty_label=("Choose Day", "Choose Month", "Choose Year")),
            'reservation_start': forms.Select(choices=RENT_TIME),
            'reservation_end': Select(choices=RENT_TIME),
        }

        help_texts = {'reservation_start': _('( hh.mm )'),
                      'reservation_end': _('( hh.mm )'),
                      }


class CreateReservationWithSelectedCourtForm(ModelForm):
    rez_start = Reservations.reservation_start
    rez_end = Reservations.reservation_end

    def clean(self):
        cleaned_data = super().clean()
        rez_start = cleaned_data.get('reservation_start')
        rez_end = cleaned_data.get('reservation_end')

        if rez_end < rez_start:
            raise ValidationError(f'WARNING!!! '
                                  f'Reservation end time you have chosen is before your reservation '
                                  f'starts. Change reservation start or end time.')
        if rez_end == rez_start:
            raise ValidationError(f'WARNING!!! Reservation start and end time are the same. '
                                  f' Change reservation start or end time.')
        return cleaned_data

    class Meta:
        model = Reservations
        fields = [
            'reservation_date',
            'reservation_start',
            'reservation_end',
        ]
        widgets = {
            'reservation_date': SelectDateWidget(
                empty_label=("Choose Day", "Choose Month", "Choose Year")),
            'reservation_start': forms.Select(choices=RENT_TIME),
            'reservation_end': Select(choices=RENT_TIME),
        }

        help_texts = {'reservation_start': _('( hh.mm )'),
                      'reservation_end': _('( hh.mm )'),
                      }


class CreateExactReservationModelForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.court = kwargs.pop('court')
        super().__init__(*args, **kwargs)

        self.fields['reservation_start'].choices = hour_range(self.court.open_hour, self.court.close_hour)
        self.fields['reservation_end'].choices = hour_range(self.court.open_hour, self.court.close_hour)
        if self.court.equipment_rent:
            self.fields['rent_of_equipment'] = forms.BooleanField(required=False)
        else:
            self.fields['rent_of_equipment'] = forms.BooleanField(disabled=True, required=False)


    reservation_date = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Choose Day", "Choose Month", "Choose Year")))
    reservation_start = forms.ChoiceField(help_text='( hh.mm )', choices=())
    reservation_end = forms.ChoiceField(help_text='( hh.mm )', choices=())

    def clean(self):
        result = super().clean()
        if not self.errors:
            if result["reservation_date"] < date.today() or \
                ((result["reservation_date"] == date.today() and
                    int(result["reservation_start"][:2]) < int(str(datetime.now())[11:13]))):
                raise ValidationError("You can't make reservation in the past!")
            if int(result["reservation_start"][:2]) > int(result["reservation_end"][:2]):
                self.add_error("reservation_start", "Start time should be earlier than end.")
                self.add_error("reservation_end", "End time should be later than start.")
                raise ValidationError("Reservation can't end before it even started!")
            if int(result["reservation_start"][:2]) == int(result["reservation_end"][:2]) and \
               int(result["reservation_start"][4:6]) == int(result["reservation_end"][4:6]):
                raise ValidationError("Reservation should be at least half hour long!")
            if Reservations.objects.filter(reservation_date=result["reservation_date"],
                                           reservation_start__lt=result["reservation_end"],
                                           reservation_end__gt=result["reservation_start"],
                                           ).exists():
                raise ValidationError("Already exists reservation at that time! Choose another time.")
        return result

# class ConfirmReservationForm(forms.Form):
#     reservation = forms.ModelChoiceField(queryset=None)
#     def __init__(self, *args, **kwargs):
#         reservation = kwargs.pop('reservation')
#
#         super().__init__(*args, **kwargs)
#         self.fields['reservation'] = reservation
#         print(self.fields)





class AddCourtModelForm(ModelForm):
    class Meta:
        model = TennisCourt
        # fields = '__all__'
        exclude = ['reservation_status']
        widgets = {
            'open_hour': forms.Select(choices=RENT_TIME),
            'close_hour': Select(choices=RENT_TIME),
        }

        help_texts = {'open_hour': '( hh.mm )',
                      'close_hour': '( hh.mm )',
                      }


class DeleteCourtForm(ModelForm):
    class Meta:
        model = Reservations
        fields = ['court']
        widgets = {
            'court': CheckboxSelectMultiple
        }


class CourtsParamsEditForm(ModelForm):
    class Meta:
        model = TennisCourt
        # fields = '__all__'
        exclude = ['reservation_status']
        widgets = {
            'open_hour': forms.Select(choices=RENT_TIME),
            'close_hour': Select(choices=RENT_TIME),
        }

        help_texts = {'open_hour': _('( hh.mm )'),
                      'close_hour': _('( hh.mm )'),
                      }


class ReservationsParamsEditForm(ModelForm):
    class Meta:
        model = Reservations
        fields = [
            'court',
            'reservation_date',
            'reservation_start',
            'reservation_end',
        ]
        widgets = {
            'reservation_date': SelectDateWidget(
                empty_label=("Choose Day", "Choose Month", "Choose Year")),
            'reservation_start': forms.Select(choices=RENT_TIME),
            'reservation_end': Select(choices=RENT_TIME),
        }

        help_texts = {'reservation_start': _('( hh.mm )'),
                      'reservation_end': _('( hh.mm )'),
                      }


if __name__ == '__main__':
    pass
