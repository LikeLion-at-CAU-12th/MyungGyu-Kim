from django.urls import path
from .views import *
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('join/', RegisterView.as_view()),
    path('login/', AuthView.as_view()),
    path('logout/', LogoutView.as_view()),
    
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    path("google/login/finish/", GoogleLogin.as_view(), name="google_login_finish"),
    path("google/join/", google_join, name="google_join"),

    # 토큰
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]