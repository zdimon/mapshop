from django.conf.urls import patterns, include, url

from django.contrib import admin
from mapshop import urls as mapshop_urls

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'mapshop.views.home', name='home'),
    url(r'', include('mapshop.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
     url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name='logout'),
     url(r'^login/$', 'django.contrib.auth.views.login', name='login'),

)

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
