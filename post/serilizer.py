from rest_framework import serializers
from .models import Mygroup ,Request , Post , Like , Comment ,Notification ,Share , Profile , Follower,Aexperts , Group_profile
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class FollowerSerializer(serializers.ModelSerializer):
    class Meta :
        model = Follower
        exclude = ['id','following' ]

class FollowingSerializer(serializers.ModelSerializer):
    class Meta :
        model = Follower
        exclude = [ 'follower' ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id',"created_date","user"]
        
class ProfileSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class Group_profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Group_profile
        fields = '__all__'


class Share_of_post_serilizer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'


class all_groups_user_added(serializers.ModelSerializer):
    def get_total_members(self,obj):
        count_members = User.objects.filter(groups__name = obj.name).count()
        return "%i"% count_members
    
    total_members = serializers.SerializerMethodField()

    class Meta:
        model = Mygroup
        queryset = Mygroup.objects.all()
        
        exclude = ['permissions','Admin_id']
   
        
        
class GroupSerializer2(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name="post:group-detail", lookup_field='pk')

    def get_total_members(self,obj):
        count_members = User.objects.filter(groups__name = obj.name).count()
        return "%i"% count_members

    group_for_profile = Group_profile_Serializer(read_only=True)
    total_members = serializers.SerializerMethodField()
    class Meta:
        model = Mygroup
        queryset = Mygroup.objects.all()
        exclude = ['permissions','Admin_id']

class UserSerializer(serializers.ModelSerializer):
    url_for_detail_view = serializers.HyperlinkedIdentityField(read_only=True, view_name="post:user-detail",lookup_field = 'pk')
    groups = GroupSerializer2(many=True,read_only=True)
    user_name_for_profile = ProfileSerializer(read_only=True)
    followers = FollowerSerializer(read_only=True, many=True)
    following = FollowingSerializer(read_only=True, many=True)

    def get_total_following(self,obj):
        u= User.objects.get(id = obj.id)
        count_members = u.following.all().count()
        return "%i"% count_members


    def get_total_followers(self,obj):
        u= User.objects.get(id = obj.id)
        count_members = u.followers.all().count()
        return "%i"% count_members


    total_following = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password','is_superuser','is_staff','user_permissions',]

class UserSerializer_my(serializers.ModelSerializer):
    url_for_detail_view = serializers.HyperlinkedIdentityField(read_only=True, view_name="post:user-detail",lookup_field = 'pk')
    #groups = GroupSerializer2(many=True,read_only=True)
    user_name_for_profile = ProfileSerializer(read_only=True)
    #followers = FollowerSerializer(read_only=True, many=True)
    #following = FollowingSerializer(read_only=True, many=True)

    def get_total_following(self,obj):
        u= User.objects.get(id = obj.id)
        count_members = u.following.all().count()
        return "%i"% count_members


    def get_total_followers(self,obj):
        u= User.objects.get(id = obj.id)
        count_members = u.followers.all().count()
        return "%i"% count_members

    def get_total_posts(self , obj):
        total_posts = Post.objects.filter(user = obj).count()
        return "%i"% total_posts

    total_following = serializers.SerializerMethodField()
    total_posts = serializers.SerializerMethodField()
    total_followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password',"last_login",'is_superuser','is_staff','user_permissions',"email","is_active","date_joined","groups"]




class UserSerializer2(serializers.ModelSerializer):
    # for use of share get
    class Meta:
        model = User
        fields = [ 'groups']
        depth = 1

class UserSerializer_for_group(serializers.ModelSerializer):
    url_for_detail_view = serializers.HyperlinkedIdentityField(read_only=True, view_name="post:user-detail",lookup_field = 'pk')
    user_name_for_profile = ProfileSerializer(read_only=True)


    class Meta:
        model = User
        exclude = ['password','is_superuser','is_staff','user_permissions','groups', 'is_active','email','date_joined','last_login']

class UserSerializer_for_group1(serializers.ModelSerializer):
    url_for_detail_view = serializers.HyperlinkedIdentityField(read_only=True, view_name="post:user-detail",lookup_field = 'pk')
    user_name_for_profile = ProfileSerializer(read_only=True)


    class Meta:
        model = User
        exclude = ['password','is_superuser','is_staff','user_permissions','groups', 'is_active','email','date_joined','last_login' , 'first_name','last_name']

class GroupSerializer(serializers.ModelSerializer):
    url =  serializers.HyperlinkedIdentityField(read_only=True, view_name="post:group-detail",lookup_field = 'pk')

    def get_admin_name(self, obj):
        if obj.Admin_id is None:
            return None
        u = User.objects.get(id=obj.Admin_id)
        return "%s" % u.username

    def get_total_members(self, obj):
        count_members = User.objects.filter(groups__name=obj.name).count()
        return "%i" % count_members

    total_members = serializers.SerializerMethodField()

    admin_name = serializers.SerializerMethodField()
    user_set = UserSerializer_for_group(many =True )
    class Meta:
        model = Mygroup
        queryset = Mygroup.objects.all()
        exclude = ['permissions']



class GroupSelizer(serializers.ModelSerializer):
    #user_set = serializers.HyperlinkedIdentityField(many=True,read_only=True, view_name="post:user-detail",lookup_field = 'pk',)
    url =  serializers.HyperlinkedIdentityField(read_only=True, view_name="post:group-detail",lookup_field = 'pk')

    def get_admin_name(self, obj):
        if obj.Admin_id is None:
            return None
        u = User.objects.get(id=obj.Admin_id)
        return "%s" % u.username

    admin_name = serializers.SerializerMethodField()
    #user_set = UserSerializer(many =True )
    class Meta:
        model = Mygroup
        queryset = Mygroup.objects.all()
        exclude = ['permissions']



class RequestHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.requestor.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.requestor.pk,
            },
            request=request,
            format=format,
        )
class RequestHyperlinkedIdentityField1(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.user.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.user.pk,
            },
            request=request,
            format=format,
        )
class RequestHyperlinkedIdentityField2(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.like_on_post.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.like_on_post.pk,
            },
            request=request,
            format=format,
        )
class RequestHyperlinkedIdentityField3(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.post.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.post.pk,
            },
            request=request,
            format=format,
        )
class GroupHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.group_name.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.group_name.pk,
            },
            request=request,
            format=format,
        )

class RequestSerializer(serializers.ModelSerializer):
    requestor_url = RequestHyperlinkedIdentityField(read_only=True, view_name="post:user-detail" )
    group_name_url = GroupHyperlinkedIdentityField(read_only=True, view_name="post:group-detail")
    class Meta:
        model = Request
        fields = '__all__'


class RequestHyperlinkedIdentityField5(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.post_name.id is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.post_name.id,
            },
            request=request,
            format=format,
        )

class RequestHyperlinkedIdentityField4(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.notice_for_user.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.notice_for_user.pk,
            },
            request=request,
            format=format,
        )

class RequestHyperlinkedIdentityField6(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.action_by_user.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.action_by_user.pk,
            },
            request=request,
            format=format,
        )

class NotificationSerializer(serializers.ModelSerializer):
    notice_for_user_url =   RequestHyperlinkedIdentityField4(read_only=True, view_name="post:user-detail")
    post_name_url  =   RequestHyperlinkedIdentityField5(read_only=True, view_name="post:post-detail")
    action_by_user_url = RequestHyperlinkedIdentityField6(read_only=True, view_name="post:user-detail")
    created_date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'

class RequestHyperlinkedIdentityField7(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.share_by_user.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.share_by_user.pk,
            },
            request=request,
            format=format,
        )

class RequestHyperlinkedIdentityField8(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.share_to_user.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.share_to_user.pk,
            },
            request=request,
            format=format,
        )

class RequestHyperlinkedIdentityField9(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.share_to_group.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'pk': obj.share_to_group.pk,
            },
            request=request,
            format=format,
        )




class LikeSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    user_url = RequestHyperlinkedIdentityField1(read_only=True, view_name="post:user-detail")
    post_url = RequestHyperlinkedIdentityField2(read_only=True, view_name="post:post-detail")

    class Meta:
        model = Like
        fields = '__all__'

    def get_created_by(self,obj):
        return str(obj.user.username)

class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.SerializerMethodField()
    user_url = RequestHyperlinkedIdentityField1(read_only=True, view_name="post:user-detail")
    post_url = RequestHyperlinkedIdentityField3(read_only=True, view_name="post:post-detail")

    class Meta:
        model = Comment
        fields = '__all__'
    def get_commented_by(self,obj):
        return str(obj.user.username)


class LikeSerializer2(serializers.ModelSerializer):
    user_url = RequestHyperlinkedIdentityField1(read_only=True, view_name="post:user-detail")
    class Meta:
        model = Like
        exclude = ['user','like_on_post']



class CommentSerializer2(serializers.ModelSerializer):
    user_url = RequestHyperlinkedIdentityField1(read_only=True, view_name="post:user-detail")
    class Meta:
        model = Comment
        exclude = ['post']

class ShareSerializer(serializers.ModelSerializer):
    post_name_url  =   RequestHyperlinkedIdentityField5(read_only=True, view_name="post:post-detail")
    share_by_user_url = RequestHyperlinkedIdentityField7(read_only=True, view_name="post:user-detail")
    created_date = serializers.DateTimeField(read_only=True)
    share_to_user = UserSerializer(many=True)
    share_to_group = GroupSerializer(many=True)
    class Meta:
        model = Share
        fields = '__all__'


class RequestHyperlinkedIdentityield(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.expert_name.id is None:
            return None

        return self.reverse(view_name,
                            kwargs={
                                'pk': obj.expert_name.id,
                            },
                            request=request,
                            )

class ExpertSerializer(serializers.ModelSerializer):
    experts_url = RequestHyperlinkedIdentityield(read_only=True, view_name="post:user-detail")
    class Meta:
        model = Aexperts
        queryset = Aexperts.objects.all()
        fields = ['expert_name','experts_url']



class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    created_by_url = RequestHyperlinkedIdentityField1(read_only=True, view_name="post:user-detail" )
    post_url = serializers.HyperlinkedIdentityField(read_only=True, view_name="post:post-detail", lookup_field ='pk')
    like_set = LikeSerializer2(many=True,read_only=True)
    comment_set = CommentSerializer2(many=True,read_only=True)
    post_name  = ShareSerializer(many=True , read_only=True)
    experts_n = ExpertSerializer(read_only=True, many=True)


    class Meta:
        model = Post
        #fields = ['like_on_post','created_by_url','post_url','created_by']
        fields = '__all__'
        depth = 0
        pagination_class = CustomPagination

    def get_created_by(self,obj):
        return str(obj.user.username)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.ask_with_public = validated_data.get('ask_with_public', instance.ask_with_public)
        instance.photo = validated_data.get('photo', instance.photo)

        instance.save()
        return instance

class UserSerializer_my2(serializers.ModelSerializer):
    #url_for_detail_view = serializers.HyperlinkedIdentityField(read_only=True, view_name="post:user-detail",lookup_field = 'pk')
    #groups = GroupSerializer2(many=True,read_only=True)
    user_name_for_profile = ProfileSerializer(read_only=True)
    #followers = FollowerSerializer(read_only=True, many=True)
    #following = FollowingSerializer(read_only=True, many=True)

    # def get_total_following(self,obj):
    #     u= User.objects.get(id = obj.id)
    #     count_members = u.following.all().count()
    #     return "%i"% count_members
    #
    #
    # def get_total_followers(self,obj):
    #     u= User.objects.get(id = obj.id)
    #     count_members = u.followers.all().count()
    #     return "%i"% count_members


    # total_following = serializers.SerializerMethodField()
    # total_followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password',"last_login",'first_name','last_name','is_superuser','is_staff','user_permissions',"email","is_active","date_joined","groups"]



class PostSerializer2(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    created_by_url = RequestHyperlinkedIdentityField1(read_only=True, view_name="post:user-detail" )
    post_url = serializers.HyperlinkedIdentityField(read_only=True, view_name="post:post-detail", lookup_field ='pk')
    user = UserSerializer_my2(read_only=True)
    #like_set = LikeSerializer2(many=True,read_only=True)
    #comment_set = CommentSerializer2(many=True,read_only=True)
    #post_name  = ShareSerializer(many=True , read_only=True)
    #experts_n = ExpertSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        #fields = ['like_on_post','created_by_url','post_url','created_by']
        #fields = '__all__'
        exclude = ['edited_time' ,  'ask_with_only_experts']
        depth = 2
        pagination_class = CustomPagination

    def get_created_by(self,obj):
        return str(obj.user.username)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.ask_with_public = validated_data.get('ask_with_public', instance.ask_with_public)
        instance.photo = validated_data.get('photo', instance.photo)

        instance.save()
        return instance






