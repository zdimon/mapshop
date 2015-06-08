# -*- coding: utf-8 -*-
from django.db import models
from image_cropping import ImageRatioField
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
import pytils
from django.core.urlresolvers import reverse

class Kiosk(models.Model):
    u''' Класс Киоск содержит все данные о киоске (адрес, фото, мнемонику, широту, долготу) '''
    address = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='media')
    mnemonic = models.CharField(max_length=5)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Category(models.Model):
    ''' Класс категори товаров'''
    name = models.CharField(max_length=200)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    def get_absolute_url(self):
       return reverse("catalog_filter", kwargs={"slug": self.name_slug})
    def __unicode__(self):
        return self.name
    def save(self, **kwargs):
        if not self.id:
            self.name_slug = pytils.translit.slugify(self.name)
        return super(Category, self).save(**kwargs)


class Product(models.Model):
    u''' Класс Продукт содержит данные о товарах (имя, фото, цену, описание, наличие товара)'''
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=u"Стоимость (руб)")
    description = models.CharField(max_length=200)
    available = models.BooleanField(default=False) 
    rate = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True)

    def __unicode__(self):
        return self.name



class ProductImages(models.Model):
    from easy_thumbnails.files import get_thumbnailer
    u''' картинки товаров '''
    product = models.ForeignKey('Product')
    image  = models.ImageField(upload_to='product', verbose_name=u'Изображение')
    cropping = ImageRatioField('image', '430x360')
    @property
    def thumb(self):
        #try:
        thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
            'size': (100, 100),
            'box': self.cropping,
            'crop': True,
            'detail': True,
        }).url
        return mark_safe(u'<img src="%s" />' % thumbnail_url)
        #except:
        #    return 'no image'


   
class Client(models.Model):
    u''' Класс Клиент содержит данные о клиенте (емайл, телефон, параметр уведомления по емайлу, параметр уведомления по телефону)  '''
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
    postal_index_org = models.CharField(max_length=10)
    inn_org = models.CharField(max_length=10)
    kpp_org = models.CharField(max_length=10)
    account_org = models.CharField(max_length=16)
    bank_org = models.CharField(max_length=100)
    cor_account_org = models.CharField(max_length=16)
    bik_org = models.CharField(max_length=9)



class Order(models.Model):
    u''' заказы по клиенту '''
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
    u'''Элементы заказа'''
    order = models.ForeignKey('Order')
    product = models.ForeignKey('Product') 
    created_at = models.DateTimeField(auto_now_add=True)
    

class Preorder(models.Model):
    u'''Предзаказ содержит данные о предзаказах по клиентам'''
    product = models.ForeignKey('Product')
    client =  models.ForeignKey('Client')
