from django.urls import path

from . import views


app_name = 'account'

urlpatterns = [
    path('account/registration', views.RegistrationView.as_view(), name='registration'),
    path('account/login', views.LoginView.as_view(), name='login'),
    path('account/logout', views.LogoutView.as_view(), name='logout'),
    path('account/is-login', views.IsLoginView.as_view(), name='is-login'),
    path('users/<int:id>/todos', views.UserToDoView.as_view(), name='user-to-do'),
]
