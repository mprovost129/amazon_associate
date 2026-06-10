from django.shortcuts import get_object_or_404, redirect
from django.views import View

from .models import Product, ProductClick


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
