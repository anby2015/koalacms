# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from models import PaymentSettings
from forms import SettingsForm
from django.utils.safestring import mark_safe
import hashlib
from shop.models import Order

def render(data=None):
    text = ''
    for settings in PaymentSettings.objects.filter(is_active=True):
        dict={'PRO_CLIENT': settings.pro_client, 'PRO_RA': settings.pro_ra, \
              'PRO_SUMMA': data['amount'], 'PRO_PAYMENT_DESC': data['description'], \
              'PRO_SUCCESS_URL': data['link'], 'PRO_PAYMENT_NO': data['id'], \
              'PRO_ORDER_ID': data['id'], 'PRO_SETTINGS_ID': settings.id
              }
        form = SettingsForm(initial=dict)
        text += u"<h3>%s</h3><p>%s</p><form action=http://merchant.prochange.ru/pay.pro method=POST>%s\
        <input type='submit' value='%s'></form>" % (settings.title, settings.description, form.as_p(), _('Go to payment'))
    
    return mark_safe(text)

def result(request):
    if not request.POST:
        return HttpResponse('YES')
    try:
        settings_id = int(request.POST['PRO_SETTINGS_ID'])
        settings = PaymentSettings.objects.get(id=settings_id)
        order_id = int(request.POST['PRO_ORDER_ID'])
        order = Order.objects.get(id = order_id)
        secret_key = settings.secret_key
        if secret_key != request.POST['PRO_SECRET_KEY']:
            return HttpResponseBadRequest(_('Error. Please refer to the administration'))
        if request.POST['PRO_SUMMA'] != order.amount:
            return HttpResponseBadRequest(_('Error. Please refer to the administration'))
        payment_data = _('Payment method')+": ProChange Yandex Money\n"+_("Transaction number")+": "+request.POST['PRO_TRANS_ID']+"\n"+\
        _("Amount of order")+": "+request.POST['PRO_SUMMA']+"\n"+_("Amount to purse")+": "+request.POST['PRO_SUMMA_OUT']+"\n"+\
        _("Payer purse")+": "+request.POST['PRO_PAYER_PURSE']+"\n"
        
        order.status = 'P'
        order.payment_data = payment_data
        order.save()
    except ValueError:
        return HttpResponseBadRequest(_('Error. Please refer to the administration'))