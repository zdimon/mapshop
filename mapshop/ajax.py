# -*- coding: utf-8 -*-
from django_ajax.decorators import ajax

@ajax
def add_product_to_cart(request):
    '''  Добавление товара в корзину и вывод содержимого корзины в html блок <table id="my_busket"></table> '''
    print '----------------------------------%s' % request.GET['product_id']
    print '----------------------------------%s' % request.user.username
    data = {
            'inner-fragments': { '#my_busket': '<h1> Моя корзина </h1>' },       
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
