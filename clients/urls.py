from django.urls import path
from . import views

app_name = 'clients_urls'

urlpatterns = [
    path('profile_panel/', views.ProfileView.as_view(), name='profile_panel'),
    path('user_edit_profile/', views.UserEditView.as_view(), name='user_edit_profile'),
    path('user_reservations/', views.UserReservationsView.as_view(), name='user_reservations'),
    path('user_edit_reservations/<pk>', views.UserEditReservations.as_view(), name='user_edit_reservations'),
    path('user_edit_reservations_view/', views.UserEditReservationsView.as_view(), name='user_edit_reservations_view'),
    path('user_delete_reservations/<pk>', views.UserDeleteReservations.as_view(), name='user_delete_reservations'),
    path('user_delete_reservations_view/', views.UserDeleteReservationsList.as_view(), name='user_delete_reservations_view'),

]


