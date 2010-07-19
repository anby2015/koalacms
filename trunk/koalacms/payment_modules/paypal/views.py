# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from models import PaymentSettings
from forms import SettingsForm
from django.utils.safestring import mark_safe
import hashlib
from shop.models import Order

def render(settings_id, data=None):
    settings = PaymentSettings.objects.get(id=settings_id)
    dict={'LMI_PAYMENT_AMOUNT': data['amount'], 'LMI_PAYMENT_DESC': data['description'], \
          'LMI_PAYMENT_NO': data['id'], 'LMI_PAYEE_PURSE': settings.purse, \
          'LMI_SUCCESS_URL': settings.success_url, 'LMI_FAIL_URL': settings.fail_url}
    
    form = SettingsForm(initial=dict)
    form = mark_safe("<form action='https://merchant.webmoney.ru/lmi/payment.asp' method='post' id='web_money_redirect_form'>"+form.as_p()+\
    "<input type='hidden' value='0' name='LMI_SIM_MODE'><input type='submit' value='"+_('Go to payment').decode()+"'></form>")
    
    return form

def success(request):
    if not request.POST or request.POST.get('LMI_PREREQUEST', None):
        return HttpResponse('YES')

    string_to_sign = ''.join([request.POST['LMI_PAYEE_PURSE'], request.POST['LMI_PAYMENT_AMOUNT'],
                             request.POST['LMI_PAYMENT_NO'], request.POST['LMI_MODE'],
                             request.POST['LMI_SYS_INVS_NO'], request.POST['LMI_SYS_TRANS_NO'],
                             request.POST['LMI_SYS_TRANS_DATE'], secret_key,
                             request.POST['LMI_PAYER_PURSE'], request.POST['LMI_PAYER_WM']])
    sign = hashlib.md5(string_to_sign).hexdigest().upper()
    if sign != request.POST['LMI_HASH']:
        return HttpResponseBadRequest(_('Error. Please refer to the administration'))
    if request.POST['LMI_MODE']=="1":
        payment_data = _("Payment method: WebMoney")+"\n"+_("Purse")+": "+request.POST['LMI_PAYEE_PURSE']+"\n"+\
        _("Amount")+": "+request.POST['LMI_PAYMENT_AMOUNT']+"\n"+_("Mode")+": Test\n"+\
        _("WebMoney invoice number")+": "+request.POST['LMI_SYS_INVS_NO']+"\n"+\
        _("WebMoney transaction number")+": "+request.POST['LMI_SYS_TRANS_NO']+"\n"+\
        _("Date")+": "+request.POST['LMI_SYS_TRANS_DATE']+"\n"+\
        _("Payer purse")+": "+request.POST['LMI_PAYER_PURSE']+"\n"+\
        _("Payer WMID")+": "+request.POST['LMI_PAYER_WM']+"\n"
    else:
        payment_data = _("Payment method: WebMoney")+"\n"+_("Purse")+": "+request.POST['LMI_PAYEE_PURSE']+"\n"+\
        _("Amount")+": "+request.POST['LMI_PAYMENT_AMOUNT']+"\n"+\
        _("WebMoney invoice number")+": "+request.POST['LMI_SYS_INVS_NO']+"\n"+\
        _("WebMoney transaction number")+": "+request.POST['LMI_SYS_TRANS_NO']+"\n"+\
        _("Date")+": "+request.POST['LMI_SYS_TRANS_DATE']+"\n"+\
        _("Payer purse")+": "+request.POST['LMI_PAYER_PURSE']+"\n"+\
        _("Payer WMID")+": "+request.POST['LMI_PAYER_WM']+"\n"
    Order.objects.update(status = 'P', payment_data = payment_data)

def fail(request):
    return HttpResponse('Fail. Please refer to the administration')


