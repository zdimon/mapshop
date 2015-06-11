# -*- coding: utf-8 -*-
from django_ajax.decorators import ajax
from mapshop.models import Category, Product, Kiosk, Order

@ajax
def add_product_to_cart(request):
    '''  Добавление товара в корзину и вывод содержимого корзины в html блок <table id="my_busket"></table> '''
    print '----------------------------------%s' % request.GET.get('product_id',0)
    print '----------------------------------%s' % request.user.username
    try:
        product  = Product.objects.get(pk=request.GET.get('product_id',0))
    except:
        product = None

    session = request.session.session_key
    try:
        order = Order.objects.get(session=session)
    except:
        order = Order()
        order.session = session
        if request.user.is_authenticated:
            order.user_id = request.user.id
        order.save()
    data = {
            'inner-fragments': { '#my_basket': '<h1> Моя корзина </h1>' },       
           }     
    return data


@ajax
def getinfo_kiosk(request):
    '''   '''
    print '----------------------------------%s' % request.GET['kiosk_id']
    out = ''
    #try:
    kiosk = Kiosk.objects.get(pk=request.GET['kiosk_id'])
    out = u'киоск %s <br /> <a href="/finish/order/%s/kiosk/%d">пРОДОЛЖИТЬ ОФОРМЛЕНИЕ</a>' % (kiosk.name, request.GET['order_id'], kiosk.id)
    #except:
    #    out = 'object does not found'

    data = {
            'inner-fragments': { '#kiosk_info': out },       
           }     
    return data

'''

        <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax.min.js' %}"></script>
        <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax-plugin.min.js' %}"></script>

        <script type="text/javascript" src="{% static 'mapsho/static/driver.js' %}"></script>
    



        //// Close private chat **************************
         $('#content').on('click', function(e) {
          
            e.preventDefault();
            
                 ajaxGet('{% url 'ajax-close-private-chat' %}', { 'room_id': room_id }, function(content){ alert(content.myvar) });     
                ajaxGet('/myurl', { 'room_id': room_id }, function(content){});         
            
        });   
        //**************************************************




'''
