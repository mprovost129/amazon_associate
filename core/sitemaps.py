from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return [
            'core:home',
            'core:privacy',
            'core:terms',
            'guides:list',
            'products:collection_list',
            'products:search',
        ]

    def location(self, item):
        return reverse(item)
