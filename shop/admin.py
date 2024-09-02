from django.contrib import admin
from .models import Product, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "stock")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
