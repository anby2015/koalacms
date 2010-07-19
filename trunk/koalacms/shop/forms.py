from django import forms
from captcha import CaptchaField
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from hashlib import md5
from models import Delivery, ProductCost, Order, OrderedProduct, Category
import settings

class DeliveryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        cost = u"%s" % _("Cost")
        free_from = u"%s" % _("Free from")
        if obj.free_from:
            return mark_safe("<table><tr><td><b> %s </b><p> %s </p></td><td class='form_cost'><b> %s: %s</b><br><b>%s: %s</b></td></tr></table>" % (obj.title, obj.description, cost, obj.cost, free_from, obj.free_from))
        else:
            return mark_safe("<table><tr><td><b> %s </b><p> %s </p></td><td class='form_cost'><b> %s: %s</b></td></tr></table>" % (obj.title, obj.description, cost, obj.cost))

class RecipientForm(forms.Form):
    delivery        = DeliveryChoiceField(queryset=Delivery.objects.all(), widget=forms.RadioSelect(), empty_label = None,label=_('Delivery method'))
    name            = forms.CharField(max_length=100, label=_('Name, Sername'))
    email           = forms.EmailField(label=_('Email'))
    phone           = forms.CharField(required=False, max_length=20, label=_('Phone number'))
    address         = forms.CharField(max_length=200, label=_('Shipping Address'))
    comment         = forms.CharField(required=False, widget=forms.Textarea({'cols': '50', 'rows': '5'}), max_length=1000, label=_('Comment to order'))
    #bid = forms.IntegerField(widget=forms.HiddenInput)
    captcha = CaptchaField(label=_('Verification'), options={'fgcolor': '#000000', 'bgcolor': '#ffffff', 'minmaxheight': (20,25), 'alphabet': "abdeghkmnqrt2346789", 'imagesize': (110,40)})
    
    def clean(self):
        products = dict((int(key.strip('prd_')), int(value)) for key, value in self.data.items() if 'prd_' in key)
        if not products:
            raise forms.ValidationError(_("You cart is empty"))
        ids = ProductCost.objects.values_list('id', flat=True)
        for key, value in products.items():
            # Those products realy from site?
            if value > settings.PDORUCT_MAX_ORDER+1 or key not in ids:
                raise forms.ValidationError(_("You changed too many count of products"))
        self.cleaned_data['products'] = products
        return self.cleaned_data
    
class OrderForm(forms.ModelForm):
    delivery        = DeliveryChoiceField(queryset=Delivery.objects.all(), widget=forms.RadioSelect(), empty_label = None,label=_('Delivery method'))
    captcha         = CaptchaField(label=_('Verification'), options={'fgcolor': '#000000', 'bgcolor': '#ffffff', 'minmaxheight': (20,25), 'alphabet': "abdeghkmnqrt2346789", 'imagesize': (110,40)})
    comment         = forms.CharField(required=False, widget=forms.Textarea({'cols': '50', 'rows': '5'}), max_length=1000, label=_('Comment'))
    class Meta:
        model = Order
        exclude = ('link', 'products', 'status', 'payment_data', 'amount', 'user')
        
    def clean(self):
        products = dict((int(key.strip('prd_')), int(value)) for key, value in self.data.items() if 'prd_' in key)
        if not products:
            raise forms.ValidationError(_("Your cart is empty"))
        ids = ProductCost.objects.values_list('id', flat=True)
        for key, value in products.items():
            # Those products realy from site?
            if value > settings.PDORUCT_MAX_ORDER+1 or key not in ids:
                raise forms.ValidationError(_("You changed too many count of products"))
        self.cleaned_data['products'] = products
        #self.cleaned_data['link'] = md5(str(random(1,100)))
        return self.cleaned_data
    
class SearchForm(forms.Form):
    choices=list(Category.objects.values_list('id', 'title').filter(parent=None))
    choices.insert(0,(0,_('All')))
    category        = forms.ChoiceField(choices=choices,  label=_('Category'))
    search          = forms.CharField(min_length=4, max_length=100, label=_('Searching'))
