from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('user/', api.user, name='user'),
    path('user/sendFriendRequest/', api.sendFriendRequest, name='sendFriendRequest'),
    path('user/unFriend/', api.unFriend, name='unFriend'),
    path('user/suggestedPeople/', api.suggestedPeople, name='suggestedPeople'),
    path('user/friends/me/', api.getCurrentUserFriendsData, name='getCurrentUserFriendsData'),
    path('user/friends/viewed/<uuid:user_id>/', api.getViewedUserFriendsData, name='getViewedUserFriendsData'),
    path('user/friends/accept', api.acceptFriendRequest, name='acceptFriendRequest'),
    path('user/friends/reject', api.rejectFriendRequest, name='rejectFriendRequest'),
    path('signup/', api.signup, name='signup'),
    path('editProfile/', api.editProfile, name='editProfile'),
    path('login/', TokenObtainPairView.as_view(), name='token_login_view'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh_view')
]

