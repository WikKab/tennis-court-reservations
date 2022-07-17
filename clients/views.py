from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.views.generic import UpdateView, FormView

from clients.models import Profile
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


class UserEditView(UpdateView, FormView):
    model = Profile
    template_name = 'user_edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy("clients_urls:profile-panel")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result


class ProfileListView(ListView):
    template_name = 'profile_list_view.html'
    model = Profile
