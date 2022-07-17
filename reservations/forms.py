from datetime import date, datetime

import pandas as pd
from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    Select,
    CheckboxSelectMultiple,
)
from django import forms
from django.utils.translation import gettext_lazy as _

from reservations.models import Reservation, TennisCourt


def hour_range(open_hour, close_hour):
    datelist = pd.date_range(start=str(open_hour), end=str(close_hour),
                             freq='0.5H').to_pydatetime().tolist()
    renting_time = []
    for hours in datelist:
        hour = str(hours)[11:16]
        renting_time.append((hour, hour))
    return renting_time


def hour_range_model_form(open_hour, close_hour):
    datelist = pd.date_range(start=str(open_hour), end=str(close_hour),
                             freq='0.5H').to_pydatetime().tolist()
    renting_time = []
    for hours in datelist:
        hour = str(hours)[11:13] + '.' + str(hours)[14:16]
        renting_time.append((hour, hour))
    return renting_time



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
                    int(result["reservation_start"][3:5]) == int(result["reservation_end"][3:5]):
                raise ValidationError("Reservation should be at least half hour long!")
            if Reservation.objects.filter(reservation_date=result["reservation_date"],
                                          reservation_start__lt=result["reservation_end"],
                                          reservation_end__gt=result["reservation_start"],
                                          ).exists():
                raise ValidationError("Already exists reservation at that time! Choose another time.")
        return result


class ConfirmReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'


class AddCourtModelForm(ModelForm):
    class Meta:
        model = TennisCourt
        exclude = ['reservation_status']
        widgets = {
            'open_hour': forms.Select(choices=hour_range_model_form('06:00:00', '23:00:00')),
            'close_hour': Select(choices=hour_range_model_form('06:00:00', '23:00:00')),
            'short_description': forms.Textarea()
        }

        help_texts = {'open_hour': '( hh.mm )',
                      'close_hour': '( hh.mm )',
                      }


class DeleteCourtForm(ModelForm):
    class Meta:
        model = Reservation
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
            'open_hour': forms.Select(choices=hour_range_model_form('06:00:00', '23:00:00')),
            'close_hour': Select(choices=hour_range_model_form('06:00:00', '23:00:00')),
            'short_description': forms.Textarea()
        }

        help_texts = {'open_hour': _('( hh.mm )'),
                      'close_hour': _('( hh.mm )'),
                      }

