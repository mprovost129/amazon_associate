from django.db import migrations, models


def copy_category_to_categories(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.exclude(category=None):
        product.categories.add(product.category)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_phase4_product_operations'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products_new', to='products.category'),
        ),
        migrations.RunPython(copy_category_to_categories, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.category'),
        ),
    ]
