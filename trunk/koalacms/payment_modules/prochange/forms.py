from django import forms
from models import PaymentSettings

class SettingsForm(forms.Form):
    PRO_CLIENT          = forms.CharField(widget=forms.HiddenInput)
    PRO_RA              = forms.CharField(widget=forms.HiddenInput)
    PRO_SUMMA           = forms.CharField(widget=forms.HiddenInput)
    PRO_PAYMENT_DESC    = forms.CharField(widget=forms.HiddenInput)
    PRO_SUCCESS_URL     = forms.CharField(widget=forms.HiddenInput)
    PRO_ORDER_ID     = forms.IntegerField(widget=forms.HiddenInput)
    PRO_SETTINGS_ID     = forms.IntegerField(widget=forms.HiddenInput)