from django.http import HttpResponse
#from django.shortcuts import render_to_response
from tager_www.models import Post, UserProfile, Comment
#from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
#from mysite.contact.forms import ContactForm
#from django.contrib import auth
from django.contrib.comments.views.comments import post_free_comment
import sqlite3



# def my_post_free_comment(request):
#         if 'url' in request.REQUEST and 'preview' not in request.REQUEST:
#                 response = post_free_comment(request)
                
#                 # Check there's a url to redirect to, and that post_free_comment worked
#                 if len(request.REQUEST['url'].strip()) > 0 and isinstance(response, HttpResponseRedirect):
#                         return HttpResponseRedirect(request.REQUEST['url'])
                
#                 # Fall back on the default post_free_comment response
#                 return response
        
#         return post_free_comment(request)


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

   def comments(request, offset):
    if request.method == 'POST':
        post = Post.objects.get(post_id=offset)
        date = request.POST.get('date', '')
        content = request.POST.get('content', '')
        # comment_obj = Comment(post_id=post_id, date=date, content=content)
        # comment_obj.save()
        # return HttpResponseRedirect('/posted.html')
conn = sqlite3.connect('privy.db')
print Comment #this returns <class 'privy.tager_www.models.Comment'>
cur = conn.cursor()
fields = ['post_id', 'user_id', 'date', 'content']
row = ['1', '2', '2013-07-3', 'bfjvbfj']
Person.objects.create(**dict(zip(fields, row)))
try:
    post = Person_Type.objects.get(post='1')
except Post.DoesNotExists:
    post_id = Post.objects.create(post_id='1')
Comment.objects.create(date=2013-07-3,user_id=2, content='bfjvbfj', post_id=post_id)

def commenting(request):
  list_of_comment =Comment.objects.all()
  return (render(request,'posted.html'),{'list_of_comment':list_of_comment})
  #retreiving the comment from comment table. 


    # user_id = request.UserProfile.id
    # user= UserProfile.objects.get(id = 1)
    # if user.canPost:
    #         post_id = request.POST["post_id"]  
    #         if  Post.objects.filter(pk=post_id).exists():
    #             post = Post.objects.get(id=post_id)
    #             content = request.POST["comments"]
    #             successful_Comment=Comment(user_id=self.user_id,post_id_id=post_id,content=content,date=datetime.datetime.now())
    #             successful_Comment.save()
    #             post.comments_count=post.comments_count+1
    # user = UserProfile.objects.get(pk=2)
    # content1 = "test"
    # post = Post.objects.get(pk=1)
    # date1 = "2013-02-02"
    # c = Comment(user_id=user, content= content1, post_id=post, date = date1)
    # c.save()
    # return HttpResponse("thank you")

# def canComment(request):
#   if request.UserProfile.is_authenticated():
#   Do something for authenticated users.
#    if request.method != 'POST':
#        raise Http404('Only POSTs are allowed')

#    if 'comment' not in request.POST:
#        raise Http404('Comment not submitted')

#     if request.session.get('has_commented', False):
#        return HttpResponse("You've already commented.")

#     c = comments.Comment(comment=request.POST['comment'])
#     c.save()
#     render_to_response('commentresult.html')

#     request.session['has_commented'] = True
#     return HttpResponse('Thanks for your comment!')    
#     Do something for anonymous users.
#     return HttpResponseRedirect("/account/invalid/")

# def search_form(request):
#    return render_to_response('search_form.html')


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

