from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import Post,Like,Comment,Aexperts,Notification,Request,Share,Mygroup,Profile,Follower ,Group_profile

admin.site.register(Post)
admin.site.register(Session)
admin.site.register(Follower)
admin.site.register(Share)
admin.site.register(Mygroup)
admin.site.register(Like)

admin.site.register(Group_profile)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Aexperts)
admin.site.register(Profile)
admin.site.register(Request)