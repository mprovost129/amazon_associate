from django.contrib.sitemaps import Sitemap

from .models import Guide


class GuideSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Guide.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
