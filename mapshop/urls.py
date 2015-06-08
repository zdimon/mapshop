# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import mapshop.views as views


from django.conf.urls import patterns, url

urlpatterns = patterns( '',
    url(r'^product/list/all.html$', 'mapshop.views.product_list', name="catalog_all"),
    url(r'^product/list/(?P<slug>[^\.]+).html$', 'mapshop.views.product_list', name="catalog_filter"),
    
)

