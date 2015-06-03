# -*- coding: utf-8 -*-
from django.db import models


class Kiosk(models.Model):
    ''' Класс Киоск содержит все данные о киоске (адрес, фото, мнемонику, широту, долготу) '''
    address = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='media')
    mnemonic = models.CharField(max_length=5)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Category(models.Model):
    ''' Класс категори товаров'''
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    ''' Класс Продукт содержит данные о товарах (имя, фото, цену, описание, наличие товара)'''
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=u"Стоимость (руб)")
    description = models.CharField(max_length=200)
    available = models.BooleanField()
    rate = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True)

    def __unicode__(self):
        return self.name



class ProductImages(models.Model):
    ''' картинки товаров '''
    product = models.ForeignKey('Product')
    image  = models.ImageField(upload_to='product', verbose_name=u'Изображение')


   
class Client(models.Model):
    ''' Класс Клиент содержит данные о клиенте (емайл, телефон, параметр уведомления по емайлу, параметр уведомления по телефону)  '''
    TREATMENTS = (
        (u'Уважаемый', u'Уважаемый'),
        (u'Уважаемая', u'Уважаемая'),
    )
    treatment = models.CharField(verbose_name=u'Формат обращения',
                                    choices=TREATMENTS,
                                    default=u'Уважаемый',
                                    max_length=10)
    surname = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    add_phone = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField()
    birthday = models.DateField()
    notice_email = models.BooleanField()
    notice_phone = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_organization = models.BooleanField(default='True')
    name_org = models.CharField(max_length=100)
    address_org = models.CharField(max_length=200)
    postal_index_org = models.DecimalField(max_digits=5, decimal_places=2)
    inn_org = models.DecimalField(max_digits=10, decimal_places=2)
    kpp_org = models.DecimalField(max_digits=10, decimal_places=2)
    account_org = models.DecimalField(max_digits=16, decimal_places=2)
    bank_org = models.CharField(max_length=100)
    cor_account_org = models.DecimalField(max_digits=16, decimal_places=2)
    bik_org = models.DecimalField(max_digits=9, decimal_places=2)


class Order(models.Model):
    ''' заказы по клиенту '''
    STATUSES = (
        (u'Новый', u'Новый'),
        (u'Оплачен', u'Оплачен'),
        (u'Доставка', u'Доставка'),
        (u'Доставлен', u'Доставлен'),
        (u'Отказ', u'Отказ'),
    )
    status = models.CharField(verbose_name=u'Статус заказа',
                                    choices=STATUSES,
                                    default=u'Новый',
                                    max_length=10)
    client = models.ForeignKey('Client') 
    kiosk = models.ForeignKey('Kiosk', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    

class OrderItem(models.Model):
    '''Элементы заказа'''
    order = models.ForeignKey('Order')
    product = models.ForeignKey('Product') 
    created_at = models.DateTimeField(auto_now_add=True)
    

class Preorder(models.Model):
    '''Предзаказ содержит данные о предзаказах по клиентам'''
    product = models.ForeignKey('Product')
    client =  models.ForeignKey('Client')
