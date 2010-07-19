from django.conf.urls.defaults import *
from pages.views import *
from users.views import *
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^django_store/', include('django_store.foo.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
)

from shop.views import *
urlpatterns += patterns('',
    (r'^$', index),                   
    (r'^product/(\d{1,7})/$',  product),
    (r'^vote/(\d{1,4})/$',  vote),
    (r'^category/(?P<category>\d{1,4})/$',  listing),
    (r'^page/(\d{1,4})/$', page),
    (r'^add_to_cart/$', add_to_cart),
    (r'^cart/$', cart),
    (r'^order/([a-z0-9]+)/$', order),
    (r'^drop_from_cart/(\d{1,4})/$', drop_from_cart),
    (r'^cart/$', cart),
    (r'^products/$', listing),
    (r'^search/$', search),
)
from django.contrib.auth.views import login, logout

urlpatterns += patterns('',
    (r'^accounts/profile/$', redirect_to, {'url': '/'}),
    (r'^accounts/login/$', redirect_to, {'url': '/login'}),
    (r'^login/$',  login, {'template_name': 'login.html'}),
    (r'^logout/$', logout, {'redirect_field_name': 'next'}),
    (r'^register/$',  register),
    (r'^ajax_register_form/$',  ajax_register_form),
    #(r'^user/(\d{1,4})/$',  user),
    #(r'^user/(\d{1,4})/edit/$',  edit),
    #(r'^user/(\d{1,4})/comments/$',  comments),
)
import webmoney.urls
urlpatterns += patterns('',
    (r'^webmoney/', include(webmoney.urls)),              
)
from django.conf import settings
urlpatterns += patterns('',
        (r'^robots.txt$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'path': "robots.txt"}),
        (r'^favicon.ico$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'path': "favicon.ico"}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
