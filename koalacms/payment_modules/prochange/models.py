# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

class PaymentSettings(models.Model):
    title               = models.CharField(max_length=100, verbose_name = _('Title'))
    description         = models.TextField(blank=True, null=True, verbose_name = _('Description'))
    is_active           = models.BooleanField(default=True, verbose_name = _('Active'))
    
    pro_client          = models.CharField(max_length=100, verbose_name = _('PRO_CLIENT'))
    pro_ra              = models.CharField(max_length=100, verbose_name = _('PRO_RA'))
    secret_key          = models.CharField(max_length=100, verbose_name = _('Secret Key'))
 
    def __unicode__(self):
        return u"%s" % self.title
    
    class Meta:
        verbose_name_plural = _('Yandex Money settings')