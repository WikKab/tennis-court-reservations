from django.urls import path
from accounts import views


app_name = 'accounts_urls'

urlpatterns = [
    path('register/', views.RegisterUserForm.as_view(), name="register"),
    path('login/', views.Login.as_view(), name='login_main'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),

]