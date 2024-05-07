from django.db import models

# Create your models here.

class Basemodel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract=True

# Hashtag는 created_at, updated_at의 컬럼이 필요하지 않기 때문에 models.Model 상속
class Hashtag(models.Model):
    tag_no = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="태그명", max_length=30)

    def __str__(self):
        return self.name

# Basemodel을 상속하면서 created_at, updated_at 컬럼을 추가로 상속 받음.
class Post(Basemodel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="제목", max_length=20)
    content = models.TextField(verbose_name="내용")
    writer = models.IntegerField(verbose_name="작성자")
    category = models.CharField(choices=CHOICES, max_length=10)
    # 다:다 관계를 표현할 때는 ManyToManyField() 사용하기
    hashtag = models.ManyToManyField(Hashtag, blank=True, null=True)

# Comment도 작성, 수정 일시를 필요로 하기 때문에 Basemodel 상속 받음.
class Comment(Basemodel):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, verbose_name="포스트ID", on_delete=models.CASCADE)
    writer = models.IntegerField(verbose_name="작성자")
    content = models.TextField(verbose_name="댓글내용")

# 중간 테이블을 직접 만들어서 사용하는 경우 ForeignKey로 참조 설정을 해줘야 함.
# class Post_tag(models.Model):
#     post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
#     tag_no = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

class Image(models.Model):
    post_id = models.ForeignKey(Post, verbose_name="포스트ID", on_delete=models.CASCADE)
    # (1) 저장경로 : MEDIA_ROOT/post/xxx.png
    	#     DB필드 : MEDIA_URL/post/xxx.png' 문자열 저장
    # image = models.ImageField(blank=True, upload_to='post')

    # (2) 저장경로 : MEDIA_ROOT/post/20210901/xxx.png
    	#     DB필드 :  'MEDIA_URL/post/20210901/xxx.png' 문자열 저장
    image = models.ImageField(blank=True, null=True, upload_to='post/%Y%m%d')