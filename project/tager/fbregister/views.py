# Create your views here.
from fbapp.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
	return render_to_response("index.html", {}, RequestContext(request))