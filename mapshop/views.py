# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from mapshop.forms import ProductFilterForm


def product_list(request):
    ''' 
        Список товаров в категории (по умолчанию во всех категориях)
        при передаче параметров sort_price, sort_rate (up/down) сортируем.

    '''
    #category = Course.objects.get(name=category_name)
    #Author.objects.order_by('-score')[:30]
    filter_form = ProductFilterForm()
    if request.method == 'GET' and bool(request.GET):
        filter_form = ProductFilterForm(request.GET)
    data = dict(filter_form=filter_form)
    return render_to_response('product_list.html', data, RequestContext(request))



