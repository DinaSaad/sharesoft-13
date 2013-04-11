from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import RegistrationForm
from tager_www.models import UserProfile 


def home(request):
    return render_to_response ('home.html',context_instance=RequestContext(request))

#C2-mahmoud ahmed-the login method is a method that allows user to log in it takes in a request
#which is of type post and it has the email and the password attribute which are 
#taken in as variables then they are authinticated and the authinticated user is 
#saved into variable user then there is an condition which check that the user is 
#actually there and if he is an active user then we log him in and render his profile page
#in case he has a disabled account then a message would appear. and if the user doesn't exist
#or information entered is wrong then he is redirected to the login page again.

def view_channels(request):
    list_of_channels = Channel.objects.all()    
    return render(request, 'index.html', {'list_of_channels': list_of_channels})

def view_subchannels(request):
    s_id = request.GET['ch_id']
    current_channel = Channel.objects.filter(pk=s_id)
    list_of_subchannels = Subchannel.objects.filter(channel_id = current_channel)
    return render(request, 'index.html', {'list_of_subchannels': list_of_subchannels})

def login(request):
    #print request
    #print "ldnfldnfndlfd"
    #print request.method
    mail = request.POST['email']
    password = request.POST['password']
   # print "before"
    # user = UserProfile.objects.get(email=mail)
    # print user.username
    # pk = user.username
    authenticated_user = authenticate(mail=mail, password=password)
    if authenticated_user is not None:
        print "auth"
        print authenticated_user.is_active
        if authenticated_user.is_active:
            print "act"
            django_login(request, authenticated_user)
            return render_to_response ('profile.html',context_instance=RequestContext(request))# Redirect to a success page.
        else:
           return HttpResponse ("sorry your account is disabled") # Return a 'disabled account' error message
    else:
        return render_to_response ('home.html',context_instance=RequestContext(request))
       #return redirect("/login/")# Return an 'invalid login' error message.

#C2-mahmoud ahmed-this isn't all of view post but this part that i did is concerend with the apperance of the
#the rate the seller button which would appear to the buyer of the post only so what it does is
#it takes object user from the session and checks if this user can rate the post that is imbeded in 
#the request and then add the results in the dictonary.Then render the post html and pass the 
#dictionary.
#
def view_post(request):

    post = Post.objects.get(pk= request.POST['post_id'])
    user = request.user
    creator = False
    if post.user_id == user:
         creator = True
    rateSellerButtonFlag = user.canRate(request.POST['post_id']) 
    d = {'view_rating':rateSellerButtonFlag, 'add_buyer_button': creator}
    
    if request.method == 'POST':
        form = BuyerIdentificationForm( request.POST )
        if form.is_valid():
            new_buyer_num = form.GetBuyerNum()
            buyer_added = user.add_Buyer(post, new_buyer_num)
            return HttpResponseRedirect( "/" )
        else :
            d.update({'form':form})
            return render_to_response( "add_buyer.html", d, context_instance = RequestContext( request ))

    else:
        form = BuyerIdentificationForm()
        d.update({'form':form})
    return render_to_response( "Post.html", d,context_instance = RequestContext( request ))



class CustomAuthentication:
    def authenticate(self, mail, password):
        try:
            user = UserProfile.objects.get(email=mail)
            if user.password == password:
                return user
        except UserProfile.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return UserProfile.object.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None




def  get_user(self):    
    User = get_user_model()
    return User



def UserRegistration(request):
     #if the user is already logged in , registered , go to profile 
    #if request.user.is_authenticated():
     #   return HttpResponseRedirect('/profile/')
     #if they r submitting the form back
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # takes the registeration form and fills it with what is entered
        if form.is_valid(): # validates all the fields on the firm,The first time you call is_valid() or access the errors attribute of a ModelForm triggers form validation as well as model validation.
                user = UserProfile.objects.create_user(name=form.cleaned_data['name'], email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
                user.save() # this creates the user 
                
                return HttpResponseRedirect('/profile/')
        else:
                return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        ''' user is not submitting the form, show them a blank registration form '''
        form = RegistrationForm()
        #add our registration form to context
        context = {'form': form}
        return render_to_response('register.html', context, context_instance=RequestContext(request))

#C1-Tharwat) This method directs the user to the report page to select a reason for reporting a post
def goToTheReportPage(request):
    return render_to_response('report.html')

#C1-Tharwat) This method takes the user input(reason) for reporting a post and calls the reportPost method in models.py
#reportPost in models.py then takes action to finish the reporting proccess
def reportThePost(request):
    return HttpResponse("hello")
# def get_subchannel(request):
#     subchannel = subchannel.objects.filter(channel_id= request.channel_id)
#     # subchannel_list = []
#     # subchannel_id_list = []
#     # for i in subchannel:
#     #     subchannel_list.append(i.name)
#     # for i in subchannel:
#     #     subchannel_list.append(i.id)
#     return subchannel
# def get_subchannel_name(subchannel,request):
#     subchannel = subchannel.objects.filter(channel_id= request.channel_id)
#         # subchannel_list = []
#     subchannel_id_list = []
#     for i in subchannel:
#          subchannel_list.append(i.name)
#     return subchannel_list
# def get_subchannel_id(subchannel ,request):
#     subchannel_id_list = []
#     for i in subchannel:
#         subchannel_list.append(i.id)

def get_attributes_of_subchannel(request):
    sub_id = request.GET['sub_ch_id']

    list_of_attributes = Attribute.objects.filter(subchannel_id = sub_id)
    return render(request, 'advanced_search.html', {'list_of_attributes' : list_of_attributes, 'sub_id' : sub_id})
# def get_attributes_names_of_subchannel(attributes,request):
#     attributes_name_list = []
#     for i in attributes:
#         attributes_name_list.append(i.name)
#     return render(request, 'advanced_search.html', {'attributes_name_list' : attributes_name_list})
def get_attributes_id_of_subchannel(attribute_list , request):
    # attributes = Attribute.objects.filter(subchannel_id = request.subchannel_id)
    attributes_search_list = []
    for j in attributes:
        attributes_search_list.append(i.attribute_id)
    return attributes_search_list
def advanced_search(request):
    sub_id = request.GET['sub_ch_id']
    attributes = Attribute.objects.filter(subchannel_id = sub_id)
    values =[]
    print "attributes"
    # print request
    post = []
    for w in attributes:
        name = w.name
        print request.GET[name]
        values.append(request.GET[name])
    # value_obj = []
    # counter = 0
    # count = 0
    # major = 0
    # i = 0

    # for att in attributes:
    #     values_obj[count] = Value.objects.filter(attribute_id = att.id , value = values[count] )
    #     print "filtering done"
    #     count+=1
    # for a in values_obj:         
    #     for b in values_obj:
    #         for i in values_obj[counter]:
    #             if values_obj.Post_id[0][major] == values_obj[counter+1][i].Post_id:
    #                 print"in if condition"
    #                 post.append(values_obj.Post_id[0][counter])
    #                 print"done adding"
    #     major =major + 1
    #         counter = counter+1
    #             i =i+1





    i=0
    posts=[]
    for attribute in attributes:
        
        all_posts = Post.objects.all()
        
        for post in all_posts:
            
            value_obj = Value.objects.get(attribute_id=attribute.id, Post_id=post.id)
            
            value_name=value_obj.value
            if values[i]==value_name:
                # print unicode(post.id)
                posts.append(post)
    # print unicode(posts[0].id)
    return HttpResponse('filter_post_channel.html', {'posts' : posts})
   
    



    # result_search_obj = []
    # flag = False
    # result_search = []
    # result = []
    # post = []
    # i = 0
    # f = i+1
    # # post_temp = ""

    # asd = len(Value.objects.filter(attribute_id = attributes[j].id 
    #         , value = valuesobj[j].value))
    #     for q in asd:
    #         result_search_obj.append([])
    # for j in range(len(attributes)):
        
    #     result_search_obj[j].append(Value.objects.filter(attribute_id = attributes[j].id 
    #         , value = valuesobj[j].value))    
    # for k in result_search_obj:
    #     for l in result_search_obj[k]:
    #         result_search[k].append(k.post_id)
    # for a in result-search:
    #     result_search.sort(len(result_search[k]))
    # for h in result_search:
    #     post_temp = ""
    #     for g in result_search[h]:
    #         tmp=result_search[h]
    #         loc = temp[g]
    #         if loc == result_search[h+1][g]:
    #             flag = True
    #             post_temp = tmp[g]
    #             break
    #     post = post_temp
    return post


                
def view_subchannels(request):
    s_id = request.GET['ch_id']
    #current_channel = Channel.objects.filter(channel_id = s_id)
    list_of_subchannels = Subchannel.objects.filter(channel_id = s_id)
    return render(request, 'advanced_search.html', {'list_of_subchannels': list_of_subchannels})
def view_channels(request):
    list_of_channels = Channel.objects.all() 
    print list_of_channels   
    return render(request, 'advanced_search.html', {'list_of_channels': list_of_channels})











    
