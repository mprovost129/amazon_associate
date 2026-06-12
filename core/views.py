from django.db.models import Count, Prefetch
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

from core.models import SiteSetting
from guides.models import Guide
from products.models import Category, Collection, Product, ProductClick, Tag


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_products = Prefetch(
            'products',
            queryset=Product.objects.filter(is_active=True).prefetch_related('tags'),
            to_attr='active_products',
        )
        context['sections'] = Category.objects.prefetch_related(active_products).filter(
            products__is_active=True
        ).distinct()[:6]
        context['uncategorized'] = Product.objects.filter(
            is_active=True
        ).filter(categories__isnull=True).prefetch_related('tags')[:8]
        context['featured_products'] = Product.objects.filter(
            is_active=True, is_featured=True,
        ).prefetch_related('categories', 'tags')[:8]
        context['featured_collections'] = Collection.objects.filter(
            is_published=True, is_featured=True,
        ).prefetch_related('products')[:4]
        context['featured_guides'] = Guide.objects.filter(
            is_published=True, is_featured=True,
        ).select_related('category').prefetch_related('tags')[:3]
        context['popular_tags'] = Tag.objects.filter(products__is_active=True).distinct()[:12]
        site_setting, _ = SiteSetting.objects.get_or_create(pk=1)
        context['home_hero'] = site_setting.home_hero
        return context


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /accounts/',
        'Disallow: /go/',
        '',
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


class PerformanceDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'core/performance.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clicks = ProductClick.objects.select_related('product')
        context['total_clicks'] = clicks.count()
        context['top_products'] = (
            Product.objects.filter(clicks__isnull=False)
            .annotate(total_clicks=Count('clicks'))
            .order_by('-total_clicks', 'name')[:10]
        )
        context['top_sources'] = (
            clicks.values('source')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )
        context['top_campaigns'] = (
            clicks.values('campaign')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )
        context['top_pages'] = (
            clicks.values('page_path')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )
        context['recent_clicks'] = clicks.order_by('-clicked_at')[:25]
        return context
