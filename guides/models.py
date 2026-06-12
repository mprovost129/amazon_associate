from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from products.models import Category, Product, Tag


class Guide(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    dek = models.CharField(
        'short summary',
        max_length=240,
        blank=True,
        help_text='One- or two-sentence summary shown on guide cards.',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='guides',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='guides')
    body = models.TextField(help_text='Main guide content. Plain text with paragraph breaks is fine.')
    related_products = models.ManyToManyField(Product, blank=True, related_name='guides')
    featured_image_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:55] or 'guide'
            slug = base_slug
            counter = 2
            while Guide.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('guides:detail', args=[self.slug])

    @property
    def display_seo_title(self):
        return self.seo_title or self.title

    @property
    def display_seo_description(self):
        description = self.seo_description or self.dek or self.body
        return description[:155]
