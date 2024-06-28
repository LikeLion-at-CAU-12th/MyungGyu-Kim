from django.shortcuts import render
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from config.permissions import IsAuthenticatedAndReturnUser

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
        
from django.contrib.auth  import logout

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)

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
