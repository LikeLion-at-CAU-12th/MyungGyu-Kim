from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Student
from posts.models import *

def hello_world(request) :
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello likelion-12th!!"
        })
    
def index(request):
    return render(request, 'index.html')

def introduction(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공 !', 
            'data' : [
                {
                    "name" : "김명규",
                    "age" : 24,
                    "major" : "CSE"
                },
                {
                    "name" : "이영주",
                    "age" : 24,
                    "major" : "Department of Chinese Language and Literature"
                }
            ]
        },
        json_dumps_params={'ensure_ascii': False})
    
def student_view(request):
    students = Student.objects.all()
    me = students[0]
    my_duo = students[1]
    return render(request, 'student.html', {'me' : me, 'my_duo' : my_duo})

@require_http_methods(["GET"])
def get_post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "writer" : post.writer,
        "category" : post.category,
    }

    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공', 
        'data' : post_detail_json
    })