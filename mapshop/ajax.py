from django_ajax.decorators import ajax

@ajax
def my_view(request)
    return {'myvar'}

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
