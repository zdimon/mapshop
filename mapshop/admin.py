from django.contrib import admin

# Register your models here.
from mapshop.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rate')
    list_filter = ('name', 'price', 'rate')

admin.site.register(Product, ProductAdmin)