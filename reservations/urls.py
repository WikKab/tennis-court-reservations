from django.contrib import admin
from django.urls import path
from . import views

app_name = 'reservations_urls'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('korty/', views.CourtsListView.as_view(), name='korty2'),

    path(
        'reserved-courts-list-view/',
        views.ReservedCourtsListView.as_view(),
        name='reserved_courts_list_views'),

    path('index/', views.IndexListView.as_view(), name='index-list-view'),

    path('reservations/', views.ReservationSystemListView.as_view(), name='reservations'),

    path('login/', views.Login.as_view(), name='login_main'),

    path('logout/', views.Logout.as_view(), name='logout'),

    path('reservation-form/', views.CreateReservationFormView.as_view(), name='reservation-form'),

]
