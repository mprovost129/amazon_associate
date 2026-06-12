import csv

from django.contrib import admin, messages
from django.db.models import Count
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Category, Collection, Product, ProductClick, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'hero_text')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = 'admin/products/product/change_list.html'
    list_display = (
        'name', 'category', 'review_status', 'is_active', 'is_featured',
        'order', 'click_count', 'last_checked_at', 'next_review_at', 'created_at',
    )
    list_editable = ('review_status', 'is_active', 'is_featured', 'order')
    list_filter = (
        'review_status', 'is_active', 'is_featured', 'category', 'tags',
        'last_checked_at', 'next_review_at',
    )
    search_fields = (
        'name', 'description', 'best_for', 'why_i_like_it', 'seo_title',
        'seo_description', 'amazon_asin', 'review_notes',
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    filter_horizontal = ('tags', 'related_products')
    actions = ('mark_current', 'mark_needs_review', 'mark_inactive', 'export_selected_csv')
    fieldsets = (
        (None, {
            'fields': ('category', 'tags', 'related_products', 'name', 'slug', 'description', 'amazon_url', 'amazon_asin', 'image_url'),
        }),
        ('Recommendation copy', {
            'fields': ('best_for', 'why_i_like_it'),
        }),
        ('Display controls', {
            'fields': ('is_active', 'is_featured', 'order'),
        }),
        ('Review workflow', {
            'fields': ('review_status', 'last_checked_at', 'next_review_at', 'review_notes'),
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_click_count=Count('clicks'))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-template/', self.admin_site.admin_view(self.export_template), name='products_product_export_template'),
        ]
        return custom_urls + urls

    @admin.display(ordering='_click_count', description='Clicks')
    def click_count(self, obj):
        return obj._click_count

    @admin.action(description='Mark selected products as current/reviewed')
    def mark_current(self, request, queryset):
        updated = queryset.update(review_status=Product.REVIEW_CURRENT, last_checked_at=timezone.now())
        self.message_user(request, f'{updated} products marked current.', messages.SUCCESS)

    @admin.action(description='Mark selected products as needing review')
    def mark_needs_review(self, request, queryset):
        updated = queryset.update(review_status=Product.REVIEW_NEEDS_REVIEW)
        self.message_user(request, f'{updated} products marked as needing review.', messages.WARNING)

    @admin.action(description='Deactivate selected products')
    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False, review_status=Product.REVIEW_ARCHIVED)
        self.message_user(request, f'{updated} products deactivated and archived.', messages.SUCCESS)

    @admin.action(description='Export selected products to CSV')
    def export_selected_csv(self, request, queryset):
        return write_product_csv(queryset)

    def export_template(self, request):
        return write_product_csv(Product.objects.none())

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['product_csv_template_url'] = reverse('admin:products_product_export_template')
        return super().changelist_view(request, extra_context=extra_context)


def write_product_csv(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'name', 'slug', 'category', 'tags', 'amazon_url', 'amazon_asin', 'image_url',
        'description', 'best_for', 'why_i_like_it', 'is_active', 'is_featured',
        'order', 'seo_title', 'seo_description', 'review_status', 'last_checked_at',
        'next_review_at', 'review_notes',
    ])
    for product in queryset.select_related('category').prefetch_related('tags'):
        writer.writerow([
            product.name, product.slug, product.category.name if product.category else '',
            ', '.join(product.tags.values_list('name', flat=True)), product.amazon_url,
            product.amazon_asin, product.image_url, product.description, product.best_for,
            product.why_i_like_it, product.is_active, product.is_featured, product.order,
            product.seo_title, product.seo_description, product.review_status,
            product.last_checked_at.isoformat() if product.last_checked_at else '',
            product.next_review_at.isoformat() if product.next_review_at else '', product.review_notes,
        ])
    return response


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'is_featured', 'order', 'updated_at')
    list_editable = ('is_published', 'is_featured', 'order')
    list_filter = ('is_published', 'is_featured', 'updated_at')
    search_fields = ('title', 'subtitle', 'intro', 'seo_title', 'seo_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('products',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProductClick)
class ProductClickAdmin(admin.ModelAdmin):
    list_display = ('product', 'clicked_at', 'source', 'medium', 'campaign', 'page_path')
    list_filter = ('product', 'source', 'medium', 'campaign', 'clicked_at')
    search_fields = ('product__name', 'referrer', 'user_agent', 'source', 'medium', 'campaign', 'page_path')
    readonly_fields = (
        'product', 'clicked_at', 'referrer', 'user_agent', 'ip_hash',
        'source', 'medium', 'campaign', 'term', 'content', 'landing_page', 'page_path',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
