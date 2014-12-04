from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from ajax_select import urls as ajax_select_urls

urlpatterns = patterns(
	'',
    # Examples:
    # url(r'^$', 'care4care.views.home', name='home'),
    url(r'', include('main.urls')),
    (r'^lookups/', include(ajax_select_urls)),
    url(r'^branch/', include('branch.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^translate/', include('rosetta.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
