from rest_framework import serializers
from .models import Post, Comment

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
    
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        
        fields = "__all__"
