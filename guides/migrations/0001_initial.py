# Generated manually for Phase 2 launch work.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0005_tags_collections'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('dek', models.CharField(blank=True, help_text='One- or two-sentence summary shown on guide cards.', max_length=240, verbose_name='short summary')),
                ('body', models.TextField(help_text='Main guide content. Plain text with paragraph breaks is fine.')),
                ('featured_image_url', models.URLField(blank=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('seo_title', models.CharField(blank=True, max_length=70)),
                ('seo_description', models.CharField(blank=True, max_length=160)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guides', to='products.category')),
                ('related_products', models.ManyToManyField(blank=True, related_name='guides', to='products.product')),
                ('tags', models.ManyToManyField(blank=True, related_name='guides', to='products.tag')),
            ],
            options={
                'ordering': ['-published_at', '-created_at'],
            },
        ),
    ]
