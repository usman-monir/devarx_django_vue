from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('user/', api.user, name='user'),
    path('user/SendfriendRequest/', api.sendFriendRequest, name='sendFriendRequest'),
    path('user/friends/', api.friends, name='friends'),
    path('user/friends/accept', api.acceptFriendRequest, name='acceptFriendRequest'),
    path('user/friends/reject', api.rejectFriendRequest, name='rejectFriendRequest'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_login_view'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh_view')
]

