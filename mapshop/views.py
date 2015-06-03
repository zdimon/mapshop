# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, RequestContext

def home(request):
    context = {}
    return render_to_response('mapshop/home.html', context, RequestContext(request))

def product_list(request,category_name='all'):
    u''' 
        Список товаров в категории (по умолчанию во всех категориях)
        при передаче параметров sort_price, sort_rate (up/down) сортируем.
    '''
    #category = Course.objects.get(name=category_name)
    #Author.objects.order_by('-score')[:30]
    context = {}
    return render_to_response('mapshop/product_list.html', context, RequestContext(request))



