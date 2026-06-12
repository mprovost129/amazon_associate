import hashlib

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    hero_text = models.TextField(
        blank=True,
        help_text='Text shown below the navbar on this category page.',
    )

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('products:category', args=[self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    REVIEW_DRAFT = 'draft'
    REVIEW_CURRENT = 'current'
    REVIEW_NEEDS_REVIEW = 'needs_review'
    REVIEW_ARCHIVED = 'archived'
    REVIEW_STATUS_CHOICES = (
        (REVIEW_DRAFT, 'Draft'),
        (REVIEW_CURRENT, 'Current'),
        (REVIEW_NEEDS_REVIEW, 'Needs review'),
        (REVIEW_ARCHIVED, 'Archived'),
    )

    category = models.ForeignKey(
        Category, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='products',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    related_products = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='recommended_with',
        help_text='Optional hand-picked internal links shown on the product detail page.',
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    best_for = models.CharField(
        max_length=200,
        blank=True,
        help_text='Short use-case text, e.g. Beginner 3D printing cleanup.',
    )
    why_i_like_it = models.TextField(
        blank=True,
        help_text='Longer product detail copy explaining why this item is recommended.',
    )
    amazon_url = models.URLField()
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    last_checked_at = models.DateTimeField(null=True, blank=True)
    next_review_at = models.DateField(null=True, blank=True)
    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS_CHOICES,
        default=REVIEW_DRAFT,
    )
    review_notes = models.TextField(blank=True)
    amazon_asin = models.CharField(max_length=20, blank=True, help_text='Optional ASIN for exports/imports and review tracking.')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:45] or 'product'
            slug = base_slug
            counter = 2
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('products:detail', args=[self.slug])

    def get_redirect_url(self):
        from django.urls import reverse
        return reverse('products:redirect', args=[self.pk])

    def mark_reviewed(self):
        self.review_status = self.REVIEW_CURRENT
        self.last_checked_at = timezone.now()
        self.save(update_fields=['review_status', 'last_checked_at'])

    @property
    def display_seo_title(self):
        return self.seo_title or self.name

    @property
    def display_seo_description(self):
        description = self.seo_description or self.description or self.best_for or self.why_i_like_it
        return description[:155]


class Collection(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField(max_length=240, blank=True)
    intro = models.TextField(blank=True)
    products = models.ManyToManyField(Product, blank=True, related_name='collections')
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:45] or 'collection'
            slug = base_slug
            counter = 2
            while Collection.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('products:collection_detail', args=[self.slug])

    @property
    def display_seo_title(self):
        return self.seo_title or self.title

    @property
    def display_seo_description(self):
        description = self.seo_description or self.subtitle or self.intro
        return description[:155]


class ProductClick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=500, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    ip_hash = models.CharField(max_length=64, blank=True)
    source = models.CharField(max_length=120, blank=True)
    medium = models.CharField(max_length=120, blank=True)
    campaign = models.CharField(max_length=200, blank=True)
    term = models.CharField(max_length=200, blank=True)
    content = models.CharField(max_length=200, blank=True)
    landing_page = models.CharField(max_length=500, blank=True)
    page_path = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-clicked_at']

    @staticmethod
    def hash_ip(ip):
        return hashlib.sha256(ip.encode()).hexdigest()
