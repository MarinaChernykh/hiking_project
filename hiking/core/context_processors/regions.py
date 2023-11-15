from django.core.cache import cache

from trails.models import Region


def regions(request):
    """Regions list for navigation menu."""
    regions = list(Region.objects.all())
    regions_cache_key = 'regions'
    regions = cache.get(regions_cache_key)
    if regions is None:
        regions = list(Region.objects.all())
        cache.set(regions_cache_key, regions, 500)
    return {'regions': regions}
