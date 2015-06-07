from django.contrib import admin

# Register your models here.
from mapshop.models import Product, Category, ProductImages, Kiosk
from image_cropping import ImageCroppingMixin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rate')
    list_filter = ('name', 'price', 'rate')

class CategoryAdmin(admin.ModelAdmin):
    pass

class KioskAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Kiosk, KioskAdmin)


class ProductImagesAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('thumb',)


admin.site.register(ProductImages, ProductImagesAdmin)
