from django.contrib import admin
from tager_www.models import UserProfile, Channel, SubChannel, Attribute, Post, Values

admin.site.register(UserProfile)
admin.site.register(Values)
admin.site.register(Channel)
admin.site.register(SubChannel)
admin.site.register(Attribute)
admin.site.register(Post)


