from django.urls import include, path
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as view2

router = routers.DefaultRouter()
#router.register(r'group', views.GroupViewSet,base_name='group')

#router.register(r'request_to_join', views.RequestViewSet)
#router.register(r'post', views.PostViewSet,base_name='post')
#router.register(r'like', views.LikeViewSet)
#router.register(r'profile', views.ProfileViewSet)
#router.register(r'share', views.ShareViewSet)
#router.register(r'comment', views.CommentViewSet)
#router.register(r'notification', views.NotificationViewSet)

app_name = 'post'



urlpatterns = [
    path('api-token-auth/', view2.obtain_auth_token) ,
    path('top_suggested_u/', views.top_three_user.as_view()),
    path('top_suggested_g/', views.top_three_group.as_view()),
    path('shares_of_post/<int:pk>/', views.shares_of_post.as_view()),
    path('user_info/', views.User_info.as_view()),
    path('user_post/', views.Users_post.as_view()),
    # path('top_three_comments', )
    path('activity_of_group/<int:pk>/', views.Activity_of_group.as_view()),
    path('', include(router.urls)),
    path('profile/',views.ProfileView.as_view()),
    path('profile/<int:pk>/',views.ProfileView2.as_view()),
    path('user/',views.User_Class.as_view()),
    path('user/<int:pk>/',views.User_class2.as_view(),name = 'user-detail'),
    path('group/',views.GroupView.as_view()),
    path('group/<int:pk>/',views.GroupView2.as_view(),name = 'group-detail'),
    path('request/',views.RequestView.as_view()),
   # path('request/<int:pk>/', views.RequestView2.as_view()),
    path('add_in_group/',views.Add_in_Group.as_view()),# no serilizer
    path('post/',views.PostView.as_view()),
    path('post/<int:pk>/',views.PostView2.as_view(),name='post-detail'),
    path('like/',views.LikeView.as_view()),
    path('like/<int:pk>/', views.LikeView2.as_view()),
    path('comment/', views.CommentView.as_view()),
    path('comment/<int:pk>/', views.CommentView2.as_view()),
    path('notification/',views.NotificationView.as_view()),
    path('activity_by_user/', views.Activity_of_user.as_view()),
    path('share/', views.ShareView.as_view()),
    path('follow/',views.FollowView.as_view()),
    #path('unfollow')
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('password-reset/<uidb64>/<token>/', views.empty_view, name='password_reset_confirm'),
    path('search/',views.SearchView.as_view()),
    path('list/',views.list_of_followers_and_groupadded.as_view()),
    #see here below
    #path('search/user/',views.SearchUserView.as_view()),
    path('expert/',views.ExpertView.as_view()),
    path('Share_expert/',views.Share_expert.as_view()),
    #yash u have to do some changes for angualr in context for reset pasword u have to pass token with uid with request
]

# router.register(r'user', views.UserViewSet,base_name='user')