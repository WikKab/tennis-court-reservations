from django.contrib import admin
from django.urls import path
from . import views

app_name = 'reservations_urls'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('courts/', views.CourtsListView.as_view(), name='courts'),

    path('courts-details/', views.CourtsListDetailView.as_view(), name='courts-details'),

    path('court-exact-detail/<pk>', views.CourtDetailView.as_view(), name='court-exact-detail'),

    path(
        'reserved-courts-list-view/',
        views.ReservedCourtsListView.as_view(),
        name='reserved_courts_list_views'),

    path(
        'reserved-courts-details-view/',
        views.ReservedCourtsDetailsView.as_view(),
        name='reserved_courts_details_views'),

    path('index/', views.IndexListView.as_view(), name='index-list-view'),

    path('reservations/', views.ReservationSystemListView.as_view(), name='reservations'),

    path('login/', views.Login.as_view(), name='login_main'),

    path('logout/', views.Logout.as_view(), name='logout'),

    path('admin-panel/', views.AdminPanel.as_view(), name='admin-panel'),

    path('reservation-form/', views.CreateReservationFormView.as_view(), name='reservation-form'),

    path('reservation-court-selection/',
         views.CreateReservationCourtSelect.as_view(), name='reservation-court-selection'),

    path('reservation-with-selected-court/<pk>',
         views.CreateReservationWithSelectedCourt.as_view(), name='reservation-with-selected-court'),


    path('add-court/', views.AddCourtFormView.as_view(), name='add-court'),

    path('delete-court/<pk>', views.DeleteCourtView.as_view(), name='delete'),

    path('courts-detail_admin_view/', views.CourtsListDetailAdminView.as_view(), name='courts-detail-admin'),

    path('courts-params/', views.CourtsParamsEditView.as_view(), name='courts-params-edit-view'),

    path('courts-edit/<pk>', views.CourtParamsEdit.as_view(), name='courts-params-edit'),

    path('create-exact-reservation/<pk>',
         views.CreateExactCourtReservationFormView.as_view(), name='create-exact--reservation'),


    path('reservations-params/', views.ReservationsParamsEditView.as_view(), name='reservations-params-edit-view'),

    path('reservations-edit/<pk>', views.ReservationsParamsEdit.as_view(), name='reservations-params-edit'),

    path('reservation-delete/<pk>', views.DeleteReservation.as_view(), name='reservation-delete'),

    path('reservations-detail_admin_view/', views.ReservationsListDetailAdminView.as_view(), name='reservations-details'),

]
