from django.urls import path
from .views import CreateUserView, CustomTokenRefreshView, InviteUser, ChangePasswordView, MyTokenObtainPairView

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='create_user'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('user/change-password/', ChangePasswordView.as_view()),
    
    path('user/department/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/invite/', InviteUser.as_view()),
]
