# Generated manually for Phase 2 launch work.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_launch_seo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('subtitle', models.CharField(blank=True, max_length=240)),
                ('intro', models.TextField(blank=True)),
                ('is_published', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('seo_title', models.CharField(blank=True, max_length=70)),
                ('seo_description', models.CharField(blank=True, max_length=160)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('products', models.ManyToManyField(blank=True, related_name='collections', to='products.product')),
            ],
            options={
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.tag'),
        ),
    ]
