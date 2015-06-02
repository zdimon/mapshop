from django.conf.urls import patterns, include, url

from django.contrib import admin
from mapshop import urls as mapshop_urls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mapshop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(mapshop_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
