# Generated manually for Phase 4 operations/scaling work.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_click_campaign_attribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amazon_asin',
            field=models.CharField(blank=True, help_text='Optional ASIN for exports/imports and review tracking.', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='next_review_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='review_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='review_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('current', 'Current'), ('needs_review', 'Needs review'), ('archived', 'Archived')], default='draft', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=models.ManyToManyField(blank=True, help_text='Optional hand-picked internal links shown on the product detail page.', related_name='recommended_with', to='products.product'),
        ),
    ]
