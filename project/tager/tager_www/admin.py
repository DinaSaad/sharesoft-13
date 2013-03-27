from django.contrib import admin
from tager_www.models import UserProfile,Post,InterestedIn

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(InterestedIn)