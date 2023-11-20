from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from trails.models import Region, Trail


class RegionSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Region.objects.all()

    def lastmod(self, obj):
        return obj.updated


class TrailSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Trail.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated


class StaticPageSitemap(Sitemap):
    priority = 1
    changefreq = 'yearly'
    protocol = 'https'

    def items(self):
        return ['trails:index']

    def location(self, item):
        return reverse(item)
