from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template , Context
from django.template import RequestContext
from Guest.forms import RegistrationForm


def user_guestRegistration(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/profile/')
        if request.method == 'POST':
                pass
        else:
                ''' user is not submitting the form, show them a blank registration form '''
                form = RegistrationForm()
                context = {'form': form}
                return render_to_response('register.html', context, context_instance=RequestContext(request))
		