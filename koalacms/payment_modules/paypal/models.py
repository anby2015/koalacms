# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from shop.models import Payment
from django.db.models.signals import post_save

class PaymentSettings(models.Model):
    payment             = models.ForeignKey(Payment, unique=True)
    purse               = models.CharField(max_length=100, verbose_name = _('Purse'))
    secret_key          = models.CharField(max_length=100, verbose_name = _('Secret Key'))
    success_url         = models.CharField(max_length=100, verbose_name = _('Success URL'))
    fail_url         = models.CharField(max_length=100, verbose_name = _('Fail URL'))
 
    def __unicode__(self):
        return u"Purse #%s" % self.purse
    
    class Meta:
        verbose_name_plural = _('Payment settings')
        
#Добавляем в модель Payment id настроек модуля, перенести в shop.admin.PaymentAdmin
from shop.models import Payment 
def post_save_payment(sender, **kwargs):
    payment = kwargs['instance'].payment
    Payment.objects.update(settings_id = payment)
        
post_save.connect(post_save_payment, sender=PaymentSettings)  
