from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_hero', models.TextField(blank=True, help_text='Text shown below the navbar on the home page.')),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
    ]
