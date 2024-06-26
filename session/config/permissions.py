from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# secret_key의 값이 같은 경우에만 인가
class HasSecretKey(BasePermission):
    def has_permission(self, request, view):
        secret_key = request.headers.get('Secret-Key')
        return secret_key == 'DDing is good'

# secret_key의 값이 같고 post, comment 객체의 작성자인 경우에만 인가
class IsWriterOrReadOnly(HasSecretKey):
    
    # 헤더의 토큰에 대응되는 User 객체가 writer와 같은 경우 인가
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated:
                if obj.writer == request.user:
                    return True
                raise PermissionDenied('작성자만 수정 가능합니다')
            raise PermissionDenied('로그인 후 이용해주세요')

class IsAuthenticatedAndReturnUser(IsAuthenticated):
    def has_permission(self, request, view):
        # IsAuthenticated 권한 확인.
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False

        # JWT 토큰으로 사용자 인증.
        jwt_authenticator = JWTAuthentication()
        try:
            # Authorization 헤더에서 토큰 추출.
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return False

            # Bearer 토큰으로 추출.
            token = auth_header.split()[1] if auth_header.startswith('Bearer') else None
            if not token:
                return False

            # 토큰 검증, 사용자 객체를 요청 객체에 설정.
            validated_token = jwt_authenticator.get_validated_token(token)
            request.user = jwt_authenticator.get_user(validated_token)
            return True
        except AuthenticationFailed:
            return False
        except Exception:
            return False    
