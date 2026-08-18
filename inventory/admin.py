from django.contrib import admin
from .models import Category, Supplier, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'supplier', 'quantity', 'price', 'get_stock_status']
    search_fields = ['name', 'sku']
    list_filter = ['category', 'supplier', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    search_fields = ['order_number', 'user__username']
    list_filter = ['status', 'created_at']
    readonly_fields = ['order_number', 'created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price_at_order', 'get_subtotal']
    search_fields = ['order__order_number', 'product__name']
    list_filter = ['created_at']
    readonly_fields = ['created_at']