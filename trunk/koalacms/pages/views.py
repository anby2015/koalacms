from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response
from pages.models import *
from django.utils.translation import ugettext_lazy as _

def page(request, i):
    i = int(i)
    try:
        page = Page.objects.get(id=i)
    except Page.DoesNotExist:
        raise Http404()

    return render_to_response('page.html', {'page': page}, context_instance=RequestContext(request))
