# -*- coding: utf-8 -*-
from celery import task
from termcolor import colored
from mapshop.models import Preorder
from django.template import loader, Context
from django.contrib.sites.models import get_current_site
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from settings import EMAIL_REPLY

def sendm(email, title, body):
    msg = EmailMultiAlternatives(title, body, EMAIL_REPLY, (email,))
    msg.content_subtype = "html"
    msg.send() 


@task(name='test_task')
def test_task(product):
    site = Site.objects.get_current()
    for i in Preorder.objects.all().filter(type='email'):
        t = loader.get_template('mapshop/mail_templates/remaind_mail.tpl')
        print colored('send email to %s' % i.contact, 'red')
        link_url = ''.join(['http://', site.domain, i.product.get_absolute_url()])
        link_html = '<a href="%s">%s</a>' % (link_url,i.product)
        c = Context({'site_name': site.name, 'product': i.product, 'link': link_html})
        print colored(t.render(c), 'yellow')
        sendm(i.contact,u'Уведомление о поступлении товара', t.render(c))
    for i in Preorder.objects.all().filter(type='phone'):
        print colored('Sending SMS to %s' % i.contact, 'white')


@task(name='change_order_status_task')
def change_order_status_task(order):
    if order.status==6:
        t = loader.get_template('mapshop/mail_templates/order_delivered.tpl')
        title = u'Ваш товар доставлен.' 
    elif order.status==5:
        t = loader.get_template('mapshop/mail_templates/order_delivering.tpl')
        title = u'Ваш товар передан в службу доставки.'
    #try:
    c = Context({'order': order})
    print colored(t.render(c), 'yellow')
    sendm(order.client.email,title, t.render(c))
    #except:
    #    pass


