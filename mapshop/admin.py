# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from mapshop.models import Product, Category, ProductImages, Kiosk, Order, OrderItem, Client, Preorder
from image_cropping import ImageCroppingMixin
from mptt.admin import MPTTModelAdmin
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.contrib import admin, messages
from django.shortcuts import redirect

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug', 'thumb', 'price', 'rate', 'category', 'ammount')
    list_filter = ('name', 'price', 'rate')
    list_editable = ('ammount',)

class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'name_slug', 'level', 'parent')

class KioskAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Kiosk, KioskAdmin)


class ProductImagesAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('thumb', 'product', 'is_main')


admin.site.register(ProductImages, ProductImagesAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    verbose_name_plural = u'Элементы'

def change_order_status(request, order_id,status):
    o = Order.objects.get(pk=order_id)
    o.status = status
    o.save()
    messages.success(request, u' Статус изменен!')
    return redirect(reverse('admin:mapshop_order_changelist'))

class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'session', 'kiosk', 'client', 'status', 'set_status_link')
    list_filter = ('status',)
    inlines = [
        OrderItemInline,
    ]

    def set_status_link(self, instance):
        if instance.id is None:
            return ''
        url_delivered = reverse('admin:change_order_status', args=[instance.id,6])
        url_delivering = reverse('admin:change_order_status', args=[instance.id,5])
        return u'<a href="{0}">{1}</a><br /><a href="{2}">{3}</a>'.format(url_delivered, 
                                                                          u'сделать "Доставлен"',
                                                                          url_delivering,
                                                                          u'сделать "Доставка"',      
                                                                          )
    set_status_link.allow_tags = True

    def get_urls(self):
        urls = super(OrderAdmin, self).get_urls()
        admin_urls = patterns(
            '',

            url(r'^change_status_order/(?P<order_id>\d+)/(?P<status>\d+)$',
                admin.site.admin_view(change_order_status),
                name="change_order_status")
        )
        return admin_urls + urls


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'ammount')


admin.site.register(OrderItem, OrderItemAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'email', 'kiosk')


admin.site.register(Client, ClientAdmin)

class PreorderAdmin(admin.ModelAdmin):
    list_display = ('product', 'contact', 'type', 'created_at')
    list_filter = ('type',)

admin.site.register(Preorder, PreorderAdmin)



