# Create your views here.
from django.http import HttpResponse
from doList.models import Tolist
from django.template import Context, loader

def index(request):
	doList_list = Tolist.objects.all()
	t = loader.get_template('D:/Gam3a/templates/doList/index.html')
	c = Context ({'doList_list': doList_list,})
    	return HttpResponse(t.render(c))