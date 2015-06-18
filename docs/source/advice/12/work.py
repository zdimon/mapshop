
########Установка поля

class Person(models.Model):
  name = models.CharField()

  __original_name = None

  def __init__(self, *args, **kwargs):
    super(Person, self).__init__(*args, **kwargs)
    self.__original_name = self.name

  def save(self, force_insert=False, force_update=False, *args, **kwargs):
    if self.name != self.__original_name:
      # name changed - do something here

    super(Person, self).save(force_insert, force_update, *args, **kwargs)
    self.__original_name = self.name


#### Mailing


EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'support@pressa.ru'

#EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/home/zarik/tmp' # change this to a proper location



from django.core.mail import send_mail


send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['to@example.com'], fail_silently=False)


from django.core.mail import EmailMultiAlternatives

def sendm(email):
    em = email
    title = u'Поздравляем Вас с 8 марта!'
    body = u'''
            <p> <a href="http://pressa.ru/rlogin/pressa--dot--test/71683"><img src="http://pressa.ru/static/images/story.jpg"></a> </p>'''
    msg = EmailMultiAlternatives(title, body, 'noreply@pressa.ru', (em,))
    msg.content_subtype = "html"
    msg.send() 


# Middleware
#http://www.webforefront.com/django/middlewaredjango.html


# -*- coding: utf-8 -*-
from django.conf import settings
import re

class TemplateInjector(object):
    
    def process_request(self, request):
        request.supervar = 'my super var'
        return None


    def process_response(self, request, response):
        #return if admin
        if request.get_full_path().startswith('/admin'):
            return response
        response.content = 'blabla'
        return response



# Template context_processors

def my_context_processor(request):
   return {'orders':'value'} 




from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def mytag():
    return request.my_var




# requests
# send
    import json
    data = {'user_id': user_id, 'issue_id': issue_id, 'mirror_id': MIRROR_ID, 'sign': sign}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    oo = requests.post(url, data=json.dumps(data), headers=headers).content
#get
    d = simplejson.loads(request.body)


# Signals

sender  — компонент посылающий сигнал;
receiver — компонент отвечающий за обработку сигнала.

Встроенные 
pre_init, post_init — посылаются соответственно до и после вызова метода  __init__ модели;
pre_save, post_save — соответственно посылаются до и после вызова метода save модели;
pre_delete, post_delete — по аналогии, до и после удаления объекта (вызов метода delete);
m2m_changed — отправляется при изменении объектов m2m (ManyToMany) связи;

pre_syncdb, post_syncdb — вызваются до и после запуска команды manage.py syncdb

request_started — посылается когда Django начинает обработку request;
request_finished — посылается после завершения обработки request;



from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender = Order)
def manage_with_order(instance, **kwargs):
    print 'work with order %s' % instance.pk


from django.db.models.signals import post_save
from app.models import Order

def manage_with_order(sender, instance, created, **kwargs):
    print 'work with order %s' % instance.pk

post_save.connect(send_update, sender=Order)




'debug_toolbar.panels.signals.SignalDebugPanel',


# Defining signals
import django.dispatch
payment_done = django.dispatch.Signal(providing_args=["order_id"])


def send_pizza(self, toppings, size):
    pizza_done.send(sender=self.__class__, toppings=toppings, size=size)





# Admin customization

class EventImagesInline(ImageCroppingMixin,admin.TabularInline):
    model = EventImages
    verbose_name_plural = u'Изображения'

class EventAdmin(ImageCroppingMixin,admin.ModelAdmin):
    ...
    inlines = [
        EventImagesInline,
    ]



# Custom settings




















