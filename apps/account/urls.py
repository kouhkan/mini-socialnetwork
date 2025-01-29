from django.urls import path

from apps.account.api.v1 import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register_user"),
    path("login/", views.LoginView.as_view(), name="login_user"),
]
