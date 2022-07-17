from django.urls import path
from . import views

app_name = 'reservations_urls'

urlpatterns = [

    path('index/', views.IndexListView.as_view(), name='index-list-view'),

    path('courts-list/', views.CourtsListView.as_view(), name='courts-list'),

    path('courts-details/', views.CourtsListDetailView.as_view(), name='courts-details'),

    path('court-exact-detail/<pk>', views.CourtDetailView.as_view(), name='court-exact-detail'),

    path(
        'reserved-courts-details-views/',
        views.ReservedCourtsDetailsView.as_view(),
        name='reserved_courts_details_views'),


    path('admin-panel/', views.AdminPanel.as_view(), name='admin-panel'),

    path('add-court/', views.AddCourtFormView.as_view(), name='add-court'),

    path('delete-court/', views.DeleteCourtListView.as_view(), name='delete-court'),

    path('delete-exact-court/<pk>', views.DeleteExactCourtView.as_view(), name='delete-exact-court'),

    path('court-params-edit/', views.CourtsParamsEditView.as_view(), name='court-params-edit'),

    path('exact-court-edit/<pk>', views.ExactCourtParamsEdit.as_view(), name='exact-court-edit'),

    path('create-exact-reservation/<pk>',
         views.CreateExactCourtReservation.as_view(), name='create-exact-reservation'),

    path('reservation-delete-list/', views.ReservationsDeleteList.as_view(),
         name='reservation-delete-list'),

    path('reservation-delete/<pk>', views.DeleteReservation.as_view(), name='reservation-delete'),

    path('reservation-delete-user/<pk>', views.DeleteReservationUser.as_view(), name='reservation-delete-user'),


]
