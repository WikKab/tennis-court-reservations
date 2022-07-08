from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from clients.models import Profile
from django.views.generic import ListView
from django.contrib.auth.forms import User, UserCreationForm, UserChangeForm
from django.views.generic import CreateView, UpdateView, FormView
from django.urls import reverse_lazy


class ProfileView(ListView):
    template_name = 'profile_panel.html'
    model = Profile


class ProfileListView(ListView):
    template_name = 'user_profile.html'
    model = Profile


class UserReservationsView(ListView):
    template_name = 'user_reservations.html'
    model = Profile


class UserEditReservations(ListView):
    template_name = 'user_edit_reservations.html'
    model = Profile


class UserDeleteReservations(ListView):
    template_name = 'user_delete_reservations.html'
    model = Profile


class UserEditView(UpdateView):
    model = Profile
    template_name = 'user_edit_profile.html'
    form_class = UserChangeForm
    success_url = reverse_lazy("clients_urls:user_profile")

    def get_object(self):
        return self.request.user
