from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from core.viewSet.contribution_viewset import ContributionViewSet
from core.viewSet.feed_post_viewset import FeedPostViewSet
from core.viewSet.follow_request_viewset import FollowRequestViewSet
from core.viewSet.group_admin_viewset import GroupAdminViewSet
from core.viewSet.group_chat_message_viewset import GroupChatViewSet
from core.viewSet.group_viewset import GroupViewSet
from core.viewSet.interest_viewset import InterestViewSet
from core.viewSet.notification_viewset import NotificationViewSet
from core.viewSet.private_chat_message_viewset import PrivateChatViewSet
from core.viewSet.profile_viewset import UserProfileViewSet
from core.viewSet.programming_group_viewset import ProgrammingGroupViewSet
from core.viewSet.task_comment_viewset import TaskCommentViewSet
from core.viewSet.task_viewset import TaskViewSet
from core.viewSet.technology_viewset import TechnologyViewSet
from core.viewSet.token_viewset import CustomTokenPairView
from core.viewSet.university_viewset import UniversityViewSet
from core.viewSet.user_following_viewset import UserFollowingViewSet
from core.viewSet.user_viewset import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'universitys',UniversityViewSet, basename='university')
router.register(r'programmingGroups', ProgrammingGroupViewSet, basename='programmingGroup')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'groupAdmins', GroupAdminViewSet, basename='groupAdmin')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'privateChats', PrivateChatViewSet, basename='privateChat')
router.register(r'groupChats', GroupChatViewSet, basename='groupChat')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'taskComments', TaskCommentViewSet, basename='taskComment')
router.register(r'technologies', TechnologyViewSet, basename='technology')
router.register(r'interests', InterestViewSet, basename='interest')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'contributions', ContributionViewSet, basename='contribution')
router.register(r'follow-requests', FollowRequestViewSet, basename='follow-request')  
router.register(r'followings', UserFollowingViewSet, basename='user-following')
router.register(r'posts', FeedPostViewSet, basename='feedPost')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/token/', CustomTokenPairView.as_view(), name='token_obtain_pair'),
    
    path('follow_requests/user_requests', FollowRequestViewSet.as_view({'get': 'list'}), name='user_requests'),
    path('follow_requests/send_request/<uuid:user_id>/', FollowRequestViewSet.as_view({'post': 'create'})),
    path('follow_requests/reject-accept/<uuid:pk>/handle/<str:action>/', FollowRequestViewSet.as_view({'put': 'handle_request'})),
    
    path('followings/following/', UserFollowingViewSet.as_view({'get': 'list_following'}), name='list-following'),
    path('followings/followers/', UserFollowingViewSet.as_view({'get': 'list_followers'}), name='list-followers'),
    path('followings/remove-follower/<uuid:follower_id>/', UserFollowingViewSet.as_view({'delete': 'remove_follower'}), name='remove-follower'),
    path('followings/unfollow/<uuid:followed_id>/', UserFollowingViewSet.as_view({'delete': 'unfollow_user'}), name='unfollow-user'),
    path('followings/non_friends/', UserFollowingViewSet.as_view({'get': 'list_non_friends'}), name='list-non-friends'),

     path('feedposts/', FeedPostViewSet.as_view({'get': 'list'}), name='list-posts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
