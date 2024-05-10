from rest_framework.permissions import BasePermission, SAFE_METHODS

# secret_key의 값이 같은 경우에만 인가
class HasSecretKey(BasePermission):
    def has_permission(self, request, view):
        secret_key = request.headers.get('Secret-Key')
        return secret_key == 'DDing is good'

# secret_key의 값이 같고 post, comment 객체의 작성자인 경우에만 인가
class IsWriterOrReadOnly(HasSecretKey):
    # HasSecretKey의 has_permission으로 secret_key 값 확인
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    # 요청 body의 writer에 대응되는 값이 객체의 writer와 같은 경우 인가
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.writer == request.data.get('writer')
