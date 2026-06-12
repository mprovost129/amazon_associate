from django.contrib.sitemaps import Sitemap

from .models import Category, Collection, Product


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.filter(products__is_active=True).distinct()


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.last_checked_at or obj.created_at


class CollectionSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.75

    def items(self):
        return Collection.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
