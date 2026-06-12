from django.views.generic import DetailView, ListView

from .models import Guide


class GuideListView(ListView):
    model = Guide
    template_name = 'guides/list.html'
    context_object_name = 'guides'
    paginate_by = 12

    def get_queryset(self):
        return Guide.objects.filter(is_published=True).select_related('category').prefetch_related('tags')


class GuideDetailView(DetailView):
    model = Guide
    template_name = 'guides/detail.html'
    context_object_name = 'guide'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Guide.objects.filter(is_published=True).select_related('category').prefetch_related('tags', 'related_products__category')
