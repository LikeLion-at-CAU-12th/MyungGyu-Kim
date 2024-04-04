from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Student
from posts.models import *
import json

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

@require_http_methods(["POST", "GET"])
def post_list(request):

    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))

        new_post = Post.objects.create(
            writer = body['writer'],
            title = body['title'],
            content = body['content'],
            category = body['category']
        )

        new_post_json = {
            "id" : new_post.id,
            "writer" : new_post.writer,
            "title" : new_post.title,
            "content" : new_post.content,
            "category" : new_post.category
        }

        # response = Post.objects.filter(id=4).delete()
        # # response= new_post.delete()
        # return JsonResponse({
        #     "entity": response
        # })
        return JsonResponse({
            "status" : 200,
            "message" : "게시글 생성 성공",
            "data" : new_post_json
        })
    
    if request.method == "GET":
        post_all = Post.objects.all()

        post_json_all = []

        for post in post_all:
            post_json = {
                "id" : post.id,
                "title" : post.title,
                "writer" : post.writer,
                "content" : post.content,
                "category" : post.category
            }
            
            post_json_all.append(post_json)
        
        return JsonResponse({
            "status" : 200,
            "message" : "게시글 목록 조회 성공",
            "data" : post_json_all
        })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
    
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)

        post_json = {
            "id" : post.id,
            "title" : post.title,
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category
        }

        return JsonResponse({
            "status" : 200,
            "message" : "게시글 조회 성공",
            "data" : post_json
        })
    
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        update_post = get_object_or_404(Post, pk=id)

        update_post.title = body["title"]
        update_post.content = body["content"]
        update_post.category = body["category"]

        update_post.save()

        update_post_json = {
            "id" : update_post.id,
            "title" : update_post.title,
            "writer" : update_post.writer,
            "content" : update_post.content,
            "category" : update_post.category
        }

        return JsonResponse({
            "status" : 200,
            "message" : "게시물 수정 성공",
            "data" : update_post_json
        })

    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=id) 

        delete_post.delete()

        return JsonResponse({
            "status" : 200,
            "message" : "게시글 삭제 성공",
            "data" : None
        })
    
@require_http_methods(["GET"])
def post_comment_list(request):
    