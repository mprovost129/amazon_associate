import hashlib

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='products',
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amazon_url = models.URLField()
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def get_redirect_url(self):
        from django.urls import reverse
        return reverse('products:redirect', args=[self.pk])


class ProductClick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=500, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    ip_hash = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ['-clicked_at']

    @staticmethod
    def hash_ip(ip):
        return hashlib.sha256(ip.encode()).hexdigest()
