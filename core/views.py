from django.db.models import Prefetch
from django.views.generic import TemplateView

from core.models import SiteSetting
from products.models import Category, Product


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_products = Prefetch(
            'products',
            queryset=Product.objects.filter(is_active=True),
            to_attr='active_products',
        )
        context['sections'] = Category.objects.prefetch_related(active_products).filter(
            products__is_active=True
        ).distinct()
        context['uncategorized'] = Product.objects.filter(
            is_active=True, category__isnull=True
        )
        site_setting, _ = SiteSetting.objects.get_or_create(pk=1)
        context['home_hero'] = site_setting.home_hero
        return context
