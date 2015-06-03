from django.contrib import admin

# Register your models here.
from mapshop.models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rate')
    list_filter = ('name', 'price', 'rate')

class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)