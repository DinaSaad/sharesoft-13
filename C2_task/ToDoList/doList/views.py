from django.http import HttpResponse

# Create your views here.
from doList.models import *


from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):
        return render_to_response('index.html', RequestContext(request))

def delete_list(request):
    if request.POST:
        toList = toList.objects.delete(list_name = request.POST['list_name'] , user = request.user)
        return render_to_response('index.html', RequestContext(request))

List creators can mark done or edit a task in one of his lists
        
def task_done(request):
    if request.post:
        toList = toList.objects.all(task_done = 'true')
    return render_to_response('index.html', RequestContext(request))   
