from django.urls import path
from accounts import views


app_name = 'accounts_urls'

urlpatterns = [
    path('register/', views.RegisterUserForm.as_view(), name="register"),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),

]