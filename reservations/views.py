from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView

from reservations.forms import CreateReservationModelForm, AddCourtModelForm
from reservations.models import TennisCourt, Reservations


class CourtsListView(ListView):
    template_name = 'courts.html'
    model = TennisCourt


class IndexListView(ListView):
    template_name = 'index.html'
    model = Reservations


class ReservedCourtsListView(LoginRequiredMixin, ListView):
    template_name = 'reserved_courts_list_views.html'
    model = Reservations


class ReservationSystemListView(LoginRequiredMixin, ListView):
    template_name = 'reservations_page.html'
    model = TennisCourt


class Login(ListView):
    template_name = 'login_main.html'
    model = TennisCourt


class Logout(ListView):
    template_name = 'logout.html'
    model = TennisCourt


class CreateReservationFormView(LoginRequiredMixin, FormView):
    template_name = 'reservation_form.html'
    form_class = CreateReservationModelForm
    success_url = reverse_lazy('reservations_urls:reserved_courts_list_views')

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result


class AddCourtFormView(LoginRequiredMixin, FormView):
    template_name = 'add_court_form.html'
    form_class = AddCourtModelForm
    success_url = reverse_lazy('reservations_urls:courts')

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result


#
# def get_name(request):
#     if request.method == 'POST':
#         form = DateForm(request.POST)
#     else:
#         form = DateForm()
#
#     return render(
#         request,
#         template_name='form.html',
#         context={'form': DateForm}
#     )
