from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import RegionSitemap, TrailSitemap, StaticPageSitemap


sitemaps = {
    'regions': RegionSitemap,
    'trails': TrailSitemap,
    'static_pages': StaticPageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('', include('trails.urls', namespace='trails')),
    path(
        'sitemap.xml', sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    )
]

handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
