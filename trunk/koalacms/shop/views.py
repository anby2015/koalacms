# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import random
import itertools
from django.conf import settings
from decimal import Decimal
from django.contrib.sites.models import Site
from shop.models import Category, Product, ProductCost, ProductImage, Delivery, OrderedProduct, Order, VotedUsers
from shop.forms import RecipientForm, OrderForm, SearchForm

def index(request):
    products_queryset = Product.objects.filter(is_active=True)[:8]
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

    return render_to_response('index.html', {'products': products_dict},context_instance=RequestContext(request))

def product(request, i):
    product = get_object_or_404(Product, id=i, is_active=True)
    categories = []
    for category in product.category.all():
        categories.append(itertools.chain(category.get_ancestors(), Category.objects.filter(id=category.id)))
    costs = ProductCost.objects.filter(product=i)
    images = ProductImage.objects.filter(product=i)
    if images:
        covers = [img for img in images if img.is_cover]
        if covers:
            cover = random.choice(covers)
        else:
            cover = random.choice(images)
        return render_to_response('product.html', {'product': product, 'categories': categories, 'costs': costs, 'images': images, 'cover': cover}, context_instance=RequestContext(request))
    return render_to_response('product.html', {'product': product,'costs': costs}, context_instance=RequestContext(request))

def listing(request, category=None):
    categories = None
    if category:
        category = get_object_or_404(Category, pk=category)
        categories = itertools.chain(category.get_ancestors(), Category.objects.filter(id=category.id))
        products_queryset = Product.objects.filter(category=category).filter(is_active=True)
        #product_ids = products_queryset.values_list('id', flat=True)
        productimages_queryset = ProductImage.objects.filter(product__category=category).filter(is_cover=True).filter(product__in=products_queryset)
        productcosts_queryset = ProductCost.objects.filter(product__category=category).filter(product__is_active=True).filter(product__in=products_queryset)  
                
    else:
        products_queryset = Product.objects.filter(is_active=True)
        productimages_queryset = ProductImage.objects.filter(is_cover=True)
        productcosts_queryset = ProductCost.objects.all()

    products_dict = dict((product.pk, product) for product in products_queryset)
    for img in productimages_queryset:
        products_dict[img.product_id].cover = img
            
    for cost in productcosts_queryset:
        try:
             products_dict[cost.product_id].costs.append(cost)
        except AttributeError:
            products_dict[cost.product_id].costs= []
            products_dict[cost.product_id].costs.append(cost)

    product_list = list(products_dict.values())
    
    #START paginator creation
    paginator = Paginator(product_list, settings.PRODUCTS_PER_PAGE)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404()
    #END paginator creation

    return render_to_response('product_list.html', {"paginator":paginator,"page_obj":products, "categories": categories}, context_instance=RequestContext(request))

def add_to_cart(request):
    #if request.is_ajax():
    if request.method == 'POST':
        try:
            if 'cost' not in request.POST.keys():
                assert ProductCost.DoesNotExist
            cost = int(request.POST['cost'])
            product_opt = ProductCost.objects.get(id=cost)
            if 'products' not in request.session.keys():
                request.session['products'] = []
            if cost in request.session['products']:
                return HttpResponseRedirect('/product/'+str(product_opt.product_id))
                
            array = request.session['products']
            array.append(cost)
            request.session['products'] = array
            #assert False
            return HttpResponseRedirect('/product/'+str(product_opt.product_id))
        except ProductCost.DoesNotExist:
            return HttpResponseRedirect('/products/')
    return HttpResponseRedirect('/products/')

def cart(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if request.user.is_authenticated():
            del(form.fields['captcha'])
            form.full_clean()
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            data = form.cleaned_data
            # Заполняем у модели Order товары
            prds = ProductCost.objects.filter(id__in=data['products'].keys())
            total_cost = 0
            for prd in prds:
                op = OrderedProduct(product=prd, order=order, count=data['products'][prd.id])
                op.save()
                total_cost += Decimal(prd.cost) * data['products'][prd.id]
            if total_cost < data['delivery'].free_from:
                total_cost += Decimal(data['delivery'].cost)
            order.amount = str(total_cost)
            order.save()
            return HttpResponseRedirect('/order/'+str(order.link))      
    else:
        form = OrderForm()
        products = []
        if request.user.is_authenticated():
            del(form.fields['captcha'])
    if 'products' in request.session.keys() and request.session['products']:
        products = ProductCost.objects.filter(id__in=request.session['products'])
            
    return render_to_response('cart.html', {'products': products, 'deliveries': Delivery.objects.all(),'order_form': form, 'max_products': range(1, settings.PDORUCT_MAX_ORDER+1)}, context_instance=RequestContext(request))

def order(request, order):
    order = get_object_or_404(Order, link=order)
    products = OrderedProduct.objects.filter(order = order)
    if order.amount-order.delivery.cost > order.delivery.free_from:
            order.delivery.cost = _("Free")
    if order.status == 'P':
        order.title = _("Order # %s has been paid. Not processed" % order.id)
        return render_to_response('order.html',{'order': order, 'products': products}, context_instance=RequestContext(request))
    elif order.status == 'C':
        order.title = _("Order # %s has been paid. Processed" % order.id)
        return render_to_response('order.html',{'order': order, 'products': products}, context_instance=RequestContext(request))
    else:
        order.title = _("Order # %s not paid" % order.id )
        current_site = Site.objects.get(id=settings.SITE_ID)
        data = {'id': order.id, 'link': u'%s://%s/order/%s' % (settings.SITE_PROTOCOL, current_site, order.link),\
                'description': _('Order # %s' % order.id),'amount': order.amount, 'person': order.name,\
                'email': order.email, 'phone': order.phone, 'address': order.address} 
        #Start magic
        payments = []
        for payment in order.delivery.payments.all():
            exec('import '+payment.app_label+'.views')
            exec("text = "+payment.app_label+".views.render(data)")
            payment.render = text
            payments.append(payment)
        #end magic
        return render_to_response('order.html',{'order': order, 'products': products, 'payments': payments}, context_instance=RequestContext(request))
    
        
def drop_from_cart(request, product):
    try:
        product = int(product)
        array = request.session['products']
        array.remove(product)
        request.session['products'] = array
    except ValueError:
        pass
    return HttpResponseRedirect('/cart/')

@login_required
def vote(request, product_id):
    if request.method == 'POST':
        try:
            rating = int(request.POST['vote'])
        except ValueError:
              HttpResponse(False)
        if "vote" in request.POST.keys() and rating in range(1,6):
            try:
                product = Product.objects.get(id=product_id)
                vote, created = VotedUsers.objects.get_or_create(product=product, user=request.user, defaults={'rating': rating})
                if not created:
                    product.rating -= vote.rating
                    vote.rating = rating
                    vote.save()
                voted_count = VotedUsers.objects.filter(product=product).count()
                product.rating = (product.rating + rating) / voted_count
                product.save()
                return HttpResponse(True)
            except Product.DoesNotExist:
                HttpResponse(False)
    return HttpResponse(False)

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        category = form.cleaned_data['category']
        search = form.cleaned_data['search']
        from django.db.models import Q
        if category != "0":
            
            products_queryset = Product.objects.filter(category=category).filter(is_active=True).filter(Q(title__icontains=search) | Q(description__icontains=search))
            productimages_queryset = ProductImage.objects.filter(product__category=category).filter(is_cover=True).filter(product__in=products_queryset)
            productcosts_queryset = ProductCost.objects.filter(product__category=category).filter(product__is_active=True).filter(product__in=products_queryset)         
        else:
            products_queryset = Product.objects.filter(is_active=True).filter(Q(title__icontains=search) | Q(description__icontains=search))
            productimages_queryset = ProductImage.objects.filter(is_cover=True).filter(product__in=products_queryset)
            productcosts_queryset = ProductCost.objects.all().filter(product__in=products_queryset)
       
        products_dict = dict((product.pk, product) for product in products_queryset)
        
        for img in productimages_queryset:
            i =img.product_id
            products_dict[img.product_id].cover = img
                
        for cost in productcosts_queryset:
            try:
                 products_dict[cost.product_id].costs.append(cost)
            except AttributeError:
                products_dict[cost.product_id].costs= []
                products_dict[cost.product_id].costs.append(cost)
    
        
        return render_to_response('search.html', {"products":products_dict,"form": form}, context_instance=RequestContext(request))
      
    return render_to_response('search.html', {"form": form}, context_instance=RequestContext(request))