from django.db import models

# Create your models here.
class Student(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(default="", max_length=30)
    age = models.IntegerField(default=0)
    major = models.CharField(default="", max_length=100)
    github = models.CharField(default="", max_length=200)

class Basemodel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract=True

class Post(Basemodel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="제목", max_length=20)
    content = models.TextField(verbose_name="내용")
    writer = models.CharField(verbose_name="작성자", max_length=10)
    category = models.CharField(choices=CHOICES, max_length=10)

class Comment(Basemodel):
    id = models.AutoField(primary_key=True)
    post_id = models.IntegerField(verbose_name="포스트ID")
    writer = models.CharField(verbose_name="작성자", max_length=10)
    content = models.TextField(verbose_name="댓글내용")