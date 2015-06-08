# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from mapshop.forms import ProductFilterForm
from mapshop.models import Category, Product

def home(request):
    context = {}
    return render_to_response('mapshop/home.html', context, RequestContext(request))


def product_list(request,slug='all'):
    u''' 
        Список товаров в категории (по умолчанию во всех категориях)
        при передаче параметров sort_price, sort_rate (up/down) сортируем.
    '''
    # get all products
    #import pdb; pdb.set_trace()
    products = Product.objects.filter()
    print products
    if slug=='all':
        title = 'Все товары'
        # select all categories 
        category_list = Category.objects.all()
    else:
        
        category =  Category.objects.get(name_slug=slug)
        title = 'Товары из категории "%s"' % category
        # select all categories excluding current
        category_list = Category.objects.all().exclude(name_slug=slug)
        # add filter
        products = products.filter(category=category)

    # handle with order
    try:
        #import pdb; pdb.set_trace()
        rate_order = request.GET['rate_order']
        if rate_order == 'desc':
            products = products.order_by('-rate')
            cur_rate_order = 'desc'
        else:
            products = products.order_by('rate')  
            cur_rate_order = 'asc'
    except:
        pass

    #category = Course.objects.get(name=category_name)
    #Author.objects.order_by('-score')[:30]

    ''' avdey code
    filter_form = ProductFilterForm()
    if request.method == 'GET' and bool(request.GET):
        filter_form = ProductFilterForm(request.GET)
    data = dict(filter_form=filter_form)
    return render_to_response('product_list.html', data, RequestContext(request))
    '''

    context = {'title': title, 'category_list': category_list, 'product_list': products, 'cur_rate_order': cur_rate_order}
    return render_to_response('mapshop/product_list.html', context, RequestContext(request))




