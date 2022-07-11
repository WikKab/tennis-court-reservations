from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404

from clients.models import Profile
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.forms import User, UserCreationForm, UserChangeForm
from django.views.generic import CreateView, UpdateView, FormView
from django.urls import reverse_lazy

from reservations.forms import ReservationsParamsEditForm
from reservations.models import Reservation
from .forms import EditProfileForm


class ProfileView(ListView):
    template_name = 'profile_panel.html'
    model = Profile


class UserReservationsView(ListView):
    template_name = 'user_reservations.html'
    model = Reservation

    def get_queryset(self):
        return self.request.user.reservation_set.all()


class UserEditReservations(FormView, UpdateView):
    template_name = 'user_edit_reservations.html'
    model = Reservation
    # fields = '__all__'
    form_class = ReservationsParamsEditForm
    success_url = reverse_lazy("clients_urls:user_reservations.html")


class UserEditReservationsView(ListView):
    template_name = 'user_edit_reservations_view.html'
    model = Reservation
    ordering = 'reservation_date'

    def get_queryset(self):
        return self.request.user.reservations_set.all()


class UserDeleteReservationsList(ListView):
    template_name = 'user_delete_reservations_view.html'
    model = Reservation
    ordering = 'reservation_date'

    def get_queryset(self):
        return self.request.user.reservations_set.all()


class UserDeleteReservations(DeleteView):
    template_name = 'user_delete_reservations.html'
    model = Reservation
    success_url = reverse_lazy("clients_urls:profile_panel")


class UserEditView(UpdateView, FormView):
    model = Profile
    template_name = 'user_edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy("clients_urls:profile_panel")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result



       # Profile.objects.create(user=user, wallet=wallet, unit_payment=unitpayment)

    # def get_context_data(self, *args, **kwargs):
    #     user = Profile.objects.all()
    #     context = super(ProfileListView, self).get_context_data(*args, **kwargs)
    #     user_page = get_object_or_404(Profile, id=self.kwargs['pk'])
    #
    #     context['user_profile'] = user_page
    #     return context
    # wallet = form.cleaned_data["wallet"]
    # unit_payment = form.cleaned_data["unit_payment"]
    # Profile.objects.create(wallet=wallet, unit_payment=unit_payment)