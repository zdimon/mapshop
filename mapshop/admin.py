from django.contrib import admin

# Register your models here.
from mapshop.models import Product, Category, ProductImages, Kiosk, Order, OrderItem, Client
from image_cropping import ImageCroppingMixin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug', 'thumb', 'price', 'rate', 'category', 'available')
    list_filter = ('name', 'price', 'rate')
    list_editable = ('available',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug')

class KioskAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Kiosk, KioskAdmin)


class ProductImagesAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('thumb', 'product', 'is_main')


admin.site.register(ProductImages, ProductImagesAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'session', 'kiosk', 'status')
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'ammount')


admin.site.register(OrderItem, OrderItemAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'email')


admin.site.register(Client, ClientAdmin)


