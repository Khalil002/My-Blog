from django.conf import settings


def site_name(request):
    """Make SITE_NAME available in every template as {{ site_name }}."""
    return {"site_name": getattr(settings, "SITE_NAME", "My Blog")}
