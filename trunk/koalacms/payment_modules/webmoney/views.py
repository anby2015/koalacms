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
        dict={'LMI_PAYMENT_AMOUNT': data['amount'], 'LMI_PAYMENT_DESC': data['description'], \
              'LMI_PAYMENT_NO': data['id'], 'LMI_PAYEE_PURSE': settings.purse, \
              'LMI_SUCCESS_URL': data['link'], 'LMI_FAIL_URL': data['link'], 'SETTINGS_ID': settings.id
              }
        form = SettingsForm(initial=dict)
        text += u"<h3>%s</h3><p>%s</p><form action='https://merchant.webmoney.ru/lmi/payment.asp' method='post' id='web_money_redirect_form'>%s\
        <input type='hidden' value='0' name='LMI_SIM_MODE'><input type='submit' value='%s'></form>" % (settings.title, settings.description, form.as_p(), _('Go to payment'))
    
    return mark_safe(text)

def result(request):
    if not request.POST or request.POST.get('LMI_PREREQUEST', None):
        return HttpResponse('YES')
    try:
        settings_id = int(request.POST['SETTINGS_ID'])
        settings = PaymentSettings.objects.get(id=settings_id)
        order_id = int(request.POST['LMI_PAYMENT_NO '])
        order = Order.objects.get(id = order_id)
        secret_key = settings.secret_key
        string_to_sign = ''.join([request.POST['LMI_PAYEE_PURSE'], request.POST['LMI_PAYMENT_AMOUNT'],
                                 request.POST['LMI_PAYMENT_NO'], request.POST['LMI_MODE'],
                                 request.POST['LMI_SYS_INVS_NO'], request.POST['LMI_SYS_TRANS_NO'],
                                 request.POST['LMI_SYS_TRANS_DATE'], secret_key,
                                 request.POST['LMI_PAYER_PURSE'], request.POST['LMI_PAYER_WM']])
        sign = hashlib.md5(string_to_sign).hexdigest().upper()
        if sign != request.POST['LMI_HASH']:
            return HttpResponseBadRequest(_('Error. Please refer to the administration'))
        if request.POST['LMI_PAYEE_PURSE'] != settings.purse:
            return HttpResponseBadRequest(_('Error. Please refer to the administration'))

        if request.POST['LMI_PAYMENT_AMOUNT'] != order.amount:
            return HttpResponseBadRequest(_('Error. Please refer to the administration'))

        if request.POST['LMI_MODE']=="1":
            payment_data = _("Payment method: WebMoney")+"\n"+_("Purse")+": "+request.POST['LMI_PAYEE_PURSE']+"\n"+\
            _("Amount")+": "+request.POST['LMI_PAYMENT_AMOUNT']+"\n"+_("Mode")+": Test\n"+\
            _("Invoice number")+": "+request.POST['LMI_SYS_INVS_NO']+"\n"+\
            _("Transaction number")+": "+request.POST['LMI_SYS_TRANS_NO']+"\n"+\
            _("Date")+": "+request.POST['LMI_SYS_TRANS_DATE']+"\n"+\
            _("Payer purse")+": "+request.POST['LMI_PAYER_PURSE']+"\n"+\
            _("Payer WMID")+": "+request.POST['LMI_PAYER_WM']+"\n"
        else:
            payment_data = _("Payment method: WebMoney")+"\n"+_("Purse")+": "+request.POST['LMI_PAYEE_PURSE']+"\n"+\
            _("Amount")+": "+request.POST['LMI_PAYMENT_AMOUNT']+"\n"+\
            _("Invoice number")+": "+request.POST['LMI_SYS_INVS_NO']+"\n"+\
            _("Transaction number")+": "+request.POST['LMI_SYS_TRANS_NO']+"\n"+\
            _("Date")+": "+request.POST['LMI_SYS_TRANS_DATE']+"\n"+\
            _("Payer purse")+": "+request.POST['LMI_PAYER_PURSE']+"\n"+\
            _("Payer WMID")+": "+request.POST['LMI_PAYER_WM']+"\n"
        order.status = 'P'
        order.payment_data = payment_data
        order.save()
    except ValueError:
        return HttpResponseBadRequest(_('Error. Please refer to the administration'))
