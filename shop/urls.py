from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_user, name="register-user"),
    path("login", views.CustomLogin.as_view(), name="login"),
    path("products", views.ListProductsView.as_view(), name="list-products"),
]
