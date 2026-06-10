from django.views.generic import ListView

from products.models import Category, Product


class HomeView(ListView):
    model = Product
    template_name = 'core/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category')
        slug = self.request.GET.get('category')
        if slug:
            qs = qs.filter(category__slug=slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_category'] = self.request.GET.get('category', '')
        return context
