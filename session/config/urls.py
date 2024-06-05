"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from posts.views import *
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# Swagger에서 API 문서화에 포함될 URL 패턴
schema_url_patterns = [
    path('post/', include('posts.urls')),
]

# Swagger UI와 ReDoc 페이지를 생성하기 위한 뷰를 반환함
schema_view = get_schema_view(
    openapi.Info(
        # API 문서의 제목
        title="Post",
        # API의 버전
        default_version='v1',
        # API의 간단한 설명
        description='게시물, 댓글 API',
        # API 사용에 대한 약관 링크 제공
        terms_of_service="https://www.google.com/policies/terms/",
        # API 문서에 포함될 연락처 정보
        contact=openapi.Contact(name="DDing", email="kimmmm099@gmail.com"), 
        # API에 적용된 소프트웨어 라이센스의 정보를 정의함
        license=openapi.License(name="Test License"),
    ),
    # True인 경우 문서가 공개적으로 접근 가능함 == 인증 없이도 문서 확인 가능
    public=True,
    # API 문서에 대한 접근 권한을 설정 (AllowAny == 인증 요구 X. 누구나 접근 가능)
    permission_classes=(AllowAny,),
    # get_schema_view가 문서화할 패턴을 지정
    # schema_url_patterns에 포함된 url만 문서화함
    patterns=schema_url_patterns,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('post/', include('posts.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('account/', include('accounts.urls')),
    path('account/', include('dj_rest_auth.urls')),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)