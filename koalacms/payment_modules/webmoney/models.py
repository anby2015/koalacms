# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
#from shop.models import Payment
from django.db.models.signals import post_save

class PaymentSettings(models.Model):
    title               = models.CharField(max_length=100, verbose_name = _('Title'))
    description         = models.TextField(blank=True, null=True, verbose_name = _('Description'))
    is_active           = models.BooleanField(default=True, verbose_name = _('Active'))
    
    purse               = models.CharField(max_length=100, verbose_name = _('Purse'))
    secret_key          = models.CharField(max_length=100, verbose_name = _('Secret Key'))
 
    def __unicode__(self):
        return u"%s" % self.title
    
    class Meta:
        verbose_name_plural = _('WebMoney settings')
        
#Добавляем в модель Payment id настроек модуля, перенести в shop.admin.PaymentAdmin
"""
from shop.models import Payment 
def post_save_payment(sender, **kwargs):
    payment = kwargs['instance'].payment
    Payment.objects.update(settings_id = payment)
        
post_save.connect(post_save_payment, sender=PaymentSettings)  
"""