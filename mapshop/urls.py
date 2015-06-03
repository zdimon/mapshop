# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns( '',
    url(r'^product/list/all.html$', 'mapshop.views.product_list', name="catalog_all"),
    url(r'^product/list/(?P<category_name>[^\.]+).html$', 'mapshop.views.product_list', name="catalog_filter"),
    
)
