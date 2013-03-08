from django.http import HttpResponse

# Create your views here.
from doList.models import *


from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):
        return render_to_response('index.html', RequestContext(request))

def create_list(request):
    if request.POST:
        toList = toList.objects.create(list_name = request.POST['list_name'] , user = request.user)
        return render_to_response('index.html', RequestContext(request))
    else:
        return render_to_response('create_list.html', RequestContext(request))

