from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from .models import Category, Product, ProductClick


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            category=self.object, is_active=True
        )
        return context


class ProductRedirectView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        ip = request.META.get('REMOTE_ADDR', '')
        ProductClick.objects.create(
            product=product,
            referrer=request.META.get('HTTP_REFERER', '')[:500],
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            ip_hash=ProductClick.hash_ip(ip) if ip else '',
        )
        return redirect(product.amazon_url)
