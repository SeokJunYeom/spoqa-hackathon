from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views


app_name = 'account'

router = DefaultRouter(trailing_slash=False)
router.register(r'posts', views.FeedView)
router.register(r'users', views.UserPostView)

urlpatterns = [
    path('', include(router.urls)),
    path('account/registration', views.RegistrationView.as_view(), name='registration'),
    path('account/login', views.LoginView.as_view(), name='login'),
    path('account/logout', views.LogoutView.as_view(), name='logout'),
    path('account/is-login', views.IsLoginView.as_view(), name='is-login'),
    path('users/<int:id>/todos', views.UserToDoView.as_view(), name='user-to-do'),
    path('ranks', views.RankView.as_view(), name='rank'),
]
