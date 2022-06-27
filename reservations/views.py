from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DeleteView, DetailView
from reservations.forms import CreateReservationModelForm, AddCourtModelForm, DeleteCourtForm
from reservations.models import TennisCourt, Reservations, AdminPanel
from django.contrib.auth.mixins import PermissionRequiredMixin


class CourtsListView(ListView):
    template_name = 'courts.html'
    model = TennisCourt


class CourtsListDetailView(ListView):
    template_name = 'courts_details.html'
    model = TennisCourt

    ordering = 'city'

    # def get_ordering(self):
    #     return self.request.GET.get(
    #         ('o', 'city')
    #     )
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.ordered(

class CourtDetailView(DetailView):
    model = TennisCourt
    template_name = 'court_exact_detail.html'


class IndexListView(ListView):
    template_name = 'index.html'
    model = Reservations


class ReservedCourtsListView(LoginRequiredMixin, ListView):
    template_name = 'reserved_courts_list_views.html'
    model = Reservations


class ReservedCourtsDetailsView(LoginRequiredMixin, ListView):
    template_name = 'reserved_courts_details_views.html'
    model = Reservations
    ordering = 'court_object'


class ReservationSystemListView(LoginRequiredMixin, ListView):
    template_name = 'reservations_page.html'
    model = TennisCourt


class Login(ListView):
    template_name = 'login_main.html'
    model = TennisCourt


class Logout(ListView):
    template_name = 'logout.html'
    model = TennisCourt


class AdminPanel(ListView):
    template_name = 'admin_panel.html'
    model = AdminPanel


class CreateReservationFormView(LoginRequiredMixin, FormView):
    template_name = 'reservation_form.html'
    form_class = CreateReservationModelForm
    success_url = reverse_lazy('reservations_urls:reserved_courts_list_views')

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result

# class CreateExactCourtReservationFormView(FormView):
#     template_name = 'reservation_form.html'
#     form_class = CreateReservationModelForm
#     success_url = reverse_lazy('reservations_urls:reserved_courts_list_views')
#
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         form.save()
#         return result

class AddCourtFormView(PermissionRequiredMixin, FormView):
    permission_required = 'reservations_urls:add-court'
    permission_denied_message = 'You do not have permissions to do it.'

    template_name = 'add_court_form.html'
    form_class = AddCourtModelForm
    success_url = reverse_lazy('reservations_urls:add-court')

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result

    def get_test_func(self):
        return self.request.user.username.startwith('admin')


class CourtsListDetailAdminView(ListView):  # task.list.view
    template_name = 'delete_court_admin_view.html'  # list.html          delete_court_admin_view.html
    model = TennisCourt
    context_object_name = 'court_object'


class DeleteCourtView(DeleteView):  # task.delete.view
    model = TennisCourt
    template_name = 'delete_court.html'  # delete.html        delete_court.html
    context_object_name = 'court_object'
    success_url = reverse_lazy('reservations_urls:courts-detail-admin')

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
#
