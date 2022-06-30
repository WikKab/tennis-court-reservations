# import pandas as pd
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
RENT_TIME_2 = [
    ('8:00', '8:00'),
    ('8:30', '8:30'),
    ('9:00', '9:00'),
    ('9:30', '9:30'),
    ('10:00', '10:00'),
    ('10:30', '10:30'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('12:00', '12:00'),
    ('12:30', '12:30'),
    ('13:00', '13:00'),
    ('13:30', '13:30'),
    ('14:00', '14:00'),
    ('14:30', '14:30'),
    ('15:00', '15:00'),
    ('15:30', '15:30'),
    ('16:30', '16:00'),
    ('17:00', '17:00'),
    ('17:30', '17:30'),
    ('18:00', '18:00'),
    ('18:30', '18:30'),
    ('19.00', '19:00'),
    ('19:30', '19:30'),
    ('20:00', '20:00'),
    ('20:30', '20:30'),
    ('21:00', '21:00'),
    ('21:30', '21:30'),
    ('22:00', '22:00'),
]


def rez_date_validator(value):
    start = Reservations.reservation_start
    end = Reservations.reservation_end


class CreateReservationModelForm(ModelForm):
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


class CreateExactReservationModelForm(forms.Form):
    reservation_date = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Choose Day", "Choose Month", "Choose Year")))
    # datelist = pd.date_range(start=TennisCourt.open_hour, end=TennisCourt.close_hour,
    #                          freq='0.5H').to_pydatetime().tolist()
    # renting_time = []
    # for hours in datelist:
    #     hour = str(hours)[11:16]
    #     renting_time.append((hour, hour))
    # k =[
    #  (str(TennisCourt.open_hour), TennisCourt.open_hour),
    #   (TennisCourt.close_hour, TennisCourt.close_hour),
    # ]

    reservation_start = forms.ChoiceField(help_text='( hh.mm )', choices=RENT_TIME_2)
    # reservation_start = forms.ChoiceField(choices=RENT_TIME)
    reservation_end = forms.ChoiceField(help_text='( hh.mm )', choices=RENT_TIME_2)
    #
    # help_texts = {'reservation_start': _('( hh.mm )'),
    #               'reservation_end': _('( hh.mm )'),
    #               }


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
