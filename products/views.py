import csv
from io import TextIOWrapper
from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ProductImportForm
from .models import Category, Collection, Product, ProductClick, Tag


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('tags')
        self.query = self.request.GET.get('q', '').strip()
        self.category_slug = self.request.GET.get('category', '').strip()
        self.tag_slug = self.request.GET.get('tag', '').strip()

        if self.query:
            queryset = queryset.filter(
                Q(name__icontains=self.query)
                | Q(description__icontains=self.query)
                | Q(best_for__icontains=self.query)
                | Q(why_i_like_it__icontains=self.query)
                | Q(category__name__icontains=self.query)
                | Q(tags__name__icontains=self.query)
            )
        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
        if self.tag_slug:
            queryset = queryset.filter(tags__slug=self.tag_slug)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.query
        context['selected_category'] = self.category_slug
        context['selected_tag'] = self.tag_slug
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            category=self.object, is_active=True
        ).prefetch_related('tags')
        context['featured_products'] = Product.objects.filter(
            category=self.object, is_active=True, is_featured=True
        ).prefetch_related('tags')[:8]
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category').prefetch_related('tags', 'related_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        related = product.related_products.filter(is_active=True).select_related('category').prefetch_related('tags')
        if not related.exists():
            related = Product.objects.filter(is_active=True).exclude(pk=product.pk)
            if product.category_id:
                related = related.filter(category=product.category)
            related = related.select_related('category').prefetch_related('tags')[:4]
        context['related_products'] = related
        return context


class CollectionListView(ListView):
    model = Collection
    template_name = 'products/collection_list.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return Collection.objects.filter(is_published=True).prefetch_related('products')


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'products/collection_detail.html'
    context_object_name = 'collection'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Collection.objects.filter(is_published=True).prefetch_related('products__category', 'products__tags')


class ProductRedirectView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        ip = request.META.get('REMOTE_ADDR', '')
        referrer = request.META.get('HTTP_REFERER', '')[:500]
        campaign = request.session.get('campaign_attribution', {})
        page_path = ''
        if referrer:
            parsed_referrer = urlparse(referrer)
            page_path = parsed_referrer.path[:500]

        ProductClick.objects.create(
            product=product,
            referrer=referrer,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            ip_hash=ProductClick.hash_ip(ip) if ip else '',
            source=request.GET.get('utm_source', '')[:120] or campaign.get('utm_source', '')[:120],
            medium=request.GET.get('utm_medium', '')[:120] or campaign.get('utm_medium', '')[:120],
            campaign=request.GET.get('utm_campaign', '')[:200] or campaign.get('utm_campaign', '')[:200],
            term=request.GET.get('utm_term', '')[:200] or campaign.get('utm_term', '')[:200],
            content=request.GET.get('utm_content', '')[:200] or campaign.get('utm_content', '')[:200],
            landing_page=campaign.get('landing_page', '')[:500],
            page_path=page_path,
        )
        return redirect(product.amazon_url)


@method_decorator(staff_member_required, name='dispatch')
class ProductExportView(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products-export.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'name', 'slug', 'category', 'tags', 'amazon_url', 'amazon_asin', 'image_url',
            'description', 'best_for', 'why_i_like_it', 'is_active', 'is_featured',
            'order', 'seo_title', 'seo_description', 'review_status', 'last_checked_at',
            'next_review_at', 'review_notes',
        ])
        for product in Product.objects.select_related('category').prefetch_related('tags'):
            writer.writerow([
                product.name, product.slug, product.category.name if product.category else '',
                ', '.join(product.tags.values_list('name', flat=True)), product.amazon_url,
                product.amazon_asin, product.image_url, product.description, product.best_for,
                product.why_i_like_it, product.is_active, product.is_featured, product.order,
                product.seo_title, product.seo_description, product.review_status,
                product.last_checked_at.isoformat() if product.last_checked_at else '',
                product.next_review_at.isoformat() if product.next_review_at else '', product.review_notes,
            ])
        return response


@method_decorator(staff_member_required, name='dispatch')
class ProductImportView(View):
    template_name = 'products/import.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ProductImportForm()})

    def post(self, request):
        form = ProductImportForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8-sig')
        reader = csv.DictReader(csv_file)
        created = 0
        updated = 0
        skipped = 0
        update_existing = form.cleaned_data['update_existing']

        for row in reader:
            name = (row.get('name') or '').strip()
            amazon_url = (row.get('amazon_url') or '').strip()
            slug = (row.get('slug') or '').strip()
            if not name or not amazon_url:
                skipped += 1
                continue

            category = None
            category_name = (row.get('category') or '').strip()
            if category_name:
                category, _ = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'slug': category_name.lower().replace(' ', '-')[:50]},
                )

            product = Product.objects.filter(slug=slug).first() if slug else None
            if product and not update_existing:
                skipped += 1
                continue

            if not product:
                product = Product(name=name, amazon_url=amazon_url)
                created += 1
            else:
                updated += 1

            product.name = name
            product.amazon_url = amazon_url
            if slug:
                product.slug = slug
            product.category = category
            product.amazon_asin = (row.get('amazon_asin') or '').strip()
            product.image_url = (row.get('image_url') or '').strip()
            product.description = (row.get('description') or '').strip()
            product.best_for = (row.get('best_for') or '').strip()
            product.why_i_like_it = (row.get('why_i_like_it') or '').strip()
            product.is_active = str(row.get('is_active', 'True')).strip().lower() in ('1', 'true', 'yes', 'y')
            product.is_featured = str(row.get('is_featured', 'False')).strip().lower() in ('1', 'true', 'yes', 'y')
            product.order = int(row.get('order') or 0)
            product.seo_title = (row.get('seo_title') or '').strip()
            product.seo_description = (row.get('seo_description') or '').strip()
            product.review_status = (row.get('review_status') or Product.REVIEW_DRAFT).strip()
            product.review_notes = (row.get('review_notes') or '').strip()
            product.save()

            tag_names = [tag.strip() for tag in (row.get('tags') or '').split(',') if tag.strip()]
            if tag_names:
                tags = []
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': tag_name.lower().replace(' ', '-')[:50]},
                    )
                    tags.append(tag)
                product.tags.set(tags)

        messages.success(request, f'Import complete: {created} created, {updated} updated, {skipped} skipped.')
        return redirect('admin:products_product_changelist')
