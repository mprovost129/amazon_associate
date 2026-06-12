# Generated for Phase 1 launch readiness.

from django.db import migrations, models
from django.utils.text import slugify


def populate_product_slugs(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    used_slugs = set()
    for product in Product.objects.order_by('pk'):
        base_slug = slugify(product.name)[:45] or 'product'
        slug = base_slug
        counter = 2
        while slug in used_slugs or Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        product.slug = slug
        product.save(update_fields=['slug'])
        used_slugs.add(slug)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_hero_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='best_for',
            field=models.CharField(blank=True, help_text='Short use-case text, e.g. Beginner 3D printing cleanup.', max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='last_checked_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_description',
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_title',
            field=models.CharField(blank=True, max_length=70),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='why_i_like_it',
            field=models.TextField(blank=True, help_text='Longer product detail copy explaining why this item is recommended.'),
        ),
        migrations.RunPython(populate_product_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
