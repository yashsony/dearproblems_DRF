
#'''change user to request.user.id'''
from rest_framework import generics , viewsets
from rest_framework.views import APIView
from . import serilizer
from .models import Mygroup ,Request , Post , Like , Comment, Notification, Share , Profile, Follower,Aexperts
from django.http import HttpResponse
from django.contrib.auth.models import User ,Permission , Group
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Count

def empty_view(request):
    return HttpResponse('')



#class ProfileViewSet(viewsets.ModelViewSet):
#    queryset = Profile.objects.all()
#    serializer_class = serilizer.ProfileSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = serilizer.UserSerializer


class User_Class(APIView):
    def get(self ,request):
        name = self.request.GET.get('q')

        if name:
            u = User.objects.filter(Q(username__icontains=name)|
                                    Q(last_name__icontains=name)|
                                    Q(first_name__icontains=name)).annotate(followers1=Count('followers')
                        ).annotate(following1=Count('following')).order_by('-followers1','-following1')
        else:
            u = User.objects.all().annotate(followers1=Count('followers')
                        ).annotate(following1=Count('following')).order_by('-followers1','-following1')
        serializer_context = {
            'request': request,
        }
        s = serilizer.UserSerializer_my(u, many=True, context=serializer_context)
        return Response(s.data)

class User_class2(APIView):
    def get(self,request , pk):
        u = get_object_or_404(User, pk=pk)
        if u is not None:
            serializer_context = {
                'request': request,
            }
            s = serilizer.UserSerializer(u, context=serializer_context)
            return Response(s.data)
        else:
            return Response({"error": "not found"})
#make a post request to update the field






class NotificationView(APIView):
    def get(self,request):
        user = request.user.id
        u = Notification.objects.filter(notice_for_user = user)
        serializer_context = {
            'request': request,
        }
        s = serilizer.NotificationSerializer(u, many=True, context=serializer_context)
        return Response(s.data)

class Activity_of_user(APIView):
    def get(self,request):
        user = request.user.id
        u = Notification.objects.filter(action_by_user = user).filter(Message_to_creater_for_share = False)
        serializer_context = {
            'request': request,
        }
        s = serilizer.NotificationSerializer(u, many=True, context=serializer_context)
        return Response(s.data)

class GroupView(APIView):
    def post(self, request):
        if request.user.id:
            s = request.data.get('name')
            user_id = request.user.id
            serializer = serilizer.GroupSelizer(data={"name": s , "Admin_id": user_id })
            if serializer.is_valid(raise_exception=True):
                M = serializer.save()
                #user_object = get_object_or_404(User, pk = 16 )
                M.user_set.add(request.user)
                return Response({"success": "Group '{}' created successfully".format( M.name)})
        else:
            return Response({"error": "u r logout"})



    def get(self,request):
        name = self.request.GET.get('q')

        if name:
            u = Mygroup.objects.filter(Q(name__icontains=name)).annotate(total_members=Count('user__groups')).annotate(total_shares=Count('share__share_to_group')).order_by('-total_members','-total_shares')

        else:
            u = Mygroup.objects.all().annotate(total_members=Count('user__groups')).annotate(total_shares=Count('share__share_to_group')).order_by('-total_shares','-total_members')
        serializer_context = {
            'request': request ,
        }
        s = serilizer.GroupSerializer2(u , many=True,context=serializer_context)
        return Response(s.data)



class GroupView2(APIView):
    def get(self,request,pk):
        u = get_object_or_404(Mygroup, pk = pk )
        if u is not None:
            serializer_context = {
                'request': request,
            }
            s = serilizer.GroupSerializer(u,context=serializer_context)
            return Response(s.data)
        else:
            return Response({"error":"not found"})


    def post(self,request,pk):
        u = get_object_or_404(Mygroup, pk=pk)
        if u is not None:
            s = request.data.get('name')
            serializer = serilizer.GroupSerializer(u ,data={"name": s, "Admin_id": request.user.id} , partial=True)
            if serializer.is_valid(raise_exception=True):
                M = serializer.save()
                return Response({"success": "Group '{}' updated successfully".format(M.name)})
            else:
                return Response({"error": "data given by you is not acceptable"})
        else:
            return Response({"error": "not found"})


    def delete(self, request, pk):
        u = get_object_or_404(Mygroup, pk=pk)
        if u is not None:
            M = u.name
            u.delete()
            return Response({"success": "Group '{}' deleted successfully".format(M)})
        else:
            return Response({"error": "not found"})

# class RequestView2(APIView):
#     def delete(self, request, pk):
#         u = get_object_or_404(Request, pk=pk)
#         if u is not None:
#             M = u.group_name
#             u.delete()
#             return Response({"success": "request to '{}' deleted successfully".format(M)})
#         else:
#             return Response({"error": "not found"})
#
#     def update(self,request,pk):
#         pass

class RequestView(APIView):
    def post(self, request):
        s = request.data.get('group_name')
        '''here group_name is group_id u have to pass id'''
        mg_obj = get_object_or_404(Mygroup, pk= s)
        if mg_obj is not None :
            if mg_obj.Admin_id is not request.user.id :
                serializer = serilizer.RequestSerializer(data={"group_name": s, "requestor": request.user.id })
                if serializer.is_valid(raise_exception=True):
                    M = serializer.save()
                    return Response({"success": "request to '{}' created successfully".format(M.group_name)})
                else:
                    return Response({"error": "data given by you is not acceptable"})
            else:
                return Response({"error": "u r admin of group that u requested to join"})
        return Response({"error": "data given by you is not acceptable"})


    def get(self,request):
        u = Request.objects.filter(group_name__Admin_id = request.user.id)
        serializer_context = {
            'request': request,
        }
        s = serilizer.RequestSerializer(u, many=True, context=serializer_context)
        return Response(s.data)


class Add_in_Group(APIView):
    def post(self,request):
        r_id = request.data.get('request_id')
        add = request.data.get('add')
        if r_id :
            r = Request.objects.get(pk = r_id)
            if r :
                g =  Mygroup.objects.get(id = r.group_name.id)
                if g.Admin_id is request.user.id :
                    if add :
                        g.user_set.add(r.requestor)
                        r.delete()
                        return Response({"success": "successful added in group"})
                    else:
                        r.delete()
                        return Response({"success": "successful deleted requests"})

                else :
                    return Response({"error": "y have no excess to add user in group"})
            else :
                return Response({"error": "no request found"})
        else :
            return Response({"error": "request_id is compulsary "})

from rest_framework import status
from rest_framework.parsers import FileUploadParser ,JSONParser,MultiPartParser, FormParser ,ParseError
from rest_framework.permissions import AllowAny

class ProfileView(APIView):
        parser_class = [FileUploadParser]
        permission_classes = (AllowAny,)
        def post(self,request):
            if 'file' not in request.data:
                
                raise ParseError("Empty content fofoff")

            photo = request.data["file"]
            u = request.user.id 
            serializer_context = {
            'request': request,
            }
            s = Profile.objects.filter(user = request.user)
            if s :
                s.delete()
            ps = serilizer.ProfileSerializer2(data={"profile_photo": photo,"user": u },context=serializer_context)
            if ps.is_valid():
                ps.save()
                import json
                #return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)
                return Response({"success": "successful image upload"})
            else:
                return Response(ps.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
        
        def get(self,request):
        
            u = Profile.objects.all()


            serializer_context = {
                'request': request ,
            }
            s = serilizer.ProfileSerializer(u , many=True,context=serializer_context)
            return Response(s.data)

    
class ProfileView2(APIView):

    parser_class = (FileUploadParser)
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        u = get_object_or_404(Profile, pk=pk)
        if u is not None:
            serializer_context = {                                                                                                                                                                                                                                                                                                                                      
                'request': request,
            }
            s = serilizer.ProfileSerializer(u, context=serializer_context)
            return Response(s.data)
        else:
            return Response({"error": "not found"})
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
class PostView(APIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    #parser_class =[   ]
    #permission_classes = (AllowAny,)

    '''you have to work on image security and how it works'''
    def post(self,request):
        text = request.data.get('text')
        title = request.data.get('title')
        ask_with_only_experts = request.data.get('ask_with_only_experts')

        if 'file' not in request.data:
            raise ParseError("Empty content ")

        photo = request.data["file"]
        u = request.user.id

        serializer_context = {
            'request': request,
        }
        ps = serilizer.PostSerializer(data={"text":text,"title":title,"photo":photo,"ask_with_only_experts": ask_with_only_experts
                                            ,"user": u,"points":"0"},context=serializer_context)

        if ps.is_valid():
            n = ps.save()
            import json
            if n.ask_with_only_experts is not True:
                
                return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)
            else :
                print('hee')
                return Response({'message': "expert_list" ,"success": "{}".format(n.id)})

        else:
            return Response(ps.errors, status=status.HTTP_400_BAD_REQUEST)




    def get(self,request):
        #user = request.user.id
        #user1 =  User.objects.get(id = user)


#        followings_id = Follower.objects.filter(follower = user).values_list('following_id',flat=True)
#        added_groups_id = user1.groups.values_list('id', flat=True)
#
#        added_group_users_id = []
#        for i in added_groups_id:
#            jkl = User.objects.filter(groups__id=i).values_list('id', flat=True)
#            for j in jkl:
#                added_group_users_id.append(j)

        # unique = []
        # for item in added_group_users_id:
        #     if item not in unique:
        #         unique.append(item)
        # added_group_users_id = unique

        page = self.request.GET.get('page')
        u = Post.objects.all()
        paginator = Paginator(u, 12)
        print(page)
        try:
            u = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            u = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            #u = paginator.page(paginator.num_pages)
            return Response({"error":"empty"})

        # u = Post.objects.filter(
        #post i shared with any group
        # Q(post_name__share_to_user=user)|   #post related share by another user
        # Q(user__id__in = followings_id)|    # post related followings of user
        # Q(user__id__in = added_group_users_id) |#post related to added group users
        # Q(ask_with_only_experts = False)      # post that only shared with public
        # ).distinct().annotate(like_count=Count('like')
        # ,comment_count = Count('comment'),share_count = Count('post_name')).order_by(
        #     '-created_time','-edited_time', '-like_count','-comment_count','-share_count',
        # )
        serializer_context = {
            'request': request ,
        }
        s = serilizer.PostSerializer2(u , many=True,context=serializer_context)
        return Response(s.data)


class Users_post(APIView):
    def get(selfself, request):
        user = request.user
        p = Post.objects.filter(user = user).order_by('-created_time','-edited_time')
        serializer_context = {
            'request': request,
        }
        s = serilizer.PostSerializer2(p, many=True, context=serializer_context)
        return Response(s.data)



class list_of_followers_and_groupadded(APIView):
    def get(self ,request):
        user = request.user.id

        followings_id = Follower.objects.filter(following = user).values_list('follower_id', flat=True)
        a =[]
        for id in followings_id:
            u = get_object_or_404(User, pk=id)
            a.append(u)
        added_groups_id = Mygroup.objects.filter(user = user)
        serializer_context = {
            'request': request ,
        }
        s = serilizer.UserSerializer_for_group1(a , many=True , context=serializer_context)
        s1 = serilizer.all_groups_user_added(added_groups_id , many=True , context=serializer_context)
        Serializer_list = [s1.data, s.data]
        return Response(Serializer_list)
#        return Response({"followers" : '{}'.format(s.data) , "groups" : '{}'.format(s1.data)})

        
        
    
    


class PostView2(APIView):

    parser_class = (FileUploadParser,JSONParser,MultiPartParser, FormParser)
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        user = 1#request.user.id
        u = get_object_or_404(Post, pk=pk)
        if u is not None:
            if u.ask_with_only_experts is True:
                e = get_object_or_404(User, id = user)
                if e.has_perm('post.is_expert') :
                    serializer_context = {
                        'request': request,
                    }
                    s = serilizer.PostSerializer(u, context=serializer_context)
                    return Response(s.data)
                else :
                    return Response({"error": "you dont have permissions to view it"})
            else :
                serializer_context = {
                    'request': request,
                }
                s = serilizer.PostSerializer(u, context=serializer_context)
                return Response(s.data)
        else:
            return Response({"error": "not found"})


    def put(self, request, pk):
        serializer_context = {'request': request , }
        # te = request.data.get('text')
        # t = request.data.get('title')
        # ask = request.data.get('ask_with_only_experts')
        # p = request.data.get('photo'),
        # if post was for public than u cant change to expert
        try :
            saved_article = get_object_or_404(Post, pk=pk)
            if saved_article.ask_with_only_experts is True :
                serializer = serilizer.PostSerializer(instance=saved_article, data={
                "text" : request.data.get('text'),
                "title" : request.data.get('title'),
                "ask_with_only_experts" : request.data.get('ask_with_only_experts'),
                "photo" : request.data["file"]
                }, context=serializer_context, partial=True)
            else :
                serializer = serilizer.PostSerializer(instance=saved_article, data={
                "text" : request.data.get('text'),
                "title" : request.data.get('title'),
                "photo" : request.data["file"]
                }, context=serializer_context, partial=True)
        except :
            return Response({"error":"incomplete data"})
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
            return Response({"success": "Article '{}' updated successfully".format(article_saved.title)})



    def delete(self, request, pk):
        u = get_object_or_404(Post, pk=pk)
        if u is not None:
            M = u.title
            u.delete()
            return Response({"success": "POST '{}' deleted successfully".format(M)})
        else:
            return Response({"error": "not found"})

class LikeView(APIView):

    def post(self,request):
        like_on_post = request.data.get('like_on_post')
        user = request.user.id
        like_ratio = request.data.get('like_ratio')
        serializer_context = {
            'request': request,
        }
        p = Post.objects.get(id = like_on_post)
        a = Notification.objects.create(notice_for_user=p.user, action_by_user_id=user, action="L",post_name=p,group_id= 7)
        ps = serilizer.LikeSerializer(
            data={
                "like_on_post" : like_on_post,
                "user": user,
                "like_ratio" : like_ratio,
                "Notification_id" : a.id
            }, context=serializer_context)
        if ps.is_valid():
            if like_ratio is "E":
                p.points = p.points + 100
            elif like_ratio is "V":
                p.points = p.points + 75
            elif like_ratio is "G":
                p.points = p.points + 50
            else:
                p.points = p.points + 25
            save2 = p.save()
            u = ps.save()
            return Response({"success": "{}".format(p.points)})
        else:
            return Response(ps.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeView2(APIView):

    def get(self, request, pk):
        u = get_object_or_404(Like, pk=pk)
        if u is not None:
            serializer_context = {
                'request': request,
            }
            s = serilizer.LikeSerializer(u, context=serializer_context)
            return Response(s.data)
        else:
            return Response({"error": "not found"})


    def delete(self, request, pk):
        u = get_object_or_404(Like, pk=pk)
        if u is not None:
            n = get_object_or_404(Notification,pk = u.Notification_id)
            if n is not None :
                print("helllll")
                u.delete()
                n.delete()
                return Response({"success": "POST '{}' deleted successfully".format(u.like_on_post)})
            else:
                return Response({"error": "your likes Notification does not exist"})
        else:
            return Response({"error": "not fouhhhhhnd"})


class Activity_of_group(APIView):
    def get(self ,request , pk):
        s = Share.objects.filter(share_to_group = pk)
        serializer_context = {
            'request': request,
        }
        u = serilizer.Share_of_post_serilizer(s, many=True, context=serializer_context)
        return Response(u.data)

class User_info(APIView):
    def get(self,request):
        user = request.user
        serializer_context = {
            'request': request,
        }

        s = serilizer.UserSerializer_my(user, context=serializer_context)
        return Response(s.data)

class top_three_group(APIView):
    def get(self ,request):

        user = request.user.id
        g = []
        gcv = []
        followings_id = Follower.objects.filter(follower=user).values_list('following_id', flat=True)
        for id in followings_id:
            added_groups_id = Mygroup.objects.filter(user=id)
            g.append(added_groups_id)
            g = list(dict.fromkeys(g))

        for id1 in g:
            for id2 in id1:
                gcv.append(id2)




        users_group = Mygroup.objects.filter(user=user)
        for i1 in gcv:
            for i2 in users_group:
                if i1 == i2:
                    gcv.remove(i1)
        gcv2=[]
        for i in gcv:
            print(i.id + 1000)
            try:
                Request.objects.get(requestor=request.user , group_name=i.id)
            except:
                gcv2.append(i)

            # print(already_request_made)
            # if already_request_made is None:
            #     gcv2.append(i)


        serializer_context = {
        'request': request,
        }


        s = serilizer.GroupSerializer2(gcv2, many=True, context=serializer_context)
        return Response(s.data)


class shares_of_post(APIView):
    def get(self ,request , pk):
        s = Share.objects.filter(post_name = pk)
        #s = Share.objects.all()
        serializer_context = {
            'request': request,
        }
        u = serilizer.Share_of_post_serilizer(s , many=True , context=serializer_context)
        return Response(u.data)


class top_three_user(APIView):
    def get(self ,request):
        user = request.user.id
        followings_id = Follower.objects.filter(follower=user ).values_list('following_id', flat=True)

        a = []
        u_b = []
        for id in followings_id:
            followerings_followings_id = Follower.objects.filter(follower=id ).values_list('following_id', flat=True)
            a.append(followerings_followings_id)
        s = []
        for id1 in a:
            for id2 in id1:
                s.append(id2)
        s = list(dict.fromkeys(s))

        for i1 in followings_id:
            for i2 in s:
                if i2 == i1:
                    s.remove(i1)

        if user in s:# for check user in following fields
            s.remove(user)


        for iz2 in s:
            u = get_object_or_404(User, pk=iz2)
            u_b.append(u)

        page = self.request.GET.get('page')

        paginator = Paginator(u_b, 3)

        try:
            u_b = paginator.page(page)
        except PageNotAnInteger:
            u_b = paginator.page(1)
        except EmptyPage:
            return Response({"error": "empty"})


        serializer_context = {
            'request': request,
        }
        s = serilizer.UserSerializer_for_group1(u_b , many=True , context=serializer_context)

        # print(followings_id)
        # print(s)
        return Response(s.data)

class CommentView(APIView):

    def post(self,request):
        post = request.data.get('post')
        opinion_type = request.data.get('opinion_type')
        user = request.user.id
        opinion = request.data.get('opinion')
        serializer_context = {
            'request': request,
        }
        p = Post.objects.get(id = post)
        a = Notification.objects.create(notice_for_user=p.user, action_by_user_id=user, action="C",post_name=p,group_id= 7)
        ps = serilizer.CommentSerializer(
            data={
                "post" : post,
                "user": user,
                "opinion_type" : opinion_type,
                "Notification_id" : a.id,
                "opinion" : opinion
            }, context=serializer_context)
        if ps.is_valid():
            u = ps.save()
            return Response({"success": "you commented on '{}' ".format(u.post)})
        else:
            return Response(ps.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentView2(APIView):

    def get(self, request, pk):
        u = get_object_or_404(Comment, pk=pk)
        if u is not None:
            serializer_context = {
                'request': request,
            }
            s = serilizer.CommentSerializer(u, context=serializer_context)
            return Response(s.data)
        else:
            return Response({"error": "not found"})

    def delete(self, request, pk):
        u = get_object_or_404(Comment, pk=pk)
        if u is not None:
            n = get_object_or_404(Notification,pk = u.Notification_id)
            if n is not None :
                u.delete()
                n.delete()
                return Response({"success": "Comment '{}' deleted successfully".format(u.post)})
            else:
                return Response({"error": "your Comment Notification does not exist"})
        else:
            return Response({"error": "not found"})

class ShareView(APIView):
    def get(self,request):
        user = request.user.id
        u = get_object_or_404(User, pk=user)
        if u is not None:
            serializer_context = {
                'request': request,
            }
            s = serilizer.UserSerializer2(u, context=serializer_context)
            return Response(s.data)
        else:
            return Response({"error": "not found"})


    def post(self,request):
        post_name = request.data.get('post_name')
        share_to_user = request.data.get('share_to_user')
        share_by_user = request.user.id
        share_to_group = request.data.get('share_to_group')
        print(post_name)
        print(share_to_user)
        print(share_to_group)
        #idsg = get_object_or_404(Mygroup, pk=4)
        p = Post.objects.get(id=post_name)
        a = Notification.objects.create(notice_for_user_id=p.user.id, action_by_user_id=share_by_user, action="S", post_name=p,Message_to_creater_for_share=True,group_id= 7)
        s = Share.objects.create(post_name =p , share_by_user_id = share_by_user, Notification_id = a.id)
        for s_u in share_to_user:
            n11 = Notification.objects.create(notice_for_user_id=s_u, action_by_user_id=share_by_user, action="S", post_name=p , group_id= 7)
            s_u1 = User.objects.get(pk = s_u)
            if s_u1.has_perm('post.is_expert') is False:# for not allow to share to expert and only allow public post
                s.share_to_user.add(s_u1)
            else:
                n11.delete()
        for s_g in share_to_group:
            s_g_obj = Mygroup.objects.get(id = s_g)
            s.share_to_group.add(s_g_obj)
            s.save()
            added_group_users_id = []
            jkl = User.objects.filter(groups__id=s_g).values_list('id', flat=True)
            for j in jkl:
                added_group_users_id.append(j)
            for i in added_group_users_id:
                Notification.objects.create(notice_for_user_id=i, action_by_user_id=share_by_user, action="G",
                                                  post_name=p , group = s_g_obj)
        return Response({"success": "you shared "})
        # else:
        #     return Response(ps.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response({"success": "you shared "})

        
class Share_expert(APIView):
    def post(self ,request):
        user = request.user.id
        post_name = request.data.get('post_name')
        experts_id = request.data['experts_id']
        p = Post.objects.get(id=post_name)
        for s_u in experts_id:
            s_u1 = User.objects.get(pk = s_u)
            if s_u1.has_perm('post.is_expert') is True:# for only allow to share to expert
                Notification.objects.create(notice_for_user_id = s_u1.id , action_by_user_id = user , action="S", post_name=p , group_id= 7)
                return Response({"success": "you shared "})
            return Response({"success": "you not shared "})
       

        
    

    
    

class FollowView(APIView):
    def get(self,request):
        user = request.user.id
        u = Follower.objects.filter(following_id = user)
        print(u)
        if u is not None:
            serializer_context = {
                'request': request,
            }
            s = serilizer.FollowingSerializer(u, context=serializer_context , many=True)
            return Response(s.data)
        else:
            return Response({"error": "not found"})

    def post(self,request):
        follow_s = request.data.get('follow_s')
        user = request.user.id
        if user is not follow_s:
            want_to_follow_someone = User.objects.get(id = user)
            someone = User.objects.get(id = follow_s)
            want_to_follow_someone.following.add(Follower(following=someone),bulk=False)
            p = Post.objects.get(id=3)
            #i = Mygroup.objects.get(id = 4)
            #post_name should be your choice for default may be 1 that exits
            Notification.objects.create(notice_for_user_id=someone.id, action_by_user_id=want_to_follow_someone.id,post_name=p, action="F" ,group_id= 7)
            return Response({"success": "you followed '{}' ".format(someone.username)})
        else:

            return Response({"error": "user does not follow ourself"})



class SearchView(APIView) :
    def get(self,request):
        name = self.request.GET.get('q')
        p = Post.objects.filter(Q(title__icontains=name) |
                                Q(text__icontains=name) |
                                Q(user__username__icontains=name) |
                                Q(user__first_name__icontains=name) |
                                Q(user__last_name__icontains=name)).annotate(like_count=Count('like')).annotate(
        comment_count=Count('comment')).order_by('-like_count', '-comment_count').distinct()
        serializer_context = {
            'request': request,
        }
        s = serilizer.PostSerializer(p, many=True, context=serializer_context)
        return Response(s.data)



class SearchUserView(APIView) :
    def get(self,request):
        name = self.request.GET.get('q')
        u = User.objects.filter(
                                Q(username__icontains=name) |
                                Q(first_name__icontains=name) |
                                Q(last_name__icontains=name)).distinct()
        serializer_context = {
            'request': request,
        }
        s = serilizer.UserSerializer(u, many=True, context=serializer_context)
        return Response(s.data)





class ExpertView(APIView):
    def get(self,request):
        perm = Permission.objects.get(codename = 'is_expert')
        u = User.objects.filter(user_permissions=perm)
        serializer_context = {
            'request': request,
        }
        s = serilizer.UserSerializer(u, many=True, context=serializer_context)
        return Response(s.data)

    def post(self,request):
        expert_name = request.data.get('expert_name')
        post_name = request.data.get('post_name')
        user = 1  # request.user.id
        perm = Permission.objects.get(codename='is_expert')
        u = User.objects.filter(user_permissions=perm).values_list('id', flat=True)

        p = Post.objects.get(id=post_name)
        if p.ask_with_only_experts is True :


            flag = 0
            if (all(x in u for x in expert_name)):
                flag = 1
            if (flag):
                for i in expert_name:
                    serializer = serilizer.ExpertSerializer(data={"expert_name_id" : expert_name, "post_name_id" : post_name})
                    Notification.objects.create(notice_for_user_id=i, action_by_user_id=user, action="S",
                                                post_name_id=post_name , group_id= 7)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                return Response({"success": "shared with all experts"})
            else :
                return Response({"error": "user u choosed they r not experts"})
        else :
            return Response({"error": "u shared this post with all"})

