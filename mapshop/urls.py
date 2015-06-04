from django.conf.urls import patterns, url
import mapshop.views as views

__author__ = '1'

urlpatterns = patterns('',
                       url(r'^product-list$', views.product_list, name='page.product_list')
)