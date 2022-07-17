from django.urls import path
from . import views

app_name = 'clients_urls'

urlpatterns = [
    path('profile-panel/', views.ProfileView.as_view(), name='profile-panel'),
    path('user-edit-profile/', views.UserEditView.as_view(), name='user-edit-profile'),
    path('user-reservations/', views.UserReservationsView.as_view(), name='user-reservations'),
    path('profile-list-view/', views.ProfileListView.as_view(), name='profile-list-view'),
]


