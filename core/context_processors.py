from django.conf import settings
from products.models import Category


def site(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
        'SITE_HERO': settings.SITE_HERO,
        'nav_categories': Category.objects.all(),
    }
