from django.forms import ModelForm, SelectDateWidget, Select
from django import forms
from django.utils.translation import gettext_lazy as _

from reservations.models import Reservations, TennisCourt


class CreateReservationModelForm(ModelForm):
    class Meta:
        model = Reservations
        fields = [
            'object',
            'reservation_date',
            'reservation_start',
            'reservation_end',
        ]
        widgets = {
            'reservation_date': SelectDateWidget(
                empty_label=("Choose Day", "Choose Month", "Choose Year")),
            # 'reservation_start': Select,
            # 'reservation_end': Select,
        }

        help_texts = {'reservation_start': _('( hh.mm )'),
                      'reservation_end': _('( hh.mm )'),
                      }

        # error_messages = {
        #     'reservation_start': _("Wrong time format input. Use hh.mm format."),
        # }


class AddCourtModelForm(ModelForm):
    class Meta:
        model = TennisCourt
        # fields = '__all__'
        exclude = ['reservation_status']


if __name__ == '__main__':
    pass
