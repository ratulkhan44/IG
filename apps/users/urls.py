# Django Imports
from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserLogoutView

urlpatterns = [
    path('user-registration/', UserRegistrationView.as_view()),
    path('user-login/', UserLoginView.as_view()),
    path('user-logout/', UserLogoutView.as_view()),
]