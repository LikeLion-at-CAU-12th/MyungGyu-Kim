from django.shortcuts import render
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from config.permissions import IsAuthenticatedAndReturnUser
from django.contrib.auth  import logout
from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured

from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests
from allauth.socialaccount.models import SocialAccount
from .serializers import OAuthSerializer
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view
from dj_rest_auth.registration.serializers import SocialLoginSerializer

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

GOOGLE_SCOPE_USERINFO = get_secret("GOOGLE_SCOPE_USERINFO")
GOOGLE_REDIRECT = get_secret("GOOGLE_REDIRECT")
GOOGLE_CALLBACK_URI = get_secret("GOOGLE_CALLBACK_URI")
GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")
GOOGLE_SECRET = get_secret("GOOGLE_SECRET")

BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'account/google/callback/'

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : serializer.data,
                    "message" : "register success",
                    "token" : {
                        "access token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED
            )
            return res
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            access_token = serializer.validated_data['access_token']
            refresh_token = serializer.validated_data['refresh_token']
            res = Response(
                {
                    'user' : {
                        'id' : user.id,
                        'email' : user.email,
                    },
                    'message' : 'login success',
                    'token' : {
                        'access_token' : access_token,
                        'refresh_tokne' : refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )
            res.set_cookie('access_token', access_token, httponly=True)
            res.set_cookie('refresh_token', refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

def google_login(request):
   scope = GOOGLE_SCOPE_USERINFO        # + "https://www.googleapis.com/auth/drive.readonly" 등 scope 설정 후 자율적으로 추가
   return redirect(f"{GOOGLE_REDIRECT}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    code = request.GET.get("code")      # Query String 으로 넘어옴
    
    # 코드를 담아서 토큰을 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}")
    # 토큰 요청에 대한 응답
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    # 토큰 요청에 대한 응답이 에러가 있으면 에러 발생
    if error is not None:
        raise JSONDecodeError(error)

    # 토큰 요청에 대해 응답이 에러가 없으면 이메일을 요청
    access_token = token_req_json.get('access_token')

    email_response = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    res_status = email_response.status_code

    # 이메일 요청에 대한 응답이 200이 아니면 에러 발생
    if res_status != 200:
        return JsonResponse({'status': 400,'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    email_res_json = email_response.json()
    email = email_res_json.get('email')

    serializer = OAuthSerializer(data={"email": email})

    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
    
        if social_user.provider != "google":
            return JsonResponse({"message": "google login required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        
        return JsonResponse({
            'message': 'login success',
            'user': {
                'id': user.id,
                'email': user.email,
            },
            'token': {
                'access_token': serializer.validated_data['access_token'],
                'refresh_token': serializer.validated_data['refresh_token'],
            }
            }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return JsonResponse({'error message' : 'user not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    # User는 있지만 Social Account가 없는 경우
    except SocialAccount.DoesNotExist:
        return JsonResponse({'error message' : 'social account not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteRestoreView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RestoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            user.restore(serializer.validated_data['restore_answer'])
            return Response({"message": "복구되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        self.check_permissions(request)
        user = request.user
        user = user.soft_delete()
        return Response({"message": "탈퇴되었습니다."}, status=status.HTTP_200_OK)
        
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticatedAndReturnUser()]
        else:
            return []
    
    # delete 요청에서만 permission을 체크하기 위함.
    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, '로그인 후 시도해주세요.', None)
                )
