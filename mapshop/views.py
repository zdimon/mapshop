from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404

def product_list(request,category_name='all'):
    ''' 
        Список товаров в категории (по умолчанию во всех категориях)
        при передаче параметров sort_price, sort_rate (up/down) сортируем.

    '''
    #category = Course.objects.get(name=category_name)
    #Author.objects.order_by('-score')[:30]
    context = {}
    return render_to_response('courses_list.html', context, RequestContext(request))



