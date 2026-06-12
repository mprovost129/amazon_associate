from django.contrib import admin

from .models import Guide


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'is_featured', 'published_at', 'updated_at')
    list_editable = ('is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'category', 'tags', 'published_at')
    search_fields = ('title', 'dek', 'body', 'seo_title', 'seo_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'related_products')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'dek', 'category', 'tags', 'body', 'featured_image_url')}),
        ('Related products', {'fields': ('related_products',)}),
        ('Publishing', {'fields': ('is_published', 'is_featured', 'published_at')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
