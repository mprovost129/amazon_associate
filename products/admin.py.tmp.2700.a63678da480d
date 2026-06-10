from django.contrib import admin
from django.db.models import Count

from .models import Category, Product, ProductClick


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'order', 'click_count', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_click_count=Count('clicks'))

    @admin.display(ordering='_click_count', description='Clicks')
    def click_count(self, obj):
        return obj._click_count


@admin.register(ProductClick)
class ProductClickAdmin(admin.ModelAdmin):
    list_display = ('product', 'clicked_at', 'referrer')
    list_filter = ('product',)
    readonly_fields = ('product', 'clicked_at', 'referrer', 'user_agent', 'ip_hash')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
