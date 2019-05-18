from django.urls import path

from . import views


app_name = 'account'

urlpatterns = [
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('is-login', views.IsLoginView.as_view(), name='is-login'),
]
