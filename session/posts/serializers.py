from rest_framework import serializers
from .models import Post, Comment
from rest_framework.exceptions import ValidationError
from PIL import Image
import io

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        # 모든 필드
        fields = "__all__"

        # # 특정 필드 
        # fields = ['writer', 'content']

        # # 필드 제외
        # exclude = ['category']

        # # 수정 불가 필드
        # read_only_field = ['writer']

    # 썸네일 이미지 업로드 시 PNG 형식의 이미지는 업로드할 수 없도록 예외 처리
    def validate_thumbnail(self, value):
        if value and value.content_type == 'image/png':
            raise ValidationError("PNG 형식의 이미지는 업로드할 수 없습니다.")
        elif value:
            img = Image.open(value)
            width, height = img.size
            img_small = img.resize((width//2, height//2))
            img_io = io.BytesIO()
            img_small.save(img_io, format=img.format)
            value.file = img_io
        return value
    
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        
        fields = "__all__"
