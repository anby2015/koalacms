# -*- coding: utf-8 -*-
from django.contrib import admin
from shop.models import *
from mpttadmin import MpttAdmin
from django.conf import settings
from django.db import models


class ProductAdmin(admin.ModelAdmin):
    exclude = ('rating',)
    list_display = ('title', 'is_available', 'is_active', 'pub_date', )
    search_fields = ('title', 'description')
    list_filter = ('category', 'is_available', 'is_active',)
    #date_hierarchy = 'pub_date'
    #ordering = ('-pub_date',)
    
    class ProductCostInline(admin.TabularInline):
        model = ProductCost
        extra = 1
    class ProductImageInline(admin.TabularInline):
        model = ProductImage
        extra = 1
        #template = 'admin/imagetabular.html'
    
    inlines = [ProductCostInline, ProductImageInline,]
 
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(MpttAdmin):
    fields = ('parent', 'title', 'description', 'image')
    tree_title_field = 'title'
    #tree_display = ('title', '')
    
    class Meta:
        model = Category
admin.site.register(Category, CategoryAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "address", "delivery", "payment_data", "comment", "amount",  "date", "status")
    search_fields = ('name', 'email', 'phone', 'address', 'payment_data', 'comment')
    list_filter = ("status", "date", "delivery",)
admin.site.register(Order, OrderAdmin)

admin.site.register(Delivery)