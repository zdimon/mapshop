djangoajax==2.2.12

         $('#disagree').on('click', function(e) {
          
            e.preventDefault();
            var room_id = $(this).attr('data-room-id');
            ajaxGet('{% url 'ajax-close-private-chat' %}', { 'room_id': room_id }, function(content){});     
            
        });  



from django_ajax.decorators import ajax


@ajax
def update_contact_list(request):
    '''  Updating block  <ul id="chat_contact_list"> </ul> '''
    data = {
            'inner-fragments': { '#chat_contact_list': 'blabla' },       
           }
    return data 



        <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax.min.js' %}"></script>
        <script type="text/javascript" src="{% static 'django_ajax/js/jquery.ajax-plugin.min.js' %}"></script>


