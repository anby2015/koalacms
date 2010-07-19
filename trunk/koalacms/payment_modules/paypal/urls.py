from django.conf.urls.defaults import *
import views
urlpatterns = patterns('',
    (r'^success/', views.success),
    (r'^fail/', views.fail),
)