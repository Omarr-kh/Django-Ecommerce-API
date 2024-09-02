from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_user, name="register-user"),
    path("login", views.CustomLogin.as_view(), name="login"),
    path(
        "products", views.ProductListCreateView.as_view(), name="list-create-products"
    ),
    path(
        "products/<int:pk>",
        views.ProductRetrieveUpdateDestroyView.as_view(),
        name="update-delete-retrieve-products",
    ),
    path("orders", views.OrderListCreateView.as_view(), name="list-create-orders"),
    path(
        "orders/<int:pk>",
        views.OrderRetrieveUpdateDestroyView.as_view(),
        name="update-delete-retrieve-orders",
    ),
]
