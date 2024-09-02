from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status, generics
from rest_framework.response import Response

from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return Response(
                {"error": "Username, Password and email are required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists!!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(
            username=username, email=email, password=make_password(password)
        )
        Token.objects.create(user=user)

        return Response(
            {"message": "User registered successfully!"}, status=status.HTTP_201_CREATED
        )


class CustomLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]  # only admins can add new products
        return []  # Publicly accessible for authenticated users


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.queryset.filter(user=self.request.user)
        return Order.objects.all()
