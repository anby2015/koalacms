from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.contenttypes.models import ContentType
import mptt
from utils import *
from django.conf import settings
from hashlib import md5
import std3image, stdimage
from django import forms

"""
def category_upload_path(instance, filename, prefix = False):
    filename = str(instance.id) + '.jpg'
    return u"%s/%s" % ('category', filename)

def product_upload_path(instance, filename, prefix = False):
    filename = str(instance.product_id) + '.jpg'
    return u"%s/%s" % ('product', filename)
"""
class Category(models.Model):
    """
    Product's categories.
    """
    parent              = models.ForeignKey('self', null=True, blank=True, related_name='Children', verbose_name=_('Parent'))
    title               = models.CharField(max_length=100, verbose_name = _('Name'))
    description         = models.TextField(blank=True, verbose_name = _('Description'), help_text=_('Optional'))
    #image               = models.ImageField(upload_to=category_upload_path, default='category/default.jpg', blank=True, help_text=_('Optional'))
    image               = stdimage.StdImageField(upload_to='category', blank=True, null=True, size=settings.PRODUCT_CATEGORY_IMAGE)
    class Meta:
        ordering = ["tree_id", "id"]
        verbose_name = _('Categories')
        verbose_name_plural = _('Categories')
        
    class Admin:
        list_display = ('title')

    def __unicode__(self):
        title = self.level*"-" + self.title
        return u"%s" % title
    def get_absolute_url(self):
        return "/category/%i/" % self.id

mptt.register(Category)

class Product(models.Model):
    """
    Store products model.
    """
    title               = models.CharField(max_length=100, verbose_name = _('Name'))
    category            = models.ManyToManyField(Category)
    short_description   = models.TextField(blank=True, verbose_name = _('Short description'))
    description         = models.TextField(blank=True, verbose_name = _('Full description'))
    rating              = models.IntegerField(blank=True, default=0, verbose_name = _('Rating'))
    voted_users         = models.ManyToManyField(User, blank=True, through='VotedUsers', verbose_name = _('Voted users'))
    is_available        = models.BooleanField(default=True, verbose_name = _('Available'), help_text=_('Available in your shop?'))
    is_active           = models.BooleanField(default=True, verbose_name = _('Active'), help_text=_('Uncheck if you want hide this product from users'))
    pub_date            = models.DateTimeField(auto_now_add=True, verbose_name = _('Publication date'))

    def __unicode__(self):
        return u"%s" % self.title
    
    def get_absolute_url(self):
        return "/product/%i/" % self.id
    
    """
    def view_link(self):
        current_site = Site.objects.get(id=settings.SITE_ID)
        return u'<a href="%s://%s%s">%s</a>' % (
            settings.SITE_PROTOCOL, current_site,
            self.get_absolute_url(), _('view'))
    """
    class Meta:
        ordering = ["id"]
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        
class VotedUsers(models.Model):
    product            = models.ForeignKey(Product)
    user               = models.ForeignKey(User)
    rating             = models.IntegerField(verbose_name = _('Rating'))
        
class ProductCost(models.Model):
    """
    Product's costs.
    """
    product             = models.ForeignKey(Product)
    title               = models.CharField(max_length=100, blank=True, null=True, verbose_name = _('Option'))
    cost                = models.DecimalField(max_digits=20, decimal_places=2, verbose_name = _('Cost'))
    old_cost            = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name = _('Old cost'))

    def __unicode__(self):
        return u"%s %s" % (self.title, self.cost)
    
    class Meta:
        ordering = ["id"]
        verbose_name = _('Product\'s Costs')
        verbose_name_plural = _('Product\'s Costs')
        
class ProductImage(models.Model):
    """
    Product's images.
    """
    product             = models.ForeignKey(Product)
    title               = models.CharField(max_length=100, blank=True, verbose_name = _('Image title'), help_text=_('Optional'))
    image               = std3image.StdImageField(upload_to='product', blank=True, size=settings.PRODUCT_IMAGE_SIZE, cover_size=settings.PRODUCT_COVER_SIZE, thumbnail_size=settings.PRODUCT_THUMBNAIL_SIZE)
    #image              = models.ImageField(upload_to=product_upload_path)
    is_cover            = models.BooleanField(default=False, verbose_name = _('Cover'))
    
    def __unicode__(self):
        return u"%s" % self.title
    
    def thumb_img(self):
        path, image = str(self.image).split('/')
        return path+'/thumbs/'+image
    
    class Meta:
        ordering = ["id"]
        verbose_name = _('Product\'s Images')
        verbose_name_plural = _('Product\'s Images')

class Delivery(models.Model):
    #this override ContentType.__unicode__ representation
    def __unicode__(self):
        return self.app_label
    ContentType.__unicode__ = __unicode__
    
    title               = models.CharField(max_length=100, verbose_name = _('Title'))
    description         = models.TextField(blank=True, null=True, verbose_name = _('Description'))
    payments            = models.ManyToManyField(ContentType, limit_choices_to = {'model': 'paymentsettings'}, verbose_name = _('Payment modules'))
    cost                = models.IntegerField(verbose_name = _('Delivery cost'))
    free_from           = models.IntegerField(blank=True, null=True, verbose_name = _('Free from'))
    is_active           = models.BooleanField(default=True, verbose_name = _('Active'))
    
    def __unicode__(self):
        return u"%s" % self.title
    
    class Meta:
        ordering = ["id"]
        verbose_name_plural = _('Delivery method')
        verbose_name_plural = _('Delivery methods')

class Order(models.Model):
    STATUS_CHOICES = (
        ('N', _('New')),
        ('P', _('Process')),
        ('C', _('Completed')),
    )
    
    link                = models.CharField(max_length=100, verbose_name = _('Link'))
    products            = models.ManyToManyField(ProductCost, blank=True, through='OrderedProduct', verbose_name = _('Products'))
    delivery            = models.ForeignKey(Delivery, blank=True, null=True, verbose_name = _('Shipping method'))
    name                = models.CharField(max_length=100, verbose_name = _('Name'))
    email               = models.EmailField(blank=True, null=True, verbose_name = _('Email'))
    phone               = models.CharField(blank=True, null=True, max_length=100, verbose_name = _('Phone number'))
    address             = models.CharField(blank=True, null=True, max_length=100, verbose_name = _('Shipping address'))
    comment             = models.TextField(blank=True, null=True, verbose_name = _('Comment'))
    payment_data        = models.TextField(blank=True, null=True, verbose_name = _('Payment data'))
    amount              = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name = _('Total sum'))
    status              = models.CharField(max_length=1, choices=STATUS_CHOICES, default = 'N')
    user                = models.ForeignKey(User, blank=True, null=True)
    date                = models.DateTimeField(auto_now_add=True, verbose_name = _('Creation date'))
 
    def __unicode__(self):
        return u"Order #%s" % self.id
    
    class Meta:
        ordering = ["-id"]
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        
def post_save_order(sender, **kwargs):
    hash = md5(settings.SECRET_KEY + str(kwargs['instance'].id))
    kwargs['instance'].link = hash.hexdigest()
post_save.connect(post_save_order, sender=Order)      
        
class OrderedProduct(models.Model):
    product             = models.ForeignKey(ProductCost)
    order               = models.ForeignKey(Order)
    count               = models.IntegerField(verbose_name = _('Number of products'))