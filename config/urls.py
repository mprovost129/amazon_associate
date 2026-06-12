from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import StaticViewSitemap
from guides.sitemaps import GuideSitemap
from products.sitemaps import CategorySitemap, CollectionSitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'collections': CollectionSitemap,
    'guides': GuideSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('guides/', include('guides.urls')),
    path('', include('products.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
