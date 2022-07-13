from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, FormView, DeleteView, DetailView, UpdateView
from reservations.models import TennisCourt, Reservation, AdminPanel
from reservations.forms import (
    CreateReservationModelForm,
    AddCourtModelForm,
    CreateExactReservationModelForm,
    CourtsParamsEditForm,
    ReservationsParamsEditForm,
    CreateReservationWithSelectedCourtForm,
    ConfirmReservationForm,
)


class CourtsListView(ListView):
    template_name = 'courts.html'
    model = TennisCourt


class CourtsListDetailView(ListView):
    template_name = 'courts_details.html'
    model = TennisCourt

    ordering = 'city'


class CourtDetailView(DetailView):
    model = TennisCourt
    template_name = 'court_exact_detail.html'


class IndexListView(ListView):
    template_name = 'index.html'
    model = Reservation


class ReservedCourtsListView(LoginRequiredMixin, ListView):
    template_name = 'reserved_courts_list_views.html'
    model = Reservation


class ReservedCourtsDetailsView(LoginRequiredMixin, ListView):
    template_name = 'reserved_courts_details_views.html'
    model = Reservation
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


class CreateExactCourtReservation(View):
    def get(self, request, pk):
        court = get_object_or_404(TennisCourt, pk=pk)
        return render(
            request,
            template_name='exact_reservation_form.html',
            context={'form': CreateExactReservationModelForm(court=court), 'my_court': court}
        )

    def post(self, request, pk):
        if 'reservation_cost' not in request.POST:
            court = get_object_or_404(TennisCourt, pk=pk)
            form = CreateExactReservationModelForm(request.POST, court=court)
            if form.is_valid():
                reservation_date = form.cleaned_data["reservation_date"]
                reservation_start = form.cleaned_data["reservation_start"]
                reservation_end = form.cleaned_data["reservation_end"]
                rent_of_equipment = form.cleaned_data["rent_of_equipment"]

                creat_form = ConfirmReservationForm(
                    initial={'court': court,
                             'reservation_date': reservation_date,
                             'reservation_start': reservation_start.replace(':', '.'),
                             'reservation_end': reservation_end.replace(':', '.'),
                             'client': request.user,
                             'reservation_cost': self._calculate_cost(reservation_start,
                                                                      reservation_end,
                                                                      court,
                                                                      rent_of_equipment,
                                                                      )})
                return render(
                    request,
                    template_name="confirm_exact_reservation.html",
                    context={"form": creat_form, 'court': court}
                )
            return render(
                request,
                template_name="exact_reservation_form.html",
                context={"form": form}
            )
        form = ConfirmReservationForm(request.POST)
        if form.is_valid():
            r = form.save()
            self.request.user.profile.wallet += r.reservation_cost
            self.request.user.profile.save()
        return HttpResponseRedirect(reverse("clients_urls:user_reservations"))

    @staticmethod
    def _calculate_cost(reservation_start, reservation_end, court, rent_of_equipment):
        start_hour = int(str(reservation_start)[:2])
        start_minute = int(str(reservation_start)[3:5])
        end_hour = int(str(reservation_end)[:2])
        end_minute = int(str(reservation_end)[3:5])
        if not rent_of_equipment:
            court.equipment_cost = 0
        return court.hire_price * ((end_hour * 60 + end_minute - start_hour *
                                    60 - start_minute) / 30) + court.equipment_cost


class AddCourtFormView(PermissionRequiredMixin, FormView):
    permission_required = 'reservations_urls:add-court'
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


class ReservationsParamsEdit(UpdateView):
    model = Reservation
    # fields = '__all__'
    template_name = 'reservations_params_edit.html'
    form_class = ReservationsParamsEditForm
    success_url = reverse_lazy('reservations_urls:reservations-params-edit-view')

    def form_valid(self, form):
        print('lll', self.object.reservation_cost)
        success_url = self.get_success_url()
        self.request.user.profile.wallet -= self.object.reservation_cost
        self.object = form.save()
        print(self.object.reservation_cost)
        self.request.user.profile.wallet += self.object.reservation_cost
        self.request.user.profile.save()
        return HttpResponseRedirect(success_url)


class ReservationsParamsEditView(ListView):
    template_name = 'reservations_params_edit_view.html'
    model = Reservation
    ordering = 'reservation_date'


class ReservationsListDetailAdminView(ListView):
    template_name = 'reservations_delete_admin_view.html'
    model = Reservation
    ordering = 'reservation_date'




class DeleteReservation(DeleteView):
    model = Reservation
    template_name = 'reservation_delete.html'
    success_url = reverse_lazy('clients_urls:user_reservations')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.request.user.profile.wallet -= self.object.reservation_cost
        self.object.delete()
        self.request.user.profile.save()
        return HttpResponseRedirect(success_url)


class DeleteReservationUser(DeleteView):
    model = Reservation
    template_name = 'reservation_user_delete.html'
    success_url = reverse_lazy('clients_urls:user_reservations')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.request.user.profile.wallet -= self.object.reservation_cost
        self.object.delete()
        self.request.user.profile.save()
        return HttpResponseRedirect(success_url)
