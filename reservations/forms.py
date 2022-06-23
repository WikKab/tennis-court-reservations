from django.forms import ModelForm

from reservations.models import Reservations, TennisCourt


class CreateReservationModelForm(ModelForm):
    class Meta:
        model = Reservations
        # fields = '__all__'
        exclude = ['reservation_cost', 'reservation_status']

    # def form_valid(self, form):
    #     result = super().form_valid(form)
    #     form.save()
    #     return result


class AddCourtModelForm(ModelForm):
    class Meta:
        model = TennisCourt
        # fields = '__all__'
        exclude = ['reservation_status']






if __name__ == '__main__':
    pass
