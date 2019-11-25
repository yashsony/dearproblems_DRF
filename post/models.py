from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

#def create_slug(instance , new_slug=None):
#    slug = slugfy(instance.title)
#    if new_slug is not None:
#        slug = new_slug
#    qs = Post.objects.filter(slug = slug).order_by("-id")
#    exists = qs.exists()
#    if exists :
#        new_slug = "%s-%s" %(slug,qs.first().id)
#        return create_slug(instance, new_slug=new_slug)
#    return slug

def user_directory_path(instance, filename):
    return 'post_by_user_{0}/{1}'.format(instance.user.id, filename)

class Post(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,related_name='user_name',default=1)
    title   =  models.CharField(max_length=200, null=False ,blank=False)
    text    =  models.TextField(max_length=500,  null=False ,blank=False)
    created_time = models.DateTimeField(auto_now=False,auto_now_add=True)
    edited_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    photo = models.FileField(upload_to= user_directory_path,null=True,blank=True)
    points = models.IntegerField(default=0)
    ask_with_only_experts = models.BooleanField(null=False,default=False)

    def __str__(self):
        return self.title

    class Meta:
        permissions = (
            ('is_expert', 'expert'),
        )

def profile_directory_path(instance, filename):
    return 'userpic_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_name_for_profile', default=1)
    profile_photo = models.ImageField(upload_to=profile_directory_path, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
# post_profile.user_id

def profile_directory_path55(instance, filename):
    return 'grouppic_{0}/{1}'.format(instance.id, filename)





from django.contrib.auth import get_user_model
user = get_user_model()

class Follower(models.Model):
    follower = models.ForeignKey(user , related_name='following',on_delete=models.CASCADE)
    following = models.ForeignKey(user,related_name='followers',on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)


    class Meta:
        unique_together = ('follower', 'following')

    def __unicode__(self):
        return u'%s follows %s' % (self.follower, self.following)


class Aexperts(models.Model):
    expert_name = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE,default=1)
    post_name = models.ForeignKey(Post,null=False,on_delete=models.CASCADE,default=1,related_name='experts_n')



class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    like_on_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    lk = [
        ('N', 'Nice'),
        ('G', 'Good'),
        ('V', 'Very Good'),
        ('E', 'Excellent'),
    ]
    like_ratio = models.CharField(max_length=1,choices=lk ,null=False,blank=False)
    Notification_id = models.IntegerField(blank=False,null=False,default=1)
    class Meta:
        unique_together = ('user', 'like_on_post')




class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    ct=[
        ('S', 'Suggestion'),
        ('C','Comment'),
    ]
    opinion_type = models.CharField(max_length=1,choices=ct,null=False,blank=False)
    opinion = models.CharField(max_length=300,null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    Notification_id = models.IntegerField(blank=False,null=False,default=1)

class Mygroup(Group):
    Admin_id = models.IntegerField(null=True,blank=True)

class Notification(models.Model):
	notice_for_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE,default=1,related_name='notice_for_user')
	post_name = models.ForeignKey(Post,null=True,on_delete=models.CASCADE)
	action_by_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.DO_NOTHING)
	ch = [
		('L', 'liked'),
		('C', 'comment'),
		('S', 'share'),
		('F','follow'),
		('G' , 'share_to_group')
	]
	action = models.CharField(max_length=1,choices=ch,null=False,blank=False)
	created_date = models.DateTimeField(default=timezone.now)
	Message_to_creater_for_share = models.BooleanField(null=False,blank=False,default=False)
	group = models.ForeignKey(Mygroup, on_delete=models.CASCADE , default=1)





class Request(models.Model):
    requestor = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE,default=1,related_name='requestor_set')
    group_name = models.ForeignKey(Mygroup,null=False,on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    class Meta:
        unique_together = ('requestor', 'group_name')

    def __str__(self):
        return '%s request to %s' % (self.requestor, self.group_name)


class Share(models.Model):
    post_name = models.ForeignKey(Post, null=False, on_delete=models.CASCADE,related_name='post_name')
    share_by_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,on_delete=models.CASCADE,default=1, related_name='share_by_user')
    share_to_group = models.ManyToManyField(Mygroup,blank=True)
    share_to_user = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='share_to_user')
    created_date = models.DateTimeField(default=timezone.now)
    Notification_id = models.IntegerField(blank=False, null=False, default=1)



class Group_profile(models.Model):
    group = models.OneToOneField(Mygroup, on_delete=models.CASCADE, related_name='group_for_profile', default=1)
    profile_photo = models.ImageField(upload_to=profile_directory_path55, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)