from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, FormView, DeleteView, DetailView, UpdateView
from reservations.models import TennisCourt, Reservations, AdminPanel
from reservations.forms import (
    CreateReservationModelForm,
    AddCourtModelForm,
    CreateExactReservationModelForm,
    CourtsParamsEditForm,
    ReservationsParamsEditForm,
    CreateReservationWithSelectedCourtForm,
)


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
    ordering = '-reservation_date'


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
    success_url = reverse_lazy('reservations_urls:reserved_courts_details_views')

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result


class CreateReservationCourtSelect(LoginRequiredMixin, ListView):
    model = TennisCourt
    template_name = 'reservation_court_selection.html'
    ordering = 'city'


class CreateReservationWithSelectedCourt(LoginRequiredMixin, FormView):
    template_name = 'reservation_with_selected_court.html'
    form_class = CreateReservationWithSelectedCourtForm
    success_url = reverse_lazy('reservations_urls:reserved_courts_details_views')

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result


class CreateExactCourtReservationFormView(View):
    # template_name = 'exact_reservation_form.html'
    # form_class = CreateExactReservationModelForm
    # success_url = reverse_lazy('reservations_urls:reserved_courts_list_views')

    def get(self, request, pk):
        return render(
            request,
            template_name='exact_reservation_form.html',
            context={"form": CreateExactReservationModelForm()}
        )

    def post(self, request, pk):
        form = CreateExactReservationModelForm(request.POST or None)
        if form.is_valid():
            court = get_object_or_404(TennisCourt, pk=pk)
            reservation_date = form.cleaned_data["reservation_date"]
            reservation_start = form.cleaned_data["reservation_start"]
            reservation_end = form.cleaned_data["reservation_end"]
            Reservations.objects.create(court=court,
                                        reservation_date=reservation_date,
                                        reservation_start=reservation_start,
                                        reservation_end=reservation_end
                                        )
            return HttpResponseRedirect(reverse("reservations_urls:reserved_courts_list_views"))
        return render(
            request,
            template_name="exact_reservation_form.html",
            context={"form": form}
        )


class AddCourtFormView(PermissionRequiredMixin, FormView):
    permission_required = 'reservations_urls:add-court'
    # # permission_denied_message = 'You do not have permissions to do it.'

    template_name = 'add_court_form.html'
    form_class = AddCourtModelForm
    success_url = reverse_lazy('reservations_urls:add-court')

    def form_valid(self, form):
        result = super().form_valid(form)
        form.save()
        return result

    def get_test_func(self):
        return self.request.user.username.startwith('admin')


class CourtsListDetailAdminView(ListView):
    template_name = 'delete_court_admin_view.html'
    model = TennisCourt
    context_object_name = 'object2'
    ordering = 'city'


class DeleteCourtView(DeleteView):
    model = TennisCourt
    template_name = 'delete_court.html'
    context_object_name = 'object2'
    success_url = reverse_lazy('reservations_urls:courts-detail-admin')


class CourtParamsEdit(FormView, UpdateView):
    model = TennisCourt
    # fields = '__all__'
    template_name = 'courts_params_edit.html'
    form_class = CourtsParamsEditForm
    success_url = reverse_lazy('reservations_urls:courts-params-edit-view')


class CourtsParamsEditView(ListView):
    template_name = 'courts_params_edit_view.html'
    model = TennisCourt
    ordering = 'city'


class ReservationsParamsEdit(FormView, UpdateView):
    model = Reservations
    # fields = '__all__'
    template_name = 'reservations_params_edit.html'
    form_class = ReservationsParamsEditForm
    success_url = reverse_lazy('reservations_urls:reservations-params-edit-view')


class ReservationsParamsEditView(ListView):
    template_name = 'reservations_params_edit_view.html'
    model = Reservations
    ordering = 'reservation_date'


class ReservationsListDetailAdminView(ListView):
    template_name = 'reservations_delete_admin_view.html'
    model = Reservations
    ordering = 'reservation_date'


class DeleteReservation(DeleteView):
    model = Reservations
    template_name = 'reservation_delete.html'
    success_url = reverse_lazy('reservations_urls:reservations-details')
