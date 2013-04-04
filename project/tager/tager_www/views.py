#from django.http import HttpResponse
#from django.shortcuts import render_to_response
from tager_www.models import Post, UserProfile
#from django.core.mail import send_mail
from django.http import HttpResponseRedirect
#from mysite.contact.forms import ContactForm
#from django.contrib import auth

# def login(request):
 #   if request.method != 'POST':
  #      raise Http404('Only POSTs are allowed')
   # try:
    #    m = Member.objects.get(username=request.POST['username'])
     #   if m.password == request.POST['password']:
      #      request.session['member_id'] = m.id
       #     return HttpResponseRedirect('/you-are-logged-in/')
    #except Member.DoesNotExist:
      # return HttpResponse("Your username and password didn't match.")

#def login_view(request):
  #  username = request.POST.get('username', '')
 #   password = request.POST.get('password', '')
   # user = auth.authenticate(username=username, password=password)
    #if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
     #   auth.login(request, user)
        # Redirect to a success page.
      #  return HttpResponseRedirect("/account/loggedin/"), render_to_response('login.html')
    #else:
        # Show an error page
     #   return HttpResponse("Your username and password didn't match."), HttpResponseRedirect("/account/invalid/")

#def search_postid(request):
 #   error = False
  #  if 'q' in request.GET:
   #     q = request.GET['q']
    #    if not q
     #       error = True
      #  else:
       #     posts = Post.objects.filter(id__icontains=q)
        #return render_to_response('search_results.html',
         #   {'posts': posts, 'query': q})
    #return render_to_response('search_form.html',
     #   {'error': error})
def commenting(request):
    user_id = request.user.id
    user= UserProfile.objects.get(id = user_id)
    if user.canPost:
            if  Post.objects.filter(pk=post_in.post_id).exists():
                post = request.POST["post_id"]
                content = request.POST["comments"]
                successful_Comment=Comment(user_id=self.user_id,post_id_id=post_in.post_id,content=content,date=datetime.datetime.now())
                successful_Comment.save()
                post_in.comments_count=post_in.comments_count+1
                post_in.save()

#def canComment(request):
#   if request.user.is_authenticated():
    # Do something for authenticated users.
 #   if request.method != 'POST':
  #      raise Http404('Only POSTs are allowed')

   # if 'comment' not in request.POST:
    #    raise Http404('Comment not submitted')

    #if request.session.get('has_commented', False):
     #   return HttpResponse("You've already commented.")

    #c = comments.Comment(comment=request.POST['comment'])
    #c.save()
    #render_to_response('commentresult.html')

    #request.session['has_commented'] = True
    #return HttpResponse('Thanks for your comment!')     else:
    # Do something for anonymous users.
    #return HttpResponseRedirect("/account/invalid/")

#def search_form(request):
   # return render_to_response('search_form.html')


#def Comment(request):
 #   if request.method == 'POST':
  #      form = Comment(request.POST)
   #     if form.is_valid():
    #        cd = form.cleaned_data
     #       send_notification(
      #          cd['message'],
       #     )
        #    return HttpResponseRedirect('/Commment/thanks/')
    #else:
     #   form = CommentForm()
    #return render_to_response('contact_form.html', {'form': form})

