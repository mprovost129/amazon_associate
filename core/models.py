from django.db import models


class SiteSetting(models.Model):
    home_hero = models.TextField(
        blank=True,
        help_text='Text shown below the navbar on the home page.',
    )

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
