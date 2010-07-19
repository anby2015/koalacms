# -*- coding: utf-8 -*-
from shop.models import Product, ProductCost, ProductImage, Category
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('blocks/cart.html', takes_context=True)
def cart(context):
    if 'products' in context['request'].session.keys():
        prds= context['request'].session['products']
        return {'in_cart': len(prds),}
    else:
        return {'in_cart': 0,}

@register.inclusion_tag('blocks/search.html')
def search_block():
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}

@register.inclusion_tag('blocks/categories_menu.html')
def categories_menu():
    return
    
@register.inclusion_tag('blocks/new_products.html')
def new_products():
    products_queryset = Product.objects.filter(is_active=True)[:5]
    #Mysql don't support LIMIT with IN in one qeury, so:
    product_ids = list(products_queryset.values_list('id', flat=True))

    productimages_queryset = ProductImage.objects.filter(is_cover=True).filter(product__in=product_ids)
    productcosts_queryset = ProductCost.objects.filter(product__in=product_ids)
    
    products_dict = dict((product.pk, product) for product in products_queryset)
    
    for img in productimages_queryset:
        products_dict[img.product_id].cover = img
            
    for cost in productcosts_queryset:
        if not hasattr(products_dict[cost.product_id], 'cost'):
            products_dict[cost.product_id].cost = cost
        elif cost.cost < products_dict[cost.product_id].cost.cost:
            products_dict[cost.product_id].cost = cost

    return {'products': products_dict}
   
class PaginatorNode(template.Node):
    def __init__(self, preserve_keys):
        self.preserve_keys = preserve_keys

    def render(self, context):
        paginator = context['paginator']
        page = context['page_obj']
        context['previous_list'] = [p + 1 for p in range(page.number - 1)]
        context['next_list'] = [p + 1 for p in range(page.number - 1 + 1, paginator.num_pages)]
        t = template.loader.get_template('paginator.html')
        result = t.render(context)

        preserve_values = dict([(k, context[k]) for k in self.preserve_keys if k in context])
        # Hack: converting timeless datetimes to a nice format
        for k in preserve_values:
            if isinstance(preserve_values[k], datetime):
                dt = preserve_values[k]
                if dt.hour == dt.minute == dt.second == 0:
                    preserve_values[k] = dt.strftime('%Y-%m-%d')
        if preserve_values:
            param_str = u'&amp;' + escape(urlencode(preserve_values, True))
            result = re.sub(ur'(\?page=\d*)', ur'\1' + param_str, result)

        return result
    
@register.tag
def paginator(parser, token):
    '''
    Выводит навигатор по страницам. Данные берет из контекста в том же
    виде, как их туда передает generic view "object_list".
    '''
    bits = token.contents.split()
    if len(bits) > 1:
        preserve_keys = bits[1].split(',')
    else:
        preserve_keys = []
    return PaginatorNode(preserve_keys)
 

"""
@register.filter
def strip(value):
    return str(value).strip('0')
"""