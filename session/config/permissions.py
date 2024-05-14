from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

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
