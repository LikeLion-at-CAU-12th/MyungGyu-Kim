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
    path('delete/', DeleteView.as_view()),
    path('restore/', RestoreView.as_view()),
]