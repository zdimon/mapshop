from django.contrib import admin

# Register your models here.
from mapshop.models import Product, Category, ProductImages, Kiosk, Order
from image_cropping import ImageCroppingMixin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumb', 'price', 'rate', 'category')
    list_filter = ('name', 'price', 'rate')

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
    pass


admin.site.register(Order, OrderAdmin)
