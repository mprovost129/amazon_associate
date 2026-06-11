from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_product_category_productclick'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='hero_text',
            field=models.TextField(blank=True, help_text='Text shown below the navbar on this category page.'),
        ),
    ]
