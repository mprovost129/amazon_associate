# Generated manually for Phase 3 analytics work.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_tags_collections'),
    ]

    operations = [
        migrations.AddField(
            model_name='productclick',
            name='campaign',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='productclick',
            name='content',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='productclick',
            name='landing_page',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='productclick',
            name='medium',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='productclick',
            name='page_path',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='productclick',
            name='source',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='productclick',
            name='term',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
