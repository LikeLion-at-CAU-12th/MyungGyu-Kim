from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    restore_answer = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'email', 'restore_answer']

    def save(self, request):

        user = User.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            restore_answer = self._validated_data['restore_answer']
        )

        # password 암호화
        user.set_password(self.validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        # data['email'] 로 조회할 경우 없으면 key error가 발생하기 때문에 get() 사용
        email = data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists')
        
        return data

class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        user = User.get_user_or_none_by_username(username=username)

        if user is None:
            raise serializers.ValidationError('user account not exist')
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError('wrong password')
        
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            'user' : user,
            'refresh_token' : refresh_token,
            'access_token' : access_token,
        }

        return data

class OAuthSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, data):
        email = data.get("email", None)
        
        user = User.get_user_or_none_by_email(email=email)
        
        if user is None:
            raise serializers.ValidationError("user account not exists")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data

class RestoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    restore_answer = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'restore_answer']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        restore_answer = data.get('restore_answer', None)

        user = User.get_user_or_none_by_username(username=username)

        if user is None:
            raise serializers.ValidationError('user account not exist')
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError('wrong password')
            
        data = {
            'user' : user,
            'restore_answer' : restore_answer,
        }
        
        return data
