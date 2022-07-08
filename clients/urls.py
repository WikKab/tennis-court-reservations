from django.urls import path
from . import views

app_name = 'clients_urls'

urlpatterns = [
    path('profile_panel/', views.ProfileView.as_view(), name='profile_panel'),
    path('user_edit_profile/', views.UserEditView.as_view(), name='user_edit_profile'),
    path('user_profile/', views.ProfileListView.as_view(), name='user_profile'),
    path('user_reservations/', views.UserReservationsView.as_view(), name='user_reservations'),
    path('user_edit_reservations/', views.UserEditReservations.as_view(), name='user_edit_reservations'),
    path('user_delete_reservations/', views.UserDeleteReservations.as_view(), name='user_delete_reservations'),

]


