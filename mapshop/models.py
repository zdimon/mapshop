from django.db import models


class Kiosk(models.Model):
    ''' Класс Киоск содержит все данные о киоске (адрес, фото, мнемонику, широту, долготу) '''
    address = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='media')
    mnemonic = models.CharField(max_length=5)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Product(models.Model):
    ''' Класс Продукт содержит данные о товарах (имя, фото, цену, описание, наличие товара)'''
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=u"Стоимость (руб)")
    description = models.CharField(max_length=200)
    available = models.BooleanField()



class ProductImages(models.Model):
    ''' картинки товаров '''
    product = models.ForeignKey('Product')
    image  = models.ImageField(upload_to='product', verbose_name=u'Изображение')


   
class Client(models.Model):
    ''' Класс Клиент содержит данные о клиенте (емайл, телефон, параметр уведомления по емайлу, параметр уведомления по телефону)  '''
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    notice_email = models.BooleanField()
    notice_phone = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


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
    kiosk = models.ForeignKey('Kiosk') 
    created_at = models.DateTimeField(auto_now_add=True)
    

class OrderItem(models.Model):
    '''Элементы заказа'''
    basket = models.ForeignKey('Basket')
    product = models.ForeignKey('Product') 
    created_at = models.DateTimeField(auto_now_add=True)
    


