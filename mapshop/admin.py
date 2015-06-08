from django.contrib import admin

# Register your models here.
from mapshop.models import Product, Category, ProductImages
from image_cropping import ImageCroppingMixin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rate', 'category')
    list_filter = ('name', 'price', 'rate')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)



class ProductImagesAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('thumb',)


admin.site.register(ProductImages, ProductImagesAdmin)
