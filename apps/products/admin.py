from django.contrib import admin
from apps.products.models import Product, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'category', 'price', 'is_available']
    list_filter = ['business', 'category', 'is_available']
    search_fields = ['name', 'business__name']
