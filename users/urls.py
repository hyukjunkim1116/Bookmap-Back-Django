from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("", views.UserView.as_view(), name="user_view"),
    path("kakao/", views.KakaoLogIn.as_view(), name="kakao_login"),
    path(
        "login/",
        views.CustomTokenObtainPairView.as_view(),
        name="custom_token_obtain_pair",
    ),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "<int:uid>/verify/", views.UserSignUpVerifyView.as_view(), name="reset_password"
    ),
    path(
        "verify/<str:uidb64>/<str:token>/",
        views.UserEmailPermitView.as_view(),
        name="user_email_permit",
    ),
    path("find-password/", views.FindPasswordView.as_view(), name="find_password"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("<int:uid>/", views.UserDetailView.as_view(), name="user_detail"),
    path("<int:uid>/image/", views.UserImageView.as_view(), name="user_image"),
]
