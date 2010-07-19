from django import forms
from models import PaymentSettings

class SettingsForm(forms.Form):
    LMI_PAYMENT_AMOUNT = forms.CharField(widget=forms.HiddenInput)
    LMI_PAYMENT_DESC = forms.CharField(widget=forms.HiddenInput)
    LMI_PAYMENT_NO = forms.CharField(widget=forms.HiddenInput)
    LMI_PAYEE_PURSE = forms.CharField(widget=forms.HiddenInput)
    LMI_SUCCESS_URL = forms.CharField(widget=forms.HiddenInput)
    LMI_SUCCESS_METHOD = forms.IntegerField(widget=forms.HiddenInput, initial=1)
    LMI_FAIL_URL = forms.CharField(widget=forms.HiddenInput)
    LMI_FAIL_METHOD = forms.IntegerField(widget=forms.HiddenInput, initial=1)
